import type {
    Branch,
} from "@/features/branches/model/branch";
import {
    DataTable,
} from "@/shared/components/patterns";
import {
    Badge,
    Button,
} from "@/shared/components/ui";

export interface BranchListProps {
    readonly branches: readonly Branch[];
    readonly canEdit: boolean;
    readonly canDeactivate: boolean;
    readonly canReactivate: boolean;
    readonly busyBranchId?: string | null;
    readonly onView: (branch: Branch) => void;
    readonly onEdit: (branch: Branch) => void;
    readonly onDeactivate: (branch: Branch) => void;
    readonly onReactivate: (branch: Branch) => void;
}

function formatOptionalValue(
    value: string | null,
): string {
    return value?.trim() || "—";
}

function formatLocation(
    branch: Branch,
): string {
    const location = [
        branch.city,
        branch.state,
    ]
        .filter(
            (value): value is string =>
                value !== null &&
                value.trim().length > 0,
        )
        .join(" - ");

    return location || "—";
}

export function BranchList({
    branches,
    canEdit,
    canDeactivate,
    canReactivate,
    busyBranchId = null,
    onView,
    onEdit,
    onDeactivate,
    onReactivate,
}: BranchListProps) {
    return (
        <DataTable>
                <thead>
                    <tr>
                        <th scope="col">Filial</th>
                        <th scope="col">Tipo</th>

                        <th
                            className="og3-data-table__optional"
                            scope="col"
                        >
                            Localidade
                        </th>

                        <th
                            className="og3-data-table__optional"
                            scope="col"
                        >
                            Contato
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
                    {branches.map((branch) => {
                        const isBusy =
                            busyBranchId === branch.id;

                        return (
                            <tr key={branch.id}>
                                <td data-label="Filial">
                                    <button
                                        className="og3-data-table__primary-link"
                                        onClick={() => {
                                            onView(branch);
                                        }}
                                        type="button"
                                    >
                                        {branch.name}
                                    </button>

                                    <span className="og3-data-table__metadata">
                                        {branch.code}
                                    </span>
                                </td>

                                <td data-label="Tipo">
                                    <Badge
                                        variant={
                                            branch.is_headquarters
                                                ? "accent"
                                                : "neutral"
                                        }
                                    >
                                        {branch.is_headquarters
                                            ? "Matriz"
                                            : "Filial"}
                                    </Badge>
                                </td>

                                <td
                                    className="og3-data-table__optional"
                                    data-label="Localidade"
                                >
                                    {formatLocation(branch)}
                                </td>

                                <td
                                    className="og3-data-table__optional"
                                    data-label="Contato"
                                >
                                    <span>
                                        {formatOptionalValue(
                                            branch.phone,
                                        )}
                                    </span>

                                    {branch.email !== null && (
                                        <span className="og3-data-table__metadata">
                                            {branch.email}
                                        </span>
                                    )}
                                </td>

                                <td data-label="Status">
                                    <Badge
                                        variant={
                                            branch.is_active
                                                ? "success"
                                                : "neutral"
                                        }
                                    >
                                        {branch.is_active
                                            ? "Ativa"
                                            : "Inativa"}
                                    </Badge>
                                </td>

                                <td
                                    className="og3-data-table__actions-cell"
                                    data-label="Ações"
                                >
                                    <div className="og3-data-table__actions">
                                        <Button
                                            onClick={() => {
                                                onView(branch);
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
                                                    onEdit(branch);
                                                }}
                                                size="sm"
                                                variant="secondary"
                                            >
                                                Editar
                                            </Button>
                                        )}

                                        {branch.is_active &&
                                            canDeactivate && (
                                                <Button
                                                    disabled={isBusy}
                                                    onClick={() => {
                                                        onDeactivate(
                                                            branch,
                                                        );
                                                    }}
                                                    size="sm"
                                                    variant="danger"
                                                >
                                                    Inativar
                                                </Button>
                                            )}

                                        {!branch.is_active &&
                                            canReactivate && (
                                                <Button
                                                    disabled={isBusy}
                                                    onClick={() => {
                                                        onReactivate(
                                                            branch,
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