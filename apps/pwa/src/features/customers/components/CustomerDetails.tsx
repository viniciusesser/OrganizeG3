import {
    useId,
} from "react";

import type {
    Customer,
} from "@/features/customers/model/customer";
import {
    formatCustomerDocument,
    formatCustomerPhone,
    getCustomerTypeLabel,
} from "@/features/customers/model/customer";
import {
    useAccessibleOverlay,
} from "@/shared/hooks/useAccessibleOverlay";
import {
    Badge,
    Button,
    Heading,
    Text,
} from "@/shared/components/ui";

export interface CustomerDetailsProps {
    readonly customer: Customer;
    readonly canEdit: boolean;
    readonly canArchive: boolean;
    readonly canReactivate: boolean;
    readonly isSubmitting: boolean;
    readonly onClose: () => void;
    readonly onEdit: (
        customer: Customer,
    ) => void;
    readonly onArchive: (
        customer: Customer,
    ) => void;
    readonly onReactivate: (
        customer: Customer,
    ) => void;
}

export function CustomerDetails({
    customer,
    canEdit,
    canArchive,
    canReactivate,
    isSubmitting,
    onClose,
    onEdit,
    onArchive,
    onReactivate,
}: CustomerDetailsProps) {
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
                                customer.is_active
                                    ? "success"
                                    : "neutral"
                            }
                        >
                            {
                                customer.is_active
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
                                    customer.name
                                }
                            </span>
                        </Heading>

                        <Text
                            tone="secondary"
                        >
                            {
                                customer.code
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
                                Tipo de pessoa
                            </dt>

                            <dd>
                                {
                                    getCustomerTypeLabel(
                                        customer.customer_type,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Documento
                            </dt>

                            <dd>
                                {
                                    formatCustomerDocument(
                                        customer.document_number,
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
                                    formatCustomerPhone(
                                        customer.phone,
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
                                    customer.email ??
                                    "—"
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
                                    customer,
                                );
                            }}
                            variant="secondary"
                        >
                            Editar cliente
                        </Button>
                    )}

                    {customer.is_active &&
                        canArchive && (
                            <Button
                                disabled={
                                    isSubmitting
                                }
                                onClick={() => {
                                    onArchive(
                                        customer,
                                    );
                                }}
                                variant="danger"
                            >
                                Inativar cliente
                            </Button>
                        )}

                    {!customer.is_active &&
                        canReactivate && (
                            <Button
                                disabled={
                                    isSubmitting
                                }
                                onClick={() => {
                                    onReactivate(
                                        customer,
                                    );
                                }}
                            >
                                Reativar cliente
                            </Button>
                        )}
                </footer>
            </div>
        </div>
    );
}