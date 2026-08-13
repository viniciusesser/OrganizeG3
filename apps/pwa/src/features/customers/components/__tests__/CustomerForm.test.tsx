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
    CustomerForm,
} from "@/features/customers/components/CustomerForm";

function CustomerFormHarness() {
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
                Novo cliente
            </button>

            {isOpen ? (
                <CustomerForm
                    isSubmitting={
                        false
                    }
                    onCancel={() => {
                        setIsOpen(
                            false,
                        );
                    }}
                    onSubmit={
                        vi.fn()
                    }
                />
            ) : null}
        </>
    );
}

describe(
    "CustomerForm",
    () => {
        it(
            "moves focus to the customer name",
            () => {
                render(
                    <CustomerFormHarness />,
                );

                const openButton =
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Novo cliente",
                        },
                    );

                openButton.focus();

                fireEvent.click(
                    openButton,
                );

                expect(
                    screen.getByRole(
                        "textbox",
                        {
                            name:
                                "Nome do cliente *",
                        },
                    ),
                ).toHaveFocus();
            },
        );

        it(
            "keeps tab navigation inside the form",
            () => {
                render(
                    <CustomerFormHarness />,
                );

                const openButton =
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Novo cliente",
                        },
                    );

                openButton.focus();

                fireEvent.click(
                    openButton,
                );

                const closeButton =
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Fechar formulário",
                        },
                    );

                const saveButton =
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Salvar cliente",
                        },
                    );

                saveButton.focus();

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
                    saveButton,
                ).toHaveFocus();
            },
        );

        it(
            "closes with Escape and restores focus",
            () => {
                render(
                    <CustomerFormHarness />,
                );

                const openButton =
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Novo cliente",
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
                        "dialog",
                        {
                            name:
                                "Novo cliente",
                        },
                    ),
                ).not.toBeInTheDocument();

                expect(
                    openButton,
                ).toHaveFocus();
            },
        );
    },
);