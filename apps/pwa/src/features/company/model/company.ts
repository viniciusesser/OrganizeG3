export interface Company {
    id: string;
    tenant_id: string;

    trade_name: string;
    legal_name: string | null;
    document_number: string | null;
    state_registration: string | null;

    email: string | null;
    phone: string | null;
    website: string | null;
    logo_path: string | null;

    street: string | null;
    number: string | null;
    district: string | null;
    city: string | null;
    state: string | null;
    postal_code: string | null;

    is_active: boolean;
}

export interface CompanyContactPayload {
    document_number?: string | null;
    state_registration?: string | null;

    email?: string | null;
    phone?: string | null;
    website?: string | null;
    logo_path?: string | null;

    street?: string | null;
    number?: string | null;
    district?: string | null;
    city?: string | null;
    state?: string | null;
    postal_code?: string | null;
}

export interface CreateCompanyPayload
    extends CompanyContactPayload {
    trade_name: string;
    legal_name?: string | null;
}

export interface UpdateCompanyPayload
    extends CompanyContactPayload {
    trade_name?: string | null;
    legal_name?: string | null;
}