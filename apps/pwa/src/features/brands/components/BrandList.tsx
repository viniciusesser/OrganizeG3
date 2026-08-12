import type {
    Brand,
} from "@/features/brands/model/brand";
import {
    DataTable,
} from "@/shared/components/patterns";
import {
    Badge,
    Button,
} from "@/shared/components/ui";

export interface BrandListProps {
    readonly brands:
    readonly Brand[];
    readonly canEdit: boolean;
    readonly canDeactivate: boolean;
    readonly canReactivate: boolean;
    readonly busyBrandId?:
    string | null;
    readonly onView: (
        brand: Brand,
    ) => void;
    readonly onEdit: (
        brand: Brand,
    ) => void;
    readonly onDeactivate: (
        brand: Brand,
    ) => void;
    readonly onReactivate: (
        brand: Brand,
    ) => void;
}

export function BrandList({
    brands,
    canEdit,
    canDeactivate,
    canReactivate,
    busyBrandId = null,
    onView,
    onEdit,
    onDeactivate,
    onReactivate,
}: BrandListProps) {
    return (
        <DataTable>
                <thead>
                    <tr>
                        <th scope="col">
                            Marca
                        </th>

                        <th scope="col">
                            Código
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
                    {brands.map(
                        (brand) => {
                            const isBusy =
                                busyBrandId ===
                                brand.id;

                            return (
                                <tr key={brand.id}>
                                    <td data-label="Marca">
                                        <button
                                            className="og3-data-table__primary-link"
                                            onClick={() => {
                                                onView(
                                                    brand,
                                                );
                                            }}
                                            type="button"
                                        >
                                            {brand.name}
                                        </button>
                                    </td>

                                    <td data-label="Código">
                                        {brand.code}
                                    </td>

                                    <td data-label="Status">
                                        <Badge
                                            variant={
                                                brand.is_active
                                                    ? "success"
                                                    : "neutral"
                                            }
                                        >
                                            {brand.is_active
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
                                                    onView(
                                                        brand,
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
                                                            brand,
                                                        );
                                                    }}
                                                    size="sm"
                                                    variant="secondary"
                                                >
                                                    Editar
                                                </Button>
                                            )}

                                            {brand.is_active &&
                                                canDeactivate && (
                                                    <Button
                                                        disabled={
                                                            isBusy
                                                        }
                                                        onClick={() => {
                                                            onDeactivate(
                                                                brand,
                                                            );
                                                        }}
                                                        size="sm"
                                                        variant="danger"
                                                    >
                                                        Inativar
                                                    </Button>
                                                )}

                                            {!brand.is_active &&
                                                canReactivate && (
                                                    <Button
                                                        disabled={
                                                            isBusy
                                                        }
                                                        onClick={() => {
                                                            onReactivate(
                                                                brand,
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