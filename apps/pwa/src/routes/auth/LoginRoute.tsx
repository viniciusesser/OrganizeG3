import {
    useState,
} from "react";
import type {
    FormEvent,
} from "react";
import {
    Navigate,
    useLocation,
} from "react-router";

import type {
    AccessibleTenant,
} from "@/features/auth/model/accessibleTenant";
import {
    useAuth,
} from "@/features/auth/session/useAuth";
import {
    Button,
    Card,
    Heading,
    Input,
    Text,
} from "@/shared/components/ui";

interface ReturnLocation {
    readonly pathname?: unknown;
    readonly search?: unknown;
    readonly hash?: unknown;
}

interface LoginNavigationState {
    readonly from?: ReturnLocation;
}

function getErrorMessage(
    error: unknown,
): string {
    if (error instanceof Error) {
        return error.message;
    }

    return (
        "Não foi possível concluir a operação."
    );
}

function normalizeLocationPart(
    value: unknown,
): string {
    return typeof value === "string"
        ? value
        : "";
}

function resolveReturnPath(
    state: unknown,
): string {
    if (
        state === null ||
        typeof state !== "object"
    ) {
        return "/";
    }

    const navigationState =
        state as LoginNavigationState;

    const from =
        navigationState.from;

    if (
        from === undefined ||
        from === null
    ) {
        return "/";
    }

    const pathname =
        normalizeLocationPart(
            from.pathname,
        );

    if (
        !pathname.startsWith("/") ||
        pathname.startsWith("//")
    ) {
        return "/";
    }

    const search =
        normalizeLocationPart(
            from.search,
        );

    const hash =
        normalizeLocationPart(
            from.hash,
        );

    return (
        pathname +
        search +
        hash
    );
}

export function LoginRoute() {
    const auth =
        useAuth();

    const location =
        useLocation();

    const returnPath =
        resolveReturnPath(
            location.state,
        );

    const [
        email,
        setEmail,
    ] =
        useState("");

    const [
        password,
        setPassword,
    ] =
        useState("");

    const [
        submitting,
        setSubmitting,
    ] =
        useState(false);

    const [
        actionError,
        setActionError,
    ] =
        useState<string | null>(
            null,
        );

    if (
        auth.status ===
        "authenticated"
    ) {
        return (
            <Navigate
                replace
                to={returnPath}
            />
        );
    }

    async function handleSignIn(
        event: FormEvent<HTMLFormElement>,
    ): Promise<void> {
        event.preventDefault();

        setSubmitting(true);
        setActionError(null);

        try {
            await auth.signIn({
                email,
                password,
            });
        } catch (error) {
            setActionError(
                getErrorMessage(
                    error,
                ),
            );
        } finally {
            setSubmitting(false);
        }
    }

    async function handleTenantSelection(
        tenant: AccessibleTenant,
    ): Promise<void> {
        setSubmitting(true);
        setActionError(null);

        try {
            await auth.selectTenant(
                tenant.tenantId,
            );
        } catch (error) {
            setActionError(
                getErrorMessage(
                    error,
                ),
            );
        } finally {
            setSubmitting(false);
        }
    }

    async function handleRetry():
        Promise<void> {
        setSubmitting(true);
        setActionError(null);

        try {
            await auth.retry();
        } catch (error) {
            setActionError(
                getErrorMessage(
                    error,
                ),
            );
        } finally {
            setSubmitting(false);
        }
    }

    async function handleSignOut():
        Promise<void> {
        setSubmitting(true);
        setActionError(null);

        try {
            await auth.signOut();
        } catch (error) {
            setActionError(
                getErrorMessage(
                    error,
                ),
            );
        } finally {
            setSubmitting(false);
        }
    }

    const isResolving =
        auth.status ===
        "bootstrapping" ||
        auth.status ===
        "resolving_tenants";

    return (
        <main className="og3-auth-page">
            <section
                aria-label="Autenticação OrganizeG3"
                className="og3-auth-layout"
            >
                <div className="og3-auth-brand">
                    <Text
                        className="og3-auth-brand__eyebrow"
                        size="sm"
                        tone="muted"
                    >
                        Plataforma de gestão
                    </Text>

                    <Heading
                        className="og3-auth-brand__title"
                        level={1}
                    >
                        OrganizeG3
                    </Heading>

                    <Text
                        className="og3-auth-brand__description"
                        tone="secondary"
                    >
                        Gestão integrada para
                        comercial, produção,
                        pessoas e operações.
                    </Text>
                </div>

                <Card
                    className="og3-auth-card"
                    header={
                        <div className="og3-auth-card__heading">
                            <Heading level={2}>
                                {auth.status ===
                                    "tenant_selection_required"
                                    ? "Escolha a empresa"
                                    : "Acessar sistema"}
                            </Heading>

                            <Text tone="secondary">
                                {auth.status ===
                                    "tenant_selection_required"
                                    ? "Selecione o ambiente que deseja acessar."
                                    : "Entre com seu usuário e senha."}
                            </Text>
                        </div>
                    }
                >
                    {isResolving && (
                        <div
                            aria-live="polite"
                            className="og3-auth-status"
                            role="status"
                        >
                            <Text tone="secondary">
                                Carregando seu acesso...
                            </Text>
                        </div>
                    )}

                    {auth.status ===
                        "signed_out" && (
                            <form
                                className="og3-auth-form"
                                onSubmit={(event) => {
                                    void handleSignIn(
                                        event,
                                    );
                                }}
                            >
                                <Input
                                    autoComplete="email"
                                    disabled={submitting}
                                    label="E-mail"
                                    name="email"
                                    onChange={(event) => {
                                        setEmail(
                                            event.target.value,
                                        );
                                    }}
                                    placeholder="seu@email.com"
                                    type="email"
                                    value={email}
                                />

                                <Input
                                    autoComplete="current-password"
                                    disabled={submitting}
                                    label="Senha"
                                    name="password"
                                    onChange={(event) => {
                                        setPassword(
                                            event.target.value,
                                        );
                                    }}
                                    type="password"
                                    value={password}
                                />

                                {actionError !== null && (
                                    <div
                                        className="og3-auth-message og3-auth-message--danger"
                                        role="alert"
                                    >
                                        <Text size="sm">
                                            {actionError}
                                        </Text>
                                    </div>
                                )}

                                <Button
                                    className="og3-auth-submit"
                                    disabled={submitting}
                                    size="lg"
                                    type="submit"
                                >
                                    {submitting
                                        ? "Entrando..."
                                        : "Entrar"}
                                </Button>
                            </form>
                        )}

                    {auth.status ===
                        "tenant_selection_required" && (
                            <div className="og3-auth-selection">
                                <div
                                    className="og3-auth-tenant-list"
                                    role="list"
                                >
                                    {auth.tenants.map(
                                        (tenant) => (
                                            <Button
                                                className="og3-auth-tenant"
                                                disabled={submitting}
                                                key={
                                                    tenant.tenantId
                                                }
                                                onClick={() => {
                                                    void handleTenantSelection(
                                                        tenant,
                                                    );
                                                }}
                                                size="lg"
                                                type="button"
                                                variant="secondary"
                                            >
                                                {tenant.name}
                                            </Button>
                                        ),
                                    )}
                                </div>

                                {actionError !== null && (
                                    <div
                                        className="og3-auth-message og3-auth-message--danger"
                                        role="alert"
                                    >
                                        <Text size="sm">
                                            {actionError}
                                        </Text>
                                    </div>
                                )}

                                <Button
                                    disabled={submitting}
                                    onClick={() => {
                                        void handleSignOut();
                                    }}
                                    type="button"
                                    variant="secondary"
                                >
                                    Sair
                                </Button>
                            </div>
                        )}

                    {auth.status ===
                        "no_tenant_access" && (
                            <div className="og3-auth-status">
                                <div className="og3-auth-message og3-auth-message--warning">
                                    <Heading level={3}>
                                        Acesso não disponível
                                    </Heading>

                                    <Text tone="secondary">
                                        Seu usuário está
                                        autenticado, mas não
                                        possui uma empresa ativa
                                        disponível no OrganizeG3.
                                    </Text>
                                </div>

                                {actionError !== null && (
                                    <div
                                        className="og3-auth-message og3-auth-message--danger"
                                        role="alert"
                                    >
                                        <Text size="sm">
                                            {actionError}
                                        </Text>
                                    </div>
                                )}

                                <Button
                                    disabled={submitting}
                                    onClick={() => {
                                        void handleRetry();
                                    }}
                                    type="button"
                                    variant="secondary"
                                >
                                    Verificar novamente
                                </Button>

                                <Button
                                    disabled={submitting}
                                    onClick={() => {
                                        void handleSignOut();
                                    }}
                                    type="button"
                                >
                                    Sair
                                </Button>
                            </div>
                        )}

                    {auth.status ===
                        "error" && (
                            <div className="og3-auth-status">
                                <div
                                    className="og3-auth-message og3-auth-message--danger"
                                    role="alert"
                                >
                                    <Heading level={3}>
                                        Não foi possível
                                        carregar seu acesso
                                    </Heading>

                                    <Text tone="secondary">
                                        {auth.error?.message ??
                                            "Ocorreu um erro ao carregar a autenticação."}
                                    </Text>
                                </div>

                                {actionError !== null && (
                                    <div
                                        className="og3-auth-message og3-auth-message--danger"
                                        role="alert"
                                    >
                                        <Text size="sm">
                                            {actionError}
                                        </Text>
                                    </div>
                                )}

                                <Button
                                    disabled={submitting}
                                    onClick={() => {
                                        void handleRetry();
                                    }}
                                    type="button"
                                >
                                    Tentar novamente
                                </Button>

                                {auth.session !== null && (
                                    <Button
                                        disabled={submitting}
                                        onClick={() => {
                                            void handleSignOut();
                                        }}
                                        type="button"
                                        variant="secondary"
                                    >
                                        Sair
                                    </Button>
                                )}
                            </div>
                        )}
                </Card>

                <Text
                    className="og3-auth-footer"
                    size="sm"
                    tone="muted"
                >
                    Acesso protegido pela
                    autenticação da plataforma.
                </Text>
            </section>
        </main>
    );
}