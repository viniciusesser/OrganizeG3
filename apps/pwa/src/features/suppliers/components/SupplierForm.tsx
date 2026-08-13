import {
    useId,
    useState,
} from "react";
import type {
    FormEvent,
} from "react";

import type {
    Supplier,
    SupplierCreateInput,
} from "@/features/suppliers/model/supplier";
import {
    useAccessibleOverlay,
} from "@/shared/hooks/useAccessibleOverlay";
import {
    Button,
    Heading,
    Input,
    Text,
} from "@/shared/components/ui";

export interface SupplierFormProps {
    readonly supplier?: Supplier;
    readonly isSubmitting: boolean;
    readonly submitError?: string | null;
    readonly onCancel: () => void;
    readonly onSubmit: (
        values: SupplierCreateInput,
    ) => Promise<void> | void;
}

interface SupplierFormDraft {
    readonly code: string;
    readonly name: string;
    readonly tradeName: string;
    readonly legalName: string;
    readonly documentNumber: string;
    readonly stateRegistration: string;
    readonly email: string;
    readonly invoiceEmail: string;
    readonly phone: string;
    readonly secondaryPhone: string;
    readonly website: string;
    readonly contactName: string;
    readonly postalCode: string;
    readonly street: string;
    readonly number: string;
    readonly district: string;
    readonly city: string;
    readonly state: string;
}

interface SupplierFormErrors {
    readonly code?: string;
    readonly name?: string;
    readonly email?: string;
    readonly invoiceEmail?: string;
    readonly state?: string;
}

function createDraft(
    supplier?: Supplier,
): SupplierFormDraft {
    return {
        code:
            supplier?.code ??
            "",
        name:
            supplier?.name ??
            "",
        tradeName:
            supplier?.trade_name ??
            "",
        legalName:
            supplier?.legal_name ??
            "",
        documentNumber:
            supplier?.document_number ??
            "",
        stateRegistration:
            supplier?.state_registration ??
            "",
        email:
            supplier?.email ??
            "",
        invoiceEmail:
            supplier?.invoice_email ??
            "",
        phone:
            supplier?.phone ??
            "",
        secondaryPhone:
            supplier?.secondary_phone ??
            "",
        website:
            supplier?.website ??
            "",
        contactName:
            supplier?.contact_name ??
            "",
        postalCode:
            supplier?.postal_code ??
            "",
        street:
            supplier?.street ??
            "",
        number:
            supplier?.number ??
            "",
        district:
            supplier?.district ??
            "",
        city:
            supplier?.city ??
            "",
        state:
            supplier?.state ??
            "",
    };
}

function optionalValue(
    value: string,
): string | null {
    const normalized =
        value.trim();

    return normalized.length > 0
        ? normalized
        : null;
}

function isValidEmail(
    value: string,
): boolean {
    const normalized =
        value.trim();

    return (
        normalized.length === 0 ||
        /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
            normalized,
        )
    );
}

function validateForm(
    draft: SupplierFormDraft,
): SupplierFormErrors {
    const errors: {
        code?: string;
        name?: string;
        email?: string;
        invoiceEmail?: string;
        state?: string;
    } = {};

    if (
        draft.code
            .trim()
            .length === 0
    ) {
        errors.code =
            "Informe o código do fornecedor.";
    }

    if (
        draft.name
            .trim()
            .length === 0
    ) {
        errors.name =
            "Informe o nome do fornecedor.";
    }

    if (
        !isValidEmail(
            draft.email,
        )
    ) {
        errors.email =
            "Informe um email válido.";
    }

    if (
        !isValidEmail(
            draft.invoiceEmail,
        )
    ) {
        errors.invoiceEmail =
            "Informe um email de faturamento válido.";
    }

    const normalizedState =
        draft.state.trim();

    if (
        normalizedState.length > 0 &&
        normalizedState.length !== 2
    ) {
        errors.state =
            "Informe a UF com duas letras.";
    }

    return errors;
}

export function SupplierForm({
    supplier,
    isSubmitting,
    submitError = null,
    onCancel,
    onSubmit,
}: SupplierFormProps) {
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
    ] = useState<SupplierFormDraft>(
        createDraft(
            supplier,
        ),
    );

    const [
        errors,
        setErrors,
    ] = useState<SupplierFormErrors>(
        {},
    );

    const isEditing =
        supplier !== undefined;

    const updateField = (
        field:
            keyof SupplierFormDraft,
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

        await onSubmit({
            code:
                draft.code.trim(),
            name:
                draft.name.trim(),
            trade_name:
                optionalValue(
                    draft.tradeName,
                ),
            legal_name:
                optionalValue(
                    draft.legalName,
                ),
            document_number:
                optionalValue(
                    draft.documentNumber,
                ),
            state_registration:
                optionalValue(
                    draft.stateRegistration,
                ),
            email:
                optionalValue(
                    draft.email,
                ),
            invoice_email:
                optionalValue(
                    draft.invoiceEmail,
                ),
            phone:
                optionalValue(
                    draft.phone,
                ),
            secondary_phone:
                optionalValue(
                    draft.secondaryPhone,
                ),
            website:
                optionalValue(
                    draft.website,
                ),
            contact_name:
                optionalValue(
                    draft.contactName,
                ),
            postal_code:
                optionalValue(
                    draft.postalCode,
                ),
            street:
                optionalValue(
                    draft.street,
                ),
            number:
                optionalValue(
                    draft.number,
                ),
            district:
                optionalValue(
                    draft.district,
                ),
            city:
                optionalValue(
                    draft.city,
                ),
            state:
                optionalValue(
                    draft.state,
                )?.toUpperCase() ??
                null,
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
                                        ? "Editar fornecedor"
                                        : "Novo fornecedor"
                                }
                            </span>
                        </Heading>

                        <Text
                            id={
                                descriptionId
                            }
                            tone="secondary"
                        >
                            Preencha os dados cadastrais, de contato e endereço.
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
                                label="Código do fornecedor *"
                                maxLength={
                                    100
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "code",
                                        event.target.value,
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
                                label="Nome do fornecedor *"
                                maxLength={
                                    255
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "name",
                                        event.target.value,
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
                                label="Nome fantasia"
                                maxLength={
                                    255
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "tradeName",
                                        event.target.value,
                                    );
                                }}
                                value={
                                    draft.tradeName
                                }
                            />

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                label="Razão social"
                                maxLength={
                                    255
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "legalName",
                                        event.target.value,
                                    );
                                }}
                                value={
                                    draft.legalName
                                }
                            />

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                label="CPF ou CNPJ"
                                maxLength={
                                    32
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "documentNumber",
                                        event.target.value,
                                    );
                                }}
                                value={
                                    draft.documentNumber
                                }
                            />

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                label="Inscrição estadual"
                                maxLength={
                                    50
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "stateRegistration",
                                        event.target.value,
                                    );
                                }}
                                value={
                                    draft.stateRegistration
                                }
                            />

                            <Input
                                autoComplete="email"
                                disabled={
                                    isSubmitting
                                }
                                error={
                                    errors.email
                                }
                                label="Email"
                                maxLength={
                                    255
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "email",
                                        event.target.value,
                                    );
                                }}
                                type="email"
                                value={
                                    draft.email
                                }
                            />

                            <Input
                                autoComplete="email"
                                disabled={
                                    isSubmitting
                                }
                                error={
                                    errors.invoiceEmail
                                }
                                label="Email de faturamento"
                                maxLength={
                                    255
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "invoiceEmail",
                                        event.target.value,
                                    );
                                }}
                                type="email"
                                value={
                                    draft.invoiceEmail
                                }
                            />

                            <Input
                                autoComplete="tel"
                                disabled={
                                    isSubmitting
                                }
                                label="Telefone"
                                maxLength={
                                    32
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "phone",
                                        event.target.value,
                                    );
                                }}
                                type="tel"
                                value={
                                    draft.phone
                                }
                            />

                            <Input
                                autoComplete="tel"
                                disabled={
                                    isSubmitting
                                }
                                label="Telefone secundário"
                                maxLength={
                                    32
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "secondaryPhone",
                                        event.target.value,
                                    );
                                }}
                                type="tel"
                                value={
                                    draft.secondaryPhone
                                }
                            />

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                label="Pessoa de contato"
                                maxLength={
                                    255
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "contactName",
                                        event.target.value,
                                    );
                                }}
                                value={
                                    draft.contactName
                                }
                            />

                            <Input
                                autoComplete="url"
                                disabled={
                                    isSubmitting
                                }
                                label="Site"
                                maxLength={
                                    500
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "website",
                                        event.target.value,
                                    );
                                }}
                                type="url"
                                value={
                                    draft.website
                                }
                            />

                            <Input
                                autoComplete="postal-code"
                                disabled={
                                    isSubmitting
                                }
                                label="CEP"
                                maxLength={
                                    16
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "postalCode",
                                        event.target.value,
                                    );
                                }}
                                value={
                                    draft.postalCode
                                }
                            />

                            <Input
                                autoComplete="street-address"
                                disabled={
                                    isSubmitting
                                }
                                label="Logradouro"
                                maxLength={
                                    255
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "street",
                                        event.target.value,
                                    );
                                }}
                                value={
                                    draft.street
                                }
                            />

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                label="Número"
                                maxLength={
                                    50
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "number",
                                        event.target.value,
                                    );
                                }}
                                value={
                                    draft.number
                                }
                            />

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                label="Bairro"
                                maxLength={
                                    255
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "district",
                                        event.target.value,
                                    );
                                }}
                                value={
                                    draft.district
                                }
                            />

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                label="Cidade"
                                maxLength={
                                    255
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "city",
                                        event.target.value,
                                    );
                                }}
                                value={
                                    draft.city
                                }
                            />

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                error={
                                    errors.state
                                }
                                label="UF"
                                maxLength={
                                    2
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateField(
                                        "state",
                                        event.target.value,
                                    );
                                }}
                                value={
                                    draft.state
                                }
                            />
                        </div>

                        {submitError !==
                            null && (
                                <div
                                    className={[
                                        "og3-inline-message",
                                        "og3-inline-message--danger",
                                    ].join(" ")}
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
                                        : "Salvar fornecedor"
                            }
                        </Button>
                    </footer>
                </form>
            </div>
        </div>
    );
}