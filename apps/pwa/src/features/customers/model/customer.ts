export const CUSTOMER_TYPES = [
    "INDIVIDUAL",
    "CORPORATE",
] as const;

export type CustomerType =
    (typeof CUSTOMER_TYPES)[number];

export interface Customer {
    readonly id: number;
    readonly tenant_id: string;
    readonly code: string;
    readonly name: string;
    readonly customer_type: CustomerType;
    readonly document_number: string | null;
    readonly email: string | null;
    readonly phone: string | null;
    readonly is_active: boolean;
    readonly row_version: number;
}

export interface CustomerCreateInput {
    readonly name: string;
    readonly customer_type: CustomerType;
    readonly document_number?: string | null;
    readonly email?: string | null;
    readonly phone?: string | null;
}

export interface CustomerUpdateInput {
    readonly row_version: number;
    readonly name?: string;
    readonly customer_type?: CustomerType;
    readonly document_number?: string | null;
    readonly email?: string | null;
    readonly phone?: string | null;
}

export interface CustomerVersionInput {
    readonly row_version: number;
}

export interface CustomerListFilters {
    readonly includeInactive?: boolean;
    readonly search?: string;
    readonly customerType?: CustomerType | null;
    readonly limit?: number;
    readonly offset?: number;
}

export interface CustomerPage {
    readonly items: readonly Customer[];
    readonly hasPrevious: boolean;
    readonly hasNext: boolean;
    readonly offset: number;
    readonly pageSize: number;
}

export const DEFAULT_CUSTOMER_PAGE_SIZE = 20;

export function getCustomerTypeLabel(
    customerType: CustomerType,
): string {
    switch (customerType) {
        case "INDIVIDUAL":
            return "Pessoa Física";
        case "CORPORATE":
            return "Pessoa Jurídica";
    }
}

export function formatCustomerDocument(
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

export function formatCustomerPhone(
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