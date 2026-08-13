import {
    useState,
} from "react";
import {
    fireEvent,
    render,
    screen,
} from "@testing-library/react";
import {
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    useAccessibleOverlay,
} from "@/shared/hooks/useAccessibleOverlay";

interface TestOverlayProps {
    readonly onClose: () => void;
}

function TestOverlay({
    onClose,
}: TestOverlayProps) {
    const {
        overlayRef,
    } = useAccessibleOverlay<HTMLDivElement>({
        onClose,
    });

    return (
        <div
            aria-label="Overlay de teste"
            aria-modal="true"
            ref={overlayRef}
            role="dialog"
            tabIndex={-1}
        >
            <button type="button">
                Primeira ação
            </button>

            <button type="button">
                Última ação
            </button>
        </div>
    );
}

function OverlayHarness() {
    const [
        isOpen,
        setIsOpen,
    ] = useState(false);

    return (
        <>
            <button
                onClick={() => {
                    setIsOpen(true);
                }}
                type="button"
            >
                Abrir overlay
            </button>

            {isOpen ? (
                <TestOverlay
                    onClose={() => {
                        setIsOpen(false);
                    }}
                />
            ) : null}
        </>
    );
}

describe(
    "useAccessibleOverlay",
    () => {
        it(
            "moves focus into the overlay when it opens",
            () => {
                render(
                    <OverlayHarness />,
                );

                const openButton =
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Abrir overlay",
                        },
                    );

                openButton.focus();

                fireEvent.click(
                    openButton,
                );

                expect(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Primeira ação",
                        },
                    ),
                ).toHaveFocus();
            },
        );

        it(
            "keeps tab navigation inside the overlay",
            () => {
                render(
                    <OverlayHarness />,
                );

                const openButton =
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Abrir overlay",
                        },
                    );

                openButton.focus();

                fireEvent.click(
                    openButton,
                );

                const firstButton =
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Primeira ação",
                        },
                    );

                const lastButton =
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Última ação",
                        },
                    );

                lastButton.focus();

                fireEvent.keyDown(
                    document,
                    {
                        key: "Tab",
                    },
                );

                expect(
                    firstButton,
                ).toHaveFocus();

                fireEvent.keyDown(
                    document,
                    {
                        key: "Tab",
                        shiftKey: true,
                    },
                );

                expect(
                    lastButton,
                ).toHaveFocus();
            },
        );

        it(
            "closes with Escape and restores focus",
            () => {
                render(
                    <OverlayHarness />,
                );

                const openButton =
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Abrir overlay",
                        },
                    );

                openButton.focus();

                expect(
                    openButton,
                ).toHaveFocus();

                fireEvent.click(
                    openButton,
                );

                expect(
                    screen.getByRole(
                        "dialog",
                        {
                            name:
                                "Overlay de teste",
                        },
                    ),
                ).toBeInTheDocument();

                fireEvent.keyDown(
                    document,
                    {
                        key: "Escape",
                    },
                );

                expect(
                    screen.queryByRole(
                        "dialog",
                        {
                            name:
                                "Overlay de teste",
                        },
                    ),
                ).not.toBeInTheDocument();

                expect(
                    openButton,
                ).toHaveFocus();
            },
        );

        it(
            "locks and restores body scrolling",
            () => {
                const {
                    unmount,
                } = render(
                    <TestOverlay
                        onClose={vi.fn()}
                    />,
                );

                expect(
                    document.body,
                ).toHaveClass(
                    "og3-overlay-open",
                );

                unmount();

                expect(
                    document.body,
                ).not.toHaveClass(
                    "og3-overlay-open",
                );
            },
        );
    },
);