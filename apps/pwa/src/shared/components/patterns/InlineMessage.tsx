import type {
    HTMLAttributes,
    ReactNode,
} from "react";

export type InlineMessageTone =
    | "danger"
    | "success";

export interface InlineMessageProps
    extends Omit<
        HTMLAttributes<HTMLDivElement>,
        "children"
    > {
    readonly children: ReactNode;
    readonly tone: InlineMessageTone;
}

export function InlineMessage({
    children,
    className,
    role,
    tone,
    ...messageProps
}: InlineMessageProps) {
    const messageClassName = [
        "og3-inline-message",
        `og3-inline-message--${tone}`,
        className,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <div
            {...messageProps}
            className={messageClassName}
            role={
                role ??
                (tone === "danger"
                    ? "alert"
                    : "status")
            }
        >
            {children}
        </div>
    );
}