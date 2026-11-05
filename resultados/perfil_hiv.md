# Perfil da base HIV16_25.csv (Brasil, sem filtros)

Gerado por `scripts/01_perfil.py`. Todos os números abaixo foram calculados sobre o arquivo original, lido inteiramente como texto. **Nenhum filtro de município ou critério foi aplicado ainda.**

## 1. Dimensões

- Arquivo bruto: 423.017 linhas de dados × 77 colunas.
- Coluna de índice sem nome descartada: 1.
- Base de trabalho: **423.017 registros × 76 colunas**.

## 2. Ano de notificação (`NU_ANO`)

| NU_ANO | Registros | % |
|---|---:|---:|
| 2016 | 47.909 | 11,3% |
| 2017 | 55.937 | 13,2% |
| 2018 | 52.035 | 12,3% |
| 2019 | 51.053 | 12,1% |
| 2020 | 39.946 | 9,4% |
| 2021 | 47.017 | 11,1% |
| 2022 | 49.802 | 11,8% |
| 2023 | 53.582 | 12,7% |
| 2024 | 25.736 | 6,1% |
| **Total** | **423.017** | 100,0% |

- Ano de `DT_NOTIFIC` coincide com `NU_ANO` em 100,0% dos registros.
- Data de notificação mínima: 01/01/2016; máxima: 30/06/2024.

### Notificações por mês em 2023 e 2024

| Mês | 2023 | 2024 |
|---|---:|---:|
| 01 | 4.701 | 4.724 |
| 02 | 4.096 | 4.160 |
| 03 | 4.974 | 3.989 |
| 04 | 4.076 | 4.601 |
| 05 | 4.836 | 4.210 |
| 06 | 4.337 | 4.052 |
| 07 | 4.612 | 0 |
| 08 | 5.152 | 0 |
| 09 | 4.244 | 0 |
| 10 | 4.376 | 0 |
| 11 | 4.213 | 0 |
| 12 | 3.965 | 0 |

## 3. Tipo de notificação (`TP_NOT`)

Dicionário: 1 Negativa · 2 Individual · 3 Surto · 4 Agregado.

| TP_NOT | Registros | % |
|---|---:|---:|
| 2 | 423.017 | 100,0% |
| **Total** | **423.017** | 100,0% |

## 4. Agravo (`ID_AGRAVO`)

| ID_AGRAVO | Registros | % |
|---|---:|---:|
| B24 | 423.017 | 100,0% |
| **Total** | **423.017** | 100,0% |

## 5. Ano de diagnóstico (`DT_DIAG`) — apoio

Registros sem data de diagnóstico válida: 0 (0,0%).

- Diagnóstico antes de 2016: 48.202 registros (11,4%); ano mais antigo: 2007.

| Ano diag. | Registros |
|---|---:|
| 2010 | 3.788 |
| 2011 | 5.021 |
| 2012 | 5.353 |
| 2013 | 6.643 |
| 2014 | 7.311 |
| 2015 | 11.828 |
| 2016 | 42.974 |
| 2017 | 46.523 |
| 2018 | 47.130 |
| 2019 | 47.025 |
| 2020 | 37.345 |
| 2021 | 43.140 |
| 2022 | 44.368 |
| 2023 | 46.383 |
| 2024 | 19.927 |

- `DT_DIAG` exatamente 01/01/2007 (a data mais antiga da base): 105 registros (0,0%).
- `DT_DIAG` em 1º de janeiro de qualquer ano: 2.612 (0,6%); se as datas fossem distribuídas ao acaso, seria cerca de 0,3% (1/365).
- `DT_DIAG` posterior a `DT_NOTIFIC`: 0 registros.

## 6. Ausentes por coluna

Ausente = célula vazia ou formada só por asteriscos (ex.: `********`, usado pelo SINAN para data vazia). Ordenado do maior para o menor.

| Coluna | Vazio | `****` | Total ausente | % |
|---|---:|---:|---:|---:|
| SEM_DIAG | 423.017 | 0 | 423.017 | 100,0% |
| ANTUFTRANS | 422.041 | 0 | 422.041 | 99,8% |
| ANT_INVEST | 421.561 | 0 | 421.561 | 99,7% |
| ANTDTTRANS | 0 | 421.535 | 421.535 | 99,6% |
| ANTMUNTRAN | 421.522 | 9 | 421.531 | 99,6% |
| DT_OBITO | 0 | 414.368 | 414.368 | 98,0% |
| DT_RAPIDO | 0 | 249.621 | 249.621 | 59,0% |
| TRA_UF | 224.199 | 0 | 224.199 | 53,0% |
| TPRAPIDO3 | 208.730 | 0 | 208.730 | 49,3% |
| ID_OCUPA_N | 197.034 | 0 | 197.034 | 46,6% |
| DT_CONFIRM | 0 | 141.884 | 141.884 | 33,5% |
| DTTRIAGEM | 0 | 135.060 | 135.060 | 31,9% |
| TPRAPIDO2 | 125.319 | 0 | 125.319 | 29,6% |
| TPRAPIDO1 | 114.461 | 0 | 114.461 | 27,1% |
| TRA_MUNICI | 94.780 | 0 | 94.780 | 22,4% |
| ID_RG_RESI | 62.773 | 0 | 62.773 | 14,8% |
| ID_REGIONA | 62.555 | 0 | 62.555 | 14,8% |
| LAB_CONFIR | 3.428 | 0 | 3.428 | 0,8% |
| ID_PAIS | 3.428 | 0 | 3.428 | 0,8% |
| CS_RACA | 3.112 | 0 | 3.112 | 0,7% |
| NU_IDADE_N | 0 | 2.840 | 2.840 | 0,7% |
| DEF_DIAGNO | 2.364 | 0 | 2.364 | 0,6% |
| EVOLUCAO | 935 | 0 | 935 | 0,2% |
| SG_UF | 216 | 0 | 216 | 0,1% |
| ANTTRANS_M | 36 | 0 | 36 | 0,0% |
| CS_GESTANT | 13 | 0 | 13 | 0,0% |
| DT_NOTIFIC | 0 | 0 | 0 | 0,0% |
| NU_ANO | 0 | 0 | 0 | 0,0% |
| CS_SEXO | 0 | 0 | 0 | 0,0% |
| SG_UF_NOT | 0 | 0 | 0 | 0,0% |
| ID_MUNICIP | 0 | 0 | 0 | 0,0% |
| DT_DIAG | 0 | 0 | 0 | 0,0% |
| TP_NOT | 0 | 0 | 0 | 0,0% |
| ID_AGRAVO | 0 | 0 | 0 | 0,0% |
| ANT_DROGA | 0 | 0 | 0 | 0,0% |
| ANT_ACIDEN | 0 | 0 | 0 | 0,0% |
| LAB_TRIAGE | 0 | 0 | 0 | 0,0% |
| ANT_SARCOM | 0 | 0 | 0 | 0,0% |
| ANT_TUBERC | 0 | 0 | 0 | 0,0% |
| ANTRELSE_N | 0 | 0 | 0 | 0,0% |
| ID_MN_RESI | 0 | 0 | 0 | 0,0% |
| CS_ESCOL_N | 0 | 0 | 0 | 0,0% |
| ANT_TRASMI | 0 | 0 | 0 | 0,0% |
| ANT_HEMOLF | 0 | 0 | 0 | 0,0% |
| ANT_DIARRE | 0 | 0 | 0 | 0,0% |
| ANT_DISFUN | 0 | 0 | 0 | 0,0% |
| ANT_HERPES | 0 | 0 | 0 | 0,0% |
| ANT_PULMON | 0 | 0 | 0 | 0,0% |
| ANT_CANDID | 0 | 0 | 0 | 0,0% |
| ANT_FEBRE | 0 | 0 | 0 | 0,0% |
| ANT_ASTERI | 0 | 0 | 0 | 0,0% |
| ANT_CAQUEX | 0 | 0 | 0 | 0,0% |
| ANT_ESOF_N | 0 | 0 | 0 | 0,0% |
| ANT_PULM_N | 0 | 0 | 0 | 0,0% |
| ANT_CITO | 0 | 0 | 0 | 0,0% |
| ANT_DERMAT | 0 | 0 | 0 | 0,0% |
| ANT_ANEMIA | 0 | 0 | 0 | 0,0% |
| ANT_TOSSE | 0 | 0 | 0 | 0,0% |
| ANT_LINFO | 0 | 0 | 0 | 0,0% |
| ANT_CANCER | 0 | 0 | 0 | 0,0% |
| ANT_ISOPOR | 0 | 0 | 0 | 0,0% |
| ANT_HISTO | 0 | 0 | 0 | 0,0% |
| ANT_H_SIMP | 0 | 0 | 0 | 0,0% |
| ANT_CRIP_1 | 0 | 0 | 0 | 0,0% |
| ANT_CRIPTO | 0 | 0 | 0 | 0,0% |
| ANT_LEUCO | 0 | 0 | 0 | 0,0% |
| ANT_LINFO_ | 0 | 0 | 0 | 0,0% |
| ANT_LINFOM | 0 | 0 | 0 | 0,0% |
| ANT_TOXO | 0 | 0 | 0 | 0,0% |
| ANT_SALMO | 0 | 0 | 0 | 0,0% |
| ANT_CHAGAS | 0 | 0 | 0 | 0,0% |
| ANT_PNEUMO | 0 | 0 | 0 | 0,0% |
| ANT_MICRO | 0 | 0 | 0 | 0,0% |
| ANT_CONTAG | 0 | 0 | 0 | 0,0% |
| CRITERIO | 0 | 0 | 0 | 0,0% |
| ANT_REL_CA | 0 | 0 | 0 | 0,0% |

Observação: o código `9` (Ignorado) **não** foi contado como ausente aqui; será medido campo a campo na etapa de qualidade.

## 7. Duplicados

- Linhas idênticas em todas as 76 colunas (excluindo a primeira ocorrência): **47** (0,0%).
- Grupos distintos de linhas repetidas: 45.
- A base não tem identificador do paciente; por isso não é possível detectar a mesma pessoa notificada duas vezes com dados ligeiramente diferentes.

## 8. O que chama atenção

1. **Período coberto: 2016 a 2024, não 2016–2025.** Anos ausentes: 2025. A última notificação é de 30/06/2024.
2. **2024 está incompleto:** só há notificações de janeiro a 06; 25.736 registros, contra média de 49.660 por ano em 2016–2023. Não pode ser comparado com os anos fechados como ano cheio.
3. **2020 tem a menor contagem (39.946)**, coerente com a redução de testagem e atendimento na pandemia de covid-19; é queda de notificação, não necessariamente de infecções.
4. `TP_NOT` e `ID_AGRAVO` têm um único valor (individual, B24): a base já vem filtrada para notificações individuais de HIV adulto.
5. **11,4% dos registros têm diagnóstico anterior a 2016** (desde 2007): são notificações tardias de casos antigos. Contar por ano de notificação ou de diagnóstico muda os números.
6. Campos centrais (município, sexo, datas, critério, categoria de exposição, escolaridade) não têm vazios, mas isso não significa boa qualidade: o "Ignorado" (código 9/90) ainda precisa ser medido.
7. `EVOLUCAO` quase completa, mas `DT_OBITO` ausente em 98,0%: reforça que óbitos tendem a estar sub-registrados nesta ficha.
8. Duplicados exatos são raros (47); serão removidos na base tratada.
