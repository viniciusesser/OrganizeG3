import type {
    RouteObject,
} from "react-router";

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
    ModulePlaceholderRoute,
} from "@/routes/placeholders/ModulePlaceholderRoute";
import {
    ThemePreviewRoute,
} from "@/routes/theme-preview/ThemePreviewRoute";

export const appRoutes: RouteObject[] = [
    {
        Component: AppShellRoute,
        children: [
            {
                index: true,
                Component: RootRoute,
            },
            {
                path: "clientes",
                element: (
                    <ModulePlaceholderRoute
                        description="Cadastro e gestão dos clientes da empresa."
                        title="Clientes"
                    />
                ),
            },
            {
                path: "fornecedores",
                element: (
                    <ModulePlaceholderRoute
                        description="Cadastro e gestão dos fornecedores."
                        title="Fornecedores"
                    />
                ),
            },
            {
                path: "materiais",
                element: (
                    <ModulePlaceholderRoute
                        description="Materiais utilizados nas operações da empresa."
                        title="Materiais"
                    />
                ),
            },
            {
                path: "servicos",
                element: (
                    <ModulePlaceholderRoute
                        description="Serviços executados ou comercializados pela empresa."
                        title="Serviços"
                    />
                ),
            },
            {
                path: "maquinas",
                element: (
                    <ModulePlaceholderRoute
                        description="Cadastro e acompanhamento das máquinas."
                        title="Máquinas"
                    />
                ),
            },
            {
                path: "marcas",
                element: (
                    <ModulePlaceholderRoute
                        description="Cadastro das marcas utilizadas pelo sistema."
                        title="Marcas"
                    />
                ),
            },
            {
                path: "funcionarios",
                element: (
                    <ModulePlaceholderRoute
                        description="Cadastro e gestão dos funcionários."
                        title="Funcionários"
                    />
                ),
            },
            {
                path: "empresa",
                element: (
                    <ModulePlaceholderRoute
                        description="Informações principais da empresa."
                        title="Empresa"
                    />
                ),
            },
            {
                path: "filiais",
                element: (
                    <ModulePlaceholderRoute
                        description="Estrutura e gestão das filiais."
                        title="Filiais"
                    />
                ),
            },
        ],
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