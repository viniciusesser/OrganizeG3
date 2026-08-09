const CORRELATION_ID_HEADER = "X-Correlation-ID";

export function createCorrelationId(): string {
    return crypto.randomUUID();
}

export function getCorrelationIdHeaderName(): string {
    return CORRELATION_ID_HEADER;
}