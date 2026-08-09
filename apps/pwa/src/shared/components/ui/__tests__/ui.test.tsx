import {
    fireEvent,
    render,
    screen,
} from "@testing-library/react";
import {
    describe,
    expect,
    it,
    vi,
} from "vitest";

import {
    Badge,
    Button,
    Card,
    Heading,
    Input,
    Surface,
    Text,
} from "@/shared/components/ui";

describe("UI foundations", () => {
    it(
        "renders and activates a button",
        () => {
            const onClick = vi.fn();

            render(
                <Button onClick={onClick}>
                    Salvar
                </Button>,
            );

            fireEvent.click(
                screen.getByRole(
                    "button",
                    {
                        name: "Salvar",
                    },
                ),
            );

            expect(
                onClick,
            ).toHaveBeenCalledTimes(1);
        },
    );

    it(
        "renders an accessible input",
        () => {
            render(
                <Input
                    label="Nome"
                    placeholder="Informe o nome"
                    supportText="Campo obrigatório"
                />,
            );

            expect(
                screen.getByLabelText("Nome"),
            ).toHaveAttribute(
                "placeholder",
                "Informe o nome",
            );

            expect(
                screen.getByText(
                    "Campo obrigatório",
                ),
            ).toBeInTheDocument();
        },
    );

    it(
        "renders input validation feedback",
        () => {
            render(
                <Input
                    error="Nome inválido"
                    label="Nome"
                />,
            );

            expect(
                screen.getByRole("alert"),
            ).toHaveTextContent(
                "Nome inválido",
            );

            expect(
                screen.getByLabelText("Nome"),
            ).toHaveAttribute(
                "aria-invalid",
                "true",
            );
        },
    );

    it(
        "renders card regions",
        () => {
            render(
                <Card
                    footer="Rodapé"
                    header="Cabeçalho"
                >
                    Conteúdo
                </Card>,
            );

            expect(
                screen.getByText("Cabeçalho"),
            ).toBeInTheDocument();

            expect(
                screen.getByText("Conteúdo"),
            ).toBeInTheDocument();

            expect(
                screen.getByText("Rodapé"),
            ).toBeInTheDocument();
        },
    );

    it(
        "renders badge and surface variants",
        () => {
            render(
                <Surface variant="raised">
                    <Badge variant="success">
                        Ativo
                    </Badge>
                </Surface>,
            );

            expect(
                screen.getByText("Ativo"),
            ).toHaveClass(
                "og3-badge--success",
            );
        },
    );

    it(
        "renders semantic typography",
        () => {
            render(
                <>
                    <Heading level={1}>
                        OrganizeG3
                    </Heading>

                    <Text tone="muted">
                        Texto secundário
                    </Text>
                </>,
            );

            expect(
                screen.getByRole(
                    "heading",
                    {
                        level: 1,
                        name: "OrganizeG3",
                    },
                ),
            ).toBeInTheDocument();

            expect(
                screen.getByText(
                    "Texto secundário",
                ),
            ).toHaveClass(
                "og3-text--muted",
            );
        },
    );
});