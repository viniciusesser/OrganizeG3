import { Link } from "react-router";

export function NotFoundRoute() {
    return (
        <main>
            <h1>Página não encontrada</h1>

            <p>
                A rota informada não existe.
            </p>

            <Link to="/">
                Voltar para o início
            </Link>
        </main>
    );
}