# HIV no Baixo Amazonas: dashboard de notificações (SESPA/PA)

Projeto da disciplina **Introdução à Ciência de Dados**. É um painel sobre as notificações de HIV (SINAN/Ministério da Saúde) de pessoas que moram nos 13 municípios da Região de Saúde do Baixo Amazonas (Pará), feito para a vigilância epidemiológica da SESPA.

**Dashboard (versão pública):** https://elian-sss.github.io/hiv-baixo-amazonas/

> **Notificação não é incidência.** Os números mostram casos de HIV notificados no SINAN, não o total de pessoas com HIV nem de novas infecções. Há subnotificação. 2024 tem só janeiro a junho, e 2025 não está na base. Não há população na base, por isso não há taxas.

## O que tem aqui

| Caminho | Conteúdo |
|---|---|
| `dashboard/index.html` | Painel **público** (arquivo único, Chart.js por CDN) |
| `resultados/resumo_achados_hiv.pdf` | Resumo da interpretação dos principais achados |
| `RELATORIO.md` | Resumo do processo e roteiro de apresentação de 5 minutos |
| `DIARIO.md` | Registro de cada etapa: prompt, o que foi feito, decisões e problemas |
| `prompts.txt` | Todos os prompts usados no projeto, na ordem |
| `resultados/` | Relatórios e tabelas agregadas: perfil, limpeza, séries, achados, wireframe, auditoria |
| `scripts/` | Código Python de cada etapa e o modelo do painel |
| `dados/dados_dashboard_publico.json` | Dados agregados usados pelo painel público |

## Privacidade (LGPD)

Dados de saúde são dados pessoais sensíveis (Lei nº 13.709/2018). Por isso:

- **Não estão no repositório:** o arquivo original do SINAN (`HIV16_25.csv`) e a base tratada com registros individuais (`dados/hiv_baixo_amazonas.csv`).
- **A versão pública do painel:**
  - não cruza município com sexo, idade ou outras características;
  - mostra o perfil sempre para a região inteira;
  - exibe como "<5" toda contagem de 1 a 4.
- **A versão interna**, com todos os cruzamentos, também fica fora do repositório (uso da SESPA).

## Como reproduzir

Você precisa do arquivo `HIV16_25.csv` na raiz da pasta. Ele não está neste repositório.

```bash
python scripts/02_limpeza.py
python scripts/03_series.py
python scripts/04_perfil.py
python scripts/05_dados_dashboard.py
python scripts/06_build_dashboard.py
python scripts/05_auditoria.py
python scripts/07_pdf_achados.py
```

Dependências: Python 3.10, `pandas`, `matplotlib`, `pypdf` e `reportlab`.

**Fonte:** Sistema de Informação de Agravos de Notificação (SINAN) / Ministério da Saúde.
