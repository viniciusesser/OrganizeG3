import {
    Outlet,
} from "react-router";

import {
    AppShell,
} from "@/app/shell/AppShell";

export function AppShellRoute() {
    return (
        <AppShell>
            <Outlet />
        </AppShell>
    );
}