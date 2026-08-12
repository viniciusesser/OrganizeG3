import {
    useCallback,
    useEffect,
    useMemo,
    useRef,
    useState,
} from "react";
import type {
    FormEvent,
} from "react";

import {
    hasPermission,
} from "@/features/auth/model/currentIdentity";
import {
    useAuth,
} from "@/features/auth/session/useAuth";
import {
    listBrands,
} from "@/features/materials/api/brandsApi";
import {
    createMaterial,
    deactivateMaterial,
    listMaterialPage,
    reactivateMaterial,
    updateMaterial,
} from "@/features/materials/api/materialsApi";
import {
    MaterialDetails,
} from "@/features/materials/components/MaterialDetails";
import {
    MaterialForm,
} from "@/features/materials/components/MaterialForm";
import {
    MaterialList,
} from "@/features/materials/components/MaterialList";
import {
    createBrandMap,
} from "@/features/materials/model/brand";
import type {
    Brand,
} from "@/features/materials/model/brand";
import type {
    Material,
    MaterialCreateInput,
    MaterialPage,
} from "@/features/materials/model/material";
import {
    DEFAULT_MATERIAL_PAGE_SIZE,
} from "@/features/materials/model/material";
import {
    ApiError,
} from "@/infrastructure/api/apiError";
import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";
import {
    Checkbox,
    ConfirmationDialog,
    FilterBar,
    InlineMessage,
    PageHeader,
    Pagination,
    StatePanel,
} from "@/shared/components/patterns";
import {
    Button,
    Card,
    Input,
} from "@/shared/components/ui";

const EMPTY_PAGE: MaterialPage = {
    items: [],
    hasPrevious: false,
    hasNext: false,
    offset: 0,
    pageSize: DEFAULT_MATERIAL_PAGE_SIZE,
};

const BRAND_PAGE_SIZE = 200;

type MaterialDialog =
    | {
        readonly type: "create";
    }
    | {
        readonly type: "details";
        readonly material: Material;
    }
    | {
        readonly type: "edit";
        readonly material: Material;
    }
    | {
        readonly type: "deactivate";
        readonly material: Material;
    }
    | null;

interface MaterialFeedback {
    readonly message: string;
    readonly tone: "success" | "danger";
}

function getErrorMessage(
    error: unknown,
    fallback: string,
): string {
    if (error instanceof ApiError) {
        return error.message;
    }

    if (
        error instanceof Error &&
        error.message.trim().length > 0
    ) {
        return error.message;
    }

    return fallback;
}

export function MaterialsRoute() {
    const auth = useAuth();
    const identity = auth.identity;

    const canRead =
        identity !== null &&
        hasPermission(
            identity,
            "materials.read",
        );

    const canCreate =
        identity !== null &&
        hasPermission(
            identity,
            "materials.create",
        );

    const canEdit =
        identity !== null &&
        hasPermission(
            identity,
            "materials.update",
        );

    const canDeactivate =
        identity !== null &&
        hasPermission(
            identity,
            "materials.deactivate",
        );

    const canReactivate =
        identity !== null &&
        hasPermission(
            identity,
            "materials.reactivate",
        );

    const canReadBrands =
        identity !== null &&
        hasPermission(
            identity,
            "brands.read",
        );

    const apiContext =
        useMemo<AuthenticatedApiContext | null>(
            () => {
                if (
                    auth.session === null ||
                    auth.selectedTenant === null
                ) {
                    return null;
                }

                return {
                    accessToken:
                        auth.session.accessToken,
                    tenantId:
                        auth.selectedTenant.tenantId,
                };
            },
            [
                auth.selectedTenant,
                auth.session,
            ],
        );

    const [page, setPage] =
        useState<MaterialPage>(
            EMPTY_PAGE,
        );

    const [brands, setBrands] =
        useState<readonly Brand[]>([]);

    const brandById =
        useMemo(
            () => createBrandMap(brands),
            [brands],
        );

    const [searchDraft, setSearchDraft] =
        useState("");

    const [search, setSearch] =
        useState("");

    const [
        categoryDraft,
        setCategoryDraft,
    ] = useState("");

    const [category, setCategory] =
        useState("");

    const [brandId, setBrandId] =
        useState("");

    const [
        includeInactive,
        setIncludeInactive,
    ] = useState(false);

    const [offset, setOffset] =
        useState(0);

    const [isLoading, setIsLoading] =
        useState(false);

    const [
        isLoadingBrands,
        setIsLoadingBrands,
    ] = useState(false);

    const [loadError, setLoadError] =
        useState<string | null>(null);

    const [
        brandLoadError,
        setBrandLoadError,
    ] = useState<string | null>(null);

    const [dialog, setDialog] =
        useState<MaterialDialog>(null);

    const [
        isSubmitting,
        setIsSubmitting,
    ] = useState(false);

    const [
        submitError,
        setSubmitError,
    ] = useState<string | null>(null);

    const [feedback, setFeedback] =
        useState<MaterialFeedback | null>(
            null,
        );

    const [
        busyMaterialId,
        setBusyMaterialId,
    ] = useState<string | null>(null);

    const loadRevisionRef =
        useRef(0);

    const brandLoadRevisionRef =
        useRef(0);

    const loadMaterials =
        useCallback(
            async (): Promise<void> => {
                if (
                    !canRead ||
                    apiContext === null
                ) {
                    return;
                }

                const revision =
                    loadRevisionRef.current + 1;

                loadRevisionRef.current =
                    revision;

                setIsLoading(true);
                setLoadError(null);

                try {
                    const result =
                        await listMaterialPage(
                            apiContext,
                            {
                                includeInactive,
                                search,
                                category,
                                brandId:
                                    brandId.length > 0
                                        ? brandId
                                        : null,
                                limit:
                                    DEFAULT_MATERIAL_PAGE_SIZE,
                                offset,
                            },
                        );

                    if (
                        loadRevisionRef.current !==
                        revision
                    ) {
                        return;
                    }

                    setPage(result);
                } catch (error) {
                    if (
                        loadRevisionRef.current !==
                        revision
                    ) {
                        return;
                    }

                    setLoadError(
                        getErrorMessage(
                            error,
                            "Não foi possível carregar os materiais.",
                        ),
                    );
                } finally {
                    if (
                        loadRevisionRef.current ===
                        revision
                    ) {
                        setIsLoading(false);
                    }
                }
            },
            [
                apiContext,
                brandId,
                canRead,
                category,
                includeInactive,
                offset,
                search,
            ],
        );

    const loadBrands =
        useCallback(
            async (): Promise<void> => {
                if (
                    !canReadBrands ||
                    apiContext === null
                ) {
                    setBrands([]);
                    setBrandLoadError(null);
                    return;
                }

                const revision =
                    brandLoadRevisionRef.current + 1;

                brandLoadRevisionRef.current =
                    revision;

                setIsLoadingBrands(true);
                setBrandLoadError(null);

                try {
                    const loadedBrands: Brand[] = [];
                    let brandOffset = 0;
                    let hasNextPage = true;

                    while (hasNextPage) {
                        const currentItems =
                            await listBrands(
                                apiContext,
                                {
                                    includeInactive: true,
                                    limit:
                                        BRAND_PAGE_SIZE,
                                    offset:
                                        brandOffset,
                                },
                            );

                        if (
                            brandLoadRevisionRef.current !==
                            revision
                        ) {
                            return;
                        }

                        loadedBrands.push(
                            ...currentItems,
                        );

                        hasNextPage =
                            currentItems.length ===
                            BRAND_PAGE_SIZE;

                        brandOffset +=
                            currentItems.length;
                    }

                    setBrands(loadedBrands);
                } catch (error) {
                    if (
                        brandLoadRevisionRef.current !==
                        revision
                    ) {
                        return;
                    }

                    setBrands([]);

                    setBrandLoadError(
                        getErrorMessage(
                            error,
                            "Não foi possível carregar as marcas.",
                        ),
                    );
                } finally {
                    if (
                        brandLoadRevisionRef.current ===
                        revision
                    ) {
                        setIsLoadingBrands(false);
                    }
                }
            },
            [
                apiContext,
                canReadBrands,
            ],
        );

    useEffect(
        () => {
            const timeoutId =
                window.setTimeout(
                    () => {
                        void loadMaterials();
                    },
                    0,
                );

            return () => {
                window.clearTimeout(
                    timeoutId,
                );

                loadRevisionRef.current += 1;
            };
        },
        [loadMaterials],
    );

    useEffect(
        () => {
            const timeoutId =
                window.setTimeout(
                    () => {
                        void loadBrands();
                    },
                    0,
                );

            return () => {
                window.clearTimeout(
                    timeoutId,
                );

                brandLoadRevisionRef.current += 1;
            };
        },
        [loadBrands],
    );

    const closeDialog =
        useCallback(
            () => {
                if (isSubmitting) {
                    return;
                }

                setDialog(null);
                setSubmitError(null);
            },
            [isSubmitting],
        );

    const handleSearch = (
        event: FormEvent<HTMLFormElement>,
    ) => {
        event.preventDefault();

        setOffset(0);
        setSearch(
            searchDraft.trim(),
        );
        setCategory(
            categoryDraft.trim(),
        );
    };

    const clearFilters = () => {
        setSearchDraft("");
        setSearch("");
        setCategoryDraft("");
        setCategory("");
        setBrandId("");
        setIncludeInactive(false);
        setOffset(0);
    };

    const handleCreate = async (
        values: MaterialCreateInput,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setSubmitError(null);

        try {
            await createMaterial(
                apiContext,
                values,
            );

            setDialog(null);
            setFeedback({
                message:
                    "Material cadastrado com sucesso.",
                tone: "success",
            });

            if (offset === 0) {
                await loadMaterials();
            } else {
                setOffset(0);
            }
        } catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível cadastrar o material.",
                ),
            );
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleUpdate = async (
        material: Material,
        values: MaterialCreateInput,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setSubmitError(null);

        try {
            await updateMaterial(
                apiContext,
                material.id,
                values,
            );

            setDialog(null);

            setFeedback({
                message:
                    "Material atualizado com sucesso.",
                tone: "success",
            });

            await loadMaterials();
        } catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível atualizar o material.",
                ),
            );
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleDeactivate = async (
        material: Material,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setBusyMaterialId(
            material.id,
        );
        setSubmitError(null);

        try {
            await deactivateMaterial(
                apiContext,
                material.id,
            );

            setDialog(null);

            setFeedback({
                message:
                    "Material inativado com sucesso.",
                tone: "success",
            });

            await loadMaterials();
        } catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível inativar o material.",
                ),
            );
        } finally {
            setBusyMaterialId(null);
            setIsSubmitting(false);
        }
    };

    const handleReactivate = async (
        material: Material,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setBusyMaterialId(
            material.id,
        );
        setSubmitError(null);

        try {
            await reactivateMaterial(
                apiContext,
                material.id,
            );

            setDialog(null);

            setFeedback({
                message:
                    "Material reativado com sucesso.",
                tone: "success",
            });

            await loadMaterials();
        } catch (error) {
            setFeedback({
                message:
                    getErrorMessage(
                        error,
                        "Não foi possível reativar o material.",
                    ),
                tone: "danger",
            });
        } finally {
            setBusyMaterialId(null);
            setIsSubmitting(false);
        }
    };

    const hasFilters =
        search.length > 0 ||
        category.length > 0 ||
        brandId.length > 0 ||
        includeInactive;

    const currentPage =
        Math.floor(
            page.offset /
            page.pageSize,
        ) + 1;

    return (
        <div className="og3-page-layout">
            <PageHeader
                actions={
                    canCreate ? (
                        <Button
                            onClick={() => {
                                setSubmitError(null);
                                setDialog({
                                    type: "create",
                                });
                            }}
                        >
                            Novo material
                        </Button>
                    ) : undefined
                }
                badge="Catálogo"
                description="Gerencie materiais, categorias, unidades e vínculos com marcas por empresa."
                title="Materiais"
            />

            {!canRead ? (
                <Card>
                    <StatePanel
                        description="Você não possui permissão para visualizar materiais."
                        heading="Acesso restrito"
                    />
                </Card>
            ) : apiContext === null ? (
                <Card>
                    <StatePanel
                        description="Não foi possível identificar a sessão e a empresa ativa."
                        heading="Contexto indisponível"
                        role="alert"
                    />
                </Card>
            ) : (
                <>
                    <Card>
                        <FilterBar
                            actions={
                                <>
                                    <Button type="submit">
                                        Pesquisar
                                    </Button>

                                    {hasFilters && (
                                        <Button
                                            onClick={
                                                clearFilters
                                            }
                                            type="button"
                                            variant="secondary"
                                        >
                                            Limpar filtros
                                        </Button>
                                    )}

                                </>
                            }
                            onSubmit={handleSearch}
                        >
                            <div className="og3-filter-bar__search">
                                <Input
                                    label="Pesquisar materiais"
                                    onChange={(event) => {
                                        setSearchDraft(
                                            event.target.value,
                                        );
                                    }}
                                    placeholder="Código ou nome"
                                    type="search"
                                    value={searchDraft}
                                />
                            </div>

                            <Input
                                label="Categoria"
                                onChange={(event) => {
                                    setCategoryDraft(
                                        event.target.value,
                                    );
                                }}
                                placeholder="Ex.: MDF ou ferragem"
                                value={categoryDraft}
                            />

                            {canReadBrands && (
                                <div className="og3-field">
                                    <label
                                        className="og3-field__label"
                                        htmlFor="material-brand-filter"
                                    >
                                        Marca
                                    </label>

                                    <select
                                        className="og3-field__input"
                                        disabled={
                                            isLoadingBrands
                                        }
                                        id="material-brand-filter"
                                        onChange={(event) => {
                                            setBrandId(
                                                event.target.value,
                                            );
                                            setOffset(0);
                                        }}
                                        value={brandId}
                                    >
                                        <option value="">
                                            Todas as marcas
                                        </option>

                                        {brands.map(
                                            (brand) => (
                                                <option
                                                    key={brand.id}
                                                    value={brand.id}
                                                >
                                                    {brand.code}
                                                    {" — "}
                                                    {brand.name}
                                                    {!brand.is_active &&
                                                        " — Inativa"}
                                                </option>
                                            ),
                                        )}
                                    </select>
                                </div>
                            )}

                            <Checkbox
                                checked={
                                    includeInactive
                                }
                                onChange={(event) => {
                                    setIncludeInactive(
                                        event.target.checked,
                                    );
                                    setOffset(0);
                                }}
                                label="Exibir inativos"
                            />
                        </FilterBar>
                    </Card>

                    {brandLoadError !== null && (
                        <InlineMessage tone="danger">
                            <span>
                                {brandLoadError}
                            </span>

                            <Button
                                onClick={() => {
                                    void loadBrands();
                                }}
                                size="sm"
                                type="button"
                                variant="secondary"
                            >
                                Tentar carregar marcas novamente
                            </Button>
                        </InlineMessage>
                    )}

                    {feedback !== null && (
                        <InlineMessage tone={feedback.tone}>
                            {feedback.message}
                        </InlineMessage>
                    )}

                    <Card>
                        {isLoading &&
                            page.items.length === 0 ? (
                            <StatePanel
                                aria-live="polite"
                                description="Aguarde enquanto os dados são consultados."
                                heading="Carregando materiais"
                            />
                        ) : loadError !== null ? (
                            <StatePanel
                                actions={
                                    <Button
                                        onClick={() => {
                                            void loadMaterials();
                                        }}
                                        variant="secondary"
                                    >
                                        Tentar novamente
                                    </Button>
                                }
                                description={loadError}
                                heading="Não foi possível carregar os materiais"
                                role="alert"
                            />
                        ) : page.items.length === 0 ? (
                            <StatePanel
                                actions={
                                    hasFilters ? (
                                        <Button
                                            onClick={clearFilters}
                                            variant="secondary"
                                        >
                                            Limpar filtros
                                        </Button>
                                    ) : canCreate ? (
                                        <Button
                                            onClick={() => {
                                                setSubmitError(null);
                                                setDialog({
                                                    type: "create",
                                                });
                                            }}
                                        >
                                            Novo material
                                        </Button>
                                    ) : undefined
                                }
                                description={
                                    hasFilters
                                        ? "Revise a pesquisa ou limpe os filtros."
                                        : "Cadastre o primeiro material da empresa."
                                }
                                heading={
                                    hasFilters
                                        ? "Nenhum material encontrado"
                                        : "Nenhum material cadastrado"
                                }
                            />
                        ) : (
                            <>
                                {isLoading && (
                                    <div
                                        className="og3-data-table__loading"
                                        role="status"
                                    >
                                        Atualizando materiais...
                                    </div>
                                )}

                                <MaterialList
                                    brandById={brandById}
                                    busyMaterialId={
                                        busyMaterialId
                                    }
                                    canDeactivate={
                                        canDeactivate
                                    }
                                    canEdit={canEdit}
                                    canReactivate={
                                        canReactivate
                                    }
                                    materials={page.items}
                                    onDeactivate={(
                                        material,
                                    ) => {
                                        setSubmitError(null);

                                        setDialog({
                                            type: "deactivate",
                                            material,
                                        });
                                    }}
                                    onEdit={(material) => {
                                        setSubmitError(null);

                                        setDialog({
                                            type: "edit",
                                            material,
                                        });
                                    }}
                                    onReactivate={(
                                        material,
                                    ) => {
                                        void handleReactivate(
                                            material,
                                        );
                                    }}
                                    onView={(material) => {
                                        setDialog({
                                            type: "details",
                                            material,
                                        });
                                    }}
                                />

                                <Pagination
                                    aria-label="Paginação de materiais"
                                    currentPage={currentPage}
                                    hasNext={page.hasNext}
                                    hasPrevious={page.hasPrevious}
                                    isLoading={isLoading}
                                    onNext={() => {
                                        setOffset(
                                            page.offset +
                                            page.pageSize,
                                        );
                                    }}
                                    onPrevious={() => {
                                        setOffset(
                                            Math.max(
                                                0,
                                                page.offset -
                                                page.pageSize,
                                            ),
                                        );
                                    }}
                                />
                            </>
                        )}
                    </Card>
                </>
            )}

            {dialog?.type === "create" && (
                <MaterialForm
                    brands={brands}
                    canReadBrands={canReadBrands}
                    isLoadingBrands={
                        isLoadingBrands
                    }
                    isSubmitting={isSubmitting}
                    onCancel={closeDialog}
                    onSubmit={handleCreate}
                    submitError={submitError}
                />
            )}

            {dialog?.type === "edit" && (
                <MaterialForm
                    brands={brands}
                    canReadBrands={canReadBrands}
                    isLoadingBrands={
                        isLoadingBrands
                    }
                    isSubmitting={isSubmitting}
                    material={dialog.material}
                    onCancel={closeDialog}
                    onSubmit={(values) =>
                        handleUpdate(
                            dialog.material,
                            values,
                        )
                    }
                    submitError={submitError}
                />
            )}

            {dialog?.type === "details" && (
                <MaterialDetails
                    brand={
                        dialog.material.brand_id !==
                            null
                            ? brandById.get(
                                dialog.material.brand_id,
                            )
                            : undefined
                    }
                    canDeactivate={canDeactivate}
                    canEdit={canEdit}
                    canReactivate={canReactivate}
                    isSubmitting={isSubmitting}
                    material={dialog.material}
                    onClose={closeDialog}
                    onDeactivate={(material) => {
                        setSubmitError(null);

                        setDialog({
                            type: "deactivate",
                            material,
                        });
                    }}
                    onEdit={(material) => {
                        setSubmitError(null);

                        setDialog({
                            type: "edit",
                            material,
                        });
                    }}
                    onReactivate={(material) => {
                        void handleReactivate(
                            material,
                        );
                    }}
                />
            )}

            {dialog?.type ===
                "deactivate" && (
                    <ConfirmationDialog
                        confirmLabel="Inativar material"
                        description={
                            <>
                                Material{" "}
                                {dialog.material.name}{" "}
                                ficará inativo e poderá ser reativado depois.
                            </>
                        }
                        errorMessage={submitError}
                        isSubmitting={isSubmitting}
                        onCancel={closeDialog}
                        onConfirm={() => {
                            void handleDeactivate(
                                dialog.material,
                            );
                        }}
                        pendingLabel="Inativando..."
                        title="Inativar material?"
                        titleId="deactivate-material-title"
                    />
                )}
        </div>
    );
}