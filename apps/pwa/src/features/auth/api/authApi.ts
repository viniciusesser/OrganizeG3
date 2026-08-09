import {
    mapAccessibleTenant,
} from "@/features/auth/model/accessibleTenant";
import type {
    AccessibleTenant,
    AccessibleTenantResponse,
} from "@/features/auth/model/accessibleTenant";
import {
    mapCurrentIdentity,
} from "@/features/auth/model/currentIdentity";
import type {
    AuthenticatedIdentity,
    CurrentIdentity,
} from "@/features/auth/model/currentIdentity";
import {
    authenticatedApiRequest,
} from "@/infrastructure/api/authenticatedApi";
import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";
import {
    bearerApiRequest,
} from "@/infrastructure/api/bearerApi";

export async function listAccessibleTenants(
    accessToken: string,
): Promise<readonly AccessibleTenant[]> {
    const response =
        await bearerApiRequest<
            AccessibleTenantResponse[]
        >(
            "/v1/auth/tenants",
            accessToken,
            {
                method: "GET",
            },
        );

    return Object.freeze(
        response.map(
            mapAccessibleTenant,
        ),
    );
}

export async function getCurrentIdentity(
    context: AuthenticatedApiContext,
): Promise<AuthenticatedIdentity> {
    const response =
        await authenticatedApiRequest<
            CurrentIdentity
        >(
            "/v1/auth/me",
            context,
            {
                method: "GET",
            },
        );

    return mapCurrentIdentity(
        response,
    );
}