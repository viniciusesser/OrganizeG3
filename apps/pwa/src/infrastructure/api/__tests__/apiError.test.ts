import {
    describe,
    expect,
    it,
} from "vitest";

import {
    ApiError,
    isApiErrorEnvelope,
} from "@/infrastructure/api/apiError";

describe("ApiError", () => {
    it(
        "stores structured API error information",
        () => {
            const error = new ApiError({
                status: 409,
                code: "conflict",
                message: "Resource conflict.",
                details: {
                    field: "name",
                },
                correlationId:
                    "correlation-123",
            });

            expect(error).toBeInstanceOf(
                Error,
            );

            expect(error.name).toBe(
                "ApiError",
            );

            expect(error.status).toBe(
                409,
            );

            expect(error.code).toBe(
                "conflict",
            );

            expect(error.message).toBe(
                "Resource conflict.",
            );

            expect(error.details).toEqual({
                field: "name",
            });

            expect(
                error.correlationId,
            ).toBe("correlation-123");
        },
    );
});

describe(
    "isApiErrorEnvelope",
    () => {
        it(
            "accepts the OrganizeG3 error envelope",
            () => {
                expect(
                    isApiErrorEnvelope({
                        success: false,
                        error: {
                            code: "not_found",
                            message:
                                "Resource not found.",
                            details: null,
                        },
                        meta: {
                            correlation_id:
                                "correlation-123",
                        },
                    }),
                ).toBe(true);
            },
        );

        it(
            "rejects an invalid error envelope",
            () => {
                expect(
                    isApiErrorEnvelope({
                        success: true,
                    }),
                ).toBe(false);

                expect(
                    isApiErrorEnvelope(null),
                ).toBe(false);

                expect(
                    isApiErrorEnvelope(
                        "invalid",
                    ),
                ).toBe(false);
            },
        );
    },
);