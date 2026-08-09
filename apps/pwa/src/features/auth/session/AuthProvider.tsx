import {
    useCallback,
    useEffect,
    useMemo,
    useReducer,
    useRef,
} from "react";
import type {
    PropsWithChildren,
} from "react";

import {
    getCurrentIdentity,
    listAccessibleTenants,
} from "@/features/auth/api/authApi";
import type {
    AccessibleTenant,
} from "@/features/auth/model/accessibleTenant";
import {
    AuthClientError,
} from "@/features/auth/model/authError";
import type {
    AuthSession,
} from "@/features/auth/model/authSession";
import type {
    AuthenticatedIdentity,
} from "@/features/auth/model/currentIdentity";
import {
    AuthContext,
} from "@/features/auth/session/AuthContext";
import type {
    AuthContextValue,
    AuthStatus,
} from "@/features/auth/session/AuthContext";
import {
    getStoredAuthSession,
    onAuthSessionChange,
    signInWithPassword,
    signOut as signOutSession,
} from "@/features/auth/session/authSessionService";
import type {
    SignInCredentials,
} from "@/features/auth/session/authSessionService";
import {
    clearStoredTenantId,
    readStoredTenantId,
    storeTenantId,
} from "@/features/auth/session/tenantSelectionStorage";

interface AuthState {
    readonly status: AuthStatus;
    readonly session: AuthSession | null;
    readonly tenants: readonly AccessibleTenant[];
    readonly selectedTenant: AccessibleTenant | null;
    readonly identity: AuthenticatedIdentity | null;
    readonly error: AuthClientError | null;
}

type AuthAction =
    | {
        readonly type: "signed_out";
    }
    | {
        readonly type: "resolving_tenants";
        readonly session: AuthSession;
    }
    | {
        readonly type: "no_tenant_access";
        readonly session: AuthSession;
    }
    | {
        readonly type: "tenant_selection_required";
        readonly session: AuthSession;
        readonly tenants: readonly AccessibleTenant[];
    }
    | {
        readonly type: "authenticated";
        readonly session: AuthSession;
        readonly tenants: readonly AccessibleTenant[];
        readonly tenant: AccessibleTenant;
        readonly identity: AuthenticatedIdentity;
    }
    | {
        readonly type: "error";
        readonly session: AuthSession | null;
        readonly tenants: readonly AccessibleTenant[];
        readonly error: AuthClientError;
    };

const INITIAL_STATE: AuthState =
    Object.freeze({
        status: "bootstrapping",
        session: null,
        tenants: [],
        selectedTenant: null,
        identity: null,
        error: null,
    });

function authReducer(
    state: AuthState,
    action: AuthAction,
): AuthState {
    switch (action.type) {
        case "signed_out":
            return {
                status: "signed_out",
                session: null,
                tenants: [],
                selectedTenant: null,
                identity: null,
                error: null,
            };

        case "resolving_tenants":
            return {
                status: "resolving_tenants",
                session: action.session,
                tenants: [],
                selectedTenant: null,
                identity: null,
                error: null,
            };

        case "no_tenant_access":
            return {
                status: "no_tenant_access",
                session: action.session,
                tenants: [],
                selectedTenant: null,
                identity: null,
                error: null,
            };

        case "tenant_selection_required":
            return {
                status:
                    "tenant_selection_required",
                session: action.session,
                tenants: action.tenants,
                selectedTenant: null,
                identity: null,
                error: null,
            };

        case "authenticated":
            return {
                status: "authenticated",
                session: action.session,
                tenants: action.tenants,
                selectedTenant:
                    action.tenant,
                identity: action.identity,
                error: null,
            };

        case "error":
            return {
                ...state,
                status: "error",
                session: action.session,
                tenants: action.tenants,
                selectedTenant: null,
                identity: null,
                error: action.error,
            };
    }
}

function toAuthClientError(
    error: unknown,
): AuthClientError {
    if (
        error instanceof AuthClientError
    ) {
        return error;
    }

    return new AuthClientError({
        code:
            "authentication.context_resolution_failed",
        message:
            "Não foi possível carregar o contexto de acesso.",
        causeMessage:
            error instanceof Error
                ? error.message
                : null,
    });
}

type AuthProviderProps =
    PropsWithChildren;

export function AuthProvider({
    children,
}: AuthProviderProps) {
    const [
        state,
        dispatch,
    ] =
        useReducer(
            authReducer,
            INITIAL_STATE,
        );

    const revisionRef =
        useRef(0);

    const selectedTenantIdRef =
        useRef<string | null>(
            readStoredTenantId(),
        );

    const resolveIdentity =
        useCallback(
            async (
                session: AuthSession,
                tenants:
                    readonly AccessibleTenant[],
                tenant: AccessibleTenant,
                revision: number,
            ): Promise<void> => {
                try {
                    const identity =
                        await getCurrentIdentity({
                            accessToken:
                                session.accessToken,
                            tenantId:
                                tenant.tenantId,
                        });

                    if (
                        revision !==
                        revisionRef.current
                    ) {
                        return;
                    }

                    selectedTenantIdRef.current =
                        tenant.tenantId;

                    storeTenantId(
                        tenant.tenantId,
                    );

                    dispatch({
                        type: "authenticated",
                        session,
                        tenants,
                        tenant,
                        identity,
                    });
                } catch (error) {
                    if (
                        revision !==
                        revisionRef.current
                    ) {
                        return;
                    }

                    dispatch({
                        type: "error",
                        session,
                        tenants,
                        error:
                            toAuthClientError(
                                error,
                            ),
                    });
                }
            },
            [],
        );

    const synchronizeSession =
        useCallback(
            async (
                session: AuthSession | null,
            ): Promise<void> => {
                const revision =
                    revisionRef.current + 1;

                revisionRef.current =
                    revision;

                if (session === null) {
                    selectedTenantIdRef.current =
                        null;

                    clearStoredTenantId();

                    dispatch({
                        type: "signed_out",
                    });

                    return;
                }

                dispatch({
                    type: "resolving_tenants",
                    session,
                });

                try {
                    const tenants =
                        await listAccessibleTenants(
                            session.accessToken,
                        );

                    if (
                        revision !==
                        revisionRef.current
                    ) {
                        return;
                    }

                    if (tenants.length === 0) {
                        selectedTenantIdRef.current =
                            null;

                        clearStoredTenantId();

                        dispatch({
                            type:
                                "no_tenant_access",
                            session,
                        });

                        return;
                    }

                    const storedTenantId =
                        selectedTenantIdRef.current;

                    const storedTenant =
                        storedTenantId === null
                            ? undefined
                            : tenants.find(
                                (tenant) =>
                                    tenant.tenantId ===
                                    storedTenantId,
                            );

                    if (
                        storedTenant !== undefined
                    ) {
                        await resolveIdentity(
                            session,
                            tenants,
                            storedTenant,
                            revision,
                        );

                        return;
                    }

                    if (tenants.length === 1) {
                        const tenant =
                            tenants[0];

                        await resolveIdentity(
                            session,
                            tenants,
                            tenant,
                            revision,
                        );

                        return;
                    }

                    selectedTenantIdRef.current =
                        null;

                    clearStoredTenantId();

                    dispatch({
                        type:
                            "tenant_selection_required",
                        session,
                        tenants,
                    });
                } catch (error) {
                    if (
                        revision !==
                        revisionRef.current
                    ) {
                        return;
                    }

                    dispatch({
                        type: "error",
                        session,
                        tenants: [],
                        error:
                            toAuthClientError(
                                error,
                            ),
                    });
                }
            },
            [
                resolveIdentity,
            ],
        );

    useEffect(
        () => {
            let active = true;

            const unsubscribe =
                onAuthSessionChange(
                    (session) => {
                        if (!active) {
                            return;
                        }

                        void synchronizeSession(
                            session,
                        );
                    },
                );

            void getStoredAuthSession()
                .then(
                    (session) => {
                        if (!active) {
                            return;
                        }

                        return synchronizeSession(
                            session,
                        );
                    },
                )
                .catch(
                    (error: unknown) => {
                        if (!active) {
                            return;
                        }

                        dispatch({
                            type: "error",
                            session: null,
                            tenants: [],
                            error:
                                toAuthClientError(
                                    error,
                                ),
                        });
                    },
                );

            return () => {
                active = false;

                revisionRef.current += 1;

                unsubscribe();
            };
        },
        [
            synchronizeSession,
        ],
    );

    const signIn =
        useCallback(
            async (
                credentials:
                    SignInCredentials,
            ): Promise<void> => {
                const session =
                    await signInWithPassword(
                        credentials,
                    );

                await synchronizeSession(
                    session,
                );
            },
            [
                synchronizeSession,
            ],
        );

    const selectTenant =
        useCallback(
            async (
                tenantId: string,
            ): Promise<void> => {
                const normalizedTenantId =
                    tenantId.trim();

                if (
                    normalizedTenantId.length ===
                    0
                ) {
                    throw new AuthClientError({
                        code:
                            "authentication.invalid_tenant_selection",
                        message:
                            "A empresa selecionada é inválida.",
                    });
                }

                if (state.session === null) {
                    throw new AuthClientError({
                        code:
                            "authentication.session_unavailable",
                        message:
                            "Não existe uma sessão autenticada.",
                    });
                }

                const tenant =
                    state.tenants.find(
                        (candidate) =>
                            candidate.tenantId ===
                            normalizedTenantId,
                    );

                if (tenant === undefined) {
                    throw new AuthClientError({
                        code:
                            "authentication.tenant_unavailable",
                        message:
                            "A empresa selecionada não está disponível.",
                    });
                }

                const revision =
                    revisionRef.current + 1;

                revisionRef.current =
                    revision;

                await resolveIdentity(
                    state.session,
                    state.tenants,
                    tenant,
                    revision,
                );
            },
            [
                resolveIdentity,
                state.session,
                state.tenants,
            ],
        );

    const signOut =
        useCallback(
            async (): Promise<void> => {
                revisionRef.current += 1;

                await signOutSession();

                selectedTenantIdRef.current =
                    null;

                clearStoredTenantId();

                dispatch({
                    type: "signed_out",
                });
            },
            [],
        );

    const retry =
        useCallback(
            async (): Promise<void> => {
                if (state.session !== null) {
                    await synchronizeSession(
                        state.session,
                    );

                    return;
                }

                const session =
                    await getStoredAuthSession();

                await synchronizeSession(
                    session,
                );
            },
            [
                state.session,
                synchronizeSession,
            ],
        );

    const value =
        useMemo<AuthContextValue>(
            () => ({
                status:
                    state.status,
                session:
                    state.session,
                tenants:
                    state.tenants,
                selectedTenant:
                    state.selectedTenant,
                identity:
                    state.identity,
                error:
                    state.error,
                signIn,
                selectTenant,
                signOut,
                retry,
            }),
            [
                retry,
                selectTenant,
                signIn,
                signOut,
                state.error,
                state.identity,
                state.selectedTenant,
                state.session,
                state.status,
                state.tenants,
            ],
        );

    return (
        <AuthContext.Provider
            value={value}
        >
            {children}
        </AuthContext.Provider>
    );
}