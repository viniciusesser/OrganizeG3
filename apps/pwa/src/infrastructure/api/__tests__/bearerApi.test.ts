import {
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    bearerApiRequest,
    buildBearerHeaders,
} from "@/infrastructure/api/bearerApi";
import {
    apiRequest,
} from "@/infrastructure/api/httpClient";

vi.mock(
    "@/infrastructure/api/httpClient",
    () => ({
        apiRequest: vi.fn(),
    }),
);

const apiRequestMock =
    vi.mocked(apiRequest);

describe(
    "bearerApi",
    () => {
        it(
            "builds a bearer authorization header",
            () => {
                const headers =
                    buildBearerHeaders(
                        "access-token",
                    );

                expect(
                    headers.get(
                        "Authorization",
                    ),
                ).toBe(
                    "Bearer access-token",
                );
            },
        );

        it(
            "rejects an empty access token",
            () => {
                expect(
                    () =>
                        buildBearerHeaders(
                            "   ",
                        ),
                ).toThrow(
                    "accessToken não pode ser vazio.",
                );
            },
        );

        it(
            "delegates to the base API client",
            async () => {
                apiRequestMock
                    .mockResolvedValue({
                        ok: true,
                    });

                const result =
                    await bearerApiRequest<{
                        readonly ok: boolean;
                    }>(
                        "/v1/auth/tenants",
                        "access-token",
                        {
                            method: "GET",
                        },
                    );

                expect(result).toEqual({
                    ok: true,
                });

                const [
                    path,
                    options,
                ] =
                    apiRequestMock.mock.calls[0];

                expect(path).toBe(
                    "/v1/auth/tenants",
                );

                const headers =
                    new Headers(
                        options?.headers,
                    );

                expect(
                    headers.get(
                        "Authorization",
                    ),
                ).toBe(
                    "Bearer access-token",
                );

                expect(
                    headers.has(
                        "X-Tenant-ID",
                    ),
                ).toBe(false);
            },
        );
    },
);