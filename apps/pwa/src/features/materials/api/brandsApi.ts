import type {
    Brand,
    BrandListFilters,
} from "@/features/materials/model/brand";
import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";
import {
    authenticatedApiRequest,
} from "@/infrastructure/api/authenticatedApi";

const BRANDS_PATH =
    "/api/v1/brands";

const DEFAULT_BRAND_LIST_LIMIT =
    200;

function normalizeSearch(
    search: string | undefined,
): string | null {
    if (search === undefined) {
        return null;
    }

    const normalized =
        search.trim();

    return normalized.length > 0
        ? normalized
        : null;
}

function buildBrandListPath({
    includeInactive = false,
    search,
    limit = DEFAULT_BRAND_LIST_LIMIT,
    offset = 0,
}: BrandListFilters = {}): string {
    const params =
        new URLSearchParams();

    if (includeInactive) {
        params.set(
            "include_inactive",
            "true",
        );
    }

    const normalizedSearch =
        normalizeSearch(search);

    if (normalizedSearch !== null) {
        params.set(
            "search",
            normalizedSearch,
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

    return `${BRANDS_PATH}?${params.toString()}`;
}

export function listBrands(
    context: AuthenticatedApiContext,
    filters: BrandListFilters = {},
): Promise<readonly Brand[]> {
    return authenticatedApiRequest<
        Brand[]
    >(
        buildBrandListPath(filters),
        context,
        {
            method: "GET",
        },
    );
}