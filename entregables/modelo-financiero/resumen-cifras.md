# Auro by BFE · cifras clave del modelo financiero (roadmap acelerado)

Fuente: `modelo-financiero-auro.xlsx`. Todas las cifras salen de fórmulas sobre la hoja Supuestos; el archivo se regenera con `generar_modelo.py`. Fecha de corte: 12-nov-2026.

**Unidades.** COP M = millones de pesos. Los montos en US$ usan el tipo de cambio del modelo (COP 3.250). Mes 1 = enero de 2027.

**Horizonte.** El caso se evalúa a 3 años (2027-2029). 2030-2031 es una **extensión indicativa** que solo se usa para el payback y el valor terminal.

**Roadmap acelerado.** El calendario se edita en Supuestos (`mes_ini_tes`, `mes_ini_cupo`, `mes_ini_uso`):

| Hito | Mes |
|---|---|
| Construcción | ~10 personas × 3 meses, con desarrollo asistido por IA |
| Tesorería en piloto | Mes 1 |
| Preaprobado y activación del cupo | Mes 2 |
| Uso del cupo y abono con mandato | Mes 3 |
| Medición de cohortes | Meses 4-6 |

Todo lo que no tiene fuente en la hoja Fuentes es un **supuesto propio por validar**. Ninguna cifra es una certeza.

## Cifras por escenario

| Indicador | Pesimista | Base | Optimista |
|---|---:|---:|---:|
| Inversión inicial (año 0) | 3.800 | 2.950 (≈ US$0,91 M) | 2.500 |
| — de la cual, desarrollo (3 meses) | 1.400 | 1.100 | 950 |
| Registros acumulados en tesorería, 2029 | 9.540 | 18.420 | 21.840 |
| Usuarios activos de tesorería, 2029 | 3.173 | 8.164 | 11.978 |
| Cupos activos, dic-2029 | 452 | 2.320 | 4.268 |
| Cartera total, dic-2029 (cupo + inversión) | 9.000 | 76.470 | 188.607 |
| Ingresos netos 2027 / 2028 / 2029 | 2 / 37 / 154 | 124 / 1.365 / 4.388 | 304 / 3.514 / 11.804 |
| Margen financiero neto, 3 años | 181 | 5.711 | 15.021 |
| Pérdida esperada, 3 años | 330 | 1.294 | 1.566 |
| Costos de operación, 3 años | 15.668 | 14.125 | 13.003 |
| Costo de IA, 3 años (% de los costos de operación) | 245 (1,6 %) | 406 (2,9 %) | 463 (3,6 %) |
| Utilidad neta 2027 / 2028 / 2029 | −3.417 / −4.253 / −4.788 | −2.637 / −3.082 / −2.181 | −2.241 / −1.347 / +2.834 |
| Utilidad neta acumulada, 3 años | −12.458 | −7.900 | −754 |
| VPN a 3 años (sin valor terminal) | −10.696 | −10.825 | −9.965 |
| TIR a 3 años | n.a. | n.a. | n.a. |
| Flujo acumulado al accionista, dic-2029 | −13.268 | −13.406 | −12.070 |
| Extensión: utilidad neta 2030 / 2031 | −4.098 / −4.203 | +255 / +2.114 | +10.029 / +17.403 |
| Extensión: cupos activos / cartera, 2031 | 864 / 19.447 | 4.563 / 179.156 | 8.704 / 490.950 |
| Extensión: ROE 2031 | negativo | 19,2 % | 70,7 % |
| VPN a 5 años sin valor terminal | −15.444 | −13.676 | −4.812 |
| VPN a 5 años con valor terminal | −31.492 | −4.935 | +97.232 |
| Payback operativo (recupera inversión y pérdidas, sin capital) | > 60 meses | > 60 meses | mes 38 (feb-2030) |
| Payback del flujo al accionista (incluye capital de la cartera) | > 60 | > 60 | > 60 |
| Necesidad máxima de caja (5 años) | −22.509 | −18.430 | −12.173 |

**Punto de equilibrio (base).** Son los cupos activos promedio que hacen falta para cubrir los costos de operación de cada año:

| Año | 2027 | 2028 | 2029 | 2030 | 2031 |
|---|---:|---:|---:|---:|---:|
| Cupos de equilibrio | ~3.510 | ~3.340 | ~2.990 | ~2.780 | ~2.730 |
| Margen después de riesgo por cupo-año (M COP) | — | — | 1,96 | 2,3 | 2,4 |

La base cierra 2029 con 2.320 cupos activos.

**Supuestos de la base:**
- Tasa de política: 12,0 % en 2027, 10,5 % en 2028 y 9,0 % en 2029.
- Fondeo = tasa de política + 0,75 p.p.
- Compensación de tasa de la línea de fomento: +2,6 p.p.
- Ke: 14 %.
- Capital: 12 % × ponderación de 60 %.
- Impuesto: 40 % en 2027 y 35 % después. Las pérdidas generan escudo fiscal en el BFE.

## Qué cambió con el roadmap acelerado

Base, frente a la versión anterior de 6 meses de construcción:

| Indicador | Antes | Ahora |
|---|---:|---:|
| Inversión inicial | 4.050 | 2.950 (−1.100) |
| Utilidad neta acumulada, 3 años | −8.596 | −7.900 |
| VPN a 3 años | −11.611 | −10.825 |
| VPN a 5 años con valor terminal | −5.721 | −4.935 |
| Necesidad máxima de caja | −19.127 | −18.430 |

Mover el uso del cupo al mes 3 casi no cambia los ingresos (2027: 124 frente a 125). La cartera del piloto es pequeña: el efecto del calendario está en la **velocidad para aprender**, no en el P&G.

## Cómo leer el resultado del escenario base

- **En 3 años el caso no se paga.** Es una curva J de crédito: la inversión, el equipo y la adquisición llegan antes que la cartera.
  - La utilidad neta se vuelve positiva en 2030.
  - El ROE de 2031 es 19 %.
  - El VPN a 5 años con valor terminal sigue negativo (−4,9 mil M).
- **El costo de IA no es el problema.** Es ≈ 3 % de los costos de operación, ≈ US$8.100 al mes en el mes 36. Lo que decide el caso es el spread de la tasa, la escala y la utilización.
- **Valor de la IA (base, 3 años).**
  - Ahorro neto en originación y soporte: ≈ 1.046 M COP.
  - Margen por conversión: ≈ 651 M COP.
  - Valor total: ≈ 1.697 M COP, unas 4,5 veces su costo en 2028-2029.
  - Costo por cupo originado en 2029: 0,40 M COP con agentes frente a 0,64 M COP sin ellos.
  - Tiempo de respuesta: de 10 días hábiles a 0,5 (−95 %).
- **Valor para la pyme.** Paga 14,9 % E.A., frente al IBC de 18,89 % y la usura de 28,34 % (nov-2026). Con la comisión FNG, que paga la empresa, el costo total es ≈ 18,5 %.

## Los 5 supuestos más sensibles

El tornado mide el efecto sobre el VPN a 5 años con valor terminal, en el escenario base, con un choque de ±20 %.

| # | Supuesto | Base | Rango de VPN (COP M) | Cómo se valida |
|---|---|---|---:|---|
| 1 | Tasa al cliente y spread sobre el fondeo, incluida la compensación de tasa (+2,6 p.p.) | 14,9 % + 2,6 p.p. vs. fondeo de 12,75 % | 25.492 (−12.898 / +12.595) | Decisión de tesorería y MinCIT antes del mes 1; prueba de precio en el piloto |
| 2 | Utilización promedio del cupo | 45 % | 11.294 | Saldo/cupo de las primeras cohortes (umbral ≥ 30 %), meses 3-6 |
| 3 | Conversión de preaprobado a cupo | 45 % al mes siguiente + 2 %/mes después | 8.631 | A/B de la alerta de hueco con oferta (umbral ≥ 25 % en 60 días), meses 2-6 |
| 4 | Pérdida esperada (PD 4,5 %, LGD 55 %, garantía 50 %) | ≈ 1,2 % de la EAD al año | 4.203 | Backtesting en los meses 1-2; indicador temprano en los meses 3-6: mora 30+ observada ≤ 3 % y ≥ 95 % de los primeros usos pagados a tiempo. La mora 30+ a 6 meses se sigue después de escalar (meses 8-12) |
| 5 | CAC por registro | COP 150.000 | 2.809 | Tres canales en el piloto; ≤ COP 400.000 por usuario activo |

El sexto factor del tornado, el costo de IA (±20 %), mueve el VPN solo ±426 M COP (rango de 852).

**Sin compensación de tasa** (`subsidio_fondeo` = 0), en el escenario base:

| Indicador | Con compensación | Sin compensación |
|---|---:|---:|
| Spread sobre el fondeo, 2027 | — | ≈ 2,2 p.p. |
| VPN a 5 años con valor terminal | −4.935 | ≈ −17.400 |
| VPN a 5 años sin valor terminal | −13.676 | ≈ −16.240 |
| Utilidad neta acumulada, 3 años | −7.900 | ≈ −9.060 |

## Mensaje para el comité

Hay que aprobar el piloto de 6 meses, no la escala. La inversión inicial es de COP 2.950 M y tiene compuertas. Con el roadmap acelerado, la conversión a cupo y la utilización ya se observan entre los meses 2 y 6. Para escalar se exigen tres condiciones:

1. Un spread de al menos ≈ 4 p.p. sobre el fondeo, con compensación de tasa o con la tasa indexada a IBR.
2. Una utilización de al menos 30 %.
3. Una conversión a cupo de al menos 25 %.

Además, el indicador temprano de riesgo debe cumplirse: mora 30+ ≤ 3 % y ≥ 95 % de los primeros usos pagados a tiempo.
