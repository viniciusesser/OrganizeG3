import type {
    HTMLAttributes,
} from "react";

export type SurfaceVariant =
    | "page"
    | "base"
    | "raised"
    | "overlay";

export interface SurfaceProps
    extends HTMLAttributes<HTMLDivElement> {
    readonly variant?: SurfaceVariant;
}

export function Surface({
    variant = "base",
    className,
    ...props
}: SurfaceProps) {
    const classes = [
        "og3-surface",
        `og3-surface--${variant}`,
        className,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <div
            {...props}
            className={classes}
        />
    );
}