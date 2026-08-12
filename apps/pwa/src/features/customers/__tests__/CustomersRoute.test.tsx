import {
    fireEvent,
    render,
    screen,
    waitFor,
} from "@testing-library/react";
import {
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    archiveCustomer,
    createCustomer,
    listCustomerPage,
    reactivateCustomer,
    updateCustomer,
} from "@/features/customers/api/customersApi";
import type {
    AuthContextValue,
} from "@/features/auth/session/AuthContext";
import {
    useAuth,
} from "@/features/auth/session/useAuth";
import type {
    Customer,
    CustomerPage,
} from "@/features/customers/model/customer";
import {
    CustomersRoute,
} from "@/features/customers/routes/CustomersRoute";
import {
    ApiError,
} from "@/infrastructure/api/apiError";

vi.mock(
    "@/features/auth/session/useAuth",
    () => ({
        useAuth: vi.fn(),
    }),
);

vi.mock(
    "@/features/customers/api/customersApi",
    () => ({
        listCustomerPage: vi.fn(),
        createCustomer: vi.fn(),
        updateCustomer: vi.fn(),
        archiveCustomer: vi.fn(),
        reactivateCustomer: vi.fn(),
    }),
);

const useAuthMock = vi.mocked(useAuth);
const listCustomerPageMock =
    vi.mocked(listCustomerPage);
const createCustomerMock =
    vi.mocked(createCustomer);
const updateCustomerMock =
    vi.mocked(updateCustomer);
const archiveCustomerMock =
    vi.mocked(archiveCustomer);
const reactivateCustomerMock =
    vi.mocked(reactivateCustomer);

const customer: Customer = {
    id: 17,
    tenant_id:
        "11111111-1111-4111-8111-111111111111",
    code: "CLI-0017",
    name: "Antônio Marcos",
    customer_type: "INDIVIDUAL",
    document_number: "12345678901",
    email: "antonio@example.com",
    phone: "18999998888",
    is_active: true,
    row_version: 4,
};

const page: CustomerPage = {
    items: [customer],
    hasPrevious: false,
    hasNext: true,
    offset: 0,
    pageSize: 20,
};

const allPermissions = [
    "customers.read",
    "customers.create",
    "customers.update",
    "customers.archive",
    "customers.reactivate",
];

function createAuthContext(
    permissions: readonly string[] =
        allPermissions,
): AuthContextValue {
    return {
        status: "authenticated",
        session: {
            accessToken: "access-token",
            refreshToken: "refresh-token",
            expiresAt: null,
            authUserId: "auth-user-id",
            email: "user@example.com",
        },
        tenants: [],
        selectedTenant: {
            tenantId:
                "11111111-1111-4111-8111-111111111111",
            membershipId:
                "22222222-2222-4222-8222-222222222222",
            name: "Marcenaria Galdino",
        },
        identity: {
            tenantId:
                "11111111-1111-4111-8111-111111111111",
            userId:
                "33333333-3333-4333-8333-333333333333",
            membershipId:
                "22222222-2222-4222-8222-222222222222",
            authUserId: "auth-user-id",
            email: "user@example.com",
            displayName: "Vinícius",
            permissions:
                new Set(permissions),
        },
        error: null,
        signIn: vi.fn(),
        selectTenant: vi.fn(),
        signOut: vi.fn(),
        retry: vi.fn(),
    };
}

describe(
    "CustomersRoute",
    () => {
        beforeEach(() => {
            vi.clearAllMocks();

            useAuthMock.mockReturnValue(
                createAuthContext(),
            );

            listCustomerPageMock
                .mockResolvedValue(page);

            createCustomerMock
                .mockResolvedValue(customer);

            updateCustomerMock
                .mockResolvedValue(customer);

            archiveCustomerMock
                .mockResolvedValue({
                    ...customer,
                    is_active: false,
                    row_version: 5,
                });

            reactivateCustomerMock
                .mockResolvedValue(customer);
        });

        it(
            "loads and renders customers using the authenticated tenant context",
            async () => {
                render(<CustomersRoute />);

                expect(
                    screen.getByRole(
                        "heading",
                        {
                            level: 1,
                            name: "Clientes",
                        },
                    ),
                ).toBeInTheDocument();

                expect(
                    await screen.findByText(
                        "Antônio Marcos",
                    ),
                ).toBeInTheDocument();

                expect(
                    listCustomerPageMock,
                ).toHaveBeenCalledWith(
                    {
                        accessToken:
                            "access-token",
                        tenantId:
                            customer.tenant_id,
                    },
                    {
                        includeInactive: false,
                        search: "",
                        customerType: null,
                        limit: 20,
                        offset: 0,
                    },
                );
            },
        );

        it(
            "shows an empty state and allows creating the first customer",
            async () => {
                listCustomerPageMock
                    .mockResolvedValue({
                        ...page,
                        items: [],
                        hasNext: false,
                    });

                render(<CustomersRoute />);

                expect(
                    await screen.findByRole(
                        "heading",
                        {
                            name:
                                "Nenhum cliente cadastrado",
                        },
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getAllByRole(
                        "button",
                        {
                            name: "Novo cliente",
                        },
                    ),
                ).toHaveLength(2);
            },
        );

        it(
            "shows API errors and retries the list",
            async () => {
                listCustomerPageMock
                    .mockRejectedValueOnce(
                        new ApiError({
                            status: 503,
                            code:
                                "service.unavailable",
                            message:
                                "Serviço temporariamente indisponível.",
                        }),
                    )
                    .mockResolvedValue(page);

                render(<CustomersRoute />);

                expect(
                    await screen.findByText(
                        "Serviço temporariamente indisponível.",
                    ),
                ).toBeInTheDocument();

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name: "Tentar novamente",
                        },
                    ),
                );

                expect(
                    await screen.findByText(
                        "Antônio Marcos",
                    ),
                ).toBeInTheDocument();

                expect(
                    listCustomerPageMock,
                ).toHaveBeenCalledTimes(2);
            },
        );

        it(
            "applies search, type and inactive filters from the first page",
            async () => {
                render(<CustomersRoute />);

                await screen.findByText(
                    "Antônio Marcos",
                );

                fireEvent.change(
                    screen.getByLabelText(
                        "Pesquisar clientes",
                    ),
                    {
                        target: {
                            value: "Empresa",
                        },
                    },
                );

                fireEvent.change(
                    screen.getByLabelText(
                        "Tipo de pessoa",
                    ),
                    {
                        target: {
                            value: "CORPORATE",
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
                        listCustomerPageMock,
                    ).toHaveBeenLastCalledWith(
                        expect.any(Object),
                        expect.objectContaining({
                            includeInactive: true,
                            search: "Empresa",
                            customerType:
                                "CORPORATE",
                            offset: 0,
                        }),
                    );
                });
            },
        );

        it(
            "creates a customer with normalized optional values",
            async () => {
                render(<CustomersRoute />);

                await screen.findByText(
                    "Antônio Marcos",
                );

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name: "Novo cliente",
                        },
                    ),
                );

                fireEvent.change(
                    screen.getByLabelText(
                        "Nome do cliente *",
                    ),
                    {
                        target: {
                            value:
                                "  Cliente Novo  ",
                        },
                    },
                );

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name: "Salvar cliente",
                        },
                    ),
                );

                await waitFor(() => {
                    expect(
                        createCustomerMock,
                    ).toHaveBeenCalledWith(
                        expect.any(Object),
                        {
                            name: "Cliente Novo",
                            customer_type:
                                "INDIVIDUAL",
                            document_number: null,
                            email: null,
                            phone: null,
                        },
                    );
                });

                expect(
                    await screen.findByText(
                        "Cliente cadastrado com sucesso.",
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "updates a customer preserving row_version",
            async () => {
                render(<CustomersRoute />);

                await screen.findByText(
                    "Antônio Marcos",
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
                        "Nome do cliente *",
                    ),
                    {
                        target: {
                            value:
                                "Antônio Atualizado",
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
                        updateCustomerMock,
                    ).toHaveBeenCalledWith(
                        expect.any(Object),
                        customer.id,
                        expect.objectContaining({
                            row_version: 4,
                            name:
                                "Antônio Atualizado",
                        }),
                    );
                });
            },
        );

        it(
            "requires confirmation before archiving and preserves row_version",
            async () => {
                render(<CustomersRoute />);

                await screen.findByText(
                    "Antônio Marcos",
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
                    screen.getByRole(
                        "alertdialog",
                    ),
                ).toBeInTheDocument();

                expect(
                    archiveCustomerMock,
                ).not.toHaveBeenCalled();

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Inativar cliente",
                        },
                    ),
                );

                await waitFor(() => {
                    expect(
                        archiveCustomerMock,
                    ).toHaveBeenCalledWith(
                        expect.any(Object),
                        customer.id,
                        {
                            row_version: 4,
                        },
                    );
                });
            },
        );

        it(
            "hides protected actions and blocks loading without read permission",
            async () => {
                useAuthMock.mockReturnValue(
                    createAuthContext([]),
                );

                render(<CustomersRoute />);

                expect(
                    screen.getByRole(
                        "heading",
                        {
                            name: "Acesso restrito",
                        },
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.queryByRole(
                        "button",
                        {
                            name: "Novo cliente",
                        },
                    ),
                ).not.toBeInTheDocument();

                expect(
                    listCustomerPageMock,
                ).not.toHaveBeenCalled();
            },
        );

        it(
            "reactivates an inactive customer preserving row_version",
            async () => {
                const inactiveCustomer = {
                    ...customer,
                    is_active: false,
                    row_version: 9,
                };

                listCustomerPageMock
                    .mockResolvedValue({
                        ...page,
                        items: [inactiveCustomer],
                    });

                render(<CustomersRoute />);

                fireEvent.click(
                    await screen.findByRole(
                        "button",
                        {
                            name: "Reativar",
                        },
                    ),
                );

                await waitFor(() => {
                    expect(
                        reactivateCustomerMock,
                    ).toHaveBeenCalledWith(
                        expect.any(Object),
                        customer.id,
                        {
                            row_version: 9,
                        },
                    );
                });
            },
        );
    },
);