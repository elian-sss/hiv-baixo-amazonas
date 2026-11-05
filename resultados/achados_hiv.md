# Perfil dos casos de HIV e achados principais — Baixo Amazonas

Gerado por `scripts/04_perfil.py` a partir de `dados/hiv_baixo_amazonas.csv`. **Recorte: notificações de 2016 a 2023 (n = 1.507)**, residentes nos 13 municípios. 2024 ficou de fora das comparações por ter só janeiro a junho (está nos CSVs `perfil_*_ano.csv`).

**Como ler a mudança:** comparamos dois períodos de quatro anos (2016–2019 × 2020–2023), porque ano a ano os números são pequenos. A coluna "Diferença além do acaso?" usa um teste de duas proporções (5%): "não" quer dizer que a diferença pode ser só oscilação. Um "sim" mostra diferença nas **notificações**, não prova mudança na epidemia.

> Notificação não é incidência. Casos dependem de testagem, acesso e qualidade do preenchimento.

## 1. Percentual de ignorados por campo

Ignorado = código 9/99/90, campo vazio ou idade não informada.

| Campo | 2016–2023 | 2016–2019 | 2020–2023 |
|---|---:|---:|---:|
| Sexo | 0,0% (0) | 0,0% | 0,0% |
| Faixa etária | 0,6% (9) | 1,5% | 0,1% |
| Raça/cor | 0,5% (7) | 0,8% | 0,3% |
| Escolaridade | 5,4% (81) | 10,6% | 2,6% |
| Categoria de exposição | 4,4% (67) | 4,0% | 4,7% |
| Evolução | 0,7% (10) | 1,1% | 0,4% |
| Gestante (só mulheres) | 1,0% (4) | 1,7% | 0,4% |

Observação: escolaridade também tem "Não se aplica" = 0. Em evolução, o campo está preenchido, mas é atualizado raramente; dos 18 óbitos, 0 estão sem data de óbito.

## 2. Sexo

| Categoria | 2016–2023 n | % | 2016–2019 % (n=529) | 2020–2023 % (n=978) | Diferença (p.p.) | Diferença além do acaso? |
|---|---:|---:|---:|---:|---:|---|
| Masculino | 1.088 | 72,2% | 66,7% | 75,2% | +8,4 | sim (p<0,05) |
| Feminino | 419 | 27,8% | 33,3% | 24,8% | -8,4 | sim (p<0,05) |
| **Total** | **1.507** | 100% | 100% | 100% | | |

Razão de sexo (homens por mulher), por ano: 2016: 2,1, 2017: 1,4, 2018: 2,4, 2019: 2,4, 2020: 2,6, 2021: 3,2, 2022: 3,4, 2023: 2,9.

## 3. Faixa etária

| Categoria | 2016–2023 n | % | 2016–2019 % (n=529) | 2020–2023 % (n=978) | Diferença (p.p.) | Diferença além do acaso? |
|---|---:|---:|---:|---:|---:|---|
| <15 | 3 | 0,2% | 0,2% | 0,2% | +0,0 | não |
| 15-19 | 120 | 8,0% | 10,0% | 6,9% | -3,2 | sim (p<0,05) |
| 20-24 | 333 | 22,1% | 19,3% | 23,6% | +4,3 | não |
| 25-29 | 292 | 19,4% | 17,4% | 20,4% | +3,1 | não |
| 30-39 | 399 | 26,5% | 26,8% | 26,3% | -0,6 | não |
| 40-49 | 228 | 15,1% | 16,6% | 14,3% | -2,3 | não |
| 50-59 | 85 | 5,6% | 5,9% | 5,5% | -0,3 | não |
| 60+ | 38 | 2,5% | 2,3% | 2,7% | +0,4 | não |
| Ignorada | 9 | 0,6% | 1,5% | 0,1% | -1,4 | sim (p<0,05) |
| **Total** | **1.507** | 100% | 100% | 100% | | |

Mediana de idade: 30 anos em 2016–2023 (30 em 2016–2019; 29 em 2020–2023). Pessoas de 15 a 29 anos: 745 (49,7% dos casos com idade informada).

Faixa etária por sexo (2016–2023, n):

| Faixa | Masculino | Feminino |
|---|---:|---:|
| <15 | 1 | 2 |
| 15-19 | 84 | 36 |
| 20-24 | 251 | 82 |
| 25-29 | 220 | 72 |
| 30-39 | 284 | 115 |
| 40-49 | 152 | 76 |
| 50-59 | 58 | 27 |
| 60+ | 31 | 7 |
| Ignorada | 7 | 2 |

## 4. Raça/cor

| Categoria | 2016–2023 n | % | 2016–2019 % (n=529) | 2020–2023 % (n=978) | Diferença (p.p.) | Diferença além do acaso? |
|---|---:|---:|---:|---:|---:|---|
| Parda | 1.437 | 95,4% | 93,4% | 96,4% | +3,0 | sim (p<0,05) |
| Preta | 26 | 1,7% | 2,3% | 1,4% | -0,8 | não |
| Branca | 24 | 1,6% | 2,1% | 1,3% | -0,8 | não |
| Indígena | 8 | 0,5% | 1,1% | 0,2% | -0,9 | sim (p<0,05) |
| Amarela | 5 | 0,3% | 0,4% | 0,3% | -0,1 | não |
| Ignorado | 7 | 0,5% | 0,8% | 0,3% | -0,4 | não |
| **Total** | **1.507** | 100% | 100% | 100% | | |

## 5. Escolaridade

| Categoria | 2016–2023 n | % | 2016–2019 % (n=529) | 2020–2023 % (n=978) | Diferença (p.p.) | Diferença além do acaso? |
|---|---:|---:|---:|---:|---:|---|
| Até fundamental incompleto | 257 | 17,1% | 32,3% | 8,8% | -23,5 | sim (p<0,05) |
| Fundamental completo / médio incompleto | 424 | 28,1% | 28,0% | 28,2% | +0,2 | não |
| Médio completo / superior incompleto | 541 | 35,9% | 21,6% | 43,7% | +22,1 | sim (p<0,05) |
| Superior completo | 204 | 13,5% | 7,6% | 16,8% | +9,2 | sim (p<0,05) |
| Ignorado | 81 | 5,4% | 10,6% | 2,6% | -8,0 | sim (p<0,05) |
| **Total** | **1.507** | 100% | 100% | 100% | | |

## 6. Categoria de exposição

| Categoria | 2016–2023 n | % | 2016–2019 % (n=529) | 2020–2023 % (n=978) | Diferença (p.p.) | Diferença além do acaso? |
|---|---:|---:|---:|---:|---:|---|
| Heterossexual | 806 | 53,5% | 58,6% | 50,7% | -7,9 | sim (p<0,05) |
| Homossexual | 473 | 31,4% | 22,3% | 36,3% | +14,0 | sim (p<0,05) |
| Bissexual | 140 | 9,3% | 13,2% | 7,2% | -6,1 | sim (p<0,05) |
| Vertical | 21 | 1,4% | 1,9% | 1,1% | -0,8 | não |
| Ignorado | 67 | 4,4% | 4,0% | 4,7% | +0,7 | não |
| **Total** | **1.507** | 100% | 100% | 100% | | |

Só homens (n=1.088):

| Categoria | 2016–2023 n | % | 2016–2019 % (n=353) | 2020–2023 % (n=735) | Diferença (p.p.) | Diferença além do acaso? |
|---|---:|---:|---:|---:|---:|---|
| Heterossexual | 414 | 38,1% | 42,2% | 36,1% | -6,2 | não |
| Homossexual | 467 | 42,9% | 32,6% | 47,9% | +15,3 | sim (p<0,05) |
| Bissexual | 139 | 12,8% | 19,8% | 9,4% | -10,4 | sim (p<0,05) |
| Vertical | 14 | 1,3% | 1,1% | 1,4% | +0,2 | não |
| Ignorado | 54 | 5,0% | 4,2% | 5,3% | +1,1 | não |
| **Total** | **1.088** | 100% | 100% | 100% | | |

Só mulheres (n=419):

| Categoria | 2016–2023 n | % | 2016–2019 % (n=176) | 2020–2023 % (n=243) | Diferença (p.p.) | Diferença além do acaso? |
|---|---:|---:|---:|---:|---:|---|
| Heterossexual | 392 | 93,6% | 91,5% | 95,1% | +3,6 | não |
| Homossexual | 6 | 1,4% | 1,7% | 1,2% | -0,5 | não |
| Bissexual | 1 | 0,2% | 0,0% | 0,4% | +0,4 | não |
| Vertical | 7 | 1,7% | 3,4% | 0,4% | -3,0 | sim (p<0,05) |
| Ignorado | 13 | 3,1% | 3,4% | 2,9% | -0,5 | não |
| **Total** | **419** | 100% | 100% | 100% | | |

## 7. Gestantes

- Mulheres notificadas que estavam gestantes: **96 de 419 (22,9%)** em 2016–2023.
- 2016–2019: 33 de 176 (18,8%); 2020–2023: 63 de 243 (25,9%). Diferença além do acaso? não (p = 0,085).
- Momento da gestação: 2º trimestre: 45, 3º trimestre: 25, 1º trimestre: 20, Idade gestacional ignorada: 6.
- Por ano (gestantes / mulheres): 2016: 10/47, 2017: 12/52, 2018: 4/30, 2019: 7/47, 2020: 19/53, 2021: 21/60, 2022: 14/66, 2023: 9/64.
- Limitação: gestantes com HIV têm ficha própria no SINAN (HIV em gestante); esta base pode não captar todas.

## 8. Evolução

| Categoria | 2016–2023 n | % | 2016–2019 % (n=529) | 2020–2023 % (n=978) | Diferença (p.p.) | Diferença além do acaso? |
|---|---:|---:|---:|---:|---:|---|
| Vivo | 1.479 | 98,1% | 97,5% | 98,5% | +0,9 | não |
| Óbito por aids | 9 | 0,6% | 0,6% | 0,6% | +0,0 | não |
| Óbito por outras causas | 9 | 0,6% | 0,8% | 0,5% | -0,2 | não |
| Ignorado | 10 | 0,7% | 1,1% | 0,4% | -0,7 | não |
| **Total** | **1.507** | 100% | 100% | 100% | | |

## 9. Cinco achados principais

Todos sobre notificações de residentes nos 13 municípios, 2016–2023 (n = 1.507).

### Achado 1 — Os casos notificados são majoritariamente de homens, e a participação masculina aumentou

- **Número:** homens são 72,2% dos casos (1.088 de 1.507). A participação das mulheres caiu de 33,3% (2016–2019) para 24,8% (2020–2023), diferença além do acaso. A razão homem/mulher foi de 2,1 em 2016 para 2,9 em 2023 (máximo de 3,4 em 2022).
- **Período:** 2016–2023.
- **Limitação:** reflete quem foi testado e notificado. Mulheres são testadas de rotina no pré-natal e homens buscam menos os serviços; a mudança pode ser de testagem, não de transmissão.
- **Pergunta de vigilância:** a oferta de testagem para homens mudou a partir de 2019 nos serviços que mais notificam, e as mulheres fora do pré-natal estão sendo testadas?

### Achado 2 — Entre homens, cresceu a exposição homossexual e caiu a bissexual

- **Número:** entre homens, a categoria homossexual passou de 32,6% para 47,9% e a bissexual de 19,8% para 9,4% (as duas diferenças além do acaso). Somadas (homens que fazem sexo com homens), foram de 52,4% para 57,3%. Na região toda, a heterossexual segue como a maior categoria (53,5%).
- **Período:** 2016–2019 × 2020–2023.
- **Limitação:** a categoria é informada pelo paciente sobre um tema sensível e calculada pelo sistema; 5,0% dos homens têm exposição ignorada. A troca entre "bissexual" e "homossexual" pode ser mudança na forma de perguntar ou registrar, não de comportamento.
- **Pergunta de vigilância:** houve mudança no preenchimento da ficha (quem pergunta e como) ou ampliação de ações de testagem voltadas a homens que fazem sexo com homens na região?

### Achado 3 — Metade dos casos é de jovens de 15 a 29 anos

- **Número:** 745 casos (49,7% dos que têm idade informada) têm 15 a 29 anos; a mediana de idade é 30 anos. A faixa de 20 a 24 anos sozinha tem 22,1%. A faixa de 15 a 19 anos caiu de 10,0% para 6,9% (53 e 67 casos), diferença além do acaso.
- **Período:** 2016–2023.
- **Limitação:** a idade pode ser a aparente (sem data de nascimento) e a data é a da notificação, não a da infecção, que pode ter ocorrido anos antes. A ficha é de HIV adulto.
- **Pergunta de vigilância:** onde esses jovens estão sendo diagnosticados, e a queda entre 15 e 19 anos é de casos ou de testagem de adolescentes?

### Achado 4 — Quase uma em cada quatro mulheres notificadas estava gestante, a maioria no 2º ou 3º trimestre

- **Número:** 96 de 419 mulheres (22,9%) estavam gestantes na notificação; 70 delas (72,9%) no 2º ou 3º trimestre e 20 no 1º. A proporção foi de 18,8% (2016–2019) para 25,9% (2020–2023), diferença que pode ser acaso (p = 0,08). Há ainda 21 casos de transmissão vertical (mãe para filho) no período.
- **Período:** 2016–2023.
- **Limitação:** o trimestre é o da notificação, não o do diagnóstico; gestantes com HIV têm ficha própria no SINAN, que não está nesta base, então o número pode estar incompleto.
- **Pergunta de vigilância:** as gestantes estão sendo testadas no 1º trimestre do pré-natal, como recomendado, e todas as gestantes com HIV foram também notificadas na ficha de gestante?

### Achado 5 — O preenchimento melhorou, mas a evolução dos casos não é acompanhada

- **Número:** escolaridade ignorada caiu de 10,6% para 2,6%. Ao mesmo tempo, "até fundamental incompleto" caiu de 32,3% para 8,8%, mudança muito grande para quatro anos. Na evolução, 98,1% constam como vivos e só 18 óbitos foram registrados (9 por aids).
- **Período:** 2016–2023.
- **Limitação:** a evolução é registrada na notificação e raramente atualizada, então os óbitos não medem mortalidade. A mudança brusca na escolaridade pode ser de preenchimento e não do perfil das pessoas.
- **Pergunta de vigilância:** os óbitos por aids de residentes estão sendo cruzados com o SIM (Sistema de Informações sobre Mortalidade), e o que mudou no registro da escolaridade a partir de 2020?

## 10. O que estes dados não permitem dizer

- Se o risco de HIV é maior num município ou grupo: não há população para calcular taxas.
- Se a epidemia cresceu ou diminuiu: só há notificações, que dependem de testagem.
- Mortalidade por aids: a evolução não é acompanhada nesta ficha.
- Diferenças por município no perfil: com poucos casos na maioria dos municípios, os percentuais seriam instáveis (não foram calculados aqui).
