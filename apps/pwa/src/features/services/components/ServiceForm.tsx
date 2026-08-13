import {
    useId,
    useState,
} from "react";
import type {
    FormEvent,
} from "react";

import type {
    Service,
    ServiceCreateInput,
    ServiceExecutionMode,
} from "@/features/services/model/service";
import {
    SERVICE_EXECUTION_MODES,
    getServiceExecutionModeLabel,
} from "@/features/services/model/service";
import {
    useAccessibleOverlay,
} from "@/shared/hooks/useAccessibleOverlay";
import {
    Button,
    Heading,
    Input,
    Text,
} from "@/shared/components/ui";

export interface ServiceFormProps {
    readonly service?: Service;
    readonly isSubmitting: boolean;
    readonly submitError?: string | null;
    readonly onCancel: () => void;
    readonly onSubmit: (
        values: ServiceCreateInput,
    ) => Promise<void> | void;
}

interface ServiceFormDraft {
    readonly code: string;
    readonly name: string;
    readonly category: string;
    readonly unit: string;
    readonly executionMode:
    ServiceExecutionMode;
    readonly estimatedDurationMinutes:
    string;
}

interface ServiceFormErrors {
    readonly code?: string;
    readonly name?: string;
    readonly category?: string;
    readonly unit?: string;
    readonly estimatedDurationMinutes?:
    string;
}

function createDraft(
    service?: Service,
): ServiceFormDraft {
    return {
        code:
            service?.code ??
            "",
        name:
            service?.name ??
            "",
        category:
            service?.category ??
            "",
        unit:
            service?.unit ??
            "",
        executionMode:
            service?.execution_mode ??
            "INTERNAL",
        estimatedDurationMinutes:
            service
                ?.estimated_duration_minutes
                ?.toString() ??
            "",
    };
}

function validateForm(
    draft: ServiceFormDraft,
): ServiceFormErrors {
    const errors: {
        code?: string;
        name?: string;
        category?: string;
        unit?: string;
        estimatedDurationMinutes?:
        string;
    } = {};

    if (
        draft.code
            .trim()
            .length === 0
    ) {
        errors.code =
            "Informe o código do serviço.";
    }

    if (
        draft.name
            .trim()
            .length === 0
    ) {
        errors.name =
            "Informe o nome do serviço.";
    }

    if (
        draft.category
            .trim()
            .length === 0
    ) {
        errors.category =
            "Informe a categoria do serviço.";
    }

    if (
        draft.unit
            .trim()
            .length === 0
    ) {
        errors.unit =
            "Informe a unidade do serviço.";
    }

    const durationText =
        draft
            .estimatedDurationMinutes
            .trim();

    if (
        durationText.length > 0
    ) {
        const duration =
            Number(
                durationText,
            );

        if (
            !Number.isInteger(
                duration,
            ) ||
            duration <= 0
        ) {
            errors.estimatedDurationMinutes =
                "Informe uma duração em minutos maior que zero.";
        }
    }

    return errors;
}

export function ServiceForm({
    service,
    isSubmitting,
    submitError = null,
    onCancel,
    onSubmit,
}: ServiceFormProps) {
    const titleId =
        useId();

    const descriptionId =
        useId();

    const executionModeFieldId =
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
    ] = useState<ServiceFormDraft>(
        createDraft(
            service,
        ),
    );

    const [
        errors,
        setErrors,
    ] = useState<ServiceFormErrors>(
        {},
    );

    const isEditing =
        service !== undefined;

    const updateField = (
        field:
            keyof ServiceFormDraft,
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
            validateForm(
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

        const durationText =
            draft
                .estimatedDurationMinutes
                .trim();

        await onSubmit({
            code:
                draft.code
                    .trim()
                    .toUpperCase(),
            name:
                draft.name
                    .trim(),
            category:
                draft.category
                    .trim(),
            unit:
                draft.unit
                    .trim()
                    .toUpperCase(),
            execution_mode:
                draft.executionMode,
            estimated_duration_minutes:
                durationText.length >
                    0
                    ? Number(
                        durationText,
                    )
                    : null,
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
                                        ? "Editar serviço"
                                        : "Novo serviço"
                                }
                            </span>
                        </Heading>

                        <Text
                            id={
                                descriptionId
                            }
                            tone="secondary"
                        >
                            Preencha a identificação, a categoria, a unidade, o modo de execução e a duração estimada.
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
                                label="Código do serviço *"
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
                                label="Nome do serviço *"
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
                                    errors.category
                                }
                                label="Categoria *"
                                maxLength={
                                    100
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "category",
                                        event
                                            .target
                                            .value,
                                    );
                                }}
                                value={
                                    draft.category
                                }
                            />

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                error={
                                    errors.unit
                                }
                                label="Unidade *"
                                maxLength={
                                    30
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "unit",
                                        event
                                            .target
                                            .value,
                                    );
                                }}
                                supportText="Exemplos: HORA, UN, M² ou DIÁRIA."
                                value={
                                    draft.unit
                                }
                            />

                            <div
                                className="og3-field"
                            >
                                <label
                                    className="og3-field__label"
                                    htmlFor={
                                        executionModeFieldId
                                    }
                                >
                                    Modo de execução *
                                </label>

                                <select
                                    className="og3-field__input"
                                    disabled={
                                        isSubmitting
                                    }
                                    id={
                                        executionModeFieldId
                                    }
                                    onChange={(
                                        event,
                                    ) => {
                                        updateField(
                                            "executionMode",
                                            event
                                                .target
                                                .value,
                                        );
                                    }}
                                    value={
                                        draft.executionMode
                                    }
                                >
                                    {SERVICE_EXECUTION_MODES.map(
                                        (
                                            mode,
                                        ) => (
                                            <option
                                                key={
                                                    mode
                                                }
                                                value={
                                                    mode
                                                }
                                            >
                                                {
                                                    getServiceExecutionModeLabel(
                                                        mode,
                                                    )
                                                }
                                            </option>
                                        ),
                                    )}
                                </select>
                            </div>

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                error={
                                    errors.estimatedDurationMinutes
                                }
                                label="Duração estimada (minutos)"
                                min={
                                    1
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "estimatedDurationMinutes",
                                        event
                                            .target
                                            .value,
                                    );
                                }}
                                step={
                                    1
                                }
                                supportText="Campo opcional. Informe o tempo médio do serviço."
                                type="number"
                                value={
                                    draft.estimatedDurationMinutes
                                }
                            />
                        </div>

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
                                        : "Salvar serviço"
                            }
                        </Button>
                    </footer>
                </form>
            </div>
        </div>
    );
}