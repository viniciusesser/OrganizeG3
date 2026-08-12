import type {
    Branch,
    BranchListFilters,
    CreateBranchPayload,
    UpdateBranchPayload,
} from "@/features/branches/model/branch";
import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";
import {
    authenticatedApiRequest,
} from "@/infrastructure/api/authenticatedApi";

const BRANCHES_PATH =
    "/api/v1/branches";

function appendOptionalText(
    parameters: URLSearchParams,
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

    parameters.set(
        name,
        normalized,
    );
}

function buildBranchesPath(
    filters: BranchListFilters,
): string {
    const parameters =
        new URLSearchParams();

    if (
        filters.includeInactive !==
        undefined
    ) {
        parameters.set(
            "include_inactive",
            String(
                filters.includeInactive,
            ),
        );
    }

    appendOptionalText(
        parameters,
        "search",
        filters.search,
    );

    if (
        filters.isHeadquarters !==
        undefined
    ) {
        parameters.set(
            "is_headquarters",
            String(
                filters.isHeadquarters,
            ),
        );
    }

    if (filters.limit !== undefined) {
        parameters.set(
            "limit",
            String(filters.limit),
        );
    }

    if (filters.offset !== undefined) {
        parameters.set(
            "offset",
            String(filters.offset),
        );
    }

    const query =
        parameters.toString();

    if (query.length === 0) {
        return BRANCHES_PATH;
    }

    return `${BRANCHES_PATH}?${query}`;
}

export async function listBranches(
    context: AuthenticatedApiContext,
    filters: BranchListFilters = {},
): Promise<Branch[]> {
    return authenticatedApiRequest<
        Branch[]
    >(
        buildBranchesPath(
            filters,
        ),
        context,
        {
            method: "GET",
        },
    );
}

export async function getBranch(
    context: AuthenticatedApiContext,
    branchId: string,
): Promise<Branch> {
    return authenticatedApiRequest<
        Branch
    >(
        `${BRANCHES_PATH}/${branchId}`,
        context,
        {
            method: "GET",
        },
    );
}

export async function createBranch(
    context: AuthenticatedApiContext,
    payload: CreateBranchPayload,
): Promise<Branch> {
    return authenticatedApiRequest<
        Branch
    >(
        BRANCHES_PATH,
        context,
        {
            method: "POST",
            body: payload,
        },
    );
}

export async function updateBranch(
    context: AuthenticatedApiContext,
    branchId: string,
    payload: UpdateBranchPayload,
): Promise<Branch> {
    return authenticatedApiRequest<
        Branch
    >(
        `${BRANCHES_PATH}/${branchId}`,
        context,
        {
            method: "PATCH",
            body: payload,
        },
    );
}

export async function deactivateBranch(
    context: AuthenticatedApiContext,
    branchId: string,
): Promise<Branch> {
    return authenticatedApiRequest<
        Branch
    >(
        `${BRANCHES_PATH}/${branchId}/deactivate`,
        context,
        {
            method: "POST",
        },
    );
}

export async function reactivateBranch(
    context: AuthenticatedApiContext,
    branchId: string,
): Promise<Branch> {
    return authenticatedApiRequest<
        Branch
    >(
        `${BRANCHES_PATH}/${branchId}/reactivate`,
        context,
        {
            method: "POST",
        },
    );
}