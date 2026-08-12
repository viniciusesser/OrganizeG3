import {
    describe,
    expect,
    it,
} from "vitest";

import {
    createApplicationEnvironment,
    hasSupabaseBrowserConfiguration,
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

                expect(
                    hasSupabaseBrowserConfiguration(
                        environment,
                    ),
                ).toBe(true);
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

                expect(
                    hasSupabaseBrowserConfiguration(
                        environment,
                    ),
                ).toBe(false);
            },
        );

        it(
            "treats a partial Supabase configuration as unavailable",
            () => {
                const environment =
                    createApplicationEnvironment({
                        apiBaseUrl:
                            "/api",
                        supabaseUrl:
                            "https://example.supabase.co",
                        isDevelopment:
                            true,
                        isProduction:
                            false,
                        mode:
                            "test",
                    });

                expect(
                    hasSupabaseBrowserConfiguration(
                        environment,
                    ),
                ).toBe(false);
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