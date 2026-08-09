import type {
    PropsWithChildren,
} from "react";

import {
    AuthProvider,
} from "@/features/auth/session/AuthProvider";

type AppProvidersProps =
    PropsWithChildren;

export function AppProviders({
    children,
}: AppProvidersProps) {
    return (
        <AuthProvider>
            {children}
        </AuthProvider>
    );
}