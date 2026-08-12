export interface Brand {
    readonly id: string;
    readonly tenant_id: string;
    readonly code: string;
    readonly name: string;
    readonly is_active: boolean;
    readonly created_at: string;
    readonly updated_at: string;
}

export interface BrandListFilters {
    readonly includeInactive?: boolean;
    readonly search?: string;
    readonly limit?: number;
    readonly offset?: number;
}

export function formatBrandOption(
    brand: Brand,
): string {
    return `${brand.code} — ${brand.name}`;
}

export function createBrandMap(
    brands: readonly Brand[],
): ReadonlyMap<string, Brand> {
    return new Map(
        brands.map(
            (brand) => [
                brand.id,
                brand,
            ],
        ),
    );
}