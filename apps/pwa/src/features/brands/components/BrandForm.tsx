import {
    useId,
    useState,
} from "react";
import type {
    FormEvent,
} from "react";

import type {
    Brand,
    BrandCreateInput,
} from "@/features/brands/model/brand";
import {
    Button,
    Heading,
    Input,
    Text,
} from "@/shared/components/ui";

export interface BrandFormProps {
    readonly brand?: Brand;
    readonly isSubmitting: boolean;
    readonly submitError?: string | null;
    readonly onCancel: () => void;
    readonly onSubmit: (
        values: BrandCreateInput,
    ) => Promise<void> | void;
}

interface BrandFormDraft {
    readonly code: string;
    readonly name: string;
}

interface BrandFormErrors {
    readonly code?: string;
    readonly name?: string;
}

function createDraft(
    brand?: Brand,
): BrandFormDraft {
    return {
        code: brand?.code ?? "",
        name: brand?.name ?? "",
    };
}

function validateForm(
    draft: BrandFormDraft,
): BrandFormErrors {
    const errors: {
        code?: string;
        name?: string;
    } = {};

    if (draft.code.trim().length === 0) {
        errors.code =
            "Informe o código da marca.";
    }

    if (draft.name.trim().length === 0) {
        errors.name =
            "Informe o nome da marca.";
    }

    return errors;
}

export function BrandForm({
    brand,
    isSubmitting,
    submitError = null,
    onCancel,
    onSubmit,
}: BrandFormProps) {
    const titleId = useId();

    const [draft, setDraft] =
        useState<BrandFormDraft>(
            createDraft(brand),
        );

    const [errors, setErrors] =
        useState<BrandFormErrors>({});

    const isEditing =
        brand !== undefined;

    const updateField = (
        field: keyof BrandFormDraft,
        value: string,
    ): void => {
        setDraft(
            (current) => ({
                ...current,
                [field]: value,
            }),
        );
    };

    const handleSubmit = async (
        event: FormEvent<HTMLFormElement>,
    ): Promise<void> => {
        event.preventDefault();

        const nextErrors =
            validateForm(draft);

        setErrors(nextErrors);

        if (
            Object.keys(nextErrors)
                .length > 0
        ) {
            return;
        }

        await onSubmit({
            code:
                draft.code
                    .trim()
                    .toUpperCase(),
            name:
                draft.name.trim(),
        });
    };

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
                        <Heading level={3}>
                            <span id={titleId}>
                                {isEditing
                                    ? "Editar marca"
                                    : "Nova marca"}
                            </span>
                        </Heading>

                        <Text tone="secondary">
                            Informe o código e o
                            nome de identificação
                            da marca.
                        </Text>
                    </div>

                    <Button
                        aria-label="Fechar formulário"
                        disabled={isSubmitting}
                        onClick={onCancel}
                        size="sm"
                        variant="secondary"
                    >
                        Fechar
                    </Button>
                </header>

                <form
                    className="og3-customer-form"
                    onSubmit={(event) => {
                        void handleSubmit(event);
                    }}
                >
                    <div className="og3-dialog__body">
                        <div className="og3-form-grid">
                            <Input
                                autoFocus
                                disabled={
                                    isSubmitting
                                }
                                error={errors.code}
                                label="Código da marca *"
                                maxLength={100}
                                onChange={(event) => {
                                    updateField(
                                        "code",
                                        event.target.value,
                                    );
                                }}
                                supportText="O código será armazenado em letras maiúsculas."
                                value={draft.code}
                            />

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                error={errors.name}
                                label="Nome da marca *"
                                maxLength={255}
                                onChange={(event) => {
                                    updateField(
                                        "name",
                                        event.target.value,
                                    );
                                }}
                                value={draft.name}
                            />
                        </div>

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
                        <Button
                            disabled={
                                isSubmitting
                            }
                            onClick={onCancel}
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
                            {isSubmitting
                                ? "Salvando..."
                                : isEditing
                                    ? "Salvar alterações"
                                    : "Salvar marca"}
                        </Button>
                    </footer>
                </form>
            </div>
        </div>
    );
}