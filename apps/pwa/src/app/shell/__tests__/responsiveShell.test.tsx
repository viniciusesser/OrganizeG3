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
    AppShell,
} from "@/app/shell/AppShell";

describe("responsive AppShell foundation", () => {
    it(
        "keeps desktop and mobile navigation entry points in the same shell",
        () => {
            render(
                <MemoryRouter>
                    <AppShell>
                        <p>
                            Conteúdo responsivo
                        </p>
                    </AppShell>
                </MemoryRouter>,
            );

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
                    "button",
                    {
                        name: "Menu",
                    },
                ),
            ).toBeInTheDocument();
        },
    );

    it(
        "uses the shared main content region",
        () => {
            render(
                <MemoryRouter>
                    <AppShell>
                        <p>
                            Conteúdo responsivo
                        </p>
                    </AppShell>
                </MemoryRouter>,
            );

            const main =
                screen.getByRole("main");

            expect(main).toHaveClass(
                "og3-app-shell__main",
            );

            expect(
                screen.getByText(
                    "Conteúdo responsivo",
                ),
            ).toBeInTheDocument();
        },
    );
});