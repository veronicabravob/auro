"""Une la declaración de uso de IA y el anexo de proceso en un HTML con estilo Auro (para imprimir a PDF).

Uso: python build_pdf_html.py   -> genera declaracion-uso-ia.html junto a este archivo.
"""
import os
import re

import markdown

d = os.path.dirname(os.path.abspath(__file__))
LIST = re.compile(r"^\s*([-*]|\d+\.) ")


def prep(text):
    """Ajusta el Markdown a lo que espera Python-Markdown."""
    out, prev = [], ""
    for line in text.splitlines():
        m = re.match(r"^( +)([-*]|\d+\.) ", line)
        if m:  # listas anidadas: 2 espacios -> 4
            line = " " * (len(m.group(1)) * 2) + line.lstrip()
        if LIST.match(line) and not line.startswith(" ") and prev.strip() and not LIST.match(prev):
            out.append("")  # línea en blanco antes de una lista pegada a un párrafo
        out.append(line)
        prev = line
    return "\n".join(out)


def md(name):
    with open(os.path.join(d, name), encoding="utf-8") as f:
        return markdown.markdown(prep(f.read()), extensions=["tables"])


LOGO = ('<svg width="30" height="30" viewBox="0 0 48 48" aria-hidden="true">'
        '<circle cx="22" cy="27" r="15" fill="none" stroke="#6A48F5" stroke-width="9"/>'
        '<circle cx="33" cy="16" r="7.5" fill="#FFC83D"/></svg>')

CSS = """
@page { size: A4; margin: 14mm 15mm 13mm; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Outfit', system-ui, sans-serif; color: #1B1533; font-size: 9.6pt; line-height: 1.45; margin: 0; }
.page { break-after: page; } .page:last-child { break-after: auto; }
.top { display: flex; align-items: center; gap: 8px; border-bottom: 2px solid #6A48F5; padding-bottom: 5px; margin-bottom: 8px; color: #4B4470; font-size: 8pt; }
.top b { color: #1B1533; font-size: 10pt; }
h1 { font-size: 17pt; letter-spacing: -0.02em; margin: 4px 0 6px; }
h2 { font-size: 11pt; color: #4B2FD6; margin: 12px 0 4px; break-after: avoid; }
p { margin: 0 0 6px; } ul, ol { margin: 2px 0 6px; padding-left: 16px; } li { margin: 2px 0; }
table { width: 100%; border-collapse: collapse; font-size: 9pt; margin: 4px 0 8px; }
th { text-align: left; color: #4B4470; border-bottom: 1px solid #E1DAF7; padding: 4px 6px; }
td { border-bottom: 1px solid #EEEAFB; padding: 4px 6px; vertical-align: top; }
td:first-child { width: 28%; }
h1 + p { background: #F7F5FF; border-left: 4px solid #FFC83D; padding: 6px 10px; border-radius: 0 8px 8px 0; }
"""

html = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Auro by BFE · Declaración de uso de IA</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
<section class="page"><div class="top">{LOGO}<div><b>Auro by BFE</b> · Declaración de uso de IA</div></div>{md('declaracion-uso-ia.md')}</section>
<section class="page"><div class="top">{LOGO}<div><b>Auro by BFE</b> · Anexo · Proceso de diseño con IA</div></div>{md('proceso-diseno-con-ia.md')}</section>
</body></html>"""

with open(os.path.join(d, "declaracion-uso-ia.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("ok")
