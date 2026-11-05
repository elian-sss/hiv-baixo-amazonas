"""Etapa 9 - Resumo em PDF da interpretação dos principais achados.

Todos os números são calculados aqui a partir de dados/dados_dashboard.json
(contagens agregadas, auditadas) e de resultados/series_indice_2019.csv
(contexto Brasil). Gráficos reaproveitados de resultados/ (etapa 4).

Saída: resultados/resumo_achados_hiv.pdf
Uso:   python scripts/07_pdf_achados.py
"""
import csv
import json
from collections import Counter
from math import erf, sqrt
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

RAIZ = Path(__file__).resolve().parent.parent
D = json.loads((RAIZ / "dados" / "dados_dashboard.json").read_text(encoding="utf-8"))
RES = RAIZ / "resultados"
SAIDA = RES / "resumo_achados_hiv.pdf"

AZUL = colors.HexColor("#2a78d6")
CINZA = colors.HexColor("#52514e")
FUNDO = colors.HexColor("#efeee9")


def fmt(n):
    return f"{int(n):,}".replace(",", ".")


def pc(x, c=1):
    return f"{x:.{c}f}%".replace(".", ",")


def num(x, c=1):
    return f"{x:.{c}f}".replace(".", ",")


def linhas(nome):
    t = D["tabelas"][nome]
    return [dict(zip(t["colunas"], r)) for r in t["linhas"]]


def soma(rows, **f):
    return sum(r["n"] for r in rows
               if all((r[k] in v) if isinstance(v, (set, list, tuple, range)) else r[k] == v
                      for k, v in f.items()))


def p_valor(x1, n1, x2, n2):
    p = (x1 + x2) / (n1 + n2)
    se = sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    z = (x1 / n1 - x2 / n2) / se
    return 2 * (1 - 0.5 * (1 + erf(abs(z) / sqrt(2))))


def main():
    P = D["parametros"]
    (a1, b1), (a2, b2) = P["periodos_comparacao"]
    R1, R2 = range(a1, b1 + 1), range(a2, b2 + 1)
    RT = range(a1, b2 + 1)
    base, exp, ges, flu = linhas("base"), linhas("exposicao"), linhas("gestante"), linhas("fluxo")
    anos = {a["ano"]: a for a in D["anos"]}
    por_ano = {int(k): v for k, v in D["conferencia"]["por_ano"].items()}
    N_all = D["meta"]["n_total"]
    N = soma(base, ano=RT)
    polo = P["municipio_polo"]
    por_mun = D["conferencia"]["por_municipio"]
    poucos = sorted([m for m, v in por_mun.items() if v < P["limiar_poucos_casos"]], key=lambda m: por_mun[m])
    parcial = [a for a in D["anos"] if a["status"] == "parcial"]
    sem = [a for a in D["anos"] if a["status"] == "sem_dados"]

    # sexo
    h, m = soma(base, ano=RT, sexo="Masculino"), soma(base, ano=RT, sexo="Feminino")
    m1, n1 = soma(base, ano=R1, sexo="Feminino"), soma(base, ano=R1)
    m2, n2 = soma(base, ano=R2, sexo="Feminino"), soma(base, ano=R2)
    # idade
    jov = soma(base, ano=RT, faixa=P["faixa_jovem"])
    com_idade = N - soma(base, ano=RT, faixa="Ignorada")
    # exposição entre homens
    hm1, hm2 = soma(exp, ano=R1, sexo="Masculino"), soma(exp, ano=R2, sexo="Masculino")
    ho1, ho2 = soma(exp, ano=R1, sexo="Masculino", exposicao="Homossexual"), soma(exp, ano=R2, sexo="Masculino", exposicao="Homossexual")
    bi1, bi2 = soma(exp, ano=R1, sexo="Masculino", exposicao="Bissexual"), soma(exp, ano=R2, sexo="Masculino", exposicao="Bissexual")
    het = soma(exp, ano=RT, exposicao="Heterossexual")
    # gestantes
    G = ["1º trimestre", "2º trimestre", "3º trimestre", "Idade gestacional ignorada"]
    mulheres, gest = soma(ges, ano=RT), soma(ges, ano=RT, gestante=G)
    t1 = soma(ges, ano=RT, gestante="1º trimestre")
    t23 = soma(ges, ano=RT, gestante=["2º trimestre", "3º trimestre"])
    vert = soma(exp, ano=RT, exposicao="Vertical")
    # qualidade
    esc = linhas("escolaridade")
    ei1 = 100 * soma(esc, ano=R1, escolaridade="Ignorado") / n1
    ei2 = 100 * soma(esc, ano=R2, escolaridade="Ignorado") / n2
    evo = linhas("evolucao")
    vivo = soma(evo, ano=RT, evolucao="Vivo")
    obitos = soma(evo, ano=RT, evolucao=["Óbito por aids", "Óbito por outras causas"])
    # fluxo (2016-2024, todos os anos com dados)
    fora = N_all - D["conferencia"]["por_local_notificacao"]["Próprio município"]
    no_polo = D["conferencia"]["por_local_notificacao"][polo]
    fl = Counter()
    for r in flu:
        fl[(r["municipio"], r["local_notificacao"])] += r["n"]
    tot_mun_fl = Counter()
    for (mn, _), v in fl.items():
        tot_mun_fl[mn] += v
    maiores_fluxo = sorted([mn for mn in tot_mun_fl if mn != polo and tot_mun_fl[mn] >= P["limiar_n_minimo"]],
                           key=lambda mn: -fl[(mn, polo)] / tot_mun_fl[mn])[:3]
    # pandemia
    idx = {int(r["ano"]): r for r in csv.DictReader(open(RES / "series_indice_2019.csv", encoding="utf-8-sig"))}
    br19, br20 = int(idx[2019]["brasil_casos"]), int(idx[2020]["brasil_casos"])
    st = {a: soma(base, ano=a, municipio=polo) for a in (2019, 2020, 2021, 2022)}
    de = {a: soma(base, ano=a) - st[a] for a in (2019, 2020, 2021, 2022)}
    var = lambda a: 100 * (por_ano[a] - por_ano[a - 1]) / por_ano[a - 1]
    s1_23 = soma(base, ano=2023, semestre=1)
    s1_24 = soma(base, ano=parcial[0]["ano"], semestre=1) if parcial else None
    ano_max = max((a for a in RT), key=lambda a: por_ano[a])
    ano_min = min((a for a in RT), key=lambda a: por_ano[a])

    # ------------------------------------------------------------- documento
    ss = getSampleStyleSheet()
    H1 = ParagraphStyle("h1", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=17, leading=21,
                        alignment=TA_LEFT, spaceAfter=4)
    SUB = ParagraphStyle("sub", parent=ss["Normal"], fontSize=9.5, textColor=CINZA, leading=13)
    H2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=12.5,
                        textColor=AZUL, spaceBefore=10, spaceAfter=4)
    TX = ParagraphStyle("tx", parent=ss["Normal"], fontSize=10, leading=14, spaceAfter=4)
    LIM = ParagraphStyle("lim", parent=TX, fontSize=9, textColor=CINZA, leading=12.5)
    BOX = ParagraphStyle("box", parent=TX, backColor=FUNDO, borderPadding=7, spaceBefore=6, spaceAfter=10)

    def achado(n, titulo, texto, sig, limite, pergunta):
        return KeepTogether([
            Paragraph(f"{n}. {titulo}", H2),
            Paragraph(texto, TX),
            Paragraph(f"<b>O que isso significa:</b> {sig}", TX),
            Paragraph(f"<b>Cuidado:</b> {limite}", LIM),
            Paragraph(f"<b>Pergunta para a vigilância:</b> {pergunta}", TX),
        ])

    S = []
    S.append(Paragraph("HIV no Baixo Amazonas: o que os dados mostram", H1))
    S.append(Paragraph(
        f"Resumo da interpretação dos principais achados · Notificações do SINAN (Ministério da Saúde) de "
        f"residentes em {D['meta']['n_municipios']} municípios · dados até "
        f"{'/'.join(reversed(D['meta']['data_corte_extracao'].split('-')))} · elaborado em "
        f"{'/'.join(reversed(D['meta']['gerado_em'].split('-')))}", SUB))
    S.append(Spacer(1, 6))
    S.append(Paragraph(
        "<b>Antes de ler:</b> os números são de <b>notificações</b>, isto é, pessoas diagnosticadas e registradas "
        "no sistema. Não são o total de pessoas com HIV nem de novas infecções (notificação não é incidência). "
        "Há subnotificação, e os números dependem da testagem e do registro em cada município. "
        "Não há população na base, por isso não há taxas: os municípios são comparados só em números "
        f"absolutos e em participação percentual. {parcial[0]['ano']} tem só {parcial[0]['meses_com_dados']} meses "
        f"de dados e {', '.join(str(a['ano']) for a in sem)} não está na base." if parcial else "", BOX))

    S.append(Paragraph("Em uma frase", H2))
    S.append(Paragraph(
        f"Entre {a1} e {b2}, as notificações de HIV na região cresceram (de {fmt(por_ano[a1])} para "
        f"{fmt(por_ano[ano_max])} em {ano_max}), concentram-se em {polo} e em homens jovens, e o aumento "
        "pode refletir tanto mais transmissão quanto mais testagem e registro — os dados não permitem separar "
        "uma coisa da outra.", TX))

    img = RES / "series_g1_total_ano.png"
    if img.exists():
        S.append(Image(str(img), width=16 * cm, height=16 * cm * 630 / 1200))
        S.append(Paragraph("Notificações por ano. 2024 hachurado: só janeiro a junho. Faixa cinza: 2020–2021.", LIM))

    S.append(achado(1, "As notificações cresceram, sobretudo durante e depois da pandemia",
        f"O menor ano foi {ano_min} ({fmt(por_ano[ano_min])}) e o maior foi {ano_max} ({fmt(por_ano[ano_max])}). "
        f"Em 2020, enquanto as notificações no Brasil caíram {pc(100 * (br19 - br20) / br19)} "
        f"({fmt(br19)} para {fmt(br20)}), na região subiram {pc(var(2020))} e, em 2021, mais {pc(var(2021))}. "
        f"O aumento veio quase todo de {polo} ({fmt(st[2019])}, {fmt(st[2020])} e {fmt(st[2021])} em 2019, 2020 e 2021); "
        f"os demais municípios somados ficaram estáveis ({fmt(de[2019])}, {fmt(de[2020])}, {fmt(de[2021])}) e "
        f"subiram em 2022 ({fmt(de[2022])}).",
        "A região não seguiu a queda nacional da pandemia. Isso pode indicar ampliação da testagem ou mudança "
        f"no registro em {polo}, ou ainda diagnósticos que estavam represados e apareceram depois.",
        f"Não é possível afirmar a causa. {parcial[0]['ano']} parece menor ({fmt(s1_24)} no 1º semestre, contra "
        f"{fmt(s1_23)} no 1º semestre de 2023), mas pode ser atraso de digitação." if parcial else "",
        f"O que mudou na oferta de testagem e na rotina de notificação de {polo} entre 2019 e 2021?"))

    S.append(achado(2, f"{polo} concentra as notificações, e muitos moradores de outros municípios são notificados lá",
        f"{polo} tem {fmt(por_mun[polo])} das {fmt(N_all)} notificações ({pc(100 * por_mun[polo] / N_all)}) de "
        f"{min(por_ano)} a {max(por_ano)}. {fmt(fora)} notificações ({pc(100 * fora / N_all)}) foram feitas fora do "
        f"município de residência, {fmt(no_polo)} delas em {polo}. Os municípios com maior proporção de moradores "
        f"notificados em {polo} foram "
        + ", ".join(f"{mn} ({fmt(fl[(mn, polo)])} de {fmt(tot_mun_fl[mn])}, {pc(100 * fl[(mn, polo)] / tot_mun_fl[mn])})" for mn in maiores_fluxo)
        + f"; entre os maiores, Óbidos ({pc(100 * fl[('Óbidos', polo)] / tot_mun_fl['Óbidos'])}) e Juruti "
        f"({pc(100 * fl[('Juruti', polo)] / tot_mun_fl['Juruti'])}).",
        f"{polo} funciona como polo de diagnóstico da região. Contar pelo município de residência evita "
        "inflar o polo e esconder os demais.",
        "Concentração em números absolutos não é risco maior: sem população, não há taxa. "
        f"{', '.join(poucos)} têm menos de {P['limiar_poucos_casos']} notificações no período, e qualquer "
        "percentual nesses municípios é instável.",
        "Os municípios que mandam pacientes para o polo têm testagem e acompanhamento locais suficientes?"))

    S.append(achado(3, "Predominam homens e jovens; cresce a exposição homossexual entre homens",
        f"De {a1} a {b2}, homens são {pc(100 * h / N)} das notificações; a participação das mulheres caiu de "
        f"{pc(100 * m1 / n1)} ({a1}–{b1}) para {pc(100 * m2 / n2)} ({a2}–{b2}). Metade das pessoas "
        f"({pc(100 * jov / com_idade)}) tem de 15 a 29 anos. Entre homens, a categoria homossexual passou de "
        f"{pc(100 * ho1 / hm1)} para {pc(100 * ho2 / hm2)} e a bissexual caiu de {pc(100 * bi1 / hm1)} para "
        f"{pc(100 * bi2 / hm2)}. Na região como um todo, a heterossexual segue a maior ({pc(100 * het / N)}).",
        "O HIV notificado na região é, sobretudo, de homens jovens, e as ações de prevenção e testagem precisam "
        "chegar a eles, incluindo homens que fazem sexo com homens.",
        f"As diferenças entre períodos são estatisticamente significativas (teste de proporções; para "
        f"mulheres, {('p < 0,001' if p_valor(m1, n1, m2, n2) < 0.001 else 'p = ' + num(p_valor(m1, n1, m2, n2), 3))}), mas mostram mudança nas notificações, não necessariamente na epidemia. A exposição é "
        "autodeclarada e pode refletir mudança na forma de perguntar.",
        "A testagem de homens jovens aumentou? E as mulheres fora do pré-natal estão sendo testadas?"))

    S.append(achado(4, "Gestantes notificadas tarde na gravidez",
        f"{fmt(gest)} de {fmt(mulheres)} mulheres ({pc(100 * gest / mulheres)}) estavam gestantes na notificação. "
        f"Dessas, {fmt(t23)} ({pc(100 * t23 / gest)}) estavam no 2º ou 3º trimestre e só {fmt(t1)} no 1º. "
        f"Houve {fmt(vert)} notificações com transmissão de mãe para filho no período.",
        "Diagnóstico tardio na gestação reduz o tempo para evitar a transmissão para o bebê. É o ponto em que "
        "a vigilância pode agir mais diretamente.",
        "O trimestre é o da notificação, não o do diagnóstico; gestantes têm ficha própria no SINAN, que não "
        "está nesta base.",
        "O teste de HIV está sendo feito no 1º trimestre do pré-natal em todos os municípios?"))

    S.append(achado(5, "O registro melhorou, mas o desfecho dos casos não é acompanhado",
        f"A escolaridade ignorada caiu de {pc(ei1)} para {pc(ei2)}. Por outro lado, {pc(100 * vivo / N)} dos "
        f"casos constam como \"vivo\" e só {fmt(obitos)} óbitos foram registrados de {a1} a {b2}.",
        "Os campos da ficha estão mais completos, mas a evolução não é atualizada; o painel não serve para "
        "medir mortalidade por aids.",
        "Mudanças bruscas no perfil (como na escolaridade, a partir de 2020) podem ser efeito do preenchimento.",
        "Os óbitos de residentes estão sendo cruzados com o Sistema de Informações sobre Mortalidade (SIM)?"))

    S.append(Paragraph("O que estes dados não permitem dizer", H2))
    tab = [["Pergunta", "Por que não"],
           ["Qual município tem maior risco?", "Não há população para calcular taxas."],
           ["A epidemia cresceu?", "Só há notificações, que dependem da testagem."],
           ["Quantas pessoas morreram de aids?", "A evolução não é atualizada (exige o SIM)."],
           [f"{parcial[0]['ano']} foi melhor que {parcial[0]['ano'] - 1}?" if parcial else "Ano parcial",
            "O ano está incompleto e pode receber registros atrasados."],
           ["A pandemia causou o aumento?", "Os dados mostram coincidência no tempo, não causa."]]
    t = Table(tab, colWidths=[6.5 * cm, 10 * cm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9.5), ("FONT", (0, 1), (-1, -1), "Helvetica", 9.5),
                           ("BACKGROUND", (0, 0), (-1, 0), FUNDO), ("LINEBELOW", (0, 0), (-1, -1), 0.4, colors.HexColor("#d9d8d2")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    S.append(t)
    S.append(Spacer(1, 8))
    S.append(Paragraph("Próximos passos sugeridos", H2))
    S.append(Paragraph("(1) Incluir a população do IBGE para calcular taxas por município; (2) cruzar com o SIM para "
                       "óbitos; (3) atualizar a base com os dados completos de 2024 e de 2025; (4) discutir com os "
                       "municípios as perguntas acima.", TX))
    S.append(Spacer(1, 6))
    S.append(Paragraph(
        "Fonte: SINAN/Ministério da Saúde (arquivo HIV16_25.csv). Números calculados a partir de "
        "dados/dados_dashboard.json (contagens agregadas, conferidas em resultados/auditoria.md) e "
        "resultados/series_indice_2019.csv. Detalhes em resultados/achados_hiv.md e resultados/series_relatorio.md. "
        "Documento de uso interno da vigilância epidemiológica.", LIM))

    def rodape(c, doc):
        c.saveState()
        c.setFont("Helvetica", 8)
        c.setFillColor(CINZA)
        c.drawString(2 * cm, 1.2 * cm, "HIV no Baixo Amazonas · notificação não é incidência · uso interno")
        c.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"página {doc.page}")
        c.restoreState()

    doc = SimpleDocTemplate(str(SAIDA), pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                            topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                            title="HIV no Baixo Amazonas: resumo dos achados", author="Projeto Introdução à Ciência de Dados",
                            subject="Interpretação dos principais achados das notificações de HIV (SINAN)")
    doc.build(S, onFirstPage=rodape, onLaterPages=rodape)
    print(f"OK: {SAIDA}")


if __name__ == "__main__":
    main()
