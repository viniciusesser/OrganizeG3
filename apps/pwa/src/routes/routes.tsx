import type {
    RouteObject,
} from "react-router";

import {
    NotFoundRoute,
} from "@/routes/NotFoundRoute";
import {
    RootRoute,
} from "@/routes/RootRoute";

export const appRoutes: RouteObject[] = [
    {
        path: "/",
        Component: RootRoute,
    },
    {
        path: "*",
        Component: NotFoundRoute,
    },
];