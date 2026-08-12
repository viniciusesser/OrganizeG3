import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";
import {
    authenticatedApiRequest,
} from "@/infrastructure/api/authenticatedApi";

import type {
    Customer,
    CustomerCreateInput,
    CustomerListFilters,
    CustomerPage,
    CustomerUpdateInput,
    CustomerVersionInput,
} from "@/features/customers/model/customer";
import {
    DEFAULT_CUSTOMER_PAGE_SIZE,
} from "@/features/customers/model/customer";

const CUSTOMERS_PATH =
    "/api/v1/customers";

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

function buildCustomerListPath({
    includeInactive = false,
    search,
    customerType = null,
    limit = DEFAULT_CUSTOMER_PAGE_SIZE,
    offset = 0,
}: CustomerListFilters = {}): string {
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

    if (customerType !== null) {
        params.set(
            "customer_type",
            customerType,
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

    return `${CUSTOMERS_PATH}?${params.toString()}`;
}

export function listCustomers(
    context: AuthenticatedApiContext,
    filters: CustomerListFilters = {},
): Promise<readonly Customer[]> {
    return authenticatedApiRequest<
        Customer[]
    >(
        buildCustomerListPath(filters),
        context,
        {
            method: "GET",
        },
    );
}

export async function listCustomerPage(
    context: AuthenticatedApiContext,
    filters: CustomerListFilters = {},
): Promise<CustomerPage> {
    const pageSize =
        filters.limit ??
        DEFAULT_CUSTOMER_PAGE_SIZE;

    const offset =
        filters.offset ?? 0;

    const requestedLimit =
        pageSize + 1;

    const items =
        await listCustomers(
            context,
            {
                ...filters,
                limit: requestedLimit,
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

export function getCustomer(
    context: AuthenticatedApiContext,
    customerId: number,
): Promise<Customer> {
    return authenticatedApiRequest<Customer>(
        `${CUSTOMERS_PATH}/${customerId}`,
        context,
        {
            method: "GET",
        },
    );
}

export function createCustomer(
    context: AuthenticatedApiContext,
    payload: CustomerCreateInput,
): Promise<Customer> {
    return authenticatedApiRequest<Customer>(
        CUSTOMERS_PATH,
        context,
        {
            method: "POST",
            body: payload,
        },
    );
}

export function updateCustomer(
    context: AuthenticatedApiContext,
    customerId: number,
    payload: CustomerUpdateInput,
): Promise<Customer> {
    return authenticatedApiRequest<Customer>(
        `${CUSTOMERS_PATH}/${customerId}`,
        context,
        {
            method: "PATCH",
            body: payload,
        },
    );
}

export function archiveCustomer(
    context: AuthenticatedApiContext,
    customerId: number,
    payload: CustomerVersionInput,
): Promise<Customer> {
    return authenticatedApiRequest<Customer>(
        `${CUSTOMERS_PATH}/${customerId}/archive`,
        context,
        {
            method: "POST",
            body: payload,
        },
    );
}

export function reactivateCustomer(
    context: AuthenticatedApiContext,
    customerId: number,
    payload: CustomerVersionInput,
): Promise<Customer> {
    return authenticatedApiRequest<Customer>(
        `${CUSTOMERS_PATH}/${customerId}/reactivate`,
        context,
        {
            method: "POST",
            body: payload,
        },
    );
}