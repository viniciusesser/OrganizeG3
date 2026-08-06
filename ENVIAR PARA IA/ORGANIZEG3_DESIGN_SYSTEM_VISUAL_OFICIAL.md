# ORGANIZEG3 — DESIGN SYSTEM VISUAL OFICIAL

> Documento normativo para aparência, ergonomia, componentes, iconografia, acessibilidade e implementação visual do OrganizeG3.

---

| Propriedade | Valor |
|---|---|
| Documento | `ORGANIZEG3_DESIGN_SYSTEM_VISUAL_OFICIAL.md` |
| Versão | `1.0.0` |
| Data | 2026-08-05 |
| Status | Proposta visual oficial para validação |
| Nome da direção visual | Industrial Clarity |
| Aplicação inicial | Desktop Windows com PySide6 |
| Aplicação futura | PWA React |
| Fonte de ícones | Icons8 |
| Família primária de ícones | Windows 11 Outline |
| Família complementar | Windows 11 Filled, apenas para estados ativos equivalentes |
| Temas | Claro e Escuro |
| Densidade padrão | Confortável |
| Unidade-base | 4 px |

---

# 1. Finalidade

Este documento define como o OrganizeG3 deverá parecer e se comportar visualmente.

Ele será a referência obrigatória para:

- Claude;
- desenvolvedores;
- designers;
- revisores;
- testes visuais;
- Desktop PySide6;
- PWA futura;
- documentos e relatórios;
- gráficos;
- componentes compartilhados;
- `theme_design`.

Nenhuma tela poderá escolher cores, tamanhos, fontes, bordas, sombras, ícones ou espaçamentos de maneira independente.

---

# 2. Direção visual

## 2.1 Nome

```text
Industrial Clarity
```

## 2.2 Conceito

A interface deverá transmitir:

```text
Organização

Precisão

Confiabilidade

Controle

Clareza

Eficiência

Maturidade

Robustez

Tecnologia sem aparência futurista exagerada
```

## 2.3 Referências conceituais

```text
Engenharia

Marcenaria organizada

Desenho técnico

Planejamento industrial

Painéis de controle

Documentação profissional

Ferramentas de precisão
```

## 2.4 O que evitar

```text
Neon excessivo

Gradientes decorativos

Efeitos de vidro sem função

Cards excessivamente arredondados

Sombras pesadas

Cores saturadas em grandes áreas

Visual infantil

Visual gamer

Visual de aplicativo móvel ampliado

Excesso de ícones coloridos

Textos pequenos demais

Tabelas apertadas demais

Interfaces com tudo dentro de cards
```

---

# 3. Personalidade da interface

A personalidade deverá ser:

```text
Séria, mas não fria

Técnica, mas compreensível

Compacta, mas não apertada

Moderna, mas não passageira

Visualmente calma

Consistente

Direta
```

A interface deverá priorizar conteúdo, não decoração.

---

# 4. Princípios visuais

1. A informação mais importante deverá possuir maior peso visual.

2. Ações primárias deverão ser facilmente identificáveis.

3. A interface não deverá depender exclusivamente de cor.

4. Estados deverão combinar cor, ícone e texto.

5. Tabelas deverão ser legíveis por longos períodos.

6. A densidade deverá ser adequada a um ERP.

7. Nenhuma página deverá usar mais de uma ação primária dominante.

8. Bordas e fundos deverão organizar sem criar excesso de caixas.

9. Espaçamento deverá indicar hierarquia.

10. O modo escuro deverá preservar contraste e não apenas inverter cores.

11. Todos os estados interativos deverão possuir foco visível.

12. A interface deverá ser utilizável com teclado.

13. Componentes semelhantes deverão parecer e funcionar da mesma maneira.

14. A aparência será centralizada no `theme_design`.

---

# 5. Sistema de cores

## 5.1 Identidade principal

### Azul Engenharia

Cor de ação, seleção, foco e links.

| Token | Hex | Uso |
|---|---:|---|
| `brand.primary.50` | `#EFF6FF` | fundo suave |
| `brand.primary.100` | `#DBEAFE` | seleção leve |
| `brand.primary.200` | `#BFDBFE` | borda selecionada |
| `brand.primary.300` | `#93C5FD` | apoio |
| `brand.primary.400` | `#60A5FA` | destaque escuro |
| `brand.primary.500` | `#3B82F6` | destaque |
| `brand.primary.600` | `#2563EB` | ação principal |
| `brand.primary.700` | `#1D4ED8` | hover principal |
| `brand.primary.800` | `#1E40AF` | pressed |
| `brand.primary.900` | `#1E3A8A` | texto forte |
| `brand.primary.950` | `#172554` | fundo profundo |

### Âmbar Madeira

Cor de identidade secundária, usada com moderação.

| Token | Hex | Uso |
|---|---:|---|
| `brand.wood.50` | `#FFFBEB` | fundo leve |
| `brand.wood.100` | `#FEF3C7` | seleção especial |
| `brand.wood.200` | `#FDE68A` | borda |
| `brand.wood.300` | `#FCD34D` | destaque |
| `brand.wood.400` | `#FBBF24` | destaque |
| `brand.wood.500` | `#D99A16` | elemento de marca |
| `brand.wood.600` | `#B7791F` | identidade |
| `brand.wood.700` | `#A16207` | texto sobre fundo claro |
| `brand.wood.800` | `#854D0E` | pressed |
| `brand.wood.900` | `#713F12` | forte |

O âmbar não substituirá o azul nos botões principais.

---

# 6. Tema claro — Linho Técnico

## 6.1 Superfícies

| Token | Hex | Uso |
|---|---:|---|
| `light.canvas` | `#F4F7FA` | fundo geral |
| `light.surface` | `#FFFFFF` | superfície principal |
| `light.surface.subtle` | `#F8FAFC` | superfície secundária |
| `light.surface.muted` | `#EEF2F6` | áreas inativas |
| `light.surface.hover` | `#F1F5F9` | hover |
| `light.surface.selected` | `#EAF2FF` | seleção |
| `light.surface.elevated` | `#FFFFFF` | dialogs e menus |
| `light.overlay` | `rgba(15, 23, 42, 0.48)` | backdrop |

## 6.2 Textos

| Token | Hex | Uso |
|---|---:|---|
| `light.text.primary` | `#18202A` | texto principal |
| `light.text.secondary` | `#4A5868` | texto secundário |
| `light.text.tertiary` | `#6F7D8C` | metadados |
| `light.text.disabled` | `#9AA6B2` | desabilitado |
| `light.text.inverse` | `#FFFFFF` | sobre fundo escuro |
| `light.text.link` | `#1D4ED8` | link |

## 6.3 Bordas

| Token | Hex | Uso |
|---|---:|---|
| `light.border.subtle` | `#E4EAF0` | divisória leve |
| `light.border.default` | `#D4DDE6` | inputs e cards |
| `light.border.strong` | `#AAB7C4` | separação forte |
| `light.border.focus` | `#2563EB` | foco |
| `light.border.selected` | `#3B82F6` | seleção |

---

# 7. Tema escuro — Grafite Oficina

## 7.1 Superfícies

| Token | Hex | Uso |
|---|---:|---|
| `dark.canvas` | `#0F151C` | fundo geral |
| `dark.surface` | `#151D26` | superfície principal |
| `dark.surface.subtle` | `#1A232D` | superfície secundária |
| `dark.surface.muted` | `#202B36` | áreas inativas |
| `dark.surface.hover` | `#25313D` | hover |
| `dark.surface.selected` | `#17345C` | seleção |
| `dark.surface.elevated` | `#1C2631` | dialogs e menus |
| `dark.overlay` | `rgba(0, 0, 0, 0.64)` | backdrop |

## 7.2 Textos

| Token | Hex | Uso |
|---|---:|---|
| `dark.text.primary` | `#F2F5F8` | texto principal |
| `dark.text.secondary` | `#C1CAD4` | texto secundário |
| `dark.text.tertiary` | `#8F9CAA` | metadados |
| `dark.text.disabled` | `#667482` | desabilitado |
| `dark.text.inverse` | `#0F151C` | sobre fundo claro |
| `dark.text.link` | `#7DB3FF` | link |

## 7.3 Bordas

| Token | Hex | Uso |
|---|---:|---|
| `dark.border.subtle` | `#24303B` | divisória leve |
| `dark.border.default` | `#33414F` | inputs e cards |
| `dark.border.strong` | `#536273` | separação forte |
| `dark.border.focus` | `#60A5FA` | foco |
| `dark.border.selected` | `#60A5FA` | seleção |

---

# 8. Cores semânticas

## 8.1 Sucesso

| Token | Claro | Escuro |
|---|---:|---:|
| `semantic.success.bg` | `#EAF7EF` | `#153524` |
| `semantic.success.border` | `#93D3AB` | `#2E7650` |
| `semantic.success.text` | `#116B3A` | `#72D99C` |
| `semantic.success.solid` | `#16844A` | `#2DBE70` |

## 8.2 Aviso

| Token | Claro | Escuro |
|---|---:|---:|
| `semantic.warning.bg` | `#FFF6DF` | `#3A2A11` |
| `semantic.warning.border` | `#EBC66D` | `#8A6525` |
| `semantic.warning.text` | `#8A5700` | `#F3C96A` |
| `semantic.warning.solid` | `#C57A0A` | `#E7A62A` |

## 8.3 Erro

| Token | Claro | Escuro |
|---|---:|---:|
| `semantic.error.bg` | `#FDEEEE` | `#3B1C1E` |
| `semantic.error.border` | `#E5A0A4` | `#8B3D43` |
| `semantic.error.text` | `#A72D35` | `#FF9298` |
| `semantic.error.solid` | `#C43D3D` | `#E85B63` |

## 8.4 Informação

| Token | Claro | Escuro |
|---|---:|---:|
| `semantic.info.bg` | `#EAF5FB` | `#122E3C` |
| `semantic.info.border` | `#91C8E2` | `#2B708F` |
| `semantic.info.text` | `#12628A` | `#77C9ED` |
| `semantic.info.solid` | `#1677B8` | `#39A7D8` |

---

# 9. Estados operacionais

As cores deverão ser reutilizadas de forma consistente.

| Estado | Família visual |
|---|---|
| Rascunho | neutro |
| Novo | azul |
| Planejado | índigo |
| Agendado | violeta |
| Confirmado | azul |
| Em andamento | ciano |
| Pausado | âmbar |
| Aguardando | amarelo |
| Bloqueado | laranja |
| Em risco | laranja |
| Atrasado | vermelho |
| Com pendência | âmbar |
| Aprovado | verde |
| Concluído | verde |
| Reprovado | vermelho |
| Cancelado | cinza |
| Arquivado | cinza |
| Inativo | cinza |

A cor exata será obtida pelo mapa de status central, nunca pela página.

---

# 10. Paleta de gráficos

## 10.1 Sequência categórica

```text
#2563EB
#0F8A8A
#7C3AED
#D97706
#16844A
#C43D3D
#1677B8
#A16207
#DB2777
#4F46E5
#64748B
#65A30D
```

## 10.2 Regras

1. Não utilizar vermelho e verde como única diferença.

2. Séries deverão possuir legenda.

3. Gráficos de linha deverão combinar cor e padrão quando necessário.

4. Valores negativos usarão cor de erro.

5. Valores positivos não serão sempre verdes; verde será reservado a significado favorável.

6. Gráficos não utilizarão sombras ou 3D.

7. Pizza e rosca terão no máximo seis categorias visíveis.

8. Acima de seis categorias, utilizar barras ou agrupar como “Outros”.

9. Eixos deverão possuir unidade.

10. Tooltips deverão mostrar valor completo e período.

---

# 11. Tipografia

## 11.1 Família oficial

Desktop Windows:

```text
Segoe UI Variable
Segoe UI
Arial
sans-serif
```

PWA:

```css
font-family:
  "Segoe UI Variable",
  "Segoe UI",
  Inter,
  Arial,
  sans-serif;
```

Não será necessário distribuir arquivos de fonte na fase inicial.

---

# 12. Escala tipográfica

| Token | Tamanho | Peso | Altura de linha | Uso |
|---|---:|---:|---:|---|
| `type.display.lg` | 40 px | 700 | 48 px | números executivos |
| `type.display.md` | 32 px | 700 | 40 px | destaque de dashboard |
| `type.heading.1` | 28 px | 700 | 36 px | título principal raro |
| `type.heading.2` | 24 px | 700 | 32 px | título de página |
| `type.heading.3` | 20 px | 650 | 28 px | seção principal |
| `type.heading.4` | 18 px | 650 | 26 px | card ou subseção |
| `type.body.lg` | 16 px | 400 | 24 px | introduções |
| `type.body.md` | 14 px | 400 | 21 px | texto padrão |
| `type.body.sm` | 13 px | 400 | 19 px | tabelas e metadados |
| `type.label.md` | 13 px | 600 | 18 px | labels |
| `type.label.sm` | 12 px | 600 | 16 px | badges e cabeçalhos |
| `type.caption` | 11 px | 400 | 15 px | apoio não crítico |
| `type.code` | 13 px | 400 | 19 px | códigos e IDs |

O menor texto permitido para conteúdo relevante será 12 px.

11 px será reservado para informação complementar.

---

# 13. Pesos

```text
400 — texto comum

500 — ênfase moderada

600 — labels, botões e títulos menores

650 — títulos de seção quando disponível

700 — títulos e números principais
```

Não utilizar peso 300.

Não utilizar peso 800 ou 900 em telas operacionais.

---

# 14. Regras de texto

1. Títulos usarão sentence case.

2. Botões usarão verbos claros.

3. Evitar textos inteiros em caixa alta.

4. Códigos, siglas e IDs poderão usar caixa alta.

5. Colunas numéricas deverão alinhar à direita.

6. Colunas textuais deverão alinhar à esquerda.

7. Datas usarão formato local na apresentação.

8. Números não deverão quebrar em duas linhas.

9. Texto truncado deverá possuir tooltip.

10. Labels não deverão terminar com dois-pontos.

---

# 15. Sistema de espaçamento

Unidade-base:

```text
4 px
```

| Token | Valor |
|---|---:|
| `space.0` | 0 |
| `space.1` | 4 px |
| `space.2` | 8 px |
| `space.3` | 12 px |
| `space.4` | 16 px |
| `space.5` | 20 px |
| `space.6` | 24 px |
| `space.8` | 32 px |
| `space.10` | 40 px |
| `space.12` | 48 px |
| `space.16` | 64 px |

Padrão:

```text
Entre ícone e texto: 8 px

Entre campos relacionados: 12 px

Entre grupos de formulário: 24 px

Entre seções: 32 px

Padding de página: 24 px

Padding de dialog: 24 px

Padding de card: 16 ou 20 px
```

---

# 16. Raios de borda

| Token | Valor | Uso |
|---|---:|---|
| `radius.none` | 0 | tabelas contínuas |
| `radius.xs` | 3 px | pequenos indicadores |
| `radius.sm` | 5 px | inputs e badges |
| `radius.md` | 8 px | botões e cards |
| `radius.lg` | 12 px | dialogs e painéis |
| `radius.xl` | 16 px | superfícies especiais |
| `radius.full` | 999 px | status pills e avatar |

Evitar aparência excessivamente arredondada.

Cards padrão usarão 8 px.

---

# 17. Bordas

| Token | Valor |
|---|---|
| `border.width.default` | 1 px |
| `border.width.strong` | 2 px |
| `border.style` | solid |
| `focus.ring.width` | 2 px |
| `focus.ring.offset` | 2 px |

---

# 18. Sombras

## Tema claro

```text
shadow.sm:
0 1px 2px rgba(15, 23, 42, 0.08)

shadow.md:
0 4px 12px rgba(15, 23, 42, 0.10)

shadow.lg:
0 12px 32px rgba(15, 23, 42, 0.16)
```

## Tema escuro

```text
shadow.sm:
0 1px 2px rgba(0, 0, 0, 0.24)

shadow.md:
0 4px 14px rgba(0, 0, 0, 0.30)

shadow.lg:
0 16px 36px rgba(0, 0, 0, 0.40)
```

Uso:

```text
Cards comuns: sem sombra ou shadow.sm

Menus: shadow.md

Dialogs: shadow.lg

Tabelas: sem sombra
```

---

# 19. Movimento

| Token | Duração |
|---|---:|
| `motion.instant` | 0 ms |
| `motion.fast` | 100 ms |
| `motion.normal` | 160 ms |
| `motion.slow` | 240 ms |
| `motion.dialog` | 180 ms |

Curva:

```text
cubic-bezier(0.2, 0, 0, 1)
```

Não animar:

- grandes tabelas;
- valores críticos;
- carregamento por mais de 300 ms;
- mudanças que causem deslocamento inesperado.

Respeitar redução de movimento.

---

# 20. Métricas da janela

## 20.1 Desktop

```text
Resolução mínima suportada:
1280 × 720

Resolução recomendada:
1440 × 900 ou superior

Tamanho inicial:
1360 × 820

Tamanho mínimo da janela:
1180 × 680
```

## 20.2 Estrutura

| Elemento | Tamanho |
|---|---:|
| Barra superior | 56 px |
| Sidebar expandida | 248 px |
| Sidebar recolhida | 72 px |
| Rodapé de status | 28 px |
| Cabeçalho de página | mínimo 64 px |
| Padding horizontal da página | 24 px |
| Padding vertical da página | 20 px |

---

# 21. Densidade

## 21.1 Modos

```text
Compacta

Confortável

Ampla
```

## 21.2 Padrão

```text
Confortável
```

## 21.3 Alturas

| Componente | Compacta | Confortável | Ampla |
|---|---:|---:|---:|
| Input | 32 px | 38 px | 44 px |
| Botão | 32 px | 38 px | 44 px |
| Linha de tabela | 32 px | 40 px | 48 px |
| Cabeçalho de tabela | 34 px | 40 px | 44 px |
| Item de menu | 34 px | 40 px | 46 px |

A densidade poderá ser configurada pelo usuário.

---

# 22. Ícones

## 22.1 Origem

Os ícones serão baixados do Icons8.

Família primária:

```text
Windows 11 Outline
```

Família complementar:

```text
Windows 11 Filled
```

A família Filled será utilizada apenas quando houver equivalente exato e o estado ativo realmente exigir preenchimento.

---

# 23. Regras de iconografia

1. Não misturar famílias de ícones na mesma interface.

2. Utilizar SVG sempre que disponível.

3. Utilizar PNG apenas quando SVG não estiver disponível ou permitido.

4. Ícones serão monocromáticos por padrão.

5. A cor virá do estado do componente.

6. Não alterar proporção.

7. Não adicionar sombra ao ícone.

8. Não usar emojis como ícones funcionais.

9. Não usar ícones coloridos em menus comuns.

10. Todo botão somente com ícone deverá possuir tooltip.

11. Ações destrutivas usarão ícone e texto quando houver espaço.

12. Ícones decorativos deverão ser ocultados de leitores de acessibilidade.

---

# 24. Tamanhos de ícone

| Token | Tamanho | Uso |
|---|---:|---|
| `icon.xs` | 14 px | informação auxiliar |
| `icon.sm` | 16 px | tabelas e inputs |
| `icon.md` | 20 px | botões e navegação |
| `icon.lg` | 24 px | cabeçalhos e ações principais |
| `icon.xl` | 32 px | estados vazios |
| `icon.2xl` | 48 px | ilustração simples |

Tamanho padrão:

```text
20 px
```

Área clicável mínima:

```text
32 × 32 px no Desktop

40 × 40 px na PWA
```

---

# 25. Convenção de arquivos de ícones

```text
resources/icons/icons8/windows11-outline/
resources/icons/icons8/windows11-filled/
```

Nomes internos:

```text
add.svg
edit.svg
delete.svg
search.svg
filter.svg
refresh.svg
save.svg
close.svg
settings.svg
customer.svg
project.svg
budget.svg
purchase.svg
inventory.svg
production.svg
quality.svg
shipping.svg
installation.svg
finance.svg
hr.svg
fiscal.svg
dashboard.svg
```

Manter um manifesto:

```text
resources/icons/icon_manifest.json
```

Cada item deverá conter:

```text
nome interno

arquivo

família

origem

data de download

licença

uso

variante
```

---

# 26. Crédito do Icons8

Caso a licença gratuita seja utilizada, a aplicação deverá possuir crédito ao Icons8 na página:

```text
Ajuda → Sobre o OrganizeG3
```

Exemplo de texto:

```text
Ícones de interface fornecidos por Icons8.
```

A licença comercial adquirida deverá ser arquivada na documentação administrativa do projeto.

Não incluir arquivos baixados sem registro da origem e da licença aplicável.

---

# 27. Mapa funcional inicial de ícones

| Ação ou módulo | Nome de busca recomendado |
|---|---|
| Dashboard | dashboard |
| Clientes | customer |
| CRM | customer relationship |
| Projetos | project |
| Orçamentos | estimate |
| Compras | purchase order |
| Estoque | warehouse |
| PCP | planning |
| Produção | factory |
| Qualidade | quality |
| Expedição | shipping |
| Instalação | tools |
| Assistência | maintenance |
| Financeiro | accounting |
| RH | employee |
| Fiscal | invoice |
| BI | analytics |
| Configurações | settings |
| Novo | add |
| Editar | edit |
| Excluir | delete |
| Salvar | save |
| Cancelar | cancel |
| Fechar | close |
| Pesquisar | search |
| Filtrar | filter |
| Atualizar | refresh |
| Exportar | export |
| Imprimir | print |
| Anexar | attachment |
| Mais ações | more |
| Ajuda | help |
| Notificações | notification |
| Usuário | user |
| Sair | logout |

A busca poderá variar no site, mas a nomenclatura interna permanecerá em inglês.

---

# 28. Navegação principal

## 28.1 Sidebar

A sidebar conterá:

```text
Logo

Seletor de empresa

Módulos

Favoritos

Atalhos

Configurações

Ajuda
```

## 28.2 Estado expandido

```text
Largura: 248 px

Ícone: 20 px

Item: 40 px

Padding horizontal: 12 px

Gap ícone/texto: 10 px
```

## 28.3 Estado recolhido

```text
Largura: 72 px

Ícone centralizado

Tooltip obrigatório

Item ativo com fundo e indicador lateral
```

## 28.4 Item ativo

Tema claro:

```text
Fundo: brand.primary.50

Texto: brand.primary.700

Ícone: brand.primary.700

Indicador lateral: brand.primary.600
```

Tema escuro:

```text
Fundo: dark.surface.selected

Texto: dark.text.link

Ícone: dark.text.link

Indicador lateral: brand.primary.400
```

---

# 29. Barra superior

Altura:

```text
56 px
```

Elementos:

```text
Botão de recolher menu

Breadcrumb compacto

Pesquisa global

Sincronização

Notificações

Ajuda

Perfil do usuário
```

A barra superior não deverá competir visualmente com o conteúdo.

---

# 30. Cabeçalho de página

Estrutura:

```text
Breadcrumb

Título

Descrição opcional

Status ou contexto

Ações secundárias

Ação primária
```

Exemplo:

```text
Clientes / Carteira

Clientes

Gerencie cadastros, contatos e histórico comercial.

[Exportar] [Mais ações] [Novo cliente]
```

---

# 31. Breadcrumb

```text
Fonte: 12 px

Altura: 20 px

Cor padrão: texto terciário

Último item: texto secundário

Separador: chevron-right de 14 px
```

Não exibir mais de quatro níveis sem compactação.

---

# 32. Botões

## 32.1 Variantes

```text
Primary

Secondary

Tertiary

Ghost

Danger

Success

Link

Icon
```

---

# 33. Botão primário

Uso:

```text
A principal ação da área atual
```

Exemplo:

```text
Novo cliente

Salvar

Confirmar compra

Liberar produção
```

Visual claro:

```text
Fundo: brand.primary.600

Hover: brand.primary.700

Pressed: brand.primary.800

Texto: branco

Borda: transparente
```

Altura padrão:

```text
38 px
```

Padding:

```text
12 px horizontal

8 px vertical
```

---

# 34. Botão secundário

Visual:

```text
Fundo: superfície

Borda: border.default

Texto: text.primary

Hover: surface.hover
```

Uso:

```text
Exportar

Duplicar

Visualizar

Voltar
```

---

# 35. Botão terciário

Sem borda padrão.

Uso:

```text
Ação secundária de baixa ênfase
```

---

# 36. Botão destrutivo

Visual:

```text
Fundo: semantic.error.solid

Texto: branco
```

Ações destrutivas importantes deverão exigir confirmação.

Exemplo de confirmação:

```text
Excluir cliente?

Esta ação não poderá ser desfeita.

[Cancelar] [Excluir cliente]
```

Nunca usar apenas “Sim” e “Não”.

---

# 37. Botão somente com ícone

```text
Tamanho visual: 32 × 32 px

Ícone: 18 ou 20 px

Tooltip: obrigatório

Nome acessível: obrigatório
```

Em ações críticas, preferir ícone + texto.

---

# 38. Estados dos botões

```text
Default

Hover

Pressed

Focus

Loading

Disabled
```

Loading:

```text
Spinner de 16 px

Texto preservado quando houver espaço

Clique bloqueado

Largura não deverá mudar
```

---

# 39. Campos de entrada

## 39.1 Estrutura

```text
Label

Campo

Ação opcional

Helper text

Mensagem de erro
```

## 39.2 Altura

```text
38 px padrão
```

## 39.3 Tipografia

```text
Label: 13 px, peso 600

Valor: 14 px

Placeholder: 14 px

Ajuda: 12 px

Erro: 12 px
```

---

# 40. Campo de texto

Visual padrão:

```text
Fundo: surface

Borda: border.default

Raio: 5 px

Padding horizontal: 10 px

Ícone opcional: 16 px
```

Foco:

```text
Borda: border.focus

Focus ring: 2 px com transparência
```

---

# 41. Estados dos campos

```text
Default

Hover

Focus

Filled

Read-only

Disabled

Error

Warning

Success

Loading
```

Read-only não deverá parecer desabilitado.

Read-only:

```text
Texto legível

Fundo sutil

Borda discreta

Permitir seleção e cópia
```

---

# 42. Placeholders

Placeholders serão exemplos, não labels.

Cor:

```text
text.tertiary
```

Exemplo correto:

```text
Label: CNPJ
Placeholder: 00.000.000/0000-00
```

---

# 43. Textarea

```text
Altura mínima: 88 px

Redimensionamento controlado

Contador opcional

Barra de rolagem quando necessário
```

---

# 44. Campo de busca

Elementos:

```text
Ícone de busca à esquerda

Texto

Botão limpar à direita

Atalho quando global
```

Pesquisa global:

```text
Largura: 320 a 480 px

Atalho: Ctrl+K
```

---

# 45. Select e combobox

Deverão possuir:

```text
Busca quando houver mais de 10 opções

Estado vazio

Opção limpar quando permitido

Teclado

Indicador de carregamento

Descrição opcional
```

Não utilizar dropdown enorme sem busca.

---

# 46. Autocomplete de entidade

Uso:

```text
Cliente

Fornecedor

Projeto

Produto

Material

Colaborador

Conta
```

Resultado:

```text
Nome principal

Código

Informação secundária

Status
```

O componente deverá permitir abrir o cadastro selecionado quando autorizado.

---

# 47. Campos especializados

```text
MoneyInput

DecimalInput

IntegerInput

PercentageInput

QuantityInput

DateInput

DateTimeInput

TimeInput

PhoneInput

DocumentInput

EmailInput

URLInput

PasswordInput

SearchInput

EntitySelector

ColorSelector controlado

FileSelector
```

Todos deverão reutilizar componentes compartilhados.

---

# 48. MoneyInput

```text
Alinhamento: direita

Fonte: tabular

Moeda visível

Casas decimais conforme moeda

Valor interno: Decimal

Nunca float
```

Exemplo:

```text
R$ 12.450,90
```

---

# 49. DateInput

```text
Formato visual: dd/MM/yyyy

Armazenamento: date

Ícone de calendário

Digitação permitida

Calendário acessível

Atalhos de teclado
```

---

# 50. Checkbox

```text
Caixa: 18 × 18 px

Label: 14 px

Gap: 8 px

Estados:
unchecked
checked
indeterminate
disabled
focus
```

---

# 51. Radio

Usar quando:

```text
Existe apenas uma opção possível

Número de opções é pequeno

Opções precisam permanecer visíveis
```

---

# 52. Switch

Usar apenas para configuração binária de efeito imediato.

Não utilizar para ações que exigem Salvar.

Labels:

```text
Ativo

Inativo
```

Não usar apenas cor para representar estado.

---

# 53. Formulários

## 53.1 Larguras

```text
Campo curto: 120 px

Campo médio: 240 px

Campo longo: 360 px

Campo expansível: 100%
```

## 53.2 Grade

Desktop:

```text
12 colunas

Gap: 16 px
```

## 53.3 Organização

```text
Seção

Título

Descrição opcional

Campos

Ações
```

Não colocar cinquenta campos em um único bloco visual.

---

# 54. Rodapé de formulário

Para formulários longos, utilizar barra fixa:

```text
Alterações não salvas

[Cancelar] [Salvar rascunho] [Salvar]
```

A barra deverá permanecer visível sem cobrir conteúdo.

---

# 55. Tabelas

## 55.1 Estrutura

```text
Título opcional

Resumo

Pesquisa

Filtros

Ações

Cabeçalho

Linhas

Seleção

Paginação

Estado vazio
```

## 55.2 Alturas

```text
Cabeçalho: 40 px

Linha confortável: 40 px

Linha compacta: 32 px

Linha ampla: 48 px
```

## 55.3 Tipografia

```text
Cabeçalho: 12 px, peso 600

Células: 13 px

Números: tabular

Metadados: 12 px
```

---

# 56. Aparência de tabela

Tema claro:

```text
Fundo do cabeçalho: #F8FAFC

Fundo da linha: #FFFFFF

Hover: #F3F6F9

Selecionada: #EAF2FF

Divisória: #E4EAF0
```

Tema escuro:

```text
Fundo do cabeçalho: #1A232D

Fundo da linha: #151D26

Hover: #202B36

Selecionada: #17345C

Divisória: #24303B
```

Não usar zebra striping por padrão.

Zebra somente em relatórios extensos sem seleção.

---

# 57. Alinhamento de colunas

```text
Texto: esquerda

Código: esquerda

Data: centro ou esquerda consistente

Status: esquerda

Quantidade: direita

Dinheiro: direita

Percentual: direita

Ações: direita
```

---

# 58. Cabeçalho de tabela

Deverá suportar:

```text
Ordenação

Tooltip

Redimensionamento

Ocultar coluna

Fixar coluna

Menu de coluna

Indicador de filtro
```

Não utilizar texto vertical.

---

# 59. Seleção em tabela

```text
Checkbox na primeira coluna

Linha selecionada com fundo

Contagem de selecionados

Barra de ações em lote
```

A seleção não deverá ocorrer apenas pela cor da linha.

---

# 60. Ações de linha

Padrão:

```text
Ação principal visível

Menu de três pontos para demais ações
```

Exemplo:

```text
[Abrir] [⋯]
```

Não colocar seis ícones em todas as linhas.

---

# 61. Paginação

```text
Itens por página

Contagem total

Página atual

Anterior

Próxima

Ir para página quando necessário
```

Padrões:

```text
25

50

100
```

Não carregar milhares de registros no modelo visual.

---

# 62. Estados de tabela

## Loading

```text
Skeleton de linhas

Cabeçalho preservado
```

## Vazio

```text
Ícone

Título

Descrição

Ação quando aplicável
```

Exemplo:

```text
Nenhum cliente cadastrado

Cadastre o primeiro cliente para iniciar a carteira.

[Novo cliente]
```

## Sem resultado

```text
Nenhum resultado encontrado

Revise a pesquisa ou limpe os filtros.

[Limpar filtros]
```

## Erro

```text
Não foi possível carregar os clientes.

[Tentar novamente]
```

---

# 63. Cards

## 63.1 Uso

Cards serão utilizados para:

- indicadores;
- resumos;
- grupos;
- objetos em galerias;
- estados vazios;
- atalhos.

Não envolver toda seção em card por padrão.

## 63.2 Card padrão

```text
Raio: 8 px

Borda: 1 px

Padding: 16 px

Sombra: nenhuma ou sm

Título: 14 ou 16 px, peso 600
```

---

# 64. KPI Card

Estrutura:

```text
Label

Valor

Variação

Período

Contexto

Link de detalhamento
```

Exemplo:

```text
Receita no mês

R$ 184.500

+8,4% em relação ao mês anterior
```

Números:

```text
24 a 32 px

Peso 700

Tabular
```

---

# 65. Status badge

Altura:

```text
22 px
```

Estrutura:

```text
Indicador opcional

Texto

Ícone opcional
```

Padding:

```text
4 px vertical

8 px horizontal
```

Fonte:

```text
12 px, peso 600
```

Não utilizar badge somente colorido sem texto em informações críticas.

---

# 66. Chips e tags

Uso:

```text
Filtros

Categorias

Competências

Etiquetas
```

Não usar chip para status operacional se um badge semântico for mais claro.

---

# 67. Tabs

Altura:

```text
40 px
```

Estado ativo:

```text
Texto forte

Indicador inferior de 2 px

Sem fundo excessivo
```

Para mais de oito tabs, utilizar:

- agrupamento;
- rolagem;
- menu “Mais”;
- navegação secundária.

---

# 68. Accordion

Uso:

```text
Conteúdo opcional

Configurações

Ajuda

Detalhes técnicos
```

Não utilizar para esconder informações obrigatórias de formulários críticos.

---

# 69. Dialogs

## 69.1 Tamanhos

| Token | Largura |
|---|---:|
| `dialog.sm` | 420 px |
| `dialog.md` | 560 px |
| `dialog.lg` | 760 px |
| `dialog.xl` | 960 px |

## 69.2 Estrutura

```text
Título

Descrição opcional

Conteúdo

Mensagem de validação

Rodapé

Cancelar

Ação principal
```

## 69.3 Regras

1. Não abrir dialog sobre dialog, salvo confirmação controlada.

2. Dialogs extensos deverão virar páginas ou drawers.

3. Escape fechará apenas quando seguro.

4. Alterações não salvas deverão ser confirmadas.

5. O foco inicial deverá ser controlado.

6. Ao fechar, o foco retornará ao elemento de origem.

---

# 70. Drawer lateral

Uso:

```text
Detalhamento rápido

Filtros avançados

Visualização complementar

Histórico

Auditoria
```

Larguras:

```text
400 px

520 px

640 px
```

Não utilizar drawer para formulários muito complexos.

---

# 71. Menus

```text
Item: 36 px

Ícone: 16 ou 20 px

Atalho à direita

Separadores discretos

Ação destrutiva separada
```

Menus deverão permanecer dentro da tela.

---

# 72. Tooltip

```text
Atraso: 500 ms

Fonte: 12 px

Largura máxima: 280 px

Raio: 5 px

Padding: 6 × 8 px
```

Não utilizar tooltip para esconder informações essenciais.

---

# 73. Toasts

Posição:

```text
Canto superior direito
```

Tipos:

```text
Sucesso

Erro

Aviso

Informação

Progresso
```

Duração:

```text
Sucesso: 4 s

Informação: 5 s

Aviso: 7 s

Erro: persistente ou 10 s
```

Erros importantes deverão permitir copiar referência técnica.

---

# 74. Alertas inline

Uso:

```text
Mensagem contextual dentro da página
```

Estrutura:

```text
Ícone

Título

Descrição

Ação opcional
```

---

# 75. Confirmações

Confirmações deverão explicar:

```text
O que acontecerá

O impacto

Se é reversível

Qual entidade será afetada
```

Exemplo:

```text
Cancelar ordem de produção?

A ordem OP-2026-00142 será cancelada e não poderá receber novos apontamentos.

[Voltar] [Cancelar ordem]
```

---

# 76. Loading

## Spinner

Uso:

```text
Ações curtas e localizadas
```

Tamanhos:

```text
16 px

20 px

24 px

32 px
```

## Skeleton

Uso:

```text
Página

Cards

Tabelas

Listas
```

## Progress bar

Uso:

```text
Importação

Exportação

Backup

Sincronização

Upload
```

Sempre que possível, mostrar percentual e etapa atual.

---

# 77. Barra de progresso

```text
Altura: 6 px padrão

Altura: 10 px com percentual

Raio: full
```

Cores deverão refletir processo, não decoração.

---

# 78. Navegação por teclado

Padrões:

```text
Tab — próximo controle

Shift+Tab — controle anterior

Enter — ação principal ou abrir

Space — selecionar

Escape — fechar contexto seguro

Ctrl+S — salvar

Ctrl+F — pesquisar na página

Ctrl+K — pesquisa global

F5 — atualizar

Delete — solicitar exclusão quando permitido
```

Atalhos deverão ser configuráveis no futuro.

---

# 79. Foco

O foco deverá ser visível em todos os temas.

```text
Anel: 2 px

Offset: 2 px

Cor: brand.primary
```

Não remover outline sem substituição.

---

# 80. Kanban

## Estrutura

```text
Cabeçalho da coluna

Contagem

Limite opcional

Cards

Ações
```

## Card

```text
Código

Título

Cliente ou projeto

Responsável

Prazo

Status

Alertas
```

## Regras

1. Drag and drop não será obrigatório.

2. Mover deverá ser possível por clique.

3. Toda mudança de etapa deverá validar regras.

4. Colunas não deverão se sobrepor.

5. Cards simultâneos serão lado a lado quando o contexto exigir.

6. Estado atrasado deverá possuir texto ou ícone além da cor.

---

# 81. Agenda e calendário

## Visualizações

```text
Dia

Semana

Mês

Timeline

Lista
```

## Regras

```text
Sem drag and drop como única forma

Edição por clique

Eventos simultâneos lado a lado

Sem sobreposição ilegível

Cores por status ou recurso

Texto mínimo legível

Tooltip com detalhes

Linha de hora atual
```

Alturas e densidade serão configuráveis.

---

# 82. Timeline

Elementos:

```text
Data e hora

Ícone

Título

Descrição

Responsável

Origem

Anexos

Ações
```

Eventos recentes no topo por padrão.

---

# 83. Árvore

Uso:

```text
Estruturas

Categorias

Projetos

Produtos

Plano de contas

Organograma

Documentos
```

Deverá suportar:

```text
Expandir

Recolher

Pesquisa

Seleção

Teclado

Estado parcial
```

---

# 84. Upload de arquivos

Estrutura:

```text
Selecionar arquivo

Área de soltura opcional

Lista

Progresso

Status

Remover

Tentar novamente
```

Drag and drop será opcional.

Deverá existir botão “Selecionar arquivo”.

---

# 85. Visualizador de documentos

Suportará:

```text
PDF

Imagem

Metadados

Versões

Download

Abrir externamente

Histórico
```

---

# 86. Painel de auditoria

Estrutura:

```text
Data

Usuário

Ação

Entidade

Valor anterior

Valor posterior

Justificativa

Origem

Correlação
```

Diferenças deverão ser destacadas de forma legível.

---

# 87. Barra de aprovação

Uso em:

```text
Orçamentos

Compras

Pagamentos

Qualidade

Fiscal

RH
```

Estrutura:

```text
Estado

Alçada

Pendências

Histórico

Aprovar

Rejeitar

Solicitar ajuste
```

Aprovar e rejeitar não deverão possuir o mesmo peso visual.

---

# 88. Pesquisa global

Atalho:

```text
Ctrl+K
```

Resultados agrupados:

```text
Clientes

Projetos

Orçamentos

Pedidos

Produção

Documentos

Configurações
```

Cada resultado exibirá:

```text
Ícone

Título

Código

Descrição

Módulo
```

---

# 89. Filtros

## Barra rápida

```text
Pesquisa

Período

Status

Responsável

Mais filtros

Limpar
```

## Drawer avançado

```text
Grupos de filtros

Valores aplicados

Contagem de resultados

Aplicar

Limpar
```

Filtros ativos serão visíveis como chips removíveis.

---

# 90. Dashboards

Estrutura:

```text
Título

Período

Filtros

Última atualização

KPIs

Gráficos

Tabelas

Alertas
```

Não colocar mais de seis KPIs principais na primeira linha.

Dashboards operacionais priorizarão ação.

Dashboards executivos priorizarão comparação e tendência.

---

# 91. Gráficos

## Linha

Uso:

```text
Evolução temporal
```

## Barras

Uso:

```text
Comparar categorias
```

## Área

Uso:

```text
Volume acumulado
```

## Pizza ou rosca

Uso:

```text
Composição simples
```

## Funil

Uso:

```text
Conversão comercial
```

## Medidor

Uso:

```text
Meta com limite conhecido
```

Evitar excesso de medidores.

---

# 92. Formato de números

```text
Inteiro: 1.250

Decimal: 1.250,50

Dinheiro: R$ 1.250,50

Percentual: 12,5%

Quantidade: 12,500 m²

Data: 05/08/2026

Data e hora: 05/08/2026 14:30
```

Unidade deverá aparecer.

---

# 93. Avatares

Tamanhos:

```text
24 px

32 px

40 px

48 px
```

Sem foto:

```text
Iniciais

Fundo gerado por token estável

Contraste adequado
```

---

# 94. Ilustrações

Ilustrações serão usadas apenas em:

- onboarding;
- estados vazios importantes;
- página de erro;
- ajuda;
- marketing interno.

Não utilizar ilustrações em cada card.

---

# 95. Modo escuro

Regras:

1. Não usar preto puro como fundo principal.

2. Não usar branco puro em textos longos.

3. Reduzir contraste de bordas.

4. Aumentar luminosidade das cores semânticas.

5. Evitar grandes áreas de azul saturado.

6. Imagens e gráficos deverão ser adaptados.

7. Sombras serão mais discretas e profundas.

8. Inputs continuarão claramente identificáveis.

9. Tabelas deverão possuir separação visível.

10. Foco deverá permanecer evidente.

---

# 96. Acessibilidade

## Contraste

```text
Texto comum: mínimo 4.5:1

Texto grande: mínimo 3:1

Componentes e foco: mínimo 3:1
```

## Outros requisitos

```text
Teclado completo

Foco visível

Nome acessível

Tooltip em ícones

Mensagens de erro associadas

Ordem lógica

Não depender de cor

Redução de movimento

Escala de interface

Texto selecionável quando aplicável
```

---

# 97. Escala da interface

Opções futuras:

```text
90%

100%

110%

125%
```

O layout deverá tolerar aumento de fonte e DPI do Windows.

Não fixar dimensões que cortem texto.

---

# 98. Responsividade Desktop

Ao reduzir a janela:

```text
Sidebar recolhe

Filtros avançados migram para drawer

Ações secundárias migram para menu

Cards mudam de coluna

Tabelas preservam colunas prioritárias

Conteúdo não se sobrepõe
```

Não reduzir fontes para fazer o conteúdo caber.

---

# 99. PWA futura

Breakpoints:

```text
sm: 640 px

md: 768 px

lg: 1024 px

xl: 1280 px

2xl: 1536 px
```

No mobile:

- sidebar vira drawer;
- tabelas podem virar listas ou cards controlados;
- ações primárias permanecem visíveis;
- toque mínimo de 40 px;
- dialogs grandes viram tela cheia;
- filtros viram painel;
- navegação inferior poderá ser avaliada.

---

# 100. Padrões de página

## ListPage

```text
PageHeader

Summary opcional

FilterBar

DataTable

BulkActions

Pagination
```

## FormPage

```text
PageHeader

FormSections

ValidationSummary

StickyActionBar
```

## DetailPage

```text
PageHeader

Status

Summary

Tabs

Timeline

RelatedEntities

Actions
```

## DashboardPage

```text
PageHeader

Filters

KPIGrid

Charts

Alerts

Tables
```

## KanbanPage

```text
PageHeader

Filters

StageSummary

KanbanBoard
```

## CalendarPage

```text
PageHeader

ResourceFilters

CalendarToolbar

CalendarView

DetailsDrawer
```

---

# 101. Exemplo — Página de clientes

```text
┌───────────────────────────────────────────────────────────────────────────┐
│ Clientes                                              [Exportar] [Novo]  │
│ Gerencie cadastros, contatos e histórico comercial.                     │
├───────────────────────────────────────────────────────────────────────────┤
│ [Pesquisar clientes...] [Status ▾] [Cidade ▾] [Mais filtros]             │
├───────────────────────────────────────────────────────────────────────────┤
│ □  Cliente             Cidade       Telefone       Status       Ações    │
│ □  Antônio Marcos     Rosana/SP    (18) ...       Ativo        Abrir ⋯  │
│ □  Empresa Exemplo    Teodoro/SP   (18) ...       Lead         Abrir ⋯  │
├───────────────────────────────────────────────────────────────────────────┤
│ 1–25 de 184                                      [25 ▾]  ‹  1  2  3  › │
└───────────────────────────────────────────────────────────────────────────┘
```

---

# 102. Exemplo — Dashboard

```text
┌───────────────────────────────────────────────────────────────────────────┐
│ Visão geral                                     Período: Agosto de 2026  │
├────────────────┬────────────────┬────────────────┬────────────────────────┤
│ Receita        │ Pedidos        │ Em produção    │ Entregas no prazo      │
│ R$ 184.500     │ 28             │ 11             │ 92%                    │
│ +8,4%          │ +4             │ 3 em risco     │ -2,0 p.p.              │
├──────────────────────────────────┬────────────────────────────────────────┤
│ Receita por mês                  │ Situação dos projetos                  │
│ [gráfico de linha]               │ [gráfico de barras]                    │
├──────────────────────────────────┴────────────────────────────────────────┤
│ Alertas críticos                                                           │
│ • 3 materiais podem bloquear a produção                                   │
│ • 2 contas vencem hoje                                                     │
└───────────────────────────────────────────────────────────────────────────┘
```

---

# 103. Exemplo — Formulário

```text
Dados gerais

Nome do cliente *
[____________________________________________________________]

Tipo de pessoa *                 CPF/CNPJ *
[Pessoa física ▾]                [________________________]

Telefone                         Email
[________________________]       [____________________________]

Endereço

CEP               Cidade                         Estado
[__________]      [________________________]     [SP ▾]

Alterações não salvas                       [Cancelar] [Salvar cliente]
```

---

# 104. Exemplo — Kanban de produção

```text
PREPARAÇÃO (4)      CORTE (3)          MONTAGEM (5)        ACABAMENTO (2)

OP-142               OP-139             OP-136               OP-128
Cliente A            Cliente B          Cliente C            Cliente D
Cozinha              Dormitório         Cozinha              Banheiro
Prazo: hoje          Prazo: amanhã      Em atraso            Prazo: 08/08
[Abrir] [Mover]      [Abrir] [Mover]    [Abrir] [Mover]      [Abrir] [Mover]
```

---

# 105. Exemplo — Dialog de confirmação

```text
Cancelar pedido?

O pedido PED-2026-0042 será cancelado. As reservas de estoque serão
liberadas e as ordens ainda não iniciadas serão interrompidas.

Motivo *
[____________________________________________________________]

[Voltar] [Cancelar pedido]
```

---

# 106. Conteúdo e linguagem

## Botões

Correto:

```text
Salvar cliente

Gerar orçamento

Confirmar recebimento

Liberar produção

Cancelar pedido
```

Evitar:

```text
OK

Processar

Executar

Sim

Não
```

## Erros

Correto:

```text
Não foi possível salvar o cliente porque o CNPJ já está cadastrado.
```

Evitar:

```text
Erro 500.
```

---

# 107. Ícones em botões

## Com texto

```text
[ícone adicionar] Novo cliente

[ícone exportar] Exportar

[ícone salvar] Salvar
```

## Sem texto

Permitido em:

```text
Fechar

Mais ações

Atualizar

Mostrar senha

Limpar busca
```

Tooltip obrigatório.

---

# 108. Estados vazios por contexto

## Primeiro uso

```text
Nenhum projeto cadastrado

Crie o primeiro projeto para iniciar o planejamento.

[Novo projeto]
```

## Filtro sem resultado

```text
Nenhum projeto encontrado

Não há projetos correspondentes aos filtros aplicados.

[Limpar filtros]
```

## Sem permissão

```text
Acesso restrito

Você não possui permissão para visualizar estes dados.
```

---

# 109. Estados de sincronização

| Estado | Exibição |
|---|---|
| Sincronizado | check + texto opcional |
| Alteração local | nuvem com indicador |
| Sincronizando | spinner |
| Sem conexão | nuvem desligada |
| Conflito | aviso vermelho |
| Falha | erro + tentar novamente |

O usuário não deverá interpretar a sincronização apenas pela cor.

---

# 110. Estados de edição

```text
Visualização

Editando

Alterações não salvas

Salvando

Salvo

Erro ao salvar

Conflito de versão
```

Conflito de versão deverá abrir comparação.

---

# 111. Design tokens obrigatórios

Categorias:

```text
colors

typography

spacing

radius

borders

shadows

motion

sizes

density

icons

components

charts

status
```

---

# 112. Estrutura sugerida do `theme_design`

```text
src/organizeg3/core/theme_design/
├── __init__.py
├── theme_manager.py
├── theme_context.py
├── token_registry.py
├── tokens/
│   ├── colors.py
│   ├── typography.py
│   ├── spacing.py
│   ├── radius.py
│   ├── shadows.py
│   ├── motion.py
│   ├── sizes.py
│   ├── density.py
│   └── status.py
├── icons/
│   ├── icon_manager.py
│   ├── icon_manifest.py
│   └── icon_names.py
├── components/
│   ├── buttons.py
│   ├── inputs.py
│   ├── tables.py
│   ├── cards.py
│   ├── dialogs.py
│   ├── navigation.py
│   └── feedback.py
├── qt/
│   ├── qss_builder.py
│   ├── palette_builder.py
│   └── widget_styler.py
└── themes/
    ├── light.py
    └── dark.py
```

---

# 113. Exemplo de tokens em Python

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class SpacingTokens:
    xs: int = 4
    sm: int = 8
    md: int = 12
    lg: int = 16
    xl: int = 24
    xxl: int = 32


@dataclass(frozen=True)
class TypographyTokens:
    body_size: int = 14
    body_small_size: int = 13
    label_size: int = 13
    page_title_size: int = 24
    section_title_size: int = 20
```

Os valores acima pertencem ao `theme_design`, nunca às telas.

---

# 114. Exemplo de uso correto

```python
button = PrimaryButton(
    text="Novo cliente",
    icon=icons.get(IconName.ADD),
)

layout.setContentsMargins(
    spacing.xl,
    spacing.xl,
    spacing.xl,
    spacing.xl,
)
```

---

# 115. Exemplo proibido

```python
button.setStyleSheet(
    "background: #2563EB; color: white; border-radius: 8px;"
)

layout.setContentsMargins(24, 24, 24, 24)
```

Mesmo que os números coincidam com os tokens, o uso direto será proibido nas telas.

---

# 116. Componentes compartilhados obrigatórios

```text
PrimaryButton

SecondaryButton

TertiaryButton

DangerButton

IconButton

TextInput

SearchInput

MoneyInput

QuantityInput

DateInput

EntitySelector

Checkbox

RadioButton

Switch

DataTable

FilterBar

StatusBadge

Tag

Card

KpiCard

PageHeader

Breadcrumb

Tabs

Dialog

Drawer

Toast

InlineAlert

EmptyState

LoadingState

ErrorState

Pagination

CommandPalette

AuditTimeline

DocumentViewer

FileUploader

ApprovalBar

KanbanBoard

CalendarView
```

---

# 117. Revisão de ícones

Antes de incorporar um ícone:

```text
Conferir família

Conferir licença

Conferir SVG

Conferir viewBox

Conferir nome

Conferir variante

Conferir contraste

Conferir correspondência com a ação

Registrar no manifesto
```

---

# 118. Checklist de uma nova página

```text
[ ] Usa PageHeader compartilhado
[ ] Usa tokens
[ ] Não possui cor hardcoded
[ ] Não possui fonte hardcoded
[ ] Não possui caminho de ícone direto
[ ] Possui estado loading
[ ] Possui estado vazio
[ ] Possui estado de erro
[ ] Possui foco visível
[ ] Funciona por teclado
[ ] Respeita permissões
[ ] Não bloqueia a UI
[ ] Possui tooltips quando necessários
[ ] Possui ações claras
[ ] Não depende somente de drag and drop
[ ] Funciona nos dois temas
[ ] Funciona nas densidades previstas
```

---

# 119. Checklist de uma tabela

```text
[ ] Cabeçalhos claros
[ ] Ordenação indicada
[ ] Números alinhados à direita
[ ] Status semântico
[ ] Paginação
[ ] Pesquisa
[ ] Filtros
[ ] Estado vazio
[ ] Estado sem resultado
[ ] Estado de erro
[ ] Loading
[ ] Ações agrupadas
[ ] Seleção em lote quando aplicável
[ ] Colunas configuráveis
[ ] Tooltip para truncamento
[ ] Teclado
```

---

# 120. Checklist de um formulário

```text
[ ] Labels persistentes
[ ] Campos obrigatórios indicados
[ ] Validação junto ao campo
[ ] Resumo de erros quando necessário
[ ] Ordem de tabulação
[ ] Atalhos
[ ] Read-only diferenciado
[ ] Disabled diferenciado
[ ] Botão salvar claro
[ ] Alerta de alterações não salvas
[ ] Campos especializados
[ ] Valores monetários com Decimal
[ ] Ajuda contextual
```

---

# 121. Instruções diretas para o Claude

Claude, este documento define a aparência oficial do OrganizeG3.

## 121.1 Regras obrigatórias

Você deverá:

1. Ler o `theme_design` atual antes de criar componentes.

2. Preservar componentes existentes que já seguem o padrão.

3. Migrar valores hardcoded gradualmente para tokens.

4. Criar componentes compartilhados antes de duplicar estilos.

5. Usar exclusivamente ícones registrados no `IconManager`.

6. Não carregar SVG diretamente pela tela.

7. Não adicionar emoji como ícone.

8. Implementar tema claro e escuro simultaneamente.

9. Implementar estados hover, pressed, focus e disabled.

10. Respeitar a densidade configurada.

11. Não bloquear a thread principal.

12. Não esconder ações críticas em menus sem necessidade.

13. Manter alternativa por clique para movimentações.

14. Preservar contraste e teclado.

15. Entregar exemplos visuais ou screenshots de componentes alterados.

---

# 122. Ordem de implementação visual

```text
1. Token Registry

2. Tema claro

3. Tema escuro

4. ThemeManager

5. IconManager

6. Botões

7. Inputs

8. Feedback e status

9. PageHeader e navegação

10. Tabelas

11. Forms

12. Dialogs e drawers

13. Cards e KPIs

14. Filtros e pesquisa

15. Timeline

16. Kanban

17. Calendário

18. Gráficos

19. Auditoria

20. Documentos
```

---

# 123. Primeira entrega visual

A primeira entrega do Claude deverá conter uma **Galeria de Componentes** executável com:

```text
Cores

Tipografia

Ícones

Botões

Inputs

Checkboxes

Radios

Switches

Badges

Cards

Tabela

Tabs

Alertas

Toasts

Dialogs

Loading

Estados vazios
```

Essa galeria deverá funcionar nos temas claro e escuro.

Nenhuma tela de negócio deverá ser redesenhada antes da aprovação da galeria.

---

# 124. Critérios de aceite da galeria

```text
Tema claro aprovado

Tema escuro aprovado

Fonte aprovada

Escala aprovada

Cores aprovadas

Ícones aprovados

Botões aprovados

Campos aprovados

Tabela aprovada

Dialogs aprovados

Estados aprovados

Densidade aprovada

Navegação por teclado aprovada
```

---

# 125. Decisões que exigem aprovação do proprietário

```text
Alterar cor principal

Alterar fonte

Alterar família de ícones

Alterar raio padrão

Alterar densidade padrão

Alterar estrutura da navegação

Alterar tamanho-base

Adicionar gradientes

Adicionar animações relevantes

Criar nova família visual
```

---

# 126. Licença e governança dos assets

Deverá existir:

```text
docs/licenses/icons8.md
```

Conteúdo:

```text
Plano utilizado

Termos aplicáveis

Data de verificação

Crédito necessário

Local do crédito

Responsável pela conta

Comprovante de licença quando aplicável

Famílias utilizadas
```

Nenhum asset será incorporado sem governança.

---

# 127. Resultado esperado

Ao aplicar este Design System, o OrganizeG3 deverá parecer:

```text
Um ERP industrial moderno

Uma ferramenta profissional de trabalho diário

Um produto consistente

Uma aplicação confortável por muitas horas

Uma interface adequada a dados densos

Um sistema confiável e organizado
```

Ele não deverá parecer:

```text
Um protótipo

Um painel genérico de template

Um aplicativo móvel ampliado

Um sistema antigo sem hierarquia

Um software gamer

Uma coleção de telas independentes
```

---

# 128. Próximo passo

```text
Criar a Galeria Visual Executável em PySide6

Arquivo sugerido:
src/organizeg3/devtools/design_gallery.py
```

A galeria será a prova visual da especificação e deverá ser aprovada antes da aplicação em todas as páginas.
