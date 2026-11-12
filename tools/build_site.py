"""Convierte el export 'tablero' de Auro en un sitio estatico navegable y responsive.

Uso: python tools/build_site.py "Auro by BFE · Prototipo.html" site
Cada pantalla del tablero queda como un archivo con el nombre que usan sus
enlaces internos (Diagnostico.dc.html, Oferta.dc.html, ...), y a cada una se le
inyecta viewport + la hoja responsive.css.
"""
import base64, gzip, json, os, re, sys

PAGES = {
    "dda5e472-46e4-4753-8c40-2e5ae39773c0": ["index.html", "Main.dc.html"],
    "08970673-ba55-462d-800c-dc1e2d84c133": ["Registro.dc.html"],
    "7e7725c1-e59e-4ef8-9102-9f860aae1226": ["Facturas.dc.html"],
    "eb2a87c9-596a-4c1d-ae9d-799ddd34f9b0": ["Fuentes.dc.html"],
    "12bdcfaf-103c-4f87-b35a-e7dab8dd850f": ["Diagnostico.dc.html"],
    "5456a898-98b8-4c68-8b6a-409bcbdcdbf2": ["Caja.dc.html"],
    "ba34811a-8f9d-4538-a414-698577ddd57c": ["Chat.dc.html"],
    "e78265c7-2921-4f47-900b-d78d82238579": ["Nueva.dc.html"],
    "f2bddd9a-dc98-41e5-ada4-339dc4a9db41": ["Oferta.dc.html"],
    "90f7036a-55c6-4703-b5f8-68c94f151d55": ["Vinculacion.dc.html"],
    "2d4d0f04-acc3-449a-9a83-4d8549d435c4": ["Uso.dc.html"],
    "9202b114-dc82-43a9-abed-a34861d9bbf2": ["Plan.dc.html"],
    "e8a29fc6-8963-48c9-9309-da23d564eec0": ["MsgCobro.dc.html"],
    "ecfe0601-514c-47fd-a361-6159ce0e6fbd": ["MsgProntoPago.dc.html"],
    "79a7d60e-4054-4b85-8c3e-a15b96cbc1c5": ["MsgPlazo.dc.html"],
    "40c05131-a922-48d6-a443-ab20d52598e3": ["FallaDatos.dc.html"],
    "0f906788-39ab-482b-b998-8c7e725d6740": ["FallaDestino.dc.html"],
    "43fbf74d-98e5-424c-b33e-10fe0035b049": ["Abono.dc.html"],
}

# Correcciones de cifras para que el prototipo cuadre con el modelo financiero.
# Intereses con tasa efectiva: monto * (1,149^(dias/365) - 1).
#   $12 M a 60 dias = 277.130 ; $14 M a 60 dias = 323.319 ; $12 M a 90 dias = 418.086 ;
#   $12 M a 30 dias (lo que se ahorra al abonar un mes antes) = 137.774.
# Tasa de referencia de mercado: tope en la usura de nov-2026 (28,34 %).
# Comision FNG: se muestra en la oferta (costo total ~18,5 % E.A., supuesto del modelo).
FIXES = {
    "2d4d0f04-acc3-449a-9a83-4d8549d435c4": [
        ("$298.000", "$277.000", 1),
        ("La comisión de garantía se muestra al firmar.",
         "Con la comisión de la garantía pública (FNG), que pagas tú, el costo total es cerca de 18,5 % E.A.", 1),
    ],
    "9202b114-dc82-43a9-abed-a34861d9bbf2": [
        ("$298.000", "$277.000", 1),
        ("$447.000", "$418.000", 1),
        ("$149.000", "$138.000", 1),
    ],
    "43fbf74d-98e5-424c-b33e-10fe0035b049": [
        ("$149.000", "$138.000", 2),
    ],
    "0f906788-39ab-482b-b998-8c7e725d6740": [
        ("$348.000", "$323.000", 1),
    ],
    "f2bddd9a-dc98-41e5-ada4-339dc4a9db41": [
        ("22,5 % a 28,9 % E.A.", "22,5 % a 28,3 % E.A.", 1),
        ('<div style="font-size: 20px; font-weight: 600">50 %</div>',
         '<div style="font-size: 20px; font-weight: 600">50 %</div>'
         '<div style="font-size: 13px; color: #FFFFFF; opacity: 0.92">FNG · comisión a tu cargo; costo total ≈ 18,5 % E.A.</div>', 1),
    ],
}

def apply_fixes(uuid, tpl):
    for old, new, count in FIXES.get(uuid, []):
        found = tpl.count(old)
        if found != count:
            raise SystemExit(f"{uuid}: se esperaban {count} '{old}', hay {found}")
        tpl = tpl.replace(old, new)
    return tpl

def block(html, name):
    m = re.search(r'(<script type="__bundler/' + name + r'">\s*)(.*?)(\s*</script>)', html, re.S)
    if not m:
        raise SystemExit(f"bloque {name} no encontrado")
    return m

def main(src, out):
    here = os.path.dirname(os.path.abspath(__file__))
    css = open(os.path.join(here, "responsive.css"), encoding="utf-8").read()
    inject = ('<meta name="viewport" content="width=device-width, initial-scale=1">'
              '<style id="auro-responsive">' + css + '</style>')
    outer = open(src, encoding="utf-8").read()
    manifest = json.loads(block(outer, "manifest").group(2))
    os.makedirs(out, exist_ok=True)
    missing = set(PAGES) - set(manifest)
    if missing:
        raise SystemExit(f"faltan paginas en el export: {missing}")
    for uuid, names in PAGES.items():
        entry = manifest[uuid]
        data = base64.b64decode(entry["data"])
        if entry.get("compressed"):
            data = gzip.decompress(data)
        page = data.decode("utf-8")
        m = block(page, "template")
        tpl = apply_fixes(uuid, json.loads(m.group(2)))
        tpl = re.sub(r"(<head[^>]*>)", lambda h: h.group(1) + inject, tpl, count=1)
        enc = json.dumps(tpl, ensure_ascii=False).replace("</", "<\\/")
        page = page[: m.start(2)] + enc + page[m.end(2):]
        # viewport tambien en el documento cargador (antes de desempacar)
        page = page.replace('<meta charset="utf-8">',
                            '<meta charset="utf-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">', 1)
        for n in names:
            open(os.path.join(out, n), "w", encoding="utf-8").write(page)
            print("ok", n, len(page))

# Entregables publicados junto al prototipo: <site>/entregables/<nombre>
DELIVERABLES = {
    "resumen-ejecutivo-auro.pdf": "entregables/resumen-ejecutivo/resumen-ejecutivo-auro.pdf",
    "modelo-financiero-auro.xlsx": "entregables/modelo-financiero/modelo-financiero-auro.xlsx",
    "arquitectura-auro.html": "entregables/arquitectura/arquitectura-auro.html",
    "roadmap-auro.html": "entregables/roadmap/roadmap-auro.html",
    "roadmap-auro.pdf": "entregables/roadmap/roadmap-auro.pdf",
    "declaracion-uso-ia-auro.pdf": "entregables/declaracion-uso-ia/declaracion-uso-ia-auro.pdf",
}

def copy_deliverables(out):
    import shutil
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dest = os.path.join(out, "entregables")
    os.makedirs(dest, exist_ok=True)
    for name, src in DELIVERABLES.items():
        shutil.copyfile(os.path.join(root, src), os.path.join(dest, name))
        print("ok entregables/" + name)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
    copy_deliverables(sys.argv[2])
