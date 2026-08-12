import type {
    Company,
    CreateCompanyPayload,
    UpdateCompanyPayload,
} from "@/features/company/model/company";
import {
    ApiError,
} from "@/infrastructure/api/apiError";
import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";
import {
    authenticatedApiRequest,
} from "@/infrastructure/api/authenticatedApi";

const COMPANY_PATH = "/api/v1/company";

export async function getCompany(
    context: AuthenticatedApiContext,
): Promise<Company | null> {
    try {
        return await authenticatedApiRequest<Company>(
            COMPANY_PATH,
            context,
            {
                method: "GET",
            },
        );
    } catch (error: unknown) {
        if (
            error instanceof ApiError &&
            error.status === 404
        ) {
            return null;
        }

        throw error;
    }
}

export async function createCompany(
    context: AuthenticatedApiContext,
    payload: CreateCompanyPayload,
): Promise<Company> {
    return authenticatedApiRequest<Company>(
        COMPANY_PATH,
        context,
        {
            method: "POST",
            body: payload,
        },
    );
}

export async function updateCompany(
    context: AuthenticatedApiContext,
    payload: UpdateCompanyPayload,
): Promise<Company> {
    return authenticatedApiRequest<Company>(
        COMPANY_PATH,
        context,
        {
            method: "PATCH",
            body: payload,
        },
    );
}