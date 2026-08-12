export type ServiceExecutionMode =
    | "INTERNAL"
    | "EXTERNAL"
    | "BOTH";

export interface Service {
    readonly id: string;
    readonly tenant_id: string;
    readonly code: string;
    readonly name: string;
    readonly category: string;
    readonly unit: string;
    readonly execution_mode:
    ServiceExecutionMode;
    readonly estimated_duration_minutes:
    number | null;
    readonly is_active: boolean;
    readonly created_at: string;
    readonly updated_at: string;
}

export interface ServiceCreateInput {
    readonly code: string;
    readonly name: string;
    readonly category: string;
    readonly unit: string;
    readonly execution_mode:
    ServiceExecutionMode;
    readonly estimated_duration_minutes?:
    number | null;
}

export interface ServiceUpdateInput {
    readonly code?: string;
    readonly name?: string;
    readonly category?: string;
    readonly unit?: string;
    readonly execution_mode?:
    ServiceExecutionMode;
    readonly estimated_duration_minutes?:
    number | null;
}

export interface ServiceListFilters {
    readonly includeInactive?: boolean;
    readonly search?: string;
    readonly category?: string;
    readonly executionMode?:
    ServiceExecutionMode | null;
    readonly limit?: number;
    readonly offset?: number;
}

export interface ServicePage {
    readonly items:
    readonly Service[];
    readonly hasPrevious: boolean;
    readonly hasNext: boolean;
    readonly offset: number;
    readonly pageSize: number;
}

export const DEFAULT_SERVICE_PAGE_SIZE =
    20;

export const SERVICE_EXECUTION_MODES:
    readonly ServiceExecutionMode[] = [
        "INTERNAL",
        "EXTERNAL",
        "BOTH",
    ];

export const SERVICE_EXECUTION_MODE_LABELS:
    Readonly<
        Record<
            ServiceExecutionMode,
            string
        >
    > = {
    INTERNAL: "Interno",
    EXTERNAL: "Terceirizado",
    BOTH: "Interno ou terceirizado",
};

export function getServiceExecutionModeLabel(
    executionMode:
        ServiceExecutionMode,
): string {
    return SERVICE_EXECUTION_MODE_LABELS[
        executionMode
    ];
}