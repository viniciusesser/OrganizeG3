import type {
    ButtonHTMLAttributes,
} from "react";

export type ButtonVariant =
    | "primary"
    | "secondary"
    | "danger";

export type ButtonSize =
    | "sm"
    | "md"
    | "lg";

export interface ButtonProps
    extends ButtonHTMLAttributes<HTMLButtonElement> {
    readonly variant?: ButtonVariant;
    readonly size?: ButtonSize;
}

export function Button({
    variant = "primary",
    size = "md",
    className,
    type = "button",
    ...props
}: ButtonProps) {
    const classes = [
        "og3-button",
        `og3-button--${variant}`,
        `og3-button--${size}`,
        className,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <button
            {...props}
            className={classes}
            type={type}
        />
    );
}