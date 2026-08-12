import {
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    createMaterial,
    deactivateMaterial,
    getMaterial,
    listMaterialPage,
    listMaterials,
    reactivateMaterial,
    updateMaterial,
} from "@/features/materials/api/materialsApi";
import type {
    Material,
} from "@/features/materials/model/material";
import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";
import {
    authenticatedApiRequest,
} from "@/infrastructure/api/authenticatedApi";

vi.mock(
    "@/infrastructure/api/authenticatedApi",
    () => ({
        authenticatedApiRequest:
            vi.fn(),
    }),
);

const authenticatedApiRequestMock =
    vi.mocked(
        authenticatedApiRequest,
    );

const apiContext: AuthenticatedApiContext = {
    accessToken: "access-token",
    tenantId: "tenant-001",
};

const material: Material = {
    id: "material-001",
    tenant_id: "tenant-001",
    code: "MDF-001",
    name: "MDF Gianduia",
    category: "MDF",
    unit: "CHAPA",
    brand_id: "brand-001",
    is_active: true,
    created_at:
        "2026-08-10T10:00:00Z",
    updated_at:
        "2026-08-10T10:00:00Z",
};

describe("materialsApi", () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it(
        "lista materiais com filtros normalizados",
        async () => {
            authenticatedApiRequestMock
                .mockResolvedValue([
                    material,
                ]);

            const result =
                await listMaterials(
                    apiContext,
                    {
                        includeInactive:
                            true,
                        search:
                            "  Gianduia  ",
                        category:
                            "  MDF  ",
                        brandId:
                            "brand-001",
                        limit: 25,
                        offset: 50,
                    },
                );

            expect(result).toEqual([
                material,
            ]);

            expect(
                authenticatedApiRequestMock,
            ).toHaveBeenCalledWith(
                "/api/v1/materials?include_inactive=true&search=Gianduia&category=MDF&brand_id=brand-001&limit=25&offset=50",
                apiContext,
                {
                    method: "GET",
                },
            );
        },
    );

    it(
        "ignora filtros textuais vazios",
        async () => {
            authenticatedApiRequestMock
                .mockResolvedValue([
                    material,
                ]);

            await listMaterials(
                apiContext,
                {
                    search: "   ",
                    category: "   ",
                    brandId: null,
                    limit: 20,
                    offset: 0,
                },
            );

            expect(
                authenticatedApiRequestMock,
            ).toHaveBeenCalledWith(
                "/api/v1/materials?limit=20&offset=0",
                apiContext,
                {
                    method: "GET",
                },
            );
        },
    );

    it(
        "carrega uma linha adicional para detectar a próxima página",
        async () => {
            const materials =
                Array.from(
                    {
                        length: 21,
                    },
                    (_, index) => ({
                        ...material,
                        id:
                            `material-${index + 1}`,
                        code:
                            `MDF-${String(
                                index + 1,
                            ).padStart(
                                3,
                                "0",
                            )}`,
                    }),
                );

            authenticatedApiRequestMock
                .mockResolvedValue(
                    materials,
                );

            const result =
                await listMaterialPage(
                    apiContext,
                    {
                        limit: 20,
                        offset: 0,
                    },
                );

            expect(
                result.items,
            ).toHaveLength(20);

            expect(result).toEqual({
                items:
                    materials.slice(
                        0,
                        20,
                    ),
                hasPrevious: false,
                hasNext: true,
                offset: 0,
                pageSize: 20,
            });

            expect(
                authenticatedApiRequestMock,
            ).toHaveBeenCalledWith(
                "/api/v1/materials?limit=21&offset=0",
                apiContext,
                {
                    method: "GET",
                },
            );
        },
    );

    it(
        "consulta um material pelo identificador",
        async () => {
            authenticatedApiRequestMock
                .mockResolvedValue(
                    material,
                );

            const result =
                await getMaterial(
                    apiContext,
                    material.id,
                );

            expect(result).toEqual(
                material,
            );

            expect(
                authenticatedApiRequestMock,
            ).toHaveBeenCalledWith(
                `/api/v1/materials/${material.id}`,
                apiContext,
                {
                    method: "GET",
                },
            );
        },
    );

    it(
        "cadastra um material",
        async () => {
            const payload = {
                code: "MDF-001",
                name: "MDF Gianduia",
                category: "MDF",
                unit: "CHAPA",
                brand_id:
                    "brand-001",
            };

            authenticatedApiRequestMock
                .mockResolvedValue(
                    material,
                );

            const result =
                await createMaterial(
                    apiContext,
                    payload,
                );

            expect(result).toEqual(
                material,
            );

            expect(
                authenticatedApiRequestMock,
            ).toHaveBeenCalledWith(
                "/api/v1/materials",
                apiContext,
                {
                    method: "POST",
                    body: payload,
                },
            );
        },
    );

    it(
        "atualiza um material",
        async () => {
            const payload = {
                code: "MDF-001",
                name:
                    "MDF Gianduia Atualizado",
                category: "MDF",
                unit: "CHAPA",
                brand_id:
                    "brand-001",
            };

            authenticatedApiRequestMock
                .mockResolvedValue({
                    ...material,
                    ...payload,
                });

            await updateMaterial(
                apiContext,
                material.id,
                payload,
            );

            expect(
                authenticatedApiRequestMock,
            ).toHaveBeenCalledWith(
                `/api/v1/materials/${material.id}`,
                apiContext,
                {
                    method: "PATCH",
                    body: payload,
                },
            );
        },
    );

    it(
        "inativa um material",
        async () => {
            authenticatedApiRequestMock
                .mockResolvedValue({
                    ...material,
                    is_active: false,
                });

            await deactivateMaterial(
                apiContext,
                material.id,
            );

            expect(
                authenticatedApiRequestMock,
            ).toHaveBeenCalledWith(
                `/api/v1/materials/${material.id}/deactivate`,
                apiContext,
                {
                    method: "POST",
                },
            );
        },
    );

    it(
        "reativa um material",
        async () => {
            authenticatedApiRequestMock
                .mockResolvedValue(
                    material,
                );

            await reactivateMaterial(
                apiContext,
                material.id,
            );

            expect(
                authenticatedApiRequestMock,
            ).toHaveBeenCalledWith(
                `/api/v1/materials/${material.id}/reactivate`,
                apiContext,
                {
                    method: "POST",
                },
            );
        },
    );
});