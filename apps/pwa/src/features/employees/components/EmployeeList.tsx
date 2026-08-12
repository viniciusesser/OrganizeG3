import type {
    Employee,
    EmploymentStatus,
} from "@/features/employees/model/employee";
import {
    getEmploymentStatusLabel,
} from "@/features/employees/model/employee";
import {
    DataTable,
} from "@/shared/components/patterns";
import {
    Badge,
    Button,
} from "@/shared/components/ui";

export interface EmployeeListProps {
    readonly employees: readonly Employee[];
    readonly canEdit: boolean;
    readonly canDeactivate: boolean;
    readonly canReactivate: boolean;
    readonly busyEmployeeId?: string | null;
    readonly onView: (employee: Employee) => void;
    readonly onEdit: (employee: Employee) => void;
    readonly onDeactivate: (employee: Employee) => void;
    readonly onReactivate: (employee: Employee) => void;
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

    const [year, month, day] = value.split("-");

    if (
        year === undefined ||
        month === undefined ||
        day === undefined
    ) {
        return value;
    }

    return `${day}/${month}/${year}`;
}

export function EmployeeList({
    employees,
    canEdit,
    canDeactivate,
    canReactivate,
    busyEmployeeId = null,
    onView,
    onEdit,
    onDeactivate,
    onReactivate,
}: EmployeeListProps) {
    return (
        <DataTable>
                <thead>
                    <tr>
                        <th scope="col">Funcionário</th>
                        <th scope="col">Cargo</th>
                        <th
                            className="og3-data-table__optional"
                            scope="col"
                        >
                            Contato
                        </th>
                        <th
                            className="og3-data-table__optional"
                            scope="col"
                        >
                            Admissão
                        </th>
                        <th scope="col">Status</th>
                        <th
                            className="og3-data-table__actions-heading"
                            scope="col"
                        >
                            Ações
                        </th>
                    </tr>
                </thead>

                <tbody>
                    {employees.map((employee) => {
                        const isBusy =
                            busyEmployeeId === employee.id;

                        return (
                            <tr key={employee.id}>
                                <td data-label="Funcionário">
                                    <button
                                        className="og3-data-table__primary-link"
                                        onClick={() => {
                                            onView(employee);
                                        }}
                                        type="button"
                                    >
                                        {employee.full_name}
                                    </button>

                                    <span className="og3-data-table__metadata">
                                        {employee.code}
                                    </span>
                                </td>

                                <td data-label="Cargo">
                                    {formatOptionalValue(
                                        employee.job_title,
                                    )}
                                </td>

                                <td
                                    className="og3-data-table__optional"
                                    data-label="Contato"
                                >
                                    <span>
                                        {formatOptionalValue(
                                            employee.phone,
                                        )}
                                    </span>

                                    {employee.email !== null && (
                                        <span className="og3-data-table__metadata">
                                            {employee.email}
                                        </span>
                                    )}
                                </td>

                                <td
                                    className="og3-data-table__optional"
                                    data-label="Admissão"
                                >
                                    {formatDate(
                                        employee.admission_date,
                                    )}
                                </td>

                                <td data-label="Status">
                                    <Badge
                                        variant={getStatusBadgeVariant(
                                            employee.status,
                                        )}
                                    >
                                        {getEmploymentStatusLabel(
                                            employee.status,
                                        )}
                                    </Badge>
                                </td>

                                <td
                                    className="og3-data-table__actions-cell"
                                    data-label="Ações"
                                >
                                    <div className="og3-data-table__actions">
                                        <Button
                                            onClick={() => {
                                                onView(employee);
                                            }}
                                            size="sm"
                                            variant="secondary"
                                        >
                                            Abrir
                                        </Button>

                                        {canEdit && (
                                            <Button
                                                disabled={isBusy}
                                                onClick={() => {
                                                    onEdit(employee);
                                                }}
                                                size="sm"
                                                variant="secondary"
                                            >
                                                Editar
                                            </Button>
                                        )}

                                        {employee.is_active &&
                                            canDeactivate && (
                                                <Button
                                                    disabled={isBusy}
                                                    onClick={() => {
                                                        onDeactivate(
                                                            employee,
                                                        );
                                                    }}
                                                    size="sm"
                                                    variant="danger"
                                                >
                                                    Inativar
                                                </Button>
                                            )}

                                        {!employee.is_active &&
                                            canReactivate && (
                                                <Button
                                                    disabled={isBusy}
                                                    onClick={() => {
                                                        onReactivate(
                                                            employee,
                                                        );
                                                    }}
                                                    size="sm"
                                                >
                                                    Reativar
                                                </Button>
                                            )}
                                    </div>
                                </td>
                            </tr>
                        );
                    })}
                </tbody>
        </DataTable>
    );
}