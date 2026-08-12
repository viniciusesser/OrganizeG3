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
    changeMachineStatus,
    createMachine,
    deactivateMachine,
    listMachinePage,
    reactivateMachine,
    updateMachine,
} from "@/features/machines/api/machinesApi";
import {
    MachineDetails,
} from "@/features/machines/components/MachineDetails";
import {
    MachineForm,
} from "@/features/machines/components/MachineForm";
import {
    MachineList,
} from "@/features/machines/components/MachineList";
import type {
    Machine,
    MachineCreateInput,
    MachinePage,
    MachineStatus,
} from "@/features/machines/model/machine";
import {
    DEFAULT_MACHINE_PAGE_SIZE,
    MACHINE_STATUSES,
    getMachineStatusLabel,
} from "@/features/machines/model/machine";
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

const EMPTY_PAGE: MachinePage = {
    items: [],
    hasPrevious: false,
    hasNext: false,
    offset: 0,
    pageSize:
        DEFAULT_MACHINE_PAGE_SIZE,
};

type MachineDialog =
    | {
        readonly type: "create";
    }
    | {
        readonly type: "details";
        readonly machine: Machine;
    }
    | {
        readonly type: "edit";
        readonly machine: Machine;
    }
    | {
        readonly type: "deactivate";
        readonly machine: Machine;
    }
    | null;

interface Feedback {
    readonly message: string;
    readonly tone:
    | "success"
    | "danger";
}

function getErrorMessage(
    error: unknown,
    fallback: string,
): string {
    if (
        error instanceof ApiError
    ) {
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

export function MachinesRoute() {
    const auth =
        useAuth();

    const identity =
        auth.identity;

    const permission = (
        code: string,
    ): boolean =>
        identity !== null &&
        hasPermission(
            identity,
            code,
        );

    const canRead =
        permission(
            "machines.read",
        );

    const canCreate =
        permission(
            "machines.create",
        );

    const canEdit =
        permission(
            "machines.update",
        );

    const canChangeStatus =
        permission(
            "machines.change_status",
        );

    const canDeactivate =
        permission(
            "machines.deactivate",
        );

    const canReactivate =
        permission(
            "machines.reactivate",
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

    const [
        page,
        setPage,
    ] =
        useState<MachinePage>(
            EMPTY_PAGE,
        );

    const [
        searchDraft,
        setSearchDraft,
    ] =
        useState("");

    const [
        search,
        setSearch,
    ] =
        useState("");

    const [
        typeDraft,
        setTypeDraft,
    ] =
        useState("");

    const [
        machineType,
        setMachineType,
    ] =
        useState("");

    const [
        status,
        setStatus,
    ] =
        useState<
            MachineStatus | ""
        >("");

    const [
        includeInactive,
        setIncludeInactive,
    ] =
        useState(false);

    const [
        offset,
        setOffset,
    ] =
        useState(0);

    const [
        isLoading,
        setIsLoading,
    ] =
        useState(false);

    const [
        loadError,
        setLoadError,
    ] =
        useState<
            string | null
        >(null);

    const [
        dialog,
        setDialog,
    ] =
        useState<MachineDialog>(
            null,
        );

    const [
        isSubmitting,
        setIsSubmitting,
    ] =
        useState(false);

    const [
        submitError,
        setSubmitError,
    ] =
        useState<
            string | null
        >(null);

    const [
        feedback,
        setFeedback,
    ] =
        useState<
            Feedback | null
        >(null);

    const [
        busyMachineId,
        setBusyMachineId,
    ] =
        useState<
            string | null
        >(null);

    const loadRevisionRef =
        useRef(0);

    const loadMachines =
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

                setIsLoading(
                    true,
                );

                setLoadError(
                    null,
                );

                try {
                    const result =
                        await listMachinePage(
                            apiContext,
                            {
                                includeInactive,
                                search,
                                machineType,
                                status:
                                    status === ""
                                        ? null
                                        : status,
                                limit:
                                    DEFAULT_MACHINE_PAGE_SIZE,
                                offset,
                            },
                        );

                    if (
                        loadRevisionRef.current ===
                        revision
                    ) {
                        setPage(
                            result,
                        );
                    }
                }
                catch (error) {
                    if (
                        loadRevisionRef.current ===
                        revision
                    ) {
                        setLoadError(
                            getErrorMessage(
                                error,
                                "Não foi possível carregar as máquinas.",
                            ),
                        );
                    }
                }
                finally {
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
                machineType,
                offset,
                search,
                status,
            ],
        );

    useEffect(
        () => {
            const timeoutId =
                window.setTimeout(
                    () => {
                        void loadMachines();
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
        [
            loadMachines,
        ],
    );

    const closeDialog =
        useCallback(
            (): void => {
                if (
                    isSubmitting
                ) {
                    return;
                }

                setDialog(
                    null,
                );

                setSubmitError(
                    null,
                );
            },
            [
                isSubmitting,
            ],
        );

    const handleSearch = (
        event: FormEvent<HTMLFormElement>,
    ): void => {
        event.preventDefault();

        setOffset(
            0,
        );

        setSearch(
            searchDraft.trim(),
        );

        setMachineType(
            typeDraft.trim(),
        );
    };

    const clearFilters =
        (): void => {
            setSearchDraft("");
            setSearch("");
            setTypeDraft("");
            setMachineType("");
            setStatus("");
            setIncludeInactive(false);
            setOffset(0);
        };

    const handleCreate = async (
        values: MachineCreateInput,
    ): Promise<void> => {
        if (
            apiContext === null
        ) {
            return;
        }

        setIsSubmitting(
            true,
        );

        setSubmitError(
            null,
        );

        try {
            await createMachine(
                apiContext,
                values,
            );

            setDialog(
                null,
            );

            setFeedback({
                message:
                    "Máquina cadastrada com sucesso.",
                tone:
                    "success",
            });

            if (
                offset === 0
            ) {
                await loadMachines();
            }
            else {
                setOffset(
                    0,
                );
            }
        }
        catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível cadastrar a máquina.",
                ),
            );
        }
        finally {
            setIsSubmitting(
                false,
            );
        }
    };

    const handleUpdate = async (
        machine: Machine,
        values: MachineCreateInput,
    ): Promise<void> => {
        if (
            apiContext === null
        ) {
            return;
        }

        setIsSubmitting(
            true,
        );

        setSubmitError(
            null,
        );

        try {
            await updateMachine(
                apiContext,
                machine.id,
                values,
            );

            setDialog(
                null,
            );

            setFeedback({
                message:
                    "Máquina atualizada com sucesso.",
                tone:
                    "success",
            });

            await loadMachines();
        }
        catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível atualizar a máquina.",
                ),
            );
        }
        finally {
            setIsSubmitting(
                false,
            );
        }
    };

    const handleStatusChange =
        async (
            machine: Machine,
            nextStatus: MachineStatus,
        ): Promise<void> => {
            if (
                apiContext === null
            ) {
                return;
            }

            setIsSubmitting(
                true,
            );

            setSubmitError(
                null,
            );

            try {
                const updated =
                    await changeMachineStatus(
                        apiContext,
                        machine.id,
                        nextStatus,
                    );

                setDialog({
                    type:
                        "details",
                    machine:
                        updated,
                });

                setFeedback({
                    message:
                        "Status operacional atualizado.",
                    tone:
                        "success",
                });

                await loadMachines();
            }
            catch (error) {
                setSubmitError(
                    getErrorMessage(
                        error,
                        "Não foi possível atualizar o status.",
                    ),
                );
            }
            finally {
                setIsSubmitting(
                    false,
                );
            }
        };

    const handleDeactivate =
        async (
            machine: Machine,
        ): Promise<void> => {
            if (
                apiContext === null
            ) {
                return;
            }

            setIsSubmitting(
                true,
            );

            setBusyMachineId(
                machine.id,
            );

            setSubmitError(
                null,
            );

            try {
                await deactivateMachine(
                    apiContext,
                    machine.id,
                );

                setDialog(
                    null,
                );

                setFeedback({
                    message:
                        "Máquina inativada com sucesso.",
                    tone:
                        "success",
                });

                await loadMachines();
            }
            catch (error) {
                setSubmitError(
                    getErrorMessage(
                        error,
                        "Não foi possível inativar a máquina.",
                    ),
                );
            }
            finally {
                setBusyMachineId(
                    null,
                );

                setIsSubmitting(
                    false,
                );
            }
        };

    const handleReactivate =
        async (
            machine: Machine,
        ): Promise<void> => {
            if (
                apiContext === null
            ) {
                return;
            }

            setIsSubmitting(
                true,
            );

            setBusyMachineId(
                machine.id,
            );

            setSubmitError(
                null,
            );

            try {
                await reactivateMachine(
                    apiContext,
                    machine.id,
                );

                setDialog(
                    null,
                );

                setFeedback({
                    message:
                        "Máquina reativada com sucesso.",
                    tone:
                        "success",
                });

                await loadMachines();
            }
            catch (error) {
                setFeedback({
                    message:
                        getErrorMessage(
                            error,
                            "Não foi possível reativar a máquina.",
                        ),
                    tone:
                        "danger",
                });
            }
            finally {
                setBusyMachineId(
                    null,
                );

                setIsSubmitting(
                    false,
                );
            }
        };

    const hasFilters =
        search.length > 0 ||
        machineType.length > 0 ||
        status.length > 0 ||
        includeInactive;

    const currentPage =
        Math.floor(
            page.offset /
            page.pageSize,
        ) + 1;

    const openCreate =
        (): void => {
            setSubmitError(
                null,
            );

            setDialog({
                type:
                    "create",
            });
        };

    return (
        <div className="og3-page-layout">
            <PageHeader
                actions={
                    canCreate ? (
                        <Button
                            onClick={openCreate}
                        >
                            Nova máquina
                        </Button>
                    ) : undefined
                }
                badge="Produção"
                description="Gerencie máquinas, equipamentos e seus estados operacionais por empresa."
                title="Máquinas"
            />

            {!canRead ? (
                <Card>
                    <StatePanel
                        description="Você não possui permissão para visualizar máquinas."
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
                                    label="Pesquisar máquinas"
                                    onChange={(event) => {
                                        setSearchDraft(
                                            event.target.value,
                                        );
                                    }}
                                    placeholder="Código, nome, fabricante, modelo ou série"
                                    type="search"
                                    value={searchDraft}
                                />
                            </div>

                            <Input
                                label="Tipo"
                                onChange={(event) => {
                                    setTypeDraft(
                                        event.target.value,
                                    );
                                }}
                                placeholder="Ex.: Seccionadora"
                                value={typeDraft}
                            />

                            <div className="og3-field">
                                <label
                                    className="og3-field__label"
                                    htmlFor="machine-status-filter"
                                >
                                    Status operacional
                                </label>

                                <select
                                    className="og3-field__input"
                                    id="machine-status-filter"
                                    onChange={(event) => {
                                        setStatus(
                                            event.target.value as
                                            MachineStatus | "",
                                        );

                                        setOffset(
                                            0,
                                        );
                                    }}
                                    value={status}
                                >
                                    <option value="">
                                        Todos
                                    </option>

                                    {MACHINE_STATUSES.map(
                                        (item) => (
                                            <option
                                                key={item}
                                                value={item}
                                            >
                                                {getMachineStatusLabel(
                                                    item,
                                                )}
                                            </option>
                                        ),
                                    )}
                                </select>
                            </div>

                            <Checkbox
                                checked={includeInactive}
                                onChange={(event) => {
                                    setIncludeInactive(
                                        event.target.checked,
                                    );

                                    setOffset(
                                        0,
                                    );
                                }}
                                label="Exibir inativas"
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
                                heading="Carregando máquinas"
                            />
                        ) : loadError !== null ? (
                            <StatePanel
                                actions={
                                    <Button
                                        onClick={() => {
                                            void loadMachines();
                                        }}
                                        variant="secondary"
                                    >
                                        Tentar novamente
                                    </Button>
                                }
                                description={loadError}
                                heading="Não foi possível carregar as máquinas"
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
                                            onClick={openCreate}
                                        >
                                            Nova máquina
                                        </Button>
                                    ) : undefined
                                }
                                description={
                                    hasFilters
                                        ? "Revise a pesquisa ou limpe os filtros."
                                        : "Cadastre a primeira máquina da empresa."
                                }
                                heading={
                                    hasFilters
                                        ? "Nenhuma máquina encontrada"
                                        : "Nenhuma máquina cadastrada"
                                }
                            />
                        ) : (
                            <>
                                {isLoading && (
                                    <div
                                        className="og3-data-table__loading"
                                        role="status"
                                    >
                                        Atualizando máquinas...
                                    </div>
                                )}

                                <MachineList
                                    busyMachineId={busyMachineId}
                                    canDeactivate={canDeactivate}
                                    canEdit={canEdit}
                                    canReactivate={canReactivate}
                                    machines={page.items}
                                    onDeactivate={(machine) => {
                                        setSubmitError(
                                            null,
                                        );

                                        setDialog({
                                            type:
                                                "deactivate",
                                            machine,
                                        });
                                    }}
                                    onEdit={(machine) => {
                                        setSubmitError(
                                            null,
                                        );

                                        setDialog({
                                            type:
                                                "edit",
                                            machine,
                                        });
                                    }}
                                    onReactivate={(machine) => {
                                        void handleReactivate(
                                            machine,
                                        );
                                    }}
                                    onView={(machine) => {
                                        setSubmitError(
                                            null,
                                        );

                                        setDialog({
                                            type:
                                                "details",
                                            machine,
                                        });
                                    }}
                                />

                                <Pagination
                                    aria-label="Paginação de máquinas"
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
                <MachineForm
                    isSubmitting={isSubmitting}
                    onCancel={closeDialog}
                    onSubmit={handleCreate}
                    submitError={submitError}
                />
            )}

            {dialog?.type === "edit" && (
                <MachineForm
                    isSubmitting={isSubmitting}
                    machine={dialog.machine}
                    onCancel={closeDialog}
                    onSubmit={(values) =>
                        handleUpdate(
                            dialog.machine,
                            values,
                        )
                    }
                    submitError={submitError}
                />
            )}

            {dialog?.type === "details" && (
                <MachineDetails
                    canChangeStatus={canChangeStatus}
                    canDeactivate={canDeactivate}
                    canEdit={canEdit}
                    canReactivate={canReactivate}
                    isSubmitting={isSubmitting}
                    machine={dialog.machine}
                    onChangeStatus={handleStatusChange}
                    onClose={closeDialog}
                    onDeactivate={(machine) => {
                        setSubmitError(
                            null,
                        );

                        setDialog({
                            type:
                                "deactivate",
                            machine,
                        });
                    }}
                    onEdit={(machine) => {
                        setSubmitError(
                            null,
                        );

                        setDialog({
                            type:
                                "edit",
                            machine,
                        });
                    }}
                    onReactivate={(machine) => {
                        void handleReactivate(
                            machine,
                        );
                    }}
                    submitError={submitError}
                />
            )}

            {dialog?.type ===
                "deactivate" && (
                    <ConfirmationDialog
                        confirmLabel="Inativar máquina"
                        description={
                            <>
                                Máquina{" "}
                                {dialog.machine.name}{" "}
                                ficará inativa e poderá ser reativada depois.
                            </>
                        }
                        errorMessage={submitError}
                        isSubmitting={isSubmitting}
                        onCancel={closeDialog}
                        onConfirm={() => {
                            void handleDeactivate(
                                dialog.machine,
                            );
                        }}
                        pendingLabel="Inativando..."
                        title="Inativar máquina?"
                        titleId="deactivate-machine-title"
                    />
                )}
        </div>
    );
}