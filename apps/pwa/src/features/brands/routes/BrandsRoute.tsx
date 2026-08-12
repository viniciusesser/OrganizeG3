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
    createBrand,
    deactivateBrand,
    listBrandPage,
    reactivateBrand,
    updateBrand,
} from "@/features/brands/api/brandsApi";
import {
    BrandDetails,
} from "@/features/brands/components/BrandDetails";
import {
    BrandForm,
} from "@/features/brands/components/BrandForm";
import {
    BrandList,
} from "@/features/brands/components/BrandList";
import type {
    Brand,
    BrandCreateInput,
    BrandPage,
} from "@/features/brands/model/brand";
import {
    DEFAULT_BRAND_PAGE_SIZE,
} from "@/features/brands/model/brand";
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

const EMPTY_PAGE: BrandPage = {
    items: [],
    hasPrevious: false,
    hasNext: false,
    offset: 0,
    pageSize:
        DEFAULT_BRAND_PAGE_SIZE,
};

type BrandDialog =
    | {
        readonly type:
        "create";
    }
    | {
        readonly type:
        "details";
        readonly brand:
        Brand;
    }
    | {
        readonly type:
        "edit";
        readonly brand:
        Brand;
    }
    | {
        readonly type:
        "deactivate";
        readonly brand:
        Brand;
    }
    | null;

interface BrandFeedback {
    readonly message:
    string;
    readonly tone:
    "success" | "danger";
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

export function BrandsRoute() {
    const auth =
        useAuth();

    const identity =
        auth.identity;

    const canRead =
        identity !== null &&
        hasPermission(
            identity,
            "brands.read",
        );

    const canCreate =
        identity !== null &&
        hasPermission(
            identity,
            "brands.create",
        );

    const canEdit =
        identity !== null &&
        hasPermission(
            identity,
            "brands.update",
        );

    const canDeactivate =
        identity !== null &&
        hasPermission(
            identity,
            "brands.deactivate",
        );

    const canReactivate =
        identity !== null &&
        hasPermission(
            identity,
            "brands.reactivate",
        );

    const apiContext =
        useMemo<
            AuthenticatedApiContext | null
        >(
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
        useState<BrandPage>(
            EMPTY_PAGE,
        );

    const [
        searchDraft,
        setSearchDraft,
    ] = useState("");

    const [search, setSearch] =
        useState("");

    const [
        includeInactive,
        setIncludeInactive,
    ] = useState(false);

    const [offset, setOffset] =
        useState(0);

    const [
        isLoading,
        setIsLoading,
    ] = useState(false);

    const [
        loadError,
        setLoadError,
    ] = useState<
        string | null
    >(null);

    const [dialog, setDialog] =
        useState<BrandDialog>(
            null,
        );

    const [
        isSubmitting,
        setIsSubmitting,
    ] = useState(false);

    const [
        submitError,
        setSubmitError,
    ] = useState<
        string | null
    >(null);

    const [
        feedback,
        setFeedback,
    ] = useState<
        BrandFeedback | null
    >(null);

    const [
        busyBrandId,
        setBusyBrandId,
    ] = useState<
        string | null
    >(null);

    const loadRevisionRef =
        useRef(0);

    const loadBrands =
        useCallback(
            async (): Promise<void> => {
                if (
                    !canRead ||
                    apiContext === null
                ) {
                    return;
                }

                const revision =
                    loadRevisionRef.current +
                    1;

                loadRevisionRef.current =
                    revision;

                setIsLoading(true);
                setLoadError(null);

                try {
                    const result =
                        await listBrandPage(
                            apiContext,
                            {
                                includeInactive,
                                search,
                                limit:
                                    DEFAULT_BRAND_PAGE_SIZE,
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
                            "Não foi possível carregar as marcas.",
                        ),
                    );
                } finally {
                    if (
                        loadRevisionRef.current ===
                        revision
                    ) {
                        setIsLoading(
                            false,
                        );
                    }
                }
            },
            [
                apiContext,
                canRead,
                includeInactive,
                offset,
                search,
            ],
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

                loadRevisionRef.current +=
                    1;
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
        event:
            FormEvent<HTMLFormElement>,
    ): void => {
        event.preventDefault();

        setOffset(0);
        setSearch(
            searchDraft.trim(),
        );
    };

    const clearFilters =
        (): void => {
            setSearchDraft("");
            setSearch("");
            setIncludeInactive(
                false,
            );
            setOffset(0);
        };

    const handleCreate =
        async (
            values:
                BrandCreateInput,
        ): Promise<void> => {
            if (
                apiContext === null
            ) {
                return;
            }

            setIsSubmitting(true);
            setSubmitError(null);

            try {
                await createBrand(
                    apiContext,
                    values,
                );

                setDialog(null);

                setFeedback({
                    message:
                        "Marca cadastrada com sucesso.",
                    tone:
                        "success",
                });

                if (offset === 0) {
                    await loadBrands();
                } else {
                    setOffset(0);
                }
            } catch (error) {
                setSubmitError(
                    getErrorMessage(
                        error,
                        "Não foi possível cadastrar a marca.",
                    ),
                );
            } finally {
                setIsSubmitting(
                    false,
                );
            }
        };

    const handleUpdate =
        async (
            brand:
                Brand,
            values:
                BrandCreateInput,
        ): Promise<void> => {
            if (
                apiContext === null
            ) {
                return;
            }

            setIsSubmitting(true);
            setSubmitError(null);

            try {
                await updateBrand(
                    apiContext,
                    brand.id,
                    values,
                );

                setDialog(null);

                setFeedback({
                    message:
                        "Marca atualizada com sucesso.",
                    tone:
                        "success",
                });

                await loadBrands();
            } catch (error) {
                setSubmitError(
                    getErrorMessage(
                        error,
                        "Não foi possível atualizar a marca.",
                    ),
                );
            } finally {
                setIsSubmitting(
                    false,
                );
            }
        };

    const handleDeactivate =
        async (
            brand:
                Brand,
        ): Promise<void> => {
            if (
                apiContext === null
            ) {
                return;
            }

            setIsSubmitting(true);
            setBusyBrandId(
                brand.id,
            );
            setSubmitError(null);

            try {
                await deactivateBrand(
                    apiContext,
                    brand.id,
                );

                setDialog(null);

                setFeedback({
                    message:
                        "Marca inativada com sucesso.",
                    tone:
                        "success",
                });

                await loadBrands();
            } catch (error) {
                setSubmitError(
                    getErrorMessage(
                        error,
                        "Não foi possível inativar a marca.",
                    ),
                );
            } finally {
                setBusyBrandId(
                    null,
                );
                setIsSubmitting(
                    false,
                );
            }
        };

    const handleReactivate =
        async (
            brand:
                Brand,
        ): Promise<void> => {
            if (
                apiContext === null
            ) {
                return;
            }

            setIsSubmitting(true);
            setBusyBrandId(
                brand.id,
            );
            setSubmitError(null);

            try {
                await reactivateBrand(
                    apiContext,
                    brand.id,
                );

                setDialog(null);

                setFeedback({
                    message:
                        "Marca reativada com sucesso.",
                    tone:
                        "success",
                });

                await loadBrands();
            } catch (error) {
                setFeedback({
                    message:
                        getErrorMessage(
                            error,
                            "Não foi possível reativar a marca.",
                        ),
                    tone:
                        "danger",
                });
            } finally {
                setBusyBrandId(
                    null,
                );
                setIsSubmitting(
                    false,
                );
            }
        };

    const hasFilters =
        search.length > 0 ||
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
                            Nova marca
                        </Button>
                    ) : undefined
                }
                badge="Cadastro"
                description="Gerencie as marcas utilizadas nos materiais, produtos, equipamentos e demais cadastros da empresa."
                title="Marcas"
            />

            {!canRead ? (
                <Card>
                    <StatePanel
                        description="Você não possui permissão para visualizar marcas."
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
                                            onClick={clearFilters}
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
                                    label="Pesquisar marcas"
                                    onChange={(
                                        event,
                                    ) => {
                                        setSearchDraft(
                                            event
                                                .target
                                                .value,
                                        );
                                    }}
                                    placeholder="Código ou nome"
                                    type="search"
                                    value={
                                        searchDraft
                                    }
                                />
                            </div>

                            <Checkbox
                                checked={includeInactive}
                                label="Exibir inativas"
                                onChange={(event) => {
                                    setIncludeInactive(
                                        event.target.checked,
                                    );
                                    setOffset(0);
                                }}
                            />
                        </FilterBar>
                    </Card>

                    {feedback !== null && (
                        <InlineMessage
                            tone={feedback.tone}
                        >
                            {feedback.message}
                        </InlineMessage>
                    )}

                    <Card>
                        {isLoading &&
                            page.items.length ===
                            0 ? (
                            <StatePanel
                                aria-live="polite"
                                description="Aguarde enquanto os dados são consultados."
                                heading="Carregando marcas"
                            />
                        ) : loadError !==
                            null ? (
                            <StatePanel
                                actions={
                                    <Button
                                        onClick={() => {
                                            void loadBrands();
                                        }}
                                        variant="secondary"
                                    >
                                        Tentar novamente
                                    </Button>
                                }
                                description={loadError}
                                heading="Não foi possível carregar as marcas"
                                role="alert"
                            />
                        ) : page.items
                            .length ===
                            0 ? (
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
                                            setSubmitError(
                                                null,
                                            );

                                            setDialog({
                                                type:
                                                    "create",
                                            });
                                        }}
                                    >
                                        Nova marca
                                    </Button>
                                    ) : undefined
                                }
                                description={
                                    hasFilters
                                        ? "Revise a pesquisa ou limpe os filtros."
                                        : "Cadastre a primeira marca da empresa."
                                }
                                heading={
                                    hasFilters
                                        ? "Nenhuma marca encontrada"
                                        : "Nenhuma marca cadastrada"
                                }
                            />
                        ) : (
                            <>
                                {isLoading && (
                                    <div
                                        className="og3-data-table__loading"
                                        role="status"
                                    >
                                        Atualizando
                                        marcas...
                                    </div>
                                )}

                                <BrandList
                                    brands={
                                        page.items
                                    }
                                    busyBrandId={
                                        busyBrandId
                                    }
                                    canDeactivate={
                                        canDeactivate
                                    }
                                    canEdit={
                                        canEdit
                                    }
                                    canReactivate={
                                        canReactivate
                                    }
                                    onDeactivate={(
                                        brand,
                                    ) => {
                                        setSubmitError(
                                            null,
                                        );

                                        setDialog({
                                            type:
                                                "deactivate",
                                            brand,
                                        });
                                    }}
                                    onEdit={(
                                        brand,
                                    ) => {
                                        setSubmitError(
                                            null,
                                        );

                                        setDialog({
                                            type:
                                                "edit",
                                            brand,
                                        });
                                    }}
                                    onReactivate={(
                                        brand,
                                    ) => {
                                        void handleReactivate(
                                            brand,
                                        );
                                    }}
                                    onView={(
                                        brand,
                                    ) => {
                                        setDialog({
                                            type:
                                                "details",
                                            brand,
                                        });
                                    }}
                                />

                                <Pagination
                                    aria-label="Paginação de marcas"
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

            {dialog?.type ===
                "create" && (
                    <BrandForm
                        isSubmitting={
                            isSubmitting
                        }
                        onCancel={
                            closeDialog
                        }
                        onSubmit={
                            handleCreate
                        }
                        submitError={
                            submitError
                        }
                    />
                )}

            {dialog?.type ===
                "edit" && (
                    <BrandForm
                        brand={
                            dialog.brand
                        }
                        isSubmitting={
                            isSubmitting
                        }
                        onCancel={
                            closeDialog
                        }
                        onSubmit={(
                            values,
                        ) =>
                            handleUpdate(
                                dialog.brand,
                                values,
                            )
                        }
                        submitError={
                            submitError
                        }
                    />
                )}

            {dialog?.type ===
                "details" && (
                    <BrandDetails
                        brand={
                            dialog.brand
                        }
                        canDeactivate={
                            canDeactivate
                        }
                        canEdit={
                            canEdit
                        }
                        canReactivate={
                            canReactivate
                        }
                        isSubmitting={
                            isSubmitting
                        }
                        onClose={
                            closeDialog
                        }
                        onDeactivate={(
                            brand,
                        ) => {
                            setSubmitError(
                                null,
                            );

                            setDialog({
                                type:
                                    "deactivate",
                                brand,
                            });
                        }}
                        onEdit={(
                            brand,
                        ) => {
                            setSubmitError(
                                null,
                            );

                            setDialog({
                                type:
                                    "edit",
                                brand,
                            });
                        }}
                        onReactivate={(
                            brand,
                        ) => {
                            void handleReactivate(
                                brand,
                            );
                        }}
                    />
                )}

            {dialog?.type ===
                "deactivate" && (
                    <ConfirmationDialog
                        confirmLabel="Inativar marca"
                        description={
                            <>
                                A marca {dialog.brand.name}{" "}
                                ficará inativa e poderá ser
                                reativada depois.
                            </>
                        }
                        errorMessage={submitError}
                        isSubmitting={isSubmitting}
                        onCancel={closeDialog}
                        onConfirm={() => {
                            void handleDeactivate(
                                dialog.brand,
                            );
                        }}
                        pendingLabel="Inativando..."
                        title="Inativar marca?"
                        titleId="deactivate-brand-title"
                    />
                )}
        </div>
    );
}