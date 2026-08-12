import {
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    createCompany,
    getCompany,
    updateCompany,
} from "@/features/company/api/companyApi";
import type {
    Company,
} from "@/features/company/model/company";
import {
    ApiError,
} from "@/infrastructure/api/apiError";

const {
    authenticatedApiRequestMock,
} = vi.hoisted(() => ({
    authenticatedApiRequestMock: vi.fn(),
}));

vi.mock(
    "@/infrastructure/api/authenticatedApi",
    () => ({
        authenticatedApiRequest:
            authenticatedApiRequestMock,
    }),
);

const context = {
    accessToken: "access-token",
    tenantId: "tenant-001",
};

const company: Company = {
    id: "company-001",
    tenant_id: "tenant-001",

    trade_name: "Marcenaria Galdino",
    legal_name: "Marcenaria Galdino Ltda.",
    document_number: "12345678000190",
    state_registration: "123456789",

    email: "contato@marcenariagaldino.com.br",
    phone: "18999998888",
    website: "https://marcenariagaldino.com.br",
    logo_path: null,

    street: "Avenida Principal",
    number: "100",
    district: "Centro",
    city: "Rosana",
    state: "SP",
    postal_code: "19273000",

    is_active: true,
};

describe(
    "companyApi",
    () => {
        beforeEach(() => {
            vi.clearAllMocks();
        });

        it(
            "consulta a empresa ativa",
            async () => {
                authenticatedApiRequestMock
                    .mockResolvedValue(company);

                await expect(
                    getCompany(context),
                ).resolves.toEqual(company);

                expect(
                    authenticatedApiRequestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/company",
                    context,
                    {
                        method: "GET",
                    },
                );
            },
        );

        it(
            "retorna nulo quando a empresa ainda não existe",
            async () => {
                authenticatedApiRequestMock
                    .mockRejectedValue(
                        new ApiError({
                            status: 404,
                            code: "resource.not_found",
                            message:
                                "Empresa não encontrada.",
                        }),
                    );

                await expect(
                    getCompany(context),
                ).resolves.toBeNull();
            },
        );

        it(
            "mantém erros diferentes de não encontrado",
            async () => {
                const error = new ApiError({
                    status: 503,
                    code: "service.unavailable",
                    message:
                        "Serviço indisponível.",
                });

                authenticatedApiRequestMock
                    .mockRejectedValue(error);

                await expect(
                    getCompany(context),
                ).rejects.toBe(error);
            },
        );

        it(
            "cadastra a empresa",
            async () => {
                authenticatedApiRequestMock
                    .mockResolvedValue(company);

                const payload = {
                    trade_name:
                        "Marcenaria Galdino",
                    legal_name:
                        "Marcenaria Galdino Ltda.",
                    document_number:
                        "12345678000190",
                    email:
                        "contato@marcenariagaldino.com.br",
                    phone: "18999998888",
                    city: "Rosana",
                    state: "SP",
                };

                await expect(
                    createCompany(
                        context,
                        payload,
                    ),
                ).resolves.toEqual(company);

                expect(
                    authenticatedApiRequestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/company",
                    context,
                    {
                        method: "POST",
                        body: payload,
                    },
                );
            },
        );

        it(
            "atualiza parcialmente a empresa",
            async () => {
                const updatedCompany: Company = {
                    ...company,
                    phone: "18988887777",
                    website: null,
                };

                authenticatedApiRequestMock
                    .mockResolvedValue(
                        updatedCompany,
                    );

                const payload = {
                    phone: "18988887777",
                    website: null,
                };

                await expect(
                    updateCompany(
                        context,
                        payload,
                    ),
                ).resolves.toEqual(
                    updatedCompany,
                );

                expect(
                    authenticatedApiRequestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/company",
                    context,
                    {
                        method: "PATCH",
                        body: payload,
                    },
                );
            },
        );
    },
);