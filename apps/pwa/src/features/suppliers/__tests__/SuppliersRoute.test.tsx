import {
    cleanup,
    fireEvent,
    render,
    screen,
    waitFor,
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
    SuppliersRoute,
} from "@/features/suppliers/routes/SuppliersRoute";

const {
    createSupplierMock,
    deactivateSupplierMock,
    hasPermissionMock,
    listSupplierPageMock,
    reactivateSupplierMock,
    updateSupplierMock,
    useAuthMock,
} = vi.hoisted(
    () => ({
        createSupplierMock:
            vi.fn(),
        deactivateSupplierMock:
            vi.fn(),
        hasPermissionMock:
            vi.fn(),
        listSupplierPageMock:
            vi.fn(),
        reactivateSupplierMock:
            vi.fn(),
        updateSupplierMock:
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
        useAuth: useAuthMock,
    }),
);

vi.mock(
    "@/features/suppliers/api/suppliersApi",
    () => ({
        createSupplier:
            createSupplierMock,
        deactivateSupplier:
            deactivateSupplierMock,
        listSupplierPage:
            listSupplierPageMock,
        reactivateSupplier:
            reactivateSupplierMock,
        updateSupplier:
            updateSupplierMock,
    }),
);

const supplier = {
    id: "supplier-001",
    tenant_id: "tenant-001",
    code: "FOR-001",
    name: "Madeiras Brasil",
    trade_name:
        "Madeiras Brasil",
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
} as const;

const activePage = {
    items: [
        supplier,
    ],
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

describe("SuppliersRoute", () => {
    beforeEach(() => {
        vi.clearAllMocks();

        configureAuthenticatedUser();

        listSupplierPageMock
            .mockResolvedValue(
                activePage,
            );

        createSupplierMock
            .mockResolvedValue(
                supplier,
            );

        updateSupplierMock
            .mockResolvedValue(
                supplier,
            );

        deactivateSupplierMock
            .mockResolvedValue({
                ...supplier,
                is_active: false,
            });

        reactivateSupplierMock
            .mockResolvedValue(
                supplier,
            );
    });

    afterEach(() => {
        cleanup();
    });

    it("carrega os fornecedores da empresa ativa", async () => {
        render(
            <SuppliersRoute />,
        );

        expect(
            await screen.findByText(
                "Madeiras Brasil",
            ),
        ).toBeInTheDocument();

        expect(
            listSupplierPageMock,
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
                limit: 20,
                offset: 0,
            },
        );
    });

    it("não consulta fornecedores sem permissão de leitura", async () => {
        hasPermissionMock
            .mockReturnValue(false);

        render(
            <SuppliersRoute />,
        );

        expect(
            screen.getByText(
                "Acesso restrito",
            ),
        ).toBeInTheDocument();

        expect(
            screen.getByText(
                "Você não possui permissão para visualizar fornecedores.",
            ),
        ).toBeInTheDocument();

        await waitFor(() => {
            expect(
                listSupplierPageMock,
            ).not.toHaveBeenCalled();
        });
    });

    it("informa quando a sessão ou a empresa ativa está indisponível", () => {
        useAuthMock.mockReturnValue({
            identity: {
                id: "user-001",
            },
            session: null,
            selectedTenant: null,
        });

        render(
            <SuppliersRoute />,
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
    });

    it("pesquisa fornecedores e inclui os inativos", async () => {
        render(
            <SuppliersRoute />,
        );

        await screen.findByText(
            "Madeiras Brasil",
        );

        fireEvent.change(
            screen.getByLabelText(
                "Pesquisar fornecedores",
            ),
            {
                target: {
                    value:
                        "  Madeiras  ",
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
                    name: "Pesquisar",
                },
            ),
        );

        await waitFor(() => {
            expect(
                listSupplierPageMock,
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
                        "Madeiras",
                    limit: 20,
                    offset: 0,
                },
            );
        });
    });

    it("cadastra um fornecedor", async () => {
        render(
            <SuppliersRoute />,
        );

        await screen.findByText(
            "Madeiras Brasil",
        );

        fireEvent.click(
            screen.getByRole(
                "button",
                {
                    name:
                        "Novo fornecedor",
                },
            ),
        );

        fireEvent.change(
            screen.getByLabelText(
                "Código do fornecedor *",
            ),
            {
                target: {
                    value:
                        " FOR-002 ",
                },
            },
        );

        fireEvent.change(
            screen.getByLabelText(
                "Nome do fornecedor *",
            ),
            {
                target: {
                    value:
                        " Ferragens Brasil ",
                },
            },
        );

        fireEvent.change(
            screen.getByLabelText(
                "UF",
            ),
            {
                target: {
                    value: "sp",
                },
            },
        );

        fireEvent.click(
            screen.getByRole(
                "button",
                {
                    name:
                        "Salvar fornecedor",
                },
            ),
        );

        await waitFor(() => {
            expect(
                createSupplierMock,
            ).toHaveBeenCalledWith(
                {
                    accessToken:
                        "access-token",
                    tenantId:
                        "tenant-001",
                },
                expect.objectContaining({
                    code: "FOR-002",
                    name:
                        "Ferragens Brasil",
                    state: "SP",
                }),
            );
        });

        expect(
            await screen.findByText(
                "Fornecedor cadastrado com sucesso.",
            ),
        ).toBeInTheDocument();
    });

    it("valida os campos obrigatórios antes do cadastro", async () => {
        render(
            <SuppliersRoute />,
        );

        await screen.findByText(
            "Madeiras Brasil",
        );

        fireEvent.click(
            screen.getByRole(
                "button",
                {
                    name:
                        "Novo fornecedor",
                },
            ),
        );

        fireEvent.click(
            screen.getByRole(
                "button",
                {
                    name:
                        "Salvar fornecedor",
                },
            ),
        );

        expect(
            screen.getByText(
                "Informe o código do fornecedor.",
            ),
        ).toBeInTheDocument();

        expect(
            screen.getByText(
                "Informe o nome do fornecedor.",
            ),
        ).toBeInTheDocument();

        expect(
            createSupplierMock,
        ).not.toHaveBeenCalled();
    });

    it("atualiza um fornecedor", async () => {
        render(
            <SuppliersRoute />,
        );

        await screen.findByText(
            "Madeiras Brasil",
        );

        fireEvent.click(
            screen.getByRole(
                "button",
                {
                    name: "Editar",
                },
            ),
        );

        const nameInput =
            screen.getByLabelText(
                "Nome do fornecedor *",
            );

        fireEvent.change(
            nameInput,
            {
                target: {
                    value:
                        "Madeiras Brasil Atualizada",
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
                updateSupplierMock,
            ).toHaveBeenCalledWith(
                {
                    accessToken:
                        "access-token",
                    tenantId:
                        "tenant-001",
                },
                supplier.id,
                expect.objectContaining({
                    code:
                        supplier.code,
                    name:
                        "Madeiras Brasil Atualizada",
                }),
            );
        });

        expect(
            await screen.findByText(
                "Fornecedor atualizado com sucesso.",
            ),
        ).toBeInTheDocument();
    });

    it("inativa um fornecedor após a confirmação", async () => {
        render(
            <SuppliersRoute />,
        );

        await screen.findByText(
            "Madeiras Brasil",
        );

        fireEvent.click(
            screen.getByRole(
                "button",
                {
                    name: "Inativar",
                },
            ),
        );

        expect(
            screen.getByText(
                "Inativar fornecedor?",
            ),
        ).toBeInTheDocument();

        fireEvent.click(
            screen.getByRole(
                "button",
                {
                    name:
                        "Inativar fornecedor",
                },
            ),
        );

        await waitFor(() => {
            expect(
                deactivateSupplierMock,
            ).toHaveBeenCalledWith(
                {
                    accessToken:
                        "access-token",
                    tenantId:
                        "tenant-001",
                },
                supplier.id,
            );
        });

        expect(
            await screen.findByText(
                "Fornecedor inativado com sucesso.",
            ),
        ).toBeInTheDocument();
    });

    it("reativa um fornecedor inativo", async () => {
        const inactiveSupplier = {
            ...supplier,
            is_active: false,
        };

        listSupplierPageMock
            .mockResolvedValue({
                ...activePage,
                items: [
                    inactiveSupplier,
                ],
            });

        render(
            <SuppliersRoute />,
        );

        await screen.findByText(
            "Madeiras Brasil",
        );

        fireEvent.click(
            screen.getByRole(
                "button",
                {
                    name: "Reativar",
                },
            ),
        );

        await waitFor(() => {
            expect(
                reactivateSupplierMock,
            ).toHaveBeenCalledWith(
                {
                    accessToken:
                        "access-token",
                    tenantId:
                        "tenant-001",
                },
                supplier.id,
            );
        });

        expect(
            await screen.findByText(
                "Fornecedor reativado com sucesso.",
            ),
        ).toBeInTheDocument();
    });

    it("apresenta erro ao carregar fornecedores", async () => {
        listSupplierPageMock
            .mockRejectedValue(
                new Error(
                    "Falha na consulta.",
                ),
            );

        render(
            <SuppliersRoute />,
        );

        expect(
            await screen.findByText(
                "Não foi possível carregar os fornecedores",
            ),
        ).toBeInTheDocument();

        expect(
            screen.getByText(
                "Falha na consulta.",
            ),
        ).toBeInTheDocument();
    });
});