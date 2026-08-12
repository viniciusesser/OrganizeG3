import {
    useContext,
} from "react";

import {
    PwaContext,
} from "./PwaContext";

export function usePwa() {
    return useContext(PwaContext);
}