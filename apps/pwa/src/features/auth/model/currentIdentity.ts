export interface CurrentIdentity {
    readonly tenant_id: string;
    readonly user_id: string;
    readonly membership_id: string;
    readonly auth_user_id: string;
    readonly email: string;
    readonly display_name: string;
    readonly permissions: readonly string[];
}

export interface AuthenticatedIdentity {
    readonly tenantId: string;
    readonly userId: string;
    readonly membershipId: string;
    readonly authUserId: string;
    readonly email: string;
    readonly displayName: string;
    readonly permissions: ReadonlySet<string>;
}

export function mapCurrentIdentity(
    response: CurrentIdentity,
): AuthenticatedIdentity {
    return Object.freeze({
        tenantId: response.tenant_id,
        userId: response.user_id,
        membershipId:
            response.membership_id,
        authUserId:
            response.auth_user_id,
        email: response.email,
        displayName:
            response.display_name,
        permissions:
            new Set(response.permissions),
    });
}

export function hasPermission(
    identity: AuthenticatedIdentity,
    permissionCode: string,
): boolean {
    return identity.permissions.has(
        permissionCode,
    );
}