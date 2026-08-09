import {
    describe,
    expect,
    it,
} from "vitest";

import {
    createApplicationEnvironment,
    requireSupabaseBrowserConfiguration,
} from "@/infrastructure/environment/environment";

describe(
    "authentication environment",
    () => {
        it(
            "normalizes Supabase browser configuration",
            () => {
                const environment =
                    createApplicationEnvironment({
                        apiBaseUrl:
                            "/api",
                        supabaseUrl:
                            " https://example.supabase.co ",
                        supabaseAnonKey:
                            " public-key ",
                        isDevelopment:
                            true,
                        isProduction:
                            false,
                        mode:
                            "test",
                    });

                expect(
                    environment.supabaseUrl,
                ).toBe(
                    "https://example.supabase.co",
                );

                expect(
                    environment.supabaseAnonKey,
                ).toBe(
                    "public-key",
                );
            },
        );

        it(
            "allows the application to start without Supabase configuration",
            () => {
                const environment =
                    createApplicationEnvironment({
                        apiBaseUrl:
                            "/api",
                        isDevelopment:
                            true,
                        isProduction:
                            false,
                        mode:
                            "test",
                    });

                expect(
                    environment.supabaseUrl,
                ).toBeNull();

                expect(
                    environment.supabaseAnonKey,
                ).toBeNull();
            },
        );

        it(
            "rejects authentication use when Supabase configuration is missing",
            () => {
                const environment =
                    createApplicationEnvironment({
                        apiBaseUrl:
                            "/api",
                        isDevelopment:
                            true,
                        isProduction:
                            false,
                        mode:
                            "test",
                    });

                expect(
                    () =>
                        requireSupabaseBrowserConfiguration(
                            environment,
                        ),
                ).toThrow(
                    "A configuração pública do Supabase não foi definida.",
                );
            },
        );
    },
);