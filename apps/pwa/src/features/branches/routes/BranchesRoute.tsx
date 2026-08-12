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
    createBranch,
    deactivateBranch,
    listBranches,
    reactivateBranch,
    updateBranch,
} from "@/features/branches/api/branchesApi";
import {
    BranchDetails,
} from "@/features/branches/components/BranchDetails";
import {
    BranchForm,
} from "@/features/branches/components/BranchForm";
import {
    BranchList,
} from "@/features/branches/components/BranchList";
import type {
    Branch,
    CreateBranchPayload,
} from "@/features/branches/model/branch";
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
    Select,
    StatePanel,
} from "@/shared/components/patterns";
import {
    Button,
    Card,
    Input,
} from "@/shared/components/ui";

const BRANCH_PAGE_SIZE = 20;

interface BranchPage {
    readonly items: readonly Branch[];
    readonly hasPrevious: boolean;
    readonly hasNext: boolean;
    readonly offset: number;
    readonly pageSize: number;
}

const EMPTY_PAGE: BranchPage = {
    items: [],
    hasPrevious: false,
    hasNext: false,
    offset: 0,
    pageSize: BRANCH_PAGE_SIZE,
};

type HeadquartersFilter =
    | ""
    | "true"
    | "false";

type BranchDialog =
    | {
        readonly type: "create";
    }
    | {
        readonly type: "details";
        readonly branch: Branch;
    }
    | {
        readonly type: "edit";
        readonly branch: Branch;
    }
    | {
        readonly type: "deactivate";
        readonly branch: Branch;
    }
    | null;

interface BranchFeedback {
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

export function BranchesRoute() {
    const auth = useAuth();
    const identity = auth.identity;

    const canRead =
        identity !== null &&
        hasPermission(
            identity,
            "branches.read",
        );

    const canCreate =
        identity !== null &&
        hasPermission(
            identity,
            "branches.create",
        );

    const canEdit =
        identity !== null &&
        hasPermission(
            identity,
            "branches.update",
        );

    const canDeactivate =
        identity !== null &&
        hasPermission(
            identity,
            "branches.deactivate",
        );

    const canReactivate =
        identity !== null &&
        hasPermission(
            identity,
            "branches.reactivate",
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
        useState<BranchPage>(EMPTY_PAGE);

    const [searchDraft, setSearchDraft] =
        useState("");

    const [search, setSearch] =
        useState("");

    const [
        headquartersFilter,
        setHeadquartersFilter,
    ] = useState<HeadquartersFilter>("");

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
        useState<BranchDialog>(null);

    const [isSubmitting, setIsSubmitting] =
        useState(false);

    const [submitError, setSubmitError] =
        useState<string | null>(null);

    const [feedback, setFeedback] =
        useState<BranchFeedback | null>(
            null,
        );

    const [
        busyBranchId,
        setBusyBranchId,
    ] = useState<string | null>(null);

    const loadRevisionRef = useRef(0);

    const loadBranches =
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
                    const loadedItems =
                        await listBranches(
                            apiContext,
                            {
                                includeInactive,
                                search,
                                isHeadquarters:
                                    headquartersFilter === ""
                                        ? undefined
                                        : headquartersFilter ===
                                        "true",
                                limit:
                                    BRANCH_PAGE_SIZE + 1,
                                offset,
                            },
                        );

                    if (
                        loadRevisionRef.current !==
                        revision
                    ) {
                        return;
                    }

                    const hasNext =
                        loadedItems.length >
                        BRANCH_PAGE_SIZE;

                    setPage({
                        items:
                            hasNext
                                ? loadedItems.slice(
                                    0,
                                    BRANCH_PAGE_SIZE,
                                )
                                : loadedItems,
                        hasPrevious:
                            offset > 0,
                        hasNext,
                        offset,
                        pageSize:
                            BRANCH_PAGE_SIZE,
                    });
                }
                catch (error) {
                    if (
                        loadRevisionRef.current !==
                        revision
                    ) {
                        return;
                    }

                    setLoadError(
                        getErrorMessage(
                            error,
                            "Não foi possível carregar as filiais.",
                        ),
                    );
                }
                finally {
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
                canRead,
                headquartersFilter,
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
                        void loadBranches();
                    },
                    0,
                );

            return () => {
                window.clearTimeout(timeoutId);
                loadRevisionRef.current += 1;
            };
        },
        [loadBranches],
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
        setSearch(searchDraft.trim());
    };

    const clearFilters = () => {
        setSearchDraft("");
        setSearch("");
        setHeadquartersFilter("");
        setIncludeInactive(false);
        setOffset(0);
    };

    const handleCreate = async (
        values: CreateBranchPayload,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setSubmitError(null);

        try {
            await createBranch(
                apiContext,
                values,
            );

            setDialog(null);

            setFeedback({
                message:
                    "Filial cadastrada com sucesso.",
                tone: "success",
            });

            if (offset === 0) {
                await loadBranches();
            }
            else {
                setOffset(0);
            }
        }
        catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível cadastrar a filial.",
                ),
            );
        }
        finally {
            setIsSubmitting(false);
        }
    };

    const handleUpdate = async (
        branch: Branch,
        values: CreateBranchPayload,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setSubmitError(null);

        try {
            await updateBranch(
                apiContext,
                branch.id,
                values,
            );

            setDialog(null);

            setFeedback({
                message:
                    "Filial atualizada com sucesso.",
                tone: "success",
            });

            await loadBranches();
        }
        catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível atualizar a filial.",
                ),
            );
        }
        finally {
            setIsSubmitting(false);
        }
    };

    const handleDeactivate = async (
        branch: Branch,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setBusyBranchId(branch.id);
        setSubmitError(null);

        try {
            await deactivateBranch(
                apiContext,
                branch.id,
            );

            setDialog(null);

            setFeedback({
                message:
                    "Filial inativada com sucesso.",
                tone: "success",
            });

            await loadBranches();
        }
        catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível inativar a filial.",
                ),
            );
        }
        finally {
            setBusyBranchId(null);
            setIsSubmitting(false);
        }
    };

    const handleReactivate = async (
        branch: Branch,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setBusyBranchId(branch.id);
        setSubmitError(null);

        try {
            await reactivateBranch(
                apiContext,
                branch.id,
            );

            setDialog(null);

            setFeedback({
                message:
                    "Filial reativada com sucesso.",
                tone: "success",
            });

            await loadBranches();
        }
        catch (error) {
            setFeedback({
                message:
                    getErrorMessage(
                        error,
                        "Não foi possível reativar a filial.",
                    ),
                tone: "danger",
            });
        }
        finally {
            setBusyBranchId(null);
            setIsSubmitting(false);
        }
    };

    const hasFilters =
        search.length > 0 ||
        headquartersFilter.length > 0 ||
        includeInactive;

    const currentPage =
        Math.floor(
            page.offset / page.pageSize,
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
                            Nova filial
                        </Button>
                    ) : undefined
                }
                badge="Cadastro"
                description="Gerencie a matriz, as filiais, os dados fiscais, os contatos e os endereços da empresa."
                title="Filiais"
            />

            {!canRead ? (
                <Card>
                    <StatePanel
                        description="Você não possui permissão para visualizar filiais."
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
                                    label="Pesquisar filiais"
                                    onChange={(event) => {
                                        setSearchDraft(
                                            event.target.value,
                                        );
                                    }}
                                    placeholder="Código, nome, documento ou cidade"
                                    type="search"
                                    value={searchDraft}
                                />
                            </div>

                            <Select
                                id="branch-type-filter"
                                label="Tipo de unidade"
                                onChange={(event) => {
                                    setHeadquartersFilter(
                                        event.target.value as
                                        HeadquartersFilter,
                                    );

                                    setOffset(0);
                                }}
                                value={headquartersFilter}
                            >
                                <option value="">
                                    Todas as unidades
                                </option>

                                <option value="true">
                                    Somente matriz
                                </option>

                                <option value="false">
                                    Somente filiais
                                </option>
                            </Select>

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
                            page.items.length === 0 ? (
                            <StatePanel
                                aria-live="polite"
                                description="Aguarde enquanto os dados são consultados."
                                heading="Carregando filiais"
                            />
                        ) : loadError !== null ? (
                            <StatePanel
                                actions={
                                    <Button
                                        onClick={() => {
                                            void loadBranches();
                                        }}
                                        variant="secondary"
                                    >
                                        Tentar novamente
                                    </Button>
                                }
                                description={loadError}
                                heading="Não foi possível carregar"
                                role="alert"
                            />
                        ) : page.items.length === 0 ? (
                            <StatePanel
                                actions={
                                    canCreate && !hasFilters ? (
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
                                            Nova filial
                                        </Button>
                                    ) : undefined
                                }
                                description={
                                    hasFilters
                                        ? "Ajuste os filtros para ampliar a busca."
                                        : "Cadastre a primeira unidade da empresa."
                                }
                                heading="Nenhuma filial encontrada"
                            />
                        ) : (
                            <>
                                <BranchList
                                    branches={page.items}
                                    busyBranchId={
                                        busyBranchId
                                    }
                                    canDeactivate={
                                        canDeactivate
                                    }
                                    canEdit={canEdit}
                                    canReactivate={
                                        canReactivate
                                    }
                                    onDeactivate={(
                                        branch,
                                    ) => {
                                        setSubmitError(
                                            null,
                                        );

                                        setDialog({
                                            type:
                                                "deactivate",
                                            branch,
                                        });
                                    }}
                                    onEdit={(branch) => {
                                        setSubmitError(
                                            null,
                                        );

                                        setDialog({
                                            type: "edit",
                                            branch,
                                        });
                                    }}
                                    onReactivate={(
                                        branch,
                                    ) => {
                                        void handleReactivate(
                                            branch,
                                        );
                                    }}
                                    onView={(branch) => {
                                        setDialog({
                                            type:
                                                "details",
                                            branch,
                                        });
                                    }}
                                />

                                <Pagination
                                    aria-label="Paginação de filiais"
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
                <BranchForm
                    isSubmitting={isSubmitting}
                    onCancel={closeDialog}
                    onSubmit={handleCreate}
                    submitError={submitError}
                />
            )}

            {dialog?.type === "edit" && (
                <BranchForm
                    branch={dialog.branch}
                    isSubmitting={isSubmitting}
                    onCancel={closeDialog}
                    onSubmit={(values) =>
                        handleUpdate(
                            dialog.branch,
                            values,
                        )
                    }
                    submitError={submitError}
                />
            )}

            {dialog?.type === "details" && (
                <BranchDetails
                    branch={dialog.branch}
                    canDeactivate={
                        canDeactivate
                    }
                    canEdit={canEdit}
                    canReactivate={
                        canReactivate
                    }
                    isSubmitting={isSubmitting}
                    onClose={closeDialog}
                    onDeactivate={(branch) => {
                        setSubmitError(null);

                        setDialog({
                            type: "deactivate",
                            branch,
                        });
                    }}
                    onEdit={(branch) => {
                        setSubmitError(null);

                        setDialog({
                            type: "edit",
                            branch,
                        });
                    }}
                    onReactivate={(branch) => {
                        void handleReactivate(
                            branch,
                        );
                    }}
                />
            )}

            {dialog?.type === "deactivate" && (
                <ConfirmationDialog
                    confirmLabel="Inativar filial"
                    description={
                        <>
                            A unidade{" "}
                            {dialog.branch.name}{" "}
                            ficará inativa e poderá ser
                            reativada depois.
                        </>
                    }
                    errorMessage={submitError}
                    isSubmitting={isSubmitting}
                    onCancel={closeDialog}
                    onConfirm={() => {
                        void handleDeactivate(
                            dialog.branch,
                        );
                    }}
                    pendingLabel="Inativando..."
                    title="Inativar filial?"
                    titleId="deactivate-branch-title"
                />
            )}
        </div>
    );
}