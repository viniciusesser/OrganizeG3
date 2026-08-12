export interface Material {
    readonly id: string;
    readonly tenant_id: string;
    readonly code: string;
    readonly name: string;
    readonly category: string;
    readonly unit: string;
    readonly brand_id: string | null;
    readonly is_active: boolean;
    readonly created_at: string;
    readonly updated_at: string;
}

export interface MaterialCreateInput {
    readonly code: string;
    readonly name: string;
    readonly category: string;
    readonly unit: string;
    readonly brand_id?: string | null;
}

export interface MaterialUpdateInput {
    readonly code?: string;
    readonly name?: string;
    readonly category?: string;
    readonly unit?: string;
    readonly brand_id?: string | null;
}

export interface MaterialListFilters {
    readonly includeInactive?: boolean;
    readonly search?: string;
    readonly category?: string;
    readonly brandId?: string | null;
    readonly limit?: number;
    readonly offset?: number;
}

export interface MaterialPage {
    readonly items: readonly Material[];
    readonly hasPrevious: boolean;
    readonly hasNext: boolean;
    readonly offset: number;
    readonly pageSize: number;
}

export const DEFAULT_MATERIAL_PAGE_SIZE =
    20;