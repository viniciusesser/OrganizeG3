import {
    buildBearerHeaders,
} from "@/infrastructure/api/bearerApi";
import {
    apiRequest,
} from "@/infrastructure/api/httpClient";
import type {
    ApiRequestOptions,
} from "@/infrastructure/api/httpClient";

export const TENANT_HEADER =
    "X-Tenant-ID";

export const BRANCH_HEADER =
    "X-Branch-ID";

export interface AuthenticatedApiContext {
    readonly accessToken: string;
    readonly tenantId: string;
    readonly branchId?: string | null;
}

function requireContextValue(
    value: string,
    fieldName: string,
): string {
    const normalized = value.trim();

    if (normalized.length === 0) {
        throw new Error(
            `${fieldName} não pode ser vazio.`,
        );
    }

    return normalized;
}

export function buildAuthenticatedHeaders(
    context: AuthenticatedApiContext,
    initialHeaders?: HeadersInit,
): Headers {
    const tenantId =
        requireContextValue(
            context.tenantId,
            "tenantId",
        );

    const headers =
        buildBearerHeaders(
            context.accessToken,
            initialHeaders,
        );

    headers.set(
        TENANT_HEADER,
        tenantId,
    );

    if (
        context.branchId !== undefined &&
        context.branchId !== null
    ) {
        const branchId =
            requireContextValue(
                context.branchId,
                "branchId",
            );

        headers.set(
            BRANCH_HEADER,
            branchId,
        );
    } else {
        headers.delete(
            BRANCH_HEADER,
        );
    }

    return headers;
}

export async function authenticatedApiRequest<
    TResponse,
>(
    path: string,
    context: AuthenticatedApiContext,
    options: ApiRequestOptions = {},
): Promise<TResponse> {
    const headers =
        buildAuthenticatedHeaders(
            context,
            options.headers,
        );

    return apiRequest<TResponse>(
        path,
        {
            ...options,
            headers,
        },
    );
}