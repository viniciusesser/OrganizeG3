import type {
    Machine,
} from "@/features/machines/model/machine";
import {
    getMachineStatusLabel,
} from "@/features/machines/model/machine";
import {
    DataTable,
} from "@/shared/components/patterns";
import {
    Badge,
    Button,
} from "@/shared/components/ui";

export interface MachineListProps {
    readonly machines: readonly Machine[];
    readonly canEdit: boolean;
    readonly canDeactivate: boolean;
    readonly canReactivate: boolean;
    readonly busyMachineId?: string | null;
    readonly onView: (
        machine: Machine,
    ) => void;
    readonly onEdit: (
        machine: Machine,
    ) => void;
    readonly onDeactivate: (
        machine: Machine,
    ) => void;
    readonly onReactivate: (
        machine: Machine,
    ) => void;
}

function statusVariant(
    machine: Machine,
): "success" | "neutral" {
    if (
        !machine.is_active
    ) {
        return "neutral";
    }

    if (
        machine.status === "AVAILABLE"
    ) {
        return "success";
    }

    return "neutral";
}

export function MachineList({
    machines,
    canEdit,
    canDeactivate,
    canReactivate,
    busyMachineId = null,
    onView,
    onEdit,
    onDeactivate,
    onReactivate,
}: MachineListProps) {
    return (
        <DataTable>
            <thead>
                <tr>
                    <th scope="col">
                        Máquina
                    </th>

                    <th scope="col">
                        Tipo
                    </th>

                    <th
                        className="og3-data-table__optional"
                        scope="col"
                    >
                        Fabricante / modelo
                    </th>

                    <th scope="col">
                        Operação
                    </th>

                    <th scope="col">
                        Cadastro
                    </th>

                    <th
                        className="og3-data-table__actions-heading"
                        scope="col"
                    >
                        Ações
                    </th>
                </tr>
            </thead>

            <tbody>
                {machines.map(
                    (machine) => {
                        const isBusy =
                            busyMachineId ===
                            machine.id;

                        return (
                            <tr key={machine.id}>
                                <td data-label="Máquina">
                                    <button
                                        className="og3-data-table__primary-link"
                                        onClick={() => {
                                            onView(
                                                machine,
                                            );
                                        }}
                                        type="button"
                                    >
                                        {machine.name}
                                    </button>

                                    <span className="og3-data-table__metadata">
                                        {machine.code}
                                    </span>
                                </td>

                                <td data-label="Tipo">
                                    {machine.machine_type}
                                </td>

                                <td
                                    className="og3-data-table__optional"
                                    data-label="Fabricante / modelo"
                                >
                                    {[
                                        machine.manufacturer,
                                        machine.model,
                                    ]
                                        .filter(Boolean)
                                        .join(" · ") || "—"}
                                </td>

                                <td data-label="Operação">
                                    <Badge
                                        variant={statusVariant(
                                            machine,
                                        )}
                                    >
                                        {getMachineStatusLabel(
                                            machine.status,
                                        )}
                                    </Badge>
                                </td>

                                <td data-label="Cadastro">
                                    <Badge
                                        variant={
                                            machine.is_active
                                                ? "success"
                                                : "neutral"
                                        }
                                    >
                                        {machine.is_active
                                            ? "Ativo"
                                            : "Inativo"}
                                    </Badge>
                                </td>

                                <td
                                    className="og3-data-table__actions-cell"
                                    data-label="Ações"
                                >
                                    <div className="og3-data-table__actions">
                                        <Button
                                            onClick={() => {
                                                onView(
                                                    machine,
                                                );
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
                                                    onEdit(
                                                        machine,
                                                    );
                                                }}
                                                size="sm"
                                                variant="secondary"
                                            >
                                                Editar
                                            </Button>
                                        )}

                                        {machine.is_active &&
                                            canDeactivate && (
                                                <Button
                                                    disabled={isBusy}
                                                    onClick={() => {
                                                        onDeactivate(
                                                            machine,
                                                        );
                                                    }}
                                                    size="sm"
                                                    variant="danger"
                                                >
                                                    Inativar
                                                </Button>
                                            )}

                                        {!machine.is_active &&
                                            canReactivate && (
                                                <Button
                                                    disabled={isBusy}
                                                    onClick={() => {
                                                        onReactivate(
                                                            machine,
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
                    },
                )}
            </tbody>
        </DataTable>
    );
}