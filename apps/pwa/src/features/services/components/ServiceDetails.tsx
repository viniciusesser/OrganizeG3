import {
    useEffect,
    useId,
} from "react";

import type {
    Service,
} from "@/features/services/model/service";
import {
    getServiceExecutionModeLabel,
} from "@/features/services/model/service";
import {
    Badge,
    Button,
    Heading,
    Text,
} from "@/shared/components/ui";

export interface ServiceDetailsProps {
    readonly service: Service;
    readonly canEdit: boolean;
    readonly canDeactivate: boolean;
    readonly canReactivate: boolean;
    readonly isSubmitting: boolean;
    readonly onClose: () => void;
    readonly onEdit: (
        service: Service,
    ) => void;
    readonly onDeactivate: (
        service: Service,
    ) => void;
    readonly onReactivate: (
        service: Service,
    ) => void;
}

function formatDuration(
    minutes: number | null,
): string {
    if (minutes === null) {
        return "Não informada";
    }

    return `${minutes} ${minutes === 1
            ? "minuto"
            : "minutos"
        }`;
}

export function ServiceDetails({
    service,
    canEdit,
    canDeactivate,
    canReactivate,
    isSubmitting,
    onClose,
    onEdit,
    onDeactivate,
    onReactivate,
}: ServiceDetailsProps) {
    const titleId = useId();

    useEffect(
        () => {
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
        },
        [onClose],
    );

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
                        <Badge
                            variant={
                                service.is_active
                                    ? "success"
                                    : "neutral"
                            }
                        >
                            {service.is_active
                                ? "Ativo"
                                : "Inativo"}
                        </Badge>

                        <Heading level={3}>
                            <span id={titleId}>
                                {service.name}
                            </span>
                        </Heading>

                        <Text tone="secondary">
                            {service.code}
                        </Text>
                    </div>

                    <Button
                        aria-label="Fechar detalhes"
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
                            <dt>Código</dt>
                            <dd>
                                {service.code}
                            </dd>
                        </div>

                        <div className="og3-details-grid__item">
                            <dt>Nome</dt>
                            <dd>
                                {service.name}
                            </dd>
                        </div>

                        <div className="og3-details-grid__item">
                            <dt>Categoria</dt>
                            <dd>
                                {service.category}
                            </dd>
                        </div>

                        <div className="og3-details-grid__item">
                            <dt>Unidade</dt>
                            <dd>
                                {service.unit}
                            </dd>
                        </div>

                        <div className="og3-details-grid__item">
                            <dt>
                                Modo de execução
                            </dt>
                            <dd>
                                {getServiceExecutionModeLabel(
                                    service.execution_mode,
                                )}
                            </dd>
                        </div>

                        <div className="og3-details-grid__item">
                            <dt>
                                Duração estimada
                            </dt>
                            <dd>
                                {formatDuration(
                                    service
                                        .estimated_duration_minutes,
                                )}
                            </dd>
                        </div>
                    </dl>
                </div>

                <footer className="og3-dialog__footer">
                    {canEdit && (
                        <Button
                            disabled={isSubmitting}
                            onClick={() => {
                                onEdit(service);
                            }}
                            variant="secondary"
                        >
                            Editar serviço
                        </Button>
                    )}

                    {service.is_active &&
                        canDeactivate && (
                            <Button
                                disabled={
                                    isSubmitting
                                }
                                onClick={() => {
                                    onDeactivate(
                                        service,
                                    );
                                }}
                                variant="danger"
                            >
                                Inativar serviço
                            </Button>
                        )}

                    {!service.is_active &&
                        canReactivate && (
                            <Button
                                disabled={
                                    isSubmitting
                                }
                                onClick={() => {
                                    onReactivate(
                                        service,
                                    );
                                }}
                            >
                                Reativar serviço
                            </Button>
                        )}
                </footer>
            </div>
        </div>
    );
}