import {
    useId,
    useState,
} from "react";
import type {
    FormEvent,
} from "react";

import type {
    Brand,
} from "@/features/materials/model/brand";
import {
    formatBrandOption,
} from "@/features/materials/model/brand";
import type {
    Material,
    MaterialCreateInput,
} from "@/features/materials/model/material";
import {
    Button,
    Heading,
    Input,
    Text,
} from "@/shared/components/ui";

export interface MaterialFormProps {
    readonly material?: Material;
    readonly brands: readonly Brand[];
    readonly canReadBrands: boolean;
    readonly isLoadingBrands: boolean;
    readonly isSubmitting: boolean;
    readonly submitError?: string | null;
    readonly onCancel: () => void;
    readonly onSubmit: (
        values: MaterialCreateInput,
    ) => Promise<void> | void;
}

interface MaterialFormDraft {
    readonly code: string;
    readonly name: string;
    readonly category: string;
    readonly unit: string;
    readonly brandId: string;
}

interface MaterialFormErrors {
    readonly code?: string;
    readonly name?: string;
    readonly category?: string;
    readonly unit?: string;
}

function createDraft(
    material?: Material,
): MaterialFormDraft {
    return {
        code: material?.code ?? "",
        name: material?.name ?? "",
        category:
            material?.category ?? "",
        unit: material?.unit ?? "",
        brandId:
            material?.brand_id ?? "",
    };
}

function validateForm(
    draft: MaterialFormDraft,
): MaterialFormErrors {
    const errors: {
        code?: string;
        name?: string;
        category?: string;
        unit?: string;
    } = {};

    if (draft.code.trim().length === 0) {
        errors.code =
            "Informe o código do material.";
    }

    if (draft.name.trim().length === 0) {
        errors.name =
            "Informe o nome do material.";
    }

    if (
        draft.category.trim().length === 0
    ) {
        errors.category =
            "Informe a categoria do material.";
    }

    if (draft.unit.trim().length === 0) {
        errors.unit =
            "Informe a unidade do material.";
    }

    return errors;
}

export function MaterialForm({
    material,
    brands,
    canReadBrands,
    isLoadingBrands,
    isSubmitting,
    submitError = null,
    onCancel,
    onSubmit,
}: MaterialFormProps) {
    const titleId = useId();
    const brandFieldId = useId();
    const brandSupportId =
        `${brandFieldId}-support`;

    const [draft, setDraft] =
        useState<MaterialFormDraft>(
            createDraft(material),
        );

    const [errors, setErrors] =
        useState<MaterialFormErrors>({});

    const isEditing =
        material !== undefined;

    const selectedBrandExists =
        draft.brandId.length === 0 ||
        brands.some(
            (brand) =>
                brand.id === draft.brandId,
        );

    const updateField = (
        field: keyof MaterialFormDraft,
        value: string,
    ) => {
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
            name: draft.name.trim(),
            category:
                draft.category.trim(),
            unit:
                draft.unit
                    .trim()
                    .toUpperCase(),
            brand_id:
                draft.brandId.length > 0
                    ? draft.brandId
                    : null,
        });
    };

    const brandSupportText =
        !canReadBrands
            ? "Você não possui permissão para consultar as marcas."
            : isLoadingBrands
                ? "Carregando marcas..."
                : "A marca é opcional.";

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
                                    ? "Editar material"
                                    : "Novo material"}
                            </span>
                        </Heading>

                        <Text tone="secondary">
                            Preencha a identificação, a
                            categoria, a unidade e a marca
                            do material.
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
                                disabled={isSubmitting}
                                error={errors.code}
                                label="Código do material *"
                                maxLength={100}
                                onChange={(event) => {
                                    updateField(
                                        "code",
                                        event.target.value,
                                    );
                                }}
                                value={draft.code}
                            />

                            <Input
                                disabled={isSubmitting}
                                error={errors.name}
                                label="Nome do material *"
                                maxLength={255}
                                onChange={(event) => {
                                    updateField(
                                        "name",
                                        event.target.value,
                                    );
                                }}
                                value={draft.name}
                            />

                            <Input
                                disabled={isSubmitting}
                                error={errors.category}
                                label="Categoria *"
                                maxLength={100}
                                onChange={(event) => {
                                    updateField(
                                        "category",
                                        event.target.value,
                                    );
                                }}
                                value={draft.category}
                            />

                            <Input
                                disabled={isSubmitting}
                                error={errors.unit}
                                label="Unidade *"
                                maxLength={50}
                                onChange={(event) => {
                                    updateField(
                                        "unit",
                                        event.target.value,
                                    );
                                }}
                                supportText="Exemplos: UN, M², M, KG ou CHAPA."
                                value={draft.unit}
                            />

                            <div className="og3-field">
                                <label
                                    className="og3-field__label"
                                    htmlFor={brandFieldId}
                                >
                                    Marca
                                </label>

                                <select
                                    aria-describedby={
                                        brandSupportId
                                    }
                                    className="og3-field__input"
                                    disabled={
                                        isSubmitting ||
                                        !canReadBrands ||
                                        isLoadingBrands
                                    }
                                    id={brandFieldId}
                                    onChange={(event) => {
                                        updateField(
                                            "brandId",
                                            event.target.value,
                                        );
                                    }}
                                    value={draft.brandId}
                                >
                                    <option value="">
                                        Sem marca
                                    </option>

                                    {!selectedBrandExists && (
                                        <option
                                            value={
                                                draft.brandId
                                            }
                                        >
                                            Marca atual indisponível
                                        </option>
                                    )}

                                    {brands.map(
                                        (brand) => (
                                            <option
                                                disabled={
                                                    !brand.is_active &&
                                                    brand.id !==
                                                    draft.brandId
                                                }
                                                key={brand.id}
                                                value={brand.id}
                                            >
                                                {formatBrandOption(
                                                    brand,
                                                )}
                                                {!brand.is_active &&
                                                    " — Inativa"}
                                            </option>
                                        ),
                                    )}
                                </select>

                                <span
                                    className="og3-field__support"
                                    id={brandSupportId}
                                >
                                    {brandSupportText}
                                </span>
                            </div>
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
                            disabled={isSubmitting}
                            onClick={onCancel}
                            variant="secondary"
                        >
                            Cancelar
                        </Button>

                        <Button
                            disabled={isSubmitting}
                            type="submit"
                        >
                            {isSubmitting
                                ? "Salvando..."
                                : isEditing
                                    ? "Salvar alterações"
                                    : "Salvar material"}
                        </Button>
                    </footer>
                </form>
            </div>
        </div>
    );
}