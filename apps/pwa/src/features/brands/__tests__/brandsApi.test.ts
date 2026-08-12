import {
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    createBrand,
    deactivateBrand,
    getBrand,
    listBrandPage,
    listBrands,
    reactivateBrand,
    updateBrand,
} from "@/features/brands/api/brandsApi";
import type {
    Brand,
} from "@/features/brands/model/brand";
import {
    authenticatedApiRequest,
} from "@/infrastructure/api/authenticatedApi";
import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";

vi.mock(
    "@/infrastructure/api/authenticatedApi",
    () => ({
        authenticatedApiRequest:
            vi.fn(),
    }),
);

const authenticatedRequestMock =
    vi.mocked(
        authenticatedApiRequest,
    );

const context: AuthenticatedApiContext = {
    accessToken:
        "access-token",
    tenantId:
        "11111111-1111-4111-8111-111111111111",
};

function makeBrand(
    index: number,
): Brand {
    return {
        id:
            `00000000-0000-4000-8000-${String(index).padStart(12, "0")}`,
        tenant_id:
            context.tenantId,
        code:
            `MARCA-${index}`,
        name:
            `Marca ${index}`,
        is_active:
            true,
        created_at:
            "2026-08-10T10:00:00Z",
        updated_at:
            "2026-08-10T10:00:00Z",
    };
}

describe(
    "brandsApi",
    () => {
        beforeEach(() => {
            authenticatedRequestMock
                .mockReset();
        });

        it(
            "lista marcas com filtros normalizados",
            async () => {
                authenticatedRequestMock
                    .mockResolvedValue([]);

                await listBrands(
                    context,
                    {
                        includeInactive:
                            true,
                        search:
                            "  Arauco  ",
                        limit:
                            20,
                        offset:
                            40,
                    },
                );

                expect(
                    authenticatedRequestMock,
                ).toHaveBeenCalledTimes(
                    1,
                );

                const [
                    path,
                    requestContext,
                    options,
                ] =
                    authenticatedRequestMock
                        .mock.calls[0];

                const url =
                    new URL(
                        path,
                        "https://example.test",
                    );

                expect(
                    url.pathname,
                ).toBe(
                    "/api/v1/brands",
                );

                expect(
                    url.searchParams.get(
                        "include_inactive",
                    ),
                ).toBe("true");

                expect(
                    url.searchParams.get(
                        "search",
                    ),
                ).toBe("Arauco");

                expect(
                    url.searchParams.get(
                        "limit",
                    ),
                ).toBe("20");

                expect(
                    url.searchParams.get(
                        "offset",
                    ),
                ).toBe("40");

                expect(
                    requestContext,
                ).toEqual(context);

                expect(
                    options,
                ).toEqual({
                    method:
                        "GET",
                });
            },
        );

        it(
            "não envia pesquisa vazia",
            async () => {
                authenticatedRequestMock
                    .mockResolvedValue([]);

                await listBrands(
                    context,
                    {
                        search:
                            "   ",
                    },
                );

                const [path] =
                    authenticatedRequestMock
                        .mock.calls[0];

                const url =
                    new URL(
                        path,
                        "https://example.test",
                    );

                expect(
                    url.searchParams.has(
                        "search",
                    ),
                ).toBe(false);

                expect(
                    url.searchParams.get(
                        "include_inactive",
                    ),
                ).toBe("false");
            },
        );

        it(
            "calcula a paginação usando um registro adicional",
            async () => {
                const brands =
                    Array.from(
                        {
                            length:
                                21,
                        },
                        (
                            _value,
                            index,
                        ) =>
                            makeBrand(
                                index + 1,
                            ),
                    );

                authenticatedRequestMock
                    .mockResolvedValue(
                        brands,
                    );

                const result =
                    await listBrandPage(
                        context,
                        {
                            limit:
                                20,
                            offset:
                                20,
                        },
                    );

                expect(
                    result.items,
                ).toHaveLength(20);

                expect(
                    result.hasPrevious,
                ).toBe(true);

                expect(
                    result.hasNext,
                ).toBe(true);

                expect(
                    result.offset,
                ).toBe(20);

                expect(
                    result.pageSize,
                ).toBe(20);

                const [path] =
                    authenticatedRequestMock
                        .mock.calls[0];

                const url =
                    new URL(
                        path,
                        "https://example.test",
                    );

                expect(
                    url.searchParams.get(
                        "limit",
                    ),
                ).toBe("21");

                expect(
                    url.searchParams.get(
                        "offset",
                    ),
                ).toBe("20");
            },
        );

        it(
            "consulta uma marca",
            async () => {
                const brand =
                    makeBrand(7);

                authenticatedRequestMock
                    .mockResolvedValue(
                        brand,
                    );

                await expect(
                    getBrand(
                        context,
                        brand.id,
                    ),
                ).resolves.toEqual(
                    brand,
                );

                expect(
                    authenticatedRequestMock,
                ).toHaveBeenCalledWith(
                    `/api/v1/brands/${brand.id}`,
                    context,
                    {
                        method:
                            "GET",
                    },
                );
            },
        );

        it(
            "cadastra uma marca",
            async () => {
                const brand =
                    makeBrand(1);

                authenticatedRequestMock
                    .mockResolvedValue(
                        brand,
                    );

                const payload = {
                    code:
                        "ARAUCO",
                    name:
                        "Arauco",
                };

                await createBrand(
                    context,
                    payload,
                );

                expect(
                    authenticatedRequestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/brands",
                    context,
                    {
                        method:
                            "POST",
                        body:
                            payload,
                    },
                );
            },
        );

        it(
            "atualiza uma marca",
            async () => {
                const brand =
                    makeBrand(4);

                authenticatedRequestMock
                    .mockResolvedValue(
                        brand,
                    );

                const payload = {
                    code:
                        "DURATEX",
                    name:
                        "Dexco Duratex",
                };

                await updateBrand(
                    context,
                    brand.id,
                    payload,
                );

                expect(
                    authenticatedRequestMock,
                ).toHaveBeenCalledWith(
                    `/api/v1/brands/${brand.id}`,
                    context,
                    {
                        method:
                            "PATCH",
                        body:
                            payload,
                    },
                );
            },
        );

        it(
            "inativa uma marca",
            async () => {
                const brand =
                    makeBrand(8);

                authenticatedRequestMock
                    .mockResolvedValue({
                        ...brand,
                        is_active:
                            false,
                    });

                await deactivateBrand(
                    context,
                    brand.id,
                );

                expect(
                    authenticatedRequestMock,
                ).toHaveBeenCalledWith(
                    `/api/v1/brands/${brand.id}/deactivate`,
                    context,
                    {
                        method:
                            "POST",
                    },
                );
            },
        );

        it(
            "reativa uma marca",
            async () => {
                const brand =
                    makeBrand(9);

                authenticatedRequestMock
                    .mockResolvedValue(
                        brand,
                    );

                await reactivateBrand(
                    context,
                    brand.id,
                );

                expect(
                    authenticatedRequestMock,
                ).toHaveBeenCalledWith(
                    `/api/v1/brands/${brand.id}/reactivate`,
                    context,
                    {
                        method:
                            "POST",
                    },
                );
            },
        );
    },
);