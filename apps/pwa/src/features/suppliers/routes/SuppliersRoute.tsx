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
    createSupplier,
    deactivateSupplier,
    listSupplierPage,
    reactivateSupplier,
    updateSupplier,
} from "@/features/suppliers/api/suppliersApi";
import {
    SupplierDetails,
} from "@/features/suppliers/components/SupplierDetails";
import {
    SupplierForm,
} from "@/features/suppliers/components/SupplierForm";
import {
    SupplierList,
} from "@/features/suppliers/components/SupplierList";
import type {
    Supplier,
    SupplierCreateInput,
    SupplierPage,
} from "@/features/suppliers/model/supplier";
import {
    DEFAULT_SUPPLIER_PAGE_SIZE,
} from "@/features/suppliers/model/supplier";
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

const EMPTY_PAGE: SupplierPage = {
    items: [],
    hasPrevious: false,
    hasNext: false,
    offset: 0,
    pageSize: DEFAULT_SUPPLIER_PAGE_SIZE,
};

type SupplierDialog =
    | {
        readonly type: "create";
    }
    | {
        readonly type: "details";
        readonly supplier: Supplier;
    }
    | {
        readonly type: "edit";
        readonly supplier: Supplier;
    }
    | {
        readonly type: "deactivate";
        readonly supplier: Supplier;
    }
    | null;

interface SupplierFeedback {
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

export function SuppliersRoute() {
    const auth = useAuth();
    const identity = auth.identity;

    const canRead =
        identity !== null &&
        hasPermission(
            identity,
            "suppliers.read",
        );

    const canCreate =
        identity !== null &&
        hasPermission(
            identity,
            "suppliers.create",
        );

    const canEdit =
        identity !== null &&
        hasPermission(
            identity,
            "suppliers.update",
        );

    const canDeactivate =
        identity !== null &&
        hasPermission(
            identity,
            "suppliers.deactivate",
        );

    const canReactivate =
        identity !== null &&
        hasPermission(
            identity,
            "suppliers.reactivate",
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
        useState<SupplierPage>(
            EMPTY_PAGE,
        );

    const [searchDraft, setSearchDraft] =
        useState("");

    const [search, setSearch] =
        useState("");

    const [
        includeInactive,
        setIncludeInactive,
    ] = useState(false);

    const [offset, setOffset] =
        useState(0);

    const [isLoading, setIsLoading] =
        useState(false);

    const [loadError, setLoadError] =
        useState<string | null>(null);

    const [dialog, setDialog] =
        useState<SupplierDialog>(null);

    const [
        isSubmitting,
        setIsSubmitting,
    ] = useState(false);

    const [
        submitError,
        setSubmitError,
    ] = useState<string | null>(null);

    const [feedback, setFeedback] =
        useState<SupplierFeedback | null>(
            null,
        );

    const [
        busySupplierId,
        setBusySupplierId,
    ] = useState<string | null>(null);

    const loadRevisionRef =
        useRef(0);

    const loadSuppliers =
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
                        await listSupplierPage(
                            apiContext,
                            {
                                includeInactive,
                                search,
                                limit:
                                    DEFAULT_SUPPLIER_PAGE_SIZE,
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
                            "Não foi possível carregar os fornecedores.",
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
                        void loadSuppliers();
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
        [loadSuppliers],
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
    };

    const clearFilters = () => {
        setSearchDraft("");
        setSearch("");
        setIncludeInactive(false);
        setOffset(0);
    };

    const handleCreate = async (
        values: SupplierCreateInput,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setSubmitError(null);

        try {
            await createSupplier(
                apiContext,
                values,
            );

            setDialog(null);
            setOffset(0);

            setFeedback({
                message:
                    "Fornecedor cadastrado com sucesso.",
                tone: "success",
            });

            await loadSuppliers();
        } catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível cadastrar o fornecedor.",
                ),
            );
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleUpdate = async (
        supplier: Supplier,
        values: SupplierCreateInput,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setSubmitError(null);

        try {
            await updateSupplier(
                apiContext,
                supplier.id,
                values,
            );

            setDialog(null);

            setFeedback({
                message:
                    "Fornecedor atualizado com sucesso.",
                tone: "success",
            });

            await loadSuppliers();
        } catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível atualizar o fornecedor.",
                ),
            );
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleDeactivate = async (
        supplier: Supplier,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setBusySupplierId(
            supplier.id,
        );
        setSubmitError(null);

        try {
            await deactivateSupplier(
                apiContext,
                supplier.id,
            );

            setDialog(null);

            setFeedback({
                message:
                    "Fornecedor inativado com sucesso.",
                tone: "success",
            });

            await loadSuppliers();
        } catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível inativar o fornecedor.",
                ),
            );
        } finally {
            setBusySupplierId(null);
            setIsSubmitting(false);
        }
    };

    const handleReactivate = async (
        supplier: Supplier,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setBusySupplierId(
            supplier.id,
        );
        setSubmitError(null);

        try {
            await reactivateSupplier(
                apiContext,
                supplier.id,
            );

            setDialog(null);

            setFeedback({
                message:
                    "Fornecedor reativado com sucesso.",
                tone: "success",
            });

            await loadSuppliers();
        } catch (error) {
            setFeedback({
                message:
                    getErrorMessage(
                        error,
                        "Não foi possível reativar o fornecedor.",
                    ),
                tone: "danger",
            });
        } finally {
            setBusySupplierId(null);
            setIsSubmitting(false);
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
                            Novo fornecedor
                        </Button>
                    ) : undefined
                }
                badge="Cadastro"
                description="Gerencie os fornecedores, contatos, documentos e endereços da empresa."
                title="Fornecedores"
            />

            {!canRead ? (
                <Card>
                    <StatePanel
                        description="Você não possui permissão para visualizar fornecedores."
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
                                    label="Pesquisar fornecedores"
                                    onChange={(
                                        event,
                                    ) => {
                                        setSearchDraft(
                                            event
                                                .target
                                                .value,
                                        );
                                    }}
                                    placeholder="Código, nome, documento, email ou telefone"
                                    type="search"
                                    value={
                                        searchDraft
                                    }
                                />
                            </div>

                            <Checkbox
                                checked={
                                    includeInactive
                                }
                                onChange={(
                                    event,
                                ) => {
                                    setIncludeInactive(
                                        event
                                            .target
                                            .checked,
                                    );

                                    setOffset(
                                        0,
                                    );
                                }}
                                label="Exibir inativos"
                            />
                        </FilterBar>
                    </Card>

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
                                heading="Carregando fornecedores"
                            />
                        ) : loadError !== null ? (
                            <StatePanel
                                actions={
                                    <Button
                                        onClick={() => {
                                            void loadSuppliers();
                                        }}
                                        variant="secondary"
                                    >
                                        Tentar novamente
                                    </Button>
                                }
                                description={loadError}
                                heading="Não foi possível carregar os fornecedores"
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
                                            Novo fornecedor
                                        </Button>
                                    ) : undefined
                                }
                                description={
                                    hasFilters
                                        ? "Revise a pesquisa ou limpe os filtros."
                                        : "Cadastre o primeiro fornecedor da empresa."
                                }
                                heading={
                                    hasFilters
                                        ? "Nenhum fornecedor encontrado"
                                        : "Nenhum fornecedor cadastrado"
                                }
                            />
                        ) : (
                            <>
                                {isLoading && (
                                    <div
                                        className="og3-data-table__loading"
                                        role="status"
                                    >
                                        Atualizando fornecedores...
                                    </div>
                                )}

                                <SupplierList
                                    busySupplierId={
                                        busySupplierId
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
                                        supplier,
                                    ) => {
                                        setSubmitError(
                                            null,
                                        );

                                        setDialog({
                                            type: "deactivate",
                                            supplier,
                                        });
                                    }}
                                    onEdit={(
                                        supplier,
                                    ) => {
                                        setSubmitError(
                                            null,
                                        );

                                        setDialog({
                                            type: "edit",
                                            supplier,
                                        });
                                    }}
                                    onReactivate={(
                                        supplier,
                                    ) => {
                                        void handleReactivate(
                                            supplier,
                                        );
                                    }}
                                    onView={(
                                        supplier,
                                    ) => {
                                        setDialog({
                                            type: "details",
                                            supplier,
                                        });
                                    }}
                                    suppliers={
                                        page.items
                                    }
                                />

                                <Pagination
                                    aria-label="Paginação de fornecedores"
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
                    <SupplierForm
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
                    <SupplierForm
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
                                dialog.supplier,
                                values,
                            )
                        }
                        submitError={
                            submitError
                        }
                        supplier={
                            dialog.supplier
                        }
                    />
                )}

            {dialog?.type ===
                "details" && (
                    <SupplierDetails
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
                            supplier,
                        ) => {
                            setSubmitError(
                                null,
                            );

                            setDialog({
                                type: "deactivate",
                                supplier,
                            });
                        }}
                        onEdit={(
                            supplier,
                        ) => {
                            setSubmitError(
                                null,
                            );

                            setDialog({
                                type: "edit",
                                supplier,
                            });
                        }}
                        onReactivate={(
                            supplier,
                        ) => {
                            void handleReactivate(
                                supplier,
                            );
                        }}
                        supplier={
                            dialog.supplier
                        }
                    />
                )}

            {dialog?.type ===
                "deactivate" && (
                    <ConfirmationDialog
                        confirmLabel="Inativar fornecedor"
                        description={
                            <>
                                Fornecedor{" "}
                                {dialog.supplier.name}{" "}
                                ficará inativo e poderá ser reativado depois.
                            </>
                        }
                        errorMessage={submitError}
                        isSubmitting={isSubmitting}
                        onCancel={closeDialog}
                        onConfirm={() => {
                            void handleDeactivate(
                                dialog.supplier,
                            );
                        }}
                        pendingLabel="Inativando..."
                        title="Inativar fornecedor?"
                        titleId="deactivate-supplier-title"
                    />
                )}
        </div>
    );
}