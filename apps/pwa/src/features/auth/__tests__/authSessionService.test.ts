import type {
    Session,
} from "@supabase/supabase-js";
import {
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    getStoredAuthSession,
    mapSupabaseSession,
    onAuthSessionChange,
    signInWithPassword,
    signOut,
} from "@/features/auth/session/authSessionService";
import {
    getSupabaseClient,
} from "@/infrastructure/auth/supabaseClient";
import {
    hasSupabaseBrowserConfiguration,
} from "@/infrastructure/environment/environment";

vi.mock(
    "@/infrastructure/auth/supabaseClient",
    () => ({
        getSupabaseClient:
            vi.fn(),
    }),
);

vi.mock(
    "@/infrastructure/environment/environment",
    () => ({
        hasSupabaseBrowserConfiguration:
            vi.fn(),
    }),
);

const getSupabaseClientMock =
    vi.mocked(
        getSupabaseClient,
    );

const hasSupabaseBrowserConfigurationMock =
    vi.mocked(
        hasSupabaseBrowserConfiguration,
    );

function createSession():
    Session {
    return {
        access_token:
            "access-token",
        refresh_token:
            "refresh-token",
        expires_in:
            3600,
        expires_at:
            123456,
        token_type:
            "bearer",
        user: {
            id:
                "auth-user-id",
            app_metadata: {},
            user_metadata: {},
            aud:
                "authenticated",
            created_at:
                "2026-08-09T00:00:00Z",
            email:
                "admin@example.com",
        },
    };
}

describe(
    "authSessionService",
    () => {
        beforeEach(() => {
            vi.clearAllMocks();

            hasSupabaseBrowserConfigurationMock
                .mockReturnValue(false);
        });

        it(
            "maps a Supabase session to the application session model",
            () => {
                const session =
                    mapSupabaseSession(
                        createSession(),
                    );

                expect(session).toEqual({
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
                });
            },
        );

        it(
            "returns no stored session when Supabase is not configured",
            async () => {
                await expect(
                    getStoredAuthSession(),
                ).resolves.toBeNull();

                expect(
                    getSupabaseClientMock,
                ).not.toHaveBeenCalled();
            },
        );

        it(
            "does not register an authentication listener when Supabase is not configured",
            () => {
                const listener =
                    vi.fn();

                const unsubscribe =
                    onAuthSessionChange(
                        listener,
                    );

                expect(
                    unsubscribe,
                ).toBeTypeOf(
                    "function",
                );

                expect(
                    listener,
                ).not.toHaveBeenCalled();

                expect(
                    getSupabaseClientMock,
                ).not.toHaveBeenCalled();

                unsubscribe();
            },
        );

        it(
            "reports a controlled error when login is attempted without configuration",
            async () => {
                await expect(
                    signInWithPassword({
                        email:
                            "admin@example.com",
                        password:
                            "password",
                    }),
                ).rejects.toMatchObject({
                    code:
                        "authentication.configuration_missing",
                    message:
                        "A autenticação ainda não foi configurada neste ambiente.",
                });

                expect(
                    getSupabaseClientMock,
                ).not.toHaveBeenCalled();
            },
        );

        it(
            "allows sign-out when there is no configured authentication provider",
            async () => {
                await expect(
                    signOut(),
                ).resolves.toBeUndefined();

                expect(
                    getSupabaseClientMock,
                ).not.toHaveBeenCalled();
            },
        );
    },
);