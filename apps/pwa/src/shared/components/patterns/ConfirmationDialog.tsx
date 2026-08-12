import {
    useEffect,
} from "react";
import type {
    ReactNode,
} from "react";

import {
    Button,
    Heading,
    Text,
} from "@/shared/components/ui";

import {
    InlineMessage,
} from "./InlineMessage";

export interface ConfirmationDialogProps {
    readonly cancelLabel?: string;
    readonly confirmLabel: string;
    readonly description: ReactNode;
    readonly errorMessage?: string | null;
    readonly isSubmitting?: boolean;
    readonly onCancel: () => void;
    readonly onConfirm: () => void;
    readonly pendingLabel: string;
    readonly title: string;
    readonly titleId: string;
}

export function ConfirmationDialog({
    cancelLabel = "Cancelar",
    confirmLabel,
    description,
    errorMessage = null,
    isSubmitting = false,
    onCancel,
    onConfirm,
    pendingLabel,
    title,
    titleId,
}: ConfirmationDialogProps) {
    useEffect(
        () => {
            const handleKeyDown = (
                event: KeyboardEvent,
            ) => {
                if (
                    event.key === "Escape" &&
                    !isSubmitting
                ) {
                    onCancel();
                }
            };

            document.addEventListener(
                "keydown",
                handleKeyDown,
            );

            return () => {
                document.removeEventListener(
                    "keydown",
                    handleKeyDown,
                );
            };
        },
        [
            isSubmitting,
            onCancel,
        ],
    );

    return (
        <div
            aria-labelledby={titleId}
            aria-modal="true"
            className="og3-dialog-backdrop"
            role="alertdialog"
        >
            <div className="og3-dialog og3-dialog--sm">
                <header className="og3-dialog__header">
                    <div className="og3-dialog__heading">
                        <Heading level={3}>
                            <span id={titleId}>
                                {title}
                            </span>
                        </Heading>

                        <Text tone="secondary">
                            {description}
                        </Text>
                    </div>
                </header>

                {errorMessage !== null && (
                    <div className="og3-dialog__body">
                        <InlineMessage tone="danger">
                            {errorMessage}
                        </InlineMessage>
                    </div>
                )}

                <footer className="og3-dialog__footer">
                    <Button
                        disabled={isSubmitting}
                        onClick={onCancel}
                        type="button"
                        variant="secondary"
                    >
                        {cancelLabel}
                    </Button>

                    <Button
                        disabled={isSubmitting}
                        onClick={onConfirm}
                        type="button"
                        variant="danger"
                    >
                        {isSubmitting
                            ? pendingLabel
                            : confirmLabel}
                    </Button>
                </footer>
            </div>
        </div>
    );
}