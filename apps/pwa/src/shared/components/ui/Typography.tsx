import type {
    HTMLAttributes,
    ReactNode,
} from "react";

export type HeadingLevel =
    | 1
    | 2
    | 3
    | 4;

export interface HeadingProps {
    readonly level?: HeadingLevel;
    readonly children: ReactNode;
    readonly className?: string;
}

export function Heading({
    level = 2,
    children,
    className,
}: HeadingProps) {
    const classes = [
        "og3-heading",
        `og3-heading--${level}`,
        className,
    ]
        .filter(Boolean)
        .join(" ");

    switch (level) {
        case 1:
            return (
                <h1 className={classes}>
                    {children}
                </h1>
            );

        case 2:
            return (
                <h2 className={classes}>
                    {children}
                </h2>
            );

        case 3:
            return (
                <h3 className={classes}>
                    {children}
                </h3>
            );

        case 4:
            return (
                <h4 className={classes}>
                    {children}
                </h4>
            );
    }
}

export type TextTone =
    | "primary"
    | "secondary"
    | "muted";

export type TextSize =
    | "sm"
    | "md"
    | "lg";

export interface TextProps
    extends HTMLAttributes<HTMLParagraphElement> {
    readonly tone?: TextTone;
    readonly size?: TextSize;
}

export function Text({
    tone = "primary",
    size = "md",
    className,
    ...props
}: TextProps) {
    const classes = [
        "og3-text",
        tone !== "primary"
            ? `og3-text--${tone}`
            : undefined,
        size !== "md"
            ? `og3-text--${size}`
            : undefined,
        className,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <p
            {...props}
            className={classes}
        />
    );
}