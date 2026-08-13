import {
    useEffect,
    useRef,
} from "react";
import type {
    RefObject,
} from "react";

const FOCUSABLE_SELECTOR = [
    "a[href]:not([tabindex='-1'])",
    "button:not([disabled]):not([tabindex='-1'])",
    "input:not([disabled]):not([type='hidden']):not([tabindex='-1'])",
    "select:not([disabled]):not([tabindex='-1'])",
    "textarea:not([disabled]):not([tabindex='-1'])",
    "[contenteditable='true']:not([tabindex='-1'])",
    "[tabindex]:not([tabindex='-1'])",
].join(",");

const overlayStack: symbol[] = [];

let bodyScrollLockCount = 0;
let bodyAlreadyHadLockClass = false;

export interface UseAccessibleOverlayOptions {
    readonly closeOnEscape?: boolean;
    readonly isActive?: boolean;
    readonly lockBodyScroll?: boolean;
    readonly onClose: () => void;
    readonly restoreFocus?: boolean;
}

export interface UseAccessibleOverlayResult<
    T extends HTMLElement,
> {
    readonly overlayRef: RefObject<T | null>;
}

function getFocusableElements(
    container: HTMLElement,
): HTMLElement[] {
    return Array.from(
        container.querySelectorAll<HTMLElement>(
            FOCUSABLE_SELECTOR,
        ),
    ).filter(
        (element) =>
            element.getAttribute(
                "aria-hidden",
            ) !== "true" &&
            !element.hasAttribute(
                "disabled",
            ),
    );
}

function lockBodyScroll(): void {
    if (bodyScrollLockCount === 0) {
        bodyAlreadyHadLockClass =
            document.body.classList.contains(
                "og3-overlay-open",
            );

        document.body.classList.add(
            "og3-overlay-open",
        );
    }

    bodyScrollLockCount += 1;
}

function unlockBodyScroll(): void {
    bodyScrollLockCount =
        Math.max(
            0,
            bodyScrollLockCount - 1,
        );

    if (
        bodyScrollLockCount === 0 &&
        !bodyAlreadyHadLockClass
    ) {
        document.body.classList.remove(
            "og3-overlay-open",
        );
    }

    if (bodyScrollLockCount === 0) {
        bodyAlreadyHadLockClass =
            false;
    }
}

function removeOverlayFromStack(
    overlayId: symbol,
): void {
    const overlayIndex =
        overlayStack.lastIndexOf(
            overlayId,
        );

    if (overlayIndex >= 0) {
        overlayStack.splice(
            overlayIndex,
            1,
        );
    }
}

export function useAccessibleOverlay<
    T extends HTMLElement,
>({
    closeOnEscape = true,
    isActive = true,
    lockBodyScroll:
    shouldLockBodyScroll = true,
    onClose,
    restoreFocus = true,
}: UseAccessibleOverlayOptions): UseAccessibleOverlayResult<T> {
    const overlayRef =
        useRef<T>(null);

    const onCloseRef =
        useRef(onClose);

    const closeOnEscapeRef =
        useRef(closeOnEscape);

    const restoreFocusTargetRef =
        useRef<HTMLElement | null>(
            null,
        );

    useEffect(
        () => {
            onCloseRef.current =
                onClose;
        },
        [
            onClose,
        ],
    );

    useEffect(
        () => {
            closeOnEscapeRef.current =
                closeOnEscape;
        },
        [
            closeOnEscape,
        ],
    );

    useEffect(
        () => {
            if (!isActive) {
                return undefined;
            }

            const overlayElement =
                overlayRef.current;

            if (
                overlayElement === null
            ) {
                return undefined;
            }

            const activeElementBeforeOpen =
                document.activeElement;

            if (
                activeElementBeforeOpen instanceof
                HTMLElement &&
                activeElementBeforeOpen !==
                document.body &&
                !overlayElement.contains(
                    activeElementBeforeOpen,
                )
            ) {
                restoreFocusTargetRef.current =
                    activeElementBeforeOpen;
            }

            const overlayId =
                Symbol(
                    "accessible-overlay",
                );

            overlayStack.push(
                overlayId,
            );

            if (
                shouldLockBodyScroll
            ) {
                lockBodyScroll();
            }

            const currentActiveElement =
                document.activeElement;

            if (
                !(
                    currentActiveElement instanceof
                    HTMLElement &&
                    overlayElement.contains(
                        currentActiveElement,
                    )
                )
            ) {
                const preferredFocusTarget =
                    overlayElement.querySelector<HTMLElement>(
                        "[data-og3-autofocus='true'], [autofocus]",
                    );

                const firstFocusableElement =
                    getFocusableElements(
                        overlayElement,
                    )[0];

                (
                    preferredFocusTarget ??
                    firstFocusableElement ??
                    overlayElement
                ).focus();
            }

            function handleKeyDown(
                event: KeyboardEvent,
            ): void {
                const isTopmostOverlay =
                    overlayStack[
                    overlayStack.length -
                    1
                    ] === overlayId;

                if (!isTopmostOverlay) {
                    return;
                }

                const activeOverlay =
                    overlayRef.current;

                if (
                    activeOverlay === null
                ) {
                    return;
                }

                if (
                    event.key ===
                    "Escape" &&
                    closeOnEscapeRef.current
                ) {
                    event.preventDefault();
                    event.stopPropagation();

                    onCloseRef.current();

                    return;
                }

                if (
                    event.key !== "Tab"
                ) {
                    return;
                }

                const focusableElements =
                    getFocusableElements(
                        activeOverlay,
                    );

                if (
                    focusableElements.length ===
                    0
                ) {
                    event.preventDefault();
                    activeOverlay.focus();

                    return;
                }

                const firstFocusable =
                    focusableElements[0];

                const lastFocusable =
                    focusableElements[
                    focusableElements.length -
                    1
                    ];

                const focusedElement =
                    document.activeElement;

                if (
                    !(
                        focusedElement instanceof
                        HTMLElement
                    ) ||
                    !activeOverlay.contains(
                        focusedElement,
                    )
                ) {
                    event.preventDefault();

                    (
                        event.shiftKey
                            ? lastFocusable
                            : firstFocusable
                    ).focus();

                    return;
                }

                if (
                    event.shiftKey &&
                    focusedElement ===
                    firstFocusable
                ) {
                    event.preventDefault();
                    lastFocusable.focus();

                    return;
                }

                if (
                    !event.shiftKey &&
                    focusedElement ===
                    lastFocusable
                ) {
                    event.preventDefault();
                    firstFocusable.focus();
                }
            }

            document.addEventListener(
                "keydown",
                handleKeyDown,
                true,
            );

            return () => {
                document.removeEventListener(
                    "keydown",
                    handleKeyDown,
                    true,
                );

                removeOverlayFromStack(
                    overlayId,
                );

                if (
                    shouldLockBodyScroll
                ) {
                    unlockBodyScroll();
                }

                const restoreTarget =
                    restoreFocusTargetRef.current;

                if (
                    restoreFocus &&
                    restoreTarget !== null &&
                    restoreTarget.isConnected
                ) {
                    restoreTarget.focus();
                }

                restoreFocusTargetRef.current =
                    null;
            };
        },
        [
            isActive,
            restoreFocus,
            shouldLockBodyScroll,
        ],
    );

    return {
        overlayRef,
    };
}