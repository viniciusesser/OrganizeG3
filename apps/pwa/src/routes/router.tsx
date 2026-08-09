import {
    createBrowserRouter,
} from "react-router";

import {
    appRoutes,
} from "@/routes/routes";

export const router =
    createBrowserRouter(
        appRoutes,
    );