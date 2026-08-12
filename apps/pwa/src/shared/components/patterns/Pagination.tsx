import type {
    HTMLAttributes,
    ReactNode,
} from "react";

import {
    Button,
    Text,
} from "@/shared/components/ui";

export interface PaginationProps
    extends Omit<
        HTMLAttributes<HTMLElement>,
        "aria-label" | "children"
    > {
    readonly "aria-label": string;
    readonly currentPage: number;
    readonly hasNext: boolean;
    readonly hasPrevious: boolean;
    readonly isLoading?: boolean;
    readonly nextLabel?: ReactNode;
    readonly onNext: () => void;
    readonly onPrevious: () => void;
    readonly previousLabel?: ReactNode;
}

export function Pagination({
    "aria-label": ariaLabel,
    className,
    currentPage,
    hasNext,
    hasPrevious,
    isLoading = false,
    nextLabel = "Próxima",
    onNext,
    onPrevious,
    previousLabel = "Anterior",
    ...navProps
}: PaginationProps) {
    const navClassName = [
        "og3-pagination",
        className,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <nav
            {...navProps}
            aria-label={ariaLabel}
            className={navClassName}
        >
            <Text
                size="sm"
                tone="secondary"
            >
                Página {currentPage}
            </Text>

            <div className="og3-pagination__actions">
                <Button
                    disabled={
                        isLoading ||
                        !hasPrevious
                    }
                    onClick={onPrevious}
                    size="sm"
                    type="button"
                    variant="secondary"
                >
                    {previousLabel}
                </Button>

                <Button
                    disabled={
                        isLoading ||
                        !hasNext
                    }
                    onClick={onNext}
                    size="sm"
                    type="button"
                    variant="secondary"
                >
                    {nextLabel}
                </Button>
            </div>
        </nav>
    );
}