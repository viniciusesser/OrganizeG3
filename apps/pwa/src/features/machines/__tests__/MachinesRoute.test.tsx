import {
    cleanup,
    fireEvent,
    render,
    screen,
    waitFor,
} from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import {
    afterEach,
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    MachinesRoute,
} from "@/features/machines/routes/MachinesRoute";

const mocks =
    vi.hoisted(
        () => ({
            changeMachineStatus:
                vi.fn(),
            createMachine:
                vi.fn(),
            deactivateMachine:
                vi.fn(),
            hasPermission:
                vi.fn(),
            listMachinePage:
                vi.fn(),
            reactivateMachine:
                vi.fn(),
            updateMachine:
                vi.fn(),
            useAuth:
                vi.fn(),
        }),
    );

vi.mock(
    "@/features/auth/model/currentIdentity",
    () => ({
        hasPermission:
            mocks.hasPermission,
    }),
);

vi.mock(
    "@/features/auth/session/useAuth",
    () => ({
        useAuth:
            mocks.useAuth,
    }),
);

vi.mock(
    "@/features/machines/api/machinesApi",
    () => ({
        changeMachineStatus:
            mocks.changeMachineStatus,
        createMachine:
            mocks.createMachine,
        deactivateMachine:
            mocks.deactivateMachine,
        listMachinePage:
            mocks.listMachinePage,
        reactivateMachine:
            mocks.reactivateMachine,
        updateMachine:
            mocks.updateMachine,
    }),
);

const machine = {
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
} as const;

describe(
    "MachinesRoute",
    () => {
        beforeEach(
            () => {
                vi.clearAllMocks();

                mocks.useAuth
                    .mockReturnValue({
                        identity: {
                            id:
                                "user-001",
                        },
                        session: {
                            accessToken:
                                "access-token",
                        },
                        selectedTenant: {
                            tenantId:
                                "tenant-001",
                        },
                    });

                mocks.hasPermission
                    .mockReturnValue(
                        true,
                    );

                mocks.listMachinePage
                    .mockResolvedValue({
                        items: [
                            machine,
                        ],
                        hasPrevious:
                            false,
                        hasNext:
                            false,
                        offset:
                            0,
                        pageSize:
                            20,
                    });

                mocks.changeMachineStatus
                    .mockResolvedValue({
                        ...machine,
                        status:
                            "MAINTENANCE",
                    });
            },
        );

        afterEach(
            () => {
                cleanup();
            },
        );

        it(
            "carrega as máquinas da empresa ativa",
            async () => {
                render(
                    <MachinesRoute />,
                );

                expect(
                    await screen.findByText(
                        "Seccionadora principal",
                    ),
                ).toBeInTheDocument();

                expect(
                    mocks.listMachinePage,
                ).toHaveBeenCalledWith(
                    {
                        accessToken:
                            "access-token",
                        tenantId:
                            "tenant-001",
                    },
                    {
                        includeInactive:
                            false,
                        search:
                            "",
                        machineType:
                            "",
                        status:
                            null,
                        limit:
                            20,
                        offset:
                            0,
                    },
                );
            },
        );

        it(
            "não consulta máquinas sem permissão de leitura",
            async () => {
                mocks.hasPermission
                    .mockReturnValue(
                        false,
                    );

                render(
                    <MachinesRoute />,
                );

                expect(
                    screen.getByText(
                        "Acesso restrito",
                    ),
                ).toBeInTheDocument();

                await waitFor(
                    () => {
                        expect(
                            mocks.listMachinePage,
                        ).not.toHaveBeenCalled();
                    },
                );
            },
        );

        it(
            "altera o status operacional pelos detalhes",
            async () => {
                render(
                    <MachinesRoute />,
                );

                await screen.findByText(
                    "Seccionadora principal",
                );

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Abrir",
                        },
                    ),
                );

                fireEvent.change(
                    screen.getByLabelText(
                        "Alterar status operacional",
                    ),
                    {
                        target: {
                            value:
                                "MAINTENANCE",
                        },
                    },
                );

                fireEvent.click(
                    screen.getByRole(
                        "button",
                        {
                            name:
                                "Atualizar status",
                        },
                    ),
                );

                await waitFor(
                    () => {
                        expect(
                            mocks.changeMachineStatus,
                        ).toHaveBeenCalledWith(
                            {
                                accessToken:
                                    "access-token",
                                tenantId:
                                    "tenant-001",
                            },
                            "machine-001",
                            "MAINTENANCE",
                        );
                    },
                );
            },
        );
    },
);