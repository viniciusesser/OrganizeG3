import type {
    HTMLAttributes,
    ReactNode,
} from "react";

import {
    Heading,
    Text,
} from "@/shared/components/ui";

export interface StatePanelProps
    extends Omit<
        HTMLAttributes<HTMLDivElement>,
        "children"
    > {
    readonly actions?: ReactNode;
    readonly description: ReactNode;
    readonly heading: ReactNode;
}

export function StatePanel({
    actions,
    className,
    description,
    heading,
    ...panelProps
}: StatePanelProps) {
    const panelClassName = [
        "og3-state-panel",
        className,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <div
            {...panelProps}
            className={panelClassName}
        >
            <Heading level={3}>
                {heading}
            </Heading>

            <Text tone="secondary">
                {description}
            </Text>

            {actions}
        </div>
    );
}