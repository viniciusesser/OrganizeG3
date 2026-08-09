import type {
    RouteObject,
} from "react-router";

import {
    NotFoundRoute,
} from "@/routes/NotFoundRoute";
import {
    RootRoute,
} from "@/routes/RootRoute";
import {
    ThemePreviewRoute,
} from "@/routes/theme-preview/ThemePreviewRoute";

export const appRoutes: RouteObject[] = [
    {
        path: "/",
        Component: RootRoute,
    },
    {
        path: "/theme-preview",
        Component: ThemePreviewRoute,
    },
    {
        path: "*",
        Component: NotFoundRoute,
    },
];