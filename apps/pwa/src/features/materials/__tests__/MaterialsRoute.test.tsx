import {
    cleanup,
    fireEvent,
    render,
    screen,
    waitFor,
    within,
} from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import {
    afterEach,
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    MaterialsRoute,
} from "@/features/materials/routes/MaterialsRoute";

const {
    createMaterialMock,
    deactivateMaterialMock,
    hasPermissionMock,
    listBrandsMock,
    listMaterialPageMock,
    reactivateMaterialMock,
    updateMaterialMock,
    useAuthMock,
} = vi.hoisted(
    () => ({
        createMaterialMock:
            vi.fn(),
        deactivateMaterialMock:
            vi.fn(),
        hasPermissionMock:
            vi.fn(),
        listBrandsMock:
            vi.fn(),
        listMaterialPageMock:
            vi.fn(),
        reactivateMaterialMock:
            vi.fn(),
        updateMaterialMock:
            vi.fn(),
        useAuthMock:
            vi.fn(),
    }),
);

vi.mock(
    "@/features/auth/model/currentIdentity",
    () => ({
        hasPermission:
            hasPermissionMock,
    }),
);

vi.mock(
    "@/features/auth/session/useAuth",
    () => ({
        useAuth: useAuthMock,
    }),
);

vi.mock(
    "@/features/materials/api/brandsApi",
    () => ({
        listBrands:
            listBrandsMock,
    }),
);

vi.mock(
    "@/features/materials/api/materialsApi",
    () => ({
        createMaterial:
            createMaterialMock,
        deactivateMaterial:
            deactivateMaterialMock,
        listMaterialPage:
            listMaterialPageMock,
        reactivateMaterial:
            reactivateMaterialMock,
        updateMaterial:
            updateMaterialMock,
    }),
);

const brand = {
    id: "brand-001",
    tenant_id: "tenant-001",
    code: "DUR",
    name: "Duratex",
    is_active: true,
    created_at:
        "2026-08-10T10:00:00Z",
    updated_at:
        "2026-08-10T10:00:00Z",
} as const;

const material = {
    id: "material-001",
    tenant_id: "tenant-001",
    code: "MDF-001",
    name: "MDF Gianduia",
    category: "MDF",
    unit: "CHAPA",
    brand_id: "brand-001",
    is_active: true,
    created_at:
        "2026-08-10T10:00:00Z",
    updated_at:
        "2026-08-10T10:00:00Z",
} as const;

const activePage = {
    items: [
        material,
    ],
    hasPrevious: false,
    hasNext: false,
    offset: 0,
    pageSize: 20,
};

function configureAuthenticatedUser() {
    useAuthMock.mockReturnValue({
        identity: {
            id: "user-001",
        },
        session: {
            accessToken:
                "access-token",
        },
        selectedTenant: {
            tenantId:
                "tenant-001",
        },
    });

    hasPermissionMock
        .mockReturnValue(true);
}

describe("MaterialsRoute", () => {
    beforeEach(() => {
        vi.clearAllMocks();

        configureAuthenticatedUser();

        listMaterialPageMock
            .mockResolvedValue(
                activePage,
            );

        listBrandsMock
            .mockResolvedValue([
                brand,
            ]);

        createMaterialMock
            .mockResolvedValue(
                material,
            );

        updateMaterialMock
            .mockResolvedValue(
                material,
            );

        deactivateMaterialMock
            .mockResolvedValue({
                ...material,
                is_active: false,
            });

        reactivateMaterialMock
            .mockResolvedValue(
                material,
            );
    });

    afterEach(() => {
        cleanup();
    });

    it(
        "carrega os materiais e as marcas da empresa ativa",
        async () => {
            render(
                <MaterialsRoute />,
            );

            expect(
                await screen.findByText(
                    "MDF Gianduia",
                ),
            ).toBeInTheDocument();

            expect(
                listMaterialPageMock,
            ).toHaveBeenCalledWith(
                {
                    accessToken:
                        "access-token",
                    tenantId:
                        "tenant-001",
                },
                {
                    includeInactive:
                        false,
                    search: "",
                    category: "",
                    brandId: null,
                    limit: 20,
                    offset: 0,
                },
            );

            expect(
                listBrandsMock,
            ).toHaveBeenCalledWith(
                {
                    accessToken:
                        "access-token",
                    tenantId:
                        "tenant-001",
                },
                {
                    includeInactive:
                        true,
                    limit: 200,
                    offset: 0,
                },
            );
        },
    );

    it(
        "não consulta materiais sem permissão de leitura",
        async () => {
            hasPermissionMock
                .mockReturnValue(false);

            render(
                <MaterialsRoute />,
            );

            expect(
                screen.getByText(
                    "Acesso restrito",
                ),
            ).toBeInTheDocument();

            expect(
                screen.getByText(
                    "Você não possui permissão para visualizar materiais.",
                ),
            ).toBeInTheDocument();

            await waitFor(() => {
                expect(
                    listMaterialPageMock,
                ).not.toHaveBeenCalled();

                expect(
                    listBrandsMock,
                ).not.toHaveBeenCalled();
            });
        },
    );

    it(
        "informa quando a sessão ou a empresa ativa está indisponível",
        () => {
            useAuthMock.mockReturnValue({
                identity: {
                    id: "user-001",
                },
                session: null,
                selectedTenant: null,
            });

            render(
                <MaterialsRoute />,
            );

            expect(
                screen.getByText(
                    "Contexto indisponível",
                ),
            ).toBeInTheDocument();

            expect(
                screen.getByText(
                    "Não foi possível identificar a sessão e a empresa ativa.",
                ),
            ).toBeInTheDocument();
        },
    );

    it(
        "pesquisa materiais usando categoria, marca e status",
        async () => {
            render(
                <MaterialsRoute />,
            );

            await screen.findByText(
                "MDF Gianduia",
            );

            await screen.findByRole(
                "option",
                {
                    name:
                        "DUR — Duratex",
                },
            );

            fireEvent.change(
                screen.getByLabelText(
                    "Pesquisar materiais",
                ),
                {
                    target: {
                        value:
                            "  Gianduia  ",
                    },
                },
            );

            fireEvent.change(
                screen.getByLabelText(
                    "Categoria",
                ),
                {
                    target: {
                        value:
                            "  MDF  ",
                    },
                },
            );

            fireEvent.change(
                screen.getByLabelText(
                    "Marca",
                ),
                {
                    target: {
                        value:
                            "brand-001",
                    },
                },
            );

            fireEvent.click(
                screen.getByLabelText(
                    "Exibir inativos",
                ),
            );

            fireEvent.click(
                screen.getByRole(
                    "button",
                    {
                        name:
                            "Pesquisar",
                    },
                ),
            );

            await waitFor(() => {
                expect(
                    listMaterialPageMock,
                ).toHaveBeenLastCalledWith(
                    {
                        accessToken:
                            "access-token",
                        tenantId:
                            "tenant-001",
                    },
                    {
                        includeInactive:
                            true,
                        search:
                            "Gianduia",
                        category: "MDF",
                        brandId:
                            "brand-001",
                        limit: 20,
                        offset: 0,
                    },
                );
            });
        },
    );

    it(
        "cadastra um material",
        async () => {
            render(
                <MaterialsRoute />,
            );

            await screen.findByText(
                "MDF Gianduia",
            );

            await screen.findByRole(
                "option",
                {
                    name:
                        "DUR — Duratex",
                },
            );

            fireEvent.click(
                screen.getByRole(
                    "button",
                    {
                        name:
                            "Novo material",
                    },
                ),
            );

            const dialog =
                screen.getByRole(
                    "dialog",
                    {
                        name:
                            "Novo material",
                    },
                );

            fireEvent.change(
                within(dialog).getByLabelText(
                    "Código do material *",
                ),
                {
                    target: {
                        value:
                            "mdf-002",
                    },
                },
            );

            fireEvent.change(
                within(dialog).getByLabelText(
                    "Nome do material *",
                ),
                {
                    target: {
                        value:
                            "MDF Cristallo",
                    },
                },
            );

            fireEvent.change(
                within(dialog).getByLabelText(
                    "Categoria *",
                ),
                {
                    target: {
                        value: "MDF",
                    },
                },
            );

            fireEvent.change(
                within(dialog).getByLabelText(
                    "Unidade *",
                ),
                {
                    target: {
                        value:
                            "chapa",
                    },
                },
            );

            fireEvent.change(
                within(dialog).getByLabelText(
                    "Marca",
                ),
                {
                    target: {
                        value:
                            "brand-001",
                    },
                },
            );

            fireEvent.click(
                within(dialog).getByRole(
                    "button",
                    {
                        name:
                            "Salvar material",
                    },
                ),
            );

            await waitFor(() => {
                expect(
                    createMaterialMock,
                ).toHaveBeenCalledWith(
                    {
                        accessToken:
                            "access-token",
                        tenantId:
                            "tenant-001",
                    },
                    {
                        code: "MDF-002",
                        name:
                            "MDF Cristallo",
                        category: "MDF",
                        unit: "CHAPA",
                        brand_id:
                            "brand-001",
                    },
                );
            });

            expect(
                await screen.findByText(
                    "Material cadastrado com sucesso.",
                ),
            ).toBeInTheDocument();
        },
    );

    it(
        "atualiza um material",
        async () => {
            render(
                <MaterialsRoute />,
            );

            await screen.findByText(
                "MDF Gianduia",
            );

            fireEvent.click(
                screen.getByRole(
                    "button",
                    {
                        name: "Editar",
                    },
                ),
            );

            fireEvent.change(
                screen.getByLabelText(
                    "Nome do material *",
                ),
                {
                    target: {
                        value:
                            "MDF Gianduia Atualizado",
                    },
                },
            );

            fireEvent.click(
                screen.getByRole(
                    "button",
                    {
                        name:
                            "Salvar alterações",
                    },
                ),
            );

            await waitFor(() => {
                expect(
                    updateMaterialMock,
                ).toHaveBeenCalledWith(
                    {
                        accessToken:
                            "access-token",
                        tenantId:
                            "tenant-001",
                    },
                    material.id,
                    {
                        code: "MDF-001",
                        name:
                            "MDF Gianduia Atualizado",
                        category: "MDF",
                        unit: "CHAPA",
                        brand_id:
                            "brand-001",
                    },
                );
            });

            expect(
                await screen.findByText(
                    "Material atualizado com sucesso.",
                ),
            ).toBeInTheDocument();
        },
    );

    it(
        "inativa um material após confirmação",
        async () => {
            render(
                <MaterialsRoute />,
            );

            await screen.findByText(
                "MDF Gianduia",
            );

            fireEvent.click(
                screen.getByRole(
                    "button",
                    {
                        name: "Inativar",
                    },
                ),
            );

            expect(
                screen.getByText(
                    "Inativar material?",
                ),
            ).toBeInTheDocument();

            fireEvent.click(
                screen.getByRole(
                    "button",
                    {
                        name:
                            "Inativar material",
                    },
                ),
            );

            await waitFor(() => {
                expect(
                    deactivateMaterialMock,
                ).toHaveBeenCalledWith(
                    {
                        accessToken:
                            "access-token",
                        tenantId:
                            "tenant-001",
                    },
                    material.id,
                );
            });

            expect(
                await screen.findByText(
                    "Material inativado com sucesso.",
                ),
            ).toBeInTheDocument();
        },
    );

    it(
        "reativa um material inativo",
        async () => {
            const inactiveMaterial = {
                ...material,
                is_active: false,
            };

            listMaterialPageMock
                .mockResolvedValue({
                    ...activePage,
                    items: [
                        inactiveMaterial,
                    ],
                });

            render(
                <MaterialsRoute />,
            );

            await screen.findByText(
                "MDF Gianduia",
            );

            fireEvent.click(
                screen.getByRole(
                    "button",
                    {
                        name: "Reativar",
                    },
                ),
            );

            await waitFor(() => {
                expect(
                    reactivateMaterialMock,
                ).toHaveBeenCalledWith(
                    {
                        accessToken:
                            "access-token",
                        tenantId:
                            "tenant-001",
                    },
                    material.id,
                );
            });

            expect(
                await screen.findByText(
                    "Material reativado com sucesso.",
                ),
            ).toBeInTheDocument();
        },
    );
});