import {
    Badge,
    Card,
    Heading,
    Text,
} from "@/shared/components/ui";

export interface ModulePlaceholderRouteProps {
    readonly title: string;
    readonly description: string;
}

export function ModulePlaceholderRoute({
    title,
    description,
}: ModulePlaceholderRouteProps) {
    return (
        <div className="og3-module-placeholder">
            <header
                className="og3-module-placeholder__header"
            >
                <Badge variant="accent">
                    Módulo
                </Badge>

                <Heading level={1}>
                    {title}
                </Heading>

                <Text tone="secondary">
                    {description}
                </Text>
            </header>

            <div
                className="og3-module-placeholder__content"
            >
                <Card
                    header={
                        <Heading level={4}>
                            Integração preparada
                        </Heading>
                    }
                >
                    <Text>
                        A navegação para este módulo já está
                        integrada ao App Shell. A implementação
                        funcional da tela será realizada nas
                        próximas etapas da Fase 4.
                    </Text>
                </Card>
            </div>
        </div>
    );
}