# Auro by BFE

Propuesta para la prueba técnica **AI Product Engineer · Banca Pyme**: un banco de segundo piso (BFE, ficticio) llega directo a la pyme con **Auro**. Auro es un tesorero digital con IA, gratuito, que proyecta la caja, avisa del faltante antes de que ocurra y, si hace falta, ofrece un **cupo rotativo de fomento** dentro de esa misma solución.

**Prototipo en vivo:** https://auro-prototipo.onrender.com

## Entregables

| # | Entregable | Archivo |
|---|---|---|
| 01 | Prototipo funcional (18 pantallas, 3 caminos de excepción, responsive) | [sitio en Render](https://auro-prototipo.onrender.com) · fuente en `site/` |
| 02 | Resumen ejecutivo (2 páginas) | `entregables/resumen-ejecutivo/resumen-ejecutivo-auro.pdf` |
| 03 | Modelo financiero a 3 años (fórmulas visibles, escenarios, sensibilidad) | `entregables/modelo-financiero/modelo-financiero-auro.xlsx` |
| — | Declaración de uso de IA + anexo del proceso de diseño | `entregables/declaracion-uso-ia/declaracion-uso-ia-auro.pdf` |
| — | Arquitectura agéntica y de la solución | `entregables/arquitectura/arquitectura-auro.html` (fuente `.md`) |

Antes de enviar el modelo financiero, ábrelo en Excel y guárdalo una vez. El archivo trae las fórmulas pero no los resultados calculados; al guardarlo en Excel, las cifras quedan visibles también en vistas previas y en Google Sheets.

## Recorrido del prototipo

**Recorrido principal:** Landing → Registro con NIT → Inicio la primera vez (carga de información) → Fuentes de datos → Inicio con alerta de faltante → Cupo preaprobado → Activación con 7 controles → Uso del cupo y desembolso → Plan del próximo mes.

**Caminos de excepción** (a un clic desde el menú):
- **A · Anomalía en documentos:** Auro ayuda a corregirla o pasa el caso a una analista.
- **B · Uso no permitido del cupo:** incluye intentos de manipular al agente; Auro se niega y explica.
- **C · Abono programado sin pago del cliente:** no se debita nada.

## Estructura del repositorio

```
Auro by BFE · Prototipo.html   export original de Claude Design (tablero con las 18 pantallas)
tools/build_site.py            convierte el export en el sitio estático site/ y corrige cifras
tools/responsive.css           capa responsive inyectada en cada pantalla (< 860 px)
site/                          sitio publicado en Render (static site, publishPath: site)
entregables/                   resumen ejecutivo, modelo financiero, arquitectura, declaración de IA
```

**Regenerar el sitio** después de un nuevo export:

```
python tools/build_site.py "Auro by BFE · Prototipo.html" site
```

**Regenerar otros entregables:**
- Modelo financiero: `python entregables/modelo-financiero/generar_modelo.py`
- Arquitectura en HTML: `python entregables/arquitectura/build_html.py <md> <html>`
- Declaración de uso de IA: `python entregables/declaracion-uso-ia/build_pdf_html.py`, y luego imprimir el HTML a PDF.

Render despliega automáticamente desde `main`.
