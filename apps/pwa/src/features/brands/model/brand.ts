export interface Brand {
    readonly id: string;
    readonly tenant_id: string;
    readonly code: string;
    readonly name: string;
    readonly is_active: boolean;
    readonly created_at: string | null;
    readonly updated_at: string | null;
}

export interface BrandCreateInput {
    readonly code: string;
    readonly name: string;
}

export interface BrandUpdateInput {
    readonly code?: string;
    readonly name?: string;
}

export interface BrandListFilters {
    readonly includeInactive?: boolean;
    readonly search?: string;
    readonly limit?: number;
    readonly offset?: number;
}

export interface BrandPage {
    readonly items:
    readonly Brand[];
    readonly hasPrevious: boolean;
    readonly hasNext: boolean;
    readonly offset: number;
    readonly pageSize: number;
}

export const DEFAULT_BRAND_PAGE_SIZE =
    20;