export class AuthClientError extends Error {
    readonly code: string;
    readonly causeMessage: string | null;

    constructor({
        code,
        message,
        causeMessage = null,
    }: {
        readonly code: string;
        readonly message: string;
        readonly causeMessage?: string | null;
    }) {
        super(message);

        this.name = "AuthClientError";
        this.code = code;
        this.causeMessage = causeMessage;
    }
}