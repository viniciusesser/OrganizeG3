const DEFAULT_API_BASE_URL = "/api";

export interface ApplicationEnvironment {
    readonly apiBaseUrl: string;
    readonly isDevelopment: boolean;
    readonly isProduction: boolean;
    readonly mode: string;
}

export interface ApplicationEnvironmentSource {
    readonly apiBaseUrl?: string;
    readonly isDevelopment: boolean;
    readonly isProduction: boolean;
    readonly mode: string;
}

function normalizeBaseUrl(
    value: string | undefined,
): string {
    if (value === undefined) {
        return DEFAULT_API_BASE_URL;
    }

    const normalized = value.trim();

    if (normalized.length === 0) {
        return DEFAULT_API_BASE_URL;
    }

    return normalized.replace(/\/+$/, "");
}

export function createApplicationEnvironment(
    source: ApplicationEnvironmentSource,
): ApplicationEnvironment {
    return Object.freeze({
        apiBaseUrl: normalizeBaseUrl(
            source.apiBaseUrl,
        ),
        isDevelopment:
            source.isDevelopment,
        isProduction:
            source.isProduction,
        mode: source.mode,
    });
}

export const environment =
    createApplicationEnvironment({
        apiBaseUrl:
            import.meta.env.VITE_API_BASE_URL,
        isDevelopment:
            import.meta.env.DEV,
        isProduction:
            import.meta.env.PROD,
        mode:
            import.meta.env.MODE,
    });