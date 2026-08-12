import type {
    ReactNode,
    TableHTMLAttributes,
} from "react";

export interface DataTableProps
    extends Omit<
        TableHTMLAttributes<HTMLTableElement>,
        "children"
    > {
    readonly children: ReactNode;
}

export function DataTable({
    children,
    className,
    ...tableProps
}: DataTableProps) {
    const tableClassName = [
        "og3-data-table",
        className,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <div className="og3-data-table-wrapper">
            <table
                {...tableProps}
                className={tableClassName}
            >
                {children}
            </table>
        </div>
    );
}