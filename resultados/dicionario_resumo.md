# Dicionário de dados: resumo para a vigilância

**Fonte:** `HIVAN_DIC_DADOS(1).pdf`, Ministério da Saúde / GT-SINAN, *Dicionário de Dados – Agravo: HIV Adulto*, revisado em fevereiro de 2024 (11 páginas).
**Como foi lido:** o texto do PDF foi extraído com `scripts/01_extrair_dicionario.py`, sem alterar o arquivo original.
**Atenção:** este documento descreve apenas o que o dicionário diz. Nenhum dado da base foi analisado ainda. Os riscos de qualidade listados abaixo são **hipóteses** a conferir na exploração.

---

## 1. Campos relevantes para a vigilância

### Identificação e datas

| Campo | Significado | Categorias / formato |
|---|---|---|
| `TP_NOT` | Tipo de notificação | 1 Negativa · 2 Individual · 3 Surto · 4 Agregado |
| `ID_AGRAVO` | Agravo notificado (CID-10) | Código CID-10 (ex.: B24) |
| `DT_NOTIFIC` | Data em que a ficha de notificação foi preenchida | Data (`AAAAMMDD` no CSV) |
| `NU_ANO` | Ano da notificação (campo interno) | Ano com 4 dígitos |
| `DT_DIAG` | Para agravos crônicos como o HIV, **data do diagnóstico** | Data (`AAAAMMDD` no CSV) |
| `SEM_DIAG` | Semana epidemiológica do diagnóstico (campo interno) | Semana do calendário epidemiológico |

### Local

| Campo | Significado | Categorias / formato |
|---|---|---|
| `SG_UF_NOT` | UF onde fica a unidade que notificou | Código/sigla IBGE |
| `ID_MUNICIP` | **Município de notificação**: onde fica a unidade de saúde que notificou | Código IBGE |
| `ID_REGIONA` | Regional de saúde do município de notificação (campo interno) | Código da regional |
| `SG_UF` | UF de residência do paciente na data da notificação | Código/sigla IBGE |
| `ID_MN_RESI` | **Município de residência** do paciente | Código IBGE |
| `ID_RG_RESI` | Regional de saúde do município de residência (campo interno) | Código da regional |
| `ID_PAIS` | País de residência (se o paciente mora fora do Brasil) | Tabela de países |
| `TRA_UF` / `TRA_MUNICI` | UF e município onde o paciente faz tratamento | Código IBGE |

### Pessoa

| Campo | Significado | Categorias |
|---|---|---|
| `NU_IDADE_N` | Idade codificada (ver seção 2) | 4 dígitos: unidade + valor |
| `CS_SEXO` | Sexo | M Masculino · F Feminino · I Ignorado |
| `CS_GESTANT` | Gestante e idade gestacional | 1 1º trimestre · 2 2º trimestre · 3 3º trimestre · 4 Idade gestacional ignorada · 5 Não · 6 Não se aplica · 9 Ignorado |
| `CS_RACA` | Raça/cor **autodeclarada** | 1 Branca · 2 Preta · 3 Amarela · 4 Parda · 5 Indígena · 9 Ignorado |
| `CS_ESCOL_N` | Escolaridade (última série concluída) | 0 Analfabeto · 1 1ª a 4ª série incompleta do EF · 2 4ª série completa do EF · 3 5ª a 8ª série incompleta do EF · 4 EF completo · 5 Médio incompleto · 6 Médio completo · 7 Superior incompleto · 8 Superior completo · 9 Ignorado · 10 Não se aplica |

**Para agrupar no dashboard (proposta):** gestante = códigos 1 a 4. Escolaridade em quatro faixas: até EF incompleto (0–3), EF completo ou médio incompleto (4–5), médio completo ou superior incompleto (6–7) e superior completo (8), com Ignorado (9) e Não se aplica (10) à parte.

### Forma de transmissão

**Categoria de exposição (`ANT_REL_CA`)** é um campo interno: o **próprio sistema calcula** a categoria com base nos campos de transmissão e numa hierarquia. É o campo mais prático para o dashboard.

| Código | Categoria | Grupo sugerido |
|---|---|---|
| 10 | Homossexual | Homossexual |
| 11–15 | Homossexual combinado com drogas, hemofilia ou transfusão | Homossexual |
| 20 | Bissexual | Bissexual |
| 21–25 | Bissexual combinado com drogas, hemofilia ou transfusão | Bissexual |
| 30 | Heterossexual | Heterossexual |
| 31–35 | Heterossexual combinado com drogas, hemofilia ou transfusão | Heterossexual |
| 36 | Heterossexual com parceria de risco indefinido | Heterossexual |
| 40–42 | Uso de drogas injetáveis (com ou sem hemofilia/transfusão) | Drogas injetáveis |
| 50 | Hemofílico | Sanguínea |
| 59, 60–69 | Transfusão e combinações | Sanguínea |
| 70 | Acidente com material biológico, com soroconversão em até 6 meses | Acidente biológico |
| 80 | Perinatal (transmissão vertical) | Vertical |
| 90 | Ignorado | Ignorado |

O agrupamento por grupo é uma proposta para simplificar a leitura. A categoria original continua disponível. O dicionário traz inconsistências nessa lista: os códigos 68 e 69 têm a mesma descrição, e o código 59 aparece fora de ordem. Vamos conferir que códigos aparecem de fato na base.

**Campos de origem da categoria (informados na ficha):**

| Campo | Significado | Categorias |
|---|---|---|
| `ANT_TRASMI` | Transmissão vertical (mãe para filho) | 1 Sim · 2 Não · 9 Ignorado |
| `ANTRELSE_N` | Transmissão sexual | 1 Relações com homens · 2 Relações com mulheres · 3 Relações com homens e mulheres · 4 Não foi sexual · 9 Ignorado |
| `ANT_DROGA` | Uso de drogas injetáveis | 1 Sim · 2 Não · 9 Ignorado |
| `ANT_HEMOLF` | Tratamento para hemofilia ou hemotransfusão | 1 Sim · 2 Não · **3 Ignorado** (atenção: aqui o código de ignorado é 3, não 9) |
| `ANTTRANS_M` | Transfusão sanguínea | 1 Sim · 2 Não · 9 Ignorado |
| `ANT_ACIDEN` | Acidente com material biológico, com soroconversão em até 6 meses | 1 Sim · 2 Não · 9 Ignorado |

### Critério e evolução

| Campo | Significado | Categorias |
|---|---|---|
| `CRITERIO` | Critério de definição de caso (campo interno) | 100 CDC adaptado · 300 Rio de Janeiro/Caracas · 600 Critério óbito · **900 Descartado** · 901 HIV+ |
| `DEF_DIAGNO` | Critério óbito: declaração de óbito com menção a aids/HIV, sem outro critério após investigação | 1 Sim · 2 Não · 9 Ignorado |
| `EVOLUCAO` | Evolução do caso | 1 Vivo · 2 Óbito por aids · 3 Óbito por outras causas · 9 Ignorado |
| `DT_OBITO` | Data do óbito | Data |

Em linguagem simples: **901 (HIV+)** é a pessoa com infecção pelo HIV confirmada. Os critérios **100, 300 e 600** indicam que o caso já preenche a definição de **aids** (doença avançada), seja por doenças oportunistas, por pontuação clínica ou pelo óbito. **900 (Descartado)** não é caso e deve ser excluído das contagens.

Os campos `ANT_SARCOM` a `ANT_CONTAG` são os sinais clínicos usados para pontuar os critérios Rio de Janeiro/Caracas e CDC adaptado. Eles não entram no dashboard. Os campos de laboratório (`LAB_TRIAGE`, `LAB_CONFIR` e `TPRAPIDO1` a `TPRAPIDO3`) podem servir para checar a qualidade, mas não são prioridade.

---

## 2. Como decodificar `NU_IDADE_N`

A idade tem 4 dígitos. O **1º dígito é a unidade** e os **3 seguintes são o valor**:

| 1º dígito | Unidade | Exemplo | Leitura |
|---|---|---|---|
| 1 | Horas | 1012 | 12 horas |
| 2 | Dias | 2015 | 15 dias |
| 3 | Meses | 3009 | 9 meses |
| 4 | Anos | 4018 | 18 anos |

**Regra para converter em anos:** se o 1º dígito for 4, a idade é o valor em anos. Se for 1, 2 ou 3, a pessoa tem menos de 1 ano (idade = 0). Qualquer outro valor é tratado como ignorado.

Pela regra do dicionário, quando não há data de nascimento, registra-se a idade informada pelo paciente ou, na falta dela, a **idade aparente**. Por isso a idade pode ser aproximada.

**Faixas etárias propostas:** <15, 15–19, 20–24, 25–29, 30–34, 35–39, 40–49, 50–59, 60+, compatíveis com as faixas usadas nos boletins de HIV/aids. Como o dicionário é de **HIV adulto**, espera-se pouca gente com menos de 13 anos. Os casos em crianças costumam ser notificados em ficha própria (HIV em criança), que não está nesta base.

---

## 3. Município de notificação × município de residência

| | Município de notificação (`ID_MUNICIP`) | Município de residência (`ID_MN_RESI`) |
|---|---|---|
| O que é | Onde fica a **unidade de saúde** que preencheu a ficha | Onde a **pessoa mora** |
| O que mostra | Onde os serviços estão diagnosticando e notificando | Onde está a população afetada |
| Uso típico | Avaliar a carga de trabalho e o desempenho dos serviços | Medir a situação epidemiológica do território e calcular taxas |

**Qual usar: residência (`ID_MN_RESI`) como padrão.** É o critério usado pelo Ministério da Saúde nos boletins epidemiológicos. Também é o único coerente com taxas por habitante, já que a população do denominador é a de moradores.

**Por que isso importa no Baixo Amazonas:** Santarém é o polo regional e concentra serviços especializados. Muitos moradores dos municípios vizinhos podem ser diagnosticados e notificados em Santarém. Pelo município de notificação, Santarém pareceria ter mais casos e os vizinhos menos. Pelo de residência, cada caso volta ao município onde a pessoa mora.

**Uso complementar sugerido:** cruzar residência com notificação para mostrar o **fluxo de pacientes** (quantos moradores de cada município foram notificados em outro). Isso ajuda a planejar a rede.

**A conferir na base:** o dicionário diz que os códigos de município têm 6 dígitos, mas nas primeiras linhas do CSV `ID_MUNICIP` e `ID_MN_RESI` aparecem com 7 dígitos (com o dígito verificador do IBGE), enquanto `TRA_MUNICI` aparece com 6. Os filtros precisam tratar os dois formatos.

---

## 4. Ano de referência: notificação ou diagnóstico

O dicionário traz duas datas: **notificação** (`DT_NOTIFIC`/`NU_ANO`) e **diagnóstico** (`DT_DIAG`). Elas podem ser bem distantes. Pessoas diagnosticadas há anos podem ser notificadas só depois (por exemplo, quando entram no serviço ou quando o HIV passou a ser de notificação compulsória). **Proposta:** usar o **ano de diagnóstico** para a série histórica e o ano de notificação para medir o volume de trabalho da vigilância. Vamos decidir depois de ver a distribuição das datas.

---

## 5. Campos com risco de baixa qualidade (hipóteses a verificar)

| Campo | Risco | Por quê |
|---|---|---|
| `CS_ESCOL_N` | **Alto** | Costuma ter muito "Ignorado" (9) ou ficar em branco no SINAN |
| `CS_RACA` | Médio/alto | Deveria ser autodeclarada, mas muitas vezes é atribuída por quem preenche ou fica como Ignorado |
| `ANT_REL_CA` e campos de transmissão | **Alto** | Dependem de perguntas sensíveis (vida sexual, drogas). Muito "Ignorado" (90). A categoria é calculada pelo sistema, então um erro nos campos de origem passa para ela |
| `ANT_HEMOLF` | Médio | O código de ignorado é diferente (3), o que confunde a digitação |
| `EVOLUCAO` / `DT_OBITO` | **Alto** | A ficha raramente é atualizada depois da notificação, então "Vivo" pode estar desatualizado. Óbitos ficam subestimados se não houver cruzamento com o SIM (sistema de mortalidade) |
| `CS_GESTANT` | Médio | Pode haver incoerência com sexo e idade (ex.: homem como gestante, ou mulher em idade fértil marcada "Não se aplica"). Gestantes com HIV têm notificação própria, o que pode reduzir o registro aqui |
| `NU_IDADE_N` | Baixo/médio | Pode ser idade aparente. Pode haver valores fora do padrão |
| `DT_DIAG` | Médio | Datas de diagnóstico antigas ou padronizadas (ex.: 1º de janeiro) indicam data aproximada |
| `ID_OCUPA_N` | Alto | Muito vazio no SINAN. Não foi incluído no resumo |
| `ID_MN_RESI` | Baixo | Geralmente bem preenchido, mas o endereço pode ser de onde a pessoa estava quando foi atendida |
| Anos recentes (2024–2025) | **Alto** | Atraso na digitação e na transferência das fichas: os últimos anos tendem a estar incompletos |

**Lembretes gerais:** notificação não é incidência. O número de notificações depende também da oferta de testagem e da capacidade de notificar de cada município. Em municípios pequenos, poucos casos a mais ou a menos mudam muito as proporções.
