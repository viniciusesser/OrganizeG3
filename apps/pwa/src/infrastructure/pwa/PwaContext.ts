import {
    createContext,
} from "react";

export interface PwaContextValue {
    readonly canInstall: boolean;
    readonly isInstalled: boolean;
    readonly isOnline: boolean;
    readonly installApp: () => Promise<void>;
}

export const PwaContext = createContext<PwaContextValue>({
    canInstall: false,
    isInstalled: false,
    isOnline: true,
    installApp: async () => undefined,
});