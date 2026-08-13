import {
    describe,
    expect,
    it,
} from "vitest";

import {
    findNavigationContext,
    getNavigationContextLabel,
    getNavigationDocumentTitle,
} from "@/app/navigation/navigation";

describe("navigation context", () => {
    it(
        "resolves the application root",
        () => {
            const context =
                findNavigationContext(
                    "/",
                );

            expect(
                context?.group.id,
            ).toBe(
                "overview",
            );

            expect(
                context?.item.id,
            ).toBe(
                "home",
            );
        },
    );

    it(
        "resolves a module route",
        () => {
            const context =
                findNavigationContext(
                    "/clientes",
                );

            expect(
                context?.group.label,
            ).toBe(
                "Comercial",
            );

            expect(
                context?.item.label,
            ).toBe(
                "Clientes",
            );
        },
    );

    it(
        "keeps the parent context for nested routes",
        () => {
            const context =
                findNavigationContext(
                    "/clientes/cliente-id",
                );

            expect(
                context?.group.id,
            ).toBe(
                "commercial",
            );

            expect(
                context?.item.id,
            ).toBe(
                "customers",
            );
        },
    );

    it(
        "does not treat another route as the root",
        () => {
            const context =
                findNavigationContext(
                    "/rota-inexistente",
                );

            expect(
                context,
            ).toBeNull();
        },
    );

    it(
        "normalizes trailing slashes",
        () => {
            const context =
                findNavigationContext(
                    "/materiais/",
                );

            expect(
                context?.item.id,
            ).toBe(
                "materials",
            );
        },
    );

    it(
        "builds the current page labels",
        () => {
            const context =
                findNavigationContext(
                    "/fornecedores",
                );

            expect(
                getNavigationContextLabel(
                    context,
                ),
            ).toBe(
                "Comercial • Fornecedores",
            );

            expect(
                getNavigationDocumentTitle(
                    context,
                ),
            ).toBe(
                "Fornecedores | OrganizeG3",
            );
        },
    );

    it(
        "uses safe labels for an unknown route",
        () => {
            expect(
                getNavigationContextLabel(
                    null,
                ),
            ).toBe(
                "OrganizeG3",
            );

            expect(
                getNavigationDocumentTitle(
                    null,
                ),
            ).toBe(
                "OrganizeG3",
            );
        },
    );
});