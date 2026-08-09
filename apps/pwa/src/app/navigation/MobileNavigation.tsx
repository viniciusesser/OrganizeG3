import {
    NavigationContent,
} from "@/app/navigation/NavigationContent";
import {
    Button,
    Heading,
} from "@/shared/components/ui";

export interface MobileNavigationProps {
    readonly isOpen: boolean;
    readonly onClose: () => void;
}

export function MobileNavigation({
    isOpen,
    onClose,
}: MobileNavigationProps) {
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
                role="dialog"
            >
                <header
                    className="og3-mobile-navigation__header"
                >
                    <Heading level={4}>
                        OrganizeG3
                    </Heading>

                    <Button
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