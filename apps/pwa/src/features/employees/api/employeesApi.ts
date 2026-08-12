import type {
    Employee,
    EmployeeCreateInput,
    EmployeeListFilters,
    EmployeePage,
    EmployeeUpdateInput,
} from "@/features/employees/model/employee";
import {
    DEFAULT_EMPLOYEE_PAGE_SIZE,
} from "@/features/employees/model/employee";
import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";
import {
    authenticatedApiRequest,
} from "@/infrastructure/api/authenticatedApi";

const EMPLOYEES_PATH =
    "/api/v1/employees";

function appendNormalizedText(
    params: URLSearchParams,
    name: string,
    value: string | undefined,
): void {
    if (value === undefined) {
        return;
    }

    const normalized =
        value.trim();

    if (normalized.length === 0) {
        return;
    }

    params.set(
        name,
        normalized,
    );
}

function buildEmployeeListPath(
    filters: EmployeeListFilters,
): string {
    const params =
        new URLSearchParams();

    params.set(
        "include_inactive",
        String(
            filters.includeInactive ??
            false,
        ),
    );

    appendNormalizedText(
        params,
        "search",
        filters.search,
    );

    if (filters.branchId != null) {
        params.set(
            "branch_id",
            filters.branchId,
        );
    }

    if (filters.status != null) {
        params.set(
            "status",
            filters.status,
        );
    }

    if (filters.limit !== undefined) {
        params.set(
            "limit",
            String(filters.limit),
        );
    }

    if (filters.offset !== undefined) {
        params.set(
            "offset",
            String(filters.offset),
        );
    }

    return `${EMPLOYEES_PATH}?${params.toString()}`;
}

export async function listEmployees(
    context: AuthenticatedApiContext,
    filters: EmployeeListFilters = {},
): Promise<Employee[]> {
    return authenticatedApiRequest<
        Employee[]
    >(
        buildEmployeeListPath(
            filters,
        ),
        context,
        {
            method: "GET",
        },
    );
}

export async function listEmployeePage(
    context: AuthenticatedApiContext,
    filters: EmployeeListFilters = {},
): Promise<EmployeePage> {
    const pageSize =
        filters.limit ??
        DEFAULT_EMPLOYEE_PAGE_SIZE;

    const offset =
        filters.offset ?? 0;

    const loadedItems =
        await listEmployees(
            context,
            {
                ...filters,
                limit:
                    pageSize + 1,
                offset,
            },
        );

    const hasNext =
        loadedItems.length >
        pageSize;

    return {
        items:
            hasNext
                ? loadedItems.slice(
                    0,
                    pageSize,
                )
                : loadedItems,
        hasPrevious:
            offset > 0,
        hasNext,
        offset,
        pageSize,
    };
}

export async function getEmployee(
    context: AuthenticatedApiContext,
    employeeId: string,
): Promise<Employee> {
    return authenticatedApiRequest<
        Employee
    >(
        `${EMPLOYEES_PATH}/${employeeId}`,
        context,
        {
            method: "GET",
        },
    );
}

export async function createEmployee(
    context: AuthenticatedApiContext,
    payload: EmployeeCreateInput,
): Promise<Employee> {
    return authenticatedApiRequest<
        Employee
    >(
        EMPLOYEES_PATH,
        context,
        {
            method: "POST",
            body: payload,
        },
    );
}

export async function updateEmployee(
    context: AuthenticatedApiContext,
    employeeId: string,
    payload: EmployeeUpdateInput,
): Promise<Employee> {
    return authenticatedApiRequest<
        Employee
    >(
        `${EMPLOYEES_PATH}/${employeeId}`,
        context,
        {
            method: "PATCH",
            body: payload,
        },
    );
}

export async function deactivateEmployee(
    context: AuthenticatedApiContext,
    employeeId: string,
): Promise<Employee> {
    return authenticatedApiRequest<
        Employee
    >(
        `${EMPLOYEES_PATH}/${employeeId}/deactivate`,
        context,
        {
            method: "POST",
        },
    );
}

export async function reactivateEmployee(
    context: AuthenticatedApiContext,
    employeeId: string,
): Promise<Employee> {
    return authenticatedApiRequest<
        Employee
    >(
        `${EMPLOYEES_PATH}/${employeeId}/reactivate`,
        context,
        {
            method: "POST",
        },
    );
}