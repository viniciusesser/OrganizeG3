import {
    fireEvent,
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
    AppShell,
} from "@/app/shell/AppShell";

function renderAppShell() {
    return render(
        <MemoryRouter>
            <AppShell>
                <p>
                    Conteúdo da página
                </p>
            </AppShell>
        </MemoryRouter>,
    );
}

describe("AppShell", () => {
    it(
        "renders the application shell regions",
        () => {
            renderAppShell();

            expect(
                screen.getByRole(
                    "complementary",
                    {
                        name:
                            "Navegação principal",
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
                    "banner",
                ),
            ).toBeInTheDocument();

            expect(
                screen.getByRole(
                    "main",
                ),
            ).toBeInTheDocument();

            expect(
                screen.getByText(
                    "Conteúdo da página",
                ),
            ).toBeInTheDocument();
        },
    );

    it(
        "renders the OrganizeG3 brand",
        () => {
            renderAppShell();

            expect(
                screen.getAllByRole(
                    "heading",
                    {
                        name: "OrganizeG3",
                    },
                ).length,
            ).toBeGreaterThanOrEqual(1);
        },
    );

    it(
        "shows the platform connection status",
        () => {
            renderAppShell();

            expect(
                screen.getByText(
                    "API conectada",
                ),
            ).toBeInTheDocument();
        },
    );

    it(
        "opens and closes the mobile navigation",
        () => {
            renderAppShell();

            expect(
                screen.queryByRole(
                    "dialog",
                    {
                        name:
                            "Navegação móvel",
                    },
                ),
            ).not.toBeInTheDocument();

            fireEvent.click(
                screen.getByRole(
                    "button",
                    {
                        name: "Menu",
                    },
                ),
            );

            expect(
                screen.getByRole(
                    "dialog",
                    {
                        name:
                            "Navegação móvel",
                    },
                ),
            ).toBeInTheDocument();

            fireEvent.click(
                screen.getByRole(
                    "button",
                    {
                        name: "Fechar",
                    },
                ),
            );

            expect(
                screen.queryByRole(
                    "dialog",
                    {
                        name:
                            "Navegação móvel",
                    },
                ),
            ).not.toBeInTheDocument();
        },
    );
});