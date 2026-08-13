import {
    fireEvent,
    render,
    screen,
    within,
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
    const view = render(
        <MemoryRouter>
            <MobileNavigation
                activeTenantName="Marcenaria Galdino"
                isOpen={isOpen}
                onClose={onClose}
                pageContextLabel="Comercial • Clientes"
            />
        </MemoryRouter>,
    );

    return {
        ...view,
        onClose,
    };
}

describe(
    "MobileNavigation",
    () => {
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
                    dialog,
                ).toHaveAttribute(
                    "id",
                    "og3-mobile-navigation",
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
            "moves focus into the drawer",
            () => {
                renderMobileNavigation();

                expect(
                    screen.getByRole(
                        "button",
                        {
                            name: "Fechar",
                        },
                    ),
                ).toHaveFocus();
            },
        );

        it(
            "keeps tab navigation inside the drawer",
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

                const closeButton =
                    within(
                        dialog,
                    ).getByRole(
                        "button",
                        {
                            name: "Fechar",
                        },
                    );

                const links =
                    within(
                        dialog,
                    ).getAllByRole(
                        "link",
                    );

                const lastLink =
                    links[
                    links.length - 1
                    ];

                lastLink.focus();

                fireEvent.keyDown(
                    document,
                    {
                        key: "Tab",
                    },
                );

                expect(
                    closeButton,
                ).toHaveFocus();

                fireEvent.keyDown(
                    document,
                    {
                        key: "Tab",
                        shiftKey: true,
                    },
                );

                expect(
                    lastLink,
                ).toHaveFocus();
            },
        );

        it(
            "closes with Escape",
            () => {
                const onClose =
                    vi.fn();

                renderMobileNavigation({
                    onClose,
                });

                fireEvent.keyDown(
                    document,
                    {
                        key: "Escape",
                    },
                );

                expect(
                    onClose,
                ).toHaveBeenCalledTimes(
                    1,
                );
            },
        );

        it(
            "closes from the close button",
            () => {
                const onClose =
                    vi.fn();

                renderMobileNavigation({
                    onClose,
                });

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Fechar",
                        },
                    ),
                );

                expect(
                    onClose,
                ).toHaveBeenCalledTimes(
                    1,
                );
            },
        );

        it(
            "closes from the backdrop",
            () => {
                const onClose =
                    vi.fn();

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
                ).toHaveBeenCalledTimes(
                    1,
                );
            },
        );

        it(
            "closes after selecting a route",
            () => {
                const onClose =
                    vi.fn();

                renderMobileNavigation({
                    onClose,
                });

                fireEvent.click(
                    screen.getByRole(
                        "link",
                        {
                            name:
                                "Clientes",
                        },
                    ),
                );

                expect(
                    onClose,
                ).toHaveBeenCalledTimes(
                    1,
                );
            },
        );

        it(
            "shows tenant and current page context",
            () => {
                renderMobileNavigation();

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
    },
);