import {
    useId,
    useState,
} from "react";
import type {
    FormEvent,
} from "react";

import type {
    Company,
    CreateCompanyPayload,
} from "@/features/company/model/company";
import {
    Button,
    Heading,
    Input,
    Text,
} from "@/shared/components/ui";

export interface CompanyFormProps {
    readonly company?: Company;
    readonly isSubmitting: boolean;
    readonly submitError?: string | null;
    readonly onCancel: () => void;
    readonly onSubmit: (
        values: CreateCompanyPayload,
    ) => Promise<void> | void;
}

interface CompanyFormDraft {
    readonly tradeName: string;
    readonly legalName: string;
    readonly documentNumber: string;
    readonly stateRegistration: string;

    readonly email: string;
    readonly phone: string;
    readonly website: string;
    readonly logoPath: string;

    readonly street: string;
    readonly number: string;
    readonly district: string;
    readonly city: string;
    readonly state: string;
    readonly postalCode: string;
}

interface CompanyFormErrors {
    readonly tradeName?: string;
    readonly email?: string;
    readonly state?: string;
}

function createDraft(
    company?: Company,
): CompanyFormDraft {
    return {
        tradeName:
            company?.trade_name ?? "",
        legalName:
            company?.legal_name ?? "",
        documentNumber:
            company?.document_number ?? "",
        stateRegistration:
            company?.state_registration ?? "",

        email:
            company?.email ?? "",
        phone:
            company?.phone ?? "",
        website:
            company?.website ?? "",
        logoPath:
            company?.logo_path ?? "",

        street:
            company?.street ?? "",
        number:
            company?.number ?? "",
        district:
            company?.district ?? "",
        city:
            company?.city ?? "",
        state:
            company?.state ?? "",
        postalCode:
            company?.postal_code ?? "",
    };
}

function optionalValue(
    value: string,
): string | null {
    const normalized = value.trim();

    return normalized.length > 0
        ? normalized
        : null;
}

function validateForm(
    draft: CompanyFormDraft,
): CompanyFormErrors {
    const errors: {
        tradeName?: string;
        email?: string;
        state?: string;
    } = {};

    if (draft.tradeName.trim().length === 0) {
        errors.tradeName =
            "Informe o nome fantasia da empresa.";
    }

    const normalizedEmail =
        draft.email.trim();

    if (
        normalizedEmail.length > 0 &&
        !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
            normalizedEmail,
        )
    ) {
        errors.email =
            "Informe um email válido.";
    }

    const normalizedState =
        draft.state.trim();

    if (
        normalizedState.length > 0 &&
        normalizedState.length !== 2
    ) {
        errors.state =
            "Informe a sigla UF com dois caracteres.";
    }

    return errors;
}

export function CompanyForm({
    company,
    isSubmitting,
    submitError = null,
    onCancel,
    onSubmit,
}: CompanyFormProps) {
    const titleId = useId();

    const [draft, setDraft] =
        useState<CompanyFormDraft>(
            createDraft(company),
        );

    const [errors, setErrors] =
        useState<CompanyFormErrors>({});

    const isEditing =
        company !== undefined;

    const updateField = (
        field: keyof CompanyFormDraft,
        value: string,
    ) => {
        setDraft((current) => ({
            ...current,
            [field]: value,
        }));
    };

    const handleSubmit = async (
        event: FormEvent<HTMLFormElement>,
    ): Promise<void> => {
        event.preventDefault();

        const nextErrors =
            validateForm(draft);

        setErrors(nextErrors);

        if (
            Object.keys(nextErrors).length > 0
        ) {
            return;
        }

        await onSubmit({
            trade_name:
                draft.tradeName.trim(),
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
                optionalValue(draft.email),
            phone:
                optionalValue(draft.phone),
            website:
                optionalValue(draft.website),
            logo_path:
                optionalValue(draft.logoPath),

            street:
                optionalValue(draft.street),
            number:
                optionalValue(draft.number),
            district:
                optionalValue(draft.district),
            city:
                optionalValue(draft.city),
            state:
                optionalValue(
                    draft.state,
                )?.toUpperCase() ?? null,
            postal_code:
                optionalValue(
                    draft.postalCode,
                ),
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
                                    ? "Editar empresa"
                                    : "Cadastrar empresa"}
                            </span>
                        </Heading>

                        <Text tone="secondary">
                            Preencha os dados cadastrais,
                            de contato e endereço da empresa.
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
                                error={
                                    errors.tradeName
                                }
                                label="Nome fantasia *"
                                maxLength={255}
                                onChange={(event) => {
                                    updateField(
                                        "tradeName",
                                        event.target.value,
                                    );
                                }}
                                value={draft.tradeName}
                            />

                            <Input
                                disabled={isSubmitting}
                                label="Razão social"
                                maxLength={255}
                                onChange={(event) => {
                                    updateField(
                                        "legalName",
                                        event.target.value,
                                    );
                                }}
                                value={draft.legalName}
                            />

                            <Input
                                disabled={isSubmitting}
                                label="CNPJ ou documento"
                                maxLength={30}
                                onChange={(event) => {
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
                                disabled={isSubmitting}
                                label="Inscrição estadual"
                                maxLength={30}
                                onChange={(event) => {
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
                                disabled={isSubmitting}
                                error={errors.email}
                                label="Email"
                                maxLength={320}
                                onChange={(event) => {
                                    updateField(
                                        "email",
                                        event.target.value,
                                    );
                                }}
                                type="email"
                                value={draft.email}
                            />

                            <Input
                                autoComplete="tel"
                                disabled={isSubmitting}
                                label="Telefone"
                                maxLength={30}
                                onChange={(event) => {
                                    updateField(
                                        "phone",
                                        event.target.value,
                                    );
                                }}
                                type="tel"
                                value={draft.phone}
                            />

                            <Input
                                autoComplete="url"
                                disabled={isSubmitting}
                                label="Site"
                                maxLength={2048}
                                onChange={(event) => {
                                    updateField(
                                        "website",
                                        event.target.value,
                                    );
                                }}
                                placeholder="https://"
                                type="url"
                                value={draft.website}
                            />

                            <Input
                                disabled={isSubmitting}
                                label="Caminho do logotipo"
                                maxLength={500}
                                onChange={(event) => {
                                    updateField(
                                        "logoPath",
                                        event.target.value,
                                    );
                                }}
                                supportText="O envio do arquivo do logotipo será integrado posteriormente."
                                value={draft.logoPath}
                            />

                            <Input
                                autoComplete="street-address"
                                disabled={isSubmitting}
                                label="Logradouro"
                                maxLength={255}
                                onChange={(event) => {
                                    updateField(
                                        "street",
                                        event.target.value,
                                    );
                                }}
                                value={draft.street}
                            />

                            <Input
                                disabled={isSubmitting}
                                label="Número"
                                maxLength={30}
                                onChange={(event) => {
                                    updateField(
                                        "number",
                                        event.target.value,
                                    );
                                }}
                                value={draft.number}
                            />

                            <Input
                                disabled={isSubmitting}
                                label="Bairro"
                                maxLength={120}
                                onChange={(event) => {
                                    updateField(
                                        "district",
                                        event.target.value,
                                    );
                                }}
                                value={draft.district}
                            />

                            <Input
                                disabled={isSubmitting}
                                label="Cidade"
                                maxLength={120}
                                onChange={(event) => {
                                    updateField(
                                        "city",
                                        event.target.value,
                                    );
                                }}
                                value={draft.city}
                            />

                            <Input
                                disabled={isSubmitting}
                                error={errors.state}
                                label="Estado (UF)"
                                maxLength={2}
                                onChange={(event) => {
                                    updateField(
                                        "state",
                                        event.target.value,
                                    );
                                }}
                                value={draft.state}
                            />

                            <Input
                                autoComplete="postal-code"
                                disabled={isSubmitting}
                                label="CEP"
                                maxLength={20}
                                onChange={(event) => {
                                    updateField(
                                        "postalCode",
                                        event.target.value,
                                    );
                                }}
                                value={draft.postalCode}
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
                                    : "Cadastrar empresa"}
                        </Button>
                    </footer>
                </form>
            </div>
        </div>
    );
}