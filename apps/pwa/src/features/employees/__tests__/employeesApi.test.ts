import {
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    createEmployee,
    deactivateEmployee,
    getEmployee,
    listEmployeePage,
    listEmployees,
    reactivateEmployee,
    updateEmployee,
} from "@/features/employees/api/employeesApi";
import type {
    Employee,
    EmployeeCreateInput,
    EmployeeUpdateInput,
} from "@/features/employees/model/employee";
import {
    authenticatedApiRequest,
} from "@/infrastructure/api/authenticatedApi";

vi.mock(
    "@/infrastructure/api/authenticatedApi",
    () => ({
        authenticatedApiRequest:
            vi.fn(),
    }),
);

const requestMock =
    vi.mocked(
        authenticatedApiRequest,
    );

const apiContext = {
    accessToken:
        "access-token",
    tenantId:
        "tenant-001",
};

const employee: Employee = {
    id:
        "employee-001",
    tenant_id:
        "tenant-001",
    branch_id:
        "branch-001",
    code:
        "FUN-001",
    full_name:
        "João da Silva",
    document_number:
        "12345678901",
    email:
        "joao@empresa.com.br",
    phone:
        "18999998888",
    job_title:
        "Marceneiro",
    contract_type:
        "CLT",
    status:
        "ACTIVE",
    birth_date:
        "1990-05-10",
    admission_date:
        "2025-01-15",
    termination_date:
        null,
    is_active:
        true,
    created_at:
        "2026-08-11T10:00:00Z",
    updated_at:
        "2026-08-11T10:00:00Z",
};

describe(
    "employeesApi",
    () => {
        beforeEach(() => {
            vi.clearAllMocks();

            requestMock
                .mockResolvedValue(
                    employee,
                );
        });

        it(
            "lista funcionários com os filtros padrão",
            async () => {
                requestMock
                    .mockResolvedValue([
                        employee,
                    ]);

                await expect(
                    listEmployees(
                        apiContext,
                    ),
                ).resolves.toEqual([
                    employee,
                ]);

                expect(
                    requestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/employees?include_inactive=false",
                    apiContext,
                    {
                        method:
                            "GET",
                    },
                );
            },
        );

        it(
            "lista funcionários com filtros normalizados",
            async () => {
                requestMock
                    .mockResolvedValue([
                        employee,
                    ]);

                await listEmployees(
                    apiContext,
                    {
                        includeInactive:
                            true,
                        search:
                            "  João  ",
                        branchId:
                            "branch-001",
                        status:
                            "ACTIVE",
                        limit:
                            25,
                        offset:
                            50,
                    },
                );

                expect(
                    requestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/employees?include_inactive=true&search=Jo%C3%A3o&branch_id=branch-001&status=ACTIVE&limit=25&offset=50",
                    apiContext,
                    {
                        method:
                            "GET",
                    },
                );
            },
        );

        it(
            "ignora pesquisa vazia e filtros nulos",
            async () => {
                requestMock
                    .mockResolvedValue([]);

                await listEmployees(
                    apiContext,
                    {
                        search:
                            "   ",
                        branchId:
                            null,
                        status:
                            null,
                    },
                );

                expect(
                    requestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/employees?include_inactive=false",
                    apiContext,
                    {
                        method:
                            "GET",
                    },
                );
            },
        );

        it(
            "monta uma página e identifica registros seguintes",
            async () => {
                const secondEmployee: Employee = {
                    ...employee,
                    id:
                        "employee-002",
                    code:
                        "FUN-002",
                    full_name:
                        "Maria Oliveira",
                };

                const extraEmployee: Employee = {
                    ...employee,
                    id:
                        "employee-003",
                    code:
                        "FUN-003",
                    full_name:
                        "Carlos Souza",
                };

                requestMock
                    .mockResolvedValue([
                        employee,
                        secondEmployee,
                        extraEmployee,
                    ]);

                await expect(
                    listEmployeePage(
                        apiContext,
                        {
                            limit:
                                2,
                            offset:
                                20,
                        },
                    ),
                ).resolves.toEqual({
                    items: [
                        employee,
                        secondEmployee,
                    ],
                    hasPrevious:
                        true,
                    hasNext:
                        true,
                    offset:
                        20,
                    pageSize:
                        2,
                });

                expect(
                    requestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/employees?include_inactive=false&limit=3&offset=20",
                    apiContext,
                    {
                        method:
                            "GET",
                    },
                );
            },
        );

        it(
            "consulta um funcionário por identificador",
            async () => {
                await expect(
                    getEmployee(
                        apiContext,
                        employee.id,
                    ),
                ).resolves.toEqual(
                    employee,
                );

                expect(
                    requestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/employees/employee-001",
                    apiContext,
                    {
                        method:
                            "GET",
                    },
                );
            },
        );

        it(
            "cadastra um funcionário",
            async () => {
                const payload:
                    EmployeeCreateInput = {
                    code:
                        "FUN-001",
                    full_name:
                        "João da Silva",
                    branch_id:
                        "branch-001",
                    document_number:
                        "12345678901",
                    email:
                        "joao@empresa.com.br",
                    phone:
                        "18999998888",
                    job_title:
                        "Marceneiro",
                    contract_type:
                        "CLT",
                    birth_date:
                        "1990-05-10",
                    admission_date:
                        "2025-01-15",
                };

                await expect(
                    createEmployee(
                        apiContext,
                        payload,
                    ),
                ).resolves.toEqual(
                    employee,
                );

                expect(
                    requestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/employees",
                    apiContext,
                    {
                        method:
                            "POST",
                        body:
                            payload,
                    },
                );
            },
        );

        it(
            "atualiza parcialmente um funcionário",
            async () => {
                const payload:
                    EmployeeUpdateInput = {
                    full_name:
                        "João da Silva Atualizado",
                    phone:
                        "18988887777",
                    branch_id:
                        null,
                };

                await updateEmployee(
                    apiContext,
                    employee.id,
                    payload,
                );

                expect(
                    requestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/employees/employee-001",
                    apiContext,
                    {
                        method:
                            "PATCH",
                        body:
                            payload,
                    },
                );
            },
        );

        it(
            "inativa e reativa um funcionário",
            async () => {
                await deactivateEmployee(
                    apiContext,
                    employee.id,
                );

                expect(
                    requestMock,
                ).toHaveBeenLastCalledWith(
                    "/api/v1/employees/employee-001/deactivate",
                    apiContext,
                    {
                        method:
                            "POST",
                    },
                );

                await reactivateEmployee(
                    apiContext,
                    employee.id,
                );

                expect(
                    requestMock,
                ).toHaveBeenLastCalledWith(
                    "/api/v1/employees/employee-001/reactivate",
                    apiContext,
                    {
                        method:
                            "POST",
                    },
                );
            },
        );
    },
);