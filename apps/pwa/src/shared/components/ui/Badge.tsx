import type {
    HTMLAttributes,
} from "react";

export type BadgeVariant =
    | "neutral"
    | "success"
    | "warning"
    | "danger"
    | "accent";

export interface BadgeProps
    extends HTMLAttributes<HTMLSpanElement> {
    readonly variant?: BadgeVariant;
}

export function Badge({
    variant = "neutral",
    className,
    ...props
}: BadgeProps) {
    const classes = [
        "og3-badge",
        `og3-badge--${variant}`,
        className,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <span
            {...props}
            className={classes}
        />
    );
}