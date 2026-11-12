# Auro by BFE · Prototipo

Prototipo navegable de Auro, el tesorero digital con IA del Banco de Fomento Empresarial para pymes.

- `Auro by BFE · Prototipo.html`: export original (tablero con las 18 pantallas).
- `tools/build_site.py`: convierte el tablero en un sitio estático navegable (`site/`), un archivo por pantalla con el nombre que usan sus enlaces.
- `tools/responsive.css`: capa responsive que se inyecta en cada pantalla (menos de 860px: menú superior desplazable y contenido a ancho completo).
- `site/`: sitio publicado en Render (static site, `publishPath: site`).

Reconstruir el sitio:

```
python tools/build_site.py "Auro by BFE · Prototipo.html" site
```

Recorrido principal: Landing → Registro → Inicio primera vez → Fuentes de datos → Inicio → Cupo preaprobado → Activar el cupo → Uso del cupo → Plan del próximo mes.
Caminos de falla: Anomalía en documentos, Uso no permitido del cupo, Abono sin pago del cliente.
