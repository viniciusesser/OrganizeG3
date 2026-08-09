import {
    render,
    screen,
} from "@testing-library/react";
import {
    MemoryRouter,
    Route,
    Routes,
    useLocation,
} from "react-router";
import {
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import type {
    AuthContextValue,
    AuthStatus,
} from "@/features/auth/session/AuthContext";
import {
    useAuth,
} from "@/features/auth/session/useAuth";
import {
    AppShellRoute,
} from "@/routes/AppShellRoute";

vi.mock(
    "@/features/auth/session/useAuth",
    () => ({
        useAuth: vi.fn(),
    }),
);

const useAuthMock =
    vi.mocked(
        useAuth,
    );

function createAuthContext(
    status: AuthStatus,
): AuthContextValue {
    return {
        status,
        session: null,
        tenants: [],
        selectedTenant: null,
        identity: null,
        error: null,
        signIn: vi.fn(),
        selectTenant: vi.fn(),
        signOut: vi.fn(),
        retry: vi.fn(),
    };
}

function LoginProbe() {
    const location =
        useLocation();

    const state =
        location.state as {
            readonly from?: {
                readonly pathname?: string;
            };
        } | null;

    return (
        <div>
            <span>
                Página de login
            </span>

            <span data-testid="return-path">
                {state?.from?.pathname ??
                    "sem-destino"}
            </span>
        </div>
    );
}

function renderProtectedRoute(
    status: AuthStatus,
) {
    useAuthMock.mockReturnValue(
        createAuthContext(
            status,
        ),
    );

    return render(
        <MemoryRouter
            initialEntries={[
                "/materiais",
            ]}
        >
            <Routes>
                <Route
                    element={
                        <AppShellRoute />
                    }
                >
                    <Route
                        path="/materiais"
                        element={
                            <div>
                                Conteúdo protegido
                            </div>
                        }
                    />
                </Route>

                <Route
                    path="/login"
                    element={
                        <LoginProbe />
                    }
                />
            </Routes>
        </MemoryRouter>,
    );
}

describe(
    "AppShellRoute authentication",
    () => {
        beforeEach(() => {
            vi.clearAllMocks();
        });

        it.each<AuthStatus>([
            "bootstrapping",
            "signed_out",
            "resolving_tenants",
            "tenant_selection_required",
            "no_tenant_access",
            "error",
        ])(
            "redirects %s state to login",
            (status) => {
                renderProtectedRoute(
                    status,
                );

                expect(
                    screen.getByText(
                        "Página de login",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.getByTestId(
                        "return-path",
                    ),
                ).toHaveTextContent(
                    "/materiais",
                );

                expect(
                    screen.queryByText(
                        "Conteúdo protegido",
                    ),
                ).not.toBeInTheDocument();
            },
        );

        it(
            "renders the protected application when authenticated",
            () => {
                renderProtectedRoute(
                    "authenticated",
                );

                expect(
                    screen.getByText(
                        "Conteúdo protegido",
                    ),
                ).toBeInTheDocument();

                expect(
                    screen.queryByText(
                        "Página de login",
                    ),
                ).not.toBeInTheDocument();
            },
        );
    },
);