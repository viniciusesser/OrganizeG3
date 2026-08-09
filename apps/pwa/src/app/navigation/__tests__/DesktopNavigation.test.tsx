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
} from "vitest";

import {
    DesktopNavigation,
} from "@/app/navigation/DesktopNavigation";

describe("DesktopNavigation", () => {
    it(
        "renders the application navigation groups",
        () => {
            render(
                <MemoryRouter>
                    <DesktopNavigation />
                </MemoryRouter>,
            );

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
                screen.getByText(
                    "Operações",
                ),
            ).toBeInTheDocument();

            expect(
                screen.getByText(
                    "Pessoas",
                ),
            ).toBeInTheDocument();

            expect(
                screen.getByText(
                    "Organização",
                ),
            ).toBeInTheDocument();
        },
    );

    it(
        "renders the module navigation links",
        () => {
            render(
                <MemoryRouter>
                    <DesktopNavigation />
                </MemoryRouter>,
            );

            expect(
                screen.getByRole(
                    "link",
                    {
                        name: "Clientes",
                    },
                ),
            ).toHaveAttribute(
                "href",
                "/clientes",
            );

            expect(
                screen.getByRole(
                    "link",
                    {
                        name: "Materiais",
                    },
                ),
            ).toHaveAttribute(
                "href",
                "/materiais",
            );

            expect(
                screen.getByRole(
                    "link",
                    {
                        name: "Funcionários",
                    },
                ),
            ).toHaveAttribute(
                "href",
                "/funcionarios",
            );
        },
    );

    it(
        "marks the current route as active",
        () => {
            render(
                <MemoryRouter
                    initialEntries={[
                        "/clientes",
                    ]}
                >
                    <DesktopNavigation />
                </MemoryRouter>,
            );

            expect(
                screen.getByRole(
                    "link",
                    {
                        name: "Clientes",
                    },
                ),
            ).toHaveClass(
                "og3-navigation__link--active",
            );

            expect(
                screen.getByRole(
                    "link",
                    {
                        name: "Início",
                    },
                ),
            ).not.toHaveClass(
                "og3-navigation__link--active",
            );
        },
    );
});