# Auro by BFE · cifras clave del modelo financiero

Fuente: `modelo-financiero-auro.xlsx` (todas las cifras salen de fórmulas sobre la hoja Supuestos). Fecha de corte: 12-nov-2026.
Unidades: COP M = millones de pesos. US$ al tipo de cambio del modelo (COP 3.250). Mes 1 = enero de 2027.
El caso se evalúa a 3 años (2027-2029). 2030-2031 es una **extensión indicativa** que se usa solo para el payback y el valor terminal.
Todo lo que no tiene fuente en la hoja Fuentes es un **supuesto propio que hay que validar**. Ninguna cifra es una certeza.

## Cifras por escenario

| Indicador | Pesimista | Base | Optimista |
|---|---:|---:|---:|
| Inversión inicial (año 0) | 5.000 | 4.050 (≈ US$1,25 M) | 3.450 |
| Registros acumulados en tesorería, 2029 | 9.540 | 18.420 | 21.840 |
| Usuarios activos de tesorería, 2029 | 3.173 | 8.164 | 11.978 |
| Cupos activos, dic-2029 | 452 | 2.320 | 4.268 |
| Cartera total, dic-2029 (cupo + inversión) | 9.000 | 76.470 | 188.607 |
| Ingresos netos 2027 / 2028 / 2029 | 3 / 37 / 154 | 125 / 1.365 / 4.388 | 306 / 3.514 / 11.804 |
| Margen financiero neto, 3 años | 181 | 5.712 | 15.024 |
| Pérdida esperada, 3 años | 330 | 1.294 | 1.566 |
| Costos de operación, 3 años | 15.668 | 14.125 | 13.003 |
| Costo de IA, 3 años (% de los costos de operación) | 245 (1,6 %) | 406 (2,9 %) | 463 (3,6 %) |
| Utilidad neta 2027 / 2028 / 2029 | −3.657 / −4.513 / −5.048 | −2.857 / −3.320 / −2.419 | −2.429 / −1.553 / +2.628 |
| Utilidad neta acumulada, 3 años | −13.218 | −8.596 | −1.354 |
| VPN a 3 años (sin valor terminal) | −11.564 | −11.611 | −10.638 |
| TIR a 3 años | n.a. | n.a. | n.a. |
| Extensión: utilidad neta 2030 / 2031 | −4.098 / −4.203 | +255 / +2.114 | +10.029 / +17.403 |
| Extensión: cupos activos / cartera, 2031 | 864 / 19.447 | 4.563 / 179.156 | 8.704 / 490.950 |
| VPN a 5 años con valor terminal | −32.360 | −5.721 | +96.559 |
| Payback operativo (recupera inversión y pérdidas, sin capital) | > 60 meses | > 60 meses | mes 39 (mar-2030) |
| Payback del flujo al accionista (incluye capital de la cartera) | > 60 | > 60 | > 60 |
| Necesidad máxima de caja (5 años) | −23.269 | −19.127 | −12.773 |

Supuestos de la base: tasa de política 12,0 % en 2027 → 10,5 % → 9,0 %; fondeo = política + 0,75 p.p.; Ke 14 %; capital 12 % × ponderación 60 %; impuesto 40 % en 2027 y 35 % después (las pérdidas generan escudo fiscal en el BFE).

## Cómo leer el resultado del escenario base

- **En 3 años el caso no se paga.** Es una curva J de crédito: la inversión, el equipo y la adquisición llegan antes que la cartera. La utilidad neta se vuelve positiva en 2030 y el ROE de 2031 es ≈ 19 %. El VPN a 5 años con valor terminal sigue negativo (−5,7 mil M).
- **Punto de equilibrio:** se necesitan ~3.000 cupos activos en promedio para cubrir los costos de operación de 2029 (~2.750 en 2031). Con ~1,96 M COP de margen después de riesgo por cupo y año en 2029, la base llega a 2.320 cupos a dic-2029.
- **El costo de IA no es el problema** (≈ 3 % de los costos de operación; ≈ US$8.100/mes en el mes 36). Los factores que deciden el caso son el spread de la tasa, la escala y la utilización.
- **Valor de la IA (base, 3 años):** ahorra ≈ 1.046 M COP netos en originación y soporte, más ≈ 651 M COP de margen por conversión. Eso es ≈ 4,5 × su costo en 2028-2029. El costo por cupo originado en 2029 baja de 0,64 a 0,40 M COP. El tiempo de respuesta pasa de 10 días hábiles a menos de 1 (−95 %).
- **Valor para la pyme:** 14,9 % E.A. frente al IBC de 18,89 % y la usura de 28,34 % (nov-2026). Con la comisión FNG que paga la empresa, el costo total es ≈ 18,5 %.

## Los 5 supuestos más sensibles

El tornado mide el efecto sobre el VPN a 5 años con valor terminal, en el escenario base, con un choque de ±20 %.

| # | Supuesto | Base | Rango de VPN (COP M) | Cómo se valida |
|---|---|---|---:|---|
| 1 | Tasa al cliente y spread sobre el fondeo, incluida la compensación de tasa de la línea de fomento (+2,6 p.p.) | 14,9 % + 2,6 p.p. vs. fondeo 12,75 % | 25.493 (−12.898 / +12.595) | Decisión de tesorería y MinCIT antes del mes 1; prueba de precio en el piloto |
| 2 | Utilización promedio del cupo | 45 % | 11.294 | Saldo/cupo a 90 días por cohorte (umbral ≥ 30 %) |
| 3 | Conversión de preaprobado a cupo | 45 % al mes siguiente + 2 %/mes después | 8.631 | A/B de la alerta de hueco con oferta (umbral ≥ 25 % en 60 días) |
| 4 | Pérdida esperada (PD 4,5 %, LGD 55 %, garantía 50 %) | ≈ 1,2 % de la EAD al año | 4.203 | Backtesting con facturas y centrales; mora 30+ a 6 meses ≤ 3 % |
| 5 | CAC por registro | COP 150.000 | 2.809 | Tres canales en el piloto; ≤ COP 400.000 por usuario activo |

El costo de IA (±20 %) mueve el VPN solo ±426 M COP.

## Mensaje para el comité

Hay que aprobar el piloto de 6 meses, no la escala. La inversión inicial es de COP 4.050 M y tiene compuertas. Para escalar, deben cumplirse tres condiciones:

1. Spread de al menos ≈ 4 p.p. sobre el fondeo, con compensación de tasa o con la tasa indexada a IBR.
2. Utilización de al menos 30 %.
3. Conversión a cupo de al menos 25 %.

Sin la compensación de tasa (`subsidio_fondeo` = 0), el spread de 2027 cae a ≈ 2,2 p.p. El VPN a 5 años con valor terminal de la base pasa de −5.721 a ≈ −18.200 M COP, y la utilidad neta acumulada a 3 años, de −8.596 a ≈ −9.755 M COP. Para verlo, cambie `subsidio_fondeo` en la hoja Supuestos; esta corrida no hace parte del tornado.
