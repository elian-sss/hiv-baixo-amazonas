"""Extrai o texto do dicionário de dados (PDF) para leitura. Não altera o original."""
import sys
from pypdf import PdfReader
r = PdfReader("HIVAN_DIC_DADOS(1).pdf")
out = []
for i, p in enumerate(r.pages, 1):
    out.append(f"\n===== PÁGINA {i} =====\n" + (p.extract_text() or ""))
open(sys.argv[1], "w", encoding="utf-8").write("".join(out))
print(len(r.pages), "páginas")
