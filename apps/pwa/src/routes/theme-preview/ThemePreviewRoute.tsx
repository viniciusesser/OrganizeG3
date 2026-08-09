import {
    Badge,
    Button,
    Card,
    Heading,
    Input,
    Surface,
    Text,
} from "@/shared/components/ui";

export function ThemePreviewRoute() {
    return (
        <main className="og3-theme-preview">
            <div className="og3-theme-preview__content">
                <header className="og3-theme-preview__header">
                    <Badge variant="accent">
                        Theme Preview
                    </Badge>

                    <Heading level={1}>
                        OrganizeG3
                    </Heading>

                    <Text
                        size="lg"
                        tone="secondary"
                    >
                        Design system do OrganizeG3
                    </Text>

                    <Text tone="muted">
                        Esta página existe para validar
                        visualmente tokens, componentes e
                        estados antes de aplicá-los às telas
                        reais do sistema.
                    </Text>
                </header>

                <section className="og3-theme-preview__section">
                    <Heading level={2}>
                        Tipografia
                    </Heading>

                    <Card>
                        <div className="og3-theme-preview__section">
                            <Heading level={1}>
                                Heading 1
                            </Heading>

                            <Heading level={2}>
                                Heading 2
                            </Heading>

                            <Heading level={3}>
                                Heading 3
                            </Heading>

                            <Heading level={4}>
                                Heading 4
                            </Heading>

                            <Text size="lg">
                                Texto grande para destaques e
                                informações importantes.
                            </Text>

                            <Text>
                                Texto principal usado no conteúdo
                                normal da aplicação.
                            </Text>

                            <Text
                                size="sm"
                                tone="secondary"
                            >
                                Texto secundário para informações
                                auxiliares.
                            </Text>

                            <Text
                                size="sm"
                                tone="muted"
                            >
                                Texto muted para informações de
                                menor hierarquia.
                            </Text>
                        </div>
                    </Card>
                </section>

                <section className="og3-theme-preview__section">
                    <Heading level={2}>
                        Botões
                    </Heading>

                    <Card>
                        <div className="og3-theme-preview__stack">
                            <Button>
                                Primary
                            </Button>

                            <Button variant="secondary">
                                Secondary
                            </Button>

                            <Button variant="danger">
                                Danger
                            </Button>

                            <Button size="sm">
                                Small
                            </Button>

                            <Button size="lg">
                                Large
                            </Button>

                            <Button disabled>
                                Disabled
                            </Button>
                        </div>
                    </Card>
                </section>

                <section className="og3-theme-preview__section">
                    <Heading level={2}>
                        Campos
                    </Heading>

                    <div className="og3-theme-preview__grid">
                        <Card>
                            <div className="og3-theme-preview__form">
                                <Input
                                    label="Nome"
                                    placeholder="Informe o nome"
                                />

                                <Input
                                    label="E-mail"
                                    placeholder="usuario@empresa.com"
                                    supportText="Usado para comunicação."
                                />

                                <Input
                                    error="Campo obrigatório."
                                    label="Documento"
                                    placeholder="Informe o documento"
                                />

                                <Input
                                    disabled
                                    label="Campo desabilitado"
                                    value="Não editável"
                                    readOnly
                                />
                            </div>
                        </Card>
                    </div>
                </section>

                <section className="og3-theme-preview__section">
                    <Heading level={2}>
                        Badges e estados
                    </Heading>

                    <Card>
                        <div className="og3-theme-preview__status-list">
                            <Badge>
                                Neutral
                            </Badge>

                            <Badge variant="accent">
                                Accent
                            </Badge>

                            <Badge variant="success">
                                Ativo
                            </Badge>

                            <Badge variant="warning">
                                Atenção
                            </Badge>

                            <Badge variant="danger">
                                Erro
                            </Badge>
                        </div>
                    </Card>
                </section>

                <section className="og3-theme-preview__section">
                    <Heading level={2}>
                        Cards
                    </Heading>

                    <div className="og3-theme-preview__grid">
                        <Card
                            header={
                                <Heading level={4}>
                                    Cliente
                                </Heading>
                            }
                            footer={
                                <Text
                                    size="sm"
                                    tone="muted"
                                >
                                    Atualizado recentemente
                                </Text>
                            }
                        >
                            <Text>
                                Exemplo de card com cabeçalho,
                                conteúdo e rodapé.
                            </Text>
                        </Card>

                        <Card
                            header={
                                <Heading level={4}>
                                    Produção
                                </Heading>
                            }
                        >
                            <Text>
                                Estrutura pronta para receber
                                indicadores e informações de
                                processo.
                            </Text>
                        </Card>

                        <Card
                            header={
                                <Heading level={4}>
                                    Financeiro
                                </Heading>
                            }
                        >
                            <Text>
                                Exemplo de superfície elevada para
                                informações gerenciais.
                            </Text>
                        </Card>
                    </div>
                </section>

                <section className="og3-theme-preview__section">
                    <Heading level={2}>
                        Superfícies
                    </Heading>

                    <div className="og3-theme-preview__grid">
                        <Surface
                            className="og3-theme-preview__surface"
                            variant="base"
                        >
                            <Heading level={4}>
                                Base
                            </Heading>

                            <Text tone="secondary">
                                Superfície base.
                            </Text>
                        </Surface>

                        <Surface
                            className="og3-theme-preview__surface"
                            variant="raised"
                        >
                            <Heading level={4}>
                                Raised
                            </Heading>

                            <Text tone="secondary">
                                Superfície elevada.
                            </Text>
                        </Surface>

                        <Surface
                            className="og3-theme-preview__surface"
                            variant="overlay"
                        >
                            <Heading level={4}>
                                Overlay
                            </Heading>

                            <Text tone="secondary">
                                Superfície para elementos acima do
                                conteúdo principal.
                            </Text>
                        </Surface>
                    </div>
                </section>
            </div>
        </main>
    );
}