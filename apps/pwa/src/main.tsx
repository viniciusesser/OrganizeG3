import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import { App } from "@/app/App";
import { AppProviders } from "@/app/providers/AppProviders";

import "./index.css";

const rootElement = document.getElementById("root");

if (rootElement === null) {
  throw new Error(
    "Não foi possível localizar o elemento raiz da aplicação.",
  );
}

createRoot(rootElement).render(
  <StrictMode>
    <AppProviders>
      <App />
    </AppProviders>
  </StrictMode>,
);