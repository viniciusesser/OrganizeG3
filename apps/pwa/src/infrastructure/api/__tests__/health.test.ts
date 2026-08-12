import {
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    getApiHealth,
} from "@/infrastructure/api/health";

describe("getApiHealth", () => {
    it(
        "requests the API health endpoint outside the API prefix",
        async () => {
            const fetchMock =
                vi.fn<typeof fetch>();

            fetchMock.mockResolvedValue(
                new Response(
                    JSON.stringify({
                        status: "healthy",
                        service:
                            "organizeg3-api",
                        version: "0.1.0",
                    }),
                    {
                        status: 200,
                        headers: {
                            "Content-Type":
                                "application/json",
                        },
                    },
                ),
            );

            vi.stubGlobal(
                "fetch",
                fetchMock,
            );

            const health =
                await getApiHealth();

            expect(health).toEqual({
                status: "healthy",
                service:
                    "organizeg3-api",
                version: "0.1.0",
            });

            expect(
                fetchMock,
            ).toHaveBeenCalledTimes(1);

            expect(
                fetchMock.mock.calls[0]?.[0],
            ).toBe("/health");
        },
    );
});