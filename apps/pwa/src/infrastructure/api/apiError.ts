export interface ApiErrorBody {
    readonly code: string;
    readonly message: string;
    readonly details: unknown;
}

export interface ApiErrorMeta {
    readonly correlation_id?: string;
}

export interface ApiErrorEnvelope {
    readonly success: false;
    readonly error: ApiErrorBody;
    readonly meta?: ApiErrorMeta;
}

export class ApiError extends Error {
    public readonly status: number;
    public readonly code: string;
    public readonly details: unknown;
    public readonly correlationId: string | null;

    public constructor({
        status,
        code,
        message,
        details = null,
        correlationId = null,
    }: {
        readonly status: number;
        readonly code: string;
        readonly message: string;
        readonly details?: unknown;
        readonly correlationId?: string | null;
    }) {
        super(message);

        this.name = "ApiError";
        this.status = status;
        this.code = code;
        this.details = details;
        this.correlationId = correlationId;
    }
}

export function isApiErrorEnvelope(
    value: unknown,
): value is ApiErrorEnvelope {
    if (
        typeof value !== "object" ||
        value === null
    ) {
        return false;
    }

    const candidate = value as Record<string, unknown>;

    if (candidate.success !== false) {
        return false;
    }

    if (
        typeof candidate.error !== "object" ||
        candidate.error === null
    ) {
        return false;
    }

    const error = candidate.error as Record<string, unknown>;

    return (
        typeof error.code === "string" &&
        typeof error.message === "string"
    );
}