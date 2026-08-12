import {
    beforeEach,
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    createService,
    deactivateService,
    getService,
    listServicePage,
    listServices,
    reactivateService,
    updateService,
} from "@/features/services/api/servicesApi";
import type {
    Service,
    ServiceCreateInput,
} from "@/features/services/model/service";
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

const authenticatedApiRequestMock =
    vi.mocked(
        authenticatedApiRequest,
    );

const apiContext = {
    accessToken:
        "access-token",
    tenantId:
        "tenant-001",
};

const service: Service = {
    id: "service-001",
    tenant_id: "tenant-001",
    code: "CORTE",
    name: "Corte de MDF",
    category: "Usinagem",
    unit: "HORA",
    execution_mode: "INTERNAL",
    estimated_duration_minutes: 60,
    is_active: true,
    created_at:
        "2026-08-10T10:00:00Z",
    updated_at:
        "2026-08-10T10:00:00Z",
};

describe("servicesApi", () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it(
        "lista serviços com filtros normalizados",
        async () => {
            authenticatedApiRequestMock
                .mockResolvedValue([
                    service,
                ]);

            const result =
                await listServices(
                    apiContext,
                    {
                        includeInactive:
                            true,
                        search:
                            "  Corte  ",
                        category:
                            "  Usinagem  ",
                        executionMode:
                            "INTERNAL",
                        limit: 25,
                        offset: 50,
                    },
                );

            expect(
                authenticatedApiRequestMock,
            ).toHaveBeenCalledWith(
                "/api/v1/services?include_inactive=true&search=Corte&category=Usinagem&execution_mode=INTERNAL&limit=25&offset=50",
                apiContext,
                {
                    method: "GET",
                },
            );

            expect(result).toEqual([
                service,
            ]);
        },
    );

    it(
        "ignora filtros textuais vazios",
        async () => {
            authenticatedApiRequestMock
                .mockResolvedValue([]);

            await listServices(
                apiContext,
                {
                    search: "   ",
                    category: "   ",
                    executionMode:
                        null,
                },
            );

            expect(
                authenticatedApiRequestMock,
            ).toHaveBeenCalledWith(
                "/api/v1/services?include_inactive=false",
                apiContext,
                {
                    method: "GET",
                },
            );
        },
    );

    it(
        "constrói a página usando um registro adicional",
        async () => {
            const secondService: Service = {
                ...service,
                id: "service-002",
                code: "FITAGEM",
                name:
                    "Aplicação de fita de borda",
            };

            const thirdService: Service = {
                ...service,
                id: "service-003",
                code: "MONTAGEM",
                name:
                    "Montagem de mobiliário",
            };

            authenticatedApiRequestMock
                .mockResolvedValue([
                    service,
                    secondService,
                    thirdService,
                ]);

            const result =
                await listServicePage(
                    apiContext,
                    {
                        limit: 2,
                        offset: 2,
                    },
                );

            expect(
                authenticatedApiRequestMock,
            ).toHaveBeenCalledWith(
                "/api/v1/services?include_inactive=false&limit=3&offset=2",
                apiContext,
                {
                    method: "GET",
                },
            );

            expect(result).toEqual({
                items: [
                    service,
                    secondService,
                ],
                hasPrevious: true,
                hasNext: true,
                offset: 2,
                pageSize: 2,
            });
        },
    );

    it(
        "consulta um serviço pelo identificador",
        async () => {
            authenticatedApiRequestMock
                .mockResolvedValue(
                    service,
                );

            const result =
                await getService(
                    apiContext,
                    service.id,
                );

            expect(
                authenticatedApiRequestMock,
            ).toHaveBeenCalledWith(
                "/api/v1/services/service-001",
                apiContext,
                {
                    method: "GET",
                },
            );

            expect(result).toEqual(
                service,
            );
        },
    );

    it(
        "cadastra um serviço",
        async () => {
            const payload:
                ServiceCreateInput = {
                code: "CORTE",
                name: "Corte de MDF",
                category: "Usinagem",
                unit: "HORA",
                execution_mode:
                    "INTERNAL",
                estimated_duration_minutes:
                    60,
            };

            authenticatedApiRequestMock
                .mockResolvedValue(
                    service,
                );

            const result =
                await createService(
                    apiContext,
                    payload,
                );

            expect(
                authenticatedApiRequestMock,
            ).toHaveBeenCalledWith(
                "/api/v1/services",
                apiContext,
                {
                    method: "POST",
                    body: payload,
                },
            );

            expect(result).toEqual(
                service,
            );
        },
    );

    it(
        "atualiza um serviço",
        async () => {
            const payload = {
                name:
                    "Corte de MDF atualizado",
                estimated_duration_minutes:
                    90,
            };

            authenticatedApiRequestMock
                .mockResolvedValue({
                    ...service,
                    ...payload,
                });

            const result =
                await updateService(
                    apiContext,
                    service.id,
                    payload,
                );

            expect(
                authenticatedApiRequestMock,
            ).toHaveBeenCalledWith(
                "/api/v1/services/service-001",
                apiContext,
                {
                    method: "PATCH",
                    body: payload,
                },
            );

            expect(result).toEqual({
                ...service,
                ...payload,
            });
        },
    );

    it(
        "inativa um serviço",
        async () => {
            const inactiveService = {
                ...service,
                is_active: false,
            };

            authenticatedApiRequestMock
                .mockResolvedValue(
                    inactiveService,
                );

            const result =
                await deactivateService(
                    apiContext,
                    service.id,
                );

            expect(
                authenticatedApiRequestMock,
            ).toHaveBeenCalledWith(
                "/api/v1/services/service-001/deactivate",
                apiContext,
                {
                    method: "POST",
                },
            );

            expect(result).toEqual(
                inactiveService,
            );
        },
    );

    it(
        "reativa um serviço",
        async () => {
            authenticatedApiRequestMock
                .mockResolvedValue(
                    service,
                );

            const result =
                await reactivateService(
                    apiContext,
                    service.id,
                );

            expect(
                authenticatedApiRequestMock,
            ).toHaveBeenCalledWith(
                "/api/v1/services/service-001/reactivate",
                apiContext,
                {
                    method: "POST",
                },
            );

            expect(result).toEqual(
                service,
            );
        },
    );
});