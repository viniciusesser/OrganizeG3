import {
    useId,
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
    ConfirmationDialog,
} from "@/shared/components/patterns/ConfirmationDialog";

function ConfirmationHarness() {
    const titleId =
        useId();

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
                Inativar cliente
            </button>

            {isOpen ? (
                <ConfirmationDialog
                    confirmLabel="Inativar"
                    description="Esta ação inativará o cliente."
                    onCancel={() => {
                        setIsOpen(
                            false,
                        );
                    }}
                    onConfirm={
                        vi.fn()
                    }
                    pendingLabel="Inativando..."
                    title="Confirmar inativação"
                    titleId={
                        titleId
                    }
                />
            ) : null}
        </>
    );
}

describe(
    "ConfirmationDialog",
    () => {
        it(
            "focuses the safe action",
            () => {
                render(
                    <ConfirmationHarness />,
                );

                const openButton =
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Inativar cliente",
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
                                "Cancelar",
                        },
                    ),
                ).toHaveFocus();
            },
        );

        it(
            "keeps focus inside the confirmation",
            () => {
                render(
                    <ConfirmationHarness />,
                );

                const openButton =
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Inativar cliente",
                        },
                    );

                openButton.focus();

                fireEvent.click(
                    openButton,
                );

                const cancelButton =
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Cancelar",
                        },
                    );

                const confirmButton =
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Inativar",
                        },
                    );

                confirmButton.focus();

                fireEvent.keyDown(
                    document,
                    {
                        key: "Tab",
                    },
                );

                expect(
                    cancelButton,
                ).toHaveFocus();

                fireEvent.keyDown(
                    document,
                    {
                        key: "Tab",
                        shiftKey: true,
                    },
                );

                expect(
                    confirmButton,
                ).toHaveFocus();
            },
        );

        it(
            "closes with Escape and restores focus",
            () => {
                render(
                    <ConfirmationHarness />,
                );

                const openButton =
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Inativar cliente",
                        },
                    );

                openButton.focus();

                fireEvent.click(
                    openButton,
                );

                fireEvent.keyDown(
                    document,
                    {
                        key: "Escape",
                    },
                );

                expect(
                    screen.queryByRole(
                        "alertdialog",
                    ),
                ).not.toBeInTheDocument();

                expect(
                    openButton,
                ).toHaveFocus();
            },
        );

        it(
            "does not close with Escape while submitting",
            () => {
                const onCancel =
                    vi.fn();

                render(
                    <ConfirmationDialog
                        confirmLabel="Inativar"
                        description="Esta ação inativará o cliente."
                        isSubmitting
                        onCancel={
                            onCancel
                        }
                        onConfirm={
                            vi.fn()
                        }
                        pendingLabel="Inativando..."
                        title="Confirmar inativação"
                        titleId="confirmation-title"
                    />,
                );

                fireEvent.keyDown(
                    document,
                    {
                        key: "Escape",
                    },
                );

                expect(
                    onCancel,
                ).not.toHaveBeenCalled();
            },
        );
    },
);