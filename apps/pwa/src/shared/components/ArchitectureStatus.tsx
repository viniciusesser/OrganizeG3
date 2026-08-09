import {
    useEffect,
    useState,
} from "react";

import { ApiError } from "@/infrastructure/api/apiError";
import { getApiHealth } from "@/infrastructure/api/health";
import type { HealthResponse } from "@/shared/types/health";

type HealthState =
    | {
        readonly status: "loading";
    }
    | {
        readonly status: "success";
        readonly health: HealthResponse;
    }
    | {
        readonly status: "error";
        readonly message: string;
        readonly correlationId: string | null;
    };

function getErrorState(
    error: unknown,
): HealthState {
    if (error instanceof ApiError) {
        return {
            status: "error",
            message: error.message,
            correlationId: error.correlationId,
        };
    }

    return {
        status: "error",
        message:
            "Ocorreu um erro inesperado ao consultar a API.",
        correlationId: null,
    };
}

export function ArchitectureStatus() {
    const [
        healthState,
        setHealthState,
    ] = useState<HealthState>({
        status: "loading",
    });

    useEffect(() => {
        let isActive = true;

        async function loadHealth(): Promise<void> {
            try {
                const health =
                    await getApiHealth();

                if (!isActive) {
                    return;
                }

                setHealthState({
                    status: "success",
                    health,
                });
            } catch (error) {
                if (!isActive) {
                    return;
                }

                setHealthState(
                    getErrorState(error),
                );
            }
        }

        void loadHealth();

        return () => {
            isActive = false;
        };
    }, []);

    return (
        <section>
            <h2>API</h2>

            {healthState.status === "loading" && (
                <p>
                    Verificando comunicação com a API...
                </p>
            )}

            {healthState.status === "success" && (
                <dl>
                    <div>
                        <dt>Status</dt>
                        <dd>
                            {healthState.health.status}
                        </dd>
                    </div>

                    <div>
                        <dt>Service</dt>
                        <dd>
                            {healthState.health.service}
                        </dd>
                    </div>

                    <div>
                        <dt>Version</dt>
                        <dd>
                            {healthState.health.version}
                        </dd>
                    </div>
                </dl>
            )}

            {healthState.status === "error" && (
                <>
                    <p>
                        {healthState.message}
                    </p>

                    {healthState.correlationId !== null && (
                        <p>
                            Correlation ID:{" "}
                            {healthState.correlationId}
                        </p>
                    )}
                </>
            )}
        </section>
    );
}