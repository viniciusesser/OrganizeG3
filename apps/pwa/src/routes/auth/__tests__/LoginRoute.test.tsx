import {
    fireEvent,
    render,
    screen,
    waitFor,
} from "@testing-library/react";
import {
    MemoryRouter,
    Route,
    Routes,
} from "react-router";
import {
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import type {
    AuthContextValue,
    AuthStatus,
} from "@/features/auth/session/AuthContext";
import {
    useAuth,
} from "@/features/auth/session/useAuth";
import {
    LoginRoute,
} from "@/routes/auth/LoginRoute";

vi.mock(
    "@/features/auth/session/useAuth",
    () => ({
        useAuth: vi.fn(),
    }),
);

const useAuthMock =
    vi.mocked(
        useAuth,
    );

const signInMock =
    vi.fn();

const selectTenantMock =
    vi.fn();

const signOutMock =
    vi.fn();

const retryMock =
    vi.fn();

function createAuthContext(
    status: AuthStatus,
    overrides:
        Partial<AuthContextValue> = {},
): AuthContextValue {
    return {
        status,
        session: null,
        tenants: [],
        selectedTenant: null,
        identity: null,
        error: null,
        signIn: signInMock,
        selectTenant:
            selectTenantMock,
        signOut:
            signOutMock,
        retry:
            retryMock,
        ...overrides,
    };
}

function renderRoute() {
    return render(
        <MemoryRouter
            initialEntries={[
                "/login",
            ]}
        >
            <LoginRoute />
        </MemoryRouter>,
    );
}

describe(
    "LoginRoute",
    () => {
        beforeEach(() => {
            vi.clearAllMocks();

            signInMock
                .mockResolvedValue(
                    undefined,
                );

            selectTenantMock
                .mockResolvedValue(
                    undefined,
                );

            signOutMock
                .mockResolvedValue(
                    undefined,
                );

            retryMock
                .mockResolvedValue(
                    undefined,
                );
        });

        it(
            "renders the credential form when signed out",
            () => {
                useAuthMock
                    .mockReturnValue(
                        createAuthContext(
                            "signed_out",
                        ),
                    );

                renderRoute();

                expect(
                    screen.getByRole(
                        "heading",
                        {
                            name:
                                "Acessar sistema",
                        },
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByLabelText(
                        "E-mail",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByLabelText(
                        "Senha",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByRole(
                        "button",
                        {
                            name: "Entrar",
                        },
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "submits e-mail and password",
            async () => {
                useAuthMock
                    .mockReturnValue(
                        createAuthContext(
                            "signed_out",
                        ),
                    );

                renderRoute();

                fireEvent.change(
                    screen.getByLabelText(
                        "E-mail",
                    ),
                    {
                        target: {
                            value:
                                "admin@example.com",
                        },
                    },
                );

                fireEvent.change(
                    screen.getByLabelText(
                        "Senha",
                    ),
                    {
                        target: {
                            value:
                                "secret-password",
                        },
                    },
                );

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name: "Entrar",
                        },
                    ),
                );

                await waitFor(
                    () => {
                        expect(
                            signInMock,
                        ).toHaveBeenCalledWith({
                            email:
                                "admin@example.com",
                            password:
                                "secret-password",
                        });
                    },
                );
            },
        );

        it(
            "shows accessible tenants when selection is required",
            async () => {
                useAuthMock
                    .mockReturnValue(
                        createAuthContext(
                            "tenant_selection_required",
                            {
                                session: {
                                    accessToken:
                                        "access-token",
                                    refreshToken:
                                        "refresh-token",
                                    expiresAt:
                                        null,
                                    authUserId:
                                        "auth-user-id",
                                    email:
                                        "admin@example.com",
                                },
                                tenants: [
                                    {
                                        tenantId:
                                            "tenant-a",
                                        membershipId:
                                            "membership-a",
                                        name:
                                            "Empresa A",
                                    },
                                    {
                                        tenantId:
                                            "tenant-b",
                                        membershipId:
                                            "membership-b",
                                        name:
                                            "Empresa B",
                                    },
                                ],
                            },
                        ),
                    );

                renderRoute();

                expect(
                    screen.getByRole(
                        "heading",
                        {
                            name:
                                "Escolha a empresa",
                        },
                    ),
                ).toBeInTheDocument();

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Empresa B",
                        },
                    ),
                );

                await waitFor(
                    () => {
                        expect(
                            selectTenantMock,
                        ).toHaveBeenCalledWith(
                            "tenant-b",
                        );
                    },
                );
            },
        );

        it(
            "renders the no tenant access state",
            () => {
                useAuthMock
                    .mockReturnValue(
                        createAuthContext(
                            "no_tenant_access",
                            {
                                session: {
                                    accessToken:
                                        "access-token",
                                    refreshToken:
                                        "refresh-token",
                                    expiresAt:
                                        null,
                                    authUserId:
                                        "auth-user-id",
                                    email:
                                        "admin@example.com",
                                },
                            },
                        ),
                    );

                renderRoute();

                expect(
                    screen.getByRole(
                        "heading",
                        {
                            name:
                                "Acesso não disponível",
                        },
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Verificar novamente",
                        },
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "renders the context error state",
            () => {
                useAuthMock
                    .mockReturnValue(
                        createAuthContext(
                            "error",
                            {
                                error: new Error(
                                    "Falha ao carregar.",
                                ) as AuthContextValue["error"],
                            },
                        ),
                    );

                renderRoute();

                expect(
                    screen.getByText(
                        "Falha ao carregar.",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Tentar novamente",
                        },
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "renders loading while authentication context is resolving",
            () => {
                useAuthMock
                    .mockReturnValue(
                        createAuthContext(
                            "resolving_tenants",
                        ),
                    );

                renderRoute();

                expect(
                    screen.getByRole(
                        "status",
                    ),
                ).toHaveTextContent(
                    "Carregando seu acesso...",
                );
            },
        );

        it(
            "returns authenticated users to the original protected route",
            () => {
                useAuthMock
                    .mockReturnValue(
                        createAuthContext(
                            "authenticated",
                        ),
                    );

                render(
                    <MemoryRouter
                        initialEntries={[
                            {
                                pathname: "/login",
                                state: {
                                    from: {
                                        pathname:
                                            "/materiais",
                                        search:
                                            "?grupo=mdf",
                                        hash:
                                            "#estoque",
                                    },
                                },
                            },
                        ]}
                    >
                        <Routes>
                            <Route
                                path="/login"
                                element={
                                    <LoginRoute />
                                }
                            />

                            <Route
                                path="/materiais"
                                element={
                                    <div>
                                        Materiais retornados
                                    </div>
                                }
                            />
                        </Routes>
                    </MemoryRouter>,
                );

                expect(
                    screen.getByText(
                        "Materiais retornados",
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "falls back to root when authenticated without an original route",
            () => {
                useAuthMock
                    .mockReturnValue(
                        createAuthContext(
                            "authenticated",
                        ),
                    );

                render(
                    <MemoryRouter
                        initialEntries={[
                            "/login",
                        ]}
                    >
                        <Routes>
                            <Route
                                path="/login"
                                element={
                                    <LoginRoute />
                                }
                            />

                            <Route
                                path="/"
                                element={
                                    <div>
                                        Página inicial
                                    </div>
                                }
                            />
                        </Routes>
                    </MemoryRouter>,
                );

                expect(
                    screen.getByText(
                        "Página inicial",
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "rejects unsafe return destinations",
            () => {
                useAuthMock
                    .mockReturnValue(
                        createAuthContext(
                            "authenticated",
                        ),
                    );

                render(
                    <MemoryRouter
                        initialEntries={[
                            {
                                pathname: "/login",
                                state: {
                                    from: {
                                        pathname:
                                            "//external.example",
                                    },
                                },
                            },
                        ]}
                    >
                        <Routes>
                            <Route
                                path="/login"
                                element={
                                    <LoginRoute />
                                }
                            />

                            <Route
                                path="/"
                                element={
                                    <div>
                                        Destino seguro
                                    </div>
                                }
                            />
                        </Routes>
                    </MemoryRouter>,
                );

                expect(
                    screen.getByText(
                        "Destino seguro",
                    ),
                ).toBeInTheDocument();
            },
        );
    },
);