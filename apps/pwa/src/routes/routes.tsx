import type {
    RouteObject,
} from "react-router";

import {
    BranchesRoute,
} from "@/features/branches/routes/BranchesRoute";
import {
    BrandsRoute,
} from "@/features/brands/routes/BrandsRoute";
import {
    CompanyRoute,
} from "@/features/company/routes/CompanyRoute";
import {
    CustomersRoute,
} from "@/features/customers/routes/CustomersRoute";
import {
    EmployeesRoute,
} from "@/features/employees/routes/EmployeesRoute";
import {
    MachinesRoute,
} from "@/features/machines/routes/MachinesRoute";
import {
    MaterialsRoute,
} from "@/features/materials/routes/MaterialsRoute";
import {
    ServicesRoute,
} from "@/features/services/routes/ServicesRoute";
import {
    SuppliersRoute,
} from "@/features/suppliers/routes/SuppliersRoute";
import {
    AppShellRoute,
} from "@/routes/AppShellRoute";
import {
    NotFoundRoute,
} from "@/routes/NotFoundRoute";
import {
    RootRoute,
} from "@/routes/RootRoute";
import {
    ThemePreviewRoute,
} from "@/routes/theme-preview/ThemePreviewRoute";

export const appRoutes:
    RouteObject[] = [
        {
            Component:
                AppShellRoute,
            children: [
                {
                    index:
                        true,
                    Component:
                        RootRoute,
                },
                {
                    path:
                        "clientes",
                    Component:
                        CustomersRoute,
                },
                {
                    path:
                        "fornecedores",
                    Component:
                        SuppliersRoute,
                },
                {
                    path:
                        "materiais",
                    Component:
                        MaterialsRoute,
                },
                {
                    path:
                        "servicos",
                    Component:
                        ServicesRoute,
                },
                {
                    path:
                        "maquinas",
                    Component:
                        MachinesRoute,
                },
                {
                    path:
                        "marcas",
                    Component:
                        BrandsRoute,
                },
                {
                    path:
                        "funcionarios",
                    Component:
                        EmployeesRoute,
                },
                {
                    path:
                        "empresa",
                    Component:
                        CompanyRoute,
                },
                {
                    path:
                        "filiais",
                    Component:
                        BranchesRoute,
                },
            ],
        },
        {
            path:
                "/theme-preview",
            Component:
                ThemePreviewRoute,
        },
        {
            path:
                "*",
            Component:
                NotFoundRoute,
        },
    ];