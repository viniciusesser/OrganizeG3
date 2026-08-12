import {
    useId,
} from "react";
import type {
    SelectHTMLAttributes,
} from "react";

export interface SelectProps
    extends SelectHTMLAttributes<HTMLSelectElement> {
    readonly error?: string;
    readonly label: string;
    readonly supportText?: string;
}

export function Select({
    "aria-describedby": ariaDescribedBy,
    "aria-invalid": ariaInvalid,
    children,
    className,
    error,
    id,
    label,
    supportText,
    ...selectProps
}: SelectProps) {
    const generatedId = useId();
    const controlId = id ?? generatedId;
    const supportId = `${controlId}-support`;
    const errorId = `${controlId}-error`;
    const hasError =
        error !== undefined &&
        error.length > 0;

    const describedBy = [
        ariaDescribedBy,
        supportText !== undefined
            ? supportId
            : undefined,
        hasError
            ? errorId
            : undefined,
    ]
        .filter(Boolean)
        .join(" ") || undefined;

    const inputClassName = [
        "og3-field__input",
        className,
    ]
        .filter(Boolean)
        .join(" ");

    return (
        <div className="og3-field">
            <label
                className="og3-field__label"
                htmlFor={controlId}
            >
                {label}
            </label>

            <select
                {...selectProps}
                aria-describedby={describedBy}
                aria-invalid={
                    ariaInvalid ??
                    (hasError
                        ? true
                        : undefined)
                }
                className={inputClassName}
                id={controlId}
            >
                {children}
            </select>

            {supportText !== undefined && (
                <span
                    className="og3-field__support"
                    id={supportId}
                >
                    {supportText}
                </span>
            )}

            {hasError && (
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