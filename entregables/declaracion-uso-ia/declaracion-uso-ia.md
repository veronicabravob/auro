# Declaración de uso de IA

**Propuesta:** Auro by BFE · Prueba técnica AI Product Engineer · Banca Pyme

## Herramientas y uso

| Herramienta | Para qué la usé |
|---|---|
| **Claude Design** (Anthropic) | Investigación de mercado y referentes; opciones de segmento, producto, nombre, personalidad, paleta, logo y tipografía; redacción de textos; construcción de las 18 pantallas del prototipo. |
| **Claude Code** con Claude Opus 5.5 (Anthropic) | Revisión del prototipo contra la rúbrica; conversión del export a un sitio navegable y responsive; pruebas automáticas de enlaces y caminos de excepción; despliegue en Render. También coordiné con esta herramienta dos agentes: uno para la arquitectura agéntica y otro para el modelo financiero. |
| **Búsqueda web** (desde Claude) | Datos de mercado y normativa colombiana. Cada cifra o norma se cita con su fuente en el modelo financiero y en la arquitectura. |

## Qué decidí yo y qué hizo la IA

**Decidí yo:**
- El problema y el segmento: el segmento lo propuso la IA y lo acepté después de cuestionarlo.
- El producto: tesorero gratuito con cupo de fomento.
- Las restricciones: 100 % digital, software propio y sin competir con el software contable.
- La marca y el flujo de la experiencia.
- Los límites del agente: no aprueba créditos, no fija montos ni tasas, no mueve dinero sin aprobación, y pasa el caso a una persona ante anomalías.

**Hizo la IA:** investigó, propuso alternativas, redactó, diseñó y construyó, siempre bajo mi revisión.

El detalle está en el anexo *Proceso de diseño con IA*.

## Cómo verifiqué el trabajo de la IA

- **Prototipo:**
  - Prueba automática de los 180 enlaces de las 18 pantallas.
  - Recorrido de los tres caminos de excepción.
  - Revisión a 390, 768 y 1440 px de ancho.
- **Cifras y normas:** cada una lleva su fuente y se marca como verificada o como supuesto. Las inconsistencias detectadas se corrigieron o quedaron declaradas.
- **Supuestos críticos:** no se presentan como certezas. Tienen un plan de validación en el modelo financiero.

## Límites conocidos

- Los datos del prototipo son de ejemplo y las conexiones son simuladas.
- Los precios de los modelos de IA y algunas normas (mecanismo de consentimiento de finanzas abiertas, acceso a RADIAN) deben confirmarse con el banco y sus proveedores antes del piloto.
