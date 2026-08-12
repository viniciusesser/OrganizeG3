export interface Supplier {
    readonly id: string;
    readonly tenant_id: string;
    readonly code: string;
    readonly name: string;
    readonly trade_name: string | null;
    readonly legal_name: string | null;
    readonly document_number: string | null;
    readonly state_registration: string | null;
    readonly email: string | null;
    readonly invoice_email: string | null;
    readonly phone: string | null;
    readonly secondary_phone: string | null;
    readonly website: string | null;
    readonly contact_name: string | null;
    readonly postal_code: string | null;
    readonly street: string | null;
    readonly number: string | null;
    readonly district: string | null;
    readonly city: string | null;
    readonly state: string | null;
    readonly is_active: boolean;
    readonly created_at: string;
    readonly updated_at: string;
}

export interface SupplierCreateInput {
    readonly code: string;
    readonly name: string;
    readonly trade_name?: string | null;
    readonly legal_name?: string | null;
    readonly document_number?: string | null;
    readonly state_registration?: string | null;
    readonly email?: string | null;
    readonly invoice_email?: string | null;
    readonly phone?: string | null;
    readonly secondary_phone?: string | null;
    readonly website?: string | null;
    readonly contact_name?: string | null;
    readonly postal_code?: string | null;
    readonly street?: string | null;
    readonly number?: string | null;
    readonly district?: string | null;
    readonly city?: string | null;
    readonly state?: string | null;
}

export interface SupplierUpdateInput {
    readonly code?: string;
    readonly name?: string;
    readonly trade_name?: string | null;
    readonly legal_name?: string | null;
    readonly document_number?: string | null;
    readonly state_registration?: string | null;
    readonly email?: string | null;
    readonly invoice_email?: string | null;
    readonly phone?: string | null;
    readonly secondary_phone?: string | null;
    readonly website?: string | null;
    readonly contact_name?: string | null;
    readonly postal_code?: string | null;
    readonly street?: string | null;
    readonly number?: string | null;
    readonly district?: string | null;
    readonly city?: string | null;
    readonly state?: string | null;
}

export interface SupplierListFilters {
    readonly includeInactive?: boolean;
    readonly search?: string;
    readonly limit?: number;
    readonly offset?: number;
}

export interface SupplierPage {
    readonly items: readonly Supplier[];
    readonly hasPrevious: boolean;
    readonly hasNext: boolean;
    readonly offset: number;
    readonly pageSize: number;
}

export const DEFAULT_SUPPLIER_PAGE_SIZE = 20;

export function formatSupplierDocument(
    documentNumber: string | null,
): string {
    if (documentNumber === null) {
        return "—";
    }

    const digits =
        documentNumber.replace(/\D/g, "");

    if (digits.length === 11) {
        return digits.replace(
            /^(\d{3})(\d{3})(\d{3})(\d{2})$/,
            "$1.$2.$3-$4",
        );
    }

    if (digits.length === 14) {
        return digits.replace(
            /^(\d{2})(\d{3})(\d{3})(\d{4})(\d{2})$/,
            "$1.$2.$3/$4-$5",
        );
    }

    return documentNumber;
}

export function formatSupplierPhone(
    phone: string | null,
): string {
    if (phone === null) {
        return "—";
    }

    const digits =
        phone.replace(/\D/g, "");

    if (digits.length === 10) {
        return digits.replace(
            /^(\d{2})(\d{4})(\d{4})$/,
            "($1) $2-$3",
        );
    }

    if (digits.length === 11) {
        return digits.replace(
            /^(\d{2})(\d{5})(\d{4})$/,
            "($1) $2-$3",
        );
    }

    return phone;
}

export function formatSupplierAddress(
    supplier: Supplier,
): string {
    const streetLine = [
        supplier.street,
        supplier.number,
    ]
        .filter(
            (value): value is string =>
                value !== null &&
                value.trim().length > 0,
        )
        .join(", ");

    const cityLine = [
        supplier.district,
        supplier.city,
        supplier.state,
    ]
        .filter(
            (value): value is string =>
                value !== null &&
                value.trim().length > 0,
        )
        .join(" - ");

    const address = [
        streetLine,
        cityLine,
        supplier.postal_code,
    ]
        .filter(
            (value): value is string =>
                value !== null &&
                value.trim().length > 0,
        )
        .join(" · ");

    return address.length > 0
        ? address
        : "—";
}