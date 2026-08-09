export interface NavigationItem {
    readonly id: string;
    readonly label: string;
    readonly path: string;
    readonly end?: boolean;
    readonly requiredPermissions?:
    readonly string[];
}

export interface NavigationGroup {
    readonly id: string;
    readonly label: string;
    readonly items:
    readonly NavigationItem[];
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
                    requiredPermissions: [
                        "customers.read",
                    ],
                },
                {
                    id: "suppliers",
                    label: "Fornecedores",
                    path: "/fornecedores",
                    requiredPermissions: [
                        "suppliers.read",
                    ],
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
                    requiredPermissions: [
                        "materials.read",
                    ],
                },
                {
                    id: "services",
                    label: "Serviços",
                    path: "/servicos",
                    requiredPermissions: [
                        "services.read",
                    ],
                },
                {
                    id: "machines",
                    label: "Máquinas",
                    path: "/maquinas",
                    requiredPermissions: [
                        "machines.read",
                    ],
                },
                {
                    id: "brands",
                    label: "Marcas",
                    path: "/marcas",
                    requiredPermissions: [
                        "brands.read",
                    ],
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
                    requiredPermissions: [
                        "employees.read",
                    ],
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
                    requiredPermissions: [
                        "company.read",
                    ],
                },
                {
                    id: "branches",
                    label: "Filiais",
                    path: "/filiais",
                    requiredPermissions: [
                        "branches.read",
                    ],
                },
            ],
        },
    ];

export function hasNavigationAccess(
    item: NavigationItem,
    permissions: ReadonlySet<string>,
): boolean {
    const requiredPermissions =
        item.requiredPermissions;

    if (
        requiredPermissions ===
        undefined ||
        requiredPermissions.length === 0
    ) {
        return true;
    }

    return requiredPermissions.every(
        (permission) =>
            permissions.has(
                permission,
            ),
    );
}

export function filterNavigationGroups(
    groups:
        readonly NavigationGroup[],
    permissions: ReadonlySet<string>,
): readonly NavigationGroup[] {
    return groups.flatMap(
        (group) => {
            const items =
                group.items.filter(
                    (item) =>
                        hasNavigationAccess(
                            item,
                            permissions,
                        ),
                );

            if (items.length === 0) {
                return [];
            }

            return [
                {
                    ...group,
                    items,
                },
            ];
        },
    );
}