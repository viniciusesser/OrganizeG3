import {
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    changeMachineStatus,
    createMachine,
    deactivateMachine,
    getMachine,
    listMachinePage,
    listMachines,
    reactivateMachine,
    updateMachine,
} from "@/features/machines/api/machinesApi";
import type {
    Machine,
    MachineCreateInput,
} from "@/features/machines/model/machine";
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

const machine: Machine = {
    id:
        "machine-001",
    tenant_id:
        "tenant-001",
    code:
        "SEQ-01",
    name:
        "Seccionadora principal",
    machine_type:
        "Seccionadora",
    status:
        "AVAILABLE",
    branch_id:
        null,
    manufacturer:
        "Homag",
    model:
        "HPP",
    serial_number:
        "SN-001",
    is_active:
        true,
    created_at:
        "2026-08-10T10:00:00Z",
    updated_at:
        "2026-08-10T10:00:00Z",
};

describe(
    "machinesApi",
    () => {
        beforeEach(
            () => {
                vi.clearAllMocks();
            },
        );

        it(
            "lista máquinas com filtros normalizados",
            async () => {
                requestMock
                    .mockResolvedValue([
                        machine,
                    ]);

                await listMachines(
                    apiContext,
                    {
                        includeInactive:
                            true,
                        search:
                            "  Seccionadora  ",
                        machineType:
                            "  Corte  ",
                        status:
                            "AVAILABLE",
                        branchId:
                            "  branch-001  ",
                        limit:
                            25,
                        offset:
                            50,
                    },
                );

                expect(
                    requestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/machines?include_inactive=true&search=Seccionadora&machine_type=Corte&branch_id=branch-001&status=AVAILABLE&limit=25&offset=50",
                    apiContext,
                    {
                        method:
                            "GET",
                    },
                );
            },
        );

        it(
            "constrói a página com um registro adicional",
            async () => {
                requestMock
                    .mockResolvedValue([
                        machine,
                        {
                            ...machine,
                            id:
                                "machine-002",
                        },
                        {
                            ...machine,
                            id:
                                "machine-003",
                        },
                    ]);

                await expect(
                    listMachinePage(
                        apiContext,
                        {
                            limit:
                                2,
                            offset:
                                2,
                        },
                    ),
                ).resolves.toMatchObject({
                    items: [
                        machine,
                        {
                            ...machine,
                            id:
                                "machine-002",
                        },
                    ],
                    hasPrevious:
                        true,
                    hasNext:
                        true,
                    offset:
                        2,
                    pageSize:
                        2,
                });
            },
        );

        it(
            "consulta, cadastra e atualiza uma máquina",
            async () => {
                const payload:
                    MachineCreateInput = {
                    code:
                        machine.code,
                    name:
                        machine.name,
                    machine_type:
                        machine.machine_type,
                    manufacturer:
                        machine.manufacturer,
                };

                requestMock
                    .mockResolvedValue(
                        machine,
                    );

                await getMachine(
                    apiContext,
                    machine.id,
                );

                expect(
                    requestMock,
                ).toHaveBeenLastCalledWith(
                    "/api/v1/machines/machine-001",
                    apiContext,
                    {
                        method:
                            "GET",
                    },
                );

                await createMachine(
                    apiContext,
                    payload,
                );

                expect(
                    requestMock,
                ).toHaveBeenLastCalledWith(
                    "/api/v1/machines",
                    apiContext,
                    {
                        method:
                            "POST",
                        body:
                            payload,
                    },
                );

                await updateMachine(
                    apiContext,
                    machine.id,
                    payload,
                );

                expect(
                    requestMock,
                ).toHaveBeenLastCalledWith(
                    "/api/v1/machines/machine-001",
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
            "altera status, inativa e reativa uma máquina",
            async () => {
                requestMock
                    .mockResolvedValue(
                        machine,
                    );

                await changeMachineStatus(
                    apiContext,
                    machine.id,
                    "MAINTENANCE",
                );

                expect(
                    requestMock,
                ).toHaveBeenLastCalledWith(
                    "/api/v1/machines/machine-001/status",
                    apiContext,
                    {
                        method:
                            "POST",
                        body: {
                            status:
                                "MAINTENANCE",
                        },
                    },
                );

                await deactivateMachine(
                    apiContext,
                    machine.id,
                );

                expect(
                    requestMock,
                ).toHaveBeenLastCalledWith(
                    "/api/v1/machines/machine-001/deactivate",
                    apiContext,
                    {
                        method:
                            "POST",
                    },
                );

                await reactivateMachine(
                    apiContext,
                    machine.id,
                );

                expect(
                    requestMock,
                ).toHaveBeenLastCalledWith(
                    "/api/v1/machines/machine-001/reactivate",
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