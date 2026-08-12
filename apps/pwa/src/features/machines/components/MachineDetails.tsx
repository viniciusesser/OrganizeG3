import {
    useEffect,
    useState,
} from "react";

import type {
    Machine,
    MachineStatus,
} from "@/features/machines/model/machine";
import {
    MACHINE_STATUSES,
    getMachineStatusLabel,
} from "@/features/machines/model/machine";
import {
    Badge,
    Button,
    Heading,
    Text,
} from "@/shared/components/ui";

export interface MachineDetailsProps {
    readonly machine: Machine;
    readonly canEdit: boolean;
    readonly canChangeStatus: boolean;
    readonly canDeactivate: boolean;
    readonly canReactivate: boolean;
    readonly isSubmitting: boolean;
    readonly submitError?: string | null;
    readonly onClose: () => void;
    readonly onEdit: (
        machine: Machine,
    ) => void;
    readonly onChangeStatus: (
        machine: Machine,
        status: MachineStatus,
    ) => Promise<void> | void;
    readonly onDeactivate: (
        machine: Machine,
    ) => void;
    readonly onReactivate: (
        machine: Machine,
    ) => void;
}

function show(
    value: string | null,
): string {
    return value ??
        "Não informado";
}

export function MachineDetails({
    machine,
    canEdit,
    canChangeStatus,
    canDeactivate,
    canReactivate,
    isSubmitting,
    submitError = null,
    onClose,
    onEdit,
    onChangeStatus,
    onDeactivate,
    onReactivate,
}: MachineDetailsProps) {
    const [
        status,
        setStatus,
    ] =
        useState<MachineStatus>(
            machine.status,
        );

    useEffect(
        () => {
            const handleKeyDown = (
                event: KeyboardEvent,
            ): void => {
                if (
                    event.key === "Escape"
                ) {
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
        [
            onClose,
        ],
    );

    return (
        <div
            aria-labelledby="machine-details-title"
            aria-modal="true"
            className="og3-dialog-backdrop"
            role="dialog"
        >
            <div className="og3-dialog og3-dialog--md">
                <header className="og3-dialog__header">
                    <div className="og3-dialog__heading">
                        <Badge
                            variant={
                                machine.is_active
                                    ? "success"
                                    : "neutral"
                            }
                        >
                            {machine.is_active
                                ? "Ativa"
                                : "Inativa"}
                        </Badge>

                        <Heading level={3}>
                            <span id="machine-details-title">
                                {machine.name}
                            </span>
                        </Heading>

                        <Text tone="secondary">
                            {machine.code}
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
                            <dt>
                                Tipo
                            </dt>

                            <dd>
                                {machine.machine_type}
                            </dd>
                        </div>

                        <div className="og3-details-grid__item">
                            <dt>
                                Status operacional
                            </dt>

                            <dd>
                                {getMachineStatusLabel(
                                    machine.status,
                                )}
                            </dd>
                        </div>

                        <div className="og3-details-grid__item">
                            <dt>
                                Fabricante
                            </dt>

                            <dd>
                                {show(
                                    machine.manufacturer,
                                )}
                            </dd>
                        </div>

                        <div className="og3-details-grid__item">
                            <dt>
                                Modelo
                            </dt>

                            <dd>
                                {show(
                                    machine.model,
                                )}
                            </dd>
                        </div>

                        <div className="og3-details-grid__item">
                            <dt>
                                Número de série
                            </dt>

                            <dd>
                                {show(
                                    machine.serial_number,
                                )}
                            </dd>
                        </div>

                        <div className="og3-details-grid__item">
                            <dt>
                                Filial
                            </dt>

                            <dd>
                                {show(
                                    machine.branch_id,
                                )}
                            </dd>
                        </div>
                    </dl>

                    {machine.is_active &&
                        canChangeStatus && (
                            <div className="og3-form-grid">
                                <div className="og3-field">
                                    <label
                                        className="og3-field__label"
                                        htmlFor="machine-status"
                                    >
                                        Alterar status operacional
                                    </label>

                                    <select
                                        className="og3-field__input"
                                        disabled={isSubmitting}
                                        id="machine-status"
                                        onChange={(event) => {
                                            setStatus(
                                                event.target.value as MachineStatus,
                                            );
                                        }}
                                        value={status}
                                    >
                                        {MACHINE_STATUSES.map(
                                            (item) => (
                                                <option
                                                    key={item}
                                                    value={item}
                                                >
                                                    {getMachineStatusLabel(
                                                        item,
                                                    )}
                                                </option>
                                            ),
                                        )}
                                    </select>
                                </div>

                                <div className="og3-filter-bar__actions">
                                    <Button
                                        disabled={
                                            isSubmitting ||
                                            status === machine.status
                                        }
                                        onClick={() => {
                                            void onChangeStatus(
                                                machine,
                                                status,
                                            );
                                        }}
                                        variant="secondary"
                                    >
                                        {isSubmitting
                                            ? "Atualizando..."
                                            : "Atualizar status"}
                                    </Button>
                                </div>
                            </div>
                        )}

                    {submitError !== null && (
                        <div
                            className="og3-inline-message og3-inline-message--danger"
                            role="alert"
                        >
                            {submitError}
                        </div>
                    )}
                </div>

                <footer className="og3-dialog__footer">
                    {canEdit && (
                        <Button
                            disabled={isSubmitting}
                            onClick={() => {
                                onEdit(
                                    machine,
                                );
                            }}
                            variant="secondary"
                        >
                            Editar máquina
                        </Button>
                    )}

                    {machine.is_active &&
                        canDeactivate && (
                            <Button
                                disabled={isSubmitting}
                                onClick={() => {
                                    onDeactivate(
                                        machine,
                                    );
                                }}
                                variant="danger"
                            >
                                Inativar máquina
                            </Button>
                        )}

                    {!machine.is_active &&
                        canReactivate && (
                            <Button
                                disabled={isSubmitting}
                                onClick={() => {
                                    onReactivate(
                                        machine,
                                    );
                                }}
                            >
                                Reativar máquina
                            </Button>
                        )}
                </footer>
            </div>
        </div>
    );
}