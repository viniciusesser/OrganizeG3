import {
    cleanup,
    fireEvent,
    render,
    screen,
    waitFor,
    within,
} from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import {
    afterEach,
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    BrandsRoute,
} from "@/features/brands/routes/BrandsRoute";

const {
    createBrandMock,
    deactivateBrandMock,
    hasPermissionMock,
    listBrandPageMock,
    reactivateBrandMock,
    updateBrandMock,
    useAuthMock,
} = vi.hoisted(
    () => ({
        createBrandMock:
            vi.fn(),
        deactivateBrandMock:
            vi.fn(),
        hasPermissionMock:
            vi.fn(),
        listBrandPageMock:
            vi.fn(),
        reactivateBrandMock:
            vi.fn(),
        updateBrandMock:
            vi.fn(),
        useAuthMock:
            vi.fn(),
    }),
);

vi.mock(
    "@/features/auth/model/currentIdentity",
    () => ({
        hasPermission:
            hasPermissionMock,
    }),
);

vi.mock(
    "@/features/auth/session/useAuth",
    () => ({
        useAuth:
            useAuthMock,
    }),
);

vi.mock(
    "@/features/brands/api/brandsApi",
    () => ({
        createBrand:
            createBrandMock,
        deactivateBrand:
            deactivateBrandMock,
        listBrandPage:
            listBrandPageMock,
        reactivateBrand:
            reactivateBrandMock,
        updateBrand:
            updateBrandMock,
    }),
);

const brand = {
    id:
        "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
    tenant_id:
        "11111111-1111-4111-8111-111111111111",
    code:
        "ARAUCO",
    name:
        "Arauco",
    is_active:
        true,
    created_at:
        "2026-08-10T10:00:00Z",
    updated_at:
        "2026-08-10T10:00:00Z",
} as const;

const activePage = {
    items: [
        brand,
    ],
    hasPrevious:
        false,
    hasNext:
        false,
    offset:
        0,
    pageSize:
        20,
};

function configureAuthenticatedUser(): void {
    useAuthMock.mockReturnValue({
        identity: {
            id:
                "user-001",
        },
        session: {
            accessToken:
                "access-token",
        },
        selectedTenant: {
            tenantId:
                "11111111-1111-4111-8111-111111111111",
        },
    });

    hasPermissionMock
        .mockReturnValue(true);
}

describe(
    "BrandsRoute",
    () => {
        beforeEach(() => {
            vi.clearAllMocks();

            configureAuthenticatedUser();

            listBrandPageMock
                .mockResolvedValue(
                    activePage,
                );

            createBrandMock
                .mockResolvedValue(
                    brand,
                );

            updateBrandMock
                .mockResolvedValue(
                    brand,
                );

            deactivateBrandMock
                .mockResolvedValue({
                    ...brand,
                    is_active:
                        false,
                });

            reactivateBrandMock
                .mockResolvedValue(
                    brand,
                );
        });

        afterEach(() => {
            cleanup();
        });

        it(
            "carrega as marcas da empresa ativa",
            async () => {
                render(
                    <BrandsRoute />,
                );

                expect(
                    await screen.findByText(
                        "Arauco",
                    ),
                ).toBeInTheDocument();

                expect(
                    listBrandPageMock,
                ).toHaveBeenCalledWith(
                    {
                        accessToken:
                            "access-token",
                        tenantId:
                            brand.tenant_id,
                    },
                    {
                        includeInactive:
                            false,
                        search:
                            "",
                        limit:
                            20,
                        offset:
                            0,
                    },
                );
            },
        );

        it(
            "não consulta marcas sem permissão de leitura",
            async () => {
                hasPermissionMock
                    .mockReturnValue(
                        false,
                    );

                render(
                    <BrandsRoute />,
                );

                expect(
                    screen.getByText(
                        "Acesso restrito",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByText(
                        "Você não possui permissão para visualizar marcas.",
                    ),
                ).toBeInTheDocument();

                await waitFor(() => {
                    expect(
                        listBrandPageMock,
                    ).not.toHaveBeenCalled();
                });
            },
        );

        it(
            "informa quando o contexto autenticado está indisponível",
            () => {
                useAuthMock
                    .mockReturnValue({
                        identity: {
                            id:
                                "user-001",
                        },
                        session:
                            null,
                        selectedTenant:
                            null,
                    });

                render(
                    <BrandsRoute />,
                );

                expect(
                    screen.getByText(
                        "Contexto indisponível",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByText(
                        "Não foi possível identificar a sessão e a empresa ativa.",
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "pesquisa marcas e inclui registros inativos",
            async () => {
                render(
                    <BrandsRoute />,
                );

                await screen.findByText(
                    "Arauco",
                );

                fireEvent.change(
                    screen.getByLabelText(
                        "Pesquisar marcas",
                    ),
                    {
                        target: {
                            value:
                                "  Duratex  ",
                        },
                    },
                );

                fireEvent.click(
                    screen.getByLabelText(
                        "Exibir inativas",
                    ),
                );

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Pesquisar",
                        },
                    ),
                );

                await waitFor(() => {
                    expect(
                        listBrandPageMock,
                    ).toHaveBeenLastCalledWith(
                        {
                            accessToken:
                                "access-token",
                            tenantId:
                                brand.tenant_id,
                        },
                        {
                            includeInactive:
                                true,
                            search:
                                "Duratex",
                            limit:
                                20,
                            offset:
                                0,
                        },
                    );
                });
            },
        );

        it(
            "cadastra uma marca normalizando o código",
            async () => {
                render(
                    <BrandsRoute />,
                );

                await screen.findByText(
                    "Arauco",
                );

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Nova marca",
                        },
                    ),
                );

                const dialog =
                    screen.getByRole(
                        "dialog",
                        {
                            name:
                                "Nova marca",
                        },
                    );

                fireEvent.change(
                    within(
                        dialog,
                    ).getByLabelText(
                        "Código da marca *",
                    ),
                    {
                        target: {
                            value:
                                " duratex ",
                        },
                    },
                );

                fireEvent.change(
                    within(
                        dialog,
                    ).getByLabelText(
                        "Nome da marca *",
                    ),
                    {
                        target: {
                            value:
                                "  Duratex  ",
                        },
                    },
                );

                fireEvent.click(
                    within(
                        dialog,
                    ).getByRole(
                        "button",
                        {
                            name:
                                "Salvar marca",
                        },
                    ),
                );

                await waitFor(() => {
                    expect(
                        createBrandMock,
                    ).toHaveBeenCalledWith(
                        {
                            accessToken:
                                "access-token",
                            tenantId:
                                brand.tenant_id,
                        },
                        {
                            code:
                                "DURATEX",
                            name:
                                "Duratex",
                        },
                    );
                });

                expect(
                    await screen.findByText(
                        "Marca cadastrada com sucesso.",
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "atualiza uma marca",
            async () => {
                render(
                    <BrandsRoute />,
                );

                await screen.findByText(
                    "Arauco",
                );

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Editar",
                        },
                    ),
                );

                const dialog =
                    screen.getByRole(
                        "dialog",
                        {
                            name:
                                "Editar marca",
                        },
                    );

                fireEvent.change(
                    within(
                        dialog,
                    ).getByLabelText(
                        "Nome da marca *",
                    ),
                    {
                        target: {
                            value:
                                "Arauco Brasil",
                        },
                    },
                );

                fireEvent.click(
                    within(
                        dialog,
                    ).getByRole(
                        "button",
                        {
                            name:
                                "Salvar alterações",
                        },
                    ),
                );

                await waitFor(() => {
                    expect(
                        updateBrandMock,
                    ).toHaveBeenCalledWith(
                        {
                            accessToken:
                                "access-token",
                            tenantId:
                                brand.tenant_id,
                        },
                        brand.id,
                        {
                            code:
                                "ARAUCO",
                            name:
                                "Arauco Brasil",
                        },
                    );
                });

                expect(
                    await screen.findByText(
                        "Marca atualizada com sucesso.",
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "inativa uma marca após confirmação",
            async () => {
                render(
                    <BrandsRoute />,
                );

                await screen.findByText(
                    "Arauco",
                );

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Inativar",
                        },
                    ),
                );

                expect(
                    screen.getByText(
                        "Inativar marca?",
                    ),
                ).toBeInTheDocument();

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Inativar marca",
                        },
                    ),
                );

                await waitFor(() => {
                    expect(
                        deactivateBrandMock,
                    ).toHaveBeenCalledWith(
                        {
                            accessToken:
                                "access-token",
                            tenantId:
                                brand.tenant_id,
                        },
                        brand.id,
                    );
                });

                expect(
                    await screen.findByText(
                        "Marca inativada com sucesso.",
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "reativa uma marca inativa",
            async () => {
                listBrandPageMock
                    .mockResolvedValue({
                        ...activePage,
                        items: [
                            {
                                ...brand,
                                is_active:
                                    false,
                            },
                        ],
                    });

                render(
                    <BrandsRoute />,
                );

                await screen.findByText(
                    "Arauco",
                );

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Reativar",
                        },
                    ),
                );

                await waitFor(() => {
                    expect(
                        reactivateBrandMock,
                    ).toHaveBeenCalledWith(
                        {
                            accessToken:
                                "access-token",
                            tenantId:
                                brand.tenant_id,
                        },
                        brand.id,
                    );
                });

                expect(
                    await screen.findByText(
                        "Marca reativada com sucesso.",
                    ),
                ).toBeInTheDocument();
            },
        );
    },
);