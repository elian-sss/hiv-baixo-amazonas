"""Etapa 8 - Auditoria independente dos totais do dashboard.

Recalcula os totais por ano e por município SEM pandas e SEM as colunas
derivadas da limpeza (usa só a biblioteca padrão `csv`):
  A) a partir de dados/hiv_baixo_amazonas.csv: ano tirado de DT_NOTIFIC (texto),
     município tirado do código ID_MN_RESI (tabela IBGE própria deste script);
  B) a partir do original HIV16_25.csv, refazendo o recorte do zero
     (filtro por residência + remoção de duplicados exatos + exclusão do CRITERIO 900);
e compara com:
  C) dados/dados_dashboard.json (bloco `conferencia`, lista `anos` e soma dos cubos);
  D) o JSON embutido em dashboard/index.html (deve ser idêntico ao arquivo JSON).

Saída: resultados/auditoria.md
Uso: python scripts/05_auditoria.py
"""
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
BASE = RAIZ / "dados" / "hiv_baixo_amazonas.csv"
ORIGINAL = RAIZ / "HIV16_25.csv"
JSON_ARQ = RAIZ / "dados" / "dados_dashboard.json"
JSON_PUB = RAIZ / "dados" / "dados_dashboard_publico.json"
HTML_INT = RAIZ / "dashboard" / "index_interno.html"   # versão interna <- dados_dashboard.json
HTML_PUB = RAIZ / "dashboard" / "index.html"           # versão pública <- dados_dashboard_publico.json
SAIDA = RAIZ / "resultados" / "auditoria.md"

# Tabela própria (códigos IBGE conferidos na API de localidades do IBGE)
IBGE = {
    "1500404": "Alenquer", "1500503": "Almeirim", "1501451": "Belterra",
    "1502855": "Curuá", "1503002": "Faro", "1503903": "Juruti",
    "1504752": "Mojuí dos Campos", "1504802": "Monte Alegre", "1505106": "Óbidos",
    "1505304": "Oriximiná", "1506005": "Prainha", "1506807": "Santarém",
    "1507979": "Terra Santa",
}

csv.field_size_limit(sys.maxsize if sys.maxsize < 2**31 else 2**31 - 1)


def fmt(n):
    return f"{n:,}".replace(",", ".")


def metodo_a():
    """Base tratada, só biblioteca padrão."""
    por_ano, por_mun, por_am = Counter(), Counter(), Counter()
    with open(BASE, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            ano = int(r["DT_NOTIFIC"][:4])          # 'AAAA-MM-DD'
            mun = IBGE[r["ID_MN_RESI"]]             # KeyError = município fora da lista
            por_ano[ano] += 1
            por_mun[mun] += 1
            por_am[(mun, ano)] += 1
    return por_ano, por_mun, por_am


def metodo_b():
    """Recorte refeito do zero a partir do arquivo original."""
    vistos = set()
    dup = desc = 0
    por_ano, por_mun, por_am = Counter(), Counter(), Counter()
    with open(ORIGINAL, encoding="utf-8", newline="") as f:
        rd = csv.reader(f)
        cab = next(rd)
        i_res, i_dt, i_crit = cab.index("ID_MN_RESI"), cab.index("DT_NOTIFIC"), cab.index("CRITERIO")
        for r in rd:
            if r[i_res] not in IBGE:
                continue
            chave = tuple(r[1:])                     # sem a coluna de índice
            if chave in vistos:
                dup += 1
                continue
            vistos.add(chave)
            if r[i_crit] == "900":
                desc += 1
                continue
            ano, mun = int(r[i_dt][:4]), IBGE[r[i_res]]
            por_ano[ano] += 1
            por_mun[mun] += 1
            por_am[(mun, ano)] += 1
    return por_ano, por_mun, por_am, dup, desc


def do_json(d):
    """Totais declarados no JSON e reconstruídos a partir dos cubos."""
    out = {
        "conferencia.por_ano": Counter({int(k): v for k, v in d["conferencia"]["por_ano"].items()}),
        "conferencia.por_municipio": Counter(d["conferencia"]["por_municipio"]),
        "anos[].n": Counter({a["ano"]: a["n"] for a in d["anos"] if a["n"] is not None}),
    }
    cubos_am = {}
    for nome, t in d["tabelas"].items():
        c = t["colunas"]
        ia, im, iN = c.index("ano"), c.index("municipio"), c.index("n")
        am = Counter()
        for row in t["linhas"]:
            am[(row[im], row[ia])] += row[iN]
        cubos_am[nome] = am
    return out, cubos_am


def compara(nome, ref, outro):
    chaves = sorted(set(ref) | set(outro), key=str)
    return [(nome, k, ref.get(k, 0), outro.get(k, 0)) for k in chaves if ref.get(k, 0) != outro.get(k, 0)]


def main():
    a_ano, a_mun, a_am = metodo_a()
    b_ano, b_mun, b_am, dup, desc = metodo_b()
    d = json.loads(JSON_ARQ.read_text(encoding="utf-8"))
    j, cubos = do_json(d)

    dp = json.loads(JSON_PUB.read_text(encoding="utf-8"))
    jp = {"conferencia.por_ano": Counter({int(k): v for k, v in dp["conferencia"]["por_ano"].items()}),
          "conferencia.por_municipio": Counter(dp["conferencia"]["por_municipio"])}

    # JSON embutido em cada HTML
    def embutido(arq):
        html = arq.read_text(encoding="utf-8")
        m = re.search(r'<script type="application/json" id="dados">(.*?)</script>', html, re.S)
        return json.loads(m.group(1).replace("<\\/", "</")) if m else None
    html_igual = embutido(HTML_INT) == d
    html_pub_igual = embutido(HTML_PUB) == dp

    div = []
    div += compara("A × B (ano)", a_ano, b_ano)
    div += compara("A × B (município)", a_mun, b_mun)
    div += compara("A × B (município×ano)", a_am, b_am)
    div += compara("A × JSON conferencia.por_ano", a_ano, j["conferencia.por_ano"])
    div += compara("A × JSON anos[].n", a_ano, j["anos[].n"])
    div += compara("A × JSON conferencia.por_municipio", a_mun, j["conferencia.por_municipio"])
    # cubos: todos menos 'gestante' devem reproduzir município×ano
    for nome, am in cubos.items():
        if nome == "gestante":
            continue
        div += compara(f"A × JSON cubo {nome} (município×ano)", a_am, am)
    # versão pública: totais e cubos territoriais (os de perfil não têm município)
    div += compara("A × JSON público conferencia.por_ano", a_ano, jp["conferencia.por_ano"])
    div += compara("A × JSON público conferencia.por_municipio", a_mun, jp["conferencia.por_municipio"])
    for nome in ("base", "fluxo"):
        t = dp["tabelas"][nome]
        c = t["colunas"]
        am = Counter()
        for row in t["linhas"]:
            am[(row[c.index("municipio")], row[c.index("ano")])] += row[c.index("n")]
        div += compara(f"A × JSON público cubo {nome} (município×ano)", a_am, am)
    for nome, t in dp["tabelas"].items():
        if "municipio" in t["colunas"] or nome == "gestante":
            continue
        c = t["colunas"]
        pa = Counter()
        for row in t["linhas"]:
            pa[row[c.index("ano")]] += row[c.index("n")]
        div += compara(f"A × JSON público cubo {nome} (ano)", a_ano, pa)
    cubos_pub_ok = [n for n in dp["tabelas"] if n != "gestante"]
    # anos que o JSON marca como sem dados não podem ter registros
    sem_dados = [a["ano"] for a in d["anos"] if a["status"] == "sem_dados"]
    for a in sem_dados:
        if a_ano.get(a, 0):
            div.append(("ano marcado sem_dados com registros", a, a_ano[a], 0))
    total_ok = sum(a_ano.values()) == sum(b_ano.values()) == d["conferencia"]["total"] == d["meta"]["n_total"]

    anos = sorted(set(a_ano) | set(b_ano) | set(j["anos[].n"]))
    muns = sorted(set(a_mun) | set(b_mun), key=lambda s: s.replace("Ó", "O"))

    L = ["# Auditoria dos totais do dashboard\n",
         "Gerado por `scripts/05_auditoria.py`. Os totais foram recalculados por **métodos independentes** "
         "dos usados na limpeza e no dashboard: leitura com a biblioteca padrão `csv` (sem pandas), ano "
         "tirado do texto da data de notificação e município tirado do código IBGE, com tabela de nomes "
         "própria deste script.\n",
         "| Fonte | Como foi calculada |",
         "|---|---|",
         "| **A** | `dados/hiv_baixo_amazonas.csv` (base tratada), sem usar as colunas derivadas `ANO_NOTIF`/`MUNICIPIO` |",
         f"| **B** | `HIV16_25.csv` (original), recorte refeito do zero: residência nos 13 códigos, {fmt(dup)} duplicado(s) exato(s) removido(s), {fmt(desc)} registro(s) com CRITERIO 900 excluído(s) |",
         "| **JSON** | `dados/dados_dashboard.json`: bloco `conferencia`, lista `anos` e soma de cada cubo |",
         "| **JSON público** | `dados/dados_dashboard_publico.json` (versão do GitHub Pages): totais e soma de cada cubo |",
         "| **HTML** | JSON embutido em `dashboard/index_interno.html` (interno) e em `dashboard/index.html` (público) |\n",
         "## Resultado\n",
         f"- Divergências encontradas: **{len(div)}**.",
         f"- Total geral: A = {fmt(sum(a_ano.values()))}, B = {fmt(sum(b_ano.values()))}, "
         f"JSON = {fmt(d['conferencia']['total'])} → {'iguais' if total_ok else '**diferentes**'}.",
         f"- JSON embutido no painel interno idêntico a `dados_dashboard.json`: **{'sim' if html_igual else 'não'}**; "
         f"no painel público, idêntico a `dados_dashboard_publico.json`: **{'sim' if html_pub_igual else 'não'}**.",
         f"- Cubos da versão pública conferidos: {', '.join(cubos_pub_ok)} (os territoriais por município × ano; "
         "os de perfil, que são da região inteira, por ano).",
         f"- Cubos conferidos (município × ano): {', '.join(k for k in cubos if k != 'gestante')}. "
         "O cubo `gestante` contém só mulheres e foi conferido pelo total de mulheres na geração do JSON.\n"]

    L.append("## Totais por ano\n")
    L.append("| Ano | A (base tratada) | B (original) | JSON `conferencia` | JSON `anos[].n` | Status no JSON | Confere? |")
    L.append("|---|---:|---:|---:|---:|---|---|")
    st = {a["ano"]: a["status"] for a in d["anos"]}
    for a in sorted(set(anos) | set(st)):
        va, vb = a_ano.get(a, 0), b_ano.get(a, 0)
        vc, vn = j["conferencia.por_ano"].get(a, 0), j["anos[].n"].get(a)
        ok = va == vb == vc and (vn == va if vn is not None else va == 0)
        L.append(f"| {a} | {fmt(va)} | {fmt(vb)} | {fmt(vc)} | {fmt(vn) if vn is not None else '— (sem dados)'} | "
                 f"{st.get(a, '—')} | {'✔' if ok else '✖'} |")
    L.append(f"| **Total** | **{fmt(sum(a_ano.values()))}** | **{fmt(sum(b_ano.values()))}** | "
             f"**{fmt(sum(j['conferencia.por_ano'].values()))}** | **{fmt(sum(j['anos[].n'].values()))}** | | |\n")

    L.append("## Totais por município\n")
    L.append("| Município | A | B | JSON `conferencia` | JSON cubo `base` | Confere? |")
    L.append("|---|---:|---:|---:|---:|---|")
    base_mun = Counter()
    for (mn, _), v in cubos["base"].items():
        base_mun[mn] += v
    for mn in muns:
        va, vb, vc, vd = a_mun.get(mn, 0), b_mun.get(mn, 0), j["conferencia.por_municipio"].get(mn, 0), base_mun.get(mn, 0)
        L.append(f"| {mn} | {fmt(va)} | {fmt(vb)} | {fmt(vc)} | {fmt(vd)} | {'✔' if va == vb == vc == vd else '✖'} |")
    L.append("")

    L.append("## Divergências e correções\n")
    if not div:
        L.append("Nenhuma divergência. Os 13 totais por município, os totais por ano e as "
                 f"{len(a_am)} combinações município × ano com casos são idênticos nas fontes A, B, no JSON "
                 "e em cada cubo. **Nenhuma correção foi necessária.**\n")
    else:
        L.append("| Comparação | Chave | Valor de referência | Valor comparado |")
        L.append("|---|---|---:|---:|")
        for nome, k, v1, v2 in div:
            L.append(f"| {nome} | {k} | {fmt(v1)} | {fmt(v2)} |")
        L.append("\n**Correção:** regerar o JSON e o dashboard (`scripts/05_dados_dashboard.py` e "
                 "`scripts/06_build_dashboard.py`) e rodar esta auditoria de novo.\n")

    L.append("## O que esta auditoria não cobre\n")
    L.append("- Confere contagens por ano e município, não a correção dos rótulos (sexo, idade, exposição etc.), "
             "que foram conferidos na limpeza (`resultados/decisoes_limpeza.md`).")
    L.append("- Não verifica a qualidade do dado na origem (SINAN): subnotificação e erros de digitação "
             "continuam possíveis.")
    L.append("- Os cálculos feitos no navegador (percentuais, variações) usam os mesmos cubos; foram conferidos "
             "por amostragem na etapa 7 (KPIs comparados com `achados_hiv.md`).\n")

    SAIDA.write_text("\n".join(L), encoding="utf-8")
    print(f"Divergências: {len(div)} | total A={sum(a_ano.values())} B={sum(b_ano.values())} "
          f"JSON={d['conferencia']['total']} | HTML interno igual: {html_igual} | HTML público igual: {html_pub_igual}")
    for x in div[:20]:
        print(x)


if __name__ == "__main__":
    main()
