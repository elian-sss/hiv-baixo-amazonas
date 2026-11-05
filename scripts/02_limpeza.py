"""Etapa 3 - Limpeza e recorte da base de HIV para o Baixo Amazonas (PA).

Entrada : HIV16_25.csv (original, somente leitura)
Saídas  : dados/hiv_baixo_amazonas.csv  (base tratada)
          resultados/decisoes_limpeza.md (decisões + tabelas de conferência)

Uso: python scripts/02_limpeza.py   (a partir da pasta do projeto)
"""
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
ARQ = RAIZ / "HIV16_25.csv"
SAIDA_BASE = RAIZ / "dados" / "hiv_baixo_amazonas.csv"
SAIDA_MD = RAIZ / "resultados" / "decisoes_limpeza.md"

# ---------------------------------------------------------------------------
# Municípios. Códigos IBGE de 7 dígitos, conferidos na API de localidades do
# IBGE (servicodados.ibge.gov.br) em 05/11/2026.
# A lista recebida no pedido tinha dois códigos de outros municípios:
#   1501956 = Cachoeira do Piriá (Nordeste Paraense)  -> Curuá é 1502855
#   1505502 = Paragominas (Sudeste Paraense)          -> Monte Alegre é 1504802
# ---------------------------------------------------------------------------
MUNICIPIOS = {
    "1500404": "Alenquer",
    "1500503": "Almeirim",
    "1501451": "Belterra",
    "1502855": "Curuá",
    "1503002": "Faro",
    "1503903": "Juruti",
    "1504752": "Mojuí dos Campos",
    "1504802": "Monte Alegre",
    "1505106": "Óbidos",
    "1505304": "Oriximiná",
    "1506005": "Prainha",
    "1506807": "Santarém",
    "1507979": "Terra Santa",
}
CODIGOS_ERRADOS = {"1501956": "Cachoeira do Piriá", "1505502": "Paragominas"}

COLS_DATA = ["DT_NOTIFIC", "DT_DIAG", "DTTRIAGEM", "DT_CONFIRM", "DT_RAPIDO",
             "DT_OBITO", "ANTDTTRANS"]

SEXO = {"M": "Masculino", "F": "Feminino", "I": "Ignorado"}
RACA = {"1": "Branca", "2": "Preta", "3": "Amarela", "4": "Parda",
        "5": "Indígena", "9": "Ignorado"}
ESCOL = {0: "Analfabeto", 1: "1ª a 4ª série incompleta do EF",
         2: "4ª série completa do EF", 3: "5ª a 8ª série incompleta do EF",
         4: "Ensino fundamental completo", 5: "Ensino médio incompleto",
         6: "Ensino médio completo", 7: "Educação superior incompleta",
         8: "Educação superior completa", 9: "Ignorado", 99: "Ignorado",
         10: "Não se aplica"}
GESTANTE = {"1": "1º trimestre", "2": "2º trimestre", "3": "3º trimestre",
            "4": "Idade gestacional ignorada", "5": "Não", "6": "Não se aplica",
            "9": "Ignorado"}
EVOLUCAO = {"1": "Vivo", "2": "Óbito por aids", "3": "Óbito por outras causas",
            "9": "Ignorado"}
EXPOSICAO = {
    10: "Homossexual", 11: "Homo/Drogas", 12: "Homo/Hemofílico",
    13: "Homo/Transfusão", 14: "Homo/Droga/Hemofílico", 15: "Homo/Droga/Transfusão",
    20: "Bissexual", 21: "Bi/Drogas", 22: "Bi/Hemofílico", 23: "Bi/Transfusão",
    24: "Bi/Droga/Hemofílico", 25: "Bi/Droga/Transfusão",
    30: "Heterossexual", 31: "Hetero/Droga", 32: "Hetero/Hemofílico",
    33: "Hetero/Transfusão", 34: "Hetero/Droga/Hemofílico",
    35: "Hetero/Droga/Transfusão", 36: "Hetero c/ parceria de risco indefinido",
    40: "Drogas", 41: "Drogas/Hemofílico", 42: "Drogas/Transfusão",
    50: "Hemofílico", 59: "Transfusão/Droga/Hetero/Hemofílico",
    60: "Transfusão", 61: "Transfusão/Drogas", 62: "Transfusão/Homo",
    63: "Transfusão/Bi", 64: "Transfusão/Droga/Homossexual",
    65: "Transfusão/Droga/Bissexual", 66: "Transfusão/Hetero",
    67: "Transfusão/Droga/Hetero", 68: "Transfusão/Droga/Homo/Hemofílico",
    69: "Transfusão/Droga/Homo/Hemofílico",
    70: "Acidente com material biológico", 80: "Perinatal", 90: "Ignorado",
}
FAIXAS = [(0, 14, "<15"), (15, 19, "15-19"), (20, 24, "20-24"), (25, 29, "25-29"),
          (30, 39, "30-39"), (40, 49, "40-49"), (50, 59, "50-59"), (60, 200, "60+")]
ORDEM_FAIXAS = [f[2] for f in FAIXAS] + ["Ignorada"]


def fmt(n):
    return f"{int(n):,}".replace(",", ".")


def pct(x):
    return f"{x:.1f}%".replace(".", ",")


def grupo_exposicao(cod):
    """Agrupa a categoria de exposição pela dezena do código (categoria principal
    na hierarquia do SINAN). Combinações (ex.: 11 Homo/Drogas) ficam no grupo da
    categoria sexual, que vem primeiro no código."""
    if pd.isna(cod):
        return "Ignorado"
    if 10 <= cod <= 15:
        return "Homossexual"
    if 20 <= cod <= 25:
        return "Bissexual"
    if 30 <= cod <= 36:
        return "Heterossexual"
    if 40 <= cod <= 42:
        return "Drogas injetáveis"
    if cod == 80:
        return "Vertical"
    if cod == 90:
        return "Ignorado"
    return "Outras"  # 50 hemofilia, 59-69 transfusão, 70 acidente biológico


def decodifica_idade(v):
    """NU_IDADE_N: 1º dígito = unidade (1 h, 2 d, 3 m, 4 anos), 3 dígitos = valor."""
    if not isinstance(v, str) or len(v) != 4 or not v.isdigit():
        return pd.NA
    unidade, valor = v[0], int(v[1:])
    if unidade == "4":
        return valor if valor <= 120 else pd.NA
    if unidade in ("1", "2", "3"):
        return 0
    return pd.NA


def faixa(idade):
    if pd.isna(idade):
        return "Ignorada"
    for lo, hi, rot in FAIXAS:
        if lo <= idade <= hi:
            return rot
    return "Ignorada"


def md_tabela(df, primeira="", total=True):
    d = df.copy()
    if total:
        d["Total"] = d.sum(axis=1)
        d.loc["Total"] = d.sum(axis=0)
    cols = [str(c) for c in d.columns]
    linhas = [f"| {primeira} | " + " | ".join(cols) + " |",
              "|---|" + "---:|" * len(cols)]
    for idx, row in d.iterrows():
        b = "**" if idx == "Total" else ""
        linhas.append(f"| {b}{idx}{b} | " + " | ".join(f"{b}{fmt(v)}{b}" for v in row) + " |")
    return "\n".join(linhas)


def main():
    log = {}
    df = pd.read_csv(ARQ, dtype=str, keep_default_na=False)
    df = df.drop(columns=[c for c in df.columns if c == "" or c.startswith("Unnamed")])
    log["n_brasil"] = len(df)

    # Registros que seriam incluídos pelos códigos errados (para documentar)
    log["errados"] = {f"{c} ({n})": int((df["ID_MN_RESI"] == c).sum())
                      for c, n in CODIGOS_ERRADOS.items()}

    # (1) Filtro por município de RESIDÊNCIA
    df = df[df["ID_MN_RESI"].isin(MUNICIPIOS)].copy()
    log["n_filtro"] = len(df)
    log["regionais"] = sorted(df["ID_RG_RESI"].unique())
    df.insert(0, "MUNICIPIO", df["ID_MN_RESI"].map(MUNICIPIOS))

    # Duplicados exatos
    dup = df.duplicated(keep="first")
    log["n_dup"] = int(dup.sum())
    df = df[~dup].copy()

    # Critério descartado (900)
    descart = df["CRITERIO"] == "900"
    log["n_descartado"] = int(descart.sum())
    df = df[~descart].copy()
    log["criterio"] = df["CRITERIO"].value_counts().to_dict()

    # (2) Datas AAAAMMDD; "********" e vazio = ausente
    log["datas"] = {}
    for c in COLS_DATA:
        bruto = df[c].str.strip()
        ausente = (bruto == "") | bruto.str.fullmatch(r"\*+")
        conv = pd.to_datetime(bruto.where(~ausente), format="%Y%m%d", errors="coerce")
        invalida = int((~ausente & conv.isna()).sum())
        log["datas"][c] = (int(ausente.sum()), invalida)
        df[c] = conv
    df["ANO_NOTIF"] = df["DT_NOTIFIC"].dt.year.astype("Int64")
    df["MES_NOTIF"] = df["DT_NOTIFIC"].dt.month.astype("Int64")
    df["ANO_DIAG"] = df["DT_DIAG"].dt.year.astype("Int64")
    log["anonotif_ok"] = bool((df["ANO_NOTIF"].astype(str) == df["NU_ANO"]).all())

    # (3) Idade e faixas
    df["IDADE_ANOS"] = df["NU_IDADE_N"].map(decodifica_idade).astype("Int64")
    df["FAIXA_ETARIA"] = pd.Categorical(df["IDADE_ANOS"].map(faixa),
                                        categories=ORDEM_FAIXAS, ordered=True)
    log["idade_unid"] = df["NU_IDADE_N"].str[0].value_counts().to_dict()
    log["idade_min_max"] = (df["IDADE_ANOS"].min(), df["IDADE_ANOS"].max())

    # (4) Rótulos
    df["SEXO"] = df["CS_SEXO"].map(SEXO).fillna("Ignorado")
    df["RACA_COR"] = df["CS_RACA"].map(RACA).fillna("Ignorado")
    esc = pd.to_numeric(df["CS_ESCOL_N"], errors="coerce")
    df["ESCOLARIDADE"] = esc.map(ESCOL).fillna("Ignorado")
    df["GESTANTE"] = df["CS_GESTANT"].map(GESTANTE).fillna("Ignorado")
    df["EVOLUCAO_DESC"] = df["EVOLUCAO"].map(EVOLUCAO).fillna("Ignorado")
    exp = pd.to_numeric(df["ANT_REL_CA"], errors="coerce")
    df["CAT_EXPOSICAO"] = exp.map(EXPOSICAO).fillna("Ignorado")
    df["CAT_EXPOSICAO_GRUPO"] = exp.map(grupo_exposicao)
    log["brutos"] = {c: df[c].value_counts().to_dict()
                     for c in ["CS_SEXO", "CS_RACA", "CS_ESCOL_N", "CS_GESTANT",
                               "EVOLUCAO", "ANT_REL_CA"]}
    # Coerência gestante × sexo
    gest_sim = df["CS_GESTANT"].isin(["1", "2", "3", "4"])
    log["gest_masc"] = int((gest_sim & (df["CS_SEXO"] == "M")).sum())
    log["gest_n"] = int((gest_sim & (df["CS_SEXO"] == "F")).sum())

    # Salvar base
    SAIDA_BASE.parent.mkdir(exist_ok=True)
    out = df.copy()
    for c in COLS_DATA:
        out[c] = out[c].dt.strftime("%Y-%m-%d")
    out.to_csv(SAIDA_BASE, index=False, encoding="utf-8-sig")

    # (5) Tabelas de conferência
    import unicodedata
    ordem = sorted(MUNICIPIOS.values(),
                   key=lambda s: unicodedata.normalize("NFKD", s).encode("ascii", "ignore"))
    mun_ano = pd.crosstab(df["MUNICIPIO"], df["ANO_NOTIF"]).reindex(ordem, fill_value=0)
    mun_ano_diag = pd.crosstab(df["MUNICIPIO"], df["ANO_DIAG"]).reindex(ordem, fill_value=0)
    mensal = pd.crosstab(df["MES_NOTIF"], df["ANO_NOTIF"])
    mensal = mensal.reindex(range(1, 13), fill_value=0)
    mensal.index = [f"{m:02d}" for m in mensal.index]
    anos_presentes = sorted(df["ANO_NOTIF"].dropna().unique())
    meses_por_ano = {a: int((mensal[a] > 0).sum()) for a in mensal.columns}
    tem_2025 = 2025 in anos_presentes
    ult = df["DT_NOTIFIC"].max()

    # ---------------------------------------------------------------- relatório
    L = []
    L.append("# Decisões de limpeza: base de HIV do Baixo Amazonas\n")
    L.append("Gerado por `scripts/02_limpeza.py`. Base tratada: `dados/hiv_baixo_amazonas.csv` "
             "(UTF-8, separador vírgula, datas no formato AAAA-MM-DD). O arquivo original não foi alterado.\n")

    L.append("## Resumo do fluxo\n")
    L.append("| Passo | Registros |")
    L.append("|---|---:|")
    L.append(f"| Base Brasil (sem índice) | {fmt(log['n_brasil'])} |")
    L.append(f"| Residentes nos 13 municípios | {fmt(log['n_filtro'])} |")
    L.append(f"| − duplicados exatos | {fmt(log['n_dup'])} |")
    L.append(f"| − critério 900 (descartado) | {fmt(log['n_descartado'])} |")
    L.append(f"| **Base final** | **{fmt(len(df))}** |\n")

    L.append("## Decisão 1 — Recorte pelo município de residência\n")
    L.append("- Filtro em `ID_MN_RESI` (onde a pessoa mora), padrão do Ministério da Saúde e "
             "coerente com taxas por habitante. O município de notificação (`ID_MUNICIP`) foi "
             "mantido na base para análises de fluxo.")
    L.append("- **Correção de dois códigos da lista recebida.** Conferidos na API de localidades "
             "do IBGE:")
    L.append("  - `1501956` é **Cachoeira do Piriá** (Nordeste Paraense). O código de **Curuá** é `1502855`.")
    L.append("  - `1505502` é **Paragominas** (Sudeste Paraense). O código de **Monte Alegre** é `1504802`.")
    errados = "; ".join(f"{k}: {fmt(v)} registros" for k, v in log["errados"].items())
    L.append(f"  - Com a lista original, entrariam por engano: {errados}.")
    L.append(f"- Confirmação interna: todos os registros filtrados têm regional de residência "
             f"(`ID_RG_RESI`) = {', '.join(log['regionais'])}, a mesma para os 13 municípios.")
    L.append("- Coluna `MUNICIPIO` criada com os nomes (com acento).\n")

    L.append("## Decisão 2 — Duplicados e casos descartados\n")
    L.append(f"- Removidos {fmt(log['n_dup'])} registros idênticos em todas as colunas (mantida a 1ª ocorrência).")
    L.append(f"- Removidos {fmt(log['n_descartado'])} registros com `CRITERIO` = 900 (descartado).")
    L.append(f"- Critérios na base final: {log['criterio']} (901 = HIV+).")
    L.append("- Sem identificador do paciente não é possível achar a mesma pessoa notificada "
             "duas vezes com dados diferentes.\n")

    L.append("## Decisão 3 — Datas\n")
    L.append("Formato `AAAAMMDD` convertido para data; `********` ou vazio = ausente; "
             "valor que não forma data válida = ausente (contado abaixo).\n")
    L.append("| Campo | Ausentes | Inválidas | % ausente+inválida |")
    L.append("|---|---:|---:|---:|")
    for c, (a, i) in log["datas"].items():
        L.append(f"| {c} | {fmt(a)} | {fmt(i)} | {pct(100 * (a + i) / len(df))} |")
    L.append("")
    L.append(f"- Criadas `ANO_NOTIF`, `MES_NOTIF` (de `DT_NOTIFIC`) e `ANO_DIAG` (de `DT_DIAG`). "
             f"`ANO_NOTIF` igual a `NU_ANO` em todos os registros: {'sim' if log['anonotif_ok'] else 'não'}.\n")

    L.append("## Decisão 4 — Idade\n")
    L.append("- `NU_IDADE_N`: 1º dígito = unidade (1 hora, 2 dia, 3 mês, 4 ano); 3 últimos = valor. "
             "Unidade 4 → anos; unidades 1–3 → 0 anos; outro valor (ex.: `****`) ou > 120 anos → ignorada.")
    L.append(f"- 1º dígito encontrado: {log['idade_unid']}.")
    L.append(f"- Idade mínima e máxima: {log['idade_min_max'][0]} e {log['idade_min_max'][1]} anos.")
    L.append("- Faixas (`FAIXA_ETARIA`): <15, 15-19, 20-24, 25-29, 30-39, 40-49, 50-59, 60+ e Ignorada.\n")
    L.append(md_tabela(df["FAIXA_ETARIA"].value_counts().sort_index().to_frame("Registros"),
                       "Faixa", total=False) + "\n")

    L.append("## Decisão 5 — Rótulos\n")
    L.append("Códigos convertidos conforme o dicionário (`resultados/dicionario_resumo.md`). "
             "Vazio ou código fora do dicionário → \"Ignorado\". Colunas originais mantidas.\n")
    L.append("| Nova coluna | Origem | Códigos encontrados (contagem) |")
    L.append("|---|---|---|")
    novas = {"CS_SEXO": "SEXO", "CS_RACA": "RACA_COR", "CS_ESCOL_N": "ESCOLARIDADE",
             "CS_GESTANT": "GESTANTE", "EVOLUCAO": "EVOLUCAO_DESC",
             "ANT_REL_CA": "CAT_EXPOSICAO / CAT_EXPOSICAO_GRUPO"}
    for c, nova in novas.items():
        cods = ", ".join(f"`{k or 'vazio'}`: {v}" for k, v in sorted(log["brutos"][c].items()))
        L.append(f"| {nova} | {c} | {cods} |")
    L.append("")
    L.append("- **Escolaridade:** a base usa `99` para Ignorado (o dicionário diz `9`); os dois foram tratados como Ignorado. "
             "Os códigos vêm com zero à esquerda (`06`) e foram lidos como número.")
    L.append(f"- **Gestante:** gestantes (códigos 1–4) do sexo feminino: {fmt(log['gest_n'])}; "
             f"marcadas como gestantes e do sexo masculino: {fmt(log['gest_masc'])}.")
    L.append("- **Categoria de exposição agrupada** (`CAT_EXPOSICAO_GRUPO`), pela dezena do código, "
             "que é a categoria principal na hierarquia do SINAN:")
    L.append("  - Homossexual = 10–15 · Bissexual = 20–25 · Heterossexual = 30–36 · "
             "Drogas injetáveis = 40–42 · Vertical = 80 · Ignorado = 90 · "
             "Outras = 50 (hemofilia), 59–69 (transfusão), 70 (acidente biológico).")
    L.append("  - Combinações como 11 (Homo/Drogas), 21 (Bi/Drogas) e 31 (Hetero/Droga) ficam no grupo sexual. "
             "Alternativa possível: contá-las em \"Drogas injetáveis\". Afeta poucos registros (ver códigos acima).")
    L.append("  - A categoria detalhada fica em `CAT_EXPOSICAO`.\n")
    L.append(md_tabela(df["CAT_EXPOSICAO_GRUPO"].value_counts().to_frame("Registros"),
                       "Grupo", total=False) + "\n")

    L.append("## Conferência — casos por município e ano de NOTIFICAÇÃO\n")
    L.append(md_tabela(mun_ano, "Município") + "\n")
    L.append("## Conferência — casos por município e ano de DIAGNÓSTICO\n")
    L.append("Inclui casos diagnosticados antes de 2016 e notificados a partir de 2016.\n")
    L.append(md_tabela(mun_ano_diag, "Município") + "\n")
    L.append("## Conferência — notificações por mês e ano (13 municípios)\n")
    L.append(md_tabela(mensal, "Mês") + "\n")
    L.append("## Cobertura temporal\n")
    L.append(f"- Anos de notificação presentes: {', '.join(map(str, anos_presentes))}.")
    L.append(f"- **2025 existe na base? {'Sim' if tem_2025 else 'Não'}.**")
    L.append(f"- Última data de notificação na região: {ult:%d/%m/%Y}.")
    L.append("- Meses com ao menos uma notificação, por ano: "
             + ", ".join(f"{a}: {m}" for a, m in meses_por_ano.items()) + ".")
    L.append("- Mês com zero notificações num município pequeno pode ser real; o que indica ano "
             "incompleto é o corte geral dos dados (na base Brasil, a última notificação é de 30/06/2024).\n")

    SAIDA_MD.write_text("\n".join(L), encoding="utf-8")
    print(f"Base: {SAIDA_BASE} ({len(df)} registros, {out.shape[1]} colunas)")
    print(f"Relatório: {SAIDA_MD}")


if __name__ == "__main__":
    main()
