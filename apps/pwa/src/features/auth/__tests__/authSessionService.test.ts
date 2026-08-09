import type {
    Session,
} from "@supabase/supabase-js";
import {
    describe,
    expect,
    it,
} from "vitest";

import {
    mapSupabaseSession,
} from "@/features/auth/session/authSessionService";

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
    },
);