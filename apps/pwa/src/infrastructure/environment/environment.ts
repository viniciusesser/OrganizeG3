const DEFAULT_API_BASE_URL = "/api";

export interface ApplicationEnvironment {
    readonly apiBaseUrl: string;
    readonly supabaseUrl: string | null;
    readonly supabaseAnonKey: string | null;
    readonly isDevelopment: boolean;
    readonly isProduction: boolean;
    readonly mode: string;
}

export interface ApplicationEnvironmentSource {
    readonly apiBaseUrl?: string;
    readonly supabaseUrl?: string;
    readonly supabaseAnonKey?: string;
    readonly isDevelopment: boolean;
    readonly isProduction: boolean;
    readonly mode: string;
}

export interface SupabaseBrowserConfiguration {
    readonly url: string;
    readonly anonKey: string;
}

function normalizeApiBaseUrl(
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

function normalizeOptionalValue(
    value: string | undefined,
): string | null {
    if (value === undefined) {
        return null;
    }

    const normalized = value.trim();

    return normalized.length > 0
        ? normalized
        : null;
}

export function createApplicationEnvironment(
    source: ApplicationEnvironmentSource,
): ApplicationEnvironment {
    return Object.freeze({
        apiBaseUrl: normalizeApiBaseUrl(
            source.apiBaseUrl,
        ),
        supabaseUrl: normalizeOptionalValue(
            source.supabaseUrl,
        ),
        supabaseAnonKey: normalizeOptionalValue(
            source.supabaseAnonKey,
        ),
        isDevelopment:
            source.isDevelopment,
        isProduction:
            source.isProduction,
        mode:
            source.mode,
    });
}

export function requireSupabaseBrowserConfiguration(
    source: ApplicationEnvironment =
        environment,
): SupabaseBrowserConfiguration {
    if (
        source.supabaseUrl === null ||
        source.supabaseAnonKey === null
    ) {
        throw new Error(
            "A configuração pública do Supabase não foi definida.",
        );
    }

    return Object.freeze({
        url: source.supabaseUrl,
        anonKey: source.supabaseAnonKey,
    });
}

export const environment =
    createApplicationEnvironment({
        apiBaseUrl:
            import.meta.env.VITE_API_BASE_URL,
        supabaseUrl:
            import.meta.env.VITE_SUPABASE_URL,
        supabaseAnonKey:
            import.meta.env.VITE_SUPABASE_ANON_KEY,
        isDevelopment:
            import.meta.env.DEV,
        isProduction:
            import.meta.env.PROD,
        mode:
            import.meta.env.MODE,
    });