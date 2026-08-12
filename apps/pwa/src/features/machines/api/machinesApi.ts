import type {
    Machine,
    MachineCreateInput,
    MachineListFilters,
    MachinePage,
    MachineStatus,
    MachineUpdateInput,
} from "@/features/machines/model/machine";
import {
    DEFAULT_MACHINE_PAGE_SIZE,
} from "@/features/machines/model/machine";
import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";
import {
    authenticatedApiRequest,
} from "@/infrastructure/api/authenticatedApi";

const MACHINES_PATH = "/api/v1/machines";

function appendText(
    params: URLSearchParams,
    name: string,
    value: string | undefined,
): void {
    const normalized =
        value?.trim() ?? "";

    if (normalized.length > 0) {
        params.set(
            name,
            normalized,
        );
    }
}

function buildMachineListPath(
    filters: MachineListFilters,
): string {
    const params =
        new URLSearchParams();

    params.set(
        "include_inactive",
        String(
            filters.includeInactive ?? false,
        ),
    );

    appendText(
        params,
        "search",
        filters.search,
    );

    appendText(
        params,
        "machine_type",
        filters.machineType,
    );

    appendText(
        params,
        "branch_id",
        filters.branchId,
    );

    if (
        filters.status !== undefined &&
        filters.status !== null
    ) {
        params.set(
            "status",
            filters.status,
        );
    }

    if (
        filters.limit !== undefined
    ) {
        params.set(
            "limit",
            String(filters.limit),
        );
    }

    if (
        filters.offset !== undefined
    ) {
        params.set(
            "offset",
            String(filters.offset),
        );
    }

    return `${MACHINES_PATH}?${params.toString()}`;
}

export async function listMachines(
    context: AuthenticatedApiContext,
    filters: MachineListFilters = {},
): Promise<readonly Machine[]> {
    return authenticatedApiRequest<Machine[]>(
        buildMachineListPath(filters),
        context,
        {
            method:
                "GET",
        },
    );
}

export async function listMachinePage(
    context: AuthenticatedApiContext,
    filters: MachineListFilters = {},
): Promise<MachinePage> {
    const pageSize =
        filters.limit ??
        DEFAULT_MACHINE_PAGE_SIZE;

    const offset =
        filters.offset ?? 0;

    const loadedItems =
        await listMachines(
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

export async function createMachine(
    context: AuthenticatedApiContext,
    payload: MachineCreateInput,
): Promise<Machine> {
    return authenticatedApiRequest<Machine>(
        MACHINES_PATH,
        context,
        {
            method:
                "POST",
            body:
                payload,
        },
    );
}

export async function getMachine(
    context: AuthenticatedApiContext,
    machineId: string,
): Promise<Machine> {
    return authenticatedApiRequest<Machine>(
        `${MACHINES_PATH}/${machineId}`,
        context,
        {
            method:
                "GET",
        },
    );
}

export async function updateMachine(
    context: AuthenticatedApiContext,
    machineId: string,
    payload: MachineUpdateInput,
): Promise<Machine> {
    return authenticatedApiRequest<Machine>(
        `${MACHINES_PATH}/${machineId}`,
        context,
        {
            method:
                "PATCH",
            body:
                payload,
        },
    );
}

export async function changeMachineStatus(
    context: AuthenticatedApiContext,
    machineId: string,
    status: MachineStatus,
): Promise<Machine> {
    return authenticatedApiRequest<Machine>(
        `${MACHINES_PATH}/${machineId}/status`,
        context,
        {
            method:
                "POST",
            body: {
                status,
            },
        },
    );
}

export async function deactivateMachine(
    context: AuthenticatedApiContext,
    machineId: string,
): Promise<Machine> {
    return authenticatedApiRequest<Machine>(
        `${MACHINES_PATH}/${machineId}/deactivate`,
        context,
        {
            method:
                "POST",
        },
    );
}

export async function reactivateMachine(
    context: AuthenticatedApiContext,
    machineId: string,
): Promise<Machine> {
    return authenticatedApiRequest<Machine>(
        `${MACHINES_PATH}/${machineId}/reactivate`,
        context,
        {
            method:
                "POST",
        },
    );
}