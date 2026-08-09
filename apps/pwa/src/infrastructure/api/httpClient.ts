import {
    ApiError,
    isApiErrorEnvelope,
} from "@/infrastructure/api/apiError";
import {
    createCorrelationId,
    getCorrelationIdHeaderName,
} from "@/infrastructure/api/correlationId";
import {
    environment,
} from "@/infrastructure/environment/environment";

export interface ApiRequestOptions
    extends Omit<RequestInit, "body"> {
    readonly body?: unknown;
}

function buildUrl(
    path: string,
): string {
    const normalizedPath =
        path.startsWith("/")
            ? path
            : `/${path}`;

    return `${environment.apiBaseUrl}${normalizedPath}`;
}

function buildHeaders(
    headers?: HeadersInit,
): Headers {
    const result =
        new Headers(headers);

    if (!result.has("Accept")) {
        result.set(
            "Accept",
            "application/json",
        );
    }

    if (
        !result.has(
            getCorrelationIdHeaderName(),
        )
    ) {
        result.set(
            getCorrelationIdHeaderName(),
            createCorrelationId(),
        );
    }

    return result;
}

function serializeBody(
    body: unknown,
    headers: Headers,
): BodyInit | undefined {
    if (body === undefined) {
        return undefined;
    }

    if (
        body instanceof FormData ||
        body instanceof Blob ||
        body instanceof URLSearchParams ||
        typeof body === "string"
    ) {
        return body;
    }

    if (!headers.has("Content-Type")) {
        headers.set(
            "Content-Type",
            "application/json",
        );
    }

    return JSON.stringify(body);
}

async function readResponseBody(
    response: Response,
): Promise<unknown> {
    if (response.status === 204) {
        return null;
    }

    const contentType =
        response.headers.get(
            "content-type",
        ) ?? "";

    if (
        contentType.includes(
            "application/json",
        )
    ) {
        return response.json();
    }

    const text =
        await response.text();

    return text.length > 0
        ? text
        : null;
}

function getResponseCorrelationId(
    response: Response,
    body: unknown,
): string | null {
    const headerCorrelationId =
        response.headers.get(
            getCorrelationIdHeaderName(),
        );

    if (
        headerCorrelationId !== null
    ) {
        return headerCorrelationId;
    }

    if (
        isApiErrorEnvelope(body) &&
        typeof body.meta
            ?.correlation_id === "string"
    ) {
        return body.meta.correlation_id;
    }

    return null;
}

function createApiError(
    response: Response,
    body: unknown,
): ApiError {
    const correlationId =
        getResponseCorrelationId(
            response,
            body,
        );

    if (isApiErrorEnvelope(body)) {
        return new ApiError({
            status: response.status,
            code: body.error.code,
            message: body.error.message,
            details: body.error.details,
            correlationId,
        });
    }

    return new ApiError({
        status: response.status,
        code: "unexpected_api_error",
        message:
            `A API respondeu com HTTP ${response.status}.`,
        details: body,
        correlationId,
    });
}

export async function apiRequest<
    TResponse,
>(
    path: string,
    options: ApiRequestOptions = {},
): Promise<TResponse> {
    const headers =
        buildHeaders(
            options.headers,
        );

    const body =
        serializeBody(
            options.body,
            headers,
        );

    let response: Response;

    try {
        response = await fetch(
            buildUrl(path),
            {
                ...options,
                headers,
                body,
            },
        );
    } catch (error) {
        throw new ApiError({
            status: 0,
            code: "network_error",
            message:
                "Não foi possível estabelecer comunicação com a API.",
            details:
                error instanceof Error
                    ? error.message
                    : null,
        });
    }

    const responseBody =
        await readResponseBody(
            response,
        );

    if (!response.ok) {
        throw createApiError(
            response,
            responseBody,
        );
    }

    return responseBody as TResponse;
}