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
                            "https://api.example.com///",
                        isDevelopment: false,
                        isProduction: true,
                        mode: "production",
                    });

                expect(
                    result.apiBaseUrl,
                ).toBe(
                    "https://api.example.com",
                );
            },
        );

        it(
            "returns an immutable environment object",
            () => {
                const result =
                    createApplicationEnvironment({
                        isDevelopment: false,
                        isProduction: true,
                        mode: "production",
                    });

                expect(
                    Object.isFrozen(result),
                ).toBe(true);
            },
        );
    },
);