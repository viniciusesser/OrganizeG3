export type MachineStatus =
    | "AVAILABLE"
    | "IN_USE"
    | "MAINTENANCE"
    | "OUT_OF_SERVICE";

export interface Machine {
    readonly id: string;
    readonly tenant_id: string;
    readonly code: string;
    readonly name: string;
    readonly machine_type: string;
    readonly status: MachineStatus;
    readonly branch_id: string | null;
    readonly manufacturer: string | null;
    readonly model: string | null;
    readonly serial_number: string | null;
    readonly is_active: boolean;
    readonly created_at: string;
    readonly updated_at: string;
}

export interface MachineCreateInput {
    readonly code: string;
    readonly name: string;
    readonly machine_type: string;
    readonly branch_id?: string | null;
    readonly manufacturer?: string | null;
    readonly model?: string | null;
    readonly serial_number?: string | null;
}

export type MachineUpdateInput = MachineCreateInput;

export interface MachineListFilters {
    readonly includeInactive?: boolean;
    readonly search?: string;
    readonly machineType?: string;
    readonly status?: MachineStatus | null;
    readonly branchId?: string;
    readonly limit?: number;
    readonly offset?: number;
}

export interface MachinePage {
    readonly items: readonly Machine[];
    readonly hasPrevious: boolean;
    readonly hasNext: boolean;
    readonly offset: number;
    readonly pageSize: number;
}

export const DEFAULT_MACHINE_PAGE_SIZE = 20;

export const MACHINE_STATUSES: readonly MachineStatus[] = [
    "AVAILABLE",
    "IN_USE",
    "MAINTENANCE",
    "OUT_OF_SERVICE",
];

export const MACHINE_STATUS_LABELS: Readonly<
    Record<MachineStatus, string>
> = {
    AVAILABLE: "Disponível",
    IN_USE: "Em uso",
    MAINTENANCE: "Em manutenção",
    OUT_OF_SERVICE: "Fora de serviço",
};

export function getMachineStatusLabel(
    status: MachineStatus,
): string {
    return MACHINE_STATUS_LABELS[status];
}