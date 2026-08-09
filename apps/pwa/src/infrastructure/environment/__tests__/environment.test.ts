import {
    describe,
    expect,
    it,
} from "vitest";

import {
    createApplicationEnvironment,
} from "@/infrastructure/environment/environment";

describe(
    "createApplicationEnvironment",
    () => {
        it(
            "uses /api when API base URL is absent",
            () => {
                const result =
                    createApplicationEnvironment({
                        isDevelopment: true,
                        isProduction: false,
                        mode: "development",
                    });

                expect(result).toEqual({
                    apiBaseUrl: "/api",
                    supabaseUrl: null,
                    supabaseAnonKey: null,
                    isDevelopment: true,
                    isProduction: false,
                    mode: "development",
                });
            },
        );

        it(
            "uses /api when API base URL is blank",
            () => {
                const result =
                    createApplicationEnvironment({
                        apiBaseUrl: "   ",
                        isDevelopment: true,
                        isProduction: false,
                        mode: "development",
                    });

                expect(
                    result.apiBaseUrl,
                ).toBe("/api");
            },
        );

        it(
            "removes trailing slashes from API base URL",
            () => {
                const result =
                    createApplicationEnvironment({
                        apiBaseUrl:
                            "http://localhost:8000///",
                        isDevelopment: true,
                        isProduction: false,
                        mode: "development",
                    });

                expect(
                    result.apiBaseUrl,
                ).toBe(
                    "http://localhost:8000",
                );
            },
        );

        it(
            "returns an immutable environment object",
            () => {
                const result =
                    createApplicationEnvironment({
                        apiBaseUrl: "/api",
                        isDevelopment: true,
                        isProduction: false,
                        mode: "development",
                    });

                expect(
                    Object.isFrozen(result),
                ).toBe(true);
            },
        );
    },
);