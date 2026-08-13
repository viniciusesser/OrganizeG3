import {
    NavigationContent,
} from "@/app/navigation/NavigationContent";
import {
    useAccessibleOverlay,
} from "@/shared/hooks/useAccessibleOverlay";
import {
    Button,
    Heading,
    Text,
} from "@/shared/components/ui";

export interface MobileNavigationProps {
    readonly activeTenantName:
    string;
    readonly isOpen: boolean;
    readonly onClose: () => void;
    readonly pageContextLabel:
    string;
}

export function MobileNavigation({
    activeTenantName,
    isOpen,
    onClose,
    pageContextLabel,
}: MobileNavigationProps) {
    const {
        overlayRef,
    } = useAccessibleOverlay<HTMLElement>({
        isActive: isOpen,
        onClose,
    });

    if (!isOpen) {
        return null;
    }

    return (
        <div
            className="og3-mobile-navigation"
            data-testid="mobile-navigation"
        >
            <button
                aria-label="Fechar navegação"
                className="og3-mobile-navigation__backdrop"
                onClick={onClose}
                type="button"
            />

            <aside
                aria-label="Navegação móvel"
                aria-modal="true"
                className="og3-mobile-navigation__drawer"
                id="og3-mobile-navigation"
                ref={overlayRef}
                role="dialog"
                tabIndex={-1}
            >
                <header
                    className="og3-mobile-navigation__header"
                >
                    <div
                        className="og3-mobile-navigation__identity"
                    >
                        <Heading level={4}>
                            OrganizeG3
                        </Heading>

                        <Text
                            size="sm"
                        >
                            {activeTenantName}
                        </Text>

                        <Text
                            size="sm"
                            tone="secondary"
                        >
                            {pageContextLabel}
                        </Text>
                    </div>

                    <Button
                        data-og3-autofocus="true"
                        onClick={onClose}
                        size="sm"
                        variant="secondary"
                    >
                        Fechar
                    </Button>
                </header>

                <nav
                    aria-label="Módulos do sistema no celular"
                    className="og3-navigation og3-mobile-navigation__content"
                >
                    <NavigationContent
                        onNavigate={onClose}
                    />
                </nav>
            </aside>
        </div>
    );
}