import type {
    PropsWithChildren,
} from "react";

import {
    AuthProvider,
} from "@/features/auth/session/AuthProvider";
import {
    PwaProvider,
} from "@/infrastructure/pwa/PwaProvider";

type AppProvidersProps =
    PropsWithChildren;

export function AppProviders({
    children,
}: AppProvidersProps) {
    return (
        <PwaProvider>
            <AuthProvider>
                {children}
            </AuthProvider>
        </PwaProvider>
    );
}