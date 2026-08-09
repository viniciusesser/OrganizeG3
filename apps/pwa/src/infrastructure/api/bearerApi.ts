import {
    apiRequest,
} from "@/infrastructure/api/httpClient";
import type {
    ApiRequestOptions,
} from "@/infrastructure/api/httpClient";

export const AUTHORIZATION_HEADER =
    "Authorization";

function requireAccessToken(
    accessToken: string,
): string {
    const normalized =
        accessToken.trim();

    if (normalized.length === 0) {
        throw new Error(
            "accessToken não pode ser vazio.",
        );
    }

    return normalized;
}

export function buildBearerHeaders(
    accessToken: string,
    initialHeaders?: HeadersInit,
): Headers {
    const token =
        requireAccessToken(
            accessToken,
        );

    const headers =
        new Headers(initialHeaders);

    headers.set(
        AUTHORIZATION_HEADER,
        `Bearer ${token}`,
    );

    return headers;
}

export async function bearerApiRequest<
    TResponse,
>(
    path: string,
    accessToken: string,
    options: ApiRequestOptions = {},
): Promise<TResponse> {
    const headers =
        buildBearerHeaders(
            accessToken,
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