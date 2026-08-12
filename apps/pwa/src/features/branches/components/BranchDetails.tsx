import { useEffect, useId } from "react";

import type {
    Branch,
} from "@/features/branches/model/branch";
import {
    Badge,
    Button,
    Heading,
    Text,
} from "@/shared/components/ui";

export interface BranchDetailsProps {
    readonly branch: Branch;
    readonly canEdit: boolean;
    readonly canDeactivate: boolean;
    readonly canReactivate: boolean;
    readonly isSubmitting: boolean;
    readonly onClose: () => void;
    readonly onEdit: (branch: Branch) => void;
    readonly onDeactivate: (branch: Branch) => void;
    readonly onReactivate: (branch: Branch) => void;
}

function formatOptionalValue(
    value: string | null,
): string {
    return value?.trim() || "—";
}

function formatAddress(
    branch: Branch,
): string {
    const streetLine = [
        branch.street,
        branch.number,
    ]
        .filter(
            (value): value is string =>
                value !== null &&
                value.trim().length > 0,
        )
        .join(", ");

    const cityLine = [
        branch.district,
        branch.city,
        branch.state,
        branch.postal_code,
    ]
        .filter(
            (value): value is string =>
                value !== null &&
                value.trim().length > 0,
        )
        .join(" — ");

    return (
        [streetLine, cityLine]
            .filter((value) => value.length > 0)
            .join(" | ") ||
        "—"
    );
}

export function BranchDetails({
    branch,
    canEdit,
    canDeactivate,
    canReactivate,
    isSubmitting,
    onClose,
    onEdit,
    onDeactivate,
    onReactivate,
}: BranchDetailsProps) {
    const titleId = useId();

    useEffect(() => {
        const handleKeyDown = (
            event: KeyboardEvent,
        ) => {
            if (event.key === "Escape") {
                onClose();
            }
        };

        window.addEventListener(
            "keydown",
            handleKeyDown,
        );

        return () => {
            window.removeEventListener(
                "keydown",
                handleKeyDown,
            );
        };
    }, [onClose]);

    return (
        <div
            aria-labelledby={titleId}
            aria-modal="true"
            className="og3-dialog-backdrop"
            role="dialog"
        >
            <div className="og3-dialog og3-dialog--md">
                <header className="og3-dialog__header">
                    <div className="og3-dialog__heading">
                        <div className="og3-data-table__actions">
                            <Badge
                                variant={
                                    branch.is_active
                                        ? "success"
                                        : "neutral"
                                }
                            >
                                {branch.is_active
                                    ? "Ativa"
                                    : "Inativa"}
                            </Badge>

                            <Badge
                                variant={
                                    branch.is_headquarters
                                        ? "accent"
                                        : "neutral"
                                }
                            >
                                {branch.is_headquarters
                                    ? "Matriz"
                                    : "Filial"}
                            </Badge>
                        </div>

                        <Heading level={3}>
                            <span id={titleId}>
                                {branch.name}
                            </span>
                        </Heading>

                        <Text tone="secondary">
                            {branch.code}
                        </Text>
                    </div>

                    <Button
                        aria-label="Fechar detalhes"
                        disabled={isSubmitting}
                        onClick={onClose}
                        size="sm"
                        variant="secondary"
                    >
                        Fechar
                    </Button>
                </header>

                <div className="og3-dialog__body">
                    <dl className="og3-details-grid">
                        <div className="og3-details-grid__item">
                            <dt>Razão social</dt>
                            <dd>
                                {formatOptionalValue(
                                    branch.legal_name,
                                )}
                            </dd>
                        </div>

                        <div className="og3-details-grid__item">
                            <dt>CNPJ ou documento</dt>
                            <dd>
                                {formatOptionalValue(
                                    branch.document_number,
                                )}
                            </dd>
                        </div>

                        <div className="og3-details-grid__item">
                            <dt>Inscrição estadual</dt>
                            <dd>
                                {formatOptionalValue(
                                    branch.state_registration,
                                )}
                            </dd>
                        </div>

                        <div className="og3-details-grid__item">
                            <dt>Telefone</dt>
                            <dd>
                                {formatOptionalValue(
                                    branch.phone,
                                )}
                            </dd>
                        </div>

                        <div className="og3-details-grid__item">
                            <dt>Email</dt>
                            <dd>
                                {formatOptionalValue(
                                    branch.email,
                                )}
                            </dd>
                        </div>

                        <div className="og3-details-grid__item">
                            <dt>Site</dt>
                            <dd>
                                {formatOptionalValue(
                                    branch.website,
                                )}
                            </dd>
                        </div>

                        <div className="og3-details-grid__item">
                            <dt>Endereço</dt>
                            <dd>
                                {formatAddress(branch)}
                            </dd>
                        </div>
                    </dl>
                </div>

                <footer className="og3-dialog__footer">
                    {canEdit && (
                        <Button
                            disabled={isSubmitting}
                            onClick={() => {
                                onEdit(branch);
                            }}
                            variant="secondary"
                        >
                            Editar filial
                        </Button>
                    )}

                    {branch.is_active &&
                        canDeactivate && (
                            <Button
                                disabled={isSubmitting}
                                onClick={() => {
                                    onDeactivate(branch);
                                }}
                                variant="danger"
                            >
                                Inativar filial
                            </Button>
                        )}

                    {!branch.is_active &&
                        canReactivate && (
                            <Button
                                disabled={isSubmitting}
                                onClick={() => {
                                    onReactivate(branch);
                                }}
                            >
                                Reativar filial
                            </Button>
                        )}
                </footer>
            </div>
        </div>
    );
}