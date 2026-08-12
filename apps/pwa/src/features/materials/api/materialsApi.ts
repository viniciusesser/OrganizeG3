import type {
    Material,
    MaterialCreateInput,
    MaterialListFilters,
    MaterialPage,
    MaterialUpdateInput,
} from "@/features/materials/model/material";
import {
    DEFAULT_MATERIAL_PAGE_SIZE,
} from "@/features/materials/model/material";
import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";
import {
    authenticatedApiRequest,
} from "@/infrastructure/api/authenticatedApi";

const MATERIALS_PATH =
    "/api/v1/materials";

function normalizeFilter(
    value: string | undefined,
): string | null {
    if (value === undefined) {
        return null;
    }

    const normalized =
        value.trim();

    return normalized.length > 0
        ? normalized
        : null;
}

function buildMaterialListPath({
    includeInactive = false,
    search,
    category,
    brandId,
    limit = DEFAULT_MATERIAL_PAGE_SIZE,
    offset = 0,
}: MaterialListFilters = {}): string {
    const params =
        new URLSearchParams();

    if (includeInactive) {
        params.set(
            "include_inactive",
            "true",
        );
    }

    const normalizedSearch =
        normalizeFilter(search);

    if (normalizedSearch !== null) {
        params.set(
            "search",
            normalizedSearch,
        );
    }

    const normalizedCategory =
        normalizeFilter(category);

    if (normalizedCategory !== null) {
        params.set(
            "category",
            normalizedCategory,
        );
    }

    const normalizedBrandId =
        normalizeFilter(
            brandId ?? undefined,
        );

    if (normalizedBrandId !== null) {
        params.set(
            "brand_id",
            normalizedBrandId,
        );
    }

    params.set(
        "limit",
        String(limit),
    );

    params.set(
        "offset",
        String(offset),
    );

    return `${MATERIALS_PATH}?${params.toString()}`;
}

export function listMaterials(
    context: AuthenticatedApiContext,
    filters: MaterialListFilters = {},
): Promise<readonly Material[]> {
    return authenticatedApiRequest<
        Material[]
    >(
        buildMaterialListPath(filters),
        context,
        {
            method: "GET",
        },
    );
}

export async function listMaterialPage(
    context: AuthenticatedApiContext,
    filters: MaterialListFilters = {},
): Promise<MaterialPage> {
    const pageSize =
        filters.limit ??
        DEFAULT_MATERIAL_PAGE_SIZE;

    const offset =
        filters.offset ?? 0;

    const items =
        await listMaterials(
            context,
            {
                ...filters,
                limit: pageSize + 1,
                offset,
            },
        );

    const hasNext =
        items.length > pageSize;

    return {
        items: hasNext
            ? items.slice(
                0,
                pageSize,
            )
            : items,
        hasPrevious: offset > 0,
        hasNext,
        offset,
        pageSize,
    };
}

export function getMaterial(
    context: AuthenticatedApiContext,
    materialId: string,
): Promise<Material> {
    return authenticatedApiRequest<Material>(
        `${MATERIALS_PATH}/${materialId}`,
        context,
        {
            method: "GET",
        },
    );
}

export function createMaterial(
    context: AuthenticatedApiContext,
    payload: MaterialCreateInput,
): Promise<Material> {
    return authenticatedApiRequest<Material>(
        MATERIALS_PATH,
        context,
        {
            method: "POST",
            body: payload,
        },
    );
}

export function updateMaterial(
    context: AuthenticatedApiContext,
    materialId: string,
    payload: MaterialUpdateInput,
): Promise<Material> {
    return authenticatedApiRequest<Material>(
        `${MATERIALS_PATH}/${materialId}`,
        context,
        {
            method: "PATCH",
            body: payload,
        },
    );
}

export function deactivateMaterial(
    context: AuthenticatedApiContext,
    materialId: string,
): Promise<Material> {
    return authenticatedApiRequest<Material>(
        `${MATERIALS_PATH}/${materialId}/deactivate`,
        context,
        {
            method: "POST",
        },
    );
}

export function reactivateMaterial(
    context: AuthenticatedApiContext,
    materialId: string,
): Promise<Material> {
    return authenticatedApiRequest<Material>(
        `${MATERIALS_PATH}/${materialId}/reactivate`,
        context,
        {
            method: "POST",
        },
    );
}