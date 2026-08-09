import {
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    apiRequest,
} from "@/infrastructure/api/httpClient";
import {
    authenticatedApiRequest,
    buildAuthenticatedHeaders,
} from "@/infrastructure/api/authenticatedApi";

vi.mock(
    "@/infrastructure/api/httpClient",
    () => ({
        apiRequest: vi.fn(),
    }),
);

const apiRequestMock =
    vi.mocked(apiRequest);

describe(
    "authenticatedApi",
    () => {
        it(
            "builds bearer and tenant headers",
            () => {
                const headers =
                    buildAuthenticatedHeaders({
                        accessToken:
                            "access-token",
                        tenantId:
                            "tenant-id",
                    });

                expect(
                    headers.get(
                        "Authorization",
                    ),
                ).toBe(
                    "Bearer access-token",
                );

                expect(
                    headers.get(
                        "X-Tenant-ID",
                    ),
                ).toBe(
                    "tenant-id",
                );
            },
        );

        it(
            "adds branch context when present",
            () => {
                const headers =
                    buildAuthenticatedHeaders({
                        accessToken:
                            "access-token",
                        tenantId:
                            "tenant-id",
                        branchId:
                            "branch-id",
                    });

                expect(
                    headers.get(
                        "X-Branch-ID",
                    ),
                ).toBe(
                    "branch-id",
                );
            },
        );

        it(
            "delegates the request to the base client",
            async () => {
                apiRequestMock
                    .mockResolvedValue({
                        ok: true,
                    });

                const response =
                    await authenticatedApiRequest<
                        {
                            readonly ok: boolean;
                        }
                    >(
                        "/v1/example",
                        {
                            accessToken:
                                "access-token",
                            tenantId:
                                "tenant-id",
                        },
                        {
                            method: "GET",
                        },
                    );

                expect(response).toEqual({
                    ok: true,
                });

                expect(
                    apiRequestMock,
                ).toHaveBeenCalledTimes(1);

                const [
                    path,
                    options,
                ] =
                    apiRequestMock.mock.calls[0];

                expect(path).toBe(
                    "/v1/example",
                );

                expect(
                    options?.method,
                ).toBe("GET");

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
                    headers.get(
                        "X-Tenant-ID",
                    ),
                ).toBe(
                    "tenant-id",
                );
            },
        );

        it(
            "rejects empty authentication context values",
            () => {
                expect(
                    () =>
                        buildAuthenticatedHeaders({
                            accessToken: "",
                            tenantId:
                                "tenant-id",
                        }),
                ).toThrow();

                expect(
                    () =>
                        buildAuthenticatedHeaders({
                            accessToken:
                                "token",
                            tenantId: "",
                        }),
                ).toThrow();
            },
        );
    },
);