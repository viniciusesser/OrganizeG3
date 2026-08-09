export interface NavigationItem {
    readonly id: string;
    readonly label: string;
    readonly path: string;
    readonly end?: boolean;
    readonly requiredPermissions?: readonly string[];
}

export interface NavigationGroup {
    readonly id: string;
    readonly label: string;
    readonly items: readonly NavigationItem[];
}

export const navigationGroups:
    readonly NavigationGroup[] = [
        {
            id: "overview",
            label: "Visão geral",
            items: [
                {
                    id: "home",
                    label: "Início",
                    path: "/",
                    end: true,
                },
            ],
        },
        {
            id: "commercial",
            label: "Comercial",
            items: [
                {
                    id: "customers",
                    label: "Clientes",
                    path: "/clientes",
                },
                {
                    id: "suppliers",
                    label: "Fornecedores",
                    path: "/fornecedores",
                },
            ],
        },
        {
            id: "operations",
            label: "Operações",
            items: [
                {
                    id: "materials",
                    label: "Materiais",
                    path: "/materiais",
                },
                {
                    id: "services",
                    label: "Serviços",
                    path: "/servicos",
                },
                {
                    id: "machines",
                    label: "Máquinas",
                    path: "/maquinas",
                },
                {
                    id: "brands",
                    label: "Marcas",
                    path: "/marcas",
                },
            ],
        },
        {
            id: "people",
            label: "Pessoas",
            items: [
                {
                    id: "employees",
                    label: "Funcionários",
                    path: "/funcionarios",
                },
            ],
        },
        {
            id: "organization",
            label: "Organização",
            items: [
                {
                    id: "company",
                    label: "Empresa",
                    path: "/empresa",
                },
                {
                    id: "branches",
                    label: "Filiais",
                    path: "/filiais",
                },
            ],
        },
    ];