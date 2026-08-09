export type ApplicationArchitectureStatus =
    | "ready"
    | "pending";

export interface ApplicationArchitectureArea {
    readonly name: string;
    readonly status: ApplicationArchitectureStatus;
}