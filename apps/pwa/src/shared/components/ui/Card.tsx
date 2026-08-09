import type {
    HTMLAttributes,
    ReactNode,
} from "react";

export interface CardProps
    extends HTMLAttributes<HTMLElement> {
    readonly header?: ReactNode;
    readonly footer?: ReactNode;
}

export function Card({
    header,
    footer,
    children,
    className,
    ...props
}: CardProps) {
    const classes = [
        "og3-card",
        className,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <article
            {...props}
            className={classes}
        >
            {header !== undefined && (
                <header className="og3-card__header">
                    {header}
                </header>
            )}

            <div className="og3-card__body">
                {children}
            </div>

            {footer !== undefined && (
                <footer className="og3-card__footer">
                    {footer}
                </footer>
            )}
        </article>
    );
}