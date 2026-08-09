export interface AccessibleTenantResponse {
    readonly tenant_id: string;
    readonly membership_id: string;
    readonly name: string;
}

export interface AccessibleTenant {
    readonly tenantId: string;
    readonly membershipId: string;
    readonly name: string;
}

export function mapAccessibleTenant(
    response: AccessibleTenantResponse,
): AccessibleTenant {
    return Object.freeze({
        tenantId: response.tenant_id,
        membershipId:
            response.membership_id,
        name: response.name,
    });
}