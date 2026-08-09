export interface HealthResponse {
    readonly status: string;
    readonly service: string;
    readonly version: string;
}