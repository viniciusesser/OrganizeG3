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
    DataTable,
    Pagination,
} from "@/shared/components/patterns";

describe("DataTable", () => {
    it("preserves the responsive table structure and cell labels", () => {
        render(
            <DataTable aria-label="Clientes cadastrados">
                <thead>
                    <tr>
                        <th scope="col">
                            Cliente
                        </th>
                    </tr>
                </thead>

                <tbody>
                    <tr>
                        <td data-label="Cliente">
                            Cliente teste
                        </td>
                    </tr>
                </tbody>
            </DataTable>,
        );

        const table = screen.getByRole(
            "table",
            {
                name: "Clientes cadastrados",
            },
        );

        expect(table).toHaveClass(
            "og3-data-table",
        );
        expect(table.parentElement).toHaveClass(
            "og3-data-table-wrapper",
        );
        expect(
            screen.getByRole("cell"),
        ).toHaveAttribute(
            "data-label",
            "Cliente",
        );
    });
});

describe("Pagination", () => {
    it("shows the current page and triggers navigation", () => {
        const onNext = vi.fn();
        const onPrevious = vi.fn();

        render(
            <Pagination
                aria-label="Paginação de clientes"
                currentPage={2}
                hasNext
                hasPrevious
                onNext={onNext}
                onPrevious={onPrevious}
            />,
        );

        expect(
            screen.getByText("Página 2"),
        ).toBeInTheDocument();

        fireEvent.click(
            screen.getByRole(
                "button",
                {
                    name: "Anterior",
                },
            ),
        );
        fireEvent.click(
            screen.getByRole(
                "button",
                {
                    name: "Próxima",
                },
            ),
        );

        expect(onPrevious).toHaveBeenCalledOnce();
        expect(onNext).toHaveBeenCalledOnce();
    });

    it("disables navigation while loading or at a boundary", () => {
        const { rerender } = render(
            <Pagination
                aria-label="Paginação de clientes"
                currentPage={1}
                hasNext
                hasPrevious={false}
                onNext={vi.fn()}
                onPrevious={vi.fn()}
            />,
        );

        expect(
            screen.getByRole(
                "button",
                {
                    name: "Anterior",
                },
            ),
        ).toBeDisabled();
        expect(
            screen.getByRole(
                "button",
                {
                    name: "Próxima",
                },
            ),
        ).toBeEnabled();

        rerender(
            <Pagination
                aria-label="Paginação de clientes"
                currentPage={1}
                hasNext
                hasPrevious
                isLoading
                onNext={vi.fn()}
                onPrevious={vi.fn()}
            />,
        );

        expect(
            screen.getByRole(
                "button",
                {
                    name: "Anterior",
                },
            ),
        ).toBeDisabled();
        expect(
            screen.getByRole(
                "button",
                {
                    name: "Próxima",
                },
            ),
        ).toBeDisabled();
    });
});