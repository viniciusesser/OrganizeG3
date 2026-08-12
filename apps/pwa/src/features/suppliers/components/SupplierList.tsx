import type {
    Supplier,
} from "@/features/suppliers/model/supplier";
import {
    formatSupplierDocument,
    formatSupplierPhone,
} from "@/features/suppliers/model/supplier";
import {
    DataTable,
} from "@/shared/components/patterns";
import {
    Badge,
    Button,
} from "@/shared/components/ui";

export interface SupplierListProps {
    readonly suppliers: readonly Supplier[];
    readonly canEdit: boolean;
    readonly canDeactivate: boolean;
    readonly canReactivate: boolean;
    readonly busySupplierId?: string | null;
    readonly onView: (
        supplier: Supplier,
    ) => void;
    readonly onEdit: (
        supplier: Supplier,
    ) => void;
    readonly onDeactivate: (
        supplier: Supplier,
    ) => void;
    readonly onReactivate: (
        supplier: Supplier,
    ) => void;
}

export function SupplierList({
    suppliers,
    canEdit,
    canDeactivate,
    canReactivate,
    busySupplierId = null,
    onView,
    onEdit,
    onDeactivate,
    onReactivate,
}: SupplierListProps) {
    return (
        <DataTable>
            <thead>
                <tr>
                    <th scope="col">
                        Fornecedor
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

                    <th
                        className="og3-data-table__optional"
                        scope="col"
                    >
                        Localidade
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
                {suppliers.map(
                    (supplier) => {
                        const isBusy =
                            busySupplierId ===
                            supplier.id;

                        const locality = [
                            supplier.city,
                            supplier.state,
                        ]
                            .filter(
                                (
                                    value,
                                ): value is string =>
                                    value !== null &&
                                    value.trim()
                                        .length > 0,
                            )
                            .join(" - ");

                        return (
                            <tr key={supplier.id}>
                                <td data-label="Fornecedor">
                                    <button
                                        className="og3-data-table__primary-link"
                                        onClick={() => {
                                            onView(
                                                supplier,
                                            );
                                        }}
                                        type="button"
                                    >
                                        {supplier.name}
                                    </button>

                                    <span className="og3-data-table__metadata">
                                        {supplier.code}
                                        {supplier.trade_name !==
                                            null &&
                                            ` · ${supplier.trade_name}`}
                                    </span>
                                </td>

                                <td
                                    className="og3-data-table__optional"
                                    data-label="Documento"
                                >
                                    {formatSupplierDocument(
                                        supplier.document_number,
                                    )}
                                </td>

                                <td data-label="Contato">
                                    <span>
                                        {formatSupplierPhone(
                                            supplier.phone,
                                        )}
                                    </span>

                                    {supplier.email !==
                                        null && (
                                            <span className="og3-data-table__metadata">
                                                {supplier.email}
                                            </span>
                                        )}
                                </td>

                                <td
                                    className="og3-data-table__optional"
                                    data-label="Localidade"
                                >
                                    {locality.length > 0
                                        ? locality
                                        : "—"}
                                </td>

                                <td data-label="Status">
                                    <Badge
                                        variant={
                                            supplier.is_active
                                                ? "success"
                                                : "neutral"
                                        }
                                    >
                                        {supplier.is_active
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
                                                    supplier,
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
                                                        supplier,
                                                    );
                                                }}
                                                size="sm"
                                                variant="secondary"
                                            >
                                                Editar
                                            </Button>
                                        )}

                                        {supplier.is_active &&
                                            canDeactivate && (
                                                <Button
                                                    disabled={
                                                        isBusy
                                                    }
                                                    onClick={() => {
                                                        onDeactivate(
                                                            supplier,
                                                        );
                                                    }}
                                                    size="sm"
                                                    variant="danger"
                                                >
                                                    Inativar
                                                </Button>
                                            )}

                                        {!supplier.is_active &&
                                            canReactivate && (
                                                <Button
                                                    disabled={
                                                        isBusy
                                                    }
                                                    onClick={() => {
                                                        onReactivate(
                                                            supplier,
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