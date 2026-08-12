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
    createService,
    deactivateService,
    listServicePage,
    reactivateService,
    updateService,
} from "@/features/services/api/servicesApi";
import {
    ServiceDetails,
} from "@/features/services/components/ServiceDetails";
import {
    ServiceForm,
} from "@/features/services/components/ServiceForm";
import {
    ServiceList,
} from "@/features/services/components/ServiceList";
import type {
    Service,
    ServiceCreateInput,
    ServiceExecutionMode,
    ServicePage,
} from "@/features/services/model/service";
import {
    DEFAULT_SERVICE_PAGE_SIZE,
    SERVICE_EXECUTION_MODES,
    getServiceExecutionModeLabel,
} from "@/features/services/model/service";
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

const EMPTY_PAGE: ServicePage = {
    items: [],
    hasPrevious: false,
    hasNext: false,
    offset: 0,
    pageSize:
        DEFAULT_SERVICE_PAGE_SIZE,
};

type ServiceDialog =
    | {
        readonly type: "create";
    }
    | {
        readonly type: "details";
        readonly service: Service;
    }
    | {
        readonly type: "edit";
        readonly service: Service;
    }
    | {
        readonly type: "deactivate";
        readonly service: Service;
    }
    | null;

interface ServiceFeedback {
    readonly message: string;
    readonly tone:
    | "success"
    | "danger";
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

export function ServicesRoute() {
    const auth = useAuth();
    const identity = auth.identity;

    const canRead =
        identity !== null &&
        hasPermission(
            identity,
            "services.read",
        );

    const canCreate =
        identity !== null &&
        hasPermission(
            identity,
            "services.create",
        );

    const canEdit =
        identity !== null &&
        hasPermission(
            identity,
            "services.update",
        );

    const canDeactivate =
        identity !== null &&
        hasPermission(
            identity,
            "services.deactivate",
        );

    const canReactivate =
        identity !== null &&
        hasPermission(
            identity,
            "services.reactivate",
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
                        auth.selectedTenant
                            .tenantId,
                };
            },
            [
                auth.selectedTenant,
                auth.session,
            ],
        );

    const [page, setPage] =
        useState<ServicePage>(
            EMPTY_PAGE,
        );

    const [
        searchDraft,
        setSearchDraft,
    ] = useState("");

    const [search, setSearch] =
        useState("");

    const [
        categoryDraft,
        setCategoryDraft,
    ] = useState("");

    const [category, setCategory] =
        useState("");

    const [
        executionMode,
        setExecutionMode,
    ] = useState<
        ServiceExecutionMode | ""
    >("");

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
    ] = useState<string | null>(
        null,
    );

    const [dialog, setDialog] =
        useState<ServiceDialog>(
            null,
        );

    const [
        isSubmitting,
        setIsSubmitting,
    ] = useState(false);

    const [
        submitError,
        setSubmitError,
    ] = useState<string | null>(
        null,
    );

    const [
        feedback,
        setFeedback,
    ] = useState<
        ServiceFeedback | null
    >(null);

    const [
        busyServiceId,
        setBusyServiceId,
    ] = useState<string | null>(
        null,
    );

    const loadRevisionRef =
        useRef(0);

    const loadServices =
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
                        await listServicePage(
                            apiContext,
                            {
                                includeInactive,
                                search,
                                category,
                                executionMode:
                                    executionMode ===
                                        ""
                                        ? null
                                        : executionMode,
                                limit:
                                    DEFAULT_SERVICE_PAGE_SIZE,
                                offset,
                            },
                        );

                    if (
                        loadRevisionRef
                            .current !==
                        revision
                    ) {
                        return;
                    }

                    setPage(result);
                }
                catch (error) {
                    if (
                        loadRevisionRef
                            .current !==
                        revision
                    ) {
                        return;
                    }

                    setLoadError(
                        getErrorMessage(
                            error,
                            "Não foi possível carregar os serviços.",
                        ),
                    );
                }
                finally {
                    if (
                        loadRevisionRef
                            .current ===
                        revision
                    ) {
                        setIsLoading(false);
                    }
                }
            },
            [
                apiContext,
                canRead,
                category,
                executionMode,
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
                        void loadServices();
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
        [loadServices],
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
        setCategory(
            categoryDraft.trim(),
        );
    };

    const clearFilters = (): void => {
        setSearchDraft("");
        setSearch("");
        setCategoryDraft("");
        setCategory("");
        setExecutionMode("");
        setIncludeInactive(false);
        setOffset(0);
    };

    const handleCreate = async (
        values: ServiceCreateInput,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setSubmitError(null);

        try {
            await createService(
                apiContext,
                values,
            );

            setDialog(null);
            setFeedback({
                message:
                    "Serviço cadastrado com sucesso.",
                tone: "success",
            });

            if (offset === 0) {
                await loadServices();
            }
            else {
                setOffset(0);
            }
        }
        catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível cadastrar o serviço.",
                ),
            );
        }
        finally {
            setIsSubmitting(false);
        }
    };

    const handleUpdate = async (
        service: Service,
        values: ServiceCreateInput,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setSubmitError(null);

        try {
            await updateService(
                apiContext,
                service.id,
                values,
            );

            setDialog(null);
            setFeedback({
                message:
                    "Serviço atualizado com sucesso.",
                tone: "success",
            });

            await loadServices();
        }
        catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível atualizar o serviço.",
                ),
            );
        }
        finally {
            setIsSubmitting(false);
        }
    };

    const handleDeactivate =
        async (
            service: Service,
        ): Promise<void> => {
            if (apiContext === null) {
                return;
            }

            setIsSubmitting(true);
            setBusyServiceId(
                service.id,
            );
            setSubmitError(null);

            try {
                await deactivateService(
                    apiContext,
                    service.id,
                );

                setDialog(null);
                setFeedback({
                    message:
                        "Serviço inativado com sucesso.",
                    tone: "success",
                });

                await loadServices();
            }
            catch (error) {
                setSubmitError(
                    getErrorMessage(
                        error,
                        "Não foi possível inativar o serviço.",
                    ),
                );
            }
            finally {
                setBusyServiceId(null);
                setIsSubmitting(false);
            }
        };

    const handleReactivate =
        async (
            service: Service,
        ): Promise<void> => {
            if (apiContext === null) {
                return;
            }

            setIsSubmitting(true);
            setBusyServiceId(
                service.id,
            );
            setSubmitError(null);

            try {
                await reactivateService(
                    apiContext,
                    service.id,
                );

                setDialog(null);
                setFeedback({
                    message:
                        "Serviço reativado com sucesso.",
                    tone: "success",
                });

                await loadServices();
            }
            catch (error) {
                setFeedback({
                    message:
                        getErrorMessage(
                            error,
                            "Não foi possível reativar o serviço.",
                        ),
                    tone: "danger",
                });
            }
            finally {
                setBusyServiceId(null);
                setIsSubmitting(false);
            }
        };

    const hasFilters =
        search.length > 0 ||
        category.length > 0 ||
        executionMode.length > 0 ||
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
                            Novo serviço
                        </Button>
                    ) : undefined
                }
                badge="Produção"
                description="Gerencie serviços executados internamente, terceirizados ou em modelo híbrido."
                title="Serviços"
            />

            {!canRead ? (
                <Card>
                    <StatePanel
                        description="Você não possui permissão para visualizar serviços."
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
                                    label="Pesquisar serviços"
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

                            <Input
                                label="Categoria"
                                onChange={(
                                    event,
                                ) => {
                                    setCategoryDraft(
                                        event
                                            .target
                                            .value,
                                    );
                                }}
                                placeholder="Ex.: Usinagem ou instalação"
                                value={
                                    categoryDraft
                                }
                            />

                            <div className="og3-field">
                                <label
                                    className="og3-field__label"
                                    htmlFor="service-execution-mode-filter"
                                >
                                    Modo de execução
                                </label>

                                <select
                                    className="og3-field__input"
                                    id="service-execution-mode-filter"
                                    onChange={(
                                        event,
                                    ) => {
                                        setExecutionMode(
                                            event
                                                .target
                                                .value as
                                            | ServiceExecutionMode
                                            | "",
                                        );

                                        setOffset(
                                            0,
                                        );
                                    }}
                                    value={
                                        executionMode
                                    }
                                >
                                    <option value="">
                                        Todos os modos
                                    </option>

                                    {SERVICE_EXECUTION_MODES.map(
                                        (
                                            mode,
                                        ) => (
                                            <option
                                                key={
                                                    mode
                                                }
                                                value={
                                                    mode
                                                }
                                            >
                                                {getServiceExecutionModeLabel(
                                                    mode,
                                                )}
                                            </option>
                                        ),
                                    )}
                                </select>
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
                                heading="Carregando serviços"
                            />
                        ) : loadError !== null ? (
                            <StatePanel
                                actions={
                                    <Button
                                        onClick={() => {
                                            void loadServices();
                                        }}
                                        variant="secondary"
                                    >
                                        Tentar novamente
                                    </Button>
                                }
                                description={loadError}
                                heading="Não foi possível carregar os serviços"
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
                                            Novo serviço
                                        </Button>
                                    ) : undefined
                                }
                                description={
                                    hasFilters
                                        ? "Revise a pesquisa ou limpe os filtros."
                                        : "Cadastre o primeiro serviço da empresa."
                                }
                                heading={
                                    hasFilters
                                        ? "Nenhum serviço encontrado"
                                        : "Nenhum serviço cadastrado"
                                }
                            />
                        ) : (
                            <>
                                {isLoading && (
                                    <div
                                        className="og3-data-table__loading"
                                        role="status"
                                    >
                                        Atualizando serviços...
                                    </div>
                                )}

                                <ServiceList
                                    busyServiceId={
                                        busyServiceId
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
                                        service,
                                    ) => {
                                        setSubmitError(
                                            null,
                                        );

                                        setDialog({
                                            type:
                                                "deactivate",
                                            service,
                                        });
                                    }}
                                    onEdit={(
                                        service,
                                    ) => {
                                        setSubmitError(
                                            null,
                                        );

                                        setDialog({
                                            type:
                                                "edit",
                                            service,
                                        });
                                    }}
                                    onReactivate={(
                                        service,
                                    ) => {
                                        void handleReactivate(
                                            service,
                                        );
                                    }}
                                    onView={(
                                        service,
                                    ) => {
                                        setDialog({
                                            type:
                                                "details",
                                            service,
                                        });
                                    }}
                                    services={
                                        page.items
                                    }
                                />

                                <Pagination
                                    aria-label="Paginação de serviços"
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
                    <ServiceForm
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
                    <ServiceForm
                        isSubmitting={
                            isSubmitting
                        }
                        onCancel={
                            closeDialog
                        }
                        onSubmit={(
                            values,
                        ) => {
                            return handleUpdate(
                                dialog.service,
                                values,
                            );
                        }}
                        service={
                            dialog.service
                        }
                        submitError={
                            submitError
                        }
                    />
                )}

            {dialog?.type ===
                "details" && (
                    <ServiceDetails
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
                            service,
                        ) => {
                            setSubmitError(
                                null,
                            );

                            setDialog({
                                type:
                                    "deactivate",
                                service,
                            });
                        }}
                        onEdit={(
                            service,
                        ) => {
                            setSubmitError(
                                null,
                            );

                            setDialog({
                                type:
                                    "edit",
                                service,
                            });
                        }}
                        onReactivate={(
                            service,
                        ) => {
                            void handleReactivate(
                                service,
                            );
                        }}
                        service={
                            dialog.service
                        }
                    />
                )}

            {dialog?.type ===
                "deactivate" && (
                    <ConfirmationDialog
                        confirmLabel="Inativar serviço"
                        description={
                            <>
                                Serviço{" "}
                                {dialog.service.name}{" "}
                                ficará inativo e poderá ser reativado depois.
                            </>
                        }
                        errorMessage={submitError}
                        isSubmitting={isSubmitting}
                        onCancel={closeDialog}
                        onConfirm={() => {
                            void handleDeactivate(
                                dialog.service,
                            );
                        }}
                        pendingLabel="Inativando..."
                        title="Inativar serviço?"
                        titleId="deactivate-service-title"
                    />
                )}
        </div>
    );
}