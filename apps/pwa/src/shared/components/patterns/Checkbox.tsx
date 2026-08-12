import {
    useId,
} from "react";
import type {
    InputHTMLAttributes,
    ReactNode,
} from "react";

export interface CheckboxProps
    extends Omit<
        InputHTMLAttributes<HTMLInputElement>,
        "type"
    > {
    readonly label: ReactNode;
    readonly supportText?: string;
}

export function Checkbox({
    "aria-describedby": ariaDescribedBy,
    className,
    id,
    label,
    supportText,
    ...inputProps
}: CheckboxProps) {
    const generatedId = useId();
    const controlId = id ?? generatedId;
    const supportId = `${controlId}-support`;

    const describedBy = [
        ariaDescribedBy,
        supportText !== undefined
            ? supportId
            : undefined,
    ]
        .filter(Boolean)
        .join(" ") || undefined;

    return (
        <div className="og3-field">
            <label
                className="og3-checkbox-field"
                htmlFor={controlId}
            >
                <input
                    {...inputProps}
                    aria-describedby={describedBy}
                    className={className}
                    id={controlId}
                    type="checkbox"
                />

                <span>{label}</span>
            </label>

            {supportText !== undefined && (
                <span
                    className="og3-field__support"
                    id={supportId}
                >
                    {supportText}
                </span>
            )}
        </div>
    );
}