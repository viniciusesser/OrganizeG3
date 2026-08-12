import type {
    Brand,
    BrandCreateInput,
    BrandListFilters,
    BrandPage,
    BrandUpdateInput,
} from "@/features/brands/model/brand";
import {
    DEFAULT_BRAND_PAGE_SIZE,
} from "@/features/brands/model/brand";
import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";
import {
    authenticatedApiRequest,
} from "@/infrastructure/api/authenticatedApi";

const BRANDS_PATH =
    "/api/v1/brands";

function appendNormalizedText(
    params: URLSearchParams,
    name: string,
    value: string | undefined,
): void {
    const normalizedValue =
        value?.trim() ?? "";

    if (normalizedValue.length > 0) {
        params.set(
            name,
            normalizedValue,
        );
    }
}

function buildBrandListPath(
    filters: BrandListFilters,
): string {
    const params =
        new URLSearchParams();

    params.set(
        "include_inactive",
        String(
            filters.includeInactive ??
            false,
        ),
    );

    appendNormalizedText(
        params,
        "search",
        filters.search,
    );

    if (filters.limit !== undefined) {
        params.set(
            "limit",
            String(filters.limit),
        );
    }

    if (filters.offset !== undefined) {
        params.set(
            "offset",
            String(filters.offset),
        );
    }

    return (
        `${BRANDS_PATH}?` +
        params.toString()
    );
}

export async function listBrands(
    context: AuthenticatedApiContext,
    filters: BrandListFilters = {},
): Promise<readonly Brand[]> {
    return authenticatedApiRequest<
        Brand[]
    >(
        buildBrandListPath(
            filters,
        ),
        context,
        {
            method: "GET",
        },
    );
}

export async function listBrandPage(
    context: AuthenticatedApiContext,
    filters: BrandListFilters = {},
): Promise<BrandPage> {
    const pageSize =
        filters.limit ??
        DEFAULT_BRAND_PAGE_SIZE;

    const offset =
        filters.offset ?? 0;

    const loadedItems =
        await listBrands(
            context,
            {
                ...filters,
                limit:
                    pageSize + 1,
                offset,
            },
        );

    const hasNext =
        loadedItems.length >
        pageSize;

    const items =
        hasNext
            ? loadedItems.slice(
                0,
                pageSize,
            )
            : loadedItems;

    return {
        items,
        hasPrevious:
            offset > 0,
        hasNext,
        offset,
        pageSize,
    };
}

export async function getBrand(
    context: AuthenticatedApiContext,
    brandId: string,
): Promise<Brand> {
    return authenticatedApiRequest<
        Brand
    >(
        `${BRANDS_PATH}/${brandId}`,
        context,
        {
            method: "GET",
        },
    );
}

export async function createBrand(
    context: AuthenticatedApiContext,
    payload: BrandCreateInput,
): Promise<Brand> {
    return authenticatedApiRequest<
        Brand
    >(
        BRANDS_PATH,
        context,
        {
            method: "POST",
            body: payload,
        },
    );
}

export async function updateBrand(
    context: AuthenticatedApiContext,
    brandId: string,
    payload: BrandUpdateInput,
): Promise<Brand> {
    return authenticatedApiRequest<
        Brand
    >(
        `${BRANDS_PATH}/${brandId}`,
        context,
        {
            method: "PATCH",
            body: payload,
        },
    );
}

export async function deactivateBrand(
    context: AuthenticatedApiContext,
    brandId: string,
): Promise<Brand> {
    return authenticatedApiRequest<
        Brand
    >(
        `${BRANDS_PATH}/${brandId}/deactivate`,
        context,
        {
            method: "POST",
        },
    );
}

export async function reactivateBrand(
    context: AuthenticatedApiContext,
    brandId: string,
): Promise<Brand> {
    return authenticatedApiRequest<
        Brand
    >(
        `${BRANDS_PATH}/${brandId}/reactivate`,
        context,
        {
            method: "POST",
        },
    );
}