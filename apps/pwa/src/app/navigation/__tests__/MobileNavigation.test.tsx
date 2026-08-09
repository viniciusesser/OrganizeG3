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
    vi,
} from "vitest";

import {
    MobileNavigation,
} from "@/app/navigation/MobileNavigation";

function renderMobileNavigation({
    isOpen = true,
    onClose = vi.fn(),
}: {
    readonly isOpen?: boolean;
    readonly onClose?: () => void;
} = {}) {
    render(
        <MemoryRouter>
            <MobileNavigation
                isOpen={isOpen}
                onClose={onClose}
            />
        </MemoryRouter>,
    );

    return {
        onClose,
    };
}

describe("MobileNavigation", () => {
    it(
        "does not render when closed",
        () => {
            renderMobileNavigation({
                isOpen: false,
            });

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

    it(
        "renders a modal navigation drawer when open",
        () => {
            renderMobileNavigation();

            const dialog =
                screen.getByRole(
                    "dialog",
                    {
                        name:
                            "Navegação móvel",
                    },
                );

            expect(
                dialog,
            ).toBeInTheDocument();

            expect(
                dialog,
            ).toHaveAttribute(
                "aria-modal",
                "true",
            );

            expect(
                screen.getByRole(
                    "navigation",
                    {
                        name:
                            "Módulos do sistema no celular",
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
        },
    );

    it(
        "closes from the close button",
        () => {
            const onClose = vi.fn();

            renderMobileNavigation({
                onClose,
            });

            fireEvent.click(
                screen.getByRole(
                    "button",
                    {
                        name: "Fechar",
                    },
                ),
            );

            expect(
                onClose,
            ).toHaveBeenCalledTimes(1);
        },
    );

    it(
        "closes from the backdrop",
        () => {
            const onClose = vi.fn();

            renderMobileNavigation({
                onClose,
            });

            fireEvent.click(
                screen.getByRole(
                    "button",
                    {
                        name:
                            "Fechar navegação",
                    },
                ),
            );

            expect(
                onClose,
            ).toHaveBeenCalledTimes(1);
        },
    );

    it(
        "closes after selecting a route",
        () => {
            const onClose = vi.fn();

            renderMobileNavigation({
                onClose,
            });

            fireEvent.click(
                screen.getByRole(
                    "link",
                    {
                        name: "Clientes",
                    },
                ),
            );

            expect(
                onClose,
            ).toHaveBeenCalledTimes(1);
        },
    );
});