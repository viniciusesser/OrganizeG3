import type {
    Customer,
} from "@/features/customers/model/customer";
import {
    formatCustomerDocument,
    formatCustomerPhone,
    getCustomerTypeLabel,
} from "@/features/customers/model/customer";
import {
    DataTable,
} from "@/shared/components/patterns";
import {
    Badge,
    Button,
} from "@/shared/components/ui";

export interface CustomerListProps {
    readonly customers: readonly Customer[];
    readonly canEdit: boolean;
    readonly canArchive: boolean;
    readonly canReactivate: boolean;
    readonly busyCustomerId?: number | null;
    readonly onView: (customer: Customer) => void;
    readonly onEdit: (customer: Customer) => void;
    readonly onArchive: (customer: Customer) => void;
    readonly onReactivate: (customer: Customer) => void;
}

export function CustomerList({
    customers,
    canEdit,
    canArchive,
    canReactivate,
    busyCustomerId = null,
    onView,
    onEdit,
    onArchive,
    onReactivate,
}: CustomerListProps) {
    return (
        <DataTable>
            <thead>
                <tr>
                    <th scope="col">
                        Cliente
                    </th>
                    <th
                        className="og3-data-table__optional"
                        scope="col"
                    >
                        Tipo
                    </th>
                    <th
                        className="og3-data-table__optional"
                        scope="col"
                    >
                        Documento
                    </th>
                    <th scope="col">
                        Contato
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
                {customers.map(
                    (customer) => {
                        const isBusy =
                            busyCustomerId ===
                            customer.id;

                        return (
                            <tr
                                key={customer.id}
                            >
                                <td data-label="Cliente">
                                    <button
                                        className="og3-data-table__primary-link"
                                        onClick={() => {
                                            onView(customer);
                                        }}
                                        type="button"
                                    >
                                        {customer.name}
                                    </button>

                                    <span
                                        className="og3-data-table__metadata"
                                    >
                                        {customer.code}
                                    </span>
                                </td>

                                <td
                                    className="og3-data-table__optional"
                                    data-label="Tipo"
                                >
                                    {getCustomerTypeLabel(
                                        customer.customer_type,
                                    )}
                                </td>

                                <td
                                    className="og3-data-table__optional"
                                    data-label="Documento"
                                >
                                    {formatCustomerDocument(
                                        customer.document_number,
                                    )}
                                </td>

                                <td data-label="Contato">
                                    <span>
                                        {formatCustomerPhone(
                                            customer.phone,
                                        )}
                                    </span>

                                    {customer.email !== null && (
                                        <span
                                            className="og3-data-table__metadata"
                                        >
                                            {customer.email}
                                        </span>
                                    )}
                                </td>

                                <td data-label="Status">
                                    <Badge
                                        variant={
                                            customer.is_active
                                                ? "success"
                                                : "neutral"
                                        }
                                    >
                                        {customer.is_active
                                            ? "Ativo"
                                            : "Inativo"}
                                    </Badge>
                                </td>

                                <td
                                    className="og3-data-table__actions-cell"
                                    data-label="Ações"
                                >
                                    <div
                                        className="og3-data-table__actions"
                                    >
                                        <Button
                                            onClick={() => {
                                                onView(customer);
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
                                                    onEdit(customer);
                                                }}
                                                size="sm"
                                                variant="secondary"
                                            >
                                                Editar
                                            </Button>
                                        )}

                                        {customer.is_active &&
                                            canArchive && (
                                                <Button
                                                    disabled={isBusy}
                                                    onClick={() => {
                                                        onArchive(customer);
                                                    }}
                                                    size="sm"
                                                    variant="danger"
                                                >
                                                    Inativar
                                                </Button>
                                            )}

                                        {!customer.is_active &&
                                            canReactivate && (
                                                <Button
                                                    disabled={isBusy}
                                                    onClick={() => {
                                                        onReactivate(customer);
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