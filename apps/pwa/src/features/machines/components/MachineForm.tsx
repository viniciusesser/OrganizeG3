import {
    useId,
    useState,
} from "react";
import type {
    FormEvent,
} from "react";

import type {
    Machine,
    MachineCreateInput,
} from "@/features/machines/model/machine";
import {
    useAccessibleOverlay,
} from "@/shared/hooks/useAccessibleOverlay";
import {
    Button,
    Heading,
    Input,
    Text,
} from "@/shared/components/ui";

export interface MachineFormProps {
    readonly machine?: Machine;
    readonly isSubmitting: boolean;
    readonly submitError?: string | null;
    readonly onCancel: () => void;
    readonly onSubmit: (
        values: MachineCreateInput,
    ) => Promise<void> | void;
}

interface Draft {
    readonly code: string;
    readonly name: string;
    readonly machineType: string;
    readonly manufacturer: string;
    readonly model: string;
    readonly serialNumber: string;
}

interface Errors {
    readonly code?: string;
    readonly name?: string;
    readonly machineType?: string;
}

function createDraft(
    machine?: Machine,
): Draft {
    return {
        code:
            machine?.code ??
            "",
        name:
            machine?.name ??
            "",
        machineType:
            machine?.machine_type ??
            "",
        manufacturer:
            machine?.manufacturer ??
            "",
        model:
            machine?.model ??
            "",
        serialNumber:
            machine?.serial_number ??
            "",
    };
}

function optionalText(
    value: string,
): string | null {
    const normalized =
        value.trim();

    return normalized.length > 0
        ? normalized
        : null;
}

function validate(
    draft: Draft,
): Errors {
    const errors: {
        code?: string;
        name?: string;
        machineType?: string;
    } = {};

    if (
        draft.code
            .trim()
            .length === 0
    ) {
        errors.code =
            "Informe o código da máquina.";
    }

    if (
        draft.name
            .trim()
            .length === 0
    ) {
        errors.name =
            "Informe o nome da máquina.";
    }

    if (
        draft.machineType
            .trim()
            .length === 0
    ) {
        errors.machineType =
            "Informe o tipo da máquina.";
    }

    return errors;
}

export function MachineForm({
    machine,
    isSubmitting,
    submitError = null,
    onCancel,
    onSubmit,
}: MachineFormProps) {
    const titleId =
        useId();

    const descriptionId =
        useId();

    const {
        overlayRef,
    } = useAccessibleOverlay<HTMLDivElement>({
        closeOnEscape:
            !isSubmitting,
        onClose:
            onCancel,
    });

    const [
        draft,
        setDraft,
    ] = useState<Draft>(
        createDraft(
            machine,
        ),
    );

    const [
        errors,
        setErrors,
    ] = useState<Errors>(
        {},
    );

    const isEditing =
        machine !== undefined;

    const updateField = (
        field: keyof Draft,
        value: string,
    ): void => {
        setDraft(
            (current) => ({
                ...current,
                [field]:
                    value,
            }),
        );
    };

    const handleSubmit = async (
        event:
            FormEvent<HTMLFormElement>,
    ): Promise<void> => {
        event.preventDefault();

        const nextErrors =
            validate(
                draft,
            );

        setErrors(
            nextErrors,
        );

        if (
            Object.keys(
                nextErrors,
            ).length > 0
        ) {
            return;
        }

        await onSubmit({
            code:
                draft.code
                    .trim()
                    .toUpperCase(),
            name:
                draft.name
                    .trim(),
            machine_type:
                draft.machineType
                    .trim(),
            manufacturer:
                optionalText(
                    draft.manufacturer,
                ),
            model:
                optionalText(
                    draft.model,
                ),
            serial_number:
                optionalText(
                    draft.serialNumber,
                ),
        });
    };

    return (
        <div
            aria-describedby={
                descriptionId
            }
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
                        <Heading
                            level={3}
                        >
                            <span
                                id={
                                    titleId
                                }
                            >
                                {
                                    isEditing
                                        ? "Editar máquina"
                                        : "Nova máquina"
                                }
                            </span>
                        </Heading>

                        <Text
                            id={
                                descriptionId
                            }
                            tone="secondary"
                        >
                            Informe a identificação e os dados técnicos do equipamento.
                        </Text>
                    </div>

                    <Button
                        aria-label="Fechar formulário"
                        disabled={
                            isSubmitting
                        }
                        onClick={
                            onCancel
                        }
                        size="sm"
                        variant="secondary"
                    >
                        Fechar
                    </Button>
                </header>

                <form
                    className="og3-customer-form"
                    onSubmit={(
                        event,
                    ) => {
                        void handleSubmit(
                            event,
                        );
                    }}
                >
                    <div
                        className="og3-dialog__body"
                    >
                        <div
                            className="og3-form-grid"
                        >
                            <Input
                                data-og3-autofocus="true"
                                disabled={
                                    isSubmitting
                                }
                                error={
                                    errors.code
                                }
                                label="Código da máquina *"
                                maxLength={
                                    100
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "code",
                                        event
                                            .target
                                            .value,
                                    );
                                }}
                                value={
                                    draft.code
                                }
                            />

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                error={
                                    errors.name
                                }
                                label="Nome da máquina *"
                                maxLength={
                                    255
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "name",
                                        event
                                            .target
                                            .value,
                                    );
                                }}
                                value={
                                    draft.name
                                }
                            />

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                error={
                                    errors.machineType
                                }
                                label="Tipo da máquina *"
                                maxLength={
                                    100
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "machineType",
                                        event
                                            .target
                                            .value,
                                    );
                                }}
                                placeholder="Ex.: Seccionadora"
                                value={
                                    draft.machineType
                                }
                            />

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                label="Fabricante"
                                maxLength={
                                    255
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "manufacturer",
                                        event
                                            .target
                                            .value,
                                    );
                                }}
                                value={
                                    draft.manufacturer
                                }
                            />

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                label="Modelo"
                                maxLength={
                                    255
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "model",
                                        event
                                            .target
                                            .value,
                                    );
                                }}
                                value={
                                    draft.model
                                }
                            />

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                label="Número de série"
                                maxLength={
                                    255
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "serialNumber",
                                        event
                                            .target
                                            .value,
                                    );
                                }}
                                value={
                                    draft.serialNumber
                                }
                            />
                        </div>

                        <Text
                            size="sm"
                            tone="secondary"
                        >
                            O vínculo com filial será disponibilizado na integração da tela de Filiais.
                        </Text>

                        {submitError !==
                            null && (
                                <div
                                    className={[
                                        "og3-inline-message",
                                        "og3-inline-message--danger",
                                    ].join(
                                        " ",
                                    )}
                                    role="alert"
                                >
                                    {
                                        submitError
                                    }
                                </div>
                            )}
                    </div>

                    <footer
                        className="og3-dialog__footer"
                    >
                        <Button
                            disabled={
                                isSubmitting
                            }
                            onClick={
                                onCancel
                            }
                            variant="secondary"
                        >
                            Cancelar
                        </Button>

                        <Button
                            disabled={
                                isSubmitting
                            }
                            type="submit"
                        >
                            {
                                isSubmitting
                                    ? "Salvando..."
                                    : isEditing
                                        ? "Salvar alterações"
                                        : "Salvar máquina"
                            }
                        </Button>
                    </footer>
                </form>
            </div>
        </div>
    );
}