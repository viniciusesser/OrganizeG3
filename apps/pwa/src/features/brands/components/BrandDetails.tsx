import {
    useId,
} from "react";

import type {
    Brand,
} from "@/features/brands/model/brand";
import {
    useAccessibleOverlay,
} from "@/shared/hooks/useAccessibleOverlay";
import {
    Badge,
    Button,
    Heading,
    Text,
} from "@/shared/components/ui";

export interface BrandDetailsProps {
    readonly brand: Brand;
    readonly canEdit: boolean;
    readonly canDeactivate: boolean;
    readonly canReactivate: boolean;
    readonly isSubmitting: boolean;
    readonly onClose: () => void;
    readonly onEdit: (
        brand: Brand,
    ) => void;
    readonly onDeactivate: (
        brand: Brand,
    ) => void;
    readonly onReactivate: (
        brand: Brand,
    ) => void;
}

export function BrandDetails({
    brand,
    canEdit,
    canDeactivate,
    canReactivate,
    isSubmitting,
    onClose,
    onEdit,
    onDeactivate,
    onReactivate,
}: BrandDetailsProps) {
    const titleId =
        useId();

    const {
        overlayRef,
    } = useAccessibleOverlay<HTMLDivElement>({
        closeOnEscape:
            !isSubmitting,
        onClose,
    });

    return (
        <div
            aria-labelledby={
                titleId
            }
            aria-modal="true"
            className="og3-dialog-backdrop"
            ref={overlayRef}
            role="dialog"
            tabIndex={-1}
        >
            <div
                className={[
                    "og3-dialog",
                    "og3-dialog--md",
                ].join(" ")}
            >
                <header
                    className="og3-dialog__header"
                >
                    <div
                        className="og3-dialog__heading"
                    >
                        <Badge
                            variant={
                                brand.is_active
                                    ? "success"
                                    : "neutral"
                            }
                        >
                            {
                                brand.is_active
                                    ? "Ativa"
                                    : "Inativa"
                            }
                        </Badge>

                        <Heading
                            level={3}
                        >
                            <span
                                id={
                                    titleId
                                }
                            >
                                {
                                    brand.name
                                }
                            </span>
                        </Heading>

                        <Text
                            tone="secondary"
                        >
                            {
                                brand.code
                            }
                        </Text>
                    </div>

                    <Button
                        aria-label="Fechar detalhes"
                        data-og3-autofocus="true"
                        disabled={
                            isSubmitting
                        }
                        onClick={
                            onClose
                        }
                        size="sm"
                        variant="secondary"
                    >
                        Fechar
                    </Button>
                </header>

                <div
                    className="og3-dialog__body"
                >
                    <dl
                        className="og3-details-grid"
                    >
                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Código
                            </dt>

                            <dd>
                                {
                                    brand.code
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Nome
                            </dt>

                            <dd>
                                {
                                    brand.name
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Status
                            </dt>

                            <dd>
                                {
                                    brand.is_active
                                        ? "Ativa"
                                        : "Inativa"
                                }
                            </dd>
                        </div>
                    </dl>
                </div>

                <footer
                    className="og3-dialog__footer"
                >
                    {canEdit && (
                        <Button
                            disabled={
                                isSubmitting
                            }
                            onClick={() => {
                                onEdit(
                                    brand,
                                );
                            }}
                            variant="secondary"
                        >
                            Editar marca
                        </Button>
                    )}

                    {brand.is_active &&
                        canDeactivate && (
                            <Button
                                disabled={
                                    isSubmitting
                                }
                                onClick={() => {
                                    onDeactivate(
                                        brand,
                                    );
                                }}
                                variant="danger"
                            >
                                Inativar marca
                            </Button>
                        )}

                    {!brand.is_active &&
                        canReactivate && (
                            <Button
                                disabled={
                                    isSubmitting
                                }
                                onClick={() => {
                                    onReactivate(
                                        brand,
                                    );
                                }}
                            >
                                Reativar marca
                            </Button>
                        )}
                </footer>
            </div>
        </div>
    );
}