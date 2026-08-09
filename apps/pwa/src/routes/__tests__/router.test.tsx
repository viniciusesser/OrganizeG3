import {
    render,
    screen,
} from "@testing-library/react";
import {
    createMemoryRouter,
} from "react-router";
import {
    RouterProvider,
} from "react-router/dom";
import {
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import type {
    AuthContextValue,
} from "@/features/auth/session/AuthContext";
import {
    useAuth,
} from "@/features/auth/session/useAuth";
import {
    getApiHealth,
} from "@/infrastructure/api/health";
import {
    appRoutes,
} from "@/routes/routes";

vi.mock(
    "@/features/auth/session/useAuth",
    () => ({
        useAuth: vi.fn(),
    }),
);

vi.mock(
    "@/infrastructure/api/health",
    () => ({
        getApiHealth: vi.fn(),
    }),
);

const useAuthMock =
    vi.mocked(useAuth);

const getApiHealthMock =
    vi.mocked(getApiHealth);

const AUTHENTICATED_CONTEXT: AuthContextValue = {
    status: "authenticated",
    session: null,
    tenants: [],
    selectedTenant: null,
    identity: null,
    error: null,
    signIn: vi.fn(),
    selectTenant: vi.fn(),
    signOut: vi.fn(),
    retry: vi.fn(),
};

function renderRoute(
    path: string,
) {
    const router =
        createMemoryRouter(
            appRoutes,
            {
                initialEntries: [
                    path,
                ],
            },
        );

    return render(
        <RouterProvider
            router={router}
        />,
    );
}

describe(
    "application routes",
    () => {
        beforeEach(() => {
            vi.clearAllMocks();

            useAuthMock.mockReturnValue(
                AUTHENTICATED_CONTEXT,
            );
        });

        it(
            "renders the application root inside the app shell",
            async () => {
                getApiHealthMock.mockResolvedValue({
                    status: "healthy",
                    service:
                        "organizeg3-api",
                    version: "0.1.0",
                });

                renderRoute("/");

                expect(
                    screen.getByRole(
                        "heading",
                        {
                            level: 1,
                            name:
                                "Visão geral",
                        },
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByRole(
                        "navigation",
                        {
                            name:
                                "Módulos do sistema",
                        },
                    ),
                ).toBeInTheDocument();

                expect(
                    await screen.findByText(
                        "healthy",
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "renders a module placeholder inside the shell",
            () => {
                renderRoute(
                    "/clientes",
                );

                expect(
                    screen.getByRole(
                        "heading",
                        {
                            level: 1,
                            name:
                                "Clientes",
                        },
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByRole(
                        "navigation",
                        {
                            name:
                                "Módulos do sistema",
                        },
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByRole(
                        "link",
                        {
                            name:
                                "Clientes",
                        },
                    ),
                ).toHaveClass(
                    "og3-navigation__link--active",
                );
            },
        );

        it(
            "renders the not-found route for an unknown URL",
            () => {
                renderRoute(
                    "/route-that-does-not-exist",
                );

                expect(
                    screen.getByRole(
                        "heading",
                        {
                            name:
                                "Página não encontrada",
                        },
                    ),
                ).toBeInTheDocument();
            },
        );

        it(
            "keeps the theme preview outside the application shell",
            () => {
                renderRoute(
                    "/theme-preview",
                );

                expect(
                    screen.getByRole(
                        "heading",
                        {
                            level: 1,
                            name:
                                "OrganizeG3",
                        },
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.queryByRole(
                        "navigation",
                        {
                            name:
                                "Módulos do sistema",
                        },
                    ),
                ).not.toBeInTheDocument();
            },
        );
    },
);