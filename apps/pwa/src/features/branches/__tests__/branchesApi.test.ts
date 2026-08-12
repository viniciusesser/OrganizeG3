import {
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    createBranch,
    deactivateBranch,
    getBranch,
    listBranches,
    reactivateBranch,
    updateBranch,
} from "@/features/branches/api/branchesApi";
import type {
    Branch,
    CreateBranchPayload,
    UpdateBranchPayload,
} from "@/features/branches/model/branch";
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

const requestMock =
    vi.mocked(
        authenticatedApiRequest,
    );

const apiContext = {
    accessToken:
        "access-token",
    tenantId:
        "tenant-001",
};

const branch: Branch = {
    id:
        "branch-001",
    tenant_id:
        "tenant-001",

    code:
        "MAT-01",
    name:
        "Matriz Rosana",

    legal_name:
        "Marcenaria Galdino Ltda.",
    document_number:
        "12345678000190",
    state_registration:
        "123456789",

    email:
        "contato@marcenariagaldino.com.br",
    phone:
        "18999998888",
    website:
        "https://marcenariagaldino.com.br",

    street:
        "Avenida Principal",
    number:
        "100",
    district:
        "Centro",
    city:
        "Rosana",
    state:
        "SP",
    postal_code:
        "19273000",

    is_headquarters:
        true,
    is_active:
        true,

    created_at:
        "2026-08-11T10:00:00Z",
    updated_at:
        "2026-08-11T10:00:00Z",
};

describe(
    "branchesApi",
    () => {
        beforeEach(() => {
            vi.clearAllMocks();

            requestMock
                .mockResolvedValue(
                    branch,
                );
        });

        it(
            "lista filiais sem filtros",
            async () => {
                requestMock
                    .mockResolvedValue([
                        branch,
                    ]);

                await expect(
                    listBranches(
                        apiContext,
                    ),
                ).resolves.toEqual([
                    branch,
                ]);

                expect(
                    requestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/branches",
                    apiContext,
                    {
                        method:
                            "GET",
                    },
                );
            },
        );

        it(
            "lista filiais com filtros normalizados",
            async () => {
                requestMock
                    .mockResolvedValue([
                        branch,
                    ]);

                await listBranches(
                    apiContext,
                    {
                        includeInactive:
                            true,
                        search:
                            "  Rosana  ",
                        isHeadquarters:
                            false,
                        limit:
                            25,
                        offset:
                            50,
                    },
                );

                expect(
                    requestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/branches?include_inactive=true&search=Rosana&is_headquarters=false&limit=25&offset=50",
                    apiContext,
                    {
                        method:
                            "GET",
                    },
                );
            },
        );

        it(
            "ignora uma pesquisa vazia",
            async () => {
                requestMock
                    .mockResolvedValue([]);

                await listBranches(
                    apiContext,
                    {
                        search:
                            "   ",
                    },
                );

                expect(
                    requestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/branches",
                    apiContext,
                    {
                        method:
                            "GET",
                    },
                );
            },
        );

        it(
            "consulta uma filial por identificador",
            async () => {
                await expect(
                    getBranch(
                        apiContext,
                        branch.id,
                    ),
                ).resolves.toEqual(
                    branch,
                );

                expect(
                    requestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/branches/branch-001",
                    apiContext,
                    {
                        method:
                            "GET",
                    },
                );
            },
        );

        it(
            "cadastra uma filial",
            async () => {
                const payload:
                    CreateBranchPayload = {
                    code:
                        "MAT-01",
                    name:
                        "Matriz Rosana",
                    legal_name:
                        "Marcenaria Galdino Ltda.",
                    city:
                        "Rosana",
                    state:
                        "SP",
                    is_headquarters:
                        true,
                };

                await expect(
                    createBranch(
                        apiContext,
                        payload,
                    ),
                ).resolves.toEqual(
                    branch,
                );

                expect(
                    requestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/branches",
                    apiContext,
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
            "atualiza parcialmente uma filial",
            async () => {
                const payload:
                    UpdateBranchPayload = {
                    name:
                        "Matriz Rosana Atualizada",
                    phone:
                        "18988887777",
                    website:
                        null,
                };

                await updateBranch(
                    apiContext,
                    branch.id,
                    payload,
                );

                expect(
                    requestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/branches/branch-001",
                    apiContext,
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
            "inativa e reativa uma filial",
            async () => {
                await deactivateBranch(
                    apiContext,
                    branch.id,
                );

                expect(
                    requestMock,
                ).toHaveBeenLastCalledWith(
                    "/api/v1/branches/branch-001/deactivate",
                    apiContext,
                    {
                        method:
                            "POST",
                    },
                );

                await reactivateBranch(
                    apiContext,
                    branch.id,
                );

                expect(
                    requestMock,
                ).toHaveBeenLastCalledWith(
                    "/api/v1/branches/branch-001/reactivate",
                    apiContext,
                    {
                        method:
                            "POST",
                    },
                );
            },
        );
    },
);