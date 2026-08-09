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
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    getApiHealth,
} from "@/infrastructure/api/health";
import {
    appRoutes,
} from "@/routes/routes";

vi.mock(
    "@/infrastructure/api/health",
    () => ({
        getApiHealth: vi.fn(),
    }),
);

const getApiHealthMock =
    vi.mocked(getApiHealth);

describe("application routes", () => {
    it(
        "renders the application root route",
        async () => {
            getApiHealthMock.mockResolvedValue({
                status: "healthy",
                service:
                    "organizeg3-api",
                version: "0.1.0",
            });

            const router =
                createMemoryRouter(
                    appRoutes,
                    {
                        initialEntries: [
                            "/",
                        ],
                    },
                );

            render(
                <RouterProvider
                    router={router}
                />,
            );

            expect(
                screen.getByRole(
                    "heading",
                    {
                        name: "OrganizeG3",
                    },
                ),
            ).toBeInTheDocument();

            expect(
                await screen.findByText(
                    "healthy",
                ),
            ).toBeInTheDocument();

            expect(
                screen.getByText(
                    "organizeg3-api",
                ),
            ).toBeInTheDocument();
        },
    );

    it(
        "renders the not-found route for an unknown URL",
        () => {
            const router =
                createMemoryRouter(
                    appRoutes,
                    {
                        initialEntries: [
                            "/route-that-does-not-exist",
                        ],
                    },
                );

            render(
                <RouterProvider
                    router={router}
                />,
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

            expect(
                screen.getByRole(
                    "link",
                    {
                        name:
                            "Voltar para o início",
                    },
                ),
            ).toHaveAttribute(
                "href",
                "/",
            );
        },
    );
});