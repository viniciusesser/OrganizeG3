import type {
    HTMLAttributes,
    ReactNode,
} from "react";

import {
    Badge,
    Heading,
    Text,
} from "@/shared/components/ui";

export interface PageHeaderProps
    extends Omit<
        HTMLAttributes<HTMLElement>,
        "children" | "title"
    > {
    readonly actions?: ReactNode;
    readonly badge: ReactNode;
    readonly description: ReactNode;
    readonly title: ReactNode;
}

export function PageHeader({
    actions,
    badge,
    className,
    description,
    title,
    ...headerProps
}: PageHeaderProps) {
    const headerClassName = [
        "og3-page-header",
        className,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <header
            {...headerProps}
            className={headerClassName}
        >
            <div className="og3-page-header__heading">
                <Badge variant="accent">
                    {badge}
                </Badge>

                <Heading level={1}>
                    {title}
                </Heading>

                <Text tone="secondary">
                    {description}
                </Text>
            </div>

            {actions}
        </header>
    );
}