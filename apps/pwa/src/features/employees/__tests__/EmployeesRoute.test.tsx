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
    EmployeesRoute,
} from "@/features/employees/routes/EmployeesRoute";
import {
    ApiError,
} from "@/infrastructure/api/apiError";

const {
    createEmployeeMock,
    deactivateEmployeeMock,
    hasPermissionMock,
    listEmployeePageMock,
    reactivateEmployeeMock,
    updateEmployeeMock,
    useAuthMock,
} = vi.hoisted(() => ({
    createEmployeeMock: vi.fn(),
    deactivateEmployeeMock: vi.fn(),
    hasPermissionMock: vi.fn(),
    listEmployeePageMock: vi.fn(),
    reactivateEmployeeMock: vi.fn(),
    updateEmployeeMock: vi.fn(),
    useAuthMock: vi.fn(),
}));

vi.mock(
    "@/features/auth/model/currentIdentity",
    () => ({
        hasPermission: hasPermissionMock,
    }),
);

vi.mock(
    "@/features/auth/session/useAuth",
    () => ({
        useAuth: useAuthMock,
    }),
);

vi.mock(
    "@/features/employees/api/employeesApi",
    () => ({
        createEmployee: createEmployeeMock,
        deactivateEmployee:
            deactivateEmployeeMock,
        listEmployeePage:
            listEmployeePageMock,
        reactivateEmployee:
            reactivateEmployeeMock,
        updateEmployee:
            updateEmployeeMock,
    }),
);

const employee = {
    id: "employee-001",
    tenant_id: "tenant-001",
    branch_id: null,
    code: "FUN-001",
    full_name: "Marcos da Silva",
    document_number: "12345678901",
    email: "marcos@example.com",
    phone: "18999998888",
    job_title: "Marceneiro",
    contract_type: "CLT",
    status: "ACTIVE",
    birth_date: "1990-05-12",
    admission_date: "2024-02-01",
    termination_date: null,
    is_active: true,
    created_at: "2026-08-10T10:00:00Z",
    updated_at: "2026-08-10T10:00:00Z",
} as const;

const activePage = {
    items: [employee],
    hasPrevious: false,
    hasNext: false,
    offset: 0,
    pageSize: 20,
};

function configureAuthenticatedUser() {
    useAuthMock.mockReturnValue({
        identity: {
            id: "user-001",
        },
        session: {
            accessToken: "access-token",
        },
        selectedTenant: {
            tenantId: "tenant-001",
        },
    });

    hasPermissionMock.mockReturnValue(true);
}

describe(
    "EmployeesRoute",
    () => {
        beforeEach(() => {
            vi.clearAllMocks();

            configureAuthenticatedUser();

            listEmployeePageMock
                .mockResolvedValue(activePage);

            createEmployeeMock
                .mockResolvedValue(employee);

            updateEmployeeMock
                .mockResolvedValue(employee);

            deactivateEmployeeMock
                .mockResolvedValue({
                    ...employee,
                    status: "INACTIVE",
                    is_active: false,
                });

            reactivateEmployeeMock
                .mockResolvedValue(employee);
        });

        afterEach(() => {
            cleanup();
        });

        it(
            "carrega os funcionários da empresa ativa",
            async () => {
                render(
                    <EmployeesRoute />,
                );

                expect(
                    await screen.findByText(
                        "Marcos da Silva",
                    ),
                ).toBeInTheDocument();

                expect(
                    listEmployeePageMock,
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
                        status: null,
                        limit: 20,
                        offset: 0,
                    },
                );
            },
        );

        it(
            "não consulta funcionários sem permissão de leitura",
            async () => {
                hasPermissionMock
                    .mockReturnValue(false);

                render(
                    <EmployeesRoute />,
                );

                expect(
                    screen.getByText(
                        "Acesso restrito",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByText(
                        "Você não possui permissão para visualizar funcionários.",
                    ),
                ).toBeInTheDocument();

                await waitFor(() => {
                    expect(
                        listEmployeePageMock,
                    ).not.toHaveBeenCalled();
                });
            },
        );

        it(
            "informa quando a sessão ou a empresa ativa está indisponível",
            () => {
                useAuthMock.mockReturnValue({
                    identity: {
                        id: "user-001",
                    },
                    session: null,
                    selectedTenant: null,
                });

                render(
                    <EmployeesRoute />,
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
            "pesquisa funcionários usando busca, situação e inativos",
            async () => {
                render(
                    <EmployeesRoute />,
                );

                await screen.findByText(
                    "Marcos da Silva",
                );

                fireEvent.change(
                    screen.getByLabelText(
                        "Pesquisar funcionários",
                    ),
                    {
                        target: {
                            value:
                                "  Marcos  ",
                        },
                    },
                );

                fireEvent.change(
                    screen.getByLabelText(
                        "Situação funcional",
                    ),
                    {
                        target: {
                            value:
                                "ON_LEAVE",
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

                await waitFor(() => {
                    expect(
                        listEmployeePageMock,
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
                                "Marcos",
                            status:
                                "ON_LEAVE",
                            limit: 20,
                            offset: 0,
                        },
                    );
                });
            },
        );

        it(
            "exibe erro da API e permite repetir a consulta",
            async () => {
                listEmployeePageMock
                    .mockRejectedValueOnce(
                        new ApiError({
                            status: 503,
                            code:
                                "service.unavailable",
                            message:
                                "Serviço temporariamente indisponível.",
                        }),
                    )
                    .mockResolvedValue(
                        activePage,
                    );

                render(
                    <EmployeesRoute />,
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
                        "Marcos da Silva",
                    ),
                ).toBeInTheDocument();

                expect(
                    listEmployeePageMock,
                ).toHaveBeenCalledTimes(2);
            },
        );

        it(
            "cadastra um funcionário",
            async () => {
                render(
                    <EmployeesRoute />,
                );

                await screen.findByText(
                    "Marcos da Silva",
                );

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Novo funcionário",
                        },
                    ),
                );

                const dialog =
                    screen.getByRole(
                        "dialog",
                        {
                            name:
                                "Novo funcionário",
                        },
                    );

                fireEvent.change(
                    within(dialog)
                        .getByLabelText(
                            "Código do funcionário *",
                        ),
                    {
                        target: {
                            value:
                                "fun-002",
                        },
                    },
                );

                fireEvent.change(
                    within(dialog)
                        .getByLabelText(
                            "Nome completo *",
                        ),
                    {
                        target: {
                            value:
                                "  João Pereira  ",
                        },
                    },
                );

                fireEvent.click(
                    within(dialog)
                        .getByRole(
                            "button",
                            {
                                name:
                                    "Salvar funcionário",
                            },
                        ),
                );

                await waitFor(() => {
                    expect(
                        createEmployeeMock,
                    ).toHaveBeenCalledWith(
                        {
                            accessToken:
                                "access-token",
                            tenantId:
                                "tenant-001",
                        },
                        {
                            code:
                                "FUN-002",
                            full_name:
                                "João Pereira",
                            document_number:
                                null,
                            email: null,
                            phone: null,
                            job_title: null,
                            contract_type:
                                null,
                            birth_date: null,
                            admission_date:
                                null,
                        },
                    );
                });

                expect(
                    await screen.findByText(
                        "Funcionário cadastrado com sucesso.",
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "atualiza um funcionário",
            async () => {
                render(
                    <EmployeesRoute />,
                );

                await screen.findByText(
                    "Marcos da Silva",
                );

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name: "Editar",
                        },
                    ),
                );

                fireEvent.change(
                    screen.getByLabelText(
                        "Nome completo *",
                    ),
                    {
                        target: {
                            value:
                                "Marcos Atualizado",
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

                await waitFor(() => {
                    expect(
                        updateEmployeeMock,
                    ).toHaveBeenCalledWith(
                        {
                            accessToken:
                                "access-token",
                            tenantId:
                                "tenant-001",
                        },
                        employee.id,
                        {
                            code:
                                "FUN-001",
                            full_name:
                                "Marcos Atualizado",
                            document_number:
                                "12345678901",
                            email:
                                "marcos@example.com",
                            phone:
                                "18999998888",
                            job_title:
                                "Marceneiro",
                            contract_type:
                                "CLT",
                            birth_date:
                                "1990-05-12",
                            admission_date:
                                "2024-02-01",
                        },
                    );
                });

                expect(
                    await screen.findByText(
                        "Funcionário atualizado com sucesso.",
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "inativa um funcionário após confirmação",
            async () => {
                render(
                    <EmployeesRoute />,
                );

                await screen.findByText(
                    "Marcos da Silva",
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
                        "Inativar funcionário?",
                    ),
                ).toBeInTheDocument();

                expect(
                    deactivateEmployeeMock,
                ).not.toHaveBeenCalled();

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Inativar funcionário",
                        },
                    ),
                );

                await waitFor(() => {
                    expect(
                        deactivateEmployeeMock,
                    ).toHaveBeenCalledWith(
                        {
                            accessToken:
                                "access-token",
                            tenantId:
                                "tenant-001",
                        },
                        employee.id,
                    );
                });

                expect(
                    await screen.findByText(
                        "Funcionário inativado com sucesso.",
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "reativa um funcionário inativo",
            async () => {
                listEmployeePageMock
                    .mockResolvedValue({
                        ...activePage,
                        items: [
                            {
                                ...employee,
                                status:
                                    "INACTIVE",
                                is_active:
                                    false,
                            },
                        ],
                    });

                render(
                    <EmployeesRoute />,
                );

                await screen.findByText(
                    "Marcos da Silva",
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
                        reactivateEmployeeMock,
                    ).toHaveBeenCalledWith(
                        {
                            accessToken:
                                "access-token",
                            tenantId:
                                "tenant-001",
                        },
                        employee.id,
                    );
                });

                expect(
                    await screen.findByText(
                        "Funcionário reativado com sucesso.",
                    ),
                ).toBeInTheDocument();
            },
        );
    },
);