export interface Branch {
    id: string;
    tenant_id: string;

    code: string;
    name: string;

    legal_name: string | null;
    document_number: string | null;
    state_registration: string | null;

    email: string | null;
    phone: string | null;
    website: string | null;

    street: string | null;
    number: string | null;
    district: string | null;
    city: string | null;
    state: string | null;
    postal_code: string | null;

    is_headquarters: boolean;
    is_active: boolean;

    created_at: string | null;
    updated_at: string | null;
}

export interface BranchOptionalFieldsPayload {
    legal_name?: string | null;
    document_number?: string | null;
    state_registration?: string | null;

    email?: string | null;
    phone?: string | null;
    website?: string | null;

    street?: string | null;
    number?: string | null;
    district?: string | null;
    city?: string | null;
    state?: string | null;
    postal_code?: string | null;
}

export interface CreateBranchPayload
    extends BranchOptionalFieldsPayload {
    code: string;
    name: string;
    is_headquarters: boolean;
}

export interface UpdateBranchPayload
    extends BranchOptionalFieldsPayload {
    code?: string | null;
    name?: string | null;
    is_headquarters?: boolean | null;
}

export interface BranchListFilters {
    includeInactive?: boolean;
    search?: string;
    isHeadquarters?: boolean;
    limit?: number;
    offset?: number;
}