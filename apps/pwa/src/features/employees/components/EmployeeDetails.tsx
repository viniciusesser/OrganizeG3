import {
    useId,
} from "react";

import type {
    Employee,
    EmploymentStatus,
} from "@/features/employees/model/employee";
import {
    getEmploymentStatusLabel,
} from "@/features/employees/model/employee";
import {
    useAccessibleOverlay,
} from "@/shared/hooks/useAccessibleOverlay";
import {
    Badge,
    Button,
    Heading,
    Text,
} from "@/shared/components/ui";

export interface EmployeeDetailsProps {
    readonly employee: Employee;
    readonly canEdit: boolean;
    readonly canDeactivate: boolean;
    readonly canReactivate: boolean;
    readonly isSubmitting: boolean;
    readonly onClose: () => void;
    readonly onEdit: (
        employee: Employee,
    ) => void;
    readonly onDeactivate: (
        employee: Employee,
    ) => void;
    readonly onReactivate: (
        employee: Employee,
    ) => void;
}

type EmployeeBadgeVariant =
    | "success"
    | "warning"
    | "neutral";

function getStatusBadgeVariant(
    status: EmploymentStatus,
): EmployeeBadgeVariant {
    if (status === "ACTIVE") {
        return "success";
    }

    if (status === "ON_LEAVE") {
        return "warning";
    }

    return "neutral";
}

function formatOptionalValue(
    value: string | null,
): string {
    return value?.trim() || "—";
}

function formatDate(
    value: string | null,
): string {
    if (value === null) {
        return "—";
    }

    const [
        year,
        month,
        day,
    ] = value.split("-");

    if (
        year === undefined ||
        month === undefined ||
        day === undefined
    ) {
        return value;
    }

    return `${day}/${month}/${year}`;
}

export function EmployeeDetails({
    employee,
    canEdit,
    canDeactivate,
    canReactivate,
    isSubmitting,
    onClose,
    onEdit,
    onDeactivate,
    onReactivate,
}: EmployeeDetailsProps) {
    const titleId =
        useId();

    const {
        overlayRef,
    } = useAccessibleOverlay<HTMLDivElement>({
        closeOnEscape:
            !isSubmitting,
        onClose,
    });

    return (
        <div
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
                        <Badge
                            variant={
                                getStatusBadgeVariant(
                                    employee.status,
                                )
                            }
                        >
                            {
                                getEmploymentStatusLabel(
                                    employee.status,
                                )
                            }
                        </Badge>

                        <Heading
                            level={3}
                        >
                            <span
                                id={
                                    titleId
                                }
                            >
                                {
                                    employee.full_name
                                }
                            </span>
                        </Heading>

                        <Text
                            tone="secondary"
                        >
                            {
                                employee.code
                            }
                        </Text>
                    </div>

                    <Button
                        aria-label="Fechar detalhes"
                        data-og3-autofocus="true"
                        disabled={
                            isSubmitting
                        }
                        onClick={
                            onClose
                        }
                        size="sm"
                        variant="secondary"
                    >
                        Fechar
                    </Button>
                </header>

                <div
                    className="og3-dialog__body"
                >
                    <dl
                        className="og3-details-grid"
                    >
                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Documento
                            </dt>

                            <dd>
                                {
                                    formatOptionalValue(
                                        employee.document_number,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Cargo ou função
                            </dt>

                            <dd>
                                {
                                    formatOptionalValue(
                                        employee.job_title,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Tipo de contrato
                            </dt>

                            <dd>
                                {
                                    formatOptionalValue(
                                        employee.contract_type,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Telefone
                            </dt>

                            <dd>
                                {
                                    formatOptionalValue(
                                        employee.phone,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Email
                            </dt>

                            <dd>
                                {
                                    formatOptionalValue(
                                        employee.email,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Data de nascimento
                            </dt>

                            <dd>
                                {
                                    formatDate(
                                        employee.birth_date,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Data de admissão
                            </dt>

                            <dd>
                                {
                                    formatDate(
                                        employee.admission_date,
                                    )
                                }
                            </dd>
                        </div>

                        <div
                            className="og3-details-grid__item"
                        >
                            <dt>
                                Data de desligamento
                            </dt>

                            <dd>
                                {
                                    formatDate(
                                        employee.termination_date,
                                    )
                                }
                            </dd>
                        </div>
                    </dl>
                </div>

                <footer
                    className="og3-dialog__footer"
                >
                    {canEdit && (
                        <Button
                            disabled={
                                isSubmitting
                            }
                            onClick={() => {
                                onEdit(
                                    employee,
                                );
                            }}
                            variant="secondary"
                        >
                            Editar funcionário
                        </Button>
                    )}

                    {employee.is_active &&
                        canDeactivate && (
                            <Button
                                disabled={
                                    isSubmitting
                                }
                                onClick={() => {
                                    onDeactivate(
                                        employee,
                                    );
                                }}
                                variant="danger"
                            >
                                Inativar funcionário
                            </Button>
                        )}

                    {!employee.is_active &&
                        canReactivate && (
                            <Button
                                disabled={
                                    isSubmitting
                                }
                                onClick={() => {
                                    onReactivate(
                                        employee,
                                    );
                                }}
                            >
                                Reativar funcionário
                            </Button>
                        )}
                </footer>
            </div>
        </div>
    );
}