import {
    Navigate,
    Outlet,
    useLocation,
} from "react-router";

import {
    AppShell,
} from "@/app/shell/AppShell";
import {
    useAuth,
} from "@/features/auth/session/useAuth";

export function AppShellRoute() {
    const auth =
        useAuth();

    const location =
        useLocation();

    if (
        auth.status !==
        "authenticated"
    ) {
        return (
            <Navigate
                replace
                state={{
                    from: location,
                }}
                to="/login"
            />
        );
    }

    return (
        <AppShell>
            <Outlet />
        </AppShell>
    );
}