import {
    createBrowserRouter,
} from "react-router";

import {
    LoginRoute,
} from "@/routes/auth/LoginRoute";
import {
    appRoutes,
} from "@/routes/routes";

export const router =
    createBrowserRouter([
        {
            path: "/login",
            Component: LoginRoute,
        },
        ...appRoutes,
    ]);