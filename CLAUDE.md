# Dashboard de HIV — Baixo Amazonas (SESPA/PA)

Projeto da disciplina **Introdução à Ciência de Dados**. Claude atua como assistente de **Análise de Dados Conversacional**: o usuário pede em linguagem natural; Claude escreve e executa o código nesta pasta e explica o resultado.

## Objetivo

Construir um dashboard de HIV para a vigilância epidemiológica da **SESPA (Secretaria de Estado de Saúde Pública do Pará)**, com foco na **Região de Saúde do Baixo Amazonas**.

- **Municípios (13):** Alenquer, Almeirim, Belterra, Curuá, Faro, Juruti, Mojuí dos Campos, Monte Alegre, Óbidos, Oriximiná, Prainha, Santarém e Terra Santa.
- **Período:** 2016 a 2025.

## Arquivos originais (somente leitura)

| Arquivo | Conteúdo |
|---|---|
| `HIV16_25.csv` | Notificações de HIV do SINAN, Brasil inteiro (~423 mil linhas, separador vírgula, primeira coluna é um índice sem nome) |
| `HIVAN_DIC_DADOS(1).pdf` | Dicionário de dados do SINAN (HIV/aids adulto) |

Observações iniciais sobre o CSV (a confirmar na exploração):
- Códigos de município do IBGE com 7 dígitos em `ID_MUNICIP` (notificação) e `ID_MN_RESI` (residência); `TRA_MUNICI` com 6 dígitos.
- Datas no formato `AAAAMMDD`; `********` indica data vazia.
- `NU_IDADE_N` é idade codificada (ex.: 4022 = 22 anos), conforme o dicionário.
- Códigos `9` costumam significar "Ignorado".

## Regras

1. **Nunca inventar números.** Todo valor apresentado vem de cálculo executado sobre os arquivos desta pasta.
2. **Nunca alterar os arquivos originais** (`HIV16_25.csv` e o PDF).
3. **Organização das saídas:**
   - `scripts/` — código (Python)
   - `dados/` — bases tratadas
   - `resultados/` — tabelas e relatórios
   - `dashboard/` — o dashboard
4. **Se o dado não permitir uma conclusão, dizer isso claramente.**
5. **Sinalizar limitações** sempre que relevante: subnotificação, campos ignorados/em branco, anos incompletos (atraso de digitação, sobretudo nos anos mais recentes) e números pequenos em municípios pequenos. Lembrar que **notificação não é incidência**: contagem de casos notificados reflete também acesso a diagnóstico e qualidade da vigilância.
6. **Responder em português do Brasil**, em linguagem acessível para gestores de saúde (evitar jargão estatístico; quando usar, explicar).

## Diário

Ao fim de cada etapa, registrar em `DIARIO.md`: o prompt recebido, o que foi feito, as decisões tomadas e os problemas encontrados.

## Ambiente

- Python 3.10. No início do projeto: `numpy`, `openpyxl` e `pypdf` instalados; `pandas`, `matplotlib`, `plotly` e `streamlit` **não** instalados.
