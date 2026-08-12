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
    createEmployee,
    deactivateEmployee,
    listEmployeePage,
    reactivateEmployee,
    updateEmployee,
} from "@/features/employees/api/employeesApi";
import {
    EmployeeDetails,
} from "@/features/employees/components/EmployeeDetails";
import {
    EmployeeForm,
} from "@/features/employees/components/EmployeeForm";
import {
    EmployeeList,
} from "@/features/employees/components/EmployeeList";
import type {
    Employee,
    EmployeeCreateInput,
    EmployeePage,
    EmploymentStatus,
} from "@/features/employees/model/employee";
import {
    DEFAULT_EMPLOYEE_PAGE_SIZE,
    EMPLOYMENT_STATUSES,
    getEmploymentStatusLabel,
} from "@/features/employees/model/employee";
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

const EMPTY_PAGE: EmployeePage = {
    items: [],
    hasPrevious: false,
    hasNext: false,
    offset: 0,
    pageSize: DEFAULT_EMPLOYEE_PAGE_SIZE,
};

type EmployeeDialog =
    | {
        readonly type: "create";
    }
    | {
        readonly type: "details";
        readonly employee: Employee;
    }
    | {
        readonly type: "edit";
        readonly employee: Employee;
    }
    | {
        readonly type: "deactivate";
        readonly employee: Employee;
    }
    | null;

interface EmployeeFeedback {
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

export function EmployeesRoute() {
    const auth = useAuth();
    const identity = auth.identity;

    const canRead =
        identity !== null &&
        hasPermission(
            identity,
            "employees.read",
        );

    const canCreate =
        identity !== null &&
        hasPermission(
            identity,
            "employees.create",
        );

    const canEdit =
        identity !== null &&
        hasPermission(
            identity,
            "employees.update",
        );

    const canDeactivate =
        identity !== null &&
        hasPermission(
            identity,
            "employees.deactivate",
        );

    const canReactivate =
        identity !== null &&
        hasPermission(
            identity,
            "employees.reactivate",
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
        useState<EmployeePage>(EMPTY_PAGE);

    const [searchDraft, setSearchDraft] =
        useState("");

    const [search, setSearch] =
        useState("");

    const [status, setStatus] =
        useState<EmploymentStatus | "">("");

    const [includeInactive, setIncludeInactive] =
        useState(false);

    const [offset, setOffset] =
        useState(0);

    const [isLoading, setIsLoading] =
        useState(false);

    const [loadError, setLoadError] =
        useState<string | null>(null);

    const [dialog, setDialog] =
        useState<EmployeeDialog>(null);

    const [isSubmitting, setIsSubmitting] =
        useState(false);

    const [submitError, setSubmitError] =
        useState<string | null>(null);

    const [feedback, setFeedback] =
        useState<EmployeeFeedback | null>(null);

    const [busyEmployeeId, setBusyEmployeeId] =
        useState<string | null>(null);

    const loadRevisionRef = useRef(0);

    const loadEmployees =
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
                        await listEmployeePage(
                            apiContext,
                            {
                                includeInactive,
                                search,
                                status:
                                    status === ""
                                        ? null
                                        : status,
                                limit:
                                    DEFAULT_EMPLOYEE_PAGE_SIZE,
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
                            "Não foi possível carregar os funcionários.",
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
                includeInactive,
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
                        void loadEmployees();
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
        [loadEmployees],
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
        setStatus("");
        setIncludeInactive(false);
        setOffset(0);
    };

    const handleCreate = async (
        values: EmployeeCreateInput,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setSubmitError(null);

        try {
            await createEmployee(
                apiContext,
                values,
            );

            setDialog(null);

            setFeedback({
                message:
                    "Funcionário cadastrado com sucesso.",
                tone: "success",
            });

            if (offset === 0) {
                await loadEmployees();
            }
            else {
                setOffset(0);
            }
        }
        catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível cadastrar o funcionário.",
                ),
            );
        }
        finally {
            setIsSubmitting(false);
        }
    };

    const handleUpdate = async (
        employee: Employee,
        values: EmployeeCreateInput,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setSubmitError(null);

        try {
            await updateEmployee(
                apiContext,
                employee.id,
                values,
            );

            setDialog(null);

            setFeedback({
                message:
                    "Funcionário atualizado com sucesso.",
                tone: "success",
            });

            await loadEmployees();
        }
        catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível atualizar o funcionário.",
                ),
            );
        }
        finally {
            setIsSubmitting(false);
        }
    };

    const handleDeactivate = async (
        employee: Employee,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setBusyEmployeeId(employee.id);
        setSubmitError(null);

        try {
            await deactivateEmployee(
                apiContext,
                employee.id,
            );

            setDialog(null);

            setFeedback({
                message:
                    "Funcionário inativado com sucesso.",
                tone: "success",
            });

            await loadEmployees();
        }
        catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível inativar o funcionário.",
                ),
            );
        }
        finally {
            setBusyEmployeeId(null);
            setIsSubmitting(false);
        }
    };

    const handleReactivate = async (
        employee: Employee,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setBusyEmployeeId(employee.id);
        setSubmitError(null);

        try {
            await reactivateEmployee(
                apiContext,
                employee.id,
            );

            setDialog(null);

            setFeedback({
                message:
                    "Funcionário reativado com sucesso.",
                tone: "success",
            });

            await loadEmployees();
        }
        catch (error) {
            setFeedback({
                message:
                    getErrorMessage(
                        error,
                        "Não foi possível reativar o funcionário.",
                    ),
                tone: "danger",
            });
        }
        finally {
            setBusyEmployeeId(null);
            setIsSubmitting(false);
        }
    };

    const hasFilters =
        search.length > 0 ||
        status.length > 0 ||
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
                            Novo funcionário
                        </Button>
                    ) : undefined
                }
                badge="Cadastro"
                description="Gerencie os dados cadastrais, profissionais e a situação dos funcionários da empresa."
                title="Funcionários"
            />

            {!canRead ? (
                <Card>
                    <StatePanel
                        description="Você não possui permissão para visualizar funcionários."
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
                                    label="Pesquisar funcionários"
                                    onChange={(event) => {
                                        setSearchDraft(
                                            event.target.value,
                                        );
                                    }}
                                    placeholder="Código, nome, documento ou email"
                                    type="search"
                                    value={searchDraft}
                                />
                            </div>

                            <Select
                                id="employee-status-filter"
                                label="Situação funcional"
                                onChange={(event) => {
                                    setStatus(
                                        event.target.value as
                                        | EmploymentStatus
                                        | "",
                                    );

                                    setOffset(0);
                                }}
                                value={status}
                            >
                                <option value="">
                                    Todas as situações
                                </option>

                                {EMPLOYMENT_STATUSES.map(
                                    (item) => (
                                        <option
                                            key={item}
                                            value={item}
                                        >
                                            {getEmploymentStatusLabel(
                                                item,
                                            )}
                                        </option>
                                    ),
                                )}
                            </Select>

                            <Checkbox
                                checked={includeInactive}
                                label="Exibir inativos"
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
                                heading="Carregando funcionários"
                            />
                        ) : loadError !== null ? (
                            <StatePanel
                                actions={
                                    <Button
                                        onClick={() => {
                                            void loadEmployees();
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
                                            Novo funcionário
                                        </Button>
                                    ) : undefined
                                }
                                description={
                                    hasFilters
                                        ? "Ajuste os filtros para ampliar a busca."
                                        : "Cadastre o primeiro funcionário da empresa."
                                }
                                heading="Nenhum funcionário encontrado"
                            />
                        ) : (
                            <>
                                <EmployeeList
                                    busyEmployeeId={
                                        busyEmployeeId
                                    }
                                    canDeactivate={
                                        canDeactivate
                                    }
                                    canEdit={canEdit}
                                    canReactivate={
                                        canReactivate
                                    }
                                    employees={page.items}
                                    onDeactivate={(
                                        employee,
                                    ) => {
                                        setSubmitError(
                                            null,
                                        );

                                        setDialog({
                                            type:
                                                "deactivate",
                                            employee,
                                        });
                                    }}
                                    onEdit={(
                                        employee,
                                    ) => {
                                        setSubmitError(
                                            null,
                                        );

                                        setDialog({
                                            type: "edit",
                                            employee,
                                        });
                                    }}
                                    onReactivate={(
                                        employee,
                                    ) => {
                                        void handleReactivate(
                                            employee,
                                        );
                                    }}
                                    onView={(
                                        employee,
                                    ) => {
                                        setDialog({
                                            type:
                                                "details",
                                            employee,
                                        });
                                    }}
                                />

                                <Pagination
                                    aria-label="Paginação de funcionários"
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
                <EmployeeForm
                    isSubmitting={isSubmitting}
                    onCancel={closeDialog}
                    onSubmit={handleCreate}
                    submitError={submitError}
                />
            )}

            {dialog?.type === "edit" && (
                <EmployeeForm
                    employee={dialog.employee}
                    isSubmitting={isSubmitting}
                    onCancel={closeDialog}
                    onSubmit={(values) =>
                        handleUpdate(
                            dialog.employee,
                            values,
                        )
                    }
                    submitError={submitError}
                />
            )}

            {dialog?.type === "details" && (
                <EmployeeDetails
                    canDeactivate={canDeactivate}
                    canEdit={canEdit}
                    canReactivate={canReactivate}
                    employee={dialog.employee}
                    isSubmitting={isSubmitting}
                    onClose={closeDialog}
                    onDeactivate={(employee) => {
                        setSubmitError(null);

                        setDialog({
                            type: "deactivate",
                            employee,
                        });
                    }}
                    onEdit={(employee) => {
                        setSubmitError(null);

                        setDialog({
                            type: "edit",
                            employee,
                        });
                    }}
                    onReactivate={(employee) => {
                        void handleReactivate(
                            employee,
                        );
                    }}
                />
            )}

            {dialog?.type === "deactivate" && (
                <ConfirmationDialog
                    confirmLabel="Inativar funcionário"
                    description={
                        <>
                            O funcionário{" "}
                            {dialog.employee.full_name}{" "}
                            ficará inativo e poderá ser
                            reativado depois.
                        </>
                    }
                    errorMessage={submitError}
                    isSubmitting={isSubmitting}
                    onCancel={closeDialog}
                    onConfirm={() => {
                        void handleDeactivate(
                            dialog.employee,
                        );
                    }}
                    pendingLabel="Inativando..."
                    title="Inativar funcionário?"
                    titleId="deactivate-employee-title"
                />
            )}
        </div>
    );
}