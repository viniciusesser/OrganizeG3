import {
    useId,
    useState,
} from "react";
import type {
    FormEvent,
} from "react";

import type {
    Customer,
    CustomerCreateInput,
    CustomerType,
} from "@/features/customers/model/customer";
import {
    InlineMessage,
    Select,
} from "@/shared/components/patterns";
import {
    Button,
    Heading,
    Input,
    Text,
} from "@/shared/components/ui";

export interface CustomerFormProps {
    readonly customer?: Customer;
    readonly isSubmitting: boolean;
    readonly submitError?: string | null;
    readonly onCancel: () => void;
    readonly onSubmit: (
        values: CustomerCreateInput,
    ) => Promise<void> | void;
}

interface CustomerFormErrors {
    readonly name?: string;
    readonly email?: string;
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
    name: string,
    email: string,
): CustomerFormErrors {
    const errors: {
        name?: string;
        email?: string;
    } = {};

    if (name.trim().length === 0) {
        errors.name =
            "Informe o nome do cliente.";
    }

    const normalizedEmail =
        email.trim();

    if (
        normalizedEmail.length > 0 &&
        !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
            normalizedEmail,
        )
    ) {
        errors.email =
            "Informe um email válido.";
    }

    return errors;
}

export function CustomerForm({
    customer,
    isSubmitting,
    submitError = null,
    onCancel,
    onSubmit,
}: CustomerFormProps) {
    const titleId = useId();

    const [name, setName] =
        useState(
            customer?.name ?? "",
        );

    const [customerType, setCustomerType] =
        useState<CustomerType>(
            customer?.customer_type ??
            "INDIVIDUAL",
        );

    const [documentNumber, setDocumentNumber] =
        useState(
            customer?.document_number ?? "",
        );

    const [email, setEmail] =
        useState(
            customer?.email ?? "",
        );

    const [phone, setPhone] =
        useState(
            customer?.phone ?? "",
        );

    const [errors, setErrors] =
        useState<CustomerFormErrors>({});

    const isEditing =
        customer !== undefined;

    const handleSubmit = async (
        event: FormEvent<HTMLFormElement>,
    ): Promise<void> => {
        event.preventDefault();

        const nextErrors =
            validateForm(
                name,
                email,
            );

        setErrors(nextErrors);

        if (
            nextErrors.name !== undefined ||
            nextErrors.email !== undefined
        ) {
            return;
        }

        await onSubmit({
            name: name.trim(),
            customer_type: customerType,
            document_number:
                optionalValue(
                    documentNumber,
                ),
            email: optionalValue(email),
            phone: optionalValue(phone),
        });
    };

    return (
        <div
            aria-labelledby={titleId}
            aria-modal="true"
            className="og3-dialog-backdrop"
            role="dialog"
        >
            <div
                className="og3-dialog og3-dialog--md"
            >
                <header
                    className="og3-dialog__header"
                >
                    <div
                        className="og3-dialog__heading"
                    >
                        <Heading
                            className="og3-dialog__title"
                            level={3}
                        >
                            <span id={titleId}>
                                {isEditing
                                    ? "Editar cliente"
                                    : "Novo cliente"}
                            </span>
                        </Heading>

                        <Text tone="secondary">
                            Preencha os dados principais do cadastro.
                        </Text>
                    </div>

                    <Button
                        aria-label="Fechar formulário"
                        disabled={isSubmitting}
                        onClick={onCancel}
                        size="sm"
                        type="button"
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
                    <div
                        className="og3-dialog__body"
                    >
                        <div
                            className="og3-form-grid"
                        >
                            <Input
                                autoComplete="name"
                                autoFocus
                                disabled={isSubmitting}
                                error={errors.name}
                                label="Nome do cliente *"
                                maxLength={200}
                                onChange={(event) => {
                                    setName(
                                        event.target.value,
                                    );
                                }}
                                value={name}
                            />

                            <Select
                                disabled={isSubmitting}
                                label="Tipo de pessoa *"
                                onChange={(event) => {
                                    setCustomerType(
                                        event.target.value as CustomerType,
                                    );
                                }}
                                value={customerType}
                            >
                                <option value="INDIVIDUAL">
                                    Pessoa Física
                                </option>

                                <option value="CORPORATE">
                                    Pessoa Jurídica
                                </option>
                            </Select>

                            <Input
                                disabled={isSubmitting}
                                label={
                                    customerType ===
                                        "INDIVIDUAL"
                                        ? "CPF"
                                        : "CNPJ"
                                }
                                maxLength={18}
                                onChange={(event) => {
                                    setDocumentNumber(
                                        event.target.value,
                                    );
                                }}
                                value={documentNumber}
                            />

                            <Input
                                autoComplete="tel"
                                disabled={isSubmitting}
                                label="Telefone"
                                maxLength={30}
                                onChange={(event) => {
                                    setPhone(
                                        event.target.value,
                                    );
                                }}
                                type="tel"
                                value={phone}
                            />

                            <Input
                                autoComplete="email"
                                disabled={isSubmitting}
                                error={errors.email}
                                label="Email"
                                maxLength={320}
                                onChange={(event) => {
                                    setEmail(
                                        event.target.value,
                                    );
                                }}
                                type="email"
                                value={email}
                            />
                        </div>

                        {submitError !== null && (
                            <InlineMessage tone="danger">
                                {submitError}
                            </InlineMessage>
                        )}
                    </div>

                    <footer
                        className="og3-dialog__footer"
                    >
                        <Button
                            disabled={isSubmitting}
                            onClick={onCancel}
                            type="button"
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
                                    : "Salvar cliente"}
                        </Button>
                    </footer>
                </form>
            </div>
        </div>
    );
}
