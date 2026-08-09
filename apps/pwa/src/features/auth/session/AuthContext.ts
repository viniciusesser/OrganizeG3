import {
    createContext,
} from "react";

import type {
    AccessibleTenant,
} from "@/features/auth/model/accessibleTenant";
import type {
    AuthClientError,
} from "@/features/auth/model/authError";
import type {
    AuthSession,
} from "@/features/auth/model/authSession";
import type {
    AuthenticatedIdentity,
} from "@/features/auth/model/currentIdentity";
import type {
    SignInCredentials,
} from "@/features/auth/session/authSessionService";

export type AuthStatus =
    | "bootstrapping"
    | "signed_out"
    | "resolving_tenants"
    | "tenant_selection_required"
    | "authenticated"
    | "no_tenant_access"
    | "error";

export interface AuthContextValue {
    readonly status: AuthStatus;
    readonly session: AuthSession | null;
    readonly tenants: readonly AccessibleTenant[];
    readonly selectedTenant: AccessibleTenant | null;
    readonly identity: AuthenticatedIdentity | null;
    readonly error: AuthClientError | null;
    readonly signIn: (
        credentials: SignInCredentials,
    ) => Promise<void>;
    readonly selectTenant: (
        tenantId: string,
    ) => Promise<void>;
    readonly signOut: () => Promise<void>;
    readonly retry: () => Promise<void>;
}

export const AuthContext =
    createContext<
        AuthContextValue | null
    >(null);