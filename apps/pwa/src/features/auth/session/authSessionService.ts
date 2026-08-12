import type {
    AuthChangeEvent,
    Session,
} from "@supabase/supabase-js";

import {
    AuthClientError,
} from "@/features/auth/model/authError";
import type {
    AuthSession,
} from "@/features/auth/model/authSession";
import {
    getSupabaseClient,
} from "@/infrastructure/auth/supabaseClient";
import {
    hasSupabaseBrowserConfiguration,
} from "@/infrastructure/environment/environment";

export interface SignInCredentials {
    readonly email: string;
    readonly password: string;
}

export type AuthSessionListener = (
    session: AuthSession | null,
    event: AuthChangeEvent,
) => void;

function normalizeCredential(
    value: string,
    fieldName: string,
): string {
    const normalized =
        value.trim();

    if (normalized.length === 0) {
        throw new AuthClientError({
            code:
                "authentication.invalid_credentials_input",
            message:
                `${fieldName} é obrigatório.`,
        });
    }

    return normalized;
}

function requireAuthenticationConfiguration():
    void {
    if (
        hasSupabaseBrowserConfiguration()
    ) {
        return;
    }

    throw new AuthClientError({
        code:
            "authentication.configuration_missing",
        message:
            "A autenticação ainda não foi configurada neste ambiente.",
        causeMessage:
            "As variáveis públicas do Supabase não foram definidas.",
    });
}

export function mapSupabaseSession(
    session: Session,
): AuthSession {
    return Object.freeze({
        accessToken:
            session.access_token,
        refreshToken:
            session.refresh_token,
        expiresAt:
            session.expires_at ?? null,
        authUserId:
            session.user.id,
        email:
            session.user.email ?? null,
    });
}

export async function signInWithPassword(
    credentials: SignInCredentials,
): Promise<AuthSession> {
    const email =
        normalizeCredential(
            credentials.email,
            "E-mail",
        );

    const password =
        normalizeCredential(
            credentials.password,
            "Senha",
        );

    requireAuthenticationConfiguration();

    const client =
        getSupabaseClient();

    const {
        data,
        error,
    } =
        await client.auth
            .signInWithPassword({
                email,
                password,
            });

    if (error !== null) {
        throw new AuthClientError({
            code:
                "authentication.sign_in_failed",
            message:
                "Não foi possível autenticar o usuário.",
            causeMessage:
                error.message,
        });
    }

    if (data.session === null) {
        throw new AuthClientError({
            code:
                "authentication.session_unavailable",
            message:
                "A autenticação não retornou uma sessão válida.",
        });
    }

    return mapSupabaseSession(
        data.session,
    );
}

export async function getStoredAuthSession():
    Promise<AuthSession | null> {
    if (
        !hasSupabaseBrowserConfiguration()
    ) {
        return null;
    }

    const client =
        getSupabaseClient();

    const {
        data,
        error,
    } =
        await client.auth.getSession();

    if (error !== null) {
        throw new AuthClientError({
            code:
                "authentication.session_read_failed",
            message:
                "Não foi possível recuperar a sessão.",
            causeMessage:
                error.message,
        });
    }

    if (data.session === null) {
        return null;
    }

    return mapSupabaseSession(
        data.session,
    );
}

export function onAuthSessionChange(
    listener: AuthSessionListener,
): () => void {
    if (
        !hasSupabaseBrowserConfiguration()
    ) {
        return () => undefined;
    }

    const client =
        getSupabaseClient();

    const {
        data,
    } =
        client.auth.onAuthStateChange(
            (
                event,
                session,
            ) => {
                listener(
                    session === null
                        ? null
                        : mapSupabaseSession(
                            session,
                        ),
                    event,
                );
            },
        );

    return () => {
        data.subscription.unsubscribe();
    };
}

export async function signOut():
    Promise<void> {
    if (
        !hasSupabaseBrowserConfiguration()
    ) {
        return;
    }

    const client =
        getSupabaseClient();

    const {
        error,
    } =
        await client.auth.signOut();

    if (error !== null) {
        throw new AuthClientError({
            code:
                "authentication.sign_out_failed",
            message:
                "Não foi possível encerrar a sessão.",
            causeMessage:
                error.message,
        });
    }
}