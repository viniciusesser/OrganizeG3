import {
    useId,
} from "react";
import type {
    ReactNode,
} from "react";

import {
    useAccessibleOverlay,
} from "@/shared/hooks/useAccessibleOverlay";
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
    const descriptionId =
        useId();

    const {
        overlayRef,
    } = useAccessibleOverlay<HTMLDivElement>({
        closeOnEscape:
            !isSubmitting,
        onClose: onCancel,
    });

    return (
        <div
            aria-describedby={
                descriptionId
            }
            aria-labelledby={
                titleId
            }
            aria-modal="true"
            className="og3-dialog-backdrop"
            ref={overlayRef}
            role="alertdialog"
            tabIndex={-1}
        >
            <div
                className={[
                    "og3-dialog",
                    "og3-dialog--sm",
                ].join(" ")}
            >
                <header
                    className="og3-dialog__header"
                >
                    <div
                        className="og3-dialog__heading"
                    >
                        <Heading
                            level={3}
                        >
                            <span
                                id={
                                    titleId
                                }
                            >
                                {title}
                            </span>
                        </Heading>

                        <Text
                            id={
                                descriptionId
                            }
                            tone="secondary"
                        >
                            {
                                description
                            }
                        </Text>
                    </div>
                </header>

                {errorMessage !==
                    null && (
                        <div
                            className="og3-dialog__body"
                        >
                            <InlineMessage
                                tone="danger"
                            >
                                {
                                    errorMessage
                                }
                            </InlineMessage>
                        </div>
                    )}

                <footer
                    className="og3-dialog__footer"
                >
                    <Button
                        data-og3-autofocus="true"
                        disabled={
                            isSubmitting
                        }
                        onClick={
                            onCancel
                        }
                        variant="secondary"
                    >
                        {
                            cancelLabel
                        }
                    </Button>

                    <Button
                        disabled={
                            isSubmitting
                        }
                        onClick={
                            onConfirm
                        }
                        variant="danger"
                    >
                        {
                            isSubmitting
                                ? pendingLabel
                                : confirmLabel
                        }
                    </Button>
                </footer>
            </div>
        </div>
    );
}