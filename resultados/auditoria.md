# Auditoria dos totais do dashboard

Gerado por `scripts/05_auditoria.py`. Os totais foram recalculados por **métodos independentes** dos usados na limpeza e no dashboard: leitura com a biblioteca padrão `csv` (sem pandas), ano tirado do texto da data de notificação e município tirado do código IBGE, com tabela de nomes própria deste script.

| Fonte | Como foi calculada |
|---|---|
| **A** | `dados/hiv_baixo_amazonas.csv` (base tratada), sem usar as colunas derivadas `ANO_NOTIF`/`MUNICIPIO` |
| **B** | `HIV16_25.csv` (original), recorte refeito do zero: residência nos 13 códigos, 1 duplicado(s) exato(s) removido(s), 0 registro(s) com CRITERIO 900 excluído(s) |
| **JSON** | `dados/dados_dashboard.json`: bloco `conferencia`, lista `anos` e soma de cada cubo |
| **JSON público** | `dados/dados_dashboard_publico.json` (versão do GitHub Pages): totais e soma de cada cubo |
| **HTML** | JSON embutido em `dashboard/index_interno.html` (interno) e em `dashboard/index.html` (público) |

## Resultado

- Divergências encontradas: **0**.
- Total geral: A = 1.596, B = 1.596, JSON = 1.596 → iguais.
- JSON embutido no painel interno idêntico a `dados_dashboard.json`: **sim**; no painel público, idêntico a `dados_dashboard_publico.json`: **sim**.
- Cubos da versão pública conferidos: base, fluxo, perfil, exposicao, evolucao, raca, escolaridade (os territoriais por município × ano; os de perfil, que são da região inteira, por ano).
- Cubos conferidos (município × ano): base, exposicao, evolucao, raca, escolaridade, fluxo. O cubo `gestante` contém só mulheres e foi conferido pelo total de mulheres na geração do JSON.

## Totais por ano

| Ano | A (base tratada) | B (original) | JSON `conferencia` | JSON `anos[].n` | Status no JSON | Confere? |
|---|---:|---:|---:|---:|---|---|
| 2016 | 145 | 145 | 145 | 145 | completo | ✔ |
| 2017 | 123 | 123 | 123 | 123 | completo | ✔ |
| 2018 | 103 | 103 | 103 | 103 | completo | ✔ |
| 2019 | 158 | 158 | 158 | 158 | completo | ✔ |
| 2020 | 189 | 189 | 189 | 189 | completo | ✔ |
| 2021 | 251 | 251 | 251 | 251 | completo | ✔ |
| 2022 | 290 | 290 | 290 | 290 | completo | ✔ |
| 2023 | 248 | 248 | 248 | 248 | completo | ✔ |
| 2024 | 89 | 89 | 89 | 89 | parcial | ✔ |
| 2025 | 0 | 0 | 0 | — (sem dados) | sem_dados | ✔ |
| **Total** | **1.596** | **1.596** | **1.596** | **1.596** | | |

## Totais por município

| Município | A | B | JSON `conferencia` | JSON cubo `base` | Confere? |
|---|---:|---:|---:|---:|---|
| Alenquer | 55 | 55 | 55 | 55 | ✔ |
| Almeirim | 22 | 22 | 22 | 22 | ✔ |
| Belterra | 22 | 22 | 22 | 22 | ✔ |
| Curuá | 18 | 18 | 18 | 18 | ✔ |
| Faro | 16 | 16 | 16 | 16 | ✔ |
| Juruti | 63 | 63 | 63 | 63 | ✔ |
| Mojuí dos Campos | 26 | 26 | 26 | 26 | ✔ |
| Monte Alegre | 52 | 52 | 52 | 52 | ✔ |
| Óbidos | 99 | 99 | 99 | 99 | ✔ |
| Oriximiná | 102 | 102 | 102 | 102 | ✔ |
| Prainha | 24 | 24 | 24 | 24 | ✔ |
| Santarém | 1.083 | 1.083 | 1.083 | 1.083 | ✔ |
| Terra Santa | 14 | 14 | 14 | 14 | ✔ |

## Divergências e correções

Nenhuma divergência. Os 13 totais por município, os totais por ano e as 106 combinações município × ano com casos são idênticos nas fontes A, B, no JSON e em cada cubo. **Nenhuma correção foi necessária.**

## O que esta auditoria não cobre

- Confere contagens por ano e município, não a correção dos rótulos (sexo, idade, exposição etc.), que foram conferidos na limpeza (`resultados/decisoes_limpeza.md`).
- Não verifica a qualidade do dado na origem (SINAN): subnotificação e erros de digitação continuam possíveis.
- Os cálculos feitos no navegador (percentuais, variações) usam os mesmos cubos; foram conferidos por amostragem na etapa 7 (KPIs comparados com `achados_hiv.md`).
