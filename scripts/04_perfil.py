"""Etapa 5 - Perfil dos casos de HIV no Baixo Amazonas e mudança 2016-2023.

Entrada : dados/hiv_baixo_amazonas.csv
Saídas  : resultados/achados_hiv.md
          resultados/perfil_<campo>_ano.csv (distribuição por ano, 2016-2024)

Recorte de análise: anos de notificação 2016-2023 (anos completos). 2024 (jan-jun)
aparece só nos CSVs por ano, nunca nas comparações.
Mudança: períodos 2016-2019 × 2020-2023 (quatro anos cada), com teste de
diferença de duas proporções (z, aproximação normal, 5%) para indicar quando a
diferença pode ser explicada pelo acaso.

Uso: python scripts/04_perfil.py
"""
from math import erf, sqrt
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
BASE = RAIZ / "dados" / "hiv_baixo_amazonas.csv"
RES = RAIZ / "resultados"
SAIDA = RES / "achados_hiv.md"

P1, P2 = (2016, 2019), (2020, 2023)
ROT_P1, ROT_P2 = "2016–2019", "2020–2023"

ORDENS = {
    "SEXO": ["Masculino", "Feminino", "Ignorado"],
    "FAIXA_ETARIA": ["<15", "15-19", "20-24", "25-29", "30-39", "40-49", "50-59", "60+", "Ignorada"],
    "RACA_COR": ["Parda", "Preta", "Branca", "Indígena", "Amarela", "Ignorado"],
    "ESCOLARIDADE_GRUPO": ["Até fundamental incompleto", "Fundamental completo / médio incompleto",
                           "Médio completo / superior incompleto", "Superior completo",
                           "Ignorado", "Não se aplica"],
    "CAT_EXPOSICAO_GRUPO": ["Heterossexual", "Homossexual", "Bissexual", "Drogas injetáveis",
                            "Vertical", "Outras", "Ignorado"],
    "EVOLUCAO_DESC": ["Vivo", "Óbito por aids", "Óbito por outras causas", "Ignorado"],
}
NOMES = {"SEXO": "Sexo", "FAIXA_ETARIA": "Faixa etária", "RACA_COR": "Raça/cor",
         "ESCOLARIDADE_GRUPO": "Escolaridade", "CAT_EXPOSICAO_GRUPO": "Categoria de exposição",
         "EVOLUCAO_DESC": "Evolução"}
IGNORADO = {"Ignorado", "Ignorada"}


def fmt(n):
    return f"{int(n):,}".replace(",", ".")


def pc(x, casas=1, sinal=False):
    if pd.isna(x):
        return "—"
    s = f"{x:+.{casas}f}" if sinal else f"{x:.{casas}f}"
    return s.replace(".", ",")


def p_valor(x1, n1, x2, n2):
    """Teste z de duas proporções (bicaudal)."""
    if n1 == 0 or n2 == 0:
        return np.nan
    p = (x1 + x2) / (n1 + n2)
    se = sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return np.nan
    z = (x1 / n1 - x2 / n2) / se
    return 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2))))


def grupo_escol(e):
    m = {"Analfabeto": 0, "1ª a 4ª série incompleta do EF": 0, "4ª série completa do EF": 0,
         "5ª a 8ª série incompleta do EF": 0, "Ensino fundamental completo": 1,
         "Ensino médio incompleto": 1, "Ensino médio completo": 2,
         "Educação superior incompleta": 2, "Educação superior completa": 3}
    g = ["Até fundamental incompleto", "Fundamental completo / médio incompleto",
         "Médio completo / superior incompleto", "Superior completo"]
    if e in m:
        return g[m[e]]
    return e  # Ignorado / Não se aplica


def compara(d, campo, base_mask=None):
    """Tabela período 1 × período 2 com %, diferença em p.p. e p-valor."""
    sub = d if base_mask is None else d[base_mask]
    ordem = ORDENS.get(campo, sorted(sub[campo].unique()))
    linhas = []
    s1 = sub[sub["PERIODO"] == ROT_P1][campo]
    s2 = sub[sub["PERIODO"] == ROT_P2][campo]
    st = sub[campo]
    n1, n2, nt = len(s1), len(s2), len(st)
    for cat in ordem:
        x1, x2, xt = int((s1 == cat).sum()), int((s2 == cat).sum()), int((st == cat).sum())
        if xt == 0:
            continue
        linhas.append({"cat": cat, "n_tot": xt, "p_tot": 100 * xt / nt,
                       "n1": x1, "p1": 100 * x1 / n1, "n2": x2, "p2": 100 * x2 / n2,
                       "dif": 100 * (x2 / n2 - x1 / n1), "pval": p_valor(x1, n1, x2, n2)})
    return pd.DataFrame(linhas), n1, n2, nt


def md_compara(t, n1, n2, nt):
    L = [f"| Categoria | 2016–2023 n | % | {ROT_P1} % (n={fmt(n1)}) | {ROT_P2} % (n={fmt(n2)}) | Diferença (p.p.) | Diferença além do acaso? |",
         "|---|---:|---:|---:|---:|---:|---|"]
    for _, r in t.iterrows():
        sig = "—" if pd.isna(r.pval) else ("sim (p<0,05)" if r.pval < 0.05 else "não")
        L.append(f"| {r['cat']} | {fmt(r.n_tot)} | {pc(r.p_tot)}% | {pc(r.p1)}% | {pc(r.p2)}% | "
                 f"{pc(r.dif, sinal=True)} | {sig} |")
    L.append(f"| **Total** | **{fmt(nt)}** | 100% | 100% | 100% | | |")
    return "\n".join(L)


def main():
    df = pd.read_csv(BASE, dtype=str, encoding="utf-8-sig")
    df["ANO_NOTIF"] = df["ANO_NOTIF"].astype(int)
    df["IDADE_ANOS"] = pd.to_numeric(df["IDADE_ANOS"], errors="coerce")
    df["ESCOLARIDADE_GRUPO"] = df["ESCOLARIDADE"].map(grupo_escol)

    # CSVs por ano (2016-2024, % na linha do ano) para todos os campos
    for campo in list(ORDENS) + ["GESTANTE"]:
        ct = pd.crosstab(df["ANO_NOTIF"], df[campo])
        ordem = [c for c in ORDENS.get(campo, ct.columns) if c in ct.columns]
        ct = ct[ordem]
        pct = ct.div(ct.sum(axis=1), axis=0) * 100
        pd.concat([ct.add_prefix("n_"), pct.round(1).add_prefix("pct_")], axis=1) \
            .to_csv(RES / f"perfil_{campo.lower()}_ano.csv", encoding="utf-8-sig")

    d = df[df["ANO_NOTIF"].between(2016, 2023)].copy()
    d["PERIODO"] = np.where(d["ANO_NOTIF"] <= P1[1], ROT_P1, ROT_P2)
    N = len(d)
    R = {}  # números usados nos achados

    L = ["# Perfil dos casos de HIV e achados principais — Baixo Amazonas\n",
         "Gerado por `scripts/04_perfil.py` a partir de `dados/hiv_baixo_amazonas.csv`. "
         f"**Recorte: notificações de 2016 a 2023 (n = {fmt(N)})**, residentes nos 13 municípios. "
         "2024 ficou de fora das comparações por ter só janeiro a junho (está nos CSVs `perfil_*_ano.csv`).\n",
         "**Como ler a mudança:** comparamos dois períodos de quatro anos (2016–2019 × 2020–2023), porque "
         "ano a ano os números são pequenos. A coluna \"Diferença além do acaso?\" usa um teste de duas "
         "proporções (5%): \"não\" quer dizer que a diferença pode ser só oscilação. Um \"sim\" mostra "
         "diferença nas **notificações**, não prova mudança na epidemia.\n",
         "> Notificação não é incidência. Casos dependem de testagem, acesso e qualidade do preenchimento.\n"]

    # ---------- % ignorados ----------
    L.append("## 1. Percentual de ignorados por campo\n")
    L.append("Ignorado = código 9/99/90, campo vazio ou idade não informada.\n")
    L.append(f"| Campo | 2016–2023 | {ROT_P1} | {ROT_P2} |")
    L.append("|---|---:|---:|---:|")
    ign = {}
    for campo in ["SEXO", "FAIXA_ETARIA", "RACA_COR", "ESCOLARIDADE_GRUPO",
                  "CAT_EXPOSICAO_GRUPO", "EVOLUCAO_DESC"]:
        is_ign = d[campo].isin(IGNORADO)
        v = [100 * is_ign.mean(),
             100 * is_ign[d["PERIODO"] == ROT_P1].mean(),
             100 * is_ign[d["PERIODO"] == ROT_P2].mean()]
        ign[campo] = v
        L.append(f"| {NOMES[campo]} | {pc(v[0])}% ({fmt(is_ign.sum())}) | {pc(v[1])}% | {pc(v[2])}% |")
    fem = d["SEXO"] == "Feminino"
    g_ign = d.loc[fem, "GESTANTE"].isin(["Ignorado"])
    L.append(f"| Gestante (só mulheres) | {pc(100 * g_ign.mean())}% ({fmt(g_ign.sum())}) | "
             f"{pc(100 * g_ign[d.loc[fem, 'PERIODO'] == ROT_P1].mean())}% | "
             f"{pc(100 * g_ign[d.loc[fem, 'PERIODO'] == ROT_P2].mean())}% |")
    obito = d["EVOLUCAO_DESC"].str.startswith("Óbito")
    sem_data = obito & d["DT_OBITO"].isna()
    L.append("")
    L.append(f"Observação: escolaridade também tem \"Não se aplica\" = "
             f"{fmt((d['ESCOLARIDADE_GRUPO'] == 'Não se aplica').sum())}. Em evolução, o campo está "
             f"preenchido, mas é atualizado raramente; dos {fmt(obito.sum())} óbitos, "
             f"{fmt(sem_data.sum())} estão sem data de óbito.\n")
    R["ign"] = ign

    # ---------- perfis ----------
    sec = 2
    tabelas = {}
    for campo in ORDENS:
        t, n1, n2, nt = compara(d, campo)
        tabelas[campo] = t
        L.append(f"## {sec}. {NOMES[campo]}\n")
        L.append(md_compara(t, n1, n2, nt) + "\n")
        if campo == "SEXO":
            ano = pd.crosstab(d["ANO_NOTIF"], d["SEXO"])
            razao = ano["Masculino"] / ano["Feminino"]
            R["razao"] = razao
            L.append("Razão de sexo (homens por mulher), por ano: "
                     + ", ".join(f"{a}: {pc(v)}" for a, v in razao.items()) + ".\n")
        if campo == "FAIXA_ETARIA":
            med = d.groupby("PERIODO")["IDADE_ANOS"].median()
            med_t = d["IDADE_ANOS"].median()
            R["med"] = (med_t, med[ROT_P1], med[ROT_P2])
            jov = d["IDADE_ANOS"].between(15, 29)
            R["jov"] = (jov.sum(), 100 * jov.sum() / d["IDADE_ANOS"].notna().sum())
            L.append(f"Mediana de idade: {pc(med_t, 0)} anos em 2016–2023 "
                     f"({pc(med[ROT_P1], 0)} em {ROT_P1}; {pc(med[ROT_P2], 0)} em {ROT_P2}). "
                     f"Pessoas de 15 a 29 anos: {fmt(jov.sum())} ({pc(R['jov'][1])}% dos casos com idade "
                     "informada).\n")
            # sexo x faixa
            ct = pd.crosstab(d["FAIXA_ETARIA"], d["SEXO"])
            ct = ct.reindex([f for f in ORDENS["FAIXA_ETARIA"] if f in ct.index])
            L.append("Faixa etária por sexo (2016–2023, n):\n")
            L.append("| Faixa | Masculino | Feminino |")
            L.append("|---|---:|---:|")
            for f, r in ct.iterrows():
                L.append(f"| {f} | {fmt(r.get('Masculino', 0))} | {fmt(r.get('Feminino', 0))} |")
            L.append("")
        if campo == "CAT_EXPOSICAO_GRUPO":
            m = d["SEXO"] == "Masculino"
            t_m, a, b, c = compara(d, campo, m)
            tabelas["EXP_MASC"] = t_m
            L.append(f"Só homens (n={fmt(c)}):\n")
            L.append(md_compara(t_m, a, b, c) + "\n")
            t_f, a, b, c = compara(d, campo, ~m)
            L.append(f"Só mulheres (n={fmt(c)}):\n")
            L.append(md_compara(t_f, a, b, c) + "\n")
        sec += 1
        if campo == "CAT_EXPOSICAO_GRUPO":
            # Gestantes logo depois da exposição
            L.append(f"## {sec}. Gestantes\n")
            gest = fem & d["GESTANTE"].isin(["1º trimestre", "2º trimestre", "3º trimestre",
                                              "Idade gestacional ignorada"])
            mulheres_ano = d[fem].groupby("ANO_NOTIF").size()
            gest_ano = d[gest].groupby("ANO_NOTIF").size().reindex(mulheres_ano.index, fill_value=0)
            g1 = gest[d["PERIODO"] == ROT_P1].sum(); f1 = fem[d["PERIODO"] == ROT_P1].sum()
            g2 = gest[d["PERIODO"] == ROT_P2].sum(); f2 = fem[d["PERIODO"] == ROT_P2].sum()
            pv = p_valor(g1, f1, g2, f2)
            R["gest"] = (gest.sum(), fem.sum(), g1, f1, g2, f2, pv)
            L.append(f"- Mulheres notificadas que estavam gestantes: **{fmt(gest.sum())} de {fmt(fem.sum())} "
                     f"({pc(100 * gest.sum() / fem.sum())}%)** em 2016–2023.")
            L.append(f"- {ROT_P1}: {fmt(g1)} de {fmt(f1)} ({pc(100 * g1 / f1)}%); "
                     f"{ROT_P2}: {fmt(g2)} de {fmt(f2)} ({pc(100 * g2 / f2)}%). "
                     f"Diferença além do acaso? {'sim' if pv < 0.05 else 'não'} (p = {pc(pv, 3)}).")
            tri = d[gest]["GESTANTE"].value_counts()
            L.append("- Momento da gestação: " + ", ".join(f"{k}: {fmt(v)}" for k, v in tri.items()) + ".")
            L.append("- Por ano (gestantes / mulheres): " + ", ".join(
                f"{a}: {gest_ano[a]}/{mulheres_ano[a]}" for a in mulheres_ano.index) + ".")
            L.append("- Limitação: gestantes com HIV têm ficha própria no SINAN (HIV em gestante); "
                     "esta base pode não captar todas.\n")
            sec += 1

    # Evolução: detalhe
    ev = tabelas["EVOLUCAO_DESC"].set_index("cat")
    R["ev"] = ev

    # guardar para achados
    R["tab"] = tabelas
    R["N"] = N
    R["razao_tot"] = (d["SEXO"] == "Masculino").sum() / (d["SEXO"] == "Feminino").sum()
    stm = d["MUNICIPIO"] == "Santarém"
    R["d"] = d

    L.extend(achados(R))
    SAIDA.write_text("\n".join(L), encoding="utf-8")
    print("OK")


def linha(t, cat):
    return t.set_index("cat").loc[cat]


def achados(R):
    """Achados montados só com números calculados acima (nada digitado à mão)."""
    d, tab, N = R["d"], R["tab"], R["N"]
    p1 = d["PERIODO"] == ROT_P1
    p2 = ~p1
    L = ["## 9. Cinco achados principais\n",
         f"Todos sobre notificações de residentes nos 13 municípios, 2016–2023 (n = {fmt(N)}).\n"]

    # 1 - sexo
    s = linha(tab["SEXO"], "Feminino")
    rz = R["razao"]
    L += ["### Achado 1 — Os casos notificados são majoritariamente de homens, e a participação masculina aumentou\n",
          f"- **Número:** homens são {pc(linha(tab['SEXO'], 'Masculino').p_tot)}% dos casos "
          f"({fmt(linha(tab['SEXO'], 'Masculino').n_tot)} de {fmt(N)}). A participação das mulheres caiu de "
          f"{pc(s.p1)}% ({ROT_P1}) para {pc(s.p2)}% ({ROT_P2}), diferença além do acaso. "
          f"A razão homem/mulher foi de {pc(rz[2016])} em 2016 para {pc(rz[2023])} em 2023 "
          f"(máximo de {pc(rz.max())} em {rz.idxmax()}).",
          f"- **Período:** 2016–2023.",
          "- **Limitação:** reflete quem foi testado e notificado. Mulheres são testadas de rotina no pré-natal e "
          "homens buscam menos os serviços; a mudança pode ser de testagem, não de transmissão.",
          "- **Pergunta de vigilância:** a oferta de testagem para homens mudou a partir de 2019 nos serviços "
          "que mais notificam, e as mulheres fora do pré-natal estão sendo testadas?\n"]

    # 2 - exposição entre homens
    m = d["SEXO"] == "Masculino"
    t_m = tab["EXP_MASC"]
    ho, bi = linha(t_m, "Homossexual"), linha(t_m, "Bissexual")
    hsh1 = 100 * (d[m & p1]["CAT_EXPOSICAO_GRUPO"].isin(["Homossexual", "Bissexual"])).mean()
    hsh2 = 100 * (d[m & p2]["CAT_EXPOSICAO_GRUPO"].isin(["Homossexual", "Bissexual"])).mean()
    ig = linha(t_m, "Ignorado")
    L += ["### Achado 2 — Entre homens, cresceu a exposição homossexual e caiu a bissexual\n",
          f"- **Número:** entre homens, a categoria homossexual passou de {pc(ho.p1)}% para {pc(ho.p2)}% e a "
          f"bissexual de {pc(bi.p1)}% para {pc(bi.p2)}% (as duas diferenças além do acaso). Somadas "
          f"(homens que fazem sexo com homens), foram de {pc(hsh1)}% para {pc(hsh2)}%. "
          f"Na região toda, a heterossexual segue como a maior categoria ({pc(linha(tab['CAT_EXPOSICAO_GRUPO'], 'Heterossexual').p_tot)}%).",
          f"- **Período:** {ROT_P1} × {ROT_P2}.",
          f"- **Limitação:** a categoria é informada pelo paciente sobre um tema sensível e calculada pelo "
          f"sistema; {pc(ig.p_tot)}% dos homens têm exposição ignorada. A troca entre \"bissexual\" e "
          "\"homossexual\" pode ser mudança na forma de perguntar ou registrar, não de comportamento.",
          "- **Pergunta de vigilância:** houve mudança no preenchimento da ficha (quem pergunta e como) ou "
          "ampliação de ações de testagem voltadas a homens que fazem sexo com homens na região?\n"]

    # 3 - jovens
    med_t, med1, med2 = R["med"]
    f1519 = linha(tab["FAIXA_ETARIA"], "15-19")
    f2024 = linha(tab["FAIXA_ETARIA"], "20-24")
    L += ["### Achado 3 — Metade dos casos é de jovens de 15 a 29 anos\n",
          f"- **Número:** {fmt(R['jov'][0])} casos ({pc(R['jov'][1])}% dos que têm idade informada) têm "
          f"15 a 29 anos; a mediana de idade é {pc(med_t, 0)} anos. A faixa de 20 a 24 anos sozinha tem "
          f"{pc(f2024.p_tot)}%. A faixa de 15 a 19 anos caiu de {pc(f1519.p1)}% para {pc(f1519.p2)}% "
          f"({fmt(f1519.n1)} e {fmt(f1519.n2)} casos), diferença além do acaso.",
          "- **Período:** 2016–2023.",
          "- **Limitação:** a idade pode ser a aparente (sem data de nascimento) e a data é a da notificação, "
          "não a da infecção, que pode ter ocorrido anos antes. A ficha é de HIV adulto.",
          "- **Pergunta de vigilância:** onde esses jovens estão sendo diagnosticados, e a queda entre 15 e 19 "
          "anos é de casos ou de testagem de adolescentes?\n"]

    # 4 - gestantes
    gt, ft, g1, f1, g2, f2, pv = R["gest"]
    fem = d["SEXO"] == "Feminino"
    gest_mask = fem & d["GESTANTE"].isin(["1º trimestre", "2º trimestre", "3º trimestre",
                                          "Idade gestacional ignorada"])
    tri23 = d[gest_mask]["GESTANTE"].isin(["2º trimestre", "3º trimestre"]).sum()
    tri1 = (d[gest_mask]["GESTANTE"] == "1º trimestre").sum()
    vert = linha(tab["CAT_EXPOSICAO_GRUPO"], "Vertical")
    L += ["### Achado 4 — Quase uma em cada quatro mulheres notificadas estava gestante, a maioria no 2º ou 3º trimestre\n",
          f"- **Número:** {fmt(gt)} de {fmt(ft)} mulheres ({pc(100 * gt / ft)}%) estavam gestantes na notificação; "
          f"{fmt(tri23)} delas ({pc(100 * tri23 / gt)}%) no 2º ou 3º trimestre e {fmt(tri1)} no 1º. "
          f"A proporção foi de {pc(100 * g1 / f1)}% ({ROT_P1}) para {pc(100 * g2 / f2)}% ({ROT_P2}), "
          f"diferença que pode ser acaso (p = {pc(pv, 2)}). Há ainda {fmt(vert.n_tot)} casos de transmissão "
          "vertical (mãe para filho) no período.",
          "- **Período:** 2016–2023.",
          "- **Limitação:** o trimestre é o da notificação, não o do diagnóstico; gestantes com HIV têm ficha "
          "própria no SINAN, que não está nesta base, então o número pode estar incompleto.",
          "- **Pergunta de vigilância:** as gestantes estão sendo testadas no 1º trimestre do pré-natal, como "
          "recomendado, e todas as gestantes com HIV foram também notificadas na ficha de gestante?\n"]

    # 5 - qualidade e desfecho
    esc_ig = R["ign"]["ESCOLARIDADE_GRUPO"]
    ev = R["ev"]
    obitos = int(ev.loc["Óbito por aids", "n_tot"] + ev.loc["Óbito por outras causas", "n_tot"])
    fi = linha(tab["ESCOLARIDADE_GRUPO"], "Até fundamental incompleto")
    L += ["### Achado 5 — O preenchimento melhorou, mas a evolução dos casos não é acompanhada\n",
          f"- **Número:** escolaridade ignorada caiu de {pc(esc_ig[1])}% para {pc(esc_ig[2])}%. "
          f"Ao mesmo tempo, \"até fundamental incompleto\" caiu de {pc(fi.p1)}% para {pc(fi.p2)}%, mudança "
          f"muito grande para quatro anos. Na evolução, {pc(ev.loc['Vivo', 'p_tot'])}% constam como vivos e "
          f"só {fmt(obitos)} óbitos foram registrados ({fmt(ev.loc['Óbito por aids', 'n_tot'])} por aids).",
          "- **Período:** 2016–2023.",
          "- **Limitação:** a evolução é registrada na notificação e raramente atualizada, então os óbitos "
          "não medem mortalidade. A mudança brusca na escolaridade pode ser de preenchimento e não do perfil "
          "das pessoas.",
          "- **Pergunta de vigilância:** os óbitos por aids de residentes estão sendo cruzados com o SIM "
          "(Sistema de Informações sobre Mortalidade), e o que mudou no registro da escolaridade a partir de 2020?\n"]

    L += ["## 10. O que estes dados não permitem dizer\n",
          "- Se o risco de HIV é maior num município ou grupo: não há população para calcular taxas.",
          "- Se a epidemia cresceu ou diminuiu: só há notificações, que dependem de testagem.",
          "- Mortalidade por aids: a evolução não é acompanhada nesta ficha.",
          "- Diferenças por município no perfil: com poucos casos na maioria dos municípios, os percentuais "
          "seriam instáveis (não foram calculados aqui).\n"]
    return L


if __name__ == "__main__":
    main()
