import {
    useId,
} from "react";

import type {
    Supplier,
} from "@/features/suppliers/model/supplier";
import {
    formatSupplierAddress,
    formatSupplierDocument,
    formatSupplierPhone,
} from "@/features/suppliers/model/supplier";
import {
    useAccessibleOverlay,
} from "@/shared/hooks/useAccessibleOverlay";
import {
    Badge,
    Button,
    Heading,
    Text,
} from "@/shared/components/ui";

export interface SupplierDetailsProps {
    readonly supplier: Supplier;
    readonly canEdit: boolean;
    readonly canDeactivate: boolean;
    readonly canReactivate: boolean;
    readonly isSubmitting: boolean;
    readonly onClose: () => void;
    readonly onEdit: (
        supplier: Supplier,
    ) => void;
    readonly onDeactivate: (
        supplier: Supplier,
    ) => void;
    readonly onReactivate: (
        supplier: Supplier,
    ) => void;
}

function displayValue(
    value: string | null,
): string {
    return (
        value !== null &&
            value.trim().length > 0
            ? value
            : "—"
    );
}

export function SupplierDetails({
    supplier,
    canEdit,
    canDeactivate,
    canReactivate,
    isSubmitting,
    onClose,
    onEdit,
    onDeactivate,
    onReactivate,
}: SupplierDetailsProps) {
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
                                supplier.is_active
                                    ? "success"
                                    : "neutral"
                            }
                        >
                            {
                                supplier.is_active
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
                                    supplier.name
                                }
                            </span>
                        </Heading>

                        <Text
                            tone="secondary"
                        >
                            {
                                supplier.code
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
                                Nome fantasia
                            </dt>

                            <dd>
                                {
                                    displayValue(
                                        supplier.trade_name,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Razão social
                            </dt>

                            <dd>
                                {
                                    displayValue(
                                        supplier.legal_name,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                CPF ou CNPJ
                            </dt>

                            <dd>
                                {
                                    formatSupplierDocument(
                                        supplier.document_number,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Inscrição estadual
                            </dt>

                            <dd>
                                {
                                    displayValue(
                                        supplier.state_registration,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Pessoa de contato
                            </dt>

                            <dd>
                                {
                                    displayValue(
                                        supplier.contact_name,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Telefone
                            </dt>

                            <dd>
                                {
                                    formatSupplierPhone(
                                        supplier.phone,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Telefone secundário
                            </dt>

                            <dd>
                                {
                                    formatSupplierPhone(
                                        supplier.secondary_phone,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Email
                            </dt>

                            <dd>
                                {
                                    displayValue(
                                        supplier.email,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Email de faturamento
                            </dt>

                            <dd>
                                {
                                    displayValue(
                                        supplier.invoice_email,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Site
                            </dt>

                            <dd>
                                {
                                    displayValue(
                                        supplier.website,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Endereço
                            </dt>

                            <dd>
                                {
                                    formatSupplierAddress(
                                        supplier,
                                    )
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
                                    supplier,
                                );
                            }}
                            variant="secondary"
                        >
                            Editar fornecedor
                        </Button>
                    )}

                    {supplier.is_active &&
                        canDeactivate && (
                            <Button
                                disabled={
                                    isSubmitting
                                }
                                onClick={() => {
                                    onDeactivate(
                                        supplier,
                                    );
                                }}
                                variant="danger"
                            >
                                Inativar fornecedor
                            </Button>
                        )}

                    {!supplier.is_active &&
                        canReactivate && (
                            <Button
                                disabled={
                                    isSubmitting
                                }
                                onClick={() => {
                                    onReactivate(
                                        supplier,
                                    );
                                }}
                            >
                                Reativar fornecedor
                            </Button>
                        )}
                </footer>
            </div>
        </div>
    );
}