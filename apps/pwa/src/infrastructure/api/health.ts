import {
    apiRequest,
} from "@/infrastructure/api/httpClient";
import type {
    HealthResponse,
} from "@/shared/types/health";

export function getApiHealth(): Promise<HealthResponse> {
    return apiRequest<HealthResponse>(
        "/health",
        {
            method: "GET",
            useApiBaseUrl: false,
        },
    );
}