import type {
    FormHTMLAttributes,
    ReactNode,
} from "react";

export interface FilterBarProps
    extends Omit<
        FormHTMLAttributes<HTMLFormElement>,
        "children"
    > {
    readonly actions?: ReactNode;
    readonly children: ReactNode;
}

export function FilterBar({
    actions,
    children,
    className,
    ...formProps
}: FilterBarProps) {
    const formClassName = [
        "og3-filter-bar",
        className,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <form
            {...formProps}
            className={formClassName}
        >
            {children}

            {actions !== undefined && (
                <div className="og3-filter-bar__actions">
                    {actions}
                </div>
            )}
        </form>
    );
}