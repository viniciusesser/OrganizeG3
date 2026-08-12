import {
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    createSupplier,
    deactivateSupplier,
    getSupplier,
    listSupplierPage,
    listSuppliers,
    reactivateSupplier,
    updateSupplier,
} from "@/features/suppliers/api/suppliersApi";
import type {
    Supplier,
} from "@/features/suppliers/model/supplier";
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

const supplier: Supplier = {
    id: "supplier-001",
    tenant_id: "tenant-001",
    code: "FOR-001",
    name: "Madeiras Brasil",
    trade_name: "Madeiras Brasil",
    legal_name:
        "Madeiras Brasil Ltda.",
    document_number:
        "12345678000190",
    state_registration:
        "123456789",
    email:
        "contato@madeirasbrasil.com.br",
    invoice_email:
        "faturamento@madeirasbrasil.com.br",
    phone: "18999998888",
    secondary_phone:
        "1833334444",
    website:
        "https://madeirasbrasil.com.br",
    contact_name:
        "Antônio Silva",
    postal_code: "19200000",
    street: "Avenida Brasil",
    number: "100",
    district: "Centro",
    city: "Rosana",
    state: "SP",
    is_active: true,
    created_at:
        "2026-08-10T10:00:00Z",
    updated_at:
        "2026-08-10T10:00:00Z",
};

describe("suppliersApi", () => {
    beforeEach(() => {
        authenticatedApiRequestMock
            .mockReset();
    });

    it("lista fornecedores com a paginação padrão", async () => {
        authenticatedApiRequestMock
            .mockResolvedValue([
                supplier,
            ]);

        const result =
            await listSuppliers(
                apiContext,
            );

        expect(result).toEqual([
            supplier,
        ]);

        expect(
            authenticatedApiRequestMock,
        ).toHaveBeenCalledWith(
            "/api/v1/suppliers?limit=20&offset=0",
            apiContext,
            {
                method: "GET",
            },
        );
    });

    it("normaliza a pesquisa e inclui fornecedores inativos", async () => {
        authenticatedApiRequestMock
            .mockResolvedValue([
                supplier,
            ]);

        await listSuppliers(
            apiContext,
            {
                includeInactive: true,
                search:
                    "  Madeiras & Cia  ",
                limit: 10,
                offset: 20,
            },
        );

        expect(
            authenticatedApiRequestMock,
        ).toHaveBeenCalledWith(
            "/api/v1/suppliers?include_inactive=true&search=Madeiras+%26+Cia&limit=10&offset=20",
            apiContext,
            {
                method: "GET",
            },
        );
    });

    it("ignora uma pesquisa composta somente por espaços", async () => {
        authenticatedApiRequestMock
            .mockResolvedValue([]);

        await listSuppliers(
            apiContext,
            {
                search: "   ",
                limit: 5,
                offset: 0,
            },
        );

        expect(
            authenticatedApiRequestMock,
        ).toHaveBeenCalledWith(
            "/api/v1/suppliers?limit=5&offset=0",
            apiContext,
            {
                method: "GET",
            },
        );
    });

    it("monta uma página e identifica a próxima página", async () => {
        const secondSupplier: Supplier = {
            ...supplier,
            id: "supplier-002",
            code: "FOR-002",
            name: "Ferragens Brasil",
        };

        const thirdSupplier: Supplier = {
            ...supplier,
            id: "supplier-003",
            code: "FOR-003",
            name: "MDF Brasil",
        };

        authenticatedApiRequestMock
            .mockResolvedValue([
                supplier,
                secondSupplier,
                thirdSupplier,
            ]);

        const result =
            await listSupplierPage(
                apiContext,
                {
                    limit: 2,
                    offset: 2,
                },
            );

        expect(result).toEqual({
            items: [
                supplier,
                secondSupplier,
            ],
            hasPrevious: true,
            hasNext: true,
            offset: 2,
            pageSize: 2,
        });

        expect(
            authenticatedApiRequestMock,
        ).toHaveBeenCalledWith(
            "/api/v1/suppliers?limit=3&offset=2",
            apiContext,
            {
                method: "GET",
            },
        );
    });

    it("monta a última página sem indicar próxima página", async () => {
        authenticatedApiRequestMock
            .mockResolvedValue([
                supplier,
            ]);

        const result =
            await listSupplierPage(
                apiContext,
                {
                    limit: 20,
                    offset: 0,
                },
            );

        expect(result).toEqual({
            items: [
                supplier,
            ],
            hasPrevious: false,
            hasNext: false,
            offset: 0,
            pageSize: 20,
        });

        expect(
            authenticatedApiRequestMock,
        ).toHaveBeenCalledWith(
            "/api/v1/suppliers?limit=21&offset=0",
            apiContext,
            {
                method: "GET",
            },
        );
    });

    it("consulta um fornecedor pelo identificador", async () => {
        authenticatedApiRequestMock
            .mockResolvedValue(
                supplier,
            );

        const result =
            await getSupplier(
                apiContext,
                supplier.id,
            );

        expect(result).toEqual(
            supplier,
        );

        expect(
            authenticatedApiRequestMock,
        ).toHaveBeenCalledWith(
            `/api/v1/suppliers/${supplier.id}`,
            apiContext,
            {
                method: "GET",
            },
        );
    });

    it("cadastra um fornecedor", async () => {
        const payload = {
            code: "FOR-001",
            name: "Madeiras Brasil",
            email:
                "contato@madeirasbrasil.com.br",
        };

        authenticatedApiRequestMock
            .mockResolvedValue(
                supplier,
            );

        const result =
            await createSupplier(
                apiContext,
                payload,
            );

        expect(result).toEqual(
            supplier,
        );

        expect(
            authenticatedApiRequestMock,
        ).toHaveBeenCalledWith(
            "/api/v1/suppliers",
            apiContext,
            {
                method: "POST",
                body: payload,
            },
        );
    });

    it("atualiza um fornecedor", async () => {
        const payload = {
            name:
                "Madeiras Brasil Atualizada",
            contact_name:
                "Maria Silva",
        };

        authenticatedApiRequestMock
            .mockResolvedValue({
                ...supplier,
                ...payload,
            });

        await updateSupplier(
            apiContext,
            supplier.id,
            payload,
        );

        expect(
            authenticatedApiRequestMock,
        ).toHaveBeenCalledWith(
            `/api/v1/suppliers/${supplier.id}`,
            apiContext,
            {
                method: "PATCH",
                body: payload,
            },
        );
    });

    it("inativa um fornecedor", async () => {
        authenticatedApiRequestMock
            .mockResolvedValue({
                ...supplier,
                is_active: false,
            });

        await deactivateSupplier(
            apiContext,
            supplier.id,
        );

        expect(
            authenticatedApiRequestMock,
        ).toHaveBeenCalledWith(
            `/api/v1/suppliers/${supplier.id}/deactivate`,
            apiContext,
            {
                method: "POST",
            },
        );
    });

    it("reativa um fornecedor", async () => {
        authenticatedApiRequestMock
            .mockResolvedValue(
                supplier,
            );

        await reactivateSupplier(
            apiContext,
            supplier.id,
        );

        expect(
            authenticatedApiRequestMock,
        ).toHaveBeenCalledWith(
            `/api/v1/suppliers/${supplier.id}/reactivate`,
            apiContext,
            {
                method: "POST",
            },
        );
    });
});