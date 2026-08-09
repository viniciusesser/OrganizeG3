import {
    ArchitectureStatus,
} from "@/shared/components/ArchitectureStatus";
import {
    Badge,
    Card,
    Heading,
    Text,
} from "@/shared/components/ui";

export function RootRoute() {
    return (
        <div className="og3-app-shell__page">
            <header
                className="og3-app-shell__page-header"
            >
                <div
                    className="og3-app-shell__page-heading"
                >
                    <Heading level={1}>
                        Visão geral
                    </Heading>

                    <Text tone="secondary">
                        Ambiente principal do OrganizeG3.
                    </Text>
                </div>

                <Badge variant="accent">
                    Fase 04
                </Badge>
            </header>

            <div
                className="og3-app-shell__page-grid"
            >
                <Card
                    header={
                        <Heading level={4}>
                            Plataforma
                        </Heading>
                    }
                >
                    <Text>
                        Frontend React integrado à
                        plataforma OrganizeG3.
                    </Text>
                </Card>

                <Card
                    header={
                        <Heading level={4}>
                            Interface
                        </Heading>
                    }
                >
                    <Text>
                        Design system centralizado e
                        estrutura de aplicação ativa.
                    </Text>
                </Card>

                <Card
                    header={
                        <Heading level={4}>
                            Próxima etapa
                        </Heading>
                    }
                >
                    <Text>
                        Navegação desktop e organização
                        dos módulos do sistema.
                    </Text>
                </Card>
            </div>

            <Card
                header={
                    <Heading level={4}>
                        Estado da API
                    </Heading>
                }
            >
                <ArchitectureStatus />
            </Card>
        </div>
    );
}