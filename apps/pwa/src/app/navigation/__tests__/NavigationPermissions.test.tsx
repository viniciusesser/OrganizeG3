import {
    render,
    screen,
} from "@testing-library/react";
import {
    MemoryRouter,
} from "react-router";
import {
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    filterNavigationGroups,
    navigationGroups,
} from "@/app/navigation/navigation";
import {
    NavigationContent,
} from "@/app/navigation/NavigationContent";
import type {
    AuthContextValue,
} from "@/features/auth/session/AuthContext";
import {
    AuthContext,
} from "@/features/auth/session/AuthContext";

function createAuthenticatedContext(
    permissions: readonly string[],
): AuthContextValue {
    return {
        status: "authenticated",
        session: null,
        tenants: [],
        selectedTenant: null,
        identity: {
            tenantId: "tenant-id",
            userId: "user-id",
            membershipId:
                "membership-id",
            authUserId:
                "auth-user-id",
            email:
                "usuario@example.com",
            displayName:
                "Usuário",
            permissions:
                new Set(
                    permissions,
                ),
        },
        error: null,
        signIn: vi.fn(),
        selectTenant: vi.fn(),
        signOut: vi.fn(),
        retry: vi.fn(),
    };
}

function renderNavigation(
    permissions: readonly string[],
) {
    return render(
        <AuthContext.Provider
            value={
                createAuthenticatedContext(
                    permissions,
                )
            }
        >
            <MemoryRouter>
                <nav>
                    <NavigationContent />
                </nav>
            </MemoryRouter>
        </AuthContext.Provider>,
    );
}

describe(
    "navigation permissions",
    () => {
        it(
            "keeps unrestricted navigation items",
            () => {
                const groups =
                    filterNavigationGroups(
                        navigationGroups,
                        new Set(),
                    );

                expect(groups).toHaveLength(
                    1,
                );

                expect(
                    groups[0]?.id,
                ).toBe(
                    "overview",
                );

                expect(
                    groups[0]?.items[0]
                        ?.id,
                ).toBe(
                    "home",
                );
            },
        );

        it(
            "shows only modules allowed by the authenticated identity",
            () => {
                renderNavigation([
                    "customers.read",
                    "materials.read",
                ]);

                expect(
                    screen.getByRole(
                        "link",
                        {
                            name: "Início",
                        },
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByRole(
                        "link",
                        {
                            name: "Clientes",
                        },
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByRole(
                        "link",
                        {
                            name: "Materiais",
                        },
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.queryByRole(
                        "link",
                        {
                            name:
                                "Fornecedores",
                        },
                    ),
                ).not.toBeInTheDocument();

                expect(
                    screen.queryByRole(
                        "link",
                        {
                            name: "Serviços",
                        },
                    ),
                ).not.toBeInTheDocument();

                expect(
                    screen.queryByRole(
                        "link",
                        {
                            name:
                                "Funcionários",
                        },
                    ),
                ).not.toBeInTheDocument();

                expect(
                    screen.queryByRole(
                        "link",
                        {
                            name: "Empresa",
                        },
                    ),
                ).not.toBeInTheDocument();
            },
        );

        it(
            "removes navigation groups without accessible items",
            () => {
                renderNavigation([
                    "customers.read",
                ]);

                expect(
                    screen.getByText(
                        "Visão geral",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByText(
                        "Comercial",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.queryByText(
                        "Operações",
                    ),
                ).not.toBeInTheDocument();

                expect(
                    screen.queryByText(
                        "Pessoas",
                    ),
                ).not.toBeInTheDocument();

                expect(
                    screen.queryByText(
                        "Organização",
                    ),
                ).not.toBeInTheDocument();
            },
        );

        it(
            "shows all protected modules when all read permissions are granted",
            () => {
                renderNavigation([
                    "customers.read",
                    "suppliers.read",
                    "materials.read",
                    "services.read",
                    "machines.read",
                    "brands.read",
                    "employees.read",
                    "company.read",
                    "branches.read",
                ]);

                const expectedLinks = [
                    "Início",
                    "Clientes",
                    "Fornecedores",
                    "Materiais",
                    "Serviços",
                    "Máquinas",
                    "Marcas",
                    "Funcionários",
                    "Empresa",
                    "Filiais",
                ];

                for (
                    const label
                    of expectedLinks
                ) {
                    expect(
                        screen.getByRole(
                            "link",
                            {
                                name: label,
                            },
                        ),
                    ).toBeInTheDocument();
                }
            },
        );

        it(
            "falls back to unrestricted items when authenticated identity is missing",
            () => {
                const context:
                    AuthContextValue = {
                    status:
                        "authenticated",
                    session: null,
                    tenants: [],
                    selectedTenant:
                        null,
                    identity: null,
                    error: null,
                    signIn: vi.fn(),
                    selectTenant:
                        vi.fn(),
                    signOut: vi.fn(),
                    retry: vi.fn(),
                };

                render(
                    <AuthContext.Provider
                        value={context}
                    >
                        <MemoryRouter>
                            <nav>
                                <NavigationContent />
                            </nav>
                        </MemoryRouter>
                    </AuthContext.Provider>,
                );

                expect(
                    screen.getByRole(
                        "link",
                        {
                            name: "Início",
                        },
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.queryByRole(
                        "link",
                        {
                            name: "Clientes",
                        },
                    ),
                ).not.toBeInTheDocument();
            },
        );
    },
);