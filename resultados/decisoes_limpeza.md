# Decisões de limpeza: base de HIV do Baixo Amazonas

Gerado por `scripts/02_limpeza.py`. Base tratada: `dados/hiv_baixo_amazonas.csv` (UTF-8, separador vírgula, datas no formato AAAA-MM-DD). O arquivo original não foi alterado.

## Resumo do fluxo

| Passo | Registros |
|---|---:|
| Base Brasil (sem índice) | 423.017 |
| Residentes nos 13 municípios | 1.597 |
| − duplicados exatos | 1 |
| − critério 900 (descartado) | 0 |
| **Base final** | **1.596** |

## Decisão 1 — Recorte pelo município de residência

- Filtro em `ID_MN_RESI` (onde a pessoa mora), padrão do Ministério da Saúde e coerente com taxas por habitante. O município de notificação (`ID_MUNICIP`) foi mantido na base para análises de fluxo.
- **Correção de dois códigos da lista recebida.** Conferidos na API de localidades do IBGE:
  - `1501956` é **Cachoeira do Piriá** (Nordeste Paraense). O código de **Curuá** é `1502855`.
  - `1505502` é **Paragominas** (Sudeste Paraense). O código de **Monte Alegre** é `1504802`.
  - Com a lista original, entrariam por engano: 1501956 (Cachoeira do Piriá): 56 registros; 1505502 (Paragominas): 204 registros.
- Confirmação interna: todos os registros filtrados têm regional de residência (`ID_RG_RESI`) = 1492, a mesma para os 13 municípios.
- Coluna `MUNICIPIO` criada com os nomes (com acento).

## Decisão 2 — Duplicados e casos descartados

- Removidos 1 registros idênticos em todas as colunas (mantida a 1ª ocorrência).
- Removidos 0 registros com `CRITERIO` = 900 (descartado).
- Critérios na base final: {'901': 1596} (901 = HIV+).
- Sem identificador do paciente não é possível achar a mesma pessoa notificada duas vezes com dados diferentes.

## Decisão 3 — Datas

Formato `AAAAMMDD` convertido para data; `********` ou vazio = ausente; valor que não forma data válida = ausente (contado abaixo).

| Campo | Ausentes | Inválidas | % ausente+inválida |
|---|---:|---:|---:|
| DT_NOTIFIC | 0 | 0 | 0,0% |
| DT_DIAG | 0 | 0 | 0,0% |
| DTTRIAGEM | 253 | 0 | 15,9% |
| DT_CONFIRM | 157 | 0 | 9,8% |
| DT_RAPIDO | 945 | 0 | 59,2% |
| DT_OBITO | 1.576 | 0 | 98,7% |
| ANTDTTRANS | 1.592 | 0 | 99,7% |

- Criadas `ANO_NOTIF`, `MES_NOTIF` (de `DT_NOTIFIC`) e `ANO_DIAG` (de `DT_DIAG`). `ANO_NOTIF` igual a `NU_ANO` em todos os registros: sim.

## Decisão 4 — Idade

- `NU_IDADE_N`: 1º dígito = unidade (1 hora, 2 dia, 3 mês, 4 ano); 3 últimos = valor. Unidade 4 → anos; unidades 1–3 → 0 anos; outro valor (ex.: `****`) ou > 120 anos → ignorada.
- 1º dígito encontrado: {'4': 1587, '*': 9}.
- Idade mínima e máxima: 14 e 80 anos.
- Faixas (`FAIXA_ETARIA`): <15, 15-19, 20-24, 25-29, 30-39, 40-49, 50-59, 60+ e Ignorada.

| Faixa | Registros |
|---|---:|
| <15 | 3 |
| 15-19 | 129 |
| 20-24 | 364 |
| 25-29 | 311 |
| 30-39 | 417 |
| 40-49 | 234 |
| 50-59 | 89 |
| 60+ | 40 |
| Ignorada | 9 |

## Decisão 5 — Rótulos

Códigos convertidos conforme o dicionário (`resultados/dicionario_resumo.md`). Vazio ou código fora do dicionário → "Ignorado". Colunas originais mantidas.

| Nova coluna | Origem | Códigos encontrados (contagem) |
|---|---|---|
| SEXO | CS_SEXO | `F`: 444, `M`: 1152 |
| RACA_COR | CS_RACA | `vazio`: 3, `1`: 24, `2`: 32, `3`: 5, `4`: 1519, `5`: 9, `9`: 4 |
| ESCOLARIDADE | CS_ESCOL_N | `00`: 21, `01`: 30, `02`: 18, `03`: 198, `04`: 323, `05`: 122, `06`: 542, `07`: 42, `08`: 216, `99`: 84 |
| GESTANTE | CS_GESTANT | `1`: 20, `2`: 49, `3`: 29, `4`: 6, `5`: 294, `6`: 1194, `9`: 4 |
| EVOLUCAO_DESC | EVOLUCAO | `1`: 1566, `2`: 11, `3`: 9, `9`: 10 |
| CAT_EXPOSICAO / CAT_EXPOSICAO_GRUPO | ANT_REL_CA | `10`: 508, `11`: 1, `20`: 143, `21`: 1, `30`: 852, `31`: 2, `80`: 21, `90`: 68 |

- **Escolaridade:** a base usa `99` para Ignorado (o dicionário diz `9`); os dois foram tratados como Ignorado. Os códigos vêm com zero à esquerda (`06`) e foram lidos como número.
- **Gestante:** gestantes (códigos 1–4) do sexo feminino: 104; marcadas como gestantes e do sexo masculino: 0.
- **Categoria de exposição agrupada** (`CAT_EXPOSICAO_GRUPO`), pela dezena do código, que é a categoria principal na hierarquia do SINAN:
  - Homossexual = 10–15 · Bissexual = 20–25 · Heterossexual = 30–36 · Drogas injetáveis = 40–42 · Vertical = 80 · Ignorado = 90 · Outras = 50 (hemofilia), 59–69 (transfusão), 70 (acidente biológico).
  - Combinações como 11 (Homo/Drogas), 21 (Bi/Drogas) e 31 (Hetero/Droga) ficam no grupo sexual. Alternativa possível: contá-las em "Drogas injetáveis". Afeta poucos registros (ver códigos acima).
  - A categoria detalhada fica em `CAT_EXPOSICAO`.

| Grupo | Registros |
|---|---:|
| Heterossexual | 854 |
| Homossexual | 509 |
| Bissexual | 144 |
| Ignorado | 68 |
| Vertical | 21 |

## Conferência — casos por município e ano de NOTIFICAÇÃO

| Município | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Alenquer | 8 | 7 | 5 | 8 | 3 | 0 | 12 | 7 | 5 | 55 |
| Almeirim | 0 | 0 | 1 | 1 | 3 | 4 | 4 | 6 | 3 | 22 |
| Belterra | 1 | 2 | 1 | 2 | 2 | 4 | 6 | 4 | 0 | 22 |
| Curuá | 1 | 2 | 2 | 2 | 2 | 1 | 3 | 4 | 1 | 18 |
| Faro | 0 | 0 | 0 | 2 | 1 | 5 | 3 | 3 | 2 | 16 |
| Juruti | 5 | 3 | 2 | 6 | 2 | 6 | 12 | 19 | 8 | 63 |
| Mojuí dos Campos | 5 | 4 | 1 | 2 | 5 | 3 | 1 | 3 | 2 | 26 |
| Monte Alegre | 5 | 4 | 4 | 7 | 9 | 2 | 9 | 7 | 5 | 52 |
| Óbidos | 10 | 15 | 10 | 7 | 10 | 11 | 16 | 8 | 12 | 99 |
| Oriximiná | 16 | 16 | 11 | 6 | 11 | 10 | 16 | 13 | 3 | 102 |
| Prainha | 3 | 1 | 2 | 2 | 1 | 3 | 5 | 7 | 0 | 24 |
| Santarém | 90 | 69 | 62 | 112 | 140 | 201 | 199 | 162 | 48 | 1.083 |
| Terra Santa | 1 | 0 | 2 | 1 | 0 | 1 | 4 | 5 | 0 | 14 |
| **Total** | **145** | **123** | **103** | **158** | **189** | **251** | **290** | **248** | **89** | **1.596** |

## Conferência — casos por município e ano de DIAGNÓSTICO

Inclui casos diagnosticados antes de 2016 e notificados a partir de 2016.

| Município | 2007 | 2008 | 2009 | 2010 | 2011 | 2012 | 2013 | 2014 | 2015 | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Alenquer | 0 | 1 | 0 | 1 | 0 | 2 | 0 | 0 | 1 | 7 | 4 | 6 | 9 | 3 | 0 | 12 | 4 | 5 | 55 |
| Almeirim | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 2 | 4 | 4 | 6 | 3 | 22 |
| Belterra | 0 | 0 | 0 | 2 | 1 | 0 | 0 | 1 | 1 | 0 | 1 | 1 | 1 | 1 | 4 | 5 | 4 | 0 | 22 |
| Curuá | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 1 | 2 | 2 | 2 | 1 | 3 | 4 | 1 | 18 |
| Faro | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 2 | 1 | 5 | 2 | 3 | 2 | 16 |
| Juruti | 1 | 1 | 0 | 1 | 0 | 1 | 2 | 0 | 2 | 3 | 3 | 2 | 7 | 0 | 5 | 12 | 15 | 8 | 63 |
| Mojuí dos Campos | 0 | 1 | 0 | 0 | 1 | 0 | 0 | 0 | 3 | 1 | 4 | 1 | 2 | 4 | 3 | 1 | 4 | 1 | 26 |
| Monte Alegre | 1 | 1 | 0 | 0 | 0 | 2 | 0 | 0 | 0 | 4 | 5 | 5 | 6 | 8 | 2 | 8 | 8 | 2 | 52 |
| Óbidos | 0 | 0 | 1 | 1 | 2 | 0 | 0 | 0 | 1 | 6 | 16 | 11 | 8 | 9 | 10 | 16 | 7 | 11 | 99 |
| Oriximiná | 1 | 1 | 0 | 2 | 1 | 1 | 0 | 0 | 2 | 14 | 15 | 7 | 7 | 12 | 8 | 16 | 13 | 2 | 102 |
| Prainha | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 3 | 1 | 2 | 3 | 1 | 2 | 5 | 7 | 0 | 24 |
| Santarém | 5 | 6 | 8 | 8 | 8 | 9 | 12 | 8 | 29 | 67 | 65 | 67 | 108 | 128 | 185 | 185 | 144 | 41 | 1.083 |
| Terra Santa | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 3 | 1 | 0 | 2 | 4 | 3 | 0 | 14 |
| **Total** | **9** | **11** | **9** | **15** | **14** | **15** | **14** | **9** | **40** | **107** | **115** | **108** | **157** | **171** | **231** | **273** | **222** | **76** | **1.596** |

## Conferência — notificações por mês e ano (13 municípios)

| Mês | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 01 | 5 | 9 | 13 | 7 | 11 | 15 | 22 | 25 | 15 | 122 |
| 02 | 30 | 8 | 9 | 10 | 22 | 20 | 11 | 25 | 18 | 153 |
| 03 | 11 | 17 | 14 | 20 | 23 | 19 | 34 | 23 | 14 | 175 |
| 04 | 17 | 8 | 7 | 6 | 7 | 17 | 22 | 15 | 14 | 113 |
| 05 | 23 | 16 | 5 | 4 | 20 | 17 | 22 | 33 | 15 | 155 |
| 06 | 32 | 8 | 7 | 0 | 3 | 24 | 32 | 26 | 13 | 145 |
| 07 | 3 | 8 | 10 | 7 | 3 | 21 | 25 | 20 | 0 | 97 |
| 08 | 3 | 8 | 12 | 8 | 26 | 18 | 30 | 20 | 0 | 125 |
| 09 | 8 | 5 | 5 | 22 | 14 | 36 | 29 | 20 | 0 | 139 |
| 10 | 1 | 11 | 6 | 49 | 27 | 23 | 20 | 12 | 0 | 149 |
| 11 | 6 | 9 | 10 | 7 | 14 | 20 | 18 | 17 | 0 | 101 |
| 12 | 6 | 16 | 5 | 18 | 19 | 21 | 25 | 12 | 0 | 122 |
| **Total** | **145** | **123** | **103** | **158** | **189** | **251** | **290** | **248** | **89** | **1.596** |

## Cobertura temporal

- Anos de notificação presentes: 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.
- **2025 existe na base? Não.**
- Última data de notificação na região: 28/06/2024.
- Meses com ao menos uma notificação, por ano: 2016: 12, 2017: 12, 2018: 12, 2019: 11, 2020: 12, 2021: 12, 2022: 12, 2023: 12, 2024: 6.
- Mês com zero notificações num município pequeno pode ser real; o que indica ano incompleto é o corte geral dos dados (na base Brasil, a última notificação é de 30/06/2024).
