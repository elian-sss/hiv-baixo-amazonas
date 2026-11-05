# Diário do projeto

Registro de cada etapa: prompt recebido, o que foi feito, decisões e problemas.

---

## Etapa 0 — Configuração do projeto (05/11/2026)

**Prompt recebido (resumo):** definir o contexto do projeto (dashboard de HIV para a SESPA, Baixo Amazonas, 13 municípios, 2016–2025, análise conversacional), criar `CLAUDE.md` com o contexto e as regras, criar este `DIARIO.md` e propor as etapas até o dashboard.

**O que foi feito:**
- Listados os arquivos da pasta: `HIV16_25.csv` (~101 MB, 423.018 linhas contando o cabeçalho) e `HIVAN_DIC_DADOS(1).pdf`.
- Lido apenas o cabeçalho e as primeiras linhas do CSV para conhecer a estrutura (separador vírgula, primeira coluna é índice sem nome, datas `AAAAMMDD`, `********` para data vazia).
- Verificadas as bibliotecas Python disponíveis.
- Criados `CLAUDE.md` e `DIARIO.md`.

**Decisões:**
- Linguagem de análise: Python.
- Nenhuma análise numérica feita ainda; nenhum número sobre casos foi apresentado.

**Problemas / pendências:**
- `pandas` não está instalado (necessário para a análise). `plotly`/`streamlit` também não — a escolha da ferramenta do dashboard depende disso.
- O PDF do dicionário ainda não foi lido por completo.

---

## Etapa 1 — Leitura do dicionário de dados (05/11/2026)

**Prompt recebido (resumo):** ler o dicionário (PDF) e salvar em `resultados/dicionario_resumo.md` os campos relevantes para a vigilância (data, município de residência, sexo, idade, raça/cor, escolaridade, gestante, categoria de exposição, critério, evolução), com significado e categorias. Explicar a decodificação de `NU_IDADE_N`, a diferença entre município de notificação e de residência (e qual usar) e quais campos têm risco de baixa qualidade. Não analisar dados ainda.

**O que foi feito:**
- Criado `scripts/01_extrair_dicionario.py`, que extrai o texto das 11 páginas do PDF com `pypdf`. O original não foi alterado e o texto extraído ficou só no diretório temporário.
- Escrito `resultados/dicionario_resumo.md`, com os campos, as categorias, a regra da idade, a explicação sobre os dois municípios, uma nota sobre qual ano usar e a lista de riscos de qualidade.
- Nenhum dado do CSV foi analisado.

**Decisões:**
- Usar o **município de residência** (`ID_MN_RESI`) como padrão; o de notificação fica para a análise de fluxo de pacientes.
- Idade: 1º dígito 4 = anos; 1, 2 ou 3 = menos de 1 ano; outros valores = ignorado.
- `CRITERIO` = 900 (Descartado) será excluído das contagens.
- Proposta (a confirmar): série histórica pelo ano de diagnóstico.
- Agrupamentos propostos para categoria de exposição, escolaridade e faixa etária.

**Problemas / pendências:**
- O dicionário diz que o código de município tem 6 dígitos, mas o CSV mostra 7 em `ID_MUNICIP`/`ID_MN_RESI`. A conferir.
- `ANT_HEMOLF` usa 3 como "Ignorado" (os outros campos usam 9).
- A lista de `ANT_REL_CA` no PDF tem inconsistências (68 e 69 com a mesma descrição; 59 fora de ordem).
- O dicionário é de **HIV adulto**; casos em crianças e gestantes têm fichas próprias no SINAN.
- Os riscos de qualidade listados são hipóteses; serão medidos na exploração.

---

## Etapa 2 — Perfil geral da base (05/11/2026)

**Prompt recebido (resumo):** ler `HIV16_25.csv` inteiro como texto (`dtype=str`), ignorar a coluna de índice sem nome, informar linhas e colunas, distribuição de `NU_ANO`, `TP_NOT` e `ID_AGRAVO`, proporção de ausentes por coluna (incluindo `********`) e duplicados; apontar o que chama atenção, principalmente anos cobertos e anos incompletos. Código em `scripts/01_perfil.py` e resultado em `resultados/perfil_hiv.md`.

**O que foi feito:**
- Instalado o `pandas` (`pip install pandas`).
- Criado `scripts/01_perfil.py`, que leva cerca de 70 s para ler os 101 MB e gera `resultados/perfil_hiv.md`.
- Base inteira do Brasil, sem filtros: 423.017 registros × 76 colunas (sem o índice).
- Além do pedido, foram incluídos como apoio: notificações por mês em 2023 e 2024, a distribuição do ano de diagnóstico (`DT_DIAG`) e checagens dessa data.

**Decisões:**
- Ausente = célula vazia ou só asteriscos. O código "9 – Ignorado" **não** foi contado como ausente; será medido na etapa de qualidade.
- Duplicado = linha idêntica em todas as 76 colunas.
- `read_csv` com `keep_default_na=False`, para que nenhum valor vire NaN de forma implícita.

**Problemas / achados:**
- **Não há 2025 na base.** O período real é 2016–2024 e a última notificação é de 30/06/2024. **O ano de 2024 só tem o 1º semestre.** Isso diverge do período definido para o projeto (2016–2025).
- 2020 tem a menor contagem (39.946), o que é compatível com o efeito da pandemia.
- 11,4% dos registros têm diagnóstico anterior a 2016 (desde 2007), o que mostra notificação tardia.
- `TP_NOT` = 2 e `ID_AGRAVO` = B24 em 100% dos registros.
- `DT_OBITO` está ausente em 98,0%; `SEM_DIAG` está 100% vazio.
- Há 47 duplicados exatos.
- Nome dos scripts: já existia `01_extrair_dicionario.py`; o novo foi nomeado `01_perfil.py`, como pedido.

---

## Etapa 3 — Limpeza e recorte do Baixo Amazonas (05/11/2026)

**Prompt recebido (resumo):** filtrar os 13 municípios pelo município de residência (`ID_MN_RESI`, lista de 13 códigos fornecida) e criar `MUNICIPIO`; converter datas `AAAAMMDD` (`********` = ausente); decodificar a idade e criar faixas (<15, 15-19, 20-24, 25-29, 30-39, 40-49, 50-59, 60+); rotular sexo, raça/cor, escolaridade, gestante, evolução e categoria de exposição (agrupada); mostrar casos por município e ano, contagem mensal por ano e dizer se 2025 existe. Código em `scripts/02_limpeza.py`, base em `dados/hiv_baixo_amazonas.csv`, decisões em `resultados/decisoes_limpeza.md`.

**O que foi feito:**
- Os códigos foram conferidos na API de localidades do IBGE antes de filtrar.
- Criado `scripts/02_limpeza.py`, que gera a base tratada (1.596 registros × 89 colunas) e o relatório de decisões com as tabelas de conferência.

**Decisões:**
- **Dois códigos da lista recebida estavam errados e foram corrigidos:** 1501956 é Cachoeira do Piriá (Curuá = 1502855) e 1505502 é Paragominas (Monte Alegre = 1504802). Com a lista original, entrariam 56 + 204 = 260 registros de fora da região. Confirmação: todos os 13 municípios corrigidos têm regional de residência 1492; os dois errados têm 1487 e 1488.
- Removido 1 duplicado exato. Não havia nenhum `CRITERIO` = 900; todos os registros são 901 (HIV+).
- Datas convertidas; nenhuma data inválida, só ausentes.
- Idade: 9 registros sem idade (`****`), que ficam na faixa "Ignorada"; a idade vai de 14 a 80 anos.
- Escolaridade: a base usa `99` como Ignorado (o dicionário diz `9`).
- Categoria de exposição agrupada pela dezena do código. As combinações com drogas (4 registros: códigos 11, 21 e 31) ficaram no grupo sexual.
- O CSV foi salvo em UTF-8 com BOM, para abrir certo no Excel.

**Problemas / achados:**
- **2025 não existe; 2024 só vai até 28/06/2024** na região.
- A contagem mensal é muito irregular, com cara de digitação em lote (ex.: jun/2019 = 0 e out/2019 = 49; jun/2016 = 32 e out/2016 = 1). Isso desaconselha análise mensal; usar o ano.
- Santarém concentra 1.083 dos 1.596 casos (68%). Vários municípios têm menos de 30 casos em 8,5 anos, então as proporções municipais são instáveis.
- Não há casos de drogas injetáveis nem da categoria "Outras". "Ignorado" na exposição: 68.

---

## Etapa 4 — Séries temporais por município (05/11/2026)

**Prompt recebido (resumo):** calcular casos por ano, variação percentual anual e participação de cada município no total de cada ano; comparar os municípios em números absolutos, sem taxas (não há população); apontar municípios com poucos casos, o ano parcial (2024) e possíveis efeitos da pandemia em 2020–2021, sem afirmar causalidade. Tabelas e gráficos em `resultados/`, código em `scripts/03_series.py`.

**O que foi feito:**
- Instalado o `matplotlib`.
- Criado `scripts/03_series.py`, que gera:
  - 6 tabelas CSV: total por ano, município × ano, participação, variação por município, 1º semestre, índice 2019 = 100;
  - 5 gráficos PNG: total por ano, Santarém × demais, total por município, mapa de calor município × ano, índice 2019 = 100;
  - o relatório `resultados/series_relatorio.md`.
- Os gráficos foram conferidos visualmente; os rótulos do gráfico 2, que se sobrepunham ao eixo, foram removidos.

**Decisões:**
- Referência temporal: **ano de notificação**.
- 2024 sem variação anual. Para comparar, foi feita uma tabela só com o 1º semestre (jan–jun) de cada ano.
- "Poucos casos" = menos de 30 no período 2016–2024.
- Variação % por município só é mostrada quando o ano anterior tem 10 casos ou mais.
- Contexto nacional da pandemia: índice 2019 = 100, calculado a partir do `NU_ANO` do arquivo original.

**Achados:**
- Região: 145 (2016), 123, 103, 158, 189, 251, 290 (2022), 248 (2023) e 89 (2024, só jan–jun).
- Santarém tem 67,9% do período (de 60,2% em 2018 a 80,1% em 2021).
- 7 municípios com menos de 30 casos: Terra Santa 14, Faro 16, Curuá 18, Belterra 22, Almeirim 22, Prainha 24, Mojuí dos Campos 26.
- Pandemia: o Brasil caiu 21,8% em 2020; a região subiu (+19,6% em 2020 e +32,8% em 2021), puxada por Santarém (112 → 140 → 201). Os demais 12 municípios ficaram estáveis (46 → 49 → 50) e saltaram em 2022 (91). A causa não pode ser determinada com estes dados.
- 1º semestre: 147 em 2023 e 89 em 2024 (−39,5%). Não é possível dizer se é queda real ou atraso de digitação.

---

## Etapa 5 — Perfil dos casos e achados principais (05/11/2026)

**Prompt recebido (resumo):** descrever o perfil (sexo, faixa etária, raça/cor, escolaridade, categoria de exposição, gestantes, evolução) e como mudou entre 2016 e 2023, com o % de ignorados por campo; escrever 5 achados, cada um com número, período, limitação e pergunta de vigilância; nada que não tenha sido calculado. Saída em `resultados/achados_hiv.md`, código em `scripts/04_perfil.py`.

**O que foi feito:**
- Criado `scripts/04_perfil.py`. Ele gera `resultados/achados_hiv.md` e 7 CSVs `resultados/perfil_<campo>_ano.csv`, com a distribuição ano a ano de 2016 a 2024.
- Todos os números dos achados são inseridos pelo código a partir dos cálculos; nenhum foi digitado à mão.

**Decisões:**
- Recorte: 2016–2023 (n = 1.507). 2024 ficou fora das comparações por ser parcial.
- Mudança medida entre dois períodos de 4 anos (2016–2019 × 2020–2023), e não ano a ano, porque os números anuais são pequenos.
- Teste z de duas proporções (5%) para indicar quando a diferença pode ser acaso. Foi implementado com a biblioteca padrão, sem `scipy`.
- Escolaridade agrupada em 4 níveis. Gestantes calculadas só entre as mulheres.

**Achados (resumo):**
1. Homens são 72,2% dos casos; mulheres caíram de 33,3% para 24,8%.
2. Entre homens, a categoria homossexual subiu de 32,6% para 47,9% e a bissexual caiu de 19,8% para 9,4%.
3. 49,7% dos casos têm 15 a 29 anos; a mediana é 30 anos.
4. 96 de 419 mulheres (22,9%) estavam gestantes; 72,9% delas no 2º ou 3º trimestre. Há 21 casos de transmissão vertical.
5. Escolaridade ignorada caiu de 10,6% para 2,6%; houve só 18 óbitos registrados (98,1% constam como "vivo").

**Problemas / limitações:**
- Ignorados baixos (≤ 5,4% por campo) não significam dados corretos. A evolução quase nunca é atualizada.
- A mudança brusca na escolaridade ("até fundamental incompleto" de 32,3% para 8,8%) sugere mudança no preenchimento.
- O perfil por município não foi calculado, porque há poucos casos na maioria deles.

---

## Etapa 6 — Proposta do dashboard e wireframe (05/11/2026)

**Prompt recebido (resumo):** para a equipe de vigilância da SESPA, propor 5 perguntas prioritárias (com indicador e visualização), no máximo 12 indicadores com fórmula e fonte, filtros globais (ano, município, sexo, faixa etária), o que não deve entrar por limitação dos dados, e um wireframe em texto com as abas Visão Geral, Perfil dos casos, Comparação entre municípios e Notas Metodológicas. Saída em `resultados/wireframe.md`.

**O que foi feito:**
- Escrito `resultados/wireframe.md` com:
  - as 5 perguntas, cada uma com seu indicador e visualização;
  - 12 indicadores (I1–I12), com fórmula, colunas e regras de exibição;
  - os 4 filtros globais;
  - a lista do que não entra e por quê;
  - os wireframes das 4 abas;
  - os requisitos de acessibilidade.
- Nenhum cálculo novo. Os valores do wireframe são lugares reservados (`[n]`, `[x%]`); os poucos números citados no texto vêm das etapas anteriores.

**Decisões:**
- Período padrão dos filtros: 2016–2023. 2024 pode ser selecionado, com aviso.
- Regra de números pequenos: com menos de 10 notificações, mostrar só o número absoluto. Variação anual só quando o ano anterior tem 10 ou mais.
- Mapa de calor município × ano no lugar de um mapa geográfico colorido, para não sugerir risco com números absolutos.
- Selos de completude: Bom (< 5%), Atenção (5% a 10%), Crítico (> 10%). A evolução é marcada como crítica por não ser atualizada, mesmo com poucos ignorados.
- Novo indicador I11 (% notificados fora do município de residência), ainda não calculado.

**Pendências:**
- Calcular I11 (fluxo residência × notificação) antes de construir o painel.
- Definir a ferramenta do dashboard (proposta anterior: HTML interativo que abre no navegador).
- Se o painel for divulgado fora da SESPA, ocultar contagens de 1 a 4.

---

## Etapa 7 — Dados agregados e dashboard (05/11/2026)

**Prompt recebido (resumo):** gerar `dados/dados_dashboard.json` com tabelas agregadas (ano, município, sexo, faixa etária, categoria de exposição, evolução), sem dados individuais e com marcação de anos parciais, mostrando os totais para conferência. Depois, construir o dashboard do wireframe em `dashboard/index.html`: arquivo único com Chart.js por CDN, dados embutidos, filtros, KPIs, série 2016–2025 com anos parciais sinalizados, aviso de subnotificação, rodapé com a fonte e acessibilidade (contraste, celular). Nenhum número fixo fora do JSON.

**O que foi feito:**
- `scripts/05_dados_dashboard.py` gera o JSON (214 KB) com:
  - `meta`: fonte, data de corte, totais;
  - `parametros`: todos os limiares e períodos usados no painel;
  - `anos`: 2016–2025, cada ano com status completo, parcial ou sem dados;
  - `municipios` (com código IBGE) e `categorias`;
  - 7 cubos agregados (`base`, `exposicao`, `evolucao`, `raca`, `escolaridade`, `gestante`, `fluxo`);
  - um bloco `conferencia` com os totais.
- O script confere automaticamente que cada cubo soma o total (1.596; gestante soma as 444 mulheres) e para se aparecer categoria inesperada.
- `scripts/dashboard_template.html` (fonte do painel) + `scripts/06_build_dashboard.py`, que embute o JSON e gera `dashboard/index.html` (272 KB, arquivo único).
- Testado no navegador:
  - sem erros no console;
  - KPIs e tabelas batem com as etapas 4 e 5 (1.507 notificações em 2016–2023; 68,7% Santarém; 49,7% de 15 a 29 anos; 22,9% gestantes; exposição por período igual à de `achados_hiv.md`);
  - filtros funcionando (Masculino → 1.088; 2016–2025 → 1.596 com aviso de 2024 parcial e 2025 sem dados);
  - layout de celular (375 px) sem rolagem horizontal.

**Decisões:**
- Cubos ano × município × sexo × faixa (+ 1 dimensão): os filtros globais funcionam em todos os gráficos sem expor registros individuais. Células pequenas existem, por isso o painel é para uso interno (regra de ocultar contagens de 1 a 4 em divulgação externa).
- Mediana de idade retirada do painel (exigiria idade individual); fica a % de 15 a 29 anos.
- A série principal mostra sempre 2016–2025 (ignora o filtro de ano), com 2024 hachurado e 2025 "sem dados". A data de corte (30/06/2024) é calculada do arquivo original.
- O gráfico Santarém × demais e a participação de Santarém ignoram o filtro de município.
- Novo indicador calculado: local de notificação (fluxo). Ex.: residentes de Óbidos 60,9% e de Juruti 69,1% notificados em Santarém (2016–2023).
- Limiares e a faixa "pandemia" (2020–2021) ficam em `parametros` no JSON.
- Filtros fixos no topo só em telas grandes; no celular rolam com a página.
- Cada gráfico tem descrição para leitor de tela e "Ver como tabela". Tema claro e escuro.

**Problemas:**
- Atributo `hidden` anulado pelo CSS do aviso; corrigido com `[hidden]{display:none!important}`.
- Sem internet o Chart.js não carrega: o painel mostra o aviso e abre as tabelas no lugar dos gráficos.

---

## Etapa 8 — Auditoria, notas metodológicas e relatório (05/11/2026)

**Prompt recebido (resumo):**
1. Recalcular, por método independente, os totais por ano e município a partir de `dados/hiv_baixo_amazonas.csv` e comparar com o JSON do dashboard, listando divergências e correções (`scripts/05_auditoria.py`, `resultados/auditoria.md`).
2. Escrever as "Notas Metodológicas e Limitações" em linguagem simples (subnotificação, anos parciais, ignorados, notificação × incidência, ausência de taxas, município de residência e LGPD, com fontes e data de acesso) e incluí-las na aba do dashboard.
3. Gerar `RELATORIO.md` com resumo de uma página e roteiro de apresentação de 5 minutos.

**O que foi feito:**
- `scripts/05_auditoria.py` (só biblioteca padrão, sem pandas) recalcula os totais de duas formas:
  - **A:** a partir da base tratada, com o ano tirado do texto de `DT_NOTIFIC` e o município do código IBGE, numa tabela própria;
  - **B:** a partir do original `HIV16_25.csv`, refazendo o recorte do zero.
  Compara com o bloco `conferencia`, com `anos[].n`, com a soma de cada cubo por município × ano e com o JSON embutido no HTML.
- Resultado: **0 divergências** (total 1.596 em A, B e JSON; 13 municípios, 10 anos e todas as combinações município × ano idênticos; JSON do HTML idêntico ao arquivo). Nenhuma correção foi necessária. A auditoria foi rodada de novo depois da mudança no painel, com o mesmo resultado.
- Aba "Notas metodológicas e limitações" reescrita, com 11 seções em linguagem simples. Todos os números são calculados a partir do JSON (ex.: 19,5% notificados fora do município de residência; ignorados por campo).
- Fontes com data de acesso adicionadas em `meta.fontes` no JSON: SINAN, dicionário, base, API IBGE, LGPD e Departamento de HIV/Aids do MS. As URLs foram abertas em 05/11/2026. Os artigos 5º (II), 11 e 13 da LGPD foram conferidos no texto do Planalto.
- `RELATORIO.md`: resumo de uma página (etapas, decisões, resultados, limitações, auditoria) e roteiro de 5 minutos em 7 blocos.

**Decisões:**
- "Independente" = outra biblioteca (`csv`), outra origem do ano e do município, e um segundo caminho a partir do arquivo original.
- A Portaria nº 1.271/2014 não foi citada: a página aberta não permitiu confirmar o trecho sobre HIV, e só foram citadas fontes conferidas.
- O nome `05_auditoria.py` foi mantido como pedido, embora já exista `05_dados_dashboard.py`.

**Problemas:**
- O site do Planalto não respondeu ao `curl` (tempo esgotado); a LGPD foi conferida pelo navegador.
- Os percentuais de ignorados nas Notas usam 2016–2024 (ex.: escolaridade 5,3%), enquanto `achados_hiv.md` usa 2016–2023 (5,4%). A diferença está explicada no texto ("no período todo").

---

## Etapa 9 — Prompts, PDF dos achados e publicação no GitHub (05/11/2026)

**Prompt recebido:** "coloca todos os prompts em um arquivo txt, sobe no github e manda o link pra acessar o dashboard no github pages e me dá um resumo da interpretação dos principais achados em um pdf".

**O que foi feito:**
- `prompts.txt` com os 10 prompts do projeto, na ordem e com o texto original.
- `scripts/07_pdf_achados.py` gera `resultados/resumo_achados_hiv.pdf` (3 páginas, A4), com reportlab instalado. O PDF traz:
  - 5 achados interpretados, cada um com o número, o que significa, o cuidado e uma pergunta para a vigilância;
  - o que os dados não permitem dizer;
  - os próximos passos.
  Todos os números são calculados do JSON auditado e de `series_indice_2019.csv`.
- **Versão pública do painel**, por decisão do usuário: ocultar contagens de 1 a 4 antes de publicar.
  - `05_dados_dashboard.py` gera também `dados/dados_dashboard_publico.json`, com menos detalhe: territorial = ano × município; perfil = região inteira (ano × sexo × faixa × característica).
  - `06_build_dashboard.py` gera `dashboard/index.html` (público) e `dashboard/index_interno.html` (interno, completo).
  - No painel público, toda contagem de 1 a 4 aparece como "<5", percentuais sobre esses grupos ficam ocultos, as barras desses grupos não são desenhadas e as células do mapa de calor ficam neutras.
  - Os filtros sem efeito numa aba ficam desativados, com aviso (sexo/idade nas abas territoriais; município no Perfil).
  - Notas e rodapé explicam a versão pública.
- Auditoria ampliada: confere também o JSON público e os dois HTML. **0 divergências.**
- Repositório: `.gitignore` excluindo os dados individuais e a versão interna, `README.md`, e `index.html` na raiz redirecionando para `dashboard/`.

**Decisões:**
- Ocultar só na tela não basta, porque o JSON fica no código-fonte da página. Por isso a versão pública usa dados menos detalhados e a supressão é feita na exibição.
- Limitação registrada nas Notas: combinar filtros pode permitir deduzir alguns valores pequenos por subtração. Por isso a versão completa fica restrita à SESPA.
- Os relatórios em `resultados/` foram publicados. Eles têm tabelas agregadas por município × ano e perfil da região, algumas com contagens pequenas.
- Repositório público `elian-sss/hiv-baixo-amazonas` (exigência do GitHub Pages gratuito).
- Commit sem linha de coautoria, conforme as instruções do usuário.

**Problemas:**
- O fluxo de notificação no PDF usa 2016–2024 (ex.: Óbidos 53,5%), enquanto o painel padrão (2016–2023) mostra 60,9%. O período está indicado no texto.
