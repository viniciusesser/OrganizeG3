import {
    useContext,
} from "react";

import {
    AuthContext,
} from "@/features/auth/session/AuthContext";
import type {
    AuthContextValue,
} from "@/features/auth/session/AuthContext";

export function useAuth():
    AuthContextValue {
    const context =
        useContext(
            AuthContext,
        );

    if (context === null) {
        throw new Error(
            "useAuth deve ser utilizado dentro de AuthProvider.",
        );
    }

    return context;
}