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
    archiveCustomer,
    createCustomer,
    listCustomerPage,
    reactivateCustomer,
    updateCustomer,
} from "@/features/customers/api/customersApi";
import {
    CustomerDetails,
} from "@/features/customers/components/CustomerDetails";
import {
    CustomerForm,
} from "@/features/customers/components/CustomerForm";
import {
    CustomerList,
} from "@/features/customers/components/CustomerList";
import {
    hasPermission,
} from "@/features/auth/model/currentIdentity";
import {
    useAuth,
} from "@/features/auth/session/useAuth";
import type {
    Customer,
    CustomerCreateInput,
    CustomerPage,
    CustomerType,
} from "@/features/customers/model/customer";
import {
    DEFAULT_CUSTOMER_PAGE_SIZE,
} from "@/features/customers/model/customer";
import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";
import {
    ApiError,
} from "@/infrastructure/api/apiError";
import {
    Checkbox,
    ConfirmationDialog,
    InlineMessage,
    Select,
} from "@/shared/components/patterns";
import {
    Badge,
    Button,
    Card,
    Heading,
    Input,
    Text,
} from "@/shared/components/ui";

const EMPTY_PAGE: CustomerPage = {
    items: [],
    hasPrevious: false,
    hasNext: false,
    offset: 0,
    pageSize: DEFAULT_CUSTOMER_PAGE_SIZE,
};

type CustomerDialog =
    | {
        readonly type: "create";
    }
    | {
        readonly type: "details";
        readonly customer: Customer;
    }
    | {
        readonly type: "edit";
        readonly customer: Customer;
    }
    | {
        readonly type: "archive";
        readonly customer: Customer;
    }
    | null;

interface CustomerFeedback {
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

export function CustomersRoute() {
    const auth = useAuth();

    const identity = auth.identity;

    const canRead =
        identity !== null &&
        hasPermission(
            identity,
            "customers.read",
        );

    const canCreate =
        identity !== null &&
        hasPermission(
            identity,
            "customers.create",
        );

    const canEdit =
        identity !== null &&
        hasPermission(
            identity,
            "customers.update",
        );

    const canArchive =
        identity !== null &&
        hasPermission(
            identity,
            "customers.archive",
        );

    const canReactivate =
        identity !== null &&
        hasPermission(
            identity,
            "customers.reactivate",
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
        useState<CustomerPage>(EMPTY_PAGE);

    const [searchDraft, setSearchDraft] =
        useState("");

    const [search, setSearch] =
        useState("");

    const [customerType, setCustomerType] =
        useState<CustomerType | null>(null);

    const [includeInactive, setIncludeInactive] =
        useState(false);

    const [offset, setOffset] =
        useState(0);

    const [isLoading, setIsLoading] =
        useState(false);

    const [loadError, setLoadError] =
        useState<string | null>(null);

    const [dialog, setDialog] =
        useState<CustomerDialog>(null);

    const [isSubmitting, setIsSubmitting] =
        useState(false);

    const [submitError, setSubmitError] =
        useState<string | null>(null);

    const [feedback, setFeedback] =
        useState<CustomerFeedback | null>(null);

    const [busyCustomerId, setBusyCustomerId] =
        useState<number | null>(null);

    const loadRevisionRef = useRef(0);

    const loadCustomers =
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
                        await listCustomerPage(
                            apiContext,
                            {
                                includeInactive,
                                search,
                                customerType,
                                limit:
                                    DEFAULT_CUSTOMER_PAGE_SIZE,
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
                            "Não foi possível carregar os clientes.",
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
                canRead,
                customerType,
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
                        void loadCustomers();
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
        [loadCustomers],
    );

    const closeDialog = useCallback(
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
        setCustomerType(null);
        setIncludeInactive(false);
        setOffset(0);
    };

    const handleCreate = async (
        values: CustomerCreateInput,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setSubmitError(null);

        try {
            await createCustomer(
                apiContext,
                values,
            );

            setDialog(null);
            setOffset(0);
            setFeedback({
                message:
                    "Cliente cadastrado com sucesso.",
                tone: "success",
            });

            await loadCustomers();
        } catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível cadastrar o cliente.",
                ),
            );
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleUpdate = async (
        customer: Customer,
        values: CustomerCreateInput,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setSubmitError(null);

        try {
            await updateCustomer(
                apiContext,
                customer.id,
                {
                    ...values,
                    row_version:
                        customer.row_version,
                },
            );

            setDialog(null);
            setFeedback({
                message:
                    "Cliente atualizado com sucesso.",
                tone: "success",
            });

            await loadCustomers();
        } catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível atualizar o cliente.",
                ),
            );
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleArchive = async (
        customer: Customer,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setBusyCustomerId(customer.id);
        setSubmitError(null);

        try {
            await archiveCustomer(
                apiContext,
                customer.id,
                {
                    row_version:
                        customer.row_version,
                },
            );

            setDialog(null);
            setFeedback({
                message:
                    "Cliente inativado com sucesso.",
                tone: "success",
            });

            await loadCustomers();
        } catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível inativar o cliente.",
                ),
            );
        } finally {
            setBusyCustomerId(null);
            setIsSubmitting(false);
        }
    };

    const handleReactivate = async (
        customer: Customer,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setBusyCustomerId(customer.id);
        setSubmitError(null);

        try {
            await reactivateCustomer(
                apiContext,
                customer.id,
                {
                    row_version:
                        customer.row_version,
                },
            );

            setDialog(null);
            setFeedback({
                message:
                    "Cliente reativado com sucesso.",
                tone: "success",
            });

            await loadCustomers();
        } catch (error) {
            setFeedback({
                message:
                    getErrorMessage(
                        error,
                        "Não foi possível reativar o cliente.",
                    ),
                tone: "danger",
            });
        } finally {
            setBusyCustomerId(null);
            setIsSubmitting(false);
        }
    };

    const hasFilters =
        search.length > 0 ||
        customerType !== null ||
        includeInactive;

    const currentPage =
        Math.floor(
            page.offset / page.pageSize,
        ) + 1;

    return (
        <div className="og3-page-layout">
            <header className="og3-page-header">
                <div className="og3-page-header__heading">
                    <Badge variant="accent">
                        Cadastro
                    </Badge>

                    <Heading level={1}>
                        Clientes
                    </Heading>

                    <Text tone="secondary">
                        Gerencie os dados principais dos clientes da empresa.
                    </Text>
                </div>

                {canCreate && (
                    <Button
                        onClick={() => {
                            setSubmitError(null);
                            setDialog({
                                type: "create",
                            });
                        }}
                    >
                        Novo cliente
                    </Button>
                )}
            </header>

            {!canRead ? (
                <Card>
                    <div className="og3-state-panel">
                        <Heading level={3}>
                            Acesso restrito
                        </Heading>

                        <Text tone="secondary">
                            Você não possui permissão para visualizar clientes.
                        </Text>
                    </div>
                </Card>
            ) : apiContext === null ? (
                <Card>
                    <div
                        className="og3-state-panel"
                        role="alert"
                    >
                        <Heading level={3}>
                            Contexto indisponível
                        </Heading>

                        <Text tone="secondary">
                            Não foi possível identificar a sessão e a empresa ativa.
                        </Text>
                    </div>
                </Card>
            ) : (
                <>
                    <Card>
                        <form
                            className="og3-filter-bar"
                            onSubmit={handleSearch}
                        >
                            <div
                                className="og3-filter-bar__search"
                            >
                                <Input
                                    label="Pesquisar clientes"
                                    onChange={(event) => {
                                        setSearchDraft(
                                            event.target.value,
                                        );
                                    }}
                                    placeholder="Nome, documento, email ou telefone"
                                    type="search"
                                    value={searchDraft}
                                />
                            </div>

                            <Select
                                id="customer-type-filter"
                                label="Tipo de pessoa"
                                onChange={(event) => {
                                    const value =
                                        event.target.value;

                                    setCustomerType(
                                        value.length === 0
                                            ? null
                                            : value as CustomerType,
                                    );

                                    setOffset(0);
                                }}
                                value={customerType ?? ""}
                            >
                                <option value="">
                                    Todos os tipos
                                </option>

                                <option value="INDIVIDUAL">
                                    Pessoa Física
                                </option>

                                <option value="CORPORATE">
                                    Pessoa Jurídica
                                </option>
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

                            <div className="og3-filter-bar__actions">
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
                            </div>
                        </form>
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
                            <div
                                aria-live="polite"
                                className="og3-state-panel"
                            >
                                <Heading level={3}>
                                    Carregando clientes
                                </Heading>

                                <Text tone="secondary">
                                    Aguarde enquanto os dados são consultados.
                                </Text>
                            </div>
                        ) : loadError !== null ? (
                            <div
                                className="og3-state-panel"
                                role="alert"
                            >
                                <Heading level={3}>
                                    Não foi possível carregar os clientes
                                </Heading>

                                <Text tone="secondary">
                                    {loadError}
                                </Text>

                                <Button
                                    onClick={() => {
                                        void loadCustomers();
                                    }}
                                    variant="secondary"
                                >
                                    Tentar novamente
                                </Button>
                            </div>
                        ) : page.items.length === 0 ? (
                            <div className="og3-state-panel">
                                <Heading level={3}>
                                    {hasFilters
                                        ? "Nenhum cliente encontrado"
                                        : "Nenhum cliente cadastrado"}
                                </Heading>

                                <Text tone="secondary">
                                    {hasFilters
                                        ? "Revise a pesquisa ou limpe os filtros."
                                        : "Cadastre o primeiro cliente para iniciar a carteira."}
                                </Text>

                                {hasFilters ? (
                                    <Button
                                        onClick={clearFilters}
                                        variant="secondary"
                                    >
                                        Limpar filtros
                                    </Button>
                                ) : canCreate ? (
                                    <Button
                                        onClick={() => {
                                            setDialog({
                                                type: "create",
                                            });
                                        }}
                                    >
                                        Novo cliente
                                    </Button>
                                ) : null}
                            </div>
                        ) : (
                            <>
                                {isLoading && (
                                    <div
                                        className="og3-data-table__loading"
                                        role="status"
                                    >
                                        Atualizando clientes...
                                    </div>
                                )}

                                <CustomerList
                                    busyCustomerId={busyCustomerId}
                                    canArchive={canArchive}
                                    canEdit={canEdit}
                                    canReactivate={canReactivate}
                                    customers={page.items}
                                    onArchive={(customer) => {
                                        setSubmitError(null);
                                        setDialog({
                                            type: "archive",
                                            customer,
                                        });
                                    }}
                                    onEdit={(customer) => {
                                        setSubmitError(null);
                                        setDialog({
                                            type: "edit",
                                            customer,
                                        });
                                    }}
                                    onReactivate={(customer) => {
                                        void handleReactivate(
                                            customer,
                                        );
                                    }}
                                    onView={(customer) => {
                                        setDialog({
                                            type: "details",
                                            customer,
                                        });
                                    }}
                                />

                                <nav
                                    aria-label="Paginação de clientes"
                                    className="og3-pagination"
                                >
                                    <Text
                                        size="sm"
                                        tone="secondary"
                                    >
                                        Página {currentPage}
                                    </Text>

                                    <div className="og3-pagination__actions">
                                        <Button
                                            disabled={
                                                isLoading ||
                                                !page.hasPrevious
                                            }
                                            onClick={() => {
                                                setOffset(
                                                    Math.max(
                                                        0,
                                                        page.offset -
                                                        page.pageSize,
                                                    ),
                                                );
                                            }}
                                            size="sm"
                                            variant="secondary"
                                        >
                                            Anterior
                                        </Button>

                                        <Button
                                            disabled={
                                                isLoading ||
                                                !page.hasNext
                                            }
                                            onClick={() => {
                                                setOffset(
                                                    page.offset +
                                                    page.pageSize,
                                                );
                                            }}
                                            size="sm"
                                            variant="secondary"
                                        >
                                            Próxima
                                        </Button>
                                    </div>
                                </nav>
                            </>
                        )}
                    </Card>
                </>
            )}

            {dialog?.type === "create" && (
                <CustomerForm
                    isSubmitting={isSubmitting}
                    onCancel={closeDialog}
                    onSubmit={handleCreate}
                    submitError={submitError}
                />
            )}

            {dialog?.type === "edit" && (
                <CustomerForm
                    customer={dialog.customer}
                    isSubmitting={isSubmitting}
                    onCancel={closeDialog}
                    onSubmit={(values) =>
                        handleUpdate(
                            dialog.customer,
                            values,
                        )
                    }
                    submitError={submitError}
                />
            )}

            {dialog?.type === "details" && (
                <CustomerDetails
                    canArchive={canArchive}
                    canEdit={canEdit}
                    canReactivate={canReactivate}
                    customer={dialog.customer}
                    isSubmitting={isSubmitting}
                    onArchive={(customer) => {
                        setSubmitError(null);
                        setDialog({
                            type: "archive",
                            customer,
                        });
                    }}
                    onClose={closeDialog}
                    onEdit={(customer) => {
                        setSubmitError(null);
                        setDialog({
                            type: "edit",
                            customer,
                        });
                    }}
                    onReactivate={(customer) => {
                        void handleReactivate(
                            customer,
                        );
                    }}
                />
            )}

            {dialog?.type === "archive" && (
                <ConfirmationDialog
                    confirmLabel="Inativar cliente"
                    description={
                        <>
                            O cliente{" "}
                            {dialog.customer.name}{" "}
                            ficará inativo e poderá ser
                            reativado depois.
                        </>
                    }
                    errorMessage={submitError}
                    isSubmitting={isSubmitting}
                    onCancel={closeDialog}
                    onConfirm={() => {
                        void handleArchive(
                            dialog.customer,
                        );
                    }}
                    pendingLabel="Inativando..."
                    title="Inativar cliente?"
                    titleId="archive-customer-title"
                />
            )}
        </div>
    );
}
