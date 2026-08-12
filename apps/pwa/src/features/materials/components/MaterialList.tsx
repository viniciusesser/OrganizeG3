import type {
    Brand,
} from "@/features/materials/model/brand";
import {
    formatBrandOption,
} from "@/features/materials/model/brand";
import type {
    Material,
} from "@/features/materials/model/material";
import {
    DataTable,
} from "@/shared/components/patterns";
import {
    Badge,
    Button,
} from "@/shared/components/ui";

export interface MaterialListProps {
    readonly materials: readonly Material[];
    readonly brandById: ReadonlyMap<
        string,
        Brand
    >;
    readonly canEdit: boolean;
    readonly canDeactivate: boolean;
    readonly canReactivate: boolean;
    readonly busyMaterialId?: string | null;
    readonly onView: (
        material: Material,
    ) => void;
    readonly onEdit: (
        material: Material,
    ) => void;
    readonly onDeactivate: (
        material: Material,
    ) => void;
    readonly onReactivate: (
        material: Material,
    ) => void;
}

function formatMaterialBrand(
    material: Material,
    brandById: ReadonlyMap<
        string,
        Brand
    >,
): string {
    if (material.brand_id === null) {
        return "—";
    }

    const brand =
        brandById.get(material.brand_id);

    if (brand === undefined) {
        return "Marca indisponível";
    }

    return formatBrandOption(brand);
}

export function MaterialList({
    materials,
    brandById,
    canEdit,
    canDeactivate,
    canReactivate,
    busyMaterialId = null,
    onView,
    onEdit,
    onDeactivate,
    onReactivate,
}: MaterialListProps) {
    return (
        <DataTable>
            <thead>
                <tr>
                    <th scope="col">
                        Material
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
                        Marca
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
                {materials.map(
                    (material) => {
                        const isBusy =
                            busyMaterialId ===
                            material.id;

                        return (
                            <tr key={material.id}>
                                <td data-label="Material">
                                    <button
                                        className="og3-data-table__primary-link"
                                        onClick={() => {
                                            onView(
                                                material,
                                            );
                                        }}
                                        type="button"
                                    >
                                        {material.name}
                                    </button>

                                    <span className="og3-data-table__metadata">
                                        {material.code}
                                    </span>
                                </td>

                                <td data-label="Categoria">
                                    {material.category}
                                </td>

                                <td
                                    className="og3-data-table__optional"
                                    data-label="Unidade"
                                >
                                    {material.unit}
                                </td>

                                <td
                                    className="og3-data-table__optional"
                                    data-label="Marca"
                                >
                                    {formatMaterialBrand(
                                        material,
                                        brandById,
                                    )}
                                </td>

                                <td data-label="Status">
                                    <Badge
                                        variant={
                                            material.is_active
                                                ? "success"
                                                : "neutral"
                                        }
                                    >
                                        {material.is_active
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
                                                    material,
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
                                                        material,
                                                    );
                                                }}
                                                size="sm"
                                                variant="secondary"
                                            >
                                                Editar
                                            </Button>
                                        )}

                                        {material.is_active &&
                                            canDeactivate && (
                                                <Button
                                                    disabled={
                                                        isBusy
                                                    }
                                                    onClick={() => {
                                                        onDeactivate(
                                                            material,
                                                        );
                                                    }}
                                                    size="sm"
                                                    variant="danger"
                                                >
                                                    Inativar
                                                </Button>
                                            )}

                                        {!material.is_active &&
                                            canReactivate && (
                                                <Button
                                                    disabled={
                                                        isBusy
                                                    }
                                                    onClick={() => {
                                                        onReactivate(
                                                            material,
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