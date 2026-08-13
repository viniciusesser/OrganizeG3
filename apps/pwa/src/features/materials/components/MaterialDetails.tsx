import {
    useId,
} from "react";

import type {
    Brand,
} from "@/features/materials/model/brand";
import {
    formatBrandOption,
} from "@/features/materials/model/brand";
import type {
    Material,
} from "@/features/materials/model/material";
import {
    useAccessibleOverlay,
} from "@/shared/hooks/useAccessibleOverlay";
import {
    Badge,
    Button,
    Heading,
    Text,
} from "@/shared/components/ui";

export interface MaterialDetailsProps {
    readonly material: Material;
    readonly brand?: Brand;
    readonly canEdit: boolean;
    readonly canDeactivate: boolean;
    readonly canReactivate: boolean;
    readonly isSubmitting: boolean;
    readonly onClose: () => void;
    readonly onEdit: (
        material: Material,
    ) => void;
    readonly onDeactivate: (
        material: Material,
    ) => void;
    readonly onReactivate: (
        material: Material,
    ) => void;
}

function formatBrand(
    material: Material,
    brand?: Brand,
): string {
    if (
        material.brand_id === null
    ) {
        return "Sem marca";
    }

    if (
        brand === undefined
    ) {
        return "Marca indisponível";
    }

    return formatBrandOption(
        brand,
    );
}

export function MaterialDetails({
    material,
    brand,
    canEdit,
    canDeactivate,
    canReactivate,
    isSubmitting,
    onClose,
    onEdit,
    onDeactivate,
    onReactivate,
}: MaterialDetailsProps) {
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
                                material.is_active
                                    ? "success"
                                    : "neutral"
                            }
                        >
                            {
                                material.is_active
                                    ? "Ativo"
                                    : "Inativo"
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
                                    material.name
                                }
                            </span>
                        </Heading>

                        <Text
                            tone="secondary"
                        >
                            {
                                material.code
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
                                    material.code
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
                                    material.name
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Categoria
                            </dt>

                            <dd>
                                {
                                    material.category
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Unidade
                            </dt>

                            <dd>
                                {
                                    material.unit
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Marca
                            </dt>

                            <dd>
                                {
                                    formatBrand(
                                        material,
                                        brand,
                                    )
                                }
                            </dd>
                        </div>

                        {brand !==
                            undefined && (
                                <div
                                    className="og3-details-grid__item"
                                >
                                    <dt>
                                        Status da marca
                                    </dt>

                                    <dd>
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
                                    </dd>
                                </div>
                            )}
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
                                    material,
                                );
                            }}
                            variant="secondary"
                        >
                            Editar material
                        </Button>
                    )}

                    {material.is_active &&
                        canDeactivate && (
                            <Button
                                disabled={
                                    isSubmitting
                                }
                                onClick={() => {
                                    onDeactivate(
                                        material,
                                    );
                                }}
                                variant="danger"
                            >
                                Inativar material
                            </Button>
                        )}

                    {!material.is_active &&
                        canReactivate && (
                            <Button
                                disabled={
                                    isSubmitting
                                }
                                onClick={() => {
                                    onReactivate(
                                        material,
                                    );
                                }}
                            >
                                Reativar material
                            </Button>
                        )}
                </footer>
            </div>
        </div>
    );
}