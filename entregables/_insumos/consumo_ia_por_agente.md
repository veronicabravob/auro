# Consumo de IA por agente · Auro by BFE

Insumo para el modelo financiero (costos de IA). Fuente: `entregables/arquitectura/arquitectura-auro.md`, sección 12.
Todas las cifras de volumen son **supuestos de diseño** a validar con el piloto (telemetría real de tokens por agente).

## Precios usados (API de Anthropic, tarifa de primera parte, noviembre de 2026)

| Modelo | Entrada US$/M tokens | Salida US$/M tokens | Lectura de caché US$/M tokens |
|---|---|---|---|
| `claude-opus-5-5` | 4,00 | 20,00 | 0,20 |
| `claude-sonnet-5-5` | 2,00 | 10,00 | 0,10 |
| `claude-haiku-5-5` | 0,10 | 0,50 | 0,005 (supuesto: 5 % del precio de entrada, igual que los otros dos) |

Supuestos de cálculo:
- 60 % de los tokens de entrada de cada llamada es prefijo estable (instrucciones del agente, definición de herramientas, políticas) que se lee de caché. El costo de escritura de caché se ignora (se amortiza en muchas llamadas).
- Los tokens de razonamiento (thinking adaptativo) están incluidos en los tokens de salida estimados.
- Las facturas electrónicas en XML (UBL de la DIAN) y los extractos que lleguen por API se procesan con parsers determinísticos: **0 tokens**. Solo los PDF, fotos y archivos sin estructura pasan por un modelo.
- La proyección de caja, el preaprobado, los intereses y los controles numéricos los calcula código determinístico; los agentes solo los explican.
- No incluye descuentos por Batch API (50 %) que aplicarían a la corrida nocturna; ver "Optimización" abajo.
- TRM de referencia: COP 4.000 por US$ (supuesto).

Perfiles de cliente:
- **N1**: pyme activa en Auro solo con tesorería (Nivel 1, sin cupo).
- **N2**: pyme con cupo activo (Nivel 2).
- **Onboarding** (una vez por empresa): registro, conexión de fuentes y primera proyección.
- **Activación del cupo** (una vez por solicitud): 5 pasos, 7 controles y eventual anomalía.

## Tabla principal

| Agente | Modelo | Evento | Llamadas por evento | Tokens entrada por llamada | Tokens salida por llamada | Eventos por cliente por mes (N1) | Eventos por cliente por mes (N2) | Eventos únicos onboarding | Eventos únicos activación del cupo |
|---|---|---|---|---|---|---|---|---|---|
| Guardia de entrada (clasificador de mensajes) | `claude-haiku-5-5` | Mensaje del cliente | 1 | 1.200 | 60 | 10 | 25 | 15 | 15 |
| Orquestador | `claude-sonnet-5-5` | Turno de conversación | 2 | 7.000 | 350 | 10 | 25 | 15 | 15 |
| Datos y caja · resumen nocturno y alertas | `claude-sonnet-5-5` | Corrida nocturna con cambios (días hábiles) | 1 | 9.000 | 700 | 22 | 22 | 1 | 0 |
| Datos y caja · extracción de documentos no estructurados | `claude-haiku-5-5` | Documento PDF o foto | 1 | 2.500 | 400 | 10 | 10 | 40 | 0 |
| Vinculación y cumplimiento (KYC/SARLAFT) | `claude-sonnet-5-5` | Paso de control | 1,5 | 6.000 | 600 | 0 | 0,1 | 1 | 7 |
| Validación documental · extracción y conciliación | `claude-sonnet-5-5` | Documento de la solicitud (RUT, EEFF, extracto) | 1 | 14.000 | 1.200 | 0 | 1 | 0 | 10 |
| Validación documental · investigación de anomalía | `claude-opus-5-5` | Expediente con alerta (25 % de solicitudes, supuesto) | 4 | 25.000 | 2.000 | 0 | 0,05 | 0 | 0,25 |
| Uso del cupo y pagos | `claude-sonnet-5-5` | Propuesta de uso o de abono | 3 | 7.000 | 500 | 0 | 3 | 0 | 0 |
| Acompañamiento y acciones (tesorero) | `claude-sonnet-5-5` | Plan semanal o mensual | 3 | 12.000 | 1.200 | 4 | 5 | 1 | 0 |
| Redactor de mensajes | `claude-haiku-5-5` | Borrador (incluye cambio de tono) | 2 | 3.000 | 500 | 3 | 4 | 0 | 0 |
| Copiloto de analista (interno) | `claude-opus-5-5` | Caso transferido a una persona | 2 | 30.000 | 2.500 | 0,01 | 0,03 | 0 | 0,2 |
| Evaluador en línea (LLM como juez, muestra 5 %) | `claude-sonnet-5-5` | Interacción muestreada | 1 | 8.000 | 300 | 1 | 2,5 | 1 | 2 |

## Totales por cliente

| Perfil | Tokens entrada | Tokens salida | US$ sin caché | US$ con caché (60 %) | COP con caché |
|---|---|---|---|---|---|
| N1 · por cliente por mes | 545.600 | 44.750 | 1,36 | 0,80 | 3.200 |
| N2 · por cliente por mes | 911.700 | 67.490 | 2,28 | 1,32 | 5.260 |
| Onboarding · una vez por empresa | 390.000 | 32.900 | 0,72 | 0,41 | 1.630 |
| Activación del cupo · una vez por solicitud | 484.000 | 33.300 | 1,36 | 0,79 | 3.150 |

Costo por agente con caché (US$ por cliente por mes): orquestador 0,19 (N1) / 0,48 (N2); resumen nocturno 0,32 / 0,32; acompañamiento 0,27 / 0,34; uso del cupo 0 / 0,10; evaluador 0,01 / 0,03; el resto suma menos de 0,04.

## Ejemplo de escala (para el modelo financiero)

Con 1.000 empresas N1 y 300 N2 en un mes, 150 onboardings y 60 solicitudes de cupo:
1.000 × 0,80 + 300 × 1,32 + 150 × 0,41 + 60 × 0,79 ≈ **US$ 1.305 por mes** (≈ COP 5,2 millones), unos 907 millones de tokens de entrada (60 % desde caché) y 72 millones de salida.

## Optimización y sensibilidad

- Corrida nocturna por Batch API: −50 % en esa línea (≈ −0,16 US$ por cliente por mes).
- Pasar el resumen nocturno a `claude-haiku-5-5` solo cuando no cambie el hueco proyectado: −0,25 US$ por cliente por mes, a validar con evals de calidad.
- Sensibilidad: si los turnos de conversación se duplican (N2 = 50 mensajes), el costo N2 sube a ≈ 1,82 US$; si la tasa de anomalías es 50 % en vez de 25 %, la activación sube a ≈ 0,83 US$.
- Costo no incluido: infraestructura (cómputo, almacenamiento, bitácora WORM), proveedor de biometría, consultas a centrales y listas, y red teaming externo. Esos van en otras líneas del modelo.
