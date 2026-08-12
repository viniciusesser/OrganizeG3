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
    ServicesRoute,
} from "@/features/services/routes/ServicesRoute";

const {
    createServiceMock,
    deactivateServiceMock,
    hasPermissionMock,
    listServicePageMock,
    reactivateServiceMock,
    updateServiceMock,
    useAuthMock,
} = vi.hoisted(
    () => ({
        createServiceMock:
            vi.fn(),
        deactivateServiceMock:
            vi.fn(),
        hasPermissionMock:
            vi.fn(),
        listServicePageMock:
            vi.fn(),
        reactivateServiceMock:
            vi.fn(),
        updateServiceMock:
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
    "@/features/services/api/servicesApi",
    () => ({
        createService:
            createServiceMock,
        deactivateService:
            deactivateServiceMock,
        listServicePage:
            listServicePageMock,
        reactivateService:
            reactivateServiceMock,
        updateService:
            updateServiceMock,
    }),
);

const service = {
    id: "service-001",
    tenant_id: "tenant-001",
    code: "CORTE",
    name: "Corte de MDF",
    category: "Usinagem",
    unit: "HORA",
    execution_mode:
        "INTERNAL",
    estimated_duration_minutes:
        60,
    is_active: true,
    created_at:
        "2026-08-10T10:00:00Z",
    updated_at:
        "2026-08-10T10:00:00Z",
} as const;

const activePage = {
    items: [service],
    hasPrevious: false,
    hasNext: false,
    offset: 0,
    pageSize: 20,
};

function configureAuthenticatedUser(): void {
    useAuthMock.mockReturnValue({
        identity: {
            id: "user-001",
        },
        session: {
            accessToken:
                "access-token",
        },
        selectedTenant: {
            tenantId:
                "tenant-001",
        },
    });

    hasPermissionMock
        .mockReturnValue(true);
}

describe(
    "ServicesRoute",
    () => {
        beforeEach(
            () => {
                vi.clearAllMocks();

                configureAuthenticatedUser();

                listServicePageMock
                    .mockResolvedValue(
                        activePage,
                    );

                createServiceMock
                    .mockResolvedValue(
                        service,
                    );

                updateServiceMock
                    .mockResolvedValue(
                        service,
                    );

                deactivateServiceMock
                    .mockResolvedValue({
                        ...service,
                        is_active: false,
                    });

                reactivateServiceMock
                    .mockResolvedValue(
                        service,
                    );
            },
        );

        afterEach(
            () => {
                cleanup();
            },
        );

        it(
            "carrega os serviços da empresa ativa",
            async () => {
                render(
                    <ServicesRoute />,
                );

                expect(
                    await screen.findByText(
                        "Corte de MDF",
                    ),
                ).toBeInTheDocument();

                expect(
                    listServicePageMock,
                ).toHaveBeenCalledWith(
                    {
                        accessToken:
                            "access-token",
                        tenantId:
                            "tenant-001",
                    },
                    {
                        includeInactive:
                            false,
                        search: "",
                        category: "",
                        executionMode:
                            null,
                        limit: 20,
                        offset: 0,
                    },
                );
            },
        );

        it(
            "não consulta serviços sem permissão de leitura",
            async () => {
                hasPermissionMock
                    .mockReturnValue(
                        false,
                    );

                render(
                    <ServicesRoute />,
                );

                expect(
                    screen.getByText(
                        "Acesso restrito",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByText(
                        "Você não possui permissão para visualizar serviços.",
                    ),
                ).toBeInTheDocument();

                await waitFor(
                    () => {
                        expect(
                            listServicePageMock,
                        ).not
                            .toHaveBeenCalled();
                    },
                );
            },
        );

        it(
            "informa quando a sessão ou a empresa ativa está indisponível",
            () => {
                useAuthMock
                    .mockReturnValue({
                        identity: {
                            id:
                                "user-001",
                        },
                        session: null,
                        selectedTenant:
                            null,
                    });

                render(
                    <ServicesRoute />,
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
            "pesquisa serviços usando categoria, execução e status",
            async () => {
                render(
                    <ServicesRoute />,
                );

                await screen.findByText(
                    "Corte de MDF",
                );

                fireEvent.change(
                    screen.getByLabelText(
                        "Pesquisar serviços",
                    ),
                    {
                        target: {
                            value:
                                "  Corte  ",
                        },
                    },
                );

                fireEvent.change(
                    screen.getByLabelText(
                        "Categoria",
                    ),
                    {
                        target: {
                            value:
                                "  Usinagem  ",
                        },
                    },
                );

                fireEvent.change(
                    screen.getByLabelText(
                        "Modo de execução",
                    ),
                    {
                        target: {
                            value:
                                "INTERNAL",
                        },
                    },
                );

                fireEvent.click(
                    screen.getByLabelText(
                        "Exibir inativos",
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

                await waitFor(
                    () => {
                        expect(
                            listServicePageMock,
                        ).toHaveBeenLastCalledWith(
                            {
                                accessToken:
                                    "access-token",
                                tenantId:
                                    "tenant-001",
                            },
                            {
                                includeInactive:
                                    true,
                                search:
                                    "Corte",
                                category:
                                    "Usinagem",
                                executionMode:
                                    "INTERNAL",
                                limit: 20,
                                offset: 0,
                            },
                        );
                    },
                );
            },
        );

        it(
            "cadastra um serviço",
            async () => {
                render(
                    <ServicesRoute />,
                );

                await screen.findByText(
                    "Corte de MDF",
                );

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Novo serviço",
                        },
                    ),
                );

                const dialog =
                    screen.getByRole(
                        "dialog",
                        {
                            name:
                                "Novo serviço",
                        },
                    );

                fireEvent.change(
                    within(
                        dialog,
                    ).getByLabelText(
                        "Código do serviço *",
                    ),
                    {
                        target: {
                            value:
                                "instalacao",
                        },
                    },
                );

                fireEvent.change(
                    within(
                        dialog,
                    ).getByLabelText(
                        "Nome do serviço *",
                    ),
                    {
                        target: {
                            value:
                                "Instalação de móveis",
                        },
                    },
                );

                fireEvent.change(
                    within(
                        dialog,
                    ).getByLabelText(
                        "Categoria *",
                    ),
                    {
                        target: {
                            value:
                                "Montagem",
                        },
                    },
                );

                fireEvent.change(
                    within(
                        dialog,
                    ).getByLabelText(
                        "Unidade *",
                    ),
                    {
                        target: {
                            value:
                                "diária",
                        },
                    },
                );

                fireEvent.change(
                    within(
                        dialog,
                    ).getByLabelText(
                        "Modo de execução *",
                    ),
                    {
                        target: {
                            value:
                                "BOTH",
                        },
                    },
                );

                fireEvent.change(
                    within(
                        dialog,
                    ).getByLabelText(
                        "Duração estimada (minutos)",
                    ),
                    {
                        target: {
                            value:
                                "480",
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
                                "Salvar serviço",
                        },
                    ),
                );

                await waitFor(
                    () => {
                        expect(
                            createServiceMock,
                        ).toHaveBeenCalledWith(
                            {
                                accessToken:
                                    "access-token",
                                tenantId:
                                    "tenant-001",
                            },
                            {
                                code:
                                    "INSTALACAO",
                                name:
                                    "Instalação de móveis",
                                category:
                                    "Montagem",
                                unit:
                                    "DIÁRIA",
                                execution_mode:
                                    "BOTH",
                                estimated_duration_minutes:
                                    480,
                            },
                        );
                    },
                );

                expect(
                    await screen.findByText(
                        "Serviço cadastrado com sucesso.",
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "atualiza um serviço",
            async () => {
                render(
                    <ServicesRoute />,
                );

                await screen.findByText(
                    "Corte de MDF",
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

                fireEvent.change(
                    screen.getByLabelText(
                        "Nome do serviço *",
                    ),
                    {
                        target: {
                            value:
                                "Corte de MDF atualizado",
                        },
                    },
                );

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Salvar alterações",
                        },
                    ),
                );

                await waitFor(
                    () => {
                        expect(
                            updateServiceMock,
                        ).toHaveBeenCalledWith(
                            {
                                accessToken:
                                    "access-token",
                                tenantId:
                                    "tenant-001",
                            },
                            service.id,
                            {
                                code:
                                    "CORTE",
                                name:
                                    "Corte de MDF atualizado",
                                category:
                                    "Usinagem",
                                unit:
                                    "HORA",
                                execution_mode:
                                    "INTERNAL",
                                estimated_duration_minutes:
                                    60,
                            },
                        );
                    },
                );

                expect(
                    await screen.findByText(
                        "Serviço atualizado com sucesso.",
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "inativa um serviço após confirmação",
            async () => {
                render(
                    <ServicesRoute />,
                );

                await screen.findByText(
                    "Corte de MDF",
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
                        "Inativar serviço?",
                    ),
                ).toBeInTheDocument();

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Inativar serviço",
                        },
                    ),
                );

                await waitFor(
                    () => {
                        expect(
                            deactivateServiceMock,
                        ).toHaveBeenCalledWith(
                            {
                                accessToken:
                                    "access-token",
                                tenantId:
                                    "tenant-001",
                            },
                            service.id,
                        );
                    },
                );

                expect(
                    await screen.findByText(
                        "Serviço inativado com sucesso.",
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "reativa um serviço inativo",
            async () => {
                listServicePageMock
                    .mockResolvedValue({
                        ...activePage,
                        items: [
                            {
                                ...service,
                                is_active:
                                    false,
                            },
                        ],
                    });

                render(
                    <ServicesRoute />,
                );

                await screen.findByText(
                    "Corte de MDF",
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

                await waitFor(
                    () => {
                        expect(
                            reactivateServiceMock,
                        ).toHaveBeenCalledWith(
                            {
                                accessToken:
                                    "access-token",
                                tenantId:
                                    "tenant-001",
                            },
                            service.id,
                        );
                    },
                );

                expect(
                    await screen.findByText(
                        "Serviço reativado com sucesso.",
                    ),
                ).toBeInTheDocument();
            },
        );
    },
);