"""Etapa 4 - Séries temporais de notificações de HIV no Baixo Amazonas.

Entrada : dados/hiv_baixo_amazonas.csv (gerado por 02_limpeza.py)
          HIV16_25.csv (original, só NU_ANO, para comparação com o Brasil)
Saídas  : resultados/series_*.csv, resultados/series_*.png, resultados/series_relatorio.md

Referência temporal: ANO DE NOTIFICAÇÃO (ANO_NOTIF). Sem taxas por habitante
(não há população na pasta): tudo em números absolutos e proporções.

Uso: python scripts/03_series.py
"""
import unicodedata
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
BASE = RAIZ / "dados" / "hiv_baixo_amazonas.csv"
ORIGINAL = RAIZ / "HIV16_25.csv"
RES = RAIZ / "resultados"

ANO_PARCIAL = 2024          # só jan-jun (última notificação em 28/06/2024)
LIMIAR_POUCOS = 30          # < 30 casos em 2016-2024 = "poucos casos"
LIMIAR_VAR = 10             # variação % só é exibida se o ano anterior tiver >= 10 casos

# Paleta (dataviz skill, modo claro)
AZUL, LARANJA, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
TXT1, TXT2, GRADE, SUP = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": GRADE,
    "axes.labelcolor": TXT2, "xtick.color": TXT2, "ytick.color": TXT2,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": SUP, "axes.facecolor": SUP, "savefig.facecolor": SUP,
})


def fmt(n):
    return f"{int(n):,}".replace(",", ".")


def pctf(x, casas=1, sinal=False):
    if pd.isna(x):
        return "—"
    s = f"{x:+.{casas}f}%" if sinal else f"{x:.{casas}f}%"
    return s.replace(".", ",")


def sem_acento(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def var_pct(serie, minimo=0):
    """Variação % em relação ao ano anterior; NaN se o anterior < minimo ou se
    o ano atual for parcial (não comparável)."""
    ant = serie.shift(1)
    v = (serie - ant) / ant * 100
    v[(ant < minimo) | (ant == 0)] = np.nan
    if ANO_PARCIAL in v.index:
        v[ANO_PARCIAL] = np.nan
    return v


def md(df, primeira):
    cols = [str(c) for c in df.columns]
    L = [f"| {primeira} | " + " | ".join(cols) + " |", "|---|" + "---:|" * len(cols)]
    for i, r in df.iterrows():
        b = "**" if str(i).startswith("Total") or str(i).startswith("13 mun") else ""
        L.append(f"| {b}{i}{b} | " + " | ".join(f"{b}{v}{b}" for v in r) + " |")
    return "\n".join(L)


def faixa_pandemia(ax):
    ax.axvspan(2019.5, 2021.5, color="#efeee9", zorder=0)
    ax.text(2020.5, ax.get_ylim()[1] * 0.98, "2020–2021\npandemia", ha="center",
            va="top", fontsize=8, color=TXT2)


def main():
    df = pd.read_csv(BASE, dtype=str, encoding="utf-8-sig")
    df["ANO_NOTIF"] = df["ANO_NOTIF"].astype(int)
    df["MES_NOTIF"] = df["MES_NOTIF"].astype(int)
    anos = list(range(2016, 2025))
    municipios = sorted(df["MUNICIPIO"].unique(), key=sem_acento)

    # ---------------- tabelas ----------------
    mun_ano = pd.crosstab(df["MUNICIPIO"], df["ANO_NOTIF"]).reindex(
        index=municipios, columns=anos, fill_value=0)
    total = mun_ano.sum()
    santarem = mun_ano.loc["Santarém"]
    demais = total - santarem

    # 1) total por ano + variação
    t1 = pd.DataFrame({"casos": total, "var_pct": var_pct(total)})
    t1["santarem"] = santarem
    t1["var_santarem_pct"] = var_pct(santarem)
    t1["demais_12"] = demais
    t1["var_demais_pct"] = var_pct(demais)
    t1.index.name = "ano"
    t1.round(1).to_csv(RES / "series_total_ano.csv", encoding="utf-8-sig")

    # 2) município × ano (absoluto) + total do período
    t2 = mun_ano.copy()
    t2["total_2016_2024"] = t2.sum(axis=1)
    t2["anos_com_zero"] = (mun_ano == 0).sum(axis=1)
    t2["poucos_casos"] = t2["total_2016_2024"] < LIMIAR_POUCOS
    t2.to_csv(RES / "series_municipio_ano.csv", encoding="utf-8-sig")

    # 3) participação % de cada município no total de cada ano
    part = mun_ano / total * 100
    part["2016_2024"] = mun_ano.sum(axis=1) / total.sum() * 100
    part.round(1).to_csv(RES / "series_participacao.csv", encoding="utf-8-sig")

    # 4) variação % por município (só quando ano anterior >= LIMIAR_VAR)
    var_mun = mun_ano.apply(lambda r: var_pct(r, LIMIAR_VAR), axis=1)
    var_mun.round(1).to_csv(RES / "series_variacao_municipio.csv", encoding="utf-8-sig")

    # 5) 1º semestre: comparação justa de 2024
    sem1 = df[df["MES_NOTIF"] <= 6]
    s1_tot = sem1.groupby("ANO_NOTIF").size().reindex(anos, fill_value=0)
    s1_stm = sem1[sem1["MUNICIPIO"] == "Santarém"].groupby("ANO_NOTIF").size().reindex(anos, fill_value=0)
    t5 = pd.DataFrame({"casos_jan_jun": s1_tot,
                       "var_pct": (s1_tot / s1_tot.shift(1) - 1) * 100,
                       "santarem_jan_jun": s1_stm,
                       "demais_jan_jun": s1_tot - s1_stm})
    t5.index.name = "ano"
    t5.round(1).to_csv(RES / "series_1o_semestre.csv", encoding="utf-8-sig")

    # 6) Brasil (contexto da pandemia), índice 2019 = 100
    br = pd.read_csv(ORIGINAL, dtype=str, usecols=["NU_ANO"])["NU_ANO"].astype(int)
    br = br.value_counts().reindex(anos)
    idx = pd.DataFrame({"brasil": br, "baixo_amazonas": total,
                        "santarem": santarem, "demais_12": demais})
    idx_100 = idx.div(idx.loc[2019]) * 100
    pd.concat([idx.add_suffix("_casos"), idx_100.round(1).add_suffix("_indice2019")], axis=1) \
        .rename_axis("ano").to_csv(RES / "series_indice_2019.csv", encoding="utf-8-sig")

    # ---------------- gráficos ----------------
    # G1: total da região por ano
    fig, ax = plt.subplots(figsize=(8, 4.2))
    cores = [AZUL] * (len(anos) - 1) + ["none"]
    bars = ax.bar(anos, total.values, color=cores, edgecolor=AZUL, linewidth=1.5, width=0.7)
    bars[-1].set_hatch("///")
    for x, v in zip(anos, total.values):
        ax.text(x, v + 4, fmt(v), ha="center", va="bottom", fontsize=9, color=TXT1)
    ax.set_ylim(0, total.max() * 1.18)
    faixa_pandemia(ax)
    ax.set_xticks(anos, [str(a) if a != ANO_PARCIAL else f"{a}*" for a in anos])
    ax.set_ylabel("Notificações")
    ax.yaxis.grid(True, color=GRADE, linewidth=0.8); ax.set_axisbelow(True)
    ax.set_title("Notificações de HIV por ano — 13 municípios do Baixo Amazonas",
                 loc="left", color=TXT1, fontsize=11)
    fig.text(0.01, 0.01, "*2024 parcial: só janeiro a junho. Notificação não é incidência. "
             "Fonte: SINAN (HIV16_25.csv), por município de residência.", fontsize=7.5, color=TXT2)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(RES / "series_g1_total_ano.png", dpi=150); plt.close(fig)

    # G2: Santarém x demais 12 municípios (linhas)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for serie, cor, nome in [(santarem, AZUL, "Santarém"), (demais, LARANJA, "Demais 12 municípios")]:
        ax.plot(anos[:-1], serie.values[:-1], color=cor, linewidth=2, marker="o", markersize=5)
        ax.plot(anos[-2:], serie.values[-2:], color=cor, linewidth=2, linestyle=":")
        ax.plot(anos[-1], serie.values[-1], marker="o", markersize=6, markerfacecolor=SUP,
                markeredgecolor=cor, markeredgewidth=1.5)
    ax.set_xlim(2015.5, 2024.5)
    ax.set_ylim(0, santarem.max() * 1.15)
    faixa_pandemia(ax)
    ax.set_xticks(anos, [str(a) if a != ANO_PARCIAL else f"{a}*" for a in anos])
    ax.set_ylabel("Notificações")
    ax.yaxis.grid(True, color=GRADE, linewidth=0.8); ax.set_axisbelow(True)
    ax.legend(handles=[plt.Line2D([], [], color=AZUL, lw=2, marker="o", label="Santarém"),
                       plt.Line2D([], [], color=LARANJA, lw=2, marker="o", label="Demais 12 municípios")],
              frameon=False, loc="upper left", fontsize=8.5)
    ax.set_title("Santarém × demais municípios — notificações por ano", loc="left", color=TXT1, fontsize=11)
    fig.text(0.01, 0.01, "*2024 parcial (jan–jun), em pontilhado. Fonte: SINAN, por município de residência.",
             fontsize=7.5, color=TXT2)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(RES / "series_g2_santarem_demais.png", dpi=150); plt.close(fig)

    # G3: total do período por município (barras horizontais)
    tot_mun = mun_ano.sum(axis=1).sort_values()
    fig, ax = plt.subplots(figsize=(8, 5))
    cores = [AZUL if v >= LIMIAR_POUCOS else "#9fc3ee" for v in tot_mun.values]
    ax.barh(tot_mun.index, tot_mun.values, color=cores, height=0.7)
    for y, v in enumerate(tot_mun.values):
        rot = fmt(v) + ("  (poucos casos)" if v < LIMIAR_POUCOS else "")
        ax.text(v + 8, y, rot, va="center", fontsize=8.5, color=TXT1)
    ax.set_xlim(0, tot_mun.max() * 1.2)
    ax.xaxis.grid(True, color=GRADE, linewidth=0.8); ax.set_axisbelow(True)
    ax.set_xlabel("Notificações 2016–2024*")
    ax.set_title("Total de notificações por município de residência, 2016–2024*",
                 loc="left", color=TXT1, fontsize=11)
    fig.text(0.01, 0.01, f"*2024 só jan–jun. Barras claras: menos de {LIMIAR_POUCOS} casos no período. "
             "Números absolutos dependem do tamanho da população.", fontsize=7.5, color=TXT2)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(RES / "series_g3_municipios_total.png", dpi=150); plt.close(fig)

    # G4: mapa de calor município × ano (sequencial, um tom)
    from matplotlib.colors import LinearSegmentedColormap, PowerNorm
    cmap = LinearSegmentedColormap.from_list("azul", ["#f3f7fd", "#9fc3ee", "#2a78d6", "#0d3a73"])
    ordem = tot_mun.index[::-1]
    m = mun_ano.loc[ordem]
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    ax.imshow(m.values, cmap=cmap, norm=PowerNorm(0.45, vmin=0, vmax=m.values.max()), aspect="auto")
    for i in range(m.shape[0]):
        for j in range(m.shape[1]):
            v = m.values[i, j]
            ax.text(j, i, str(v), ha="center", va="center", fontsize=8,
                    color="white" if v >= 40 else TXT1)
    ax.set_xticks(range(len(anos)), [str(a) if a != ANO_PARCIAL else f"{a}*" for a in anos])
    ax.set_yticks(range(len(ordem)), ordem)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)
    ax.set_title("Notificações por município e ano", loc="left", color=TXT1, fontsize=11)
    fig.text(0.01, 0.01, "*2024 parcial (jan–jun). Cor em escala comprimida para mostrar diferenças "
             "nos municípios pequenos; leia os números.", fontsize=7.5, color=TXT2)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(RES / "series_g4_mapa_calor.png", dpi=150); plt.close(fig)

    # G5: índice 2019 = 100 (Brasil × região)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for col, cor, nome in [("brasil", TXT2, "Brasil"), ("santarem", AZUL, "Santarém"),
                           ("demais_12", LARANJA, "Demais 12 municípios")]:
        y = idx_100[col].values
        ax.plot(anos[:-1], y[:-1], color=cor, lw=2, marker="o", markersize=4)
        ax.text(2023.15, y[-2], nome, va="center", fontsize=8.5, color=TXT1)
    ax.axhline(100, color=GRADE, lw=1)
    ax.set_xlim(2015.6, 2024.6)
    ax.set_xticks(anos[:-1])
    faixa_pandemia(ax)
    ax.set_ylabel("Índice (2019 = 100)")
    ax.yaxis.grid(True, color=GRADE, linewidth=0.8); ax.set_axisbelow(True)
    ax.legend(handles=[plt.Line2D([], [], color=c, lw=2, label=n) for c, n in
                       [(TXT2, "Brasil"), (AZUL, "Santarém"), (LARANJA, "Demais 12 municípios")]],
              frameon=False, loc="upper left", fontsize=8.5)
    ax.set_title("Notificações relativas a 2019 (2019 = 100), 2016–2023", loc="left", color=TXT1, fontsize=11)
    fig.text(0.01, 0.01, "2024 omitido (parcial). Índice compara tendências, não volumes. Fonte: SINAN.",
             fontsize=7.5, color=TXT2)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(RES / "series_g5_indice_2019.png", dpi=150); plt.close(fig)

    # ---------------- relatório ----------------
    L = ["# Séries de notificações de HIV — Baixo Amazonas, 2016–2024\n",
         "Gerado por `scripts/03_series.py` a partir de `dados/hiv_baixo_amazonas.csv` "
         "(1.596 notificações, município de residência, **ano de notificação**). "
         "Todos os valores são calculados; sem taxas por habitante (não há população na pasta).\n",
         "> **Leia com cuidado:** notificação não é incidência. O número depende também de testagem, "
         "acesso a serviços e digitação no SINAN. **2024 tem só janeiro a junho** e não é comparável "
         "com os anos fechados.\n"]

    L.append("## 1. Região: casos por ano e variação anual\n")
    t = pd.DataFrame({
        "Casos": [fmt(v) for v in total],
        "Var. %": [pctf(v, sinal=True) for v in t1["var_pct"]],
        "Santarém": [fmt(v) for v in santarem],
        "Var. % Stm": [pctf(v, sinal=True) for v in t1["var_santarem_pct"]],
        "Demais 12": [fmt(v) for v in demais],
        "Var. % demais": [pctf(v, sinal=True) for v in t1["var_demais_pct"]],
    }, index=[str(a) if a != ANO_PARCIAL else f"{a}*" for a in anos])
    L.append(md(t, "Ano"))
    L.append(f"\n*2024 parcial: variação não calculada. Total 2016–2024: {fmt(total.sum())}.\n")
    L.append("![Total por ano](series_g1_total_ano.png)\n")
    L.append("![Santarém e demais](series_g2_santarem_demais.png)\n")

    L.append("### Comparação justa para 2024: só o 1º semestre (jan–jun)\n")
    t = pd.DataFrame({"Casos jan–jun": [fmt(v) for v in s1_tot],
                      "Var. %": [pctf(v, sinal=True) for v in t5["var_pct"]],
                      "Santarém": [fmt(v) for v in s1_stm],
                      "Demais 12": [fmt(v) for v in s1_tot - s1_stm]}, index=[str(a) for a in anos])
    L.append(md(t, "Ano") + "\n")
    L.append("Atenção: a digitação no SINAN é irregular de mês a mês (ver `decisoes_limpeza.md`) e 2024 "
             "pode ainda receber notificações atrasadas; a comparação por semestre também é frágil.\n")

    L.append("## 2. Municípios em números absolutos\n")
    t = mun_ano.copy()
    t.columns = [str(a) if a != ANO_PARCIAL else f"{a}*" for a in anos]
    t["Total"] = mun_ano.sum(axis=1)
    t = t.map(fmt)
    t["% do total"] = [pctf(v) for v in part["2016_2024"]]
    t["Anos com 0"] = (mun_ano == 0).sum(axis=1)
    t.loc["Total"] = [fmt(v) for v in total.values] + [fmt(total.sum()), "100,0%", "—"]
    L.append(md(t, "Município") + "\n")
    L.append("![Total por município](series_g3_municipios_total.png)\n")
    L.append("![Mapa de calor](series_g4_mapa_calor.png)\n")
    L.append("![Índice 2019 = 100](series_g5_indice_2019.png)\n")

    L.append("## 3. Participação de cada município no total do ano (%)\n")
    t = part[anos].copy().map(lambda v: pctf(v))
    t.columns = [str(a) if a != ANO_PARCIAL else f"{a}*" for a in anos]
    t["2016–2024"] = [pctf(v) for v in part["2016_2024"]]
    L.append(md(t, "Município") + "\n")

    L.append("## 4. Variação % anual por município\n")
    L.append(f"Mostrada só quando o ano anterior tem pelo menos {LIMIAR_VAR} casos; abaixo disso, "
             "uma diferença de 1 ou 2 casos vira variação de 50% a 200% e não informa nada. "
             "2024 não calculado (parcial).\n")
    t = var_mun[anos[1:-1]].copy()
    t = t[t.notna().any(axis=1)].map(lambda v: pctf(v, sinal=True))
    t.columns = [str(a) for a in anos[1:-1]]
    L.append(md(t, "Município") + "\n")

    # pontos de atenção (texto montado com números calculados)
    poucos = t2[t2["poucos_casos"]].sort_values("total_2016_2024")
    L.append("## 5. Pontos de atenção\n")
    L.append(f"**Municípios com poucos casos** (menos de {LIMIAR_POUCOS} em 2016–2024): "
             + "; ".join(f"{m} ({fmt(r.total_2016_2024)}, {r.anos_com_zero} ano(s) com zero)"
                         for m, r in poucos.iterrows())
             + ". Nesses municípios, variações e participações oscilam com 1 ou 2 casos e "
             "não devem ser interpretadas como tendência. Zero casos num ano não significa ausência de HIV.\n")
    L.append(f"**Concentração em Santarém:** {pctf(part.loc['Santarém', '2016_2024'])} das notificações do "
             f"período (de {pctf(part.loc['Santarém', 2018])} em 2018 a {pctf(part.loc['Santarém', 2021])} em 2021). "
             "Isso é esperado pelo tamanho da população e por Santarém concentrar serviços de testagem, "
             "mas sem população não dá para dizer se o risco é maior lá.\n")
    L.append(f"**2024 parcial:** {fmt(total[2024])} notificações em seis meses. No 1º semestre, "
             f"2023 teve {fmt(s1_tot[2023])} e 2024 teve {fmt(s1_tot[2024])} "
             f"({pctf(t5.loc[2024, 'var_pct'], sinal=True)}). Não dá para concluir se é queda real, "
             "atraso de digitação ou oscilação.\n")
    L.append("**2020–2021 (período da pandemia de covid-19):** "
             f"no Brasil, as notificações foram de {fmt(br[2019])} em 2019 para {fmt(br[2020])} em 2020 "
             f"({pctf(idx_100.loc[2020, 'brasil'] - 100, sinal=True)}) e só superaram o nível de 2019 em "
             f"{int(idx_100.index[(idx_100.index > 2020) & (idx_100['brasil'] > 100)].min())}. "
             f"No Baixo Amazonas o movimento foi diferente: {fmt(total[2019])} em 2019, {fmt(total[2020])} "
             f"em 2020 ({pctf(t1.loc[2020, 'var_pct'], sinal=True)}) e {fmt(total[2021])} em 2021 "
             f"({pctf(t1.loc[2021, 'var_pct'], sinal=True)}). O crescimento vem principalmente de Santarém "
             f"({fmt(santarem[2019])} → {fmt(santarem[2020])} → {fmt(santarem[2021])}); os demais 12 municípios "
             f"somados ficaram estáveis ({fmt(demais[2019])} → {fmt(demais[2020])} → {fmt(demais[2021])}). "
             "Os dados não permitem dizer a causa. Hipóteses a verificar com a gestão: ampliação de testagem "
             "rápida ou de serviços em Santarém, busca ativa, mudança na rotina de digitação (a série mensal "
             "mostra lotes) ou notificação de casos antigos. Também não dá para afirmar que a pandemia não "
             "afetou a região: o diagnóstico pode ter sido represado e aparecido depois.\n")
    L.append("**Crescimento 2016–2022:** a região passou de "
             f"{fmt(total[2016])} (2016) para {fmt(total[2022])} (2022), com queda em 2023 ({fmt(total[2023])}). "
             "Aumento de notificação pode refletir mais testagem e melhor vigilância, não necessariamente "
             "mais infecções.\n")

    (RES / "series_relatorio.md").write_text("\n".join(L), encoding="utf-8")
    print("OK")


if __name__ == "__main__":
    main()
