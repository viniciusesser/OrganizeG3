import {
    useId,
    useState,
} from "react";
import type {
    FormEvent,
} from "react";

import type {
    Branch,
    CreateBranchPayload,
} from "@/features/branches/model/branch";
import {
    useAccessibleOverlay,
} from "@/shared/hooks/useAccessibleOverlay";
import {
    Button,
    Heading,
    Input,
    Text,
} from "@/shared/components/ui";

export interface BranchFormProps {
    readonly branch?: Branch;
    readonly isSubmitting: boolean;
    readonly submitError?: string | null;
    readonly onCancel: () => void;
    readonly onSubmit: (
        values: CreateBranchPayload,
    ) => Promise<void> | void;
}

interface BranchFormDraft {
    readonly code: string;
    readonly name: string;
    readonly legalName: string;
    readonly documentNumber: string;
    readonly stateRegistration: string;
    readonly email: string;
    readonly phone: string;
    readonly website: string;
    readonly street: string;
    readonly number: string;
    readonly district: string;
    readonly city: string;
    readonly state: string;
    readonly postalCode: string;
    readonly isHeadquarters: boolean;
}

interface BranchFormErrors {
    readonly code?: string;
    readonly name?: string;
    readonly email?: string;
    readonly website?: string;
    readonly state?: string;
}

function createDraft(
    branch?: Branch,
): BranchFormDraft {
    return {
        code:
            branch?.code ??
            "",
        name:
            branch?.name ??
            "",
        legalName:
            branch?.legal_name ??
            "",
        documentNumber:
            branch?.document_number ??
            "",
        stateRegistration:
            branch?.state_registration ??
            "",
        email:
            branch?.email ??
            "",
        phone:
            branch?.phone ??
            "",
        website:
            branch?.website ??
            "",
        street:
            branch?.street ??
            "",
        number:
            branch?.number ??
            "",
        district:
            branch?.district ??
            "",
        city:
            branch?.city ??
            "",
        state:
            branch?.state ??
            "",
        postalCode:
            branch?.postal_code ??
            "",
        isHeadquarters:
            branch?.is_headquarters ??
            false,
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

function isValidWebsite(
    value: string,
): boolean {
    if (
        value.length === 0
    ) {
        return true;
    }

    try {
        const url =
            new URL(
                value,
            );

        return (
            url.protocol ===
            "http:" ||
            url.protocol ===
            "https:"
        );
    }
    catch {
        return false;
    }
}

function validateForm(
    draft: BranchFormDraft,
): BranchFormErrors {
    const errors: {
        code?: string;
        name?: string;
        email?: string;
        website?: string;
        state?: string;
    } = {};

    if (
        draft.code
            .trim()
            .length === 0
    ) {
        errors.code =
            "Informe o código da filial.";
    }

    if (
        draft.name
            .trim()
            .length === 0
    ) {
        errors.name =
            "Informe o nome da filial.";
    }

    const normalizedEmail =
        draft.email.trim();

    if (
        normalizedEmail.length >
        0 &&
        !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
            normalizedEmail,
        )
    ) {
        errors.email =
            "Informe um email válido.";
    }

    const normalizedWebsite =
        draft.website.trim();

    if (
        !isValidWebsite(
            normalizedWebsite,
        )
    ) {
        errors.website =
            "Informe um endereço iniciado por http:// ou https://.";
    }

    const normalizedState =
        draft.state.trim();

    if (
        normalizedState.length >
        0 &&
        !/^[A-Za-z]{2}$/.test(
            normalizedState,
        )
    ) {
        errors.state =
            "Informe a UF com duas letras.";
    }

    return errors;
}

export function BranchForm({
    branch,
    isSubmitting,
    submitError = null,
    onCancel,
    onSubmit,
}: BranchFormProps) {
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
    ] = useState<BranchFormDraft>(
        createDraft(
            branch,
        ),
    );

    const [
        errors,
        setErrors,
    ] = useState<BranchFormErrors>(
        {},
    );

    const isEditing =
        branch !== undefined;

    const updateTextField = (
        field:
            keyof Omit<
                BranchFormDraft,
                "isHeadquarters"
            >,
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
                draft.code
                    .trim()
                    .toUpperCase(),
            name:
                draft.name
                    .trim(),
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
            phone:
                optionalValue(
                    draft.phone,
                ),
            website:
                optionalValue(
                    draft.website,
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
            postal_code:
                optionalValue(
                    draft.postalCode,
                ),
            is_headquarters:
                draft.isHeadquarters,
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
                                        ? "Editar filial"
                                        : "Nova filial"
                                }
                            </span>
                        </Heading>

                        <Text
                            id={
                                descriptionId
                            }
                            tone="secondary"
                        >
                            Preencha a identificação, o contato e o endereço da unidade.
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
                                label="Código da filial *"
                                maxLength={
                                    100
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateTextField(
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
                                label="Nome da filial *"
                                maxLength={
                                    255
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateTextField(
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
                                label="Razão social"
                                maxLength={
                                    255
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateTextField(
                                        "legalName",
                                        event
                                            .target
                                            .value,
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
                                label="CNPJ ou documento"
                                maxLength={
                                    30
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateTextField(
                                        "documentNumber",
                                        event
                                            .target
                                            .value,
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
                                    30
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateTextField(
                                        "stateRegistration",
                                        event
                                            .target
                                            .value,
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
                                    320
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateTextField(
                                        "email",
                                        event
                                            .target
                                            .value,
                                    );
                                }}
                                type="email"
                                value={
                                    draft.email
                                }
                            />

                            <Input
                                autoComplete="tel"
                                disabled={
                                    isSubmitting
                                }
                                label="Telefone"
                                maxLength={
                                    30
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateTextField(
                                        "phone",
                                        event
                                            .target
                                            .value,
                                    );
                                }}
                                type="tel"
                                value={
                                    draft.phone
                                }
                            />

                            <Input
                                disabled={
                                    isSubmitting
                                }
                                error={
                                    errors.website
                                }
                                label="Site"
                                maxLength={
                                    255
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateTextField(
                                        "website",
                                        event
                                            .target
                                            .value,
                                    );
                                }}
                                placeholder="https://exemplo.com.br"
                                type="url"
                                value={
                                    draft.website
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
                                    updateTextField(
                                        "street",
                                        event
                                            .target
                                            .value,
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
                                    30
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateTextField(
                                        "number",
                                        event
                                            .target
                                            .value,
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
                                    120
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateTextField(
                                        "district",
                                        event
                                            .target
                                            .value,
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
                                    120
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateTextField(
                                        "city",
                                        event
                                            .target
                                            .value,
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
                                    updateTextField(
                                        "state",
                                        event
                                            .target
                                            .value,
                                    );
                                }}
                                value={
                                    draft.state
                                }
                            />

                            <Input
                                autoComplete="postal-code"
                                disabled={
                                    isSubmitting
                                }
                                label="CEP"
                                maxLength={
                                    20
                                }
                                onChange={(
                                    event,
                                ) => {
                                    updateTextField(
                                        "postalCode",
                                        event
                                            .target
                                            .value,
                                    );
                                }}
                                value={
                                    draft.postalCode
                                }
                            />
                        </div>

                        <label
                            className="og3-checkbox-field"
                        >
                            <input
                                checked={
                                    draft.isHeadquarters
                                }
                                disabled={
                                    isSubmitting
                                }
                                onChange={(
                                    event,
                                ) => {
                                    setDraft(
                                        (
                                            current,
                                        ) => ({
                                            ...current,
                                            isHeadquarters:
                                                event
                                                    .target
                                                    .checked,
                                        }),
                                    );
                                }}
                                type="checkbox"
                            />

                            <span>
                                Esta unidade é a matriz da empresa
                            </span>
                        </label>

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
                                        : "Salvar filial"
                            }
                        </Button>
                    </footer>
                </form>
            </div>
        </div>
    );
}