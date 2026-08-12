import {
    useCallback,
    useEffect,
    useMemo,
    useRef,
    useState,
} from "react";

import {
    hasPermission,
} from "@/features/auth/model/currentIdentity";
import {
    useAuth,
} from "@/features/auth/session/useAuth";
import {
    createCompany,
    getCompany,
    updateCompany,
} from "@/features/company/api/companyApi";
import {
    CompanyForm,
} from "@/features/company/components/CompanyForm";
import type {
    Company,
    CreateCompanyPayload,
} from "@/features/company/model/company";
import {
    ApiError,
} from "@/infrastructure/api/apiError";
import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";
import {
    InlineMessage,
    PageHeader,
    StatePanel,
} from "@/shared/components/patterns";
import {
    Badge,
    Button,
    Card,
    Heading,
    Text,
} from "@/shared/components/ui";

interface CompanyFeedback {
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

function formatOptionalValue(
    value: string | null,
): string {
    return value?.trim() || "—";
}

function formatAddress(
    company: Company,
): string {
    const streetAndNumber = [
        company.street,
        company.number,
    ]
        .filter(
            (value): value is string =>
                value !== null &&
                value.trim().length > 0,
        )
        .join(", ");

    const location = [
        company.district,
        company.city,
        company.state,
    ]
        .filter(
            (value): value is string =>
                value !== null &&
                value.trim().length > 0,
        )
        .join(" - ");

    const address = [
        streetAndNumber,
        location,
        company.postal_code,
    ].filter(
        (value): value is string =>
            value !== null &&
            value.trim().length > 0,
    );

    return address.length > 0
        ? address.join(" · ")
        : "—";
}

export function CompanyRoute() {
    const auth = useAuth();
    const identity = auth.identity;

    const canRead =
        identity !== null &&
        hasPermission(
            identity,
            "company.read",
        );

    const canCreate =
        identity !== null &&
        hasPermission(
            identity,
            "company.create",
        );

    const canEdit =
        identity !== null &&
        hasPermission(
            identity,
            "company.update",
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

    const [company, setCompany] =
        useState<Company | null>(null);

    const [isLoading, setIsLoading] =
        useState(true);

    const [loadError, setLoadError] =
        useState<string | null>(null);

    const [isFormOpen, setIsFormOpen] =
        useState(false);

    const [isSubmitting, setIsSubmitting] =
        useState(false);

    const [submitError, setSubmitError] =
        useState<string | null>(null);

    const [feedback, setFeedback] =
        useState<CompanyFeedback | null>(null);

    const loadRevisionRef = useRef(0);

    const loadCompany =
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
                        await getCompany(
                            apiContext,
                        );

                    if (
                        loadRevisionRef.current !==
                        revision
                    ) {
                        return;
                    }

                    setCompany(result);
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
                            "Não foi possível carregar os dados da empresa.",
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
            ],
        );

    useEffect(
        () => {
            const timeoutId =
                window.setTimeout(
                    () => {
                        void loadCompany();
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
        [loadCompany],
    );

    const closeForm =
        useCallback(
            () => {
                if (isSubmitting) {
                    return;
                }

                setIsFormOpen(false);
                setSubmitError(null);
            },
            [isSubmitting],
        );

    const openForm = () => {
        setSubmitError(null);
        setFeedback(null);
        setIsFormOpen(true);
    };

    const handleCreate = async (
        values: CreateCompanyPayload,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setSubmitError(null);

        try {
            const createdCompany =
                await createCompany(
                    apiContext,
                    values,
                );

            setCompany(createdCompany);
            setIsFormOpen(false);

            setFeedback({
                message:
                    "Empresa cadastrada com sucesso.",
                tone: "success",
            });
        }
        catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível cadastrar a empresa.",
                ),
            );
        }
        finally {
            setIsSubmitting(false);
        }
    };

    const handleUpdate = async (
        values: CreateCompanyPayload,
    ): Promise<void> => {
        if (apiContext === null) {
            return;
        }

        setIsSubmitting(true);
        setSubmitError(null);

        try {
            const updatedCompany =
                await updateCompany(
                    apiContext,
                    values,
                );

            setCompany(updatedCompany);
            setIsFormOpen(false);

            setFeedback({
                message:
                    "Empresa atualizada com sucesso.",
                tone: "success",
            });
        }
        catch (error) {
            setSubmitError(
                getErrorMessage(
                    error,
                    "Não foi possível atualizar a empresa.",
                ),
            );
        }
        finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="og3-page-layout">
            <PageHeader
                actions={
                    !isLoading &&
                    company === null &&
                    canCreate ? (
                        <Button onClick={openForm}>
                            Cadastrar empresa
                        </Button>
                    ) : undefined
                }
                badge="Organização"
                description="Gerencie os dados cadastrais, de contato e endereço da empresa ativa."
                title="Empresa"
            />

            {!canRead ? (
                <Card>
                    <StatePanel
                        description="Você não possui permissão para visualizar os dados da empresa."
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
                    {feedback !== null && (
                        <InlineMessage
                            tone={feedback.tone}
                        >
                            {feedback.message}
                        </InlineMessage>
                    )}

                    <Card>
                        {isLoading ? (
                            <StatePanel
                                aria-live="polite"
                                description="Aguarde enquanto os dados cadastrais são consultados."
                                heading="Carregando empresa"
                            />
                        ) : loadError !== null ? (
                            <StatePanel
                                actions={
                                    <Button
                                        onClick={() => {
                                            void loadCompany();
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
                        ) : company === null ? (
                            <StatePanel
                                actions={
                                    canCreate ? (
                                    <Button
                                        onClick={openForm}
                                    >
                                        Cadastrar empresa
                                    </Button>
                                    ) : undefined
                                }
                                description="Cadastre as informações principais da empresa para completar a configuração."
                                heading="Empresa ainda não cadastrada"
                            />
                        ) : (
                            <>
                                <header className="og3-page-header">
                                    <div className="og3-page-header__heading">
                                        <Badge
                                            variant={
                                                company.is_active
                                                    ? "success"
                                                    : "neutral"
                                            }
                                        >
                                            {company.is_active
                                                ? "Ativa"
                                                : "Inativa"}
                                        </Badge>

                                        <Heading level={2}>
                                            {company.trade_name}
                                        </Heading>

                                        <Text tone="secondary">
                                            {formatOptionalValue(
                                                company.legal_name,
                                            )}
                                        </Text>
                                    </div>

                                    {canEdit && (
                                        <Button
                                            onClick={openForm}
                                            variant="secondary"
                                        >
                                            Editar empresa
                                        </Button>
                                    )}
                                </header>

                                <dl className="og3-details-grid">
                                    <div className="og3-details-grid__item">
                                        <dt>CNPJ ou documento</dt>
                                        <dd>
                                            {formatOptionalValue(
                                                company.document_number,
                                            )}
                                        </dd>
                                    </div>

                                    <div className="og3-details-grid__item">
                                        <dt>Inscrição estadual</dt>
                                        <dd>
                                            {formatOptionalValue(
                                                company.state_registration,
                                            )}
                                        </dd>
                                    </div>

                                    <div className="og3-details-grid__item">
                                        <dt>Email</dt>
                                        <dd>
                                            {formatOptionalValue(
                                                company.email,
                                            )}
                                        </dd>
                                    </div>

                                    <div className="og3-details-grid__item">
                                        <dt>Telefone</dt>
                                        <dd>
                                            {formatOptionalValue(
                                                company.phone,
                                            )}
                                        </dd>
                                    </div>

                                    <div className="og3-details-grid__item">
                                        <dt>Site</dt>
                                        <dd>
                                            {formatOptionalValue(
                                                company.website,
                                            )}
                                        </dd>
                                    </div>

                                    <div className="og3-details-grid__item">
                                        <dt>Logotipo</dt>
                                        <dd>
                                            {formatOptionalValue(
                                                company.logo_path,
                                            )}
                                        </dd>
                                    </div>

                                    <div className="og3-details-grid__item">
                                        <dt>Endereço</dt>
                                        <dd>
                                            {formatAddress(
                                                company,
                                            )}
                                        </dd>
                                    </div>
                                </dl>
                            </>
                        )}
                    </Card>
                </>
            )}

            {isFormOpen && company === null && (
                <CompanyForm
                    isSubmitting={isSubmitting}
                    onCancel={closeForm}
                    onSubmit={handleCreate}
                    submitError={submitError}
                />
            )}

            {isFormOpen && company !== null && (
                <CompanyForm
                    company={company}
                    isSubmitting={isSubmitting}
                    onCancel={closeForm}
                    onSubmit={handleUpdate}
                    submitError={submitError}
                />
            )}
        </div>
    );
}