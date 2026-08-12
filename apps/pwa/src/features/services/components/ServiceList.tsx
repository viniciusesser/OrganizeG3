import type {
    Service,
} from "@/features/services/model/service";
import {
    getServiceExecutionModeLabel,
} from "@/features/services/model/service";
import {
    DataTable,
} from "@/shared/components/patterns";
import {
    Badge,
    Button,
} from "@/shared/components/ui";

export interface ServiceListProps {
    readonly services:
    readonly Service[];
    readonly canEdit: boolean;
    readonly canDeactivate: boolean;
    readonly canReactivate: boolean;
    readonly busyServiceId?:
    string | null;
    readonly onView: (
        service: Service,
    ) => void;
    readonly onEdit: (
        service: Service,
    ) => void;
    readonly onDeactivate: (
        service: Service,
    ) => void;
    readonly onReactivate: (
        service: Service,
    ) => void;
}

function formatDuration(
    minutes: number | null,
): string {
    return minutes === null
        ? "—"
        : `${minutes} min`;
}

export function ServiceList({
    services,
    canEdit,
    canDeactivate,
    canReactivate,
    busyServiceId = null,
    onView,
    onEdit,
    onDeactivate,
    onReactivate,
}: ServiceListProps) {
    return (
        <DataTable>
            <thead>
                <tr>
                    <th scope="col">
                        Serviço
                    </th>

                    <th scope="col">
                        Categoria
                    </th>

                    <th
                        className="og3-data-table__optional"
                        scope="col"
                    >
                        Unidade
                    </th>

                    <th
                        className="og3-data-table__optional"
                        scope="col"
                    >
                        Execução
                    </th>

                    <th
                        className="og3-data-table__optional"
                        scope="col"
                    >
                        Duração
                    </th>

                    <th scope="col">
                        Status
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
                {services.map(
                    (service) => {
                        const isBusy =
                            busyServiceId ===
                            service.id;

                        return (
                            <tr key={service.id}>
                                <td data-label="Serviço">
                                    <button
                                        className="og3-data-table__primary-link"
                                        onClick={() => {
                                            onView(
                                                service,
                                            );
                                        }}
                                        type="button"
                                    >
                                        {service.name}
                                    </button>

                                    <span className="og3-data-table__metadata">
                                        {service.code}
                                    </span>
                                </td>

                                <td data-label="Categoria">
                                    {service.category}
                                </td>

                                <td
                                    className="og3-data-table__optional"
                                    data-label="Unidade"
                                >
                                    {service.unit}
                                </td>

                                <td
                                    className="og3-data-table__optional"
                                    data-label="Execução"
                                >
                                    {getServiceExecutionModeLabel(
                                        service.execution_mode,
                                    )}
                                </td>

                                <td
                                    className="og3-data-table__optional"
                                    data-label="Duração"
                                >
                                    {formatDuration(
                                        service
                                            .estimated_duration_minutes,
                                    )}
                                </td>

                                <td data-label="Status">
                                    <Badge
                                        variant={
                                            service.is_active
                                                ? "success"
                                                : "neutral"
                                        }
                                    >
                                        {service.is_active
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
                                                    service,
                                                );
                                            }}
                                            size="sm"
                                            variant="secondary"
                                        >
                                            Abrir
                                        </Button>

                                        {canEdit && (
                                            <Button
                                                disabled={
                                                    isBusy
                                                }
                                                onClick={() => {
                                                    onEdit(
                                                        service,
                                                    );
                                                }}
                                                size="sm"
                                                variant="secondary"
                                            >
                                                Editar
                                            </Button>
                                        )}

                                        {service.is_active &&
                                            canDeactivate && (
                                                <Button
                                                    disabled={
                                                        isBusy
                                                    }
                                                    onClick={() => {
                                                        onDeactivate(
                                                            service,
                                                        );
                                                    }}
                                                    size="sm"
                                                    variant="danger"
                                                >
                                                    Inativar
                                                </Button>
                                            )}

                                        {!service.is_active &&
                                            canReactivate && (
                                                <Button
                                                    disabled={
                                                        isBusy
                                                    }
                                                    onClick={() => {
                                                        onReactivate(
                                                            service,
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