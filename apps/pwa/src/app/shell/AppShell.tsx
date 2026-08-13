import {
    useEffect,
    useMemo,
    useState,
} from "react";
import type {
    ReactNode,
} from "react";
import {
    useLocation,
} from "react-router";

import {
    DesktopNavigation,
} from "@/app/navigation/DesktopNavigation";
import {
    MobileNavigation,
} from "@/app/navigation/MobileNavigation";
import {
    findNavigationContext,
    getNavigationContextLabel,
    getNavigationDocumentTitle,
} from "@/app/navigation/navigation";
import {
    usePwa,
} from "@/infrastructure/pwa/usePwa";
import {
    Badge,
    Button,
    Heading,
    Text,
} from "@/shared/components/ui";

export interface AppShellProps {
    readonly activeTenantName?:
    string | null;
    readonly children: ReactNode;
}

export function AppShell({
    activeTenantName = null,
    children,
}: AppShellProps) {
    const location =
        useLocation();

    const {
        canInstall,
        installApp,
        isOnline,
    } = usePwa();

    const [
        isMobileNavigationOpen,
        setIsMobileNavigationOpen,
    ] = useState(false);

    const navigationContext =
        useMemo(
            () =>
                findNavigationContext(
                    location.pathname,
                ),
            [
                location.pathname,
            ],
        );

    const normalizedTenantName =
        activeTenantName?.trim() ?? "";

    const tenantLabel =
        normalizedTenantName.length > 0
            ? normalizedTenantName
            : "Ambiente principal";

    const pageContextLabel =
        getNavigationContextLabel(
            navigationContext,
        );

    const pageTitle =
        getNavigationDocumentTitle(
            navigationContext,
        );

    useEffect(
        () => {
            const previousTitle =
                document.title;

            document.title =
                pageTitle;

            return () => {
                document.title =
                    previousTitle;
            };
        },
        [
            pageTitle,
        ],
    );

    function openMobileNavigation(): void {
        setIsMobileNavigationOpen(
            true,
        );
    }

    function closeMobileNavigation(): void {
        setIsMobileNavigationOpen(
            false,
        );
    }

    return (
        <div
            className="og3-app-shell"
        >
            <a
                className="og3-skip-link"
                href="#og3-main-content"
            >
                Ir para o conteúdo principal
            </a>

            <aside
                aria-label="Navegação principal"
                className="og3-app-shell__sidebar"
            >
                <div
                    className="og3-app-shell__brand"
                >
                    <Heading
                        level={4}
                    >
                        OrganizeG3
                    </Heading>
                </div>

                <div
                    className="og3-app-shell__sidebar-content"
                >
                    <DesktopNavigation />
                </div>
            </aside>

            <header
                className="og3-app-shell__header"
            >
                <div
                    className="og3-app-shell__header-start"
                >
                    <div
                        className="og3-app-shell__mobile-menu-trigger"
                    >
                        <Button
                            aria-controls="og3-mobile-navigation"
                            aria-expanded={
                                isMobileNavigationOpen
                            }
                            aria-haspopup="dialog"
                            onClick={
                                openMobileNavigation
                            }
                            size="sm"
                            variant="secondary"
                        >
                            Menu
                        </Button>
                    </div>

                    <div
                        className="og3-app-shell__mobile-brand"
                    >
                        <Heading
                            level={4}
                        >
                            OrganizeG3
                        </Heading>
                    </div>

                    <div
                        className="og3-app-shell__desktop-context"
                    >
                        <Text
                            size="sm"
                        >
                            {tenantLabel}
                        </Text>

                        <Text
                            size="sm"
                            tone="secondary"
                        >
                            {pageContextLabel}
                        </Text>
                    </div>
                </div>

                <div
                    className="og3-app-shell__header-end"
                >
                    <div
                        aria-atomic="true"
                        aria-live="polite"
                        className="og3-app-shell__status"
                        role="status"
                    >
                        <Badge
                            variant={
                                isOnline
                                    ? "success"
                                    : "warning"
                            }
                        >
                            {
                                isOnline
                                    ? "Online"
                                    : "Sem conexão"
                            }
                        </Badge>
                    </div>

                    {canInstall ? (
                        <Button
                            onClick={() => {
                                void installApp();
                            }}
                            size="sm"
                            variant="secondary"
                        >
                            Instalar aplicativo
                        </Button>
                    ) : null}
                </div>
            </header>

            <main
                className="og3-app-shell__main"
                id="og3-main-content"
                tabIndex={-1}
            >
                <div
                    className="og3-app-shell__content"
                >
                    {children}
                </div>
            </main>

            <MobileNavigation
                activeTenantName={
                    tenantLabel
                }
                isOpen={
                    isMobileNavigationOpen
                }
                onClose={
                    closeMobileNavigation
                }
                pageContextLabel={
                    pageContextLabel
                }
            />
        </div>
    );
}