import {
    useCallback,
    useEffect,
    useMemo,
    useRef,
    useState,
} from "react";
import type {
    PropsWithChildren,
} from "react";
import {
    registerSW,
} from "virtual:pwa-register";

import {
    Button,
    Surface,
    Text,
} from "@/shared/components/ui";

import {
    PwaContext,
} from "./PwaContext";

interface InstallChoice {
    readonly outcome: "accepted" | "dismissed";
    readonly platform: string;
}

interface BeforeInstallPromptEvent extends Event {
    readonly userChoice: Promise<InstallChoice>;
    prompt: () => Promise<void>;
}

interface NavigatorWithStandalone extends Navigator {
    readonly standalone?: boolean;
}

type UpdateServiceWorker = (
    reloadPage?: boolean,
) => Promise<void>;

function isRunningStandalone(): boolean {
    const navigatorWithStandalone =
        navigator as NavigatorWithStandalone;

    return (
        window.matchMedia(
            "(display-mode: standalone)",
        ).matches ||
        navigatorWithStandalone.standalone === true
    );
}

function requiresManualInstallation(): boolean {
    const isAppleMobile =
        /iPad|iPhone|iPod/.test(
            navigator.userAgent,
        ) ||
        (
            navigator.platform === "MacIntel" &&
            navigator.maxTouchPoints > 1
        );

    return isAppleMobile && !isRunningStandalone();
}

export function PwaProvider({
    children,
}: PropsWithChildren) {
    const [
        installPrompt,
        setInstallPrompt,
    ] = useState<BeforeInstallPromptEvent | null>(null);
    const [
        isInstalled,
        setIsInstalled,
    ] = useState(isRunningStandalone);
    const [
        isOnline,
        setIsOnline,
    ] = useState(() => navigator.onLine);
    const [
        offlineReady,
        setOfflineReady,
    ] = useState(false);
    const [
        needRefresh,
        setNeedRefresh,
    ] = useState(false);
    const [
        registrationFailed,
        setRegistrationFailed,
    ] = useState(false);
    const [
        showInstallHelp,
        setShowInstallHelp,
    ] = useState(false);
    const updateServiceWorkerRef =
        useRef<UpdateServiceWorker | null>(null);

    useEffect(() => {
        function handleBeforeInstallPrompt(
            event: Event,
        ): void {
            event.preventDefault();
            setInstallPrompt(
                event as BeforeInstallPromptEvent,
            );
        }

        function handleAppInstalled(): void {
            setInstallPrompt(null);
            setIsInstalled(true);
        }

        function handleOnline(): void {
            setIsOnline(true);
        }

        function handleOffline(): void {
            setIsOnline(false);
        }

        window.addEventListener(
            "beforeinstallprompt",
            handleBeforeInstallPrompt,
        );
        window.addEventListener(
            "appinstalled",
            handleAppInstalled,
        );
        window.addEventListener(
            "online",
            handleOnline,
        );
        window.addEventListener(
            "offline",
            handleOffline,
        );

        return () => {
            window.removeEventListener(
                "beforeinstallprompt",
                handleBeforeInstallPrompt,
            );
            window.removeEventListener(
                "appinstalled",
                handleAppInstalled,
            );
            window.removeEventListener(
                "online",
                handleOnline,
            );
            window.removeEventListener(
                "offline",
                handleOffline,
            );
        };
    }, []);

    useEffect(() => {
        if (!("serviceWorker" in navigator)) {
            return;
        }

        updateServiceWorkerRef.current = registerSW({
            immediate: true,
            onNeedRefresh: () => {
                setNeedRefresh(true);
            },
            onOfflineReady: () => {
                setOfflineReady(true);
            },
            onRegisterError: () => {
                setRegistrationFailed(true);
            },
        });
    }, []);

    const installApp = useCallback(async () => {
        if (installPrompt === null) {
            if (requiresManualInstallation()) {
                setShowInstallHelp(true);
            }

            return;
        }

        await installPrompt.prompt();

        const choice = await installPrompt.userChoice;

        setInstallPrompt(null);

        if (choice.outcome === "accepted") {
            setIsInstalled(true);
        }
    }, [installPrompt]);

    const updateApp = useCallback(async () => {
        await updateServiceWorkerRef.current?.(true);
    }, []);

    const dismissFeedback = useCallback(() => {
        setNeedRefresh(false);
        setOfflineReady(false);
        setRegistrationFailed(false);
        setShowInstallHelp(false);
    }, []);

    const contextValue = useMemo(
        () => ({
            canInstall:
                (
                    installPrompt !== null ||
                    requiresManualInstallation()
                ) &&
                !isInstalled,
            installApp,
            isInstalled,
            isOnline,
        }),
        [
            installApp,
            installPrompt,
            isInstalled,
            isOnline,
        ],
    );

    const hasFeedback =
        offlineReady ||
        needRefresh ||
        registrationFailed ||
        showInstallHelp;

    return (
        <PwaContext.Provider value={contextValue}>
            {children}

            {hasFeedback ? (
                <div
                    aria-live="polite"
                    className="og3-pwa-feedback"
                >
                    <Surface
                        className="og3-pwa-feedback__surface"
                        role={
                            registrationFailed
                                ? "alert"
                                : "status"
                        }
                        variant="overlay"
                    >
                        <Text size="sm">
                            {showInstallHelp
                                ? "No Safari, toque em Compartilhar e depois em Adicionar à Tela de Início."
                                : registrationFailed
                                    ? "Não foi possível ativar os recursos offline."
                                    : needRefresh
                                        ? "Uma nova versão do OrganizeG3 está disponível."
                                        : "O OrganizeG3 está pronto para abrir sem conexão."}
                        </Text>

                        <div
                            className="og3-pwa-feedback__actions"
                        >
                            {needRefresh ? (
                                <Button
                                    onClick={() => {
                                        void updateApp();
                                    }}
                                    size="sm"
                                >
                                    Atualizar agora
                                </Button>
                            ) : null}

                            <Button
                                onClick={dismissFeedback}
                                size="sm"
                                variant="secondary"
                            >
                                Fechar
                            </Button>
                        </div>
                    </Surface>
                </div>
            ) : null}
        </PwaContext.Provider>
    );
}