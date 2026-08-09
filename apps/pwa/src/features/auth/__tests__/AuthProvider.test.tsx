import {
    fireEvent,
    render,
    screen,
    waitFor,
} from "@testing-library/react";
import {
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    getCurrentIdentity,
    listAccessibleTenants,
} from "@/features/auth/api/authApi";
import type {
    AccessibleTenant,
} from "@/features/auth/model/accessibleTenant";
import type {
    AuthSession,
} from "@/features/auth/model/authSession";
import type {
    AuthenticatedIdentity,
} from "@/features/auth/model/currentIdentity";
import {
    AuthProvider,
} from "@/features/auth/session/AuthProvider";
import {
    getStoredAuthSession,
    onAuthSessionChange,
    signInWithPassword,
    signOut,
} from "@/features/auth/session/authSessionService";
import {
    useAuth,
} from "@/features/auth/session/useAuth";

vi.mock(
    "@/features/auth/api/authApi",
    () => ({
        getCurrentIdentity:
            vi.fn(),
        listAccessibleTenants:
            vi.fn(),
    }),
);

vi.mock(
    "@/features/auth/session/authSessionService",
    () => ({
        getStoredAuthSession:
            vi.fn(),
        onAuthSessionChange:
            vi.fn(),
        signInWithPassword:
            vi.fn(),
        signOut:
            vi.fn(),
    }),
);

const getCurrentIdentityMock =
    vi.mocked(
        getCurrentIdentity,
    );

const listAccessibleTenantsMock =
    vi.mocked(
        listAccessibleTenants,
    );

const getStoredAuthSessionMock =
    vi.mocked(
        getStoredAuthSession,
    );

const onAuthSessionChangeMock =
    vi.mocked(
        onAuthSessionChange,
    );

const signInWithPasswordMock =
    vi.mocked(
        signInWithPassword,
    );

const signOutMock =
    vi.mocked(
        signOut,
    );

const SESSION: AuthSession = {
    accessToken:
        "access-token",
    refreshToken:
        "refresh-token",
    expiresAt:
        123456,
    authUserId:
        "auth-user-id",
    email:
        "admin@example.com",
};

const TENANT_A: AccessibleTenant = {
    tenantId:
        "tenant-a",
    membershipId:
        "membership-a",
    name:
        "Empresa A",
};

const TENANT_B: AccessibleTenant = {
    tenantId:
        "tenant-b",
    membershipId:
        "membership-b",
    name:
        "Empresa B",
};

const IDENTITY: AuthenticatedIdentity = {
    tenantId:
        "tenant-a",
    userId:
        "user-id",
    membershipId:
        "membership-a",
    authUserId:
        "auth-user-id",
    email:
        "admin@example.com",
    displayName:
        "Administrador",
    permissions:
        new Set([
            "customers.read",
        ]),
};

function AuthProbe() {
    const auth =
        useAuth();

    return (
        <div>
            <span data-testid="status">
                {auth.status}
            </span>

            <span data-testid="tenant-count">
                {auth.tenants.length}
            </span>

            <span data-testid="display-name">
                {auth.identity
                    ?.displayName ?? ""}
            </span>

            <button
                type="button"
                onClick={() => {
                    void auth.selectTenant(
                        TENANT_A.tenantId,
                    );
                }}
            >
                Selecionar empresa A
            </button>
        </div>
    );
}

describe(
    "AuthProvider",
    () => {
        beforeEach(() => {
            vi.clearAllMocks();

            window.localStorage.clear();

            onAuthSessionChangeMock
                .mockReturnValue(
                    () => undefined,
                );

            signInWithPasswordMock
                .mockResolvedValue(
                    SESSION,
                );

            signOutMock
                .mockResolvedValue(
                    undefined,
                );
        });

        it(
            "resolves to signed out when there is no stored session",
            async () => {
                getStoredAuthSessionMock
                    .mockResolvedValue(
                        null,
                    );

                render(
                    <AuthProvider>
                        <AuthProbe />
                    </AuthProvider>,
                );

                await waitFor(
                    () => {
                        expect(
                            screen.getByTestId(
                                "status",
                            ),
                        ).toHaveTextContent(
                            "signed_out",
                        );
                    },
                );
            },
        );

        it(
            "automatically selects the only accessible tenant",
            async () => {
                getStoredAuthSessionMock
                    .mockResolvedValue(
                        SESSION,
                    );

                listAccessibleTenantsMock
                    .mockResolvedValue([
                        TENANT_A,
                    ]);

                getCurrentIdentityMock
                    .mockResolvedValue(
                        IDENTITY,
                    );

                render(
                    <AuthProvider>
                        <AuthProbe />
                    </AuthProvider>,
                );

                await waitFor(
                    () => {
                        expect(
                            screen.getByTestId(
                                "status",
                            ),
                        ).toHaveTextContent(
                            "authenticated",
                        );
                    },
                );

                expect(
                    getCurrentIdentityMock,
                ).toHaveBeenCalledWith({
                    accessToken:
                        SESSION.accessToken,
                    tenantId:
                        TENANT_A.tenantId,
                });

                expect(
                    screen.getByTestId(
                        "display-name",
                    ),
                ).toHaveTextContent(
                    "Administrador",
                );
            },
        );

        it(
            "requires selection when multiple tenants are available",
            async () => {
                getStoredAuthSessionMock
                    .mockResolvedValue(
                        SESSION,
                    );

                listAccessibleTenantsMock
                    .mockResolvedValue([
                        TENANT_A,
                        TENANT_B,
                    ]);

                getCurrentIdentityMock
                    .mockResolvedValue(
                        IDENTITY,
                    );

                render(
                    <AuthProvider>
                        <AuthProbe />
                    </AuthProvider>,
                );

                await waitFor(
                    () => {
                        expect(
                            screen.getByTestId(
                                "status",
                            ),
                        ).toHaveTextContent(
                            "tenant_selection_required",
                        );
                    },
                );

                expect(
                    screen.getByTestId(
                        "tenant-count",
                    ),
                ).toHaveTextContent(
                    "2",
                );

                expect(
                    getCurrentIdentityMock,
                ).not.toHaveBeenCalled();

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Selecionar empresa A",
                        },
                    ),
                );

                await waitFor(
                    () => {
                        expect(
                            screen.getByTestId(
                                "status",
                            ),
                        ).toHaveTextContent(
                            "authenticated",
                        );
                    },
                );

                expect(
                    getCurrentIdentityMock,
                ).toHaveBeenCalledWith({
                    accessToken:
                        SESSION.accessToken,
                    tenantId:
                        TENANT_A.tenantId,
                });
            },
        );

        it(
            "reports no tenant access when the membership list is empty",
            async () => {
                getStoredAuthSessionMock
                    .mockResolvedValue(
                        SESSION,
                    );

                listAccessibleTenantsMock
                    .mockResolvedValue([]);

                render(
                    <AuthProvider>
                        <AuthProbe />
                    </AuthProvider>,
                );

                await waitFor(
                    () => {
                        expect(
                            screen.getByTestId(
                                "status",
                            ),
                        ).toHaveTextContent(
                            "no_tenant_access",
                        );
                    },
                );
            },
        );
    },
);