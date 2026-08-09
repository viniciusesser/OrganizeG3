export interface AuthSession {
    readonly accessToken: string;
    readonly refreshToken: string;
    readonly expiresAt: number | null;
    readonly authUserId: string;
    readonly email: string | null;
}