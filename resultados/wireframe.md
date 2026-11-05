# Proposta do dashboard de HIV: Baixo Amazonas (SESPA)

**Público:** equipe de vigilância epidemiológica da SESPA.
**Base:** `dados/hiv_baixo_amazonas.csv`: notificações de HIV (SINAN) de residentes nos 13 municípios, 2016 a jun/2024.
**Origem da proposta:** etapas anteriores (`perfil_hiv.md`, `decisoes_limpeza.md`, `series_relatorio.md`, `achados_hiv.md`).

> Neste documento, os valores aparecem como `[n]` ou `[x%]`: são **lugares reservados**. O dashboard vai preenchê-los com cálculos feitos sobre a base, sem nenhum número digitado à mão.

---

## 1. Cinco perguntas que a equipe precisa responder rápido

| # | Pergunta | Indicadores (seção 2) | Visualização ideal | Por quê |
|---|---|---|---|---|
| 1 | **Quantos casos foram notificados e para onde vai a série?** | I1, I2, I3 | 3 cartões de número (total no período, último ano completo, variação) + **barras por ano**, com 2024 hachurado e marcado "parcial" | Barras mostram volume. O hachurado impede comparar 2024 (parcial) com anos cheios |
| 2 | **Quais municípios concentram as notificações e onde houve mudança fora do padrão?** | I1, I4, I2 | **Barras horizontais ordenadas** (total por município) + **mapa de calor município × ano** com o número escrito em cada célula | Santarém tem cerca de 2/3 dos casos e achata qualquer gráfico de linhas. O mapa de calor mostra os municípios pequenos sem perder Santarém |
| 3 | **Quem são as pessoas notificadas e o perfil está mudando?** | I5, I6, I7 | **Pirâmide etária** (faixa × sexo) + **barras 100% empilhadas** da categoria de exposição, comparando 2016–2019 com 2020–2023 | A pirâmide junta sexo e idade num gráfico só. Barras 100% mostram mudança de composição |
| 4 | **As gestantes estão sendo diagnosticadas a tempo e há transmissão vertical?** | I8, I9, I10 | Cartões (gestantes, % no 1º trimestre, casos de transmissão vertical) + **barras empilhadas por trimestre da gestação**, por ano | É o ponto de intervenção mais direto da vigilância (pré-natal) |
| 5 | **Os dados são confiáveis o bastante para decidir?** | I11, I12 | **Tabela de completude** com selo de status (ícone + texto: Bom / Atenção / Crítico) por campo e período + aviso fixo de ano parcial | Antes de agir sobre um número, a equipe precisa saber quanto dele é "ignorado" ou atraso |

---

## 2. Indicadores (12)

Fonte de todos: `dados/hiv_baixo_amazonas.csv` (SINAN, ficha de HIV adulto), gerada por `scripts/02_limpeza.py`. O recorte é sempre o dos filtros globais.

| # | Indicador | Fórmula | Colunas usadas | Regras de exibição |
|---|---|---|---|---|
| I1 | **Notificações de HIV** | contagem de registros | `ANO_NOTIF`, `MUNICIPIO` | Sempre com o rótulo "notificações", nunca "casos novos" ou "incidência" |
| I2 | **Variação anual (%)** | (n do ano − n do ano anterior) ÷ n do ano anterior × 100 | `ANO_NOTIF` | Só entre anos completos (2017–2023). Não exibir se o ano anterior tiver menos de 10 notificações |
| I3 | **Notificações no 1º semestre** | contagem com `MES_NOTIF` ≤ 6, por ano | `ANO_NOTIF`, `MES_NOTIF` | Única comparação permitida para 2024. Avisar que 2024 ainda pode receber registros atrasados |
| I4 | **Participação do município (%)** | n do município ÷ n dos 13 municípios × 100 | `MUNICIPIO` | Mostrar sempre junto com o número absoluto |
| I5 | **Razão homem/mulher** | n masculino ÷ n feminino | `SEXO` | Não exibir com menos de 10 mulheres no recorte |
| I6 | **% de 15 a 29 anos** (e mediana de idade) | n com idade entre 15 e 29 ÷ n com idade informada × 100; mediana de `IDADE_ANOS` | `IDADE_ANOS`, `FAIXA_ETARIA` | Denominador sem as idades ignoradas; informar quantas são |
| I7 | **Distribuição por categoria de exposição (%)** | n da categoria ÷ n total × 100 (Ignorado incluído no denominador e exibido) | `CAT_EXPOSICAO_GRUPO`, `SEXO` | Mostrar também separado por sexo. Rotular como "exposição informada" |
| I8 | **% de gestantes entre as mulheres notificadas** | n com `CS_GESTANT` 1 a 4 ÷ n mulheres × 100 | `GESTANTE`, `SEXO` | Nota fixa: gestantes têm ficha própria no SINAN, fora desta base |
| I9 | **% de gestantes notificadas no 1º trimestre** | n `CS_GESTANT` = 1 ÷ n `CS_GESTANT` 1 a 4 × 100 | `GESTANTE` | Ressalva: é o trimestre na notificação, não no diagnóstico |
| I10 | **Casos de transmissão vertical** | contagem com `ANT_REL_CA` = 80 | `CAT_EXPOSICAO_GRUPO` | Só número absoluto (são poucos casos) |
| I11 | **% notificados fora do município de residência** | n com `ID_MUNICIP` ≠ `ID_MN_RESI` ÷ n × 100, e para qual município foram | `ID_MUNICIP`, `ID_MN_RESI` | Mostra o fluxo de pacientes para o polo (Santarém). Ainda não calculado nas etapas anteriores |
| I12 | **Completude (% de ignorado) por campo** | n ignorado ou vazio ÷ n × 100, por campo | sexo, idade, raça/cor, escolaridade, exposição, gestante, evolução | Selo: Bom (< 5%), Atenção (5% a 10%), Crítico (> 10%). Sempre com ícone e texto, nunca só cor |

**Regra geral de números pequenos:** se o recorte filtrado tiver menos de 10 notificações, os percentuais são substituídos por "n insuficiente" e só o número absoluto aparece.

---

## 3. Filtros globais

Ficam numa linha fixa no topo de todas as abas, exceto Notas Metodológicas, e valem para todos os gráficos.

| Filtro | Tipo | Opções | Padrão | Observações |
|---|---|---|---|---|
| **Ano de notificação** | Intervalo (de–até) | 2016 … 2024 | **2016–2023** | 2024 aparece como "2024 (parcial, jan–jun)". Se o intervalo incluir 2024, aparece um aviso amarelo |
| **Município de residência** | Seleção múltipla | 13 municípios + atalhos "Todos", "Santarém" e "Demais 12" | Todos | Ordem alfabética. Ao lado do nome, o total do período, para a equipe ver o tamanho da amostra |
| **Sexo** | Seleção única | Todos, Masculino, Feminino | Todos | |
| **Faixa etária** | Seleção múltipla | <15, 15-19, 20-24, 25-29, 30-39, 40-49, 50-59, 60+, Ignorada | Todas | |

- Um chip no topo resume o recorte ativo, por exemplo: `2016–2023 · Todos os municípios · Ambos os sexos · Todas as idades · n = [n]`.
- Botão "Limpar filtros".
- Cada município mantém sempre a mesma cor, qualquer que seja o filtro, para que a cor não mude conforme o que está selecionado.

---

## 4. O que NÃO deve entrar (e por quê)

| Não incluir | Motivo |
|---|---|
| **Taxas por 100 mil habitantes, incidência, prevalência** | Não há população na pasta. Notificação não é incidência |
| **Ranking de "municípios de maior risco"** | Sem taxa, um número maior só reflete população maior ou mais testagem |
| **Mapa coroplético colorido pela contagem** | Pintar o mapa pelo número absoluto passa a ideia de risco. Também não há malha municipal na pasta |
| **Mortalidade, letalidade, sobrevida** | A evolução quase nunca é atualizada (98% constam como "vivo"). Exigiria cruzamento com o SIM |
| **Série mensal ou semanal** | Os registros entram em lotes (meses com 0 seguidos de picos), e a semana epidemiológica do diagnóstico (`SEM_DIAG`) está 100% vazia |
| **2025** | Não existe na base |
| **2024 comparado com anos cheios** (variação anual, média) | 2024 tem só janeiro a junho |
| **Percentuais de municípios pequenos sozinhos** | 7 municípios têm menos de 30 notificações em 2016–2024; 1 ou 2 casos mudam tudo |
| **Cruzamentos muito detalhados** (município × sexo × faixa × raça/cor) | Células com 1 a 4 pessoas não informam nada e podem permitir identificar alguém, principalmente em municípios pequenos e entre indígenas. Se o painel for divulgado para fora da SESPA, ocultar contagens de 1 a 4 |
| **Raça/cor como gráfico de destaque** | 95% parda; as outras categorias têm poucos casos. Fica só como tabela no Perfil |
| **Ocupação, exames laboratoriais, critérios clínicos (Rio de Janeiro/Caracas, CDC)** | Ocupação muito incompleta; os demais não respondem às perguntas da vigilância |
| **Categorias de exposição combinadas** (ex.: Homo/Drogas) | São poucos registros; ficam agrupadas |
| **Qualquer afirmação de causa** (ex.: "a pandemia reduziu…") | Os dados mostram associação no tempo, não causa |

---

## 5. Wireframe em texto

Layout pensado para monitor de 1280 px ou mais, que se reorganiza em coluna única em telas estreitas. Legenda: `[▤]` gráfico, `[#]` cartão de número, `[≡]` tabela, `⚠` aviso, `ⓘ` dica ao passar o mouse.

### Estrutura comum a todas as abas

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HIV · Baixo Amazonas (13 municípios)            SESPA · Vigilância Epidem.   │
│ Notificações SINAN · residentes · atualizado até 28/06/2024                  │
├──────────────────────────────────────────────────────────────────────────────┤
│ [Visão Geral] [Perfil dos casos] [Comparação entre municípios] [Notas Metod.]│
├──────────────────────────────────────────────────────────────────────────────┤
│ Ano: [2016 ▾]–[2023 ▾]  Município: [Todos ▾]  Sexo: [Todos ▾]               │
│ Faixa etária: [Todas ▾]                                    [Limpar filtros]  │
│ Recorte: 2016–2023 · Todos · Ambos · Todas · n = [n]                         │
│ ⚠ (só se 2024 estiver no intervalo) 2024 tem apenas jan–jun: não compare     │
│   com anos completos.                                                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Aba 1 — Visão Geral (perguntas 1 e 5)

```
┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐
│ [#] Notificações │ [#] Último ano   │ [#] Variação     │ [#] Participação │
│ no período       │ completo (2023)  │ 2022→2023        │ de Santarém      │
│     [n]          │     [n]          │    [±x%]         │    [x%]          │
│ I1               │ I1               │ I2               │ I4               │
└──────────────────┴──────────────────┴──────────────────┴──────────────────┘
┌───────────────────────────────────────────────┬────────────────────────────┐
│ [▤] Notificações por ano (I1)                 │ [▤] 1º semestre por ano    │
│  barras azuis 2016…2023 · 2024 hachurado      │     (I3)                   │
│  valor no topo de cada barra                  │  barras jan–jun, 2016…2024 │
│  faixa cinza 2020–2021 "pandemia"             │  única comparação válida   │
│  ⓘ ano · n · variação vs. ano anterior        │  para 2024                 │
│  [ver como tabela]                            │  [ver como tabela]         │
└───────────────────────────────────────────────┴────────────────────────────┘
┌───────────────────────────────────────────────┬────────────────────────────┐
│ [▤] Santarém × demais 12 municípios (I1)      │ [≡] Qualidade dos dados    │
│  2 linhas (azul / laranja) com legenda;       │     (I12)                  │
│  2024 pontilhado                              │  Campo        %ign   Selo  │
│                                               │  Sexo         [x%]   ✔ Bom │
│                                               │  Idade        [x%]   ✔ Bom │
│                                               │  Escolaridade [x%]   ▲ At. │
│                                               │  Exposição    [x%]   ✔ Bom │
│                                               │  Evolução     [x%]   ✖ Crít│
│                                               │  (evolução: "Crítico" por  │
│                                               │   não ser atualizada)      │
└───────────────────────────────────────────────┴────────────────────────────┘
│ Notificação não é incidência: o número depende de testagem e registro.     │
│ Fonte: SINAN/MS · ficha HIV adulto · município de residência.              │
```

### Aba 2 — Perfil dos casos (perguntas 3 e 4)

```
┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐
│ [#] Razão H/M    │ [#] 15 a 29 anos │ [#] Mediana de   │ [#] Exposição    │
│     [x,x]        │     [x%]         │     idade [n]    │ ignorada [x%]    │
│ I5               │ I6               │ I6               │ I7 / I12         │
└──────────────────┴──────────────────┴──────────────────┴──────────────────┘
┌───────────────────────────────────────────────┬────────────────────────────┐
│ [▤] Pirâmide etária (I6, I5)                  │ [▤] Categoria de exposição │
│   Masculino ◄──────┼──────► Feminino          │     (I7)                   │
│   60+       ▇      │ ▏                        │  barras 100% empilhadas    │
│   50-59    ▇▇      │ ▇                        │  2016–2019 │███▓▓░░·│      │
│   40-49  ▇▇▇▇      │ ▇▇                       │  2020–2023 │██▓▓▓░·│       │
│   30-39 ▇▇▇▇▇▇     │ ▇▇▇                      │  Hétero/Homo/Bi/Vertical/  │
│   25-29 ▇▇▇▇▇      │ ▇▇                       │  Ignorado (legenda + rótulo│
│   20-24 ▇▇▇▇▇▇     │ ▇▇                       │  nos segmentos grandes)    │
│   15-19  ▇▇        │ ▇                        │  [Todos | Homens | Mulheres]│
│   <15              │                          │                            │
│  números ao passar o mouse; [ver como tabela] │  [ver como tabela]         │
└───────────────────────────────────────────────┴────────────────────────────┘
┌──────────────────┬──────────────────┬──────────────────┐
│ [#] Gestantes    │ [#] No 1º        │ [#] Transmissão  │
│  [n] de [n]      │  trimestre       │  vertical        │
│  mulheres [x%]   │     [x%]         │     [n]          │
│ I8               │ I9               │ I10              │
└──────────────────┴──────────────────┴──────────────────┘
┌───────────────────────────────────────────────┬────────────────────────────┐
│ [▤] Gestantes por trimestre, por ano (I8, I9) │ [≡] Raça/cor e escolaridade│
│  barras empilhadas: 1º / 2º / 3º / ignorado   │  tabela n e %, por período │
│  ⚠ gestantes têm ficha própria no SINAN;      │  ⚠ escolaridade mudou muito│
│    este painel pode não mostrar todas         │    após 2020 (provável     │
│                                               │    mudança de registro)    │
└───────────────────────────────────────────────┴────────────────────────────┘
│ Comparação entre períodos: "≠" marca diferença além do acaso (teste de       │
│ proporções, 5%); sem marca = pode ser oscilação.                             │
```

### Aba 3 — Comparação entre municípios (pergunta 2)

```
┌───────────────────────────────────────────────┬────────────────────────────┐
│ [▤] Notificações no período por município (I1)│ [≡] Resumo por município   │
│  barras horizontais ordenadas                 │  Município  n   %reg  Var. │
│  Santarém    ████████████████████  [n]        │  Santarém  [n] [x%] [±x%]  │
│  Oriximiná   ██  [n]                          │  Oriximiná [n] [x%] [±x%]  │
│  Óbidos      ██  [n]                          │  …                         │
│  …                                            │  Terra S.  [n] [x%]  n insuf│
│  Terra Santa ▏ [n]  (poucos casos)            │  (I1, I4, I2; "n insuf."   │
│  barras claras = < 30 notificações no período │   se ano anterior < 10)    │
└───────────────────────────────────────────────┴────────────────────────────┘
┌──────────────────────────────────────────────────────────────────────────────┐
│ [▤] Mapa de calor: município × ano (I1)                                      │
│              2016 2017 2018 2019 2020 2021 2022 2023 2024*                   │
│  Santarém    [n]  [n]  [n]  [n]  [n]  [n]  [n]  [n]  [n]                     │
│  Oriximiná   [n]  …                                                          │
│  …           (um tom de azul; número escrito em cada célula)                 │
│  ⓘ município · ano · n · participação no ano (I4)                            │
└──────────────────────────────────────────────────────────────────────────────┘
┌───────────────────────────────────────────────┬────────────────────────────┐
│ [▤] Onde os residentes foram notificados (I11)│ [▤] Participação de        │
│  barras: % notificado no próprio município ×  │     Santarém por ano (I4)  │
│  em outro (principalmente Santarém), por      │  linha 2016…2023           │
│  município de residência                      │                            │
└───────────────────────────────────────────────┴────────────────────────────┘
│ Números absolutos dependem do tamanho da população: não indicam risco.      │
```

### Aba 4 — Notas Metodológicas

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ 1. Fonte e recorte                                                           │
│    SINAN, ficha HIV adulto (B24) · arquivo HIV16_25.csv · notificações       │
│    2016 a 28/06/2024 · residentes nos 13 municípios (ID_MN_RESI)            │
│    · códigos IBGE conferidos (Curuá 1502855, Monte Alegre 1504802)           │
│ 2. Limitações (sempre visíveis)                                              │
│    • Notificação não é incidência; há subnotificação                        │
│    • 2024 parcial (jan–jun); 2025 não existe na base                        │
│    • Registros entram em lotes: não use leitura mensal                       │
│    • Evolução/óbito raramente atualizada; não mede mortalidade              │
│    • Gestantes e crianças têm fichas próprias no SINAN, fora desta base     │
│    • Municípios com < 30 notificações: percentuais instáveis                │
│ 3. Definições                                                                │
│    Ano = ano de notificação · Faixas etárias · Grupos de exposição ·         │
│    Escolaridade agrupada · o que conta como "Ignorado"                       │
│ 4. Indicadores: tabela com os 12 indicadores, fórmula e regra de exibição    │
│ 5. Tratamento dos dados: duplicados removidos (1), CRITERIO 900 (nenhum)     │
│    · links para decisoes_limpeza.md e scripts/                               │
│ 6. Atualização: como rodar scripts/02 → 03 → 04 com um novo arquivo SINAN    │
│ 7. Emergência e contato da equipe (a definir pela SESPA)                     │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Requisitos de acessibilidade e leitura

- Todo gráfico tem o botão **"ver como tabela"**.
- Cor nunca é a única forma de informação: há legenda, rótulos diretos, ícones nos selos de qualidade e hachura no ano parcial.
- Um eixo por gráfico. Cores fixas por série: Santarém sempre azul, demais sempre laranja.
- Os textos de aviso ficam no próprio painel, perto do gráfico a que se referem, e não só na aba de notas.
- Números no formato brasileiro (1.083; 67,9%).
