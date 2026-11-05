"""Etapa 7b - Monta o dashboard (arquivo único) embutindo o JSON agregado.

Gera duas versões a partir do mesmo modelo (scripts/dashboard_template.html):
  - dashboard/index.html          <- dados/dados_dashboard_publico.json (versão PÚBLICA,
                                     publicada no GitHub Pages; contagens 1–4 ocultadas)
  - dashboard/index_interno.html  <- dados/dados_dashboard.json (versão INTERNA da SESPA,
                                     com todos os cruzamentos; NÃO vai para o GitHub)

Uso: python scripts/06_build_dashboard.py
"""
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TEMPLATE = RAIZ / "scripts" / "dashboard_template.html"
SAIDAS = {
    RAIZ / "dashboard" / "index.html": RAIZ / "dados" / "dados_dashboard_publico.json",
    RAIZ / "dashboard" / "index_interno.html": RAIZ / "dados" / "dados_dashboard.json",
}

html = TEMPLATE.read_text(encoding="utf-8")
assert html.count("/*__DADOS__*/") == 1
for saida, js in SAIDAS.items():
    dados = js.read_text(encoding="utf-8").replace("</", "<\\/")  # seguro dentro de <script>
    saida.parent.mkdir(exist_ok=True)
    saida.write_text(html.replace("/*__DADOS__*/", dados), encoding="utf-8")
    print(f"OK: {saida} ({saida.stat().st_size / 1024:.1f} KB) <- {js.name}")
