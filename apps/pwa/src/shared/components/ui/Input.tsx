import {
    useId,
} from "react";
import type {
    InputHTMLAttributes,
} from "react";

export interface InputProps
    extends Omit<
        InputHTMLAttributes<HTMLInputElement>,
        "id"
    > {
    readonly id?: string;
    readonly label: string;
    readonly supportText?: string;
    readonly error?: string;
}

export function Input({
    id,
    label,
    supportText,
    error,
    ...props
}: InputProps) {
    const generatedId = useId();
    const inputId = id ?? generatedId;

    const supportId =
        supportText !== undefined
            ? `${inputId}-support`
            : undefined;

    const errorId =
        error !== undefined
            ? `${inputId}-error`
            : undefined;

    const describedBy = [
        supportId,
        errorId,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <div className="og3-field">
            <label
                className="og3-field__label"
                htmlFor={inputId}
            >
                {label}
            </label>

            <input
                {...props}
                aria-describedby={
                    describedBy || undefined
                }
                aria-invalid={
                    error !== undefined
                }
                className="og3-field__input"
                id={inputId}
            />

            {supportText !== undefined && (
                <span
                    className="og3-field__support"
                    id={supportId}
                >
                    {supportText}
                </span>
            )}

            {error !== undefined && (
                <span
                    className="og3-field__error"
                    id={errorId}
                    role="alert"
                >
                    {error}
                </span>
            )}
        </div>
    );
}