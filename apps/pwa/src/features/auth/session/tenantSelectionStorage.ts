const TENANT_STORAGE_KEY =
    "organizeg3.auth.tenant_id";

function getStorage():
    Storage | null {
    if (
        typeof window === "undefined"
    ) {
        return null;
    }

    return window.localStorage;
}

export function readStoredTenantId():
    string | null {
    const storage =
        getStorage();

    if (storage === null) {
        return null;
    }

    const value =
        storage.getItem(
            TENANT_STORAGE_KEY,
        );

    if (value === null) {
        return null;
    }

    const normalized =
        value.trim();

    return normalized.length > 0
        ? normalized
        : null;
}

export function storeTenantId(
    tenantId: string,
): void {
    const normalized =
        tenantId.trim();

    if (normalized.length === 0) {
        throw new Error(
            "tenantId não pode ser vazio.",
        );
    }

    getStorage()?.setItem(
        TENANT_STORAGE_KEY,
        normalized,
    );
}

export function clearStoredTenantId():
    void {
    getStorage()?.removeItem(
        TENANT_STORAGE_KEY,
    );
}