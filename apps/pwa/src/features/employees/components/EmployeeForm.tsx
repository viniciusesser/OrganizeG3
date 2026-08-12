import { useId, useState } from "react";
import type { FormEvent } from "react";

import type {
    Employee,
    EmployeeCreateInput,
} from "@/features/employees/model/employee";
import {
    Button,
    Heading,
    Input,
    Text,
} from "@/shared/components/ui";

export interface EmployeeFormProps {
    readonly employee?: Employee;
    readonly isSubmitting: boolean;
    readonly submitError?: string | null;
    readonly onCancel: () => void;
    readonly onSubmit: (
        values: EmployeeCreateInput,
    ) => Promise<void> | void;
}

interface EmployeeFormDraft {
    readonly code: string;
    readonly fullName: string;
    readonly documentNumber: string;
    readonly email: string;
    readonly phone: string;
    readonly jobTitle: string;
    readonly contractType: string;
    readonly birthDate: string;
    readonly admissionDate: string;
}

interface EmployeeFormErrors {
    readonly code?: string;
    readonly fullName?: string;
    readonly email?: string;
    readonly birthDate?: string;
    readonly admissionDate?: string;
}

function createDraft(
    employee?: Employee,
): EmployeeFormDraft {
    return {
        code: employee?.code ?? "",
        fullName: employee?.full_name ?? "",
        documentNumber:
            employee?.document_number ?? "",
        email: employee?.email ?? "",
        phone: employee?.phone ?? "",
        jobTitle: employee?.job_title ?? "",
        contractType:
            employee?.contract_type ?? "",
        birthDate: employee?.birth_date ?? "",
        admissionDate:
            employee?.admission_date ?? "",
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

function isValidDateValue(
    value: string,
): boolean {
    if (value.length === 0) {
        return true;
    }

    return /^\d{4}-\d{2}-\d{2}$/.test(value);
}

function validateForm(
    draft: EmployeeFormDraft,
): EmployeeFormErrors {
    const errors: {
        code?: string;
        fullName?: string;
        email?: string;
        birthDate?: string;
        admissionDate?: string;
    } = {};

    if (draft.code.trim().length === 0) {
        errors.code =
            "Informe o código do funcionário.";
    }

    if (draft.fullName.trim().length === 0) {
        errors.fullName =
            "Informe o nome completo do funcionário.";
    }

    const normalizedEmail = draft.email.trim();

    if (
        normalizedEmail.length > 0 &&
        !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(
            normalizedEmail,
        )
    ) {
        errors.email = "Informe um email válido.";
    }

    if (!isValidDateValue(draft.birthDate)) {
        errors.birthDate =
            "Informe uma data de nascimento válida.";
    }

    if (!isValidDateValue(draft.admissionDate)) {
        errors.admissionDate =
            "Informe uma data de admissão válida.";
    }

    if (
        draft.birthDate.length > 0 &&
        draft.admissionDate.length > 0 &&
        draft.admissionDate < draft.birthDate
    ) {
        errors.admissionDate =
            "A admissão não pode ser anterior ao nascimento.";
    }

    return errors;
}

export function EmployeeForm({
    employee,
    isSubmitting,
    submitError = null,
    onCancel,
    onSubmit,
}: EmployeeFormProps) {
    const titleId = useId();
    const [draft, setDraft] =
        useState<EmployeeFormDraft>(
            createDraft(employee),
        );
    const [errors, setErrors] =
        useState<EmployeeFormErrors>({});
    const isEditing = employee !== undefined;

    const updateField = (
        field: keyof EmployeeFormDraft,
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

        const nextErrors = validateForm(draft);
        setErrors(nextErrors);

        if (Object.keys(nextErrors).length > 0) {
            return;
        }

        await onSubmit({
            code: draft.code.trim().toUpperCase(),
            full_name: draft.fullName.trim(),
            document_number: optionalValue(
                draft.documentNumber,
            ),
            email: optionalValue(draft.email),
            phone: optionalValue(draft.phone),
            job_title: optionalValue(draft.jobTitle),
            contract_type: optionalValue(
                draft.contractType,
            ),
            birth_date: optionalValue(
                draft.birthDate,
            ),
            admission_date: optionalValue(
                draft.admissionDate,
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
                                    ? "Editar funcionário"
                                    : "Novo funcionário"}
                            </span>
                        </Heading>

                        <Text tone="secondary">
                            Preencha a identificação, o contato e os dados
                            profissionais do funcionário.
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
                                label="Código do funcionário *"
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
                                autoComplete="name"
                                disabled={isSubmitting}
                                error={errors.fullName}
                                label="Nome completo *"
                                maxLength={255}
                                onChange={(event) => {
                                    updateField(
                                        "fullName",
                                        event.target.value,
                                    );
                                }}
                                value={draft.fullName}
                            />

                            <Input
                                disabled={isSubmitting}
                                label="CPF ou documento"
                                maxLength={30}
                                onChange={(event) => {
                                    updateField(
                                        "documentNumber",
                                        event.target.value,
                                    );
                                }}
                                value={draft.documentNumber}
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
                                disabled={isSubmitting}
                                label="Cargo ou função"
                                maxLength={120}
                                onChange={(event) => {
                                    updateField(
                                        "jobTitle",
                                        event.target.value,
                                    );
                                }}
                                value={draft.jobTitle}
                            />

                            <Input
                                disabled={isSubmitting}
                                label="Tipo de contrato"
                                maxLength={60}
                                onChange={(event) => {
                                    updateField(
                                        "contractType",
                                        event.target.value,
                                    );
                                }}
                                supportText="Exemplos: CLT, PJ, temporário ou aprendiz."
                                value={draft.contractType}
                            />

                            <Input
                                disabled={isSubmitting}
                                error={errors.birthDate}
                                label="Data de nascimento"
                                onChange={(event) => {
                                    updateField(
                                        "birthDate",
                                        event.target.value,
                                    );
                                }}
                                type="date"
                                value={draft.birthDate}
                            />

                            <Input
                                disabled={isSubmitting}
                                error={errors.admissionDate}
                                label="Data de admissão"
                                onChange={(event) => {
                                    updateField(
                                        "admissionDate",
                                        event.target.value,
                                    );
                                }}
                                type="date"
                                value={draft.admissionDate}
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
                                    : "Salvar funcionário"}
                        </Button>
                    </footer>
                </form>
            </div>
        </div>
    );
}