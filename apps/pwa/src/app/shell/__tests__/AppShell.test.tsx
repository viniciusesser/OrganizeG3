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

interface RenderAppShellOptions {
    readonly activeTenantName?:
    string | null;
    readonly path?: string;
}

function renderAppShell({
    activeTenantName =
    "Marcenaria Galdino",
    path = "/",
}: RenderAppShellOptions = {}) {
    return render(
        <MemoryRouter
            initialEntries={[
                path,
            ]}
        >
            <AppShell
                activeTenantName={
                    activeTenantName
                }
            >
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
            ).toHaveAttribute(
                "id",
                "og3-main-content",
            );

            expect(
                screen.getByText(
                    "Conteúdo da página",
                ),
            ).toBeInTheDocument();
        },
    );

    it(
        "renders the skip link",
        () => {
            renderAppShell();

            expect(
                screen.getByRole(
                    "link",
                    {
                        name:
                            "Ir para o conteúdo principal",
                    },
                ),
            ).toHaveAttribute(
                "href",
                "#og3-main-content",
            );
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
        "shows tenant and current page context",
        () => {
            renderAppShell({
                path: "/clientes",
            });

            expect(
                screen.getByText(
                    "Marcenaria Galdino",
                ),
            ).toBeInTheDocument();

            expect(
                screen.getByText(
                    "Comercial • Clientes",
                ),
            ).toBeInTheDocument();
        },
    );

    it(
        "falls back when tenant is unavailable",
        () => {
            renderAppShell({
                activeTenantName: null,
            });

            expect(
                screen.getByText(
                    "Ambiente principal",
                ),
            ).toBeInTheDocument();

            expect(
                screen.getByText(
                    "Visão geral • Início",
                ),
            ).toBeInTheDocument();
        },
    );

    it(
        "updates the browser title",
        () => {
            renderAppShell({
                path: "/materiais",
            });

            expect(
                document.title,
            ).toBe(
                "Materiais | OrganizeG3",
            );
        },
    );

    it(
        "shows the platform connection status",
        () => {
            renderAppShell();

            const status =
                screen.getByRole(
                    "status",
                );

            expect(
                status,
            ).toHaveAttribute(
                "aria-live",
                "polite",
            );

            expect(
                status,
            ).toHaveTextContent(
                "Online",
            );
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