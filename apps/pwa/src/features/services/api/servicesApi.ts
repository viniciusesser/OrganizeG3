import type {
    Service,
    ServiceCreateInput,
    ServiceListFilters,
    ServicePage,
    ServiceUpdateInput,
} from "@/features/services/model/service";
import {
    DEFAULT_SERVICE_PAGE_SIZE,
} from "@/features/services/model/service";
import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";
import {
    authenticatedApiRequest,
} from "@/infrastructure/api/authenticatedApi";

const SERVICES_PATH =
    "/api/v1/services";

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

function buildServiceListPath(
    filters: ServiceListFilters,
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

    appendNormalizedText(
        params,
        "category",
        filters.category,
    );

    if (
        filters.executionMode !==
        undefined &&
        filters.executionMode !== null
    ) {
        params.set(
            "execution_mode",
            filters.executionMode,
        );
    }

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
        `${SERVICES_PATH}?` +
        params.toString()
    );
}

export async function listServices(
    context: AuthenticatedApiContext,
    filters: ServiceListFilters = {},
): Promise<readonly Service[]> {
    return authenticatedApiRequest<
        Service[]
    >(
        buildServiceListPath(
            filters,
        ),
        context,
        {
            method: "GET",
        },
    );
}

export async function listServicePage(
    context: AuthenticatedApiContext,
    filters: ServiceListFilters = {},
): Promise<ServicePage> {
    const pageSize =
        filters.limit ??
        DEFAULT_SERVICE_PAGE_SIZE;

    const offset =
        filters.offset ?? 0;

    const loadedItems =
        await listServices(
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

export async function getService(
    context: AuthenticatedApiContext,
    serviceId: string,
): Promise<Service> {
    return authenticatedApiRequest<
        Service
    >(
        `${SERVICES_PATH}/${serviceId}`,
        context,
        {
            method: "GET",
        },
    );
}

export async function createService(
    context: AuthenticatedApiContext,
    payload: ServiceCreateInput,
): Promise<Service> {
    return authenticatedApiRequest<
        Service
    >(
        SERVICES_PATH,
        context,
        {
            method: "POST",
            body: payload,
        },
    );
}

export async function updateService(
    context: AuthenticatedApiContext,
    serviceId: string,
    payload: ServiceUpdateInput,
): Promise<Service> {
    return authenticatedApiRequest<
        Service
    >(
        `${SERVICES_PATH}/${serviceId}`,
        context,
        {
            method: "PATCH",
            body: payload,
        },
    );
}

export async function deactivateService(
    context: AuthenticatedApiContext,
    serviceId: string,
): Promise<Service> {
    return authenticatedApiRequest<
        Service
    >(
        `${SERVICES_PATH}/${serviceId}/deactivate`,
        context,
        {
            method: "POST",
        },
    );
}

export async function reactivateService(
    context: AuthenticatedApiContext,
    serviceId: string,
): Promise<Service> {
    return authenticatedApiRequest<
        Service
    >(
        `${SERVICES_PATH}/${serviceId}/reactivate`,
        context,
        {
            method: "POST",
        },
    );
}