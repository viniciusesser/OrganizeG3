import {
    render,
    screen,
} from "@testing-library/react";
import {
    describe,
    expect,
    it,
} from "vitest";

import {
    ThemePreviewRoute,
} from "@/routes/theme-preview/ThemePreviewRoute";

describe("ThemePreviewRoute", () => {
    it(
        "renders the OrganizeG3 design system preview",
        () => {
            render(
                <ThemePreviewRoute />,
            );

            expect(
                screen.getByRole(
                    "heading",
                    {
                        level: 1,
                        name: "OrganizeG3",
                    },
                ),
            ).toBeInTheDocument();

            expect(
                screen.getByRole(
                    "heading",
                    {
                        name: "Tipografia",
                    },
                ),
            ).toBeInTheDocument();

            expect(
                screen.getByRole(
                    "heading",
                    {
                        name: "Botões",
                    },
                ),
            ).toBeInTheDocument();

            expect(
                screen.getByRole(
                    "heading",
                    {
                        name: "Campos",
                    },
                ),
            ).toBeInTheDocument();

            expect(
                screen.getByRole(
                    "heading",
                    {
                        name: "Badges e estados",
                    },
                ),
            ).toBeInTheDocument();

            expect(
                screen.getByRole(
                    "heading",
                    {
                        name: "Cards",
                    },
                ),
            ).toBeInTheDocument();

            expect(
                screen.getByRole(
                    "heading",
                    {
                        name: "Superfícies",
                    },
                ),
            ).toBeInTheDocument();
        },
    );
});