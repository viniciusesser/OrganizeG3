export type EmploymentStatus =
    | "ACTIVE"
    | "ON_LEAVE"
    | "INACTIVE"
    | "TERMINATED";

export interface Employee {
    readonly id: string;
    readonly tenant_id: string;
    readonly branch_id: string | null;
    readonly code: string;
    readonly full_name: string;
    readonly document_number: string | null;
    readonly email: string | null;
    readonly phone: string | null;
    readonly job_title: string | null;
    readonly contract_type: string | null;
    readonly status: EmploymentStatus;
    readonly birth_date: string | null;
    readonly admission_date: string | null;
    readonly termination_date: string | null;
    readonly is_active: boolean;
    readonly created_at: string | null;
    readonly updated_at: string | null;
}

export interface EmployeeCreateInput {
    readonly code: string;
    readonly full_name: string;
    readonly branch_id?: string | null;
    readonly document_number?: string | null;
    readonly email?: string | null;
    readonly phone?: string | null;
    readonly job_title?: string | null;
    readonly contract_type?: string | null;
    readonly birth_date?: string | null;
    readonly admission_date?: string | null;
}

export interface EmployeeUpdateInput {
    readonly code?: string;
    readonly full_name?: string;
    readonly branch_id?: string | null;
    readonly document_number?: string | null;
    readonly email?: string | null;
    readonly phone?: string | null;
    readonly job_title?: string | null;
    readonly contract_type?: string | null;
    readonly birth_date?: string | null;
    readonly admission_date?: string | null;
}

export interface EmployeeListFilters {
    readonly includeInactive?: boolean;
    readonly search?: string;
    readonly branchId?: string | null;
    readonly status?: EmploymentStatus | null;
    readonly limit?: number;
    readonly offset?: number;
}

export interface EmployeePage {
    readonly items: readonly Employee[];
    readonly hasPrevious: boolean;
    readonly hasNext: boolean;
    readonly offset: number;
    readonly pageSize: number;
}

export const DEFAULT_EMPLOYEE_PAGE_SIZE = 20;

export const EMPLOYMENT_STATUSES: readonly EmploymentStatus[] = [
    "ACTIVE",
    "ON_LEAVE",
    "INACTIVE",
    "TERMINATED",
];

export const EMPLOYMENT_STATUS_LABELS: Readonly<
    Record<EmploymentStatus, string>
> = {
    ACTIVE: "Ativo",
    ON_LEAVE: "Afastado",
    INACTIVE: "Inativo",
    TERMINATED: "Desligado",
};

export function getEmploymentStatusLabel(
    status: EmploymentStatus,
): string {
    return EMPLOYMENT_STATUS_LABELS[status];
}