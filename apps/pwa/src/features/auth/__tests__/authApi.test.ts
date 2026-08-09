import {
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    getCurrentIdentity,
    listAccessibleTenants,
} from "@/features/auth/api/authApi";
import {
    authenticatedApiRequest,
} from "@/infrastructure/api/authenticatedApi";
import {
    bearerApiRequest,
} from "@/infrastructure/api/bearerApi";

vi.mock(
    "@/infrastructure/api/authenticatedApi",
    () => ({
        authenticatedApiRequest:
            vi.fn(),
    }),
);

vi.mock(
    "@/infrastructure/api/bearerApi",
    () => ({
        bearerApiRequest:
            vi.fn(),
    }),
);

const authenticatedApiRequestMock =
    vi.mocked(
        authenticatedApiRequest,
    );

const bearerApiRequestMock =
    vi.mocked(
        bearerApiRequest,
    );

describe(
    "authApi",
    () => {
        it(
            "lists and maps accessible tenants",
            async () => {
                bearerApiRequestMock
                    .mockResolvedValue([
                        {
                            tenant_id:
                                "tenant-a",
                            membership_id:
                                "membership-a",
                            name:
                                "Empresa A",
                        },
                        {
                            tenant_id:
                                "tenant-b",
                            membership_id:
                                "membership-b",
                            name:
                                "Empresa B",
                        },
                    ]);

                const tenants =
                    await listAccessibleTenants(
                        "access-token",
                    );

                expect(
                    bearerApiRequestMock,
                ).toHaveBeenCalledWith(
                    "/v1/auth/tenants",
                    "access-token",
                    {
                        method: "GET",
                    },
                );

                expect(tenants).toEqual([
                    {
                        tenantId:
                            "tenant-a",
                        membershipId:
                            "membership-a",
                        name:
                            "Empresa A",
                    },
                    {
                        tenantId:
                            "tenant-b",
                        membershipId:
                            "membership-b",
                        name:
                            "Empresa B",
                    },
                ]);
            },
        );

        it(
            "loads and maps the current OrganizeG3 identity",
            async () => {
                authenticatedApiRequestMock
                    .mockResolvedValue({
                        tenant_id:
                            "tenant-id",
                        user_id:
                            "user-id",
                        membership_id:
                            "membership-id",
                        auth_user_id:
                            "auth-user-id",
                        email:
                            "admin@example.com",
                        display_name:
                            "Administrador",
                        permissions: [
                            "customers.read",
                            "materials.read",
                        ],
                    });

                const identity =
                    await getCurrentIdentity({
                        accessToken:
                            "access-token",
                        tenantId:
                            "tenant-id",
                    });

                expect(
                    authenticatedApiRequestMock,
                ).toHaveBeenCalledWith(
                    "/v1/auth/me",
                    {
                        accessToken:
                            "access-token",
                        tenantId:
                            "tenant-id",
                    },
                    {
                        method: "GET",
                    },
                );

                expect(
                    identity.displayName,
                ).toBe(
                    "Administrador",
                );

                expect(
                    identity.permissions.has(
                        "customers.read",
                    ),
                ).toBe(true);

                expect(
                    identity.permissions.has(
                        "employees.read",
                    ),
                ).toBe(false);
            },
        );
    },
);