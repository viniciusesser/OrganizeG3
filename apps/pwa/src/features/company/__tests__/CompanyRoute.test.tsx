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
    CompanyRoute,
} from "@/features/company/routes/CompanyRoute";
import {
    ApiError,
} from "@/infrastructure/api/apiError";

const {
    createCompanyMock,
    getCompanyMock,
    hasPermissionMock,
    updateCompanyMock,
    useAuthMock,
} = vi.hoisted(() => ({
    createCompanyMock: vi.fn(),
    getCompanyMock: vi.fn(),
    hasPermissionMock: vi.fn(),
    updateCompanyMock: vi.fn(),
    useAuthMock: vi.fn(),
}));

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
    "@/features/company/api/companyApi",
    () => ({
        createCompany:
            createCompanyMock,
        getCompany:
            getCompanyMock,
        updateCompany:
            updateCompanyMock,
    }),
);

const company = {
    id:
        "company-001",
    tenant_id:
        "tenant-001",
    trade_name:
        "Marcenaria Galdino",
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
    logo_path:
        "/logos/marcenaria-galdino.png",
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
    is_active:
        true,
    created_at:
        "2026-08-10T10:00:00Z",
    updated_at:
        "2026-08-10T10:00:00Z",
} as const;

const apiContext = {
    accessToken:
        "access-token",
    tenantId:
        "tenant-001",
};

function configureAuthenticatedUser(): void {
    useAuthMock.mockReturnValue({
        identity: {
            id:
                "user-001",
        },
        session: {
            accessToken:
                apiContext.accessToken,
        },
        selectedTenant: {
            tenantId:
                apiContext.tenantId,
        },
    });

    hasPermissionMock.mockReturnValue(true);
}

describe(
    "CompanyRoute",
    () => {
        beforeEach(() => {
            vi.clearAllMocks();

            configureAuthenticatedUser();

            getCompanyMock
                .mockResolvedValue(company);

            createCompanyMock
                .mockResolvedValue(company);

            updateCompanyMock
                .mockResolvedValue(company);
        });

        afterEach(() => {
            cleanup();
        });

        it(
            "carrega os dados da empresa ativa",
            async () => {
                render(
                    <CompanyRoute />,
                );

                expect(
                    await screen.findByText(
                        "Marcenaria Galdino",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByText(
                        "Marcenaria Galdino Ltda.",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByText(
                        "12345678000190",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByText(
                        "contato@marcenariagaldino.com.br",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByText(
                        "Avenida Principal, 100 · Centro - Rosana - SP · 19273000",
                    ),
                ).toBeInTheDocument();

                expect(
                    getCompanyMock,
                ).toHaveBeenCalledWith(
                    apiContext,
                );
            },
        );

        it(
            "não consulta a empresa sem permissão de leitura",
            async () => {
                hasPermissionMock
                    .mockReturnValue(false);

                render(
                    <CompanyRoute />,
                );

                expect(
                    screen.getByText(
                        "Acesso restrito",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByText(
                        "Você não possui permissão para visualizar os dados da empresa.",
                    ),
                ).toBeInTheDocument();

                await waitFor(() => {
                    expect(
                        getCompanyMock,
                    ).not.toHaveBeenCalled();
                });
            },
        );

        it(
            "informa quando a sessão ou a empresa ativa está indisponível",
            () => {
                useAuthMock.mockReturnValue({
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
                    <CompanyRoute />,
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

                expect(
                    getCompanyMock,
                ).not.toHaveBeenCalled();
            },
        );

        it(
            "informa quando a empresa ainda não foi cadastrada",
            async () => {
                getCompanyMock
                    .mockResolvedValue(null);

                render(
                    <CompanyRoute />,
                );

                expect(
                    await screen.findByText(
                        "Empresa ainda não cadastrada",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByText(
                        "Cadastre as informações principais da empresa para completar a configuração.",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getAllByRole(
                        "button",
                        {
                            name:
                                "Cadastrar empresa",
                        },
                    ),
                ).toHaveLength(2);
            },
        );

        it(
            "exibe erro da API e permite repetir a consulta",
            async () => {
                getCompanyMock
                    .mockRejectedValueOnce(
                        new ApiError({
                            status:
                                503,
                            code:
                                "service.unavailable",
                            message:
                                "Serviço temporariamente indisponível.",
                        }),
                    )
                    .mockResolvedValue(
                        company,
                    );

                render(
                    <CompanyRoute />,
                );

                expect(
                    await screen.findByText(
                        "Serviço temporariamente indisponível.",
                    ),
                ).toBeInTheDocument();

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Tentar novamente",
                        },
                    ),
                );

                expect(
                    await screen.findByText(
                        "Marcenaria Galdino",
                    ),
                ).toBeInTheDocument();

                expect(
                    getCompanyMock,
                ).toHaveBeenCalledTimes(2);
            },
        );

        it(
            "valida os campos obrigatórios antes do cadastro",
            async () => {
                getCompanyMock
                    .mockResolvedValue(null);

                render(
                    <CompanyRoute />,
                );

                await screen.findByText(
                    "Empresa ainda não cadastrada",
                );

                fireEvent.click(
                    screen.getAllByRole(
                        "button",
                        {
                            name:
                                "Cadastrar empresa",
                        },
                    )[0],
                );

                const dialog =
                    screen.getByRole(
                        "dialog",
                        {
                            name:
                                "Cadastrar empresa",
                        },
                    );

                fireEvent.click(
                    within(dialog)
                        .getByRole(
                            "button",
                            {
                                name:
                                    "Cadastrar empresa",
                            },
                        ),
                );

                expect(
                    await within(dialog)
                        .findByText(
                            "Informe o nome fantasia da empresa.",
                        ),
                ).toBeInTheDocument();

                expect(
                    createCompanyMock,
                ).not.toHaveBeenCalled();
            },
        );

        it(
            "valida a sigla do estado antes do cadastro",
            async () => {
                getCompanyMock
                    .mockResolvedValue(null);

                render(
                    <CompanyRoute />,
                );

                await screen.findByText(
                    "Empresa ainda não cadastrada",
                );

                fireEvent.click(
                    screen.getAllByRole(
                        "button",
                        {
                            name:
                                "Cadastrar empresa",
                        },
                    )[0],
                );

                const dialog =
                    screen.getByRole(
                        "dialog",
                        {
                            name:
                                "Cadastrar empresa",
                        },
                    );

                fireEvent.change(
                    within(dialog)
                        .getByLabelText(
                            "Nome fantasia *",
                        ),
                    {
                        target: {
                            value:
                                "Marcenaria Galdino",
                        },
                    },
                );

                fireEvent.change(
                    within(dialog)
                        .getByLabelText(
                            "Estado (UF)",
                        ),
                    {
                        target: {
                            value:
                                "S",
                        },
                    },
                );

                fireEvent.click(
                    within(dialog)
                        .getByRole(
                            "button",
                            {
                                name:
                                    "Cadastrar empresa",
                            },
                        ),
                );

                expect(
                    await within(dialog)
                        .findByText(
                            "Informe a sigla UF com dois caracteres.",
                        ),
                ).toBeInTheDocument();

                expect(
                    createCompanyMock,
                ).not.toHaveBeenCalled();
            },
        );

        it(
            "cadastra a empresa normalizando os valores",
            async () => {
                getCompanyMock
                    .mockResolvedValue(null);

                render(
                    <CompanyRoute />,
                );

                await screen.findByText(
                    "Empresa ainda não cadastrada",
                );

                fireEvent.click(
                    screen.getAllByRole(
                        "button",
                        {
                            name:
                                "Cadastrar empresa",
                        },
                    )[0],
                );

                const dialog =
                    screen.getByRole(
                        "dialog",
                        {
                            name:
                                "Cadastrar empresa",
                        },
                    );

                fireEvent.change(
                    within(dialog)
                        .getByLabelText(
                            "Nome fantasia *",
                        ),
                    {
                        target: {
                            value:
                                "  Marcenaria Galdino  ",
                        },
                    },
                );

                fireEvent.change(
                    within(dialog)
                        .getByLabelText(
                            "Razão social",
                        ),
                    {
                        target: {
                            value:
                                "  Marcenaria Galdino Ltda.  ",
                        },
                    },
                );

                fireEvent.change(
                    within(dialog)
                        .getByLabelText(
                            "Email",
                        ),
                    {
                        target: {
                            value:
                                "  contato@marcenariagaldino.com.br  ",
                        },
                    },
                );

                fireEvent.change(
                    within(dialog)
                        .getByLabelText(
                            "Cidade",
                        ),
                    {
                        target: {
                            value:
                                "  Rosana  ",
                        },
                    },
                );

                fireEvent.change(
                    within(dialog)
                        .getByLabelText(
                            "Estado (UF)",
                        ),
                    {
                        target: {
                            value:
                                "sp",
                        },
                    },
                );

                fireEvent.click(
                    within(dialog)
                        .getByRole(
                            "button",
                            {
                                name:
                                    "Cadastrar empresa",
                            },
                        ),
                );

                await waitFor(() => {
                    expect(
                        createCompanyMock,
                    ).toHaveBeenCalledWith(
                        apiContext,
                        {
                            trade_name:
                                "Marcenaria Galdino",
                            legal_name:
                                "Marcenaria Galdino Ltda.",
                            document_number:
                                null,
                            state_registration:
                                null,
                            email:
                                "contato@marcenariagaldino.com.br",
                            phone:
                                null,
                            website:
                                null,
                            logo_path:
                                null,
                            street:
                                null,
                            number:
                                null,
                            district:
                                null,
                            city:
                                "Rosana",
                            state:
                                "SP",
                            postal_code:
                                null,
                        },
                    );
                });

                expect(
                    await screen.findByText(
                        "Empresa cadastrada com sucesso.",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.queryByRole(
                        "dialog",
                        {
                            name:
                                "Cadastrar empresa",
                        },
                    ),
                ).not.toBeInTheDocument();
            },
        );

        it(
            "atualiza os dados da empresa",
            async () => {
                updateCompanyMock
                    .mockResolvedValue({
                        ...company,
                        trade_name:
                            "Marcenaria Galdino Atualizada",
                    });

                render(
                    <CompanyRoute />,
                );

                await screen.findByText(
                    "Marcenaria Galdino",
                );

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Editar empresa",
                        },
                    ),
                );

                const dialog =
                    screen.getByRole(
                        "dialog",
                        {
                            name:
                                "Editar empresa",
                        },
                    );

                fireEvent.change(
                    within(dialog)
                        .getByLabelText(
                            "Nome fantasia *",
                        ),
                    {
                        target: {
                            value:
                                "  Marcenaria Galdino Atualizada  ",
                        },
                    },
                );

                fireEvent.click(
                    within(dialog)
                        .getByRole(
                            "button",
                            {
                                name:
                                    "Salvar alterações",
                            },
                        ),
                );

                await waitFor(() => {
                    expect(
                        updateCompanyMock,
                    ).toHaveBeenCalledWith(
                        apiContext,
                        {
                            trade_name:
                                "Marcenaria Galdino Atualizada",
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
                            logo_path:
                                "/logos/marcenaria-galdino.png",
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
                        },
                    );
                });

                expect(
                    await screen.findByText(
                        "Empresa atualizada com sucesso.",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByText(
                        "Marcenaria Galdino Atualizada",
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "exibe o erro retornado durante o cadastro",
            async () => {
                getCompanyMock
                    .mockResolvedValue(null);

                createCompanyMock
                    .mockRejectedValue(
                        new ApiError({
                            status:
                                409,
                            code:
                                "company.conflict",
                            message:
                                "A empresa já está cadastrada.",
                        }),
                    );

                render(
                    <CompanyRoute />,
                );

                await screen.findByText(
                    "Empresa ainda não cadastrada",
                );

                fireEvent.click(
                    screen.getAllByRole(
                        "button",
                        {
                            name:
                                "Cadastrar empresa",
                        },
                    )[0],
                );

                const dialog =
                    screen.getByRole(
                        "dialog",
                        {
                            name:
                                "Cadastrar empresa",
                        },
                    );

                fireEvent.change(
                    within(dialog)
                        .getByLabelText(
                            "Nome fantasia *",
                        ),
                    {
                        target: {
                            value:
                                "Marcenaria Galdino",
                        },
                    },
                );

                fireEvent.click(
                    within(dialog)
                        .getByRole(
                            "button",
                            {
                                name:
                                    "Cadastrar empresa",
                            },
                        ),
                );

                expect(
                    await within(dialog)
                        .findByText(
                            "A empresa já está cadastrada.",
                        ),
                ).toBeInTheDocument();

                expect(
                    dialog,
                ).toBeInTheDocument();
            },
        );
    },
);