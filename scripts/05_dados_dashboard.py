"""Etapa 7a - Tabelas agregadas para o dashboard (dados/dados_dashboard.json).

Entrada : dados/hiv_baixo_amazonas.csv (base tratada) e HIV16_25.csv (só DT_NOTIFIC,
          para achar a data de corte da extração)
Saída   : dados/dados_dashboard.json — SOMENTE contagens agregadas (nenhuma linha
          individual, nenhuma data exata, nenhum código de paciente).

Cada tabela é um "cubo" ano × município × sexo × faixa etária (+ uma dimensão),
para que o dashboard aplique os filtros globais. Todos os parâmetros que o
dashboard usa (limiares, períodos) também ficam no JSON.

Uso: python scripts/05_dados_dashboard.py
"""
import json
from datetime import date
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
BASE = RAIZ / "dados" / "hiv_baixo_amazonas.csv"
ORIGINAL = RAIZ / "HIV16_25.csv"
SAIDA = RAIZ / "dados" / "dados_dashboard.json"                 # interno (uso da SESPA)
SAIDA_PUB = RAIZ / "dados" / "dados_dashboard_publico.json"     # público (GitHub Pages)

PARAMETROS = {
    "periodo_projeto": [2016, 2025],
    "ano_padrao": [2016, 2023],
    "periodos_comparacao": [[2016, 2019], [2020, 2023]],
    "limiar_n_minimo": 10,        # abaixo disso: "n insuficiente" no lugar de %
    "limiar_variacao": 10,        # variação anual só se o ano anterior tiver >= 10
    "limiar_poucos_casos": 30,    # município com < 30 no período = poucos casos
    "completude_bom_max": 5,      # % ignorado < 5 = Bom
    "completude_atencao_max": 10, # 5 a 10 = Atenção; > 10 = Crítico
    "campos_criticos_desatualizacao": ["evolucao"],
    "municipio_polo": "Santarém",
    "faixa_jovem": ["15-19", "20-24", "25-29"],
    "privacidade_ocultar_ate": 4,  # em divulgação externa, ocultar contagens 1..4
    "destaque_series": {"anos": [2020, 2021], "rotulo": "pandemia de covid-19"},
}

ORD = {
    "sexo": ["Masculino", "Feminino", "Ignorado"],
    "faixa": ["<15", "15-19", "20-24", "25-29", "30-39", "40-49", "50-59", "60+", "Ignorada"],
    "exposicao": ["Heterossexual", "Homossexual", "Bissexual", "Drogas injetáveis",
                  "Vertical", "Outras", "Ignorado"],
    "evolucao": ["Vivo", "Óbito por aids", "Óbito por outras causas", "Ignorado"],
    "gestante": ["1º trimestre", "2º trimestre", "3º trimestre", "Idade gestacional ignorada",
                 "Não", "Não se aplica", "Ignorado"],
    "raca": ["Parda", "Preta", "Branca", "Indígena", "Amarela", "Ignorado"],
    "escolaridade": ["Até fundamental incompleto", "Fundamental completo / médio incompleto",
                     "Médio completo / superior incompleto", "Superior completo",
                     "Ignorado", "Não se aplica"],
    "local_notificacao": ["Próprio município", "Santarém", "Outro município"],
}
ESCOL_GRUPO = {
    "Analfabeto": 0, "1ª a 4ª série incompleta do EF": 0, "4ª série completa do EF": 0,
    "5ª a 8ª série incompleta do EF": 0, "Ensino fundamental completo": 1,
    "Ensino médio incompleto": 1, "Ensino médio completo": 2,
    "Educação superior incompleta": 2, "Educação superior completa": 3,
}
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
         "setembro", "outubro", "novembro", "dezembro"]


def cubo(df, dims):
    g = df.groupby(dims, observed=True).size().reset_index(name="n")
    return {"colunas": dims + ["n"],
            "linhas": [[(int(v) if isinstance(v, (int,)) or hasattr(v, "item") and str(v).isdigit() else v)
                        for v in row] for row in g.itertuples(index=False)]}


def main():
    df = pd.read_csv(BASE, dtype=str, encoding="utf-8-sig")
    df["ano"] = df["ANO_NOTIF"].astype(int)
    df["semestre"] = (df["MES_NOTIF"].astype(int) > 6).astype(int) + 1
    df["municipio"] = df["MUNICIPIO"]
    df["sexo"] = df["SEXO"]
    df["faixa"] = df["FAIXA_ETARIA"]
    df["exposicao"] = df["CAT_EXPOSICAO_GRUPO"]
    df["evolucao"] = df["EVOLUCAO_DESC"]
    df["gestante"] = df["GESTANTE"]
    df["raca"] = df["RACA_COR"]
    df["escolaridade"] = df["ESCOLARIDADE"].map(
        lambda e: ORD["escolaridade"][ESCOL_GRUPO[e]] if e in ESCOL_GRUPO else e)
    cod_polo = df.loc[df["MUNICIPIO"] == PARAMETROS["municipio_polo"], "ID_MN_RESI"].iloc[0]
    df["local_notificacao"] = df.apply(
        lambda r: "Próprio município" if r["ID_MUNICIP"] == r["ID_MN_RESI"]
        else ("Santarém" if r["ID_MUNICIP"] == cod_polo else "Outro município"), axis=1)

    # categorias fora da ordem prevista? (falha cedo, para não sumir dado)
    for k, ordem in ORD.items():
        extra = set(df[k].unique()) - set(ordem)
        assert not extra, f"categoria inesperada em {k}: {extra}"

    # Data de corte da extração = última notificação no arquivo inteiro (Brasil)
    dt_br = pd.to_datetime(pd.read_csv(ORIGINAL, dtype=str, usecols=["DT_NOTIFIC"])["DT_NOTIFIC"],
                           format="%Y%m%d", errors="coerce")
    corte = dt_br.max()
    ult_regiao = pd.to_datetime(df["DT_NOTIFIC"]).max()

    anos = []
    ini, fim = PARAMETROS["periodo_projeto"]
    por_ano = df.groupby("ano").size()
    for a in range(ini, fim + 1):
        if a < corte.year:
            st, rot, meses = "completo", str(a), 12
        elif a == corte.year and not (corte.month == 12 and corte.day == 31):
            st = "parcial"
            meses = corte.month
            rot = f"{a} (parcial: jan–{MESES[corte.month - 1][:3]})"
        else:
            st, rot, meses = "sem_dados", f"{a} (sem dados)", 0
        anos.append({"ano": a, "status": st, "parcial": st != "completo",
                     "rotulo": rot, "meses_com_dados": meses,
                     "n": int(por_ano[a]) if a in por_ano.index else None})

    muns = (df[["ID_MN_RESI", "MUNICIPIO"]].drop_duplicates()
            .sort_values("MUNICIPIO", key=lambda s: s.str.normalize("NFKD")
                         .str.encode("ascii", "ignore").str.decode("ascii")))
    D4 = ["ano", "municipio", "sexo", "faixa"]
    fem = df[df["sexo"] == "Feminino"]

    def conta(col):
        vc = df[col].value_counts()
        return {c: int(vc.get(c, 0)) for c in ORD[col]}

    dados = {
        "meta": {
            "titulo": "HIV · Baixo Amazonas",
            "descricao": "Notificações de HIV (ficha HIV adulto) de residentes nos municípios da "
                         "Região de Saúde do Baixo Amazonas (PA).",
            "fonte": "Sistema de Informação de Agravos de Notificação (SINAN) / Ministério da Saúde",
            "arquivo_origem": "HIV16_25.csv",
            "base_tratada": "dados/hiv_baixo_amazonas.csv",
            "gerado_em": date.today().isoformat(),
            "data_corte_extracao": corte.date().isoformat(),
            "ultima_notificacao_regiao": ult_regiao.date().isoformat(),
            "n_total": int(len(df)),
            "n_municipios": int(len(muns)),
            "referencia_temporal": "ano de notificação",
            "referencia_geografica": "município de residência",
            # Fontes citadas nas Notas Metodológicas (URLs abertas e conferidas na data de acesso)
            "fontes": [
                {"nome": "Ministério da Saúde. Portal do Sistema de Informação de Agravos de Notificação (SINAN)",
                 "url": "https://portalsinan.saude.gov.br/", "acesso": "2026-11-05"},
                {"nome": "Ministério da Saúde / GT-SINAN. Dicionário de Dados – Agravo: HIV Adulto "
                         "(revisado em fevereiro/2024). Arquivo HIVAN_DIC_DADOS(1).pdf, fornecido com a base",
                 "url": None, "acesso": "2026-11-05"},
                {"nome": "Notificações de HIV do SINAN, Brasil, 2016 a 30/06/2024. Arquivo HIV16_25.csv, "
                         "fornecido para a disciplina",
                 "url": None, "acesso": "2026-11-05"},
                {"nome": "IBGE. API de Localidades (códigos dos municípios)",
                 "url": "https://servicodados.ibge.gov.br/api/docs/localidades", "acesso": "2026-11-05"},
                {"nome": "Brasil. Lei nº 13.709, de 14 de agosto de 2018 – Lei Geral de Proteção de Dados "
                         "Pessoais (LGPD), arts. 5º, 11 e 13",
                 "url": "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm",
                 "acesso": "2026-11-05"},
                {"nome": "Ministério da Saúde. Departamento de HIV/Aids, Tuberculose, Hepatites Virais e "
                         "Infecções Sexualmente Transmissíveis",
                 "url": "https://www.gov.br/aids/pt-br", "acesso": "2026-11-05"},
            ],
        },
        "parametros": PARAMETROS,
        "anos": anos,
        "municipios": [{"codigo_ibge": c, "nome": n} for c, n in muns.itertuples(index=False)],
        "categorias": ORD,
        "tabelas": {
            "base": cubo(df, ["ano", "semestre", "municipio", "sexo", "faixa"]),
            "exposicao": cubo(df, D4 + ["exposicao"]),
            "evolucao": cubo(df, D4 + ["evolucao"]),
            "raca": cubo(df, D4 + ["raca"]),
            "escolaridade": cubo(df, D4 + ["escolaridade"]),
            "gestante": cubo(fem, ["ano", "municipio", "faixa", "gestante"]),
            "fluxo": cubo(df, D4 + ["local_notificacao"]),
        },
        "conferencia": {
            "total": int(len(df)),
            "por_ano": {str(k): int(v) for k, v in por_ano.items()},
            "por_municipio": {m: int(v) for m, v in df["municipio"].value_counts()
                              .reindex(muns["MUNICIPIO"]).items()},
            "por_sexo": conta("sexo"),
            "por_faixa": conta("faixa"),
            "por_exposicao": conta("exposicao"),
            "por_evolucao": conta("evolucao"),
            "por_local_notificacao": conta("local_notificacao"),
        },
    }
    # normaliza tipos numpy -> python
    for t in dados["tabelas"].values():
        t["linhas"] = [[int(v) if hasattr(v, "item") else v for v in row] for row in t["linhas"]]

    # checagem: todo cubo soma o total (gestante soma o total de mulheres)
    for nome, t in dados["tabelas"].items():
        soma = sum(r[-1] for r in t["linhas"])
        esperado = len(fem) if nome == "gestante" else len(df)
        assert soma == esperado, (nome, soma, esperado)

    dados["meta"]["versao_publica"] = False
    SAIDA.write_text(json.dumps(dados, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"OK: {SAIDA} ({SAIDA.stat().st_size / 1024:.1f} KB)")

    # ---------------- versão PÚBLICA (para o GitHub Pages) ----------------
    # Menos detalhe: nenhum cruzamento de município com sexo, idade ou outra
    # característica. Territorial = ano × município; perfil = região inteira.
    # Na tela, contagens de 1 a privacidade_ocultar_ate aparecem como "<5".
    pub = json.loads(json.dumps(dados))
    pub["meta"]["versao_publica"] = True
    P3 = ["ano", "sexo", "faixa"]
    pub["tabelas"] = {
        "base": cubo(df, ["ano", "semestre", "municipio"]),
        "fluxo": cubo(df, ["ano", "municipio", "local_notificacao"]),
        "perfil": cubo(df, P3),
        "exposicao": cubo(df, P3 + ["exposicao"]),
        "evolucao": cubo(df, P3 + ["evolucao"]),
        "raca": cubo(df, P3 + ["raca"]),
        "escolaridade": cubo(df, P3 + ["escolaridade"]),
        "gestante": cubo(fem, ["ano", "faixa", "gestante"]),
    }
    for t in pub["tabelas"].values():
        t["linhas"] = [[int(v) if hasattr(v, "item") else v for v in row] for row in t["linhas"]]
    for nome, t in pub["tabelas"].items():
        soma = sum(r[-1] for r in t["linhas"])
        esperado = len(fem) if nome == "gestante" else len(df)
        assert soma == esperado, ("publico", nome, soma, esperado)
    SAIDA_PUB.write_text(json.dumps(pub, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"OK: {SAIDA_PUB} ({SAIDA_PUB.stat().st_size / 1024:.1f} KB)")
    print(json.dumps({"meta": dados["meta"], "anos": anos, "conferencia": dados["conferencia"],
                      "linhas_por_tabela": {k: len(v["linhas"]) for k, v in dados["tabelas"].items()}},
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
