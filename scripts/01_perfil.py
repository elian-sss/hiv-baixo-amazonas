"""Etapa 2 - Perfil geral da base HIV16_25.csv (Brasil inteiro, sem filtros).

Lê tudo como texto (dtype=str), descarta a coluna de índice sem nome e gera
resultados/perfil_hiv.md com: dimensões, distribuição de NU_ANO, TP_NOT e
ID_AGRAVO, ausentes por coluna (vazio ou "********") e duplicados.
Não altera o arquivo original.

Uso: python scripts/01_perfil.py   (a partir da pasta do projeto)
"""
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
ARQ = RAIZ / "HIV16_25.csv"
SAIDA = RAIZ / "resultados" / "perfil_hiv.md"


def fmt(n):
    return f"{n:,}".replace(",", ".")


def pct(x):
    return f"{x:.1f}%".replace(".", ",")


def tabela(serie, rotulo):
    """Tabela markdown de contagens com percentual."""
    total = serie.sum()
    linhas = [f"| {rotulo} | Registros | % |", "|---|---:|---:|"]
    for k, v in serie.items():
        linhas.append(f"| {k} | {fmt(v)} | {pct(100 * v / total)} |")
    linhas.append(f"| **Total** | **{fmt(total)}** | 100,0% |")
    return "\n".join(linhas)


def main():
    # keep_default_na=False: nada é convertido em NaN automaticamente;
    # tratamos vazios e "********" explicitamente.
    df = pd.read_csv(ARQ, dtype=str, keep_default_na=False, na_values=[])
    linhas_brutas, colunas_brutas = df.shape
    col_indice = [c for c in df.columns if c == "" or c.startswith("Unnamed")]
    df = df.drop(columns=col_indice)
    n, m = df.shape

    # Ausente = vazio/só espaços ou só asteriscos (ex.: "********")
    limpo = df.apply(lambda s: s.str.strip())
    ausente = (limpo == "") | limpo.apply(lambda s: s.str.fullmatch(r"\*+").fillna(False))
    so_vazio = (limpo == "").sum()
    so_ast = ausente.sum() - so_vazio
    tab_aus = pd.DataFrame({
        "vazio": so_vazio,
        "asteriscos": so_ast,
        "total_ausente": ausente.sum(),
    })
    tab_aus["pct"] = 100 * tab_aus["total_ausente"] / n

    # Duplicados: linhas idênticas em todas as colunas (sem o índice)
    dup_mask = df.duplicated(keep="first")
    n_dup = int(dup_mask.sum())
    n_dup_grupos = int(df[df.duplicated(keep=False)].drop_duplicates().shape[0])

    # Distribuições
    d_ano = df["NU_ANO"].value_counts().sort_index()
    d_tpnot = df["TP_NOT"].value_counts().sort_index()
    d_agravo = df["ID_AGRAVO"].value_counts()

    # Apoio para avaliar cobertura temporal
    dt_not = pd.to_datetime(df["DT_NOTIFIC"], format="%Y%m%d", errors="coerce")
    ano_dtnot = dt_not.dt.year
    coerencia = (ano_dtnot.astype("Int64").astype(str) == df["NU_ANO"]).mean() * 100
    ultimo_ano = d_ano.index.max()
    mensal_ultimo = (dt_not[df["NU_ANO"] == ultimo_ano].dt.month
                     .value_counts().sort_index())
    mensal_penult = (dt_not[df["NU_ANO"] == str(int(ultimo_ano) - 1)].dt.month
                     .value_counts().sort_index())
    dt_diag = pd.to_datetime(df["DT_DIAG"], format="%Y%m%d", errors="coerce")
    ano_diag = dt_diag.dt.year.astype("Int64").value_counts().sort_index()

    # Também: linhas com quantidade de colunas fora do padrão (leitura ok?)
    # (pandas já falharia se houvesse; registramos que a leitura foi limpa)

    out = []
    out.append("# Perfil da base HIV16_25.csv (Brasil, sem filtros)\n")
    out.append("Gerado por `scripts/01_perfil.py`. Todos os números abaixo foram calculados "
               "sobre o arquivo original, lido inteiramente como texto. **Nenhum filtro de "
               "município ou critério foi aplicado ainda.**\n")
    out.append("## 1. Dimensões\n")
    out.append(f"- Arquivo bruto: {fmt(linhas_brutas)} linhas de dados × {colunas_brutas} colunas.")
    out.append(f"- Coluna de índice sem nome descartada: {len(col_indice)}.")
    out.append(f"- Base de trabalho: **{fmt(n)} registros × {m} colunas**.\n")

    out.append("## 2. Ano de notificação (`NU_ANO`)\n")
    out.append(tabela(d_ano, "NU_ANO") + "\n")
    out.append(f"- Ano de `DT_NOTIFIC` coincide com `NU_ANO` em {pct(coerencia)} dos registros.")
    out.append(f"- Data de notificação mínima: {dt_not.min():%d/%m/%Y}; máxima: {dt_not.max():%d/%m/%Y}.\n")
    out.append(f"### Notificações por mês em {int(ultimo_ano) - 1} e {ultimo_ano}\n")
    meses = sorted(set(mensal_penult.index) | set(mensal_ultimo.index))
    out.append(f"| Mês | {int(ultimo_ano) - 1} | {ultimo_ano} |")
    out.append("|---|---:|---:|")
    for mth in meses:
        a = mensal_penult.get(mth, 0)
        b = mensal_ultimo.get(mth, 0)
        out.append(f"| {int(mth):02d} | {fmt(int(a))} | {fmt(int(b))} |")
    out.append("")

    out.append("## 3. Tipo de notificação (`TP_NOT`)\n")
    out.append("Dicionário: 1 Negativa · 2 Individual · 3 Surto · 4 Agregado.\n")
    out.append(tabela(d_tpnot, "TP_NOT") + "\n")

    out.append("## 4. Agravo (`ID_AGRAVO`)\n")
    out.append(tabela(d_agravo, "ID_AGRAVO") + "\n")

    out.append("## 5. Ano de diagnóstico (`DT_DIAG`) — apoio\n")
    nulos_diag = int(dt_diag.isna().sum())
    out.append(f"Registros sem data de diagnóstico válida: {fmt(nulos_diag)} "
               f"({pct(100 * nulos_diag / n)}).\n")
    antes = ano_diag[ano_diag.index < 2016]
    out.append(f"- Diagnóstico antes de 2016: {fmt(int(antes.sum()))} registros "
               f"({pct(100 * antes.sum() / n)}); ano mais antigo: {ano_diag.index.min()}.")
    out.append("")
    out.append("| Ano diag. | Registros |")
    out.append("|---|---:|")
    for k, v in ano_diag[ano_diag.index >= 2010].items():
        out.append(f"| {k} | {fmt(int(v))} |")
    out.append("")
    n_2007 = int((df["DT_DIAG"] == "20070101").sum())
    n_0101 = int(df["DT_DIAG"].str.endswith("0101").sum())
    n_diag_depois = int((dt_diag > dt_not).sum())
    out.append(f"- `DT_DIAG` exatamente 01/01/2007 (a data mais antiga da base): "
               f"{fmt(n_2007)} registros ({pct(100 * n_2007 / n)}).")
    out.append(f"- `DT_DIAG` em 1º de janeiro de qualquer ano: {fmt(n_0101)} "
               f"({pct(100 * n_0101 / n)}); se as datas fossem distribuídas ao acaso, "
               f"seria cerca de 0,3% (1/365).")
    out.append(f"- `DT_DIAG` posterior a `DT_NOTIFIC`: {fmt(n_diag_depois)} registros.\n")

    out.append("## 6. Ausentes por coluna\n")
    out.append("Ausente = célula vazia ou formada só por asteriscos (ex.: `********`, "
               "usado pelo SINAN para data vazia). Ordenado do maior para o menor.\n")
    out.append("| Coluna | Vazio | `****` | Total ausente | % |")
    out.append("|---|---:|---:|---:|---:|")
    for col, r in tab_aus.sort_values("pct", ascending=False).iterrows():
        out.append(f"| {col} | {fmt(int(r.vazio))} | {fmt(int(r.asteriscos))} | "
                   f"{fmt(int(r.total_ausente))} | {pct(r.pct)} |")
    out.append("")
    out.append("Observação: o código `9` (Ignorado) **não** foi contado como ausente aqui; "
               "será medido campo a campo na etapa de qualidade.\n")

    out.append("## 7. Duplicados\n")
    out.append(f"- Linhas idênticas em todas as {m} colunas (excluindo a primeira ocorrência): "
               f"**{fmt(n_dup)}** ({pct(100 * n_dup / n)}).")
    out.append(f"- Grupos distintos de linhas repetidas: {fmt(n_dup_grupos)}.")
    out.append("- A base não tem identificador do paciente; por isso não é possível detectar "
               "a mesma pessoa notificada duas vezes com dados ligeiramente diferentes.\n")

    # Pontos de atenção (texto com números calculados acima)
    anos = sorted(d_ano.index)
    faltam = [a for a in range(2016, 2026) if str(a) not in anos]
    media_16_23 = d_ano[[str(a) for a in range(2016, 2024) if str(a) in anos]].mean()
    out.append("## 8. O que chama atenção\n")
    out.append(f"1. **Período coberto: {anos[0]} a {anos[-1]}, não 2016–2025.** "
               f"Anos ausentes: {', '.join(map(str, faltam)) or 'nenhum'}. "
               f"A última notificação é de {dt_not.max():%d/%m/%Y}.")
    out.append(f"2. **{ultimo_ano} está incompleto:** só há notificações de janeiro a "
               f"{int(mensal_ultimo.index.max()):02d}; {fmt(int(d_ano[ultimo_ano]))} registros, "
               f"contra média de {fmt(round(media_16_23))} por ano em 2016–2023. "
               f"Não pode ser comparado com os anos fechados como ano cheio.")
    out.append(f"3. **2020 tem a menor contagem ({fmt(int(d_ano['2020']))})**, "
               "coerente com a redução de testagem e atendimento na pandemia de covid-19; "
               "é queda de notificação, não necessariamente de infecções.")
    out.append("4. `TP_NOT` e `ID_AGRAVO` têm um único valor (individual, B24): a base já vem "
               "filtrada para notificações individuais de HIV adulto.")
    out.append(f"5. **{pct(100 * antes.sum() / n)} dos registros têm diagnóstico anterior a 2016** "
               "(desde 2007): são notificações tardias de casos antigos. Contar por ano de "
               "notificação ou de diagnóstico muda os números.")
    out.append("6. Campos centrais (município, sexo, datas, critério, categoria de exposição, "
               "escolaridade) não têm vazios, mas isso não significa boa qualidade: o "
               "\"Ignorado\" (código 9/90) ainda precisa ser medido.")
    out.append(f"7. `EVOLUCAO` quase completa, mas `DT_OBITO` ausente em "
               f"{pct(tab_aus.loc['DT_OBITO', 'pct'])}: reforça que óbitos tendem a estar "
               "sub-registrados nesta ficha.")
    out.append(f"8. Duplicados exatos são raros ({fmt(n_dup)}); serão removidos na base tratada.\n")

    SAIDA.parent.mkdir(exist_ok=True)
    SAIDA.write_text("\n".join(out), encoding="utf-8")
    print(f"OK: {SAIDA}")


if __name__ == "__main__":
    main()
