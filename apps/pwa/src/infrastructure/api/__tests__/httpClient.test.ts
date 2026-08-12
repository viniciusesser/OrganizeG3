import {
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    ApiError,
} from "@/infrastructure/api/apiError";
import {
    apiRequest,
} from "@/infrastructure/api/httpClient";

function createJsonResponse(
    body: unknown,
    {
        status = 200,
        correlationId,
    }: {
        readonly status?: number;
        readonly correlationId?: string;
    } = {},
): Response {
    const headers = new Headers({
        "Content-Type":
            "application/json",
    });

    if (
        correlationId !== undefined
    ) {
        headers.set(
            "X-Correlation-ID",
            correlationId,
        );
    }

    return new Response(
        JSON.stringify(body),
        {
            status,
            headers,
        },
    );
}

describe("apiRequest", () => {
    it(
        "performs a JSON GET request",
        async () => {
            const fetchMock =
                vi.fn<typeof fetch>();

            fetchMock.mockResolvedValue(
                createJsonResponse({
                    status: "ok",
                }),
            );

            vi.stubGlobal(
                "fetch",
                fetchMock,
            );

            const result =
                await apiRequest<{
                    readonly status: string;
                }>("/example");

            expect(result).toEqual({
                status: "ok",
            });

            expect(
                fetchMock,
            ).toHaveBeenCalledTimes(1);

            const [
                url,
                requestInit,
            ] = fetchMock.mock.calls[0] ?? [];

            expect(url).toBe(
                "/api/example",
            );

            const headers =
                requestInit?.headers;

            expect(
                headers,
            ).toBeInstanceOf(Headers);

            const requestHeaders =
                headers as Headers;

            expect(
                requestHeaders.get("Accept"),
            ).toBe("application/json");

            expect(
                requestHeaders.get(
                    "X-Correlation-ID",
                ),
            ).not.toBeNull();
        },
    );

    it(
        "does not duplicate the configured API base path",
        async () => {
            const fetchMock =
                vi.fn<typeof fetch>();

            fetchMock.mockResolvedValue(
                createJsonResponse({
                    status: "ok",
                }),
            );

            vi.stubGlobal(
                "fetch",
                fetchMock,
            );

            await apiRequest(
                "/api/v1/example",
            );

            expect(
                fetchMock.mock.calls[0]?.[0],
            ).toBe(
                "/api/v1/example",
            );
        },
    );

    it(
        "can request an endpoint outside the API base path",
        async () => {
            const fetchMock =
                vi.fn<typeof fetch>();

            fetchMock.mockResolvedValue(
                createJsonResponse({
                    status: "ok",
                }),
            );

            vi.stubGlobal(
                "fetch",
                fetchMock,
            );

            await apiRequest(
                "/health",
                {
                    method: "GET",
                    useApiBaseUrl: false,
                },
            );

            const [
                url,
                requestInit,
            ] = fetchMock.mock.calls[0] ?? [];

            expect(url).toBe(
                "/health",
            );

            expect(
                requestInit,
            ).not.toHaveProperty(
                "useApiBaseUrl",
            );
        },
    );

    it(
        "serializes plain objects as JSON",
        async () => {
            const fetchMock =
                vi.fn<typeof fetch>();

            fetchMock.mockResolvedValue(
                createJsonResponse({
                    success: true,
                }),
            );

            vi.stubGlobal(
                "fetch",
                fetchMock,
            );

            await apiRequest(
                "/example",
                {
                    method: "POST",
                    body: {
                        name: "OrganizeG3",
                    },
                },
            );

            const [
                ,
                requestInit,
            ] = fetchMock.mock.calls[0] ?? [];

            const headers =
                requestInit?.headers as Headers;

            expect(
                headers.get(
                    "Content-Type",
                ),
            ).toBe("application/json");

            expect(
                requestInit?.body,
            ).toBe(
                JSON.stringify({
                    name: "OrganizeG3",
                }),
            );
        },
    );

    it(
        "converts a controlled API error into ApiError",
        async () => {
            const fetchMock =
                vi.fn<typeof fetch>();

            fetchMock.mockResolvedValue(
                createJsonResponse(
                    {
                        success: false,
                        error: {
                            code: "conflict",
                            message:
                                "Resource conflict.",
                            details: {
                                field: "name",
                            },
                        },
                        meta: {
                            correlation_id:
                                "body-correlation",
                        },
                    },
                    {
                        status: 409,
                        correlationId:
                            "header-correlation",
                    },
                ),
            );

            vi.stubGlobal(
                "fetch",
                fetchMock,
            );

            let capturedError:
                unknown;

            try {
                await apiRequest(
                    "/example",
                );
            } catch (error) {
                capturedError = error;
            }

            expect(
                capturedError,
            ).toBeInstanceOf(ApiError);

            expect(
                capturedError,
            ).toMatchObject({
                status: 409,
                code: "conflict",
                message:
                    "Resource conflict.",
                correlationId:
                    "header-correlation",
            });
        },
    );

    it(
        "converts network failures into ApiError",
        async () => {
            const fetchMock =
                vi.fn<typeof fetch>();

            fetchMock.mockRejectedValue(
                new Error(
                    "Connection refused",
                ),
            );

            vi.stubGlobal(
                "fetch",
                fetchMock,
            );

            await expect(
                apiRequest("/example"),
            ).rejects.toMatchObject({
                name: "ApiError",
                status: 0,
                code: "network_error",
            });
        },
    );
});