import {
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    archiveCustomer,
    createCustomer,
    getCustomer,
    listCustomerPage,
    listCustomers,
    reactivateCustomer,
    updateCustomer,
} from "@/features/customers/api/customersApi";
import type {
    Customer,
} from "@/features/customers/model/customer";
import {
    authenticatedApiRequest,
} from "@/infrastructure/api/authenticatedApi";
import type {
    AuthenticatedApiContext,
} from "@/infrastructure/api/authenticatedApi";

vi.mock(
    "@/infrastructure/api/authenticatedApi",
    () => ({
        authenticatedApiRequest:
            vi.fn(),
    }),
);

const authenticatedRequestMock =
    vi.mocked(
        authenticatedApiRequest,
    );

const context: AuthenticatedApiContext = {
    accessToken: "access-token",
    tenantId:
        "11111111-1111-4111-8111-111111111111",
};

function makeCustomer(
    id: number,
    name = `Cliente ${id}`,
): Customer {
    return {
        id,
        tenant_id:
            context.tenantId,
        code: `CLI-${id}`,
        name,
        customer_type:
            "INDIVIDUAL",
        document_number: null,
        email: null,
        phone: null,
        is_active: true,
        row_version: 1,
    };
}

describe(
    "customersApi",
    () => {
        beforeEach(() => {
            authenticatedRequestMock
                .mockReset();
        });

        it(
            "lists customers with filters",
            async () => {
                authenticatedRequestMock
                    .mockResolvedValue([]);

                await listCustomers(
                    context,
                    {
                        includeInactive: true,
                        search: "Empresa",
                        customerType:
                            "CORPORATE",
                        limit: 20,
                        offset: 40,
                    },
                );

                expect(
                    authenticatedRequestMock,
                ).toHaveBeenCalledTimes(1);

                const [
                    path,
                    requestContext,
                    options,
                ] =
                    authenticatedRequestMock
                        .mock.calls[0];

                const url =
                    new URL(
                        path,
                        "https://example.test",
                    );

                expect(
                    url.pathname,
                ).toBe(
                    "/api/v1/customers",
                );

                expect(
                    url.searchParams.get(
                        "include_inactive",
                    ),
                ).toBe("true");

                expect(
                    url.searchParams.get(
                        "search",
                    ),
                ).toBe("Empresa");

                expect(
                    url.searchParams.get(
                        "customer_type",
                    ),
                ).toBe("CORPORATE");

                expect(
                    url.searchParams.get(
                        "limit",
                    ),
                ).toBe("20");

                expect(
                    url.searchParams.get(
                        "offset",
                    ),
                ).toBe("40");

                expect(
                    requestContext,
                ).toEqual(context);

                expect(options).toEqual({
                    method: "GET",
                });
            },
        );

        it(
            "does not send an empty search",
            async () => {
                authenticatedRequestMock
                    .mockResolvedValue([]);

                await listCustomers(
                    context,
                    {
                        search: "   ",
                    },
                );

                const [path] =
                    authenticatedRequestMock
                        .mock.calls[0];

                const url =
                    new URL(
                        path,
                        "https://example.test",
                    );

                expect(
                    url.searchParams.has(
                        "search",
                    ),
                ).toBe(false);
            },
        );

        it(
            "builds page metadata using one extra record",
            async () => {
                const customers =
                    Array.from(
                        {
                            length: 21,
                        },
                        (_, index) =>
                            makeCustomer(
                                index + 1,
                            ),
                    );

                authenticatedRequestMock
                    .mockResolvedValue(
                        customers,
                    );

                const result =
                    await listCustomerPage(
                        context,
                        {
                            limit: 20,
                            offset: 20,
                        },
                    );

                expect(
                    result.items,
                ).toHaveLength(20);

                expect(
                    result.hasPrevious,
                ).toBe(true);

                expect(
                    result.hasNext,
                ).toBe(true);

                expect(
                    result.offset,
                ).toBe(20);

                expect(
                    result.pageSize,
                ).toBe(20);

                const [path] =
                    authenticatedRequestMock
                        .mock.calls[0];

                const url =
                    new URL(
                        path,
                        "https://example.test",
                    );

                expect(
                    url.searchParams.get(
                        "limit",
                    ),
                ).toBe("21");
            },
        );

        it(
            "gets one customer",
            async () => {
                const customer =
                    makeCustomer(7);

                authenticatedRequestMock
                    .mockResolvedValue(
                        customer,
                    );

                await expect(
                    getCustomer(
                        context,
                        7,
                    ),
                ).resolves.toEqual(
                    customer,
                );

                expect(
                    authenticatedRequestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/customers/7",
                    context,
                    {
                        method: "GET",
                    },
                );
            },
        );

        it(
            "creates one customer",
            async () => {
                const customer =
                    makeCustomer(1);

                authenticatedRequestMock
                    .mockResolvedValue(
                        customer,
                    );

                const payload = {
                    name:
                        "Cliente Novo",
                    customer_type:
                        "INDIVIDUAL" as const,
                    document_number:
                        null,
                    email:
                        "cliente@example.com",
                    phone:
                        null,
                };

                await createCustomer(
                    context,
                    payload,
                );

                expect(
                    authenticatedRequestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/customers",
                    context,
                    {
                        method: "POST",
                        body: payload,
                    },
                );
            },
        );

        it(
            "updates one customer",
            async () => {
                authenticatedRequestMock
                    .mockResolvedValue(
                        makeCustomer(4),
                    );

                const payload = {
                    row_version: 3,
                    name:
                        "Cliente Atualizado",
                };

                await updateCustomer(
                    context,
                    4,
                    payload,
                );

                expect(
                    authenticatedRequestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/customers/4",
                    context,
                    {
                        method: "PATCH",
                        body: payload,
                    },
                );
            },
        );

        it(
            "archives one customer",
            async () => {
                authenticatedRequestMock
                    .mockResolvedValue(
                        makeCustomer(8),
                    );

                await archiveCustomer(
                    context,
                    8,
                    {
                        row_version: 2,
                    },
                );

                expect(
                    authenticatedRequestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/customers/8/archive",
                    context,
                    {
                        method: "POST",
                        body: {
                            row_version: 2,
                        },
                    },
                );
            },
        );

        it(
            "reactivates one customer",
            async () => {
                authenticatedRequestMock
                    .mockResolvedValue(
                        makeCustomer(9),
                    );

                await reactivateCustomer(
                    context,
                    9,
                    {
                        row_version: 5,
                    },
                );

                expect(
                    authenticatedRequestMock,
                ).toHaveBeenCalledWith(
                    "/api/v1/customers/9/reactivate",
                    context,
                    {
                        method: "POST",
                        body: {
                            row_version: 5,
                        },
                    },
                );
            },
        );
    },
);