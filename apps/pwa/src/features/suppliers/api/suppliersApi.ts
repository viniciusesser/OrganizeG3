import type {
    Supplier,
    SupplierCreateInput,
    SupplierListFilters,
    SupplierPage,
    SupplierUpdateInput,
} from "@/features/suppliers/model/supplier";
import {
    DEFAULT_SUPPLIER_PAGE_SIZE,
} from "@/features/suppliers/model/supplier";
import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";
import {
    authenticatedApiRequest,
} from "@/infrastructure/api/authenticatedApi";

const SUPPLIERS_PATH =
    "/api/v1/suppliers";

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

function buildSupplierListPath({
    includeInactive = false,
    search,
    limit = DEFAULT_SUPPLIER_PAGE_SIZE,
    offset = 0,
}: SupplierListFilters = {}): string {
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

    return `${SUPPLIERS_PATH}?${params.toString()}`;
}

export function listSuppliers(
    context: AuthenticatedApiContext,
    filters: SupplierListFilters = {},
): Promise<readonly Supplier[]> {
    return authenticatedApiRequest<
        Supplier[]
    >(
        buildSupplierListPath(filters),
        context,
        {
            method: "GET",
        },
    );
}

export async function listSupplierPage(
    context: AuthenticatedApiContext,
    filters: SupplierListFilters = {},
): Promise<SupplierPage> {
    const pageSize =
        filters.limit ??
        DEFAULT_SUPPLIER_PAGE_SIZE;

    const offset =
        filters.offset ?? 0;

    const items =
        await listSuppliers(
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
            ? items.slice(0, pageSize)
            : items,
        hasPrevious: offset > 0,
        hasNext,
        offset,
        pageSize,
    };
}

export function getSupplier(
    context: AuthenticatedApiContext,
    supplierId: string,
): Promise<Supplier> {
    return authenticatedApiRequest<Supplier>(
        `${SUPPLIERS_PATH}/${supplierId}`,
        context,
        {
            method: "GET",
        },
    );
}

export function createSupplier(
    context: AuthenticatedApiContext,
    payload: SupplierCreateInput,
): Promise<Supplier> {
    return authenticatedApiRequest<Supplier>(
        SUPPLIERS_PATH,
        context,
        {
            method: "POST",
            body: payload,
        },
    );
}

export function updateSupplier(
    context: AuthenticatedApiContext,
    supplierId: string,
    payload: SupplierUpdateInput,
): Promise<Supplier> {
    return authenticatedApiRequest<Supplier>(
        `${SUPPLIERS_PATH}/${supplierId}`,
        context,
        {
            method: "PATCH",
            body: payload,
        },
    );
}

export function deactivateSupplier(
    context: AuthenticatedApiContext,
    supplierId: string,
): Promise<Supplier> {
    return authenticatedApiRequest<Supplier>(
        `${SUPPLIERS_PATH}/${supplierId}/deactivate`,
        context,
        {
            method: "POST",
        },
    );
}

export function reactivateSupplier(
    context: AuthenticatedApiContext,
    supplierId: string,
): Promise<Supplier> {
    return authenticatedApiRequest<Supplier>(
        `${SUPPLIERS_PATH}/${supplierId}/reactivate`,
        context,
        {
            method: "POST",
        },
    );
}