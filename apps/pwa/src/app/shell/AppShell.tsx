import {
    useState,
} from "react";
import type {
    ReactNode,
} from "react";

import {
    DesktopNavigation,
} from "@/app/navigation/DesktopNavigation";
import {
    MobileNavigation,
} from "@/app/navigation/MobileNavigation";
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
    readonly children: ReactNode;
}

export function AppShell({
    children,
}: AppShellProps) {
    const {
        canInstall,
        installApp,
        isOnline,
    } = usePwa();

    const [
        isMobileNavigationOpen,
        setIsMobileNavigationOpen,
    ] = useState(false);

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
                            tone="secondary"
                        >
                            Ambiente principal
                        </Text>
                    </div>
                </div>

                <div
                    className="og3-app-shell__header-end"
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
            >
                <div
                    className="og3-app-shell__content"
                >
                    {children}
                </div>
            </main>

            <MobileNavigation
                isOpen={
                    isMobileNavigationOpen
                }
                onClose={
                    closeMobileNavigation
                }
            />
        </div>
    );
}