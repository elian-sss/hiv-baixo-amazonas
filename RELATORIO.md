# Relatório: dashboard de HIV do Baixo Amazonas (SESPA/PA)

**Disciplina:** Introdução à Ciência de Dados · **Formato:** análise de dados conversacional (pedidos em linguagem natural; código executado nesta pasta)
**Base:** notificações de HIV do SINAN (`HIV16_25.csv`) e dicionário de dados do Ministério da Saúde · **Data:** 05/11/2026
**Fonte do resumo:** `DIARIO.md` (registro de cada etapa). Todos os números vêm de cálculos registrados em `resultados/`.

---

## 1. Resumo do processo (uma página)

**Objetivo.** Dar à vigilância epidemiológica da SESPA um painel sobre as notificações de HIV em 13 municípios da Região de Saúde do Baixo Amazonas, de 2016 a 2025.

**Etapas.**

| # | Etapa | O que foi feito | Saída principal |
|---|---|---|---|
| 0 | Configuração | Regras do projeto (não inventar números, não alterar originais, sinalizar limitações) | `CLAUDE.md`, `DIARIO.md` |
| 1 | Dicionário | Leitura do PDF: campos, códigos, regra da idade, residência × notificação, campos de risco | `resultados/dicionario_resumo.md` |
| 2 | Perfil da base | 423.017 registros (Brasil) × 76 colunas. Notificações de 01/01/2016 a 30/06/2024 | `resultados/perfil_hiv.md` |
| 3 | Limpeza | Recorte por município de residência → 1.596 notificações; datas, idade, rótulos | `dados/hiv_baixo_amazonas.csv`, `resultados/decisoes_limpeza.md` |
| 4 | Séries | Casos por ano e município, variação, participação, efeito 2020–2021 | `resultados/series_relatorio.md` + 5 gráficos |
| 5 | Perfil e achados | Sexo, idade, raça/cor, escolaridade, exposição, gestantes, evolução; 5 achados | `resultados/achados_hiv.md` |
| 6 | Desenho do painel | 5 perguntas, 12 indicadores, filtros, o que não entra, wireframe | `resultados/wireframe.md` |
| 7 | Dashboard | JSON só com contagens agregadas + painel em arquivo único (4 abas) | `dados/dados_dashboard.json`, `dashboard/index.html` |
| 8 | Auditoria e notas | Totais recalculados por dois métodos independentes (0 divergências); Notas Metodológicas e LGPD | `resultados/auditoria.md` |

**Decisões que mudaram o resultado.**
- **Dois códigos IBGE da lista inicial estavam errados.** 1501956 é Cachoeira do Piriá e 1505502 é Paragominas. Foram corrigidos para Curuá (1502855) e Monte Alegre (1504802), conferindo na API do IBGE. Sem a correção, entrariam 260 notificações de fora da região.
- **Município de residência**, não de notificação. Em 2016–2024, 19,5% das notificações (312 de 1.596) foram feitas fora do município de residência, 281 delas em Santarém.
- **Ano de notificação** como referência. 2024 ficou marcado como parcial e 2025 como "sem dados".
- **Mudança no perfil medida entre períodos** (2016–2019 × 2020–2023), com teste de proporções, porque os números anuais são pequenos.
- **Sem taxas.** Como não há população na base, os municípios são comparados só em números absolutos e participação percentual.

**Principais resultados (2016–2023, 1.507 notificações, salvo indicação).**
- Notificações por ano: 145 (2016), 103 (2018, o menor), 290 (2022, o maior) e 248 (2023). 2024 tem 89, só de janeiro a junho.
- **Santarém** tem 67,9% das notificações de 2016–2024. Sete municípios têm menos de 30 notificações no período.
- **2020–2021:** o Brasil caiu 21,8% em 2020, mas a região subiu (+19,6% e +32,8%), puxada por Santarém. A causa não pode ser determinada com estes dados.
- **Sexo e idade:** homens são 72,2% (as mulheres caíram de 33,3% para 24,8%). 49,7% das pessoas têm 15 a 29 anos.
- **Exposição:** entre homens, a categoria homossexual passou de 32,6% para 47,9% e a bissexual caiu de 19,8% para 9,4%.
- **Gestantes:** 96 de 419 mulheres (22,9%) estavam gestantes; 72,9% delas foram notificadas no 2º ou 3º trimestre. Há 21 casos de transmissão vertical.
- **Qualidade:** escolaridade ignorada caiu de 10,6% para 2,6%. A evolução não é acompanhada (98,1% "vivo"; 18 óbitos registrados).

**Limitações.** Notificação não é incidência; há subnotificação; 2024 é parcial e 2025 não existe; os registros entram em lotes (sem leitura mensal); sem população não há taxas nem risco; municípios pequenos têm números instáveis; a evolução e os óbitos não medem mortalidade; gestantes e crianças têm fichas próprias fora da base. Os dados são sensíveis (LGPD): o painel é só agregado e para uso interno.

**Qualidade do trabalho.** A auditoria recalculou os totais por ano e município a partir da base tratada e, de novo, a partir do arquivo original, sem pandas. **Zero divergências** com o JSON e com o painel.

---

## 2. Roteiro de apresentação (5 minutos)

| Tempo | Bloco | O que mostrar | O que dizer (essencial) |
|---|---|---|---|
| 0:00–0:30 | **Problema** | Título do painel | "A vigilância precisa saber rápido quantos casos de HIV são notificados no Baixo Amazonas, onde e em quem, e o quanto pode confiar nesses números." |
| 0:30–1:15 | **Dados e cuidados** | Notas metodológicas (seções 1, 2 e 7) | "Usamos as notificações do SINAN: 1.596 pessoas residentes nos 13 municípios, de 2016 a junho de 2024. Duas correções importantes: dois códigos IBGE da lista estavam errados, e contamos pelo município onde a pessoa mora, não onde foi atendida." |
| 1:15–2:15 | **Visão Geral** | Barras por ano (2024 hachurado, 2025 "sem dados"); gráfico do 1º semestre | "As notificações passaram de 145 em 2016 para 290 em 2022. Em 2020, o Brasil caiu 21,8%, mas a região subiu, puxada por Santarém. Não sabemos a causa: pode ser mais testagem ou mudança de registro. 2024 só tem seis meses e não pode ser comparado com anos cheios." |
| 2:15–3:15 | **Perfil** | Pirâmide etária; exposição por período; cartões de gestantes | "Sete em cada dez notificações são de homens, e metade das pessoas tem de 15 a 29 anos. Entre homens, cresceu a categoria homossexual. 22,9% das mulheres estavam gestantes, a maioria já no 2º ou 3º trimestre. Isso levanta uma pergunta para o pré-natal: a testagem está acontecendo no início da gestação?" |
| 3:15–4:00 | **Municípios** | Mapa de calor; gráfico "onde foram notificados" | "Santarém concentra 67,9% das notificações, mas isso não é risco: não temos população para calcular taxas. O fluxo mostra que muitos moradores de Óbidos e Juruti são notificados em Santarém. Sete municípios têm menos de 30 casos, e o painel esconde percentuais instáveis ('n insuficiente')." |
| 4:00–4:40 | **Confiabilidade** | Tabela de completude; `resultados/auditoria.md` | "Os totais foram recalculados por dois métodos independentes, sem nenhuma divergência. Os campos têm poucos ignorados, mas a evolução não é atualizada, então o painel não mostra mortalidade." |
| 4:40–5:00 | **Fechamento** | Notas (LGPD) | "Próximos passos: incluir a população do IBGE para calcular taxas, cruzar com o SIM para óbitos e atualizar com 2025 quando chegar. O painel é agregado e de uso interno, como pede a LGPD." |

**Dicas para a apresentação.**
- Abrir `dashboard/index.html` antes de começar (precisa de internet para os gráficos; sem ela aparecem as tabelas).
- Repetir pelo menos uma vez: "notificação não é incidência".
- Se perguntarem "qual município tem mais risco?", responder que os dados não permitem dizer isso sem população.
