# -*- coding: utf-8 -*-
"""Genera modelo-financiero-auro.xlsx (todas las cifras calculadas son fórmulas)."""
import re, sys, os
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.comments import Comment

OUT = sys.argv[1] if len(sys.argv) > 1 else "modelo-financiero-auro.xlsx"

FONT = "Arial"
BLUE = Font(name=FONT, color="0000FF", size=10)
BLACK = Font(name=FONT, color="000000", size=10)
GREEN = Font(name=FONT, color="008000", size=10)
BOLD = Font(name=FONT, bold=True, size=10)
TITLE = Font(name=FONT, bold=True, size=14, color="1F3864")
SUB = Font(name=FONT, bold=True, size=11, color="1F3864")
HDR_FILL = PatternFill("solid", fgColor="1F3864")
HDR_FONT = Font(name=FONT, bold=True, color="FFFFFF", size=10)
SEC_FILL = PatternFill("solid", fgColor="D9E1F2")
YELLOW = PatternFill("solid", fgColor="FFFF00")
KEY_FILL = PatternFill("solid", fgColor="FFF2CC")
WRAP = Alignment(wrap_text=True, vertical="top")
thin = Side(style="thin", color="BFBFBF")
BOX = Border(top=thin, bottom=thin, left=thin, right=thin)

FMT = {
    "pct": '0.0%;(0.0%);"-"',
    "pct2": '0.00%;(0.00%);"-"',
    "int": '#,##0;(#,##0);"-"',
    "num1": '#,##0.0;(#,##0.0);"-"',
    "num2": '#,##0.00;(#,##0.00);"-"',
    "copm": '#,##0.0;(#,##0.0);"-"',
    "cop": '#,##0;(#,##0);"-"',
    "usd": '0.000;(0.000);"-"',
    "x": '0.0"x"',
}

FIRST_M_COL = 3            # C
NM = 60
LAST_M_COL = FIRST_M_COL + NM - 1   # BJ (62)
YCOL = {1: 64, 2: 65, 3: 66, 4: 67, 5: 68}   # BL..BP
TCOL = 69                           # BQ: total 3 años (horizonte del caso)
T5COL = 70                          # BR: total 5 años (extensión indicativa)
YEARS = {1: "2027", 2: "2028", 3: "2029", 4: "2030", 5: "2031"}
MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]


def month_of_col(c):
    return c - FIRST_M_COL + 1


def year_of_month(m):
    return (m - 1) // 12 + 1


# ---------------------------------------------------------------- PARÁMETROS
# (clave, etiqueta, unidad, fmt, pes, base, opt, tipo, fuente, nota, tag_sens)
S = "Supuesto propio"
V = "Verificado"
VD = "Derivado de dato verificado"
SECTIONS = []


def sec(name):
    SECTIONS.append(("SEC", name))


def p(*a):
    SECTIONS.append(("P",) + a)


sec("1. Mercado")
p("emp_activas", "Empresas activas en el registro mercantil (cierre 2025)", "empresas", "int", 1805564, 1805564, 1805564, V, "F01", "RUES vía INCP/Radio Nacional. Incluye personas naturales y jurídicas.", "")
p("pequenas", "Pequeñas empresas (Confecámaras, 2023)", "empresas", "int", 106120, 106120, 106120, V, "F02", "Último conteo por tamaño encontrado; Confecámaras 2025 da 4,2 % pequeñas (F22): dato a reconciliar con RUES.", "")
p("medianas", "Medianas empresas (Confecámaras, 2023)", "empresas", "int", 27238, 27238, 27238, V, "F02", "", "")
p("pct_b2b", "Pymes que venden a plazo a otras empresas", "%", "pct", 0.50, 0.60, 0.65, S, "F20", "Sin dato oficial; validar con Encuesta MiPyme Anif (módulo de financiación) y con datos de RADIAN.", "")
p("pct_fe", "Pymes que facturan electrónicamente (lectura posible de facturas)", "%", "pct", 0.90, 0.95, 0.98, VD, "F04", "DIAN: ~1,16-1,32 M facturadores habilitados (2025); obligación general para personas jurídicas.", "")
p("pct_manuf", "Participación de manufactura en pequeñas empresas (segmento de entrada)", "%", "pct", 0.12, 0.13, 0.14, S, "F03", "Aproximación al peso de la industria en el registro mercantil; confirmar con RUES por CIIU.", "")
p("pct_sin_credito", "Pymes sin acceso a crédito formal (brecha)", "%", "pct", 0.60, 0.60, 0.60, VD, "F05", "Anif (vía Portafolio): solo 40 % de las pymes ha accedido a crédito formal.", "")
p("ibc_nov26", "Interés bancario corriente consumo y ordinario, nov-2026", "% E.A.", "pct2", 0.1889, 0.1889, 0.1889, V, "F06", "Res. SFC 1707 de 2026. Referencia de mercado para crédito ordinario.", "")
p("usura_nov26", "Tasa de usura consumo y ordinario, nov-2026", "% E.A.", "pct2", 0.2834, 0.2834, 0.2834, V, "F06", "1,5 × IBC. Techo legal.", "")
p("usura_oct26", "Tasa de usura consumo y ordinario, oct-2026", "% E.A.", "pct2", 0.2859, 0.2859, 0.2859, V, "F07", "Res. SFC 1472 de 2026. El prototipo cita rotativos hasta 28,9 % en octubre: por encima de este techo.", "")

sec("2. Embudo (funnel)")
p("reg_p1", "Registros nuevos por mes · piloto cerrado (meses 1-6)", "empresas/mes", "int", 40, 70, 90, S, "F20", "Piloto con gremio manufacturero y un software contable aliado.", "")
p("reg_p2", "Registros nuevos por mes · apertura (meses 7-12)", "empresas/mes", "int", 150, 300, 350, S, "", "", "")
p("reg_y2", "Registros nuevos por mes · 2028", "empresas/mes", "int", 300, 600, 700, S, "", "Incluye ampliación a otros sectores B2B que venden a plazo.", "")
p("reg_y3", "Registros nuevos por mes · 2029", "empresas/mes", "int", 400, 750, 900, S, "", "", "")
p("reg_y4", "Registros nuevos por mes · 2030 (extensión)", "empresas/mes", "int", 400, 750, 900, S, "", "Años 4-5 solo para payback y valor terminal.", "")
p("reg_y5", "Registros nuevos por mes · 2031 (extensión)", "empresas/mes", "int", 400, 750, 900, S, "", "", "")
p("pct_activacion", "Registros que conectan 12 meses de facturas (activan tesorería)", "%", "pct", 0.50, 0.60, 0.70, S, "F20", "Prototipo: conexión Siigo/Alegra, buzón o listado DIAN.", "")
p("churn", "Abandono mensual de usuarios activos de tesorería", "%/mes", "pct", 0.035, 0.025, 0.02, S, "", "", "")
p("pct_preaprob", "Activos que obtienen preaprobado (pasan reglas de política)", "%", "pct", 0.40, 0.50, 0.55, S, "F20", "Política de crédito del BFE (reglas + modelo). La pyme llega con un hueco de caja: autoselección.", "")
p("conv_inicial", "Preaprobados que solicitan el cupo al mes siguiente", "%", "pct", 0.30, 0.45, 0.50, S, "", "Detonante: alerta de hueco de caja (prototipo).", "conv")
p("conv_tardia", "Preaprobados pendientes que solicitan el cupo cada mes después", "%/mes", "pct", 0.01, 0.02, 0.025, S, "", "", "conv")
p("aprob_valid", "Solicitudes que superan los 7 controles y se activan", "%", "pct", 0.80, 0.88, 0.92, S, "F20", "Incluye anomalías aclaradas por la empresa o por analista.", "")
p("attr_cupos", "Cupos que se cancelan o castigan cada mes", "%/mes", "pct", 0.015, 0.010, 0.007, S, "", "", "")
p("cupo_prom", "Cupo aprobado promedio", "COP M", "copm", 50, 60, 65, S, "F20", "Prototipo: hasta $60 M para ventas de $2.410 M/año (~2,5 % de ventas).", "")
p("utilizacion", "Utilización promedio del cupo (saldo / cupo)", "%", "pct", 0.35, 0.45, 0.50, S, "", "Uso para nómina y proveedores, con abonos al cobrar (rotativo).", "util")

sec("3. Precio, fondeo y garantía")
p("tasa_cliente", "Tasa del cupo al cliente (Línea Manufactura Productiva)", "% E.A.", "pct2", 0.149, 0.149, 0.149, S, "F20", "Valor de ejemplo del prototipo; no incluye comisión FNG.", "tasa")
p("tasa_pol_2027", "Tasa de política monetaria promedio 2027", "% E.A.", "pct2", 0.1225, 0.1200, 0.1150, VD, "F08", "BanRep 12,25 % (oct-2026). BBVA Research: estable hasta sep-2027 y luego recortes graduales.", "")
p("tasa_pol_2028", "Tasa de política monetaria promedio 2028", "% E.A.", "pct2", 0.1150, 0.1050, 0.0950, S, "F08", "Senda propia consistente con recortes graduales desde sep-2027.", "")
p("tasa_pol_2029", "Tasa de política monetaria promedio 2029", "% E.A.", "pct2", 0.1050, 0.0900, 0.0800, S, "F08", "", "")
p("tasa_pol_2030", "Tasa de política monetaria promedio 2030 (extensión)", "% E.A.", "pct2", 0.1000, 0.0850, 0.0750, S, "F08", "", "")
p("tasa_pol_2031", "Tasa de política monetaria promedio 2031 (extensión)", "% E.A.", "pct2", 0.1000, 0.0850, 0.0750, S, "F08", "", "")
p("spread_fondeo", "Margen del costo de fondeo del BFE sobre la tasa de política", "p.p.", "pct2", 0.0125, 0.0075, 0.0050, S, "F09", "Referencia: Bancóldex presta a intermediarios a IBR + 1,50-1,95 %; el fondeo propio de un banco de desarrollo es menor.", "")
p("subsidio_fondeo", "Compensación de tasa de la línea de fomento (recursos MinCIT u otros)", "p.p.", "pct2", 0.010, 0.026, 0.026, S, "F20", "Base = 17,5 % (línea Pyme General del prototipo) − 14,9 %: la línea Manufactura Productiva rinde al BFE lo mismo que la general. Decisión pendiente del BFE: sin compensación el margen se reduce a ~2 p.p. en 2027.", "")
p("fng_tarifa", "Comisión anual FNG, cobertura 50 % (antes de IVA)", "% anual", "pct2", 0.044, 0.030, 0.0215, VD, "F10", "Tarifas FNG vía Banco Serfinanza: EMP 080 2,15 %; EMP 309 3,89 %; EMP 214 4,40 % (+IVA).", "")
p("iva", "IVA sobre la comisión FNG", "%", "pct", 0.19, 0.19, 0.19, V, "F10", "", "")
p("pct_fng_bfe", "Parte de la comisión FNG que asume el BFE", "%", "pct", 0.5, 0.0, 0.0, S, "F20", "Base: la paga la empresa (el prototipo la muestra al firmar). Pesimista: el BFE asume la mitad para competir.", "")
p("cobertura", "Cobertura de la garantía pública", "%", "pct", 0.50, 0.50, 0.50, V, "F20", "Prototipo: garantía pública 50 %.", "")

sec("4. Riesgo de crédito (pérdida esperada = PD × LGD × EAD)")
p("pd", "Probabilidad de incumplimiento a 12 meses (PD)", "% anual", "pct2", 0.07, 0.045, 0.03, S, "F11", "Cartera comercial con mora 3,1 % (may-2026) es un indicador de saldo, no una PD de pequeñas empresas nuevas. Se usa una PD mayor.", "pd")
p("lgd", "Pérdida dado el incumplimiento antes de garantía (LGD)", "%", "pct", 0.65, 0.55, 0.45, S, "F19", "Crédito sin garantía real; recuperación por cobro jurídico.", "")
p("ccf", "Factor de conversión del cupo no utilizado (CCF)", "%", "pct", 0.30, 0.30, 0.30, S, "F19", "", "")

sec("5. Cross-sell: crédito de inversión (Nivel 3)")
p("tasa_grad", "Cupos con 6+ meses que toman crédito de inversión cada mes", "%/mes", "pct2", 0.003, 0.006, 0.010, S, "F20", "Ruta de niveles del prototipo (6 meses al día).", "")
p("monto_inv", "Monto promedio del crédito de inversión", "COP M", "copm", 120, 150, 180, S, "", "", "")
p("plazo_inv", "Plazo del crédito de inversión", "meses", "int", 36, 36, 36, S, "", "", "")
p("tasa_inv", "Tasa del crédito de inversión", "% E.A.", "pct2", 0.155, 0.155, 0.155, S, "", "", "")
p("com_estr", "Comisión de estructuración del crédito de inversión", "% del monto", "pct", 0.01, 0.01, 0.01, S, "", "", "")

sec("6. Inversión inicial (año 0, nov-2026 a dic-2026, y primeros desarrollos)")
p("inv_desarrollo", "Desarrollo de producto, agentes y app", "COP M", "copm", 2600, 2200, 1900, S, "", "Equipo de 10 personas × 6 meses + licencias.", "")
p("inv_integraciones", "Integraciones (software contable, DIAN/RADIAN, RUES, centrales, biometría, core de crédito)", "COP M", "copm", 1000, 800, 650, S, "", "", "")
p("inv_compliance", "Cumplimiento, legal y riesgo (SARLAFT, datos personales, modelo de riesgo, políticas)", "COP M", "copm", 600, 450, 400, S, "", "", "")
p("inv_seguridad", "Seguridad, red teaming y evals de agentes", "COP M", "copm", 400, 300, 250, S, "", "", "")
p("inv_lanzamiento", "Marca, lanzamiento y alianzas", "COP M", "copm", 400, 300, 250, S, "", "", "")

sec("7. Personas (costo mensual cargado = salario × factor prestacional)")
p("costo_tech", "Costo cargado por persona · producto y tecnología", "COP M/mes", "copm", 17, 16, 15, S, "F16", "", "")
p("costo_gerencia", "Costo cargado por persona · gerencia de línea y riesgo", "COP M/mes", "copm", 30, 28, 26, S, "F16", "", "")
p("costo_analista", "Costo cargado por persona · analista de crédito", "COP M/mes", "copm", 7.5, 7.0, 6.5, VD, "F16", "Ofertas 2026: $3,5-4,5 M/mes de salario × 1,55 de carga.", "")
p("costo_cump", "Costo cargado por persona · cumplimiento (SARLAFT)", "COP M/mes", "copm", 9.5, 9.0, 8.5, S, "F16", "", "")
p("costo_soporte", "Costo cargado por persona · soporte a clientes", "COP M/mes", "copm", 4.8, 4.5, 4.2, VD, "F16", "Salario ~$2,9 M × 1,55 (mínimo 2026: $1.750.905).", "")
p("fte_tech_2027", "Personas de producto y tecnología · 2027", "FTE", "num1", 7, 6, 6, S, "", "", "")
p("fte_tech_2028", "Personas de producto y tecnología · 2028", "FTE", "num1", 7, 6, 6, S, "", "", "")
p("fte_tech_2029", "Personas de producto y tecnología · 2029", "FTE", "num1", 8, 7, 7, S, "", "", "")
p("fte_tech_2030", "Personas de producto y tecnología · 2030 (extensión)", "FTE", "num1", 8, 7, 7, S, "", "", "")
p("fte_tech_2031", "Personas de producto y tecnología · 2031 (extensión)", "FTE", "num1", 8, 7, 7, S, "", "", "")
p("fte_gerencia", "Gerencia de línea, riesgo y modelos", "FTE", "num1", 3, 2, 2, S, "", "", "")
p("pct_rev_humana", "Solicitudes que revisa una persona (anomalía no aclarada, >$100 M, pedido del cliente)", "%", "pct", 0.25, 0.18, 0.12, S, "F20", "", "")
p("muestreo", "Cupos activos revisados por muestreo cada mes", "%/mes", "pct", 0.02, 0.02, 0.02, S, "F20", "Muestra mensual del prototipo.", "")
p("prod_ia", "Casos por analista al mes con copiloto (expediente pre-armado)", "casos/mes", "int", 50, 60, 75, S, "", "", "")
p("prod_sin", "Casos por analista al mes sin agentes (todo manual)", "casos/mes", "int", 25, 25, 25, S, "", "", "")
p("min_analistas", "Mínimo de analistas de crédito", "FTE", "int", 2, 2, 2, S, "", "", "")
p("cump_base", "Personas de cumplimiento fijas", "FTE", "int", 2, 2, 2, S, "", "", "")
p("ratio_cump_ia", "Solicitudes por persona de cumplimiento al mes (con agentes)", "solicitudes/mes", "int", 250, 300, 400, S, "", "", "")
p("ratio_cump_sin", "Solicitudes por persona de cumplimiento al mes (sin agentes)", "solicitudes/mes", "int", 80, 80, 80, S, "", "", "")
p("ratio_sop_ia", "Clientes activos por persona de soporte (con agentes)", "clientes", "int", 900, 1200, 1500, S, "", "", "")
p("ratio_sop_sin", "Clientes activos por persona de soporte (sin agentes)", "clientes", "int", 350, 350, 350, S, "", "", "")
p("min_soporte", "Mínimo de personas de soporte", "FTE", "int", 2, 2, 2, S, "", "", "")

sec("8. Inteligencia artificial")
p("trm", "Tasa de cambio (COP por US$)", "COP/US$", "cop", 3500, 3250, 3150, VD, "F15", "TRM 3.183-3.236 (3-5 nov-2026). El insumo de arquitectura usa 4.000: conciliar.", "")
p("cache_pct", "Tokens de entrada leídos de caché", "%", "pct", 0.40, 0.60, 0.70, S, "F14", "", "")
p("mult_ia", "Multiplicador de consumo de IA sobre el diseño (telemetría real vs. supuesto)", "x", "num2", 1.5, 1.0, 0.8, S, "F14", "1,0 = tabla de consumo por agente.", "ia")

sec("9. Infraestructura, datos de terceros y adquisición")
p("infra_fijo", "Infraestructura fija (nube, bitácora WORM, observabilidad)", "COP M/mes", "copm", 35, 25, 20, S, "", "", "")
p("infra_var", "Infraestructura variable por usuario activo", "COP/mes", "cop", 2500, 2000, 1500, S, "", "", "")
p("datos_sol", "Datos de terceros por solicitud (biometría, centrales, listas, firma)", "COP/solicitud", "cop", 45000, 35000, 30000, S, "", "Cotizar con proveedores.", "")
p("monit_cupo", "Monitoreo de centrales por cupo activo", "COP/mes", "cop", 5000, 4000, 3000, S, "", "", "")
p("cac", "Costo de adquisición por registro (marketing, gremios, contadores, software)", "COP/registro", "cop", 250000, 150000, 100000, S, "", "Tesorería gratuita distribuida por gremios, contadores y software contable; validar en piloto.", "cac")
p("com_aliado", "Comisión a aliado por cupo activado", "COP/cupo", "cop", 400000, 300000, 200000, S, "", "", "")

sec("10. Gastos generales, impuestos, capital y valoración")
p("overhead", "Gastos generales asignados (sobre personas + infraestructura)", "%", "pct", 0.15, 0.12, 0.10, S, "", "", "")
p("tax_2027", "Tarifa de renta 2027 (35 % + sobretasa financiera 5 p.p.)", "%", "pct", 0.40, 0.40, 0.40, V, "F17", "Ley 2277 de 2022: sobretasa hasta 2027.", "")
p("tax_2028", "Tarifa de renta 2028", "%", "pct", 0.35, 0.35, 0.35, V, "F17", "", "")
p("tax_2029", "Tarifa de renta 2029", "%", "pct", 0.35, 0.35, 0.35, V, "F17", "", "")
p("tax_2030", "Tarifa de renta 2030", "%", "pct", 0.35, 0.35, 0.35, V, "F17", "Supone que no cambia la norma.", "")
p("tax_2031", "Tarifa de renta 2031", "%", "pct", 0.35, 0.35, 0.35, V, "F17", "", "")
p("solvencia", "Capital asignado sobre activos ponderados (solvencia objetivo)", "%", "pct", 0.12, 0.12, 0.12, S, "", "Mínimo regulatorio total 9 % + colchones.", "")
p("ponderacion", "Ponderación por riesgo efectiva de la cartera (con garantía FNG)", "%", "pct", 0.75, 0.60, 0.50, S, "", "La parte cubierta por la garantía FNG pondera menos; validar tratamiento exacto con riesgo y regulación.", "")
p("ke", "Costo de capital (tasa de descuento, COP nominal)", "%", "pct", 0.16, 0.14, 0.13, S, "F08", "Tasa de política 12,25 % + prima; banco público de desarrollo.", "")
p("g_terminal", "Crecimiento a perpetuidad para valor terminal (nominal)", "%", "pct", 0.03, 0.04, 0.04, S, "", "Cercano a la inflación de largo plazo (meta 3 %); conservador frente al crecimiento de 2031.", "")

sec("11. Eficiencia y experiencia")
p("dias_ia", "Tiempo de respuesta a la solicitud con agentes", "días hábiles", "num1", 1, 0.5, 0.2, S, "F20", "Prototipo: activación el mismo día si los controles cumplen.", "")
p("dias_sin", "Tiempo de respuesta en crédito pyme tradicional", "días hábiles", "num1", 10, 10, 10, S, "", "Validar con benchmarking de bancos aliados.", "")
p("friccion_sin", "Caída de conversión sin agentes (abandono por fricción y demora)", "%", "pct", 0.20, 0.30, 0.40, S, "", "", "")

sec("12. Análisis de sensibilidad")
p("sens_delta", "Choque relativo para la sensibilidad (±)", "%", "pct", 0.20, 0.20, 0.20, S, "", "Se aplica sobre el escenario base.", "")

PARAMS = [x for x in SECTIONS if x[0] == "P"]
PKEYS = [x[1] for x in PARAMS]

# Parámetros derivados (calculados en otras hojas, iguales en todos los escenarios)
DERIVED = {}  # key -> (sheet, cell) set later

# Tabla de agentes (archivo consumo_ia_por_agente.md)
AGENTS = [
    ("Guardia de entrada (clasificador de mensajes)", "claude-haiku-5-5", "Mensaje del cliente", 1, 1200, 60, 10, 25, 15, 15),
    ("Orquestador", "claude-sonnet-5-5", "Turno de conversación", 2, 7000, 350, 10, 25, 15, 15),
    ("Datos y caja · resumen nocturno y alertas", "claude-sonnet-5-5", "Corrida nocturna con cambios", 1, 9000, 700, 22, 22, 1, 0),
    ("Datos y caja · extracción de documentos no estructurados", "claude-haiku-5-5", "Documento PDF o foto", 1, 2500, 400, 10, 10, 40, 0),
    ("Vinculación y cumplimiento (KYC/SARLAFT)", "claude-sonnet-5-5", "Paso de control", 1.5, 6000, 600, 0, 0.1, 1, 7),
    ("Validación documental · extracción y conciliación", "claude-sonnet-5-5", "Documento de la solicitud", 1, 14000, 1200, 0, 1, 0, 10),
    ("Validación documental · investigación de anomalía", "claude-opus-5-5", "Expediente con alerta", 4, 25000, 2000, 0, 0.05, 0, 0.25),
    ("Uso del cupo y pagos", "claude-sonnet-5-5", "Propuesta de uso o abono", 3, 7000, 500, 0, 3, 0, 0),
    ("Acompañamiento y acciones (tesorero)", "claude-sonnet-5-5", "Plan semanal o mensual", 3, 12000, 1200, 4, 5, 1, 0),
    ("Redactor de mensajes", "claude-haiku-5-5", "Borrador", 2, 3000, 500, 3, 4, 0, 0),
    ("Copiloto de analista (interno)", "claude-opus-5-5", "Caso transferido a una persona", 2, 30000, 2500, 0.01, 0.03, 0, 0.2),
    ("Evaluador en línea (LLM como juez, muestra 5 %)", "claude-sonnet-5-5", "Interacción muestreada", 1, 8000, 300, 1, 2.5, 1, 2),
]
PRICES = [("claude-opus-5-5", 4.0, 20.0, 0.20), ("claude-sonnet-5-5", 2.0, 10.0, 0.10), ("claude-haiku-5-5", 0.10, 0.50, 0.005)]

# ---------------------------------------------------------------- ÍTEMS MENSUALES
# key, label, unit, fmt, agg, tmpl, sheet, first_tmpl(optional)
ITEMS = []


def it(key, label, unit, fmt, agg, tmpl, sheet, first=None, bold=False):
    ITEMS.append(dict(key=key, label=label, unit=unit, fmt=fmt, agg=agg, tmpl=tmpl, sheet=sheet, first=first, bold=bold))


F, I, C, PG = "Funnel", "Ingresos_Margen", "Costos", "PyG_Flujo"
it("reg_nuevos", "Registros nuevos en tesorería", "empresas", "int", "sum", "{R:reg}", F)
it("reg_acum", "Registros acumulados", "empresas", "int", "end", "{p:reg_acum}+{c:reg_nuevos}", F)
it("activ_nuevos", "Nuevos usuarios activos (conectan facturas)", "empresas", "int", "sum", "{c:reg_nuevos}*{P:pct_activacion}", F)
it("activos_tes", "Usuarios activos de tesorería (stock)", "empresas", "int", "end", "{p:activos_tes}*(1-{P:churn})+{c:activ_nuevos}", F, bold=True)
it("preaprob_nuevos", "Nuevos preaprobados", "empresas", "int", "sum", "{c:activ_nuevos}*{P:pct_preaprob}", F)
it("solicitudes", "Solicitudes de activación del cupo", "solicitudes", "int", "sum", "{l1:preaprob_nuevos}*{P:conv_inicial}+{p:stock_pre}*{P:conv_tardia}", F)
it("stock_pre", "Preaprobados pendientes de solicitar (stock)", "empresas", "int", "end", "{p:stock_pre}*(1-{P:churn})+{c:preaprob_nuevos}-{c:solicitudes}", F)
it("cupos_nuevos", "Cupos activados en el mes", "cupos", "int", "sum", "{c:solicitudes}*{P:aprob_valid}", F)
it("cupos_activos", "Cupos activos (stock)", "cupos", "int", "end", "{p:cupos_activos}*(1-{P:attr_cupos})+{c:cupos_nuevos}", F, bold=True)
it("n1", "Usuarios solo tesorería (Nivel 1)", "empresas", "int", "end", "MAX(0,{c:activos_tes}-{c:cupos_activos})", F)
it("cupo_total", "Cupo aprobado total", "COP M", "copm", "end", "{c:cupos_activos}*{P:cupo_prom}", F)
it("cartera_cupo", "Saldo utilizado del cupo (cartera rotativa)", "COP M", "copm", "end", "{c:cupo_total}*{P:utilizacion}", F, bold=True)
it("grad_nuevos", "Nuevos créditos de inversión (Nivel 3)", "créditos", "num1", "sum", "{l6:cupos_activos}*{P:tasa_grad}", F)
it("saldo_inv", "Saldo de créditos de inversión", "COP M", "copm", "end", "{p:saldo_inv}*(1-1/{P:plazo_inv})+{c:grad_nuevos}*{P:monto_inv}", F)
it("cartera_total", "Cartera total (cupo + inversión)", "COP M", "copm", "end", "{c:cartera_cupo}+{c:saldo_inv}", F, bold=True)

it("tasa_fondeo", "Costo de fondeo del año (tasa de política + margen)", "% E.A.", "pct2", "avg", "{Y:tasa_pol}+{P:spread_fondeo}", I)
it("int_cupo", "Intereses del cupo rotativo", "COP M", "copm", "sum", "{c:cartera_cupo}*((1+{P:tasa_cliente})^(1/12)-1)", I)
it("int_inv", "Intereses del crédito de inversión", "COP M", "copm", "sum", "{c:saldo_inv}*((1+{P:tasa_inv})^(1/12)-1)", I)
it("compensacion", "Compensación de tasa de la línea de fomento (sobre saldo del cupo)", "COP M", "copm", "sum", "{c:cartera_cupo}*((1+{P:subsidio_fondeo})^(1/12)-1)", I)
it("ing_int", "Ingresos por intereses y compensación", "COP M", "copm", "sum", "{c:int_cupo}+{c:int_inv}+{c:compensacion}", I, bold=True)
it("costo_fondeo", "(−) Costo de fondeo (cartera menos capital asignado)", "COP M", "copm", "sum", "({c:cartera_total}-{c:capital})*((1+{c:tasa_fondeo})^(1/12)-1)", I)
it("com_fng", "(−) Comisión de garantía FNG asumida por el BFE", "COP M", "copm", "sum", "{c:cartera_total}*{P:fng_tarifa}*(1+{P:iva})/12*{P:pct_fng_bfe}", I)
it("mfn", "Margen financiero neto", "COP M", "copm", "sum", "{c:ing_int}-{c:costo_fondeo}-{c:com_fng}", I, bold=True)
it("com_estr", "Comisiones de estructuración (cross-sell)", "COP M", "copm", "sum", "{c:grad_nuevos}*{P:monto_inv}*{P:com_estr}", I)
it("ing_netos", "Ingresos netos totales", "COP M", "copm", "sum", "{c:mfn}+{c:com_estr}", I, bold=True)
it("ead", "Exposición al incumplimiento (EAD)", "COP M", "copm", "end", "{c:cartera_cupo}+{P:ccf}*({c:cupo_total}-{c:cartera_cupo})+{c:saldo_inv}", I)
it("pe", "(−) Pérdida esperada (PD × LGD × (1 − cobertura) × EAD)", "COP M", "copm", "sum", "{c:ead}*{P:pd}/12*{P:lgd}*(1-{P:cobertura})", I)
it("margen_riesgo", "Margen después de riesgo", "COP M", "copm", "sum", "{c:ing_netos}-{c:pe}", I, bold=True)

it("fte_tech", "Producto y tecnología", "FTE", "num1", "avg", "{Y:fte_tech}", C)
it("fte_ger", "Gerencia de línea, riesgo y modelos", "FTE", "num1", "avg", "{P:fte_gerencia}", C)
it("casos_hum", "Casos que revisa una persona", "casos", "num1", "sum", "{c:solicitudes}*{P:pct_rev_humana}+{c:cupos_activos}*{P:muestreo}", C)
it("fte_analistas", "Analistas de crédito", "FTE", "num1", "avg", "MAX({P:min_analistas},ROUNDUP({c:casos_hum}/{P:prod_ia},0))", C)
it("fte_cump", "Cumplimiento", "FTE", "num1", "avg", "{P:cump_base}+ROUNDUP({c:solicitudes}/{P:ratio_cump_ia},0)", C)
it("fte_soporte", "Soporte a clientes", "FTE", "num1", "avg", "MAX({P:min_soporte},ROUNDUP({c:activos_tes}/{P:ratio_sop_ia},0))", C)
it("c_tech", "Costo producto y tecnología", "COP M", "copm", "sum", "{c:fte_tech}*{P:costo_tech}", C)
it("c_ger", "Costo gerencia y riesgo", "COP M", "copm", "sum", "{c:fte_ger}*{P:costo_gerencia}", C)
it("c_analistas", "Costo analistas de crédito", "COP M", "copm", "sum", "{c:fte_analistas}*{P:costo_analista}", C)
it("c_cump", "Costo cumplimiento", "COP M", "copm", "sum", "{c:fte_cump}*{P:costo_cump}", C)
it("c_soporte", "Costo soporte", "COP M", "copm", "sum", "{c:fte_soporte}*{P:costo_soporte}", C)
it("c_personas", "Personas (total)", "COP M", "copm", "sum", "{c:c_tech}+{c:c_ger}+{c:c_analistas}+{c:c_cump}+{c:c_soporte}", C, bold=True)
it("ia_n1", "IA · usuarios solo tesorería", "COP M", "copm", "sum", "{c:n1}*{P:usd_n1}*{P:trm}*{P:mult_ia}/1000000", C)
it("ia_n2", "IA · usuarios con cupo", "COP M", "copm", "sum", "{c:cupos_activos}*{P:usd_n2}*{P:trm}*{P:mult_ia}/1000000", C)
it("ia_onb", "IA · onboarding de registros", "COP M", "copm", "sum", "{c:reg_nuevos}*{P:usd_onb}*{P:trm}*{P:mult_ia}/1000000", C)
it("ia_act", "IA · activación del cupo", "COP M", "copm", "sum", "{c:solicitudes}*{P:usd_act}*{P:trm}*{P:mult_ia}/1000000", C)
it("c_ia", "IA (total)", "COP M", "copm", "sum", "{c:ia_n1}+{c:ia_n2}+{c:ia_onb}+{c:ia_act}", C, bold=True)
it("c_infra", "Infraestructura", "COP M", "copm", "sum", "{P:infra_fijo}+{c:activos_tes}*{P:infra_var}/1000000", C, bold=True)
it("d_sol", "Datos de terceros · solicitudes", "COP M", "copm", "sum", "{c:solicitudes}*{P:datos_sol}/1000000", C)
it("d_mon", "Datos de terceros · monitoreo de cupos", "COP M", "copm", "sum", "{c:cupos_activos}*{P:monit_cupo}/1000000", C)
it("c_datos", "Datos de terceros (total)", "COP M", "copm", "sum", "{c:d_sol}+{c:d_mon}", C, bold=True)
it("c_adq", "Adquisición (CAC + comisión a aliados)", "COP M", "copm", "sum", "{c:reg_nuevos}*{P:cac}/1000000+{c:cupos_nuevos}*{P:com_aliado}/1000000", C, bold=True)
it("c_overhead", "Gastos generales asignados", "COP M", "copm", "sum", "({c:c_personas}+{c:c_infra})*{P:overhead}", C, bold=True)
it("opex", "Costos de operación (total)", "COP M", "copm", "sum", "{c:c_personas}+{c:c_ia}+{c:c_infra}+{c:c_datos}+{c:c_adq}+{c:c_overhead}", C, bold=True)
it("amort", "Amortización de la inversión inicial (36 meses)", "COP M", "copm", "sum", "IF({M}<=36,{P:inv_total}/36,0)", C)

it("pg_ing", "Ingresos netos totales", "COP M", "copm", "sum", "{c:ing_netos}", PG)
it("pg_pe", "(−) Pérdida esperada", "COP M", "copm", "sum", "{c:pe}", PG)
it("pg_opex", "(−) Costos de operación", "COP M", "copm", "sum", "{c:opex}", PG)
it("ebitda", "Resultado operativo antes de amortización", "COP M", "copm", "sum", "{c:pg_ing}-{c:pg_pe}-{c:pg_opex}", PG, bold=True)
it("pg_amort", "(−) Amortización de la inversión", "COP M", "copm", "sum", "{c:amort}", PG)
it("uai", "Utilidad antes de impuestos", "COP M", "copm", "sum", "{c:ebitda}-{c:pg_amort}", PG, bold=True)
it("impuestos", "(−) Impuesto de renta (pérdidas generan escudo en el BFE)", "COP M", "copm", "sum", "{c:uai}*{Y:tax}", PG)
it("un", "Utilidad neta", "COP M", "copm", "sum", "{c:uai}-{c:impuestos}", PG, bold=True)
it("capital", "Capital asignado (cartera × ponderación × solvencia)", "COP M", "copm", "end", "{c:cartera_total}*{P:ponderacion}*{P:solvencia}", PG)
it("d_capital", "(−) Aumento del capital asignado", "COP M", "copm", "sum", "{c:capital}-{p:capital}", PG)
it("flujo", "Flujo de caja para el accionista", "COP M", "copm", "sum", "{c:un}+{c:pg_amort}-{c:d_capital}", PG, bold=True)
it("flujo_acum", "Flujo acumulado (incluye inversión del año 0)", "COP M", "copm", "end", "{p:flujo_acum}+{c:flujo}", PG, first="-{P:inv_total}+{c:flujo}")
it("pb_flag", "Mes de recuperación del flujo al accionista (marca)", "mes", "int", None, 'IF(AND({c:flujo_acum}>=0,{p:flujo_acum}<0),{M},"")', PG, first='IF({c:flujo_acum}>=0,{M},"")')
it("op_acum", "Resultado acumulado operativo (utilidad neta + amortización − inversión, sin capital)", "COP M", "copm", "end", "{p:op_acum}+{c:un}+{c:pg_amort}", PG, first="-{P:inv_total}+{c:un}+{c:pg_amort}")
it("pbo_flag", "Mes de recuperación operativa (marca)", "mes", "int", None, 'IF(AND({c:op_acum}>=0,{p:op_acum}<0),{M},"")', PG, first='IF({c:op_acum}>=0,{M},"")')

IKEYS = [x["key"] for x in ITEMS]
TOKEN = re.compile(r"\{([A-Za-z0-9]+):([a-z0-9_]+)\}|\{M\}")


class Ctx:
    """Resuelve referencias para un bloque (hoja principal o bloque del motor)."""

    def __init__(self, item_loc, param_ref, month_row_ref, cur_sheet_of_item=None):
        self.item_loc = item_loc          # key -> (sheet, row)
        self.param_ref = param_ref        # key -> absolute ref string
        self.month_row_ref = month_row_ref  # function(col) -> ref
        self.cur_sheet = None

    def ref_item(self, key, col):
        sh, row = self.item_loc[key]
        a = f"{CL(col)}{row}"
        if sh != self.cur_sheet:
            return f"'{sh}'!{a}"
        return a

    def render(self, tmpl, col):
        m = month_of_col(col)
        y = year_of_month(m)

        def rep(mo):
            if mo.group(0) == "{M}":
                return self.month_row_ref(col)
            kind, key = mo.group(1), mo.group(2)
            if kind == "c":
                return self.ref_item(key, col)
            if kind == "p":
                return "0" if col == FIRST_M_COL else self.ref_item(key, col - 1)
            if kind.startswith("l"):
                k = int(kind[1:])
                return "0" if col - k < FIRST_M_COL else self.ref_item(key, col - k)
            if kind == "P":
                return self.param_ref(key)
            if kind == "Y":
                return self.param_ref(f"{key}_{YEARS[y]}")
            if kind == "R":
                if m <= 6:
                    return self.param_ref("reg_p1")
                if m <= 12:
                    return self.param_ref("reg_p2")
                return self.param_ref(f"reg_y{y}")
            raise ValueError(kind)
        return "=" + TOKEN.sub(rep, tmpl)


def write_item_row(ws, ctx, item, row, label_col=1):
    ctx.cur_sheet = ws.title
    ws.cell(row=row, column=1, value=item["label"]).font = BOLD if item["bold"] else BLACK
    ws.cell(row=row, column=2, value=item["unit"]).font = BLACK
    for col in range(FIRST_M_COL, LAST_M_COL + 1):
        t = item["first"] if (item["first"] and col == FIRST_M_COL) else item["tmpl"]
        c = ws.cell(row=row, column=col, value=ctx.render(t, col))
        c.number_format = FMT[item["fmt"]]
        c.font = BOLD if item["bold"] else BLACK
    agg = item["agg"]
    if agg:
        for y in (1, 2, 3, 4, 5):
            a = CL(FIRST_M_COL + (y - 1) * 12)
            b = CL(FIRST_M_COL + y * 12 - 1)
            if agg == "sum":
                f = f"=SUM({a}{row}:{b}{row})"
            elif agg == "end":
                f = f"={b}{row}"
            else:
                f = f"=AVERAGE({a}{row}:{b}{row})"
            c = ws.cell(row=row, column=YCOL[y], value=f)
            c.number_format = FMT[item["fmt"]]
            c.font = BOLD
        for tc, ylast in ((TCOL, 3), (T5COL, 5)):
            ya, yc = CL(YCOL[1]), CL(YCOL[ylast])
            if agg == "sum":
                f = f"=SUM({ya}{row}:{yc}{row})"
            elif agg == "end":
                f = f"={yc}{row}"
            else:
                f = f"=AVERAGE({ya}{row}:{yc}{row})"
            c = ws.cell(row=row, column=tc, value=f)
            c.number_format = FMT[item["fmt"]]
            c.font = BOLD


def month_header(ws, row, with_year_cols=True, label="Concepto"):
    ws.cell(row=row, column=1, value=label).font = HDR_FONT
    ws.cell(row=row, column=2, value="Unidad").font = HDR_FONT
    for col in range(1, T5COL + 1):
        ws.cell(row=row, column=col).fill = HDR_FILL
        ws.cell(row=row + 1, column=col).fill = HDR_FILL
    for col in range(FIRST_M_COL, LAST_M_COL + 1):
        m = month_of_col(col)
        y = year_of_month(m)
        ws.cell(row=row, column=col, value=m).font = HDR_FONT  # número de mes (etiqueta)
        ws.cell(row=row + 1, column=col, value=f"{MESES[(m - 1) % 12]}-{YEARS[y][2:]}").font = HDR_FONT
    if with_year_cols:
        for y in (1, 2, 3, 4, 5):
            ws.cell(row=row, column=YCOL[y], value=("Año " if y <= 3 else "Ext. año ") + str(y)).font = HDR_FONT
            ws.cell(row=row + 1, column=YCOL[y], value=YEARS[y]).font = HDR_FONT
        ws.cell(row=row, column=TCOL, value="Total").font = HDR_FONT
        ws.cell(row=row + 1, column=TCOL, value="3 años").font = HDR_FONT
        ws.cell(row=row, column=T5COL, value="Total").font = HDR_FONT
        ws.cell(row=row + 1, column=T5COL, value="5 años").font = HDR_FONT
    ws.cell(row=row + 1, column=1, value="Mes →").font = HDR_FONT


def set_widths(ws, first=48, second=12, months=10):
    ws.column_dimensions["A"].width = first
    ws.column_dimensions["B"].width = second
    for col in range(FIRST_M_COL, T5COL + 1):
        ws.column_dimensions[CL(col)].width = months
    ws.column_dimensions[CL(LAST_M_COL + 1)].width = 3


wb = Workbook()
wb.remove(wb.active)
ws_port = wb.create_sheet("Portada")
ws_sup = wb.create_sheet("Supuestos")
ws_fue = wb.create_sheet("Fuentes")
ws_mer = wb.create_sheet("Mercado")
ws_fun = wb.create_sheet("Funnel")
ws_ing = wb.create_sheet("Ingresos_Margen")
ws_cia = wb.create_sheet("Costos_IA")
ws_cos = wb.create_sheet("Costos")
ws_efi = wb.create_sheet("Eficiencia_IA")
ws_pyg = wb.create_sheet("PyG_Flujo")
ws_esc = wb.create_sheet("Escenarios")
ws_val = wb.create_sheet("Validacion")
ws_mp = wb.create_sheet("Motor_Params")
ws_mot = wb.create_sheet("Motor")

# ================================================================ SUPUESTOS
ws = ws_sup
ws["A1"] = "Supuestos del modelo · Auro by BFE"; ws["A1"].font = TITLE
ws["A2"] = "Todos los inputs del modelo. Azul = dato editable. Negro = fórmula. Columna G = valor del escenario activo que usan las hojas de cálculo."; ws["A2"].font = BLACK
ws["A3"] = "Escenario activo →"; ws["A3"].font = BOLD
ws["B3"] = "Base"; ws["B3"].font = Font(name=FONT, color="0000FF", bold=True, size=11); ws["B3"].fill = YELLOW
dv = DataValidation(type="list", formula1='"Pesimista,Base,Optimista"', allow_blank=False)
ws.add_data_validation(dv); dv.add("B3")
ws["C3"] = "Índice:"; ws["C3"].font = BLACK
ws["D3"] = '=MATCH(B3,{"Pesimista","Base","Optimista"},0)'
ws["D3"] = "=MATCH(B3,$D$5:$F$5,0)"
ws["E3"] = "← elija Pesimista, Base u Optimista en la celda amarilla"; ws["E3"].font = Font(name=FONT, italic=True, size=9)
hdr = ["Clave", "Parámetro", "Unidad", "Pesimista", "Base", "Optimista", "Activo", "Tipo", "Fuente", "Nota"]
for j, h in enumerate(hdr, 1):
    c = ws.cell(row=5, column=j, value=h); c.font = HDR_FONT; c.fill = HDR_FILL
PROW = {}
r = 6
for s in SECTIONS:
    if s[0] == "SEC":
        ws.cell(row=r, column=1, value=s[1]).font = SUB
        for j in range(1, 11):
            ws.cell(row=r, column=j).fill = SEC_FILL
        r += 1
        continue
    _, key, label, unit, fmt, pes, base, opt, tipo, fuente, nota, tag = s
    ws.cell(row=r, column=1, value=key).font = Font(name=FONT, size=8, color="808080")
    ws.cell(row=r, column=2, value=label).font = BLACK
    ws.cell(row=r, column=3, value=unit).font = BLACK
    for j, v in zip((4, 5, 6), (pes, base, opt)):
        c = ws.cell(row=r, column=j, value=v); c.font = BLUE; c.number_format = FMT[fmt]
    c = ws.cell(row=r, column=7, value=f"=INDEX(D{r}:F{r},$D$3)"); c.number_format = FMT[fmt]; c.font = BOLD
    ws.cell(row=r, column=8, value=tipo).font = BLACK
    ws.cell(row=r, column=9, value=fuente).font = BLACK
    ws.cell(row=r, column=10, value=nota).font = Font(name=FONT, size=9)
    ws.cell(row=r, column=10).alignment = Alignment(wrap_text=False)
    if tag:
        ws.cell(row=r, column=7).fill = KEY_FILL
    PROW[key] = r
    r += 1
    if key == "inv_lanzamiento":
        # fila derivada: inversión total
        ws.cell(row=r, column=1, value="inv_total").font = Font(name=FONT, size=8, color="808080")
        ws.cell(row=r, column=2, value="Inversión inicial total").font = BOLD
        ws.cell(row=r, column=3, value="COP M").font = BLACK
        a = PROW["inv_desarrollo"]
        for j in (4, 5, 6, 7):
            L = CL(j)
            c = ws.cell(row=r, column=j, value=f"=SUM({L}{a}:{L}{r-1})"); c.number_format = FMT["copm"]; c.font = BOLD
        ws.cell(row=r, column=8, value="Cálculo").font = BLACK
        PROW["inv_total"] = r
        r += 1
PARAM_FMT = {s[1]: s[4] for s in PARAMS}
PARAM_FMT["inv_total"] = "copm"
PARAM_TAG = {s[1]: s[11] for s in PARAMS}
PARAM_LABEL = {s[1]: s[2] for s in PARAMS}
PARAM_LABEL["inv_total"] = "Inversión inicial total"

# Tabla de agentes
r += 1
AG_HDR_ROW = r + 1
ws.cell(row=r, column=1, value="13. Consumo de IA por agente (insumo: entregables/_insumos/consumo_ia_por_agente.md · fuente F14)").font = SUB
for j in range(1, 11):
    ws.cell(row=r, column=j).fill = SEC_FILL
r += 1
ah = ["Agente", "Modelo", "Evento", "Llamadas por evento", "Tokens entrada por llamada", "Tokens salida por llamada", "Eventos/cliente/mes N1", "Eventos/cliente/mes N2", "Eventos únicos onboarding", "Eventos únicos activación"]
for j, h in enumerate(ah, 1):
    c = ws.cell(row=r, column=j, value=h); c.font = HDR_FONT; c.fill = HDR_FILL; c.alignment = WRAP
r += 1
AG_FIRST = r
for a in AGENTS:
    for j, v in enumerate(a, 1):
        c = ws.cell(row=r, column=j, value=v)
        c.font = BLUE if j >= 2 else BLACK
        if j >= 4:
            c.number_format = '#,##0.00' if j in (4, 7, 8, 9, 10) else '#,##0'
    r += 1
AG_LAST = r - 1
r += 1
ws.cell(row=r, column=1, value="Precios de la API de Anthropic (US$ por millón de tokens, tarifa de primera parte, nov-2026 · fuente F13)").font = SUB
for j in range(1, 11):
    ws.cell(row=r, column=j).fill = SEC_FILL
r += 1
for j, h in enumerate(["Modelo", "Entrada", "Salida", "Lectura de caché"], 1):
    c = ws.cell(row=r, column=j, value=h); c.font = HDR_FONT; c.fill = HDR_FILL
r += 1
PR_FIRST = r
for pr in PRICES:
    for j, v in enumerate(pr, 1):
        c = ws.cell(row=r, column=j, value=v); c.font = BLUE
        if j > 1:
            c.number_format = '0.000'
    r += 1
PR_LAST = r - 1
ws.cell(row=r, column=1, value="Lectura de caché de Haiku 5.5: supuesto (5 % del precio de entrada, igual proporción que Opus y Sonnet).").font = Font(name=FONT, size=9, italic=True)
ws.column_dimensions["A"].width = 44
ws.column_dimensions["B"].width = 70
ws.column_dimensions["C"].width = 14
for L in "DEFG":
    ws.column_dimensions[L].width = 12
ws.column_dimensions["H"].width = 24
ws.column_dimensions["I"].width = 8
ws.column_dimensions["J"].width = 90
ws.freeze_panes = "C6"


def sup_active(key):
    return f"Supuestos!$G${PROW[key]}"


# ================================================================ COSTOS_IA (por agente)
ws = ws_cia
ws["A1"] = "Costo de IA por agente · tokens × precio"; ws["A1"].font = TITLE
ws["A2"] = "Costo por llamada (US$) = [tokens de entrada × (1 − % caché) × precio entrada + tokens de entrada × % caché × precio caché + tokens de salida × precio salida] / 1.000.000. Sin descuento de Batch API (conservador)."
ws["A2"].font = BLACK
h = ["Agente", "Modelo", "Precio entrada", "Precio salida", "Precio caché", "US$ por llamada", "US$ por evento", "US$/cliente/mes N1", "US$/cliente/mes N2", "US$ onboarding", "US$ activación"]
for j, t in enumerate(h, 1):
    c = ws.cell(row=4, column=j, value=t); c.font = HDR_FONT; c.fill = HDR_FILL; c.alignment = WRAP
rr = 5
cache = sup_active("cache_pct")
for k in range(len(AGENTS)):
    sr = AG_FIRST + k
    ws.cell(row=rr, column=1, value=f"=Supuestos!A{sr}").font = GREEN
    ws.cell(row=rr, column=2, value=f"=Supuestos!B{sr}").font = GREEN
    for j, colp in zip((3, 4, 5), ("B", "C", "D")):
        c = ws.cell(row=rr, column=j, value=f"=INDEX(Supuestos!${colp}${PR_FIRST}:${colp}${PR_LAST},MATCH(B{rr},Supuestos!$A${PR_FIRST}:$A${PR_LAST},0))")
        c.number_format = '0.000'
    c = ws.cell(row=rr, column=6, value=f"=(Supuestos!E{sr}*(1-{cache})*C{rr}+Supuestos!E{sr}*{cache}*E{rr}+Supuestos!F{sr}*D{rr})/1000000"); c.number_format = '0.00000'
    c = ws.cell(row=rr, column=7, value=f"=F{rr}*Supuestos!D{sr}"); c.number_format = '0.00000'
    for j, colE in zip((8, 9, 10, 11), ("G", "H", "I", "J")):
        c = ws.cell(row=rr, column=j, value=f"=G{rr}*Supuestos!{colE}{sr}"); c.number_format = '0.0000'
    rr += 1
last = rr - 1
ws.cell(row=rr, column=1, value="Total por perfil (US$)").font = BOLD
for j in (8, 9, 10, 11):
    L = CL(j)
    c = ws.cell(row=rr, column=j, value=f"=SUM({L}5:{L}{last})"); c.number_format = '0.000'; c.font = BOLD; c.fill = KEY_FILL
TOT_ROW = rr
DERIVED["usd_n1"] = f"Costos_IA!$H${TOT_ROW}"
DERIVED["usd_n2"] = f"Costos_IA!$I${TOT_ROW}"
DERIVED["usd_onb"] = f"Costos_IA!$J${TOT_ROW}"
DERIVED["usd_act"] = f"Costos_IA!$K${TOT_ROW}"
rr += 1
ws.cell(row=rr, column=1, value="Total por perfil sin caché (US$, referencia)").font = BLACK
for j, colE in zip((8, 9, 10, 11), ("G", "H", "I", "J")):
    f = "=SUMPRODUCT(" + ",".join([]) + ")"
    # sin caché: (tin*pin + tout*pout)/1e6 * llamadas * eventos
    f = (f"=SUMPRODUCT(Supuestos!$E${AG_FIRST}:$E${AG_LAST}*$C$5:$C${last}+Supuestos!$F${AG_FIRST}:$F${AG_LAST}*$D$5:$D${last},"
         f"Supuestos!$D${AG_FIRST}:$D${AG_LAST},Supuestos!${colE}${AG_FIRST}:${colE}${AG_LAST})/1000000")
    c = ws.cell(row=rr, column=j, value=f); c.number_format = '0.000'
rr += 2
ws.cell(row=rr, column=1, value="En COP por perfil (con caché, × TRM × multiplicador de consumo)").font = SUB
rr += 1
for j, lab in zip((8, 9, 10, 11), ("N1 / mes", "N2 / mes", "Onboarding", "Activación")):
    ws.cell(row=rr, column=j, value=lab).font = BOLD
rr += 1
ws.cell(row=rr, column=1, value="COP por cliente o evento").font = BLACK
for j in (8, 9, 10, 11):
    L = CL(j)
    c = ws.cell(row=rr, column=j, value=f"={L}{TOT_ROW}*{sup_active('trm')}*{sup_active('mult_ia')}"); c.number_format = FMT["cop"]
rr += 2
ws.cell(row=rr, column=1, value="Costo mensual de IA por agente en el mes 36 (US$, escenario activo)").font = SUB
rr += 1
for j, t in enumerate(["Agente", "US$ mes 36", "% del total"], 1):
    c = ws.cell(row=rr, column=j, value=t); c.font = HDR_FONT; c.fill = HDR_FILL
rr += 1
AG36_FIRST = rr
# needed refs to funnel month 36 (set later through placeholders) -> we fill after funnel rows known
AG36_ROWS = []
for k in range(len(AGENTS)):
    AG36_ROWS.append(rr)
    rr += 1
AG36_TOTAL = rr
ws.column_dimensions["A"].width = 52
ws.column_dimensions["B"].width = 18
for col in range(3, 12):
    ws.column_dimensions[CL(col)].width = 14

# ================================================================ HOJAS PRINCIPALES (escenario activo)
MAIN_START = {F: 7, I: 7, C: 7, PG: 7}
item_loc_main = {}
rows_by_sheet = {}
for sh in (F, I, C, PG):
    rr0 = MAIN_START[sh]
    for itm in [x for x in ITEMS if x["sheet"] == sh]:
        item_loc_main[itm["key"]] = (sh, rr0)
        rr0 += 1
        # espaciado entre grupos de costos
        if sh == C and itm["key"] in ("fte_soporte", "c_personas", "c_ia", "c_infra", "c_datos", "c_adq", "c_overhead"):
            rr0 += 1
        if sh == I and itm["key"] in ("ing_int", "mfn", "ing_netos"):
            rr0 += 1
        if sh == F and itm["key"] in ("reg_acum", "activos_tes", "cupos_activos", "n1", "cartera_cupo"):
            rr0 += 1


def main_param(key):
    if key in DERIVED:
        return DERIVED[key]
    return sup_active(key)


ctx_main = Ctx(item_loc_main, main_param, lambda col: f"{CL(col)}$5")
titles = {
    F: ("Funnel mensual · 36 meses del caso + 24 de extensión (escenario activo)", "Registros en tesorería → usuarios activos → preaprobados → solicitudes → cupos activos → utilización. Mes 1 = enero 2027 (piloto cerrado meses 1-6). Meses 37-60 (2030-2031) = extensión indicativa."),
    I: ("Ingresos, margen financiero y pérdida esperada (escenario activo)", "Margen financiero neto = intereses − fondeo − comisión de garantía asumida por el BFE. Pérdida esperada = PD × LGD × (1 − cobertura de garantía) × EAD."),
    C: ("Costos de operación (escenario activo)", "Personas dimensionadas por volumen y productividad con agentes; IA por perfil de cliente (ver Costos_IA); infraestructura, datos de terceros y adquisición. La inversión inicial se amortiza en 36 meses."),
    PG: ("P&G, flujo de caja y valoración (escenario activo)", "Flujo para el accionista = utilidad neta + amortización − aumento del capital asignado a la cartera. Año 0 = inversión inicial."),
}
sheet_obj = {F: ws_fun, I: ws_ing, C: ws_cos, PG: ws_pyg}
for sh, wsx in sheet_obj.items():
    wsx["A1"] = titles[sh][0]; wsx["A1"].font = TITLE
    wsx["A2"] = titles[sh][1]; wsx["A2"].font = BLACK
    wsx["A3"] = "=\"Escenario activo: \"&Supuestos!B3"; wsx["A3"].font = BOLD
    month_header(wsx, 5)
    set_widths(wsx)
    wsx.freeze_panes = "C7"
    for itm in [x for x in ITEMS if x["sheet"] == sh]:
        write_item_row(wsx, ctx_main, itm, item_loc_main[itm["key"]][1])
# sub-títulos en Costos
ws_cos.cell(row=6, column=1, value="Personas (FTE)").font = SUB
ws_ing.cell(row=6, column=1, value="Margen financiero").font = SUB
ws_fun.cell(row=6, column=1, value="Embudo").font = SUB
ws_pyg.cell(row=6, column=1, value="P&G mensual").font = SUB


def metrics_block(wsx, start_row, loc, param, sheet_name):
    """Escribe flujos anuales (años 0-5) y métricas; devuelve dict métrica -> celda."""
    def R(key, col):
        sh, row = loc[key]
        pre = "" if sh == sheet_name else f"'{sh}'!"
        return f"{pre}{CL(col)}{row}"
    r0 = start_row
    out = {}
    wsx.cell(row=r0, column=1, value="Flujos anuales (COP M)").font = SUB
    for j, t in enumerate(["Año 0", "2027", "2028", "2029", "2030 (ext.)", "2031 (ext.)", "Valor terminal 2031"], 3):
        c = wsx.cell(row=r0, column=j, value=t); c.font = HDR_FONT; c.fill = HDR_FILL
    r1 = r0 + 1
    wsx.cell(row=r1, column=1, value="Flujo para el accionista").font = BOLD
    wsx.cell(row=r1, column=3, value=f"=-{param('inv_total')}")
    for y in (1, 2, 3, 4, 5):
        wsx.cell(row=r1, column=3 + y, value=f"={R('flujo', YCOL[y])}")
    vt = (f"=({R('un', YCOL[5])}*(1+{param('g_terminal')})-{R('capital', YCOL[5])}*{param('g_terminal')})"
          f"/({param('ke')}-{param('g_terminal')})")
    wsx.cell(row=r1, column=9, value=vt)
    r2 = r1 + 1
    wsx.cell(row=r2, column=1, value="Flujo con valor terminal en 2031").font = BLACK
    for j in range(3, 8):
        wsx.cell(row=r2, column=j, value=f"={CL(j)}{r1}")
    wsx.cell(row=r2, column=8, value=f"=H{r1}+I{r1}")
    for rr_ in (r1, r2):
        for j in range(3, 10):
            wsx.cell(row=rr_, column=j).number_format = FMT["copm"]
    r3 = r2 + 2
    pre = "" if loc["pb_flag"][0] == sheet_name else f"'{loc['pb_flag'][0]}'!"
    flag_row, cum_row, fl_row = loc["pb_flag"][1], loc["flujo_acum"][1], loc["flujo"][1]
    fr = f"{pre}{CL(FIRST_M_COL)}{flag_row}:{CL(LAST_M_COL)}{flag_row}"
    fro = f"{pre}{CL(FIRST_M_COL)}{loc['pbo_flag'][1]}:{CL(LAST_M_COL)}{loc['pbo_flag'][1]}"
    m36 = CL(FIRST_M_COL + 35)
    cap5 = R('capital', YCOL[5]); cap4 = R('capital', YCOL[4])
    mets = [
        ("vpn", "VPN a 3 años (2027-2029, sin valor terminal)", f"=C{r1}+NPV({param('ke')},D{r1}:F{r1})", "copm"),
        ("tir", "TIR a 3 años", f'=IFERROR(IRR(C{r1}:F{r1}),"n.a.")', "pct"),
        ("vpn5", "VPN a 5 años (incluye extensión 2030-2031, sin valor terminal)", f"=C{r1}+NPV({param('ke')},D{r1}:H{r1})", "copm"),
        ("vpn_vt", "VPN a 5 años con valor terminal", f"=C{r2}+NPV({param('ke')},D{r2}:H{r2})", "copm"),
        ("tir_vt", "TIR a 5 años con valor terminal", f'=IFERROR(IRR(C{r2}:H{r2}),"n.a.")', "pct"),
        ("payback", "Payback del flujo al accionista (mes, horizonte 60)", f'=IF(COUNT({fr})=0,"> 60",MIN({fr}))', "int"),
        ("payback_op", "Payback operativo: recupera inversión y pérdidas, sin capital (mes)", f'=IF(COUNT({fro})=0,"> 60",MIN({fro}))', "int"),
        ("min_acum", "Necesidad máxima de caja (mínimo del flujo acumulado al accionista)", f"=MIN({pre}{CL(FIRST_M_COL)}{cum_row}:{CL(LAST_M_COL)}{cum_row})", "copm"),
        ("cum36", "Flujo acumulado al accionista a dic-2029", f"={pre}{m36}{cum_row}", "copm"),
        ("roe5", "ROE 2031 (utilidad neta / capital asignado promedio)", f"=IFERROR({R('un', YCOL[5])}/AVERAGE({cap4},{cap5}),0)", "pct"),
    ]
    rr_ = r3
    for k, lab_, f_, fm in mets:
        wsx.cell(row=rr_, column=1, value=lab_).font = BOLD
        c = wsx.cell(row=rr_, column=3, value=f_); c.number_format = FMT[fm]; c.font = BOLD; c.fill = KEY_FILL
        out[k] = (wsx.title, f"C{rr_}")
        rr_ += 1
    out["flujo_row"] = r1
    out["end_row"] = rr_
    return out


pyg_last = max(v[1] for k, v in item_loc_main.items() if v[0] == PG)
MAIN_METRICS = metrics_block(ws_pyg, pyg_last + 3, item_loc_main, main_param, PG)

# ================================================================ MOTOR (escenarios + sensibilidad)
RUNS = [("Pesimista", "", 0), ("Base", "", 0), ("Optimista", "", 0)]
SENS = [("conv", "Conversión a cupo"), ("util", "Utilización del cupo"), ("tasa", "Tasa al cliente"),
        ("pd", "Pérdida esperada (PD)"), ("cac", "CAC por registro"), ("ia", "Costo de IA")]
for tag, name in SENS:
    RUNS.append((f"{name} −", tag, -1))
    RUNS.append((f"{name} +", tag, +1))
MP_KEYS = PKEYS + ["inv_total"]
used = set()
for itm in ITEMS:
    for t in (itm["tmpl"], itm["first"] or ""):
        for mo in TOKEN.finditer(t):
            if mo.group(0) == "{M}":
                continue
            kind, key = mo.group(1), mo.group(2)
            if kind == "P":
                used.add(key)
            elif kind == "Y":
                for y in YEARS.values():
                    used.add(f"{key}_{y}")
            elif kind == "R":
                used.update(["reg_p1", "reg_p2", "reg_y2", "reg_y3", "reg_y4", "reg_y5"])
used.update(["inv_total", "ke", "g_terminal"])
MP_LIST = [k for k in MP_KEYS if k in used] + [k for k in DERIVED]
ws = ws_mp
ws["A1"] = "Parámetros por corrida del motor (escenarios y sensibilidad)"; ws["A1"].font = TITLE
ws["A2"] = "Corridas 1-3 = escenarios de la hoja Supuestos. Corridas 4-15 = escenario base con un choque de ±(Supuestos: sens_delta) sobre el grupo de variables indicado."
RUN_COL0 = 7
ws.cell(row=4, column=1, value="Clave").font = HDR_FONT
ws.cell(row=4, column=2, value="Parámetro").font = HDR_FONT
ws.cell(row=4, column=3, value="Grupo sens.").font = HDR_FONT
for j, t in zip((4, 5, 6), ("Pesimista", "Base", "Optimista")):
    ws.cell(row=4, column=j, value=t).font = HDR_FONT
for j in range(1, RUN_COL0 + len(RUNS)):
    ws.cell(row=4, column=j).fill = HDR_FILL
    ws.cell(row=5, column=j).fill = HDR_FILL
    ws.cell(row=6, column=j).fill = HDR_FILL
ws.cell(row=5, column=2, value="Grupo choqueado →").font = HDR_FONT
ws.cell(row=6, column=2, value="Signo del choque →").font = HDR_FONT
for k, (name, tag, sign) in enumerate(RUNS):
    col = RUN_COL0 + k
    ws.cell(row=4, column=col, value=name).font = HDR_FONT
    ws.cell(row=5, column=col, value=tag).font = HDR_FONT
    ws.cell(row=6, column=col, value=sign).font = HDR_FONT
    ws.column_dimensions[CL(col)].width = 13
MPROW = {}
rr = 7
delta = sup_active("sens_delta")
for key in MP_LIST:
    ws.cell(row=rr, column=1, value=key).font = Font(name=FONT, size=8, color="808080")
    MPROW[key] = rr
    if key in DERIVED:
        ws.cell(row=rr, column=2, value="Costo IA por perfil (US$, Costos_IA)").font = BLACK
        for k in range(len(RUNS)):
            c = ws.cell(row=rr, column=RUN_COL0 + k, value=f"={DERIVED[key]}"); c.font = GREEN; c.number_format = '0.000'
        for j in (4, 5, 6):
            c = ws.cell(row=rr, column=j, value=f"={DERIVED[key]}"); c.font = GREEN; c.number_format = '0.000'
    else:
        ws.cell(row=rr, column=2, value=PARAM_LABEL.get(key, key)).font = BLACK
        ws.cell(row=rr, column=3, value=PARAM_TAG.get(key, "")).font = BLACK
        pr = PROW[key]
        fm = FMT[PARAM_FMT[key]]
        for j, L in zip((4, 5, 6), ("D", "E", "F")):
            c = ws.cell(row=rr, column=j, value=f"=Supuestos!{L}{pr}"); c.font = GREEN; c.number_format = fm
        for k, (name, tag, sign) in enumerate(RUNS):
            col = RUN_COL0 + k
            if k < 3:
                f = f"={CL(4 + k)}{rr}"
            else:
                f = f"=$E{rr}*IF($C{rr}={CL(col)}$5,1+{CL(col)}$6*{delta},1)"
            c = ws.cell(row=rr, column=col, value=f); c.number_format = fm
    rr += 1
ws.column_dimensions["A"].width = 16
ws.column_dimensions["B"].width = 60
ws.freeze_panes = "D7"

# Motor: bloques
ws = ws_mot
ws["A1"] = "Motor de cálculo por corrida (mismas fórmulas que las hojas Funnel, Ingresos_Margen, Costos y PyG_Flujo)"; ws["A1"].font = TITLE
ws["A2"] = "Cada bloque replica el cálculo mensual con los parámetros de su columna en Motor_Params. Alimenta las hojas Escenarios y la sensibilidad (tornado)."
month_header(ws, 3)
set_widths(ws, first=46)
ws.freeze_panes = "C5"
BLOCK_METRICS = []
rr = 6
for k, (name, tag, sign) in enumerate(RUNS):
    col = CL(RUN_COL0 + k)
    ws.cell(row=rr, column=1, value=f"Corrida {k+1}: {name}").font = SUB
    for j in range(1, T5COL + 1):
        ws.cell(row=rr, column=j).fill = SEC_FILL
    rr += 1
    loc = {}
    for itm in ITEMS:
        loc[itm["key"]] = ("Motor", rr)
        rr += 1

    def mparam(key, col=col):
        return f"Motor_Params!${col}${MPROW[key]}"
    ctx = Ctx(loc, mparam, lambda c_: f"{CL(c_)}$3")
    for itm in ITEMS:
        write_item_row(ws, ctx, itm, loc[itm["key"]][1])
    met = metrics_block(ws, rr + 1, loc, mparam, "Motor")
    met["loc"] = loc
    BLOCK_METRICS.append(met)
    rr = met["end_row"] + 2

# ================================================================ Costos_IA: costo por agente mes 36 (escenario activo)
ws = ws_cia
m36 = CL(FIRST_M_COL + 35)
n1 = f"Funnel!{m36}{item_loc_main['n1'][1]}"
n2 = f"Funnel!{m36}{item_loc_main['cupos_activos'][1]}"
onb = f"Funnel!{m36}{item_loc_main['reg_nuevos'][1]}"
act = f"Funnel!{m36}{item_loc_main['solicitudes'][1]}"
for k, row in enumerate(AG36_ROWS):
    src = 5 + k
    ws.cell(row=row, column=1, value=f"=A{src}").font = BLACK
    c = ws.cell(row=row, column=2, value=f"=(H{src}*{n1}+I{src}*{n2}+J{src}*{onb}+K{src}*{act})*{sup_active('mult_ia')}"); c.number_format = '#,##0.00'
    c = ws.cell(row=row, column=3, value=f"=IF($B${AG36_TOTAL}=0,0,B{row}/$B${AG36_TOTAL})"); c.number_format = FMT["pct"]
ws.cell(row=AG36_TOTAL, column=1, value="Total mes 36 (US$)").font = BOLD
c = ws.cell(row=AG36_TOTAL, column=2, value=f"=SUM(B{AG36_ROWS[0]}:B{AG36_ROWS[-1]})"); c.number_format = '#,##0.00'; c.font = BOLD
ws.cell(row=AG36_TOTAL + 1, column=1, value="Control: total mes 36 en COP M vs hoja Costos").font = BLACK
c = ws.cell(row=AG36_TOTAL + 1, column=2, value=f"=B{AG36_TOTAL}*{sup_active('trm')}/1000000"); c.number_format = FMT["copm"]
c = ws.cell(row=AG36_TOTAL + 1, column=3, value=f"=Costos!{m36}{item_loc_main['c_ia'][1]}"); c.number_format = FMT["copm"]
c = ws.cell(row=AG36_TOTAL + 1, column=4, value=f'=IF(ABS(B{AG36_TOTAL+1}-C{AG36_TOTAL+1})<0.001,"OK","REVISAR")'); c.font = BOLD


# ================================================================ helpers de referencia anual
def ann(key, y, loc=None):
    loc = loc or item_loc_main
    sh, row = loc[key]
    col = YCOL[y] if y in (1, 2, 3, 4, 5) else (TCOL if y == "T3" else T5COL)
    return f"'{sh}'!{CL(col)}{row}" if sh != "X" else ""


# ================================================================ PyG: resumen anual legible
ws = ws_pyg
r0 = MAIN_METRICS["end_row"] + 2
ws.cell(row=r0, column=1, value="Resumen anual (COP M)").font = SUB
YLIST = [1, 2, 3, "T3", 4, 5, "T5"]
for j, t in enumerate(["2027", "2028", "2029", "Total 3 años", "2030 (ext.)", "2031 (ext.)", "Total 5 años"], 3):
    c = ws.cell(row=r0, column=j, value=t); c.font = HDR_FONT; c.fill = HDR_FILL
lines = [("Intereses y compensación de tasa", "ing_int"), ("(−) Fondeo", "costo_fondeo"), ("(−) Comisión FNG asumida", "com_fng"), ("Margen financiero neto", "mfn"),
         ("Comisiones", "com_estr"), ("Ingresos netos", "ing_netos"), ("(−) Pérdida esperada", "pe"), ("(−) Personas", "c_personas"),
         ("(−) IA", "c_ia"), ("(−) Infraestructura", "c_infra"), ("(−) Datos de terceros", "c_datos"), ("(−) Adquisición", "c_adq"),
         ("(−) Gastos generales", "c_overhead"), ("(−) Amortización", "amort"), ("Utilidad antes de impuestos", "uai"), ("(−) Impuestos", "impuestos"),
         ("Utilidad neta", "un"), ("Flujo para el accionista", "flujo"), ("Cupos activos (fin de año)", "cupos_activos"), ("Cartera total (fin de año)", "cartera_total"),
         ("Margen después de riesgo", "margen_riesgo"), ("Costos de operación", "opex")]
rr = r0 + 1
SUMROW = {}
for lab, key in lines:
    ws.cell(row=rr, column=1, value=lab).font = BOLD if key in ("mfn", "ing_netos", "un", "flujo", "uai") else BLACK
    fm = "int" if key == "cupos_activos" else "copm"
    for j, y in enumerate(YLIST):
        c = ws.cell(row=rr, column=3 + j, value=f"={ann(key, y)}"); c.number_format = FMT[fm]
    SUMROW[key] = rr
    rr += 1
ws.cell(row=rr, column=1, value="Margen neto (utilidad neta / ingresos netos)").font = BLACK
for j in range(len(YLIST)):
    L = CL(3 + j)
    c = ws.cell(row=rr, column=3 + j, value=f"=IFERROR({L}{SUMROW['un']}/{L}{SUMROW['ing_netos']},0)"); c.number_format = FMT["pct"]
rr += 1
ws.cell(row=rr, column=1, value="Margen después de riesgo por cupo activo promedio (COP M/año)").font = BLACK
for j, y in enumerate(YLIST):
    if y in ("T3", "T5"):
        continue
    a_ = CL(FIRST_M_COL + (y - 1) * 12); b_ = CL(FIRST_M_COL + y * 12 - 1); cr = item_loc_main['cupos_activos'][1]
    c = ws.cell(row=rr, column=3 + j, value=f"=IFERROR({CL(3+j)}{SUMROW['margen_riesgo']}/AVERAGE(Funnel!{a_}{cr}:{b_}{cr}),0)"); c.number_format = FMT["num2"]
MARGIN_CUPO_ROW = rr
rr += 1
ws.cell(row=rr, column=1, value="Cupos activos promedio necesarios para cubrir los costos de operación del año (equilibrio)").font = BOLD
for j, y in enumerate(YLIST):
    if y in ("T3", "T5"):
        continue
    L = CL(3 + j)
    c = ws.cell(row=rr, column=3 + j, value=f"=IFERROR({L}{SUMROW['opex']}/{L}{MARGIN_CUPO_ROW},0)"); c.number_format = FMT["int"]
EQ_ROW = rr
PYG_SUMMARY_ROW = r0

# Gráfico flujo acumulado
ch = LineChart()
ch.title = "Flujo acumulado para el accionista (COP M)"
ch.y_axis.title = "COP M"
ch.x_axis.title = "Mes"
cum_row = item_loc_main["flujo_acum"][1]
data = Reference(ws, min_col=2, max_col=LAST_M_COL, min_row=cum_row)
ch.add_data(Reference(ws, min_col=FIRST_M_COL, max_col=LAST_M_COL, min_row=cum_row), from_rows=True, titles_from_data=False)
ch.set_categories(Reference(ws, min_col=FIRST_M_COL, max_col=LAST_M_COL, min_row=5))
ch.height, ch.width = 8, 18
ch.legend = None
ws.add_chart(ch, f"I{MAIN_METRICS['end_row'] + 2}")

# ================================================================ ESCENARIOS
ws = ws_esc
ws["A1"] = "Escenarios y sensibilidad"; ws["A1"].font = TITLE
ws["A2"] = "Los tres escenarios se calculan en paralelo en la hoja Motor; no dependen del selector. La sensibilidad choca ±sens_delta cada variable alrededor del escenario base."
ws["A4"] = "Resultados por escenario (COP M salvo indicación)"; ws["A4"].font = SUB
for j, t in enumerate(["Indicador", "Pesimista", "Base", "Optimista"], 1):
    c = ws.cell(row=5, column=j, value=t); c.font = HDR_FONT; c.fill = HDR_FILL


def mref(k, key, col):
    sh, row = BLOCK_METRICS[k]["loc"][key]
    return f"Motor!{CL(col)}{row}"


esc_rows = [
    ("Inversión inicial (año 0)", lambda k: f"=-Motor!C{BLOCK_METRICS[k]['flujo_row']}", "copm"),
    ("Registros acumulados a 2029", lambda k: f"={mref(k,'reg_acum',YCOL[3])}", "int"),
    ("Usuarios activos de tesorería a 2029", lambda k: f"={mref(k,'activos_tes',YCOL[3])}", "int"),
    ("Cupos activos a 2029", lambda k: f"={mref(k,'cupos_activos',YCOL[3])}", "int"),
    ("Cartera total a 2029", lambda k: f"={mref(k,'cartera_total',YCOL[3])}", "copm"),
]
for y in (1, 2, 3):
    esc_rows.append((f"Ingresos netos {YEARS[y]}", (lambda y: lambda k: f"={mref(k,'ing_netos',YCOL[y])}")(y), "copm"))
esc_rows += [
    ("Margen financiero neto (3 años)", lambda k: f"={mref(k,'mfn',TCOL)}", "copm"),
    ("Pérdida esperada (3 años)", lambda k: f"={mref(k,'pe',TCOL)}", "copm"),
    ("Costos de operación (3 años)", lambda k: f"={mref(k,'opex',TCOL)}", "copm"),
    ("Costo de IA (3 años)", lambda k: f"={mref(k,'c_ia',TCOL)}", "copm"),
    ("Costo de IA / costos de operación", lambda k: f"=IFERROR({mref(k,'c_ia',TCOL)}/{mref(k,'opex',TCOL)},0)", "pct"),
]
for y in (1, 2, 3):
    esc_rows.append((f"Utilidad neta {YEARS[y]}", (lambda y: lambda k: f"={mref(k,'un',YCOL[y])}")(y), "copm"))
esc_rows += [
    ("Utilidad neta acumulada 3 años", lambda k: f"={mref(k,'un',TCOL)}", "copm"),
    ("VPN 3 años (sin valor terminal)", lambda k: f"=Motor!{BLOCK_METRICS[k]['vpn'][1]}", "copm"),
    ("TIR 3 años", lambda k: f"=Motor!{BLOCK_METRICS[k]['tir'][1]}", "pct"),
    ("Flujo acumulado al accionista a dic-2029", lambda k: f"=Motor!{BLOCK_METRICS[k]['cum36'][1]}", "copm"),
    ("Extensión · cupos activos a 2031", lambda k: f"={mref(k,'cupos_activos',YCOL[5])}", "int"),
    ("Extensión · cartera total a 2031", lambda k: f"={mref(k,'cartera_total',YCOL[5])}", "copm"),
    ("Extensión · utilidad neta 2030", lambda k: f"={mref(k,'un',YCOL[4])}", "copm"),
    ("Extensión · utilidad neta 2031", lambda k: f"={mref(k,'un',YCOL[5])}", "copm"),
    ("Extensión · ROE 2031", lambda k: f"=Motor!{BLOCK_METRICS[k]['roe5'][1]}", "pct"),
    ("VPN 5 años (sin valor terminal)", lambda k: f"=Motor!{BLOCK_METRICS[k]['vpn5'][1]}", "copm"),
    ("VPN 5 años con valor terminal", lambda k: f"=Motor!{BLOCK_METRICS[k]['vpn_vt'][1]}", "copm"),
    ("TIR 5 años con valor terminal", lambda k: f"=Motor!{BLOCK_METRICS[k]['tir_vt'][1]}", "pct"),
    ("Payback operativo (mes)", lambda k: f"=Motor!{BLOCK_METRICS[k]['payback_op'][1]}", "int"),
    ("Payback del flujo al accionista (mes)", lambda k: f"=Motor!{BLOCK_METRICS[k]['payback'][1]}", "int"),
    ("Necesidad máxima de caja (5 años)", lambda k: f"=Motor!{BLOCK_METRICS[k]['min_acum'][1]}", "copm"),
]
rr = 6
ESC_ROW = {}
for lab, fn, fm in esc_rows:
    ws.cell(row=rr, column=1, value=lab).font = BLACK
    for k in range(3):
        c = ws.cell(row=rr, column=2 + k, value=fn(k)); c.number_format = FMT[fm]
    ESC_ROW[lab] = rr
    rr += 1
rr += 1
ws.cell(row=rr, column=1, value="Control: el motor reproduce el escenario activo de PyG_Flujo").font = BOLD
c = ws.cell(row=rr, column=2, value=f"=INDEX(B{ESC_ROW['VPN 3 años (sin valor terminal)']}:D{ESC_ROW['VPN 3 años (sin valor terminal)']},Supuestos!$D$3)"); c.number_format = FMT["copm"]
c = ws.cell(row=rr, column=3, value=f"=PyG_Flujo!{MAIN_METRICS['vpn'][1]}"); c.number_format = FMT["copm"]
c = ws.cell(row=rr, column=4, value=f'=IF(ABS(B{rr}-C{rr})<0.01,"OK","REVISAR")'); c.font = BOLD
CHECK_ROW = rr
rr += 2
# Sensibilidad
ws.cell(row=rr, column=1, value="Sensibilidad del VPN a 5 años con valor terminal (escenario base, choque ± sens_delta)").font = SUB
rr += 1
hdr = ["Variable", "VPN con choque −", "VPN con choque +", "Δ vs base (−)", "Δ vs base (+)", "Rango"]
for j, t in enumerate(hdr, 1):
    c = ws.cell(row=rr, column=j, value=t); c.font = HDR_FONT; c.fill = HDR_FILL
rr += 1
SENS_FIRST = rr
base_vpn = f"Motor!{BLOCK_METRICS[1]['vpn_vt'][1]}"
for i, (tag, name) in enumerate(SENS):
    km, kp = 3 + 2 * i, 4 + 2 * i
    ws.cell(row=rr, column=1, value=name).font = BLACK
    ws.cell(row=rr, column=2, value=f"=Motor!{BLOCK_METRICS[km]['vpn_vt'][1]}")
    ws.cell(row=rr, column=3, value=f"=Motor!{BLOCK_METRICS[kp]['vpn_vt'][1]}")
    ws.cell(row=rr, column=4, value=f"=B{rr}-{base_vpn}")
    ws.cell(row=rr, column=5, value=f"=C{rr}-{base_vpn}")
    ws.cell(row=rr, column=6, value=f"=ABS(C{rr}-B{rr})+ROW()/1000000")
    for j in range(2, 7):
        ws.cell(row=rr, column=j).number_format = FMT["copm"]
    rr += 1
SENS_LAST = rr - 1
ws.cell(row=rr, column=1, value="VPN a 5 años con valor terminal del escenario base").font = BOLD
c = ws.cell(row=rr, column=2, value=f"={base_vpn}"); c.number_format = FMT["copm"]; c.font = BOLD
rr += 2
ws.cell(row=rr, column=1, value="Tornado ordenado (de mayor a menor rango)").font = SUB
rr += 1
for j, t in enumerate(["Orden", "Variable", "Δ VPN choque −", "Δ VPN choque +", "Rango"], 1):
    c = ws.cell(row=rr, column=j, value=t); c.font = HDR_FONT; c.fill = HDR_FILL
rr += 1
TOR_FIRST = rr
rng = f"$F${SENS_FIRST}:$F${SENS_LAST}"
for i in range(len(SENS)):
    ws.cell(row=rr, column=1, value=i + 1)
    ws.cell(row=rr, column=2, value=f"=INDEX($A${SENS_FIRST}:$A${SENS_LAST},MATCH(LARGE({rng},A{rr}),{rng},0))")
    ws.cell(row=rr, column=3, value=f"=INDEX($D${SENS_FIRST}:$D${SENS_LAST},MATCH(LARGE({rng},A{rr}),{rng},0))")
    ws.cell(row=rr, column=4, value=f"=INDEX($E${SENS_FIRST}:$E${SENS_LAST},MATCH(LARGE({rng},A{rr}),{rng},0))")
    ws.cell(row=rr, column=5, value=f"=ABS(D{rr}-C{rr})")
    for j in (3, 4, 5):
        ws.cell(row=rr, column=j).number_format = FMT["copm"]
    rr += 1
TOR_LAST = rr - 1
bc = BarChart()
bc.type = "bar"
bc.grouping = "clustered"
bc.overlap = 100
bc.title = "Tornado: Δ VPN 5 años con valor terminal (COP M)"
bc.add_data(Reference(ws, min_col=3, max_col=4, min_row=TOR_FIRST - 1, max_row=TOR_LAST), titles_from_data=True)
bc.set_categories(Reference(ws, min_col=2, min_row=TOR_FIRST, max_row=TOR_LAST))
bc.y_axis.title = "Δ VPN (COP M)"
bc.x_axis.scaling.orientation = "maxMin"
bc.height, bc.width = 9, 18
ws.add_chart(bc, f"H{SENS_FIRST - 2}")
rr += 1
ws.cell(row=rr, column=1, value="Lectura: el choque es relativo (p. ej. utilización 40 % → 32 % / 48 %; tasa 14,9 % → 11,9 % / 17,9 %). Ver la hoja Validacion para los experimentos que reducen la incertidumbre de las variables de mayor rango.").font = Font(name=FONT, italic=True, size=9)
ws.column_dimensions["A"].width = 46
for L in "BCDEF":
    ws.column_dimensions[L].width = 18

# ================================================================ MERCADO
ws = ws_mer
ws["A1"] = "Mercado: TAM, SAM y SOM"; ws["A1"].font = TITLE
ws["A2"] = "Tamaño en número de empresas y en cupo potencial. Los porcentajes de filtro son supuestos (ver Supuestos, sección 1)."
for j, t in enumerate(["Concepto", "Valor", "Unidad", "Cálculo"], 1):
    c = ws.cell(row=4, column=j, value=t); c.font = HDR_FONT; c.fill = HDR_FILL
S_ = sup_active
mrows = [
    ("Empresas activas en el registro mercantil", f"={S_('emp_activas')}", "empresas", "Dato RUES (F01)", "int"),
    ("Pequeñas + medianas empresas", f"={S_('pequenas')}+{S_('medianas')}", "empresas", "Confecámaras 2023 (F02)", "int"),
    ("Pymes como % del total", "=B6/B5", "%", "", "pct"),
    ("TAM · pymes que facturan electrónicamente", f"=B6*{S_('pct_fe')}", "empresas", "pymes × % factura electrónica", "int"),
    ("TAM · cupo rotativo potencial", f"=B8*{S_('cupo_prom')}", "COP M", "TAM empresas × cupo promedio", "copm"),
    ("SAM · pymes que venden a plazo y facturan electrónicamente", f"=B8*{S_('pct_b2b')}", "empresas", "TAM × % venta a plazo", "int"),
    ("SAM · de ellas sin crédito formal (brecha)", f"=B10*{S_('pct_sin_credito')}", "empresas", "SAM × % sin crédito formal (Anif)", "int"),
    ("SAM · cupo rotativo potencial", f"=B10*{S_('cupo_prom')}", "COP M", "SAM empresas × cupo promedio", "copm"),
    ("Segmento de entrada · pequeñas manufactureras que venden a plazo", f"={S_('pequenas')}*{S_('pct_manuf')}*{S_('pct_b2b')}*{S_('pct_fe')}", "empresas", "pequeñas × % manufactura × % plazo × % FE", "int"),
    ("SOM · registros acumulados a 2029", f"=Funnel!{CL(YCOL[3])}{item_loc_main['reg_acum'][1]}", "empresas", "Hoja Funnel", "int"),
    ("SOM · usuarios activos de tesorería a 2029", f"=Funnel!{CL(YCOL[3])}{item_loc_main['activos_tes'][1]}", "empresas", "Hoja Funnel", "int"),
    ("SOM · cupos activos a 2029", f"=Funnel!{CL(YCOL[3])}{item_loc_main['cupos_activos'][1]}", "cupos", "Hoja Funnel", "int"),
    ("SOM · cartera total a 2029", f"=Funnel!{CL(YCOL[3])}{item_loc_main['cartera_total'][1]}", "COP M", "Hoja Funnel", "copm"),
    ("Penetración de registros sobre SAM", "=IFERROR(B14/B10,0)", "%", "SOM registros / SAM", "pct"),
    ("Penetración de cupos activos sobre SAM", "=IFERROR(B16/B10,0)", "%", "SOM cupos / SAM", "pct"),
    ("Registros acumulados frente al segmento de entrada", "=IFERROR(B14/B13,0)", "x", "Si > 1, el plan exige salir de manufactura (previsto desde 2028)", "num2"),
]
rr = 5
for lab, f, u, calc, fm in mrows:
    ws.cell(row=rr, column=1, value=lab).font = BLACK
    c = ws.cell(row=rr, column=2, value=f); c.number_format = FMT[fm]
    ws.cell(row=rr, column=3, value=u)
    ws.cell(row=rr, column=4, value=calc).font = Font(name=FONT, size=9)
    rr += 1
rr += 1
ws.cell(row=rr, column=1, value="Precio frente al mercado").font = SUB
rr += 1
for j, t in enumerate(["Concepto", "Valor", "Unidad", "Comentario"], 1):
    c = ws.cell(row=rr, column=j, value=t); c.font = HDR_FONT; c.fill = HDR_FILL
rr += 1
pr0 = rr
prow = [
    ("Tasa Auro (cupo de fomento)", f"={S_('tasa_cliente')}", "% E.A.", "Prototipo"),
    ("Costo total para la empresa con comisión FNG (la parte que no asume el BFE)", f"={S_('tasa_cliente')}+{S_('fng_tarifa')}*(1+{S_('iva')})*(1-{S_('pct_fng_bfe')})", "% E.A. aprox.", "El prototipo muestra la comisión al firmar: conviene mostrar el costo total desde la oferta"),
    ("Interés bancario corriente consumo y ordinario (nov-2026)", f"={S_('ibc_nov26')}", "% E.A.", "Superfinanciera"),
    ("Tasa de usura (nov-2026)", f"={S_('usura_nov26')}", "% E.A.", "Superfinanciera"),
    ("Tasa de usura (oct-2026)", f"={S_('usura_oct26')}", "% E.A.", "El prototipo cita rotativos hasta 28,9 %: supera este techo"),
    ("Ahorro anual para una empresa que usa $12 M todo el año vs. el IBC", f"=12*({S_('ibc_nov26')}-B{pr0+1})", "COP M", "Ilustrativo"),
    ("Spread de la tasa Auro sobre el fondeo 2027 (sin compensación)", f"={S_('tasa_cliente')}-Ingresos_Margen!{CL(YCOL[1])}{item_loc_main['tasa_fondeo'][1]}", "p.p.", "Clave del caso: margen estrecho con la tasa de política en 12,25 %"),
    ("Spread sobre el fondeo 2027 con compensación de tasa", f"={S_('tasa_cliente')}+{S_('subsidio_fondeo')}-Ingresos_Margen!{CL(YCOL[1])}{item_loc_main['tasa_fondeo'][1]}", "p.p.", "Compensación = supuesto a negociar (ver Validacion)"),
]
for lab, f, u, com in prow:
    ws.cell(row=rr, column=1, value=lab).font = BLACK
    c = ws.cell(row=rr, column=2, value=f); c.number_format = FMT["pct2"] if "%" in u or "p.p." in u else FMT["copm"]
    ws.cell(row=rr, column=3, value=u)
    ws.cell(row=rr, column=4, value=com).font = Font(name=FONT, size=9)
    rr += 1
ws.column_dimensions["A"].width = 70
ws.column_dimensions["B"].width = 16
ws.column_dimensions["C"].width = 14
ws.column_dimensions["D"].width = 70

# ================================================================ EFICIENCIA IA
ws = ws_efi
ws["A1"] = "Valor de eficiencia de la IA (escenario activo)"; ws["A1"].font = TITLE
ws["A2"] = "Compara el costo de originar y atender con agentes frente a un proceso manual equivalente, el tiempo de respuesta y la conversión. Sin agentes: cada solicitud la revisa un analista y cumplimiento procesa menos casos por persona."
for j, t in enumerate(["Concepto", "Unidad", "2027", "2028", "2029", "Total"], 1):
    c = ws.cell(row=4, column=j, value=t); c.font = HDR_FONT; c.fill = HDR_FILL


def A(key, y):
    return ann(key, y)


erows = []


def er(lab, unit, fn, fm="copm", bold=False):
    erows.append((lab, unit, fn, fm, bold))


er("Solicitudes de cupo", "solicitudes", lambda y: f"={A('solicitudes', y)}", "int")
er("Cupos activados", "cupos", lambda y: f"={A('cupos_nuevos', y)}", "int")
er("Con agentes · costo analistas de crédito", "COP M", lambda y: f"={A('c_analistas', y)}")
er("Con agentes · costo cumplimiento", "COP M", lambda y: f"={A('c_cump', y)}")
er("Con agentes · datos de terceros por solicitud", "COP M", lambda y: f"={A('d_sol', y)}")
er("Con agentes · IA de activación del cupo", "COP M", lambda y: f"={A('ia_act', y)}")
er("Con agentes · costo total de originación", "COP M", lambda y: "=SUM({c}7:{c}10)", bold=True)
er("Con agentes · costo por cupo activado", "COP M/cupo", lambda y: "=IFERROR({c}11/{c}6,0)", "num2", True)
er("Sin agentes · analistas (100 % de solicitudes, productividad manual)", "COP M", lambda y: f"=MAX({S_('min_analistas')}*12,{A('solicitudes', y)}/{S_('prod_sin')})*{S_('costo_analista')}")
er("Sin agentes · cumplimiento", "COP M", lambda y: f"=({S_('cump_base')}*12+{A('solicitudes', y)}/{S_('ratio_cump_sin')})*{S_('costo_cump')}")
er("Sin agentes · datos de terceros por solicitud", "COP M", lambda y: "={c}9")
er("Sin agentes · costo total de originación", "COP M", lambda y: "=SUM({c}13:{c}15)", bold=True)
er("Sin agentes · costo por cupo activado", "COP M/cupo", lambda y: "=IFERROR({c}16/{c}6,0)", "num2", True)
er("Ahorro en originación", "COP M", lambda y: "={c}16-{c}11", bold=True)
er("Soporte con agentes", "COP M", lambda y: f"={A('c_soporte', y)}")
er("Soporte sin agentes (clientes activos / ratio manual)", "COP M", lambda y: f"=MAX({S_('min_soporte')},{A('activos_tes', y)}/{S_('ratio_sop_sin')})*12*{S_('costo_soporte')}" if False else f"=MAX({S_('min_soporte')},AVERAGE(Funnel!{CL(FIRST_M_COL+(y-1)*12)}{item_loc_main['activos_tes'][1]}:{CL(FIRST_M_COL+y*12-1)}{item_loc_main['activos_tes'][1]})/{S_('ratio_sop_sin')})*12*{S_('costo_soporte')}")
er("Ahorro en soporte", "COP M", lambda y: "={c}20-{c}19", bold=True)
er("Costo de IA total (todos los agentes)", "COP M", lambda y: f"={A('c_ia', y)}")
er("Ahorro operativo neto de IA (originación + soporte − costo IA no de activación)", "COP M", lambda y: "={c}18+{c}21-({c}22-{c}10)", bold=True)
er("Conversión: cupos que se perderían sin agentes (fricción)", "cupos", lambda y: "={c}6*" + S_('friccion_sin'), "int")
er("Margen después de riesgo por cupo activo-año", "COP M/cupo", lambda y: f"=IFERROR({A('margen_riesgo', y)}/AVERAGE(Funnel!{CL(FIRST_M_COL+(y-1)*12)}{item_loc_main['cupos_activos'][1]}:{CL(FIRST_M_COL+y*12-1)}{item_loc_main['cupos_activos'][1]}),0)", "num2")
er("Valor de conversión (margen de los cupos que sí se activan gracias a los agentes, medio año promedio)", "COP M", lambda y: "={c}24*{c}25*0.5", bold=True)
er("Valor total atribuible a los agentes", "COP M", lambda y: "={c}23+{c}26", bold=True)
er("Valor por cada peso invertido en IA", "x", lambda y: "=IFERROR({c}27/{c}22,0)", "x", True)
rr = 5
for lab, unit, fn, fm, bold in erows:
    ws.cell(row=rr, column=1, value=lab).font = BOLD if bold else BLACK
    ws.cell(row=rr, column=2, value=unit)
    for y in (1, 2, 3):
        L = CL(2 + y)
        f = fn(y).replace("{c}", L)
        c = ws.cell(row=rr, column=2 + y, value=f); c.number_format = FMT[fm]; c.font = BOLD if bold else BLACK
    if fm in ("copm", "int"):
        c = ws.cell(row=rr, column=6, value=f"=SUM(C{rr}:E{rr})"); c.number_format = FMT[fm]
    rr += 1
rr += 1
ws.cell(row=rr, column=1, value="Experiencia: tiempo de respuesta a la solicitud").font = SUB
rr += 1
ws.cell(row=rr, column=1, value="Con agentes (días hábiles)"); c = ws.cell(row=rr, column=3, value=f"={S_('dias_ia')}"); c.number_format = FMT["num1"]; rr += 1
ws.cell(row=rr, column=1, value="Proceso tradicional (días hábiles)"); c = ws.cell(row=rr, column=3, value=f"={S_('dias_sin')}"); c.number_format = FMT["num1"]; rr += 1
ws.cell(row=rr, column=1, value="Reducción del tiempo de respuesta"); c = ws.cell(row=rr, column=3, value=f"=1-C{rr-2}/C{rr-1}"); c.number_format = FMT["pct"]; rr += 1
ws.cell(row=rr, column=1, value="Analistas: casos por persona al mes con copiloto vs. manual"); c = ws.cell(row=rr, column=3, value=f"={S_('prod_ia')}/{S_('prod_sin')}"); c.number_format = FMT["x"]; rr += 1
ws.cell(row=rr, column=1, value="Soporte: clientes por persona con agentes vs. manual"); c = ws.cell(row=rr, column=3, value=f"={S_('ratio_sop_ia')}/{S_('ratio_sop_sin')}"); c.number_format = FMT["x"]; rr += 1
rr += 1
ws.cell(row=rr, column=1, value="Nota: el valor de conversión asume que un cupo activado genera en su primer año, en promedio, medio año de margen. La fricción sin agentes es un supuesto a validar con el grupo de control del piloto.").font = Font(name=FONT, italic=True, size=9)
ws.column_dimensions["A"].width = 78
ws.column_dimensions["B"].width = 12
for L in "CDEF":
    ws.column_dimensions[L].width = 14

# ================================================================ FUENTES
FUENTES = [
    ("F01", "RUES / Confecámaras vía INCP y Radio Nacional", "1.805.564 empresas activas al cierre de 2025; 1.799.802 mipymes y 5.762 grandes", "https://incp.org.co/wp-content/uploads/2026/11/Microempresas-Muestra-Estudiada.pdf ; https://radionacional.co/actualidad/economia/crecimiento-empresarial-colombia-2025", "Verificado (prensa y gremio citando RUES)"),
    ("F02", "Confecámaras vía La República", "2023: 106.120 pequeñas (6,1 %) y 27.238 medianas (1,6 %) de 1.734.636 empresas", "https://www.larepublica.co/empresas/del-total-de-las-empresas-que-operan-en-colombia-7-7-son-pequenas-y-medianas-3958564", "Verificado (dato 2023)"),
    ("F03", "Confecámaras · Dinámica de creación de empresas 2025-I", "173.907 empresas creadas en el primer semestre de 2025 (+1,9 %)", "https://confecamaras.org.co/wp-content/uploads/2025/08/2025-1-dinamica-de-creacion-de-empresas.pdf", "Verificado"),
    ("F04", "DIAN vía El Tiempo, Portafolio y Cambio", "1,16 M facturadores electrónicos (may-2025); 1,3 M con 56,3 % personas jurídicas", "https://www.eltiempo.com/economia/sectores/van-mas-de-1-450-cierres-de-empresas-por-no-facturar-de-manera-electronica-como-evitar-sanciones-para-su-negocio-3476190 ; https://cambiocolombia.com/contenido-especial/articulo/2025/6/facturacion-electronica-en-colombia-mas-control-menos-evasion", "Verificado (prensa citando DIAN)"),
    ("F05", "Anif vía Portafolio", "Solo 40 % de las pymes ha accedido a crédito formal", "https://www.portafolio.co/negocios/empresas/creditos-empresariales-estrategias-para-retomar-el-control-financiero-635963", "Verificado (prensa); confirmar en Encuesta MiPyme Anif 2025-2026"),
    ("F06", "Superintendencia Financiera · Res. 1707 de 2026", "IBC consumo y ordinario nov-2026: 18,89 % E.A.; usura 28,34 %", "https://www.cerlatam.com/?p=38734 ; https://www.portafolio.co/economia/finanzas/creditos-de-consumo-tendran-nuevo-tope-de-usura-en-noviembre-superfinanciera-lo-certifico-en-28-34-efectivo-anual-505461", "Verificado"),
    ("F07", "Superintendencia Financiera · Res. 1472 de 2026", "IBC oct-2026: 19,06 % E.A.; usura 28,59 %", "https://www.portafolio.co/economia/finanzas/tasa-de-usura-baja-en-octubre-y-establece-nuevo-limite-para-el-cobro-de-intereses-a-los-bancos-503770", "Verificado"),
    ("F08", "Banco de la República y BBVA Research", "Tasa de política 12,25 % (oct-2026, votación 4-3); BBVA prevé estabilidad hasta sep-2027 y recortes graduales después", "https://www.bbvaresearch.com/publicaciones/colombia-banrep-mantuvo-la-tasa-en-1225-en-su-reunion-de-octubre/ ; https://www.banrep.gov.co/es/noticias/calendario-actividades-junta-directiva/reunion-octubre-2026", "Verificado; la senda 2028-2029 es supuesto propio"),
    ("F09", "Bancóldex · Circular línea Liquidez corto plazo 2026 y modificación 1", "Redescuento al intermediario IBR NMV + 1,50 %, luego + 1,95 %", "https://www.bancoldex.com/sites/default/files/2026-02/Modificacio%CC%81n%201%20-%20Circular%20Li%CC%81nea%20de%20cre%CC%81dito%20liquidez%20corto%20plazo%202026.pdf", "Verificado (referencia de fondeo de segundo piso)"),
    ("F10", "Fondo Nacional de Garantías · tarifas publicadas por Banco Serfinanza", "Cobertura 50 %: EMP 080 2,15 % + IVA (may-2025); EMP 309 3,89 % + IVA y EMP 214 4,40 % + IVA (mar-2026); cobro anual anticipado", "https://bancoserfinanza.com/wp-content/uploads/2026/03/TARIFAS-GARANTIAS-2-DE-MARZO-2026.pdf ; https://bancoserfinanza.com/wp-content/uploads/2025/05/TARIFAS-GARANTIAS-15-DE-MAYO-2025.pdf", "Verificado (tarifas vía intermediario; confirmar con FNG)"),
    ("F11", "Superfinanciera vía Portafolio y Valora Analitik", "Indicador de mora cartera comercial 3,1 % (may-2026); cartera pyme −5,4 % real anual en 1T-2026", "https://www.portafolio.co/economia/finanzas/continua-mejorando-la-calidad-de-la-cartera-y-los-buenos-resultados-de-los-bancos-al-cierre-de-mayo-498459 ; https://www.valoraanalitik.com/?p=584163", "Verificado (no es PD de pequeñas empresas)"),
    ("F12", "Siigo vía Portafolio y Actualícese", "~1,3 M pymes y contadores en 6 países; ~350.000 pymes en Colombia (fecha no confirmada)", "https://www.portafolio.co/negocios/empresas/siigo-compra-bsale-y-anuncia-inversion-de-us-100-millones-para-acelerar-su-expansion-en-latinoamerica-503902", "Verificado parcialmente (autorreportado)"),
    ("F13", "Anthropic · precios de la API", "Opus 5.5 US$4/20; Sonnet 5.5 US$2/10; Haiku 5.5 US$0,10/0,50 por M tokens; lectura de caché Opus 0,20 y Sonnet 0,10", "https://platform.claude.com/docs/en/about-claude/pricing (consultado vía referencia de la API, caché 2026-11-03)", "Verificado"),
    ("F14", "Equipo Auro · consumo de IA por agente", "Llamadas, tokens y eventos por agente y perfil de cliente", "entregables/_insumos/consumo_ia_por_agente.md (arquitectura, sección 12)", "Supuesto de diseño interno"),
    ("F15", "TRM vía Portafolio, Diario del Sur y Bancolombia", "TRM 3.183 (3-nov-2026) y 3.236 (5-nov-2026); rango esperado 3.120-3.300 en noviembre", "https://www.portafolio.co/economia/finanzas/dolar-en-colombia-podria-alcanzar-los-3-250-esta-semana-asi-cotiza-la-divisa-este-martes-3-de-noviembre-505595", "Verificado (prensa)"),
    ("F16", "Decreto 1469 de 2025 y portales de empleo", "Salario mínimo 2026 $1.750.905; analista de crédito $3,5-4 M/mes en ofertas de Bogotá", "https://www.infobae.com/colombia/2026/01/12/salario-minimo-de-2026-esto-es-lo-que-deben-pagar-las-empresas-a-los-trabajadores-colombianos-en-la-primera-quincena-del-ano/ ; https://www.elempleo.com/co/ofertas-empleo/bogota/trabajo-analista-credito", "Verificado (referencia salarial no estadística)"),
    ("F17", "Ley 2277 de 2022 (reforma tributaria)", "Tarifa general de renta 35 %; sobretasa de 5 p.p. para instituciones financieras 2023-2027", "https://www.funcionpublica.gov.co/eva/gestornormativo/norma.php?i=199883", "Verificado (norma; confirmar aplicación al BFE con tributaria)"),
    ("F18", "Banco de la República · Reporte de la situación del crédito", "Demanda de crédito estable para pequeñas empresas en bancos (dic-2025)", "https://banrep.gov.co/es/publicaciones-investigaciones/reporte-situacion-credito-colombia/marzo-2026", "Verificado (contexto)"),
    ("F19", "Superfinanciera · Circular Básica Contable, capítulo II", "Pérdida esperada = PD × exposición × pérdida dado el incumplimiento, horizonte 12 meses", "https://www.ambitojuridico.com/sites/default/files/2022-05/cap02riesgocrediticio.doc", "Verificado (metodología)"),
    ("F20", "Prototipo Auro (18 pantallas)", "Cupo hasta $60 M, 14,9 % E.A., hasta 6 meses por uso, garantía 50 %, revisión humana > $100 M, destinos permitidos", "entregables/_insumos/pantallas_prototipo.md", "Supuesto de producto (valores de ejemplo)"),
    ("F21", "Superfinanciera y Banca de las Oportunidades · RIF 2024", "96,3 % de adultos con algún producto; ~35 % con crédito (personas, no empresas)", "https://www.superfinanciera.gov.co/publicaciones/10115642/para-2024-el-963-de-los-colombianos-adultos-tenia-al-menos-un-producto-de-deposito-o-credito/", "Verificado (contexto)"),
    ("F22", "Confecámaras vía INCP", "Pequeñas ≈ 4,2 % y medianas ≈ 1 % del tejido empresarial (proporciones recientes)", "https://incp.org.co/wp-content/uploads/2026/11/Microempresas-Muestra-Estudiada.pdf", "Verificado; difiere del conteo 2023 (F02): reconciliar con RUES"),
]
ws = ws_fue
ws["A1"] = "Fuentes"; ws["A1"].font = TITLE
ws["A2"] = "Consultadas el 12 de noviembre de 2026. Las cifras de prensa citan a la entidad oficial; antes del comité, confirmar en el documento original."
for j, t in enumerate(["ID", "Entidad / documento", "Dato usado", "URL", "Tipo / calidad"], 1):
    c = ws.cell(row=4, column=j, value=t); c.font = HDR_FONT; c.fill = HDR_FILL
for i, row in enumerate(FUENTES):
    for j, v in enumerate(row, 1):
        c = ws.cell(row=5 + i, column=j, value=v); c.font = BLACK; c.alignment = WRAP
ws.column_dimensions["A"].width = 6
ws.column_dimensions["B"].width = 40
ws.column_dimensions["C"].width = 60
ws.column_dimensions["D"].width = 70
ws.column_dimensions["E"].width = 34

# ================================================================ VALIDACIÓN
ws = ws_val
ws["A1"] = "Supuestos críticos y plan de validación"; ws["A1"].font = TITLE
ws["A2"] = "Ordenados por impacto en el VPN (ver tornado en Escenarios). Cada hipótesis tiene un experimento en el piloto de 6 meses y un umbral que decide si se escala."
hdr = ["#", "Supuesto crítico (hipótesis)", "Valor en el modelo (activo)", "Experimento", "Métrica", "Umbral para escalar", "Cuándo", "Decisión si falla"]
for j, t in enumerate(hdr, 1):
    c = ws.cell(row=4, column=j, value=t); c.font = HDR_FONT; c.fill = HDR_FILL; c.alignment = WRAP
VAL = [
    ("La tasa del cupo deja margen sobre el fondeo del BFE", f'=TEXT({S_("tasa_cliente")},"0.0%")&" vs fondeo 2027 "&TEXT(Ingresos_Margen!{CL(YCOL[1])}{item_loc_main["tasa_fondeo"][1]},"0.0%")',
     "Mesa con tesorería del BFE y MinCIT: costo real de fondeo de la línea y opción de compensación de tasa; prueba de precio (14,9 % vs 16,5 %) con preaprobados del piloto", "Spread tasa − fondeo; conversión por nivel de precio", "Spread ≥ 4 p.p. o compensación aprobada; conversión cae < 20 % con el precio alto", "Antes del mes 1 (decisión de comité) y meses 2-4", "Indexar la tasa a IBR + margen o pedir compensación de tasa"),
    ("Utilización promedio del cupo", f'=TEXT({S_("utilizacion")},"0%")',
     "Medir saldo diario / cupo de las primeras cohortes", "Utilización promedio a 90 días por cohorte", "≥ 30 %", "Meses 3-6", "Bajar cupo inicial o subir por uso; revisar casos de uso permitidos"),
    ("Conversión de preaprobado a cupo", f'=TEXT({S_("conv_inicial")},"0%")&" al mes + "&TEXT({S_("conv_tardia")},"0.0%")&"/mes"',
     "A/B: alerta de hueco con oferta de cupo vs. sin oferta; guion de activación de 10 minutos", "% de preaprobados que activan en 60 días", "≥ 25 %", "Meses 2-6", "Revisar momento de la oferta y fricción documental"),
    ("Pérdida esperada (PD de pequeñas empresas evaluadas con facturas)", f'=TEXT({S_("pd")},"0.0%")&" PD; LGD "&TEXT({S_("lgd")},"0%")',
     "Backtesting del modelo con facturas + centrales sobre cartera histórica de intermediarios; seguimiento de mora 30+ de las cohortes del piloto", "Mora 30+ a 6 meses; PD estimada vs. observada", "Mora 30+ ≤ 3 % a 6 meses", "Meses 1-2 (backtesting) y 6-12", "Ajustar cupo, política o exigir más garantía"),
    ("Activación de datos: la pyme conecta 12 meses de facturas", f'=TEXT({S_("pct_activacion")},"0%")',
     "Piloto cerrado con gremio manufacturero y un software contable aliado; medir por canal de conexión", "% de registros con 12 meses completos en 7 días", "≥ 50 %", "Meses 1-3", "Priorizar conectores o asistencia humana en onboarding"),
    ("CAC por registro", f'=TEXT({S_("cac")},"#,##0")&" COP"',
     "Probar tres canales: gremios, contadores, software contable (referidos)", "Costo por registro activo y por cupo activado", "≤ 400.000 COP por usuario activo", "Meses 1-6", "Concentrar en el canal más barato; frenar pauta"),
    ("Costo de IA por cliente", f'=TEXT(Costos_IA!H{TOT_ROW},"0.00")&" / "&TEXT(Costos_IA!I{TOT_ROW},"0.00")&" US$ (N1/N2) × "&TEXT({S_("mult_ia")},"0.0")',
     "Telemetría de tokens por agente y por interacción desde el día 1; evals de calidad al bajar de modelo", "US$ por cliente-mes por perfil", "≤ 2 × lo diseñado", "Meses 1-3", "Batch nocturno, más caché, bajar modelo donde las evals lo permitan"),
    ("Revisión humana y productividad del analista con copiloto", f'=TEXT({S_("pct_rev_humana")},"0%")&" a persona; "&{S_("prod_ia")}&" casos/mes"',
     "Medir casos transferidos, tiempo por caso y acuerdo analista-agente", "% a revisión humana; casos por analista", "≤ 20 % y ≥ 45 casos/mes", "Meses 2-6", "Ajustar umbrales de anomalía y el expediente"),
    ("La empresa acepta pagar la comisión FNG (costo total)", f'=TEXT(Mercado!B{pr0+1},"0.0%")&" costo total"',
     "Mostrar costo total desde la oferta y medir abandono en el paso de firma", "Abandono en firma", "≤ 15 %", "Meses 2-4", "BFE asume parte de la comisión (ver pct_fng_bfe)"),
]
rr = 5
for i, v in enumerate(VAL, 1):
    ws.cell(row=rr, column=1, value=i)
    for j, t in enumerate(v, 2):
        c = ws.cell(row=rr, column=j, value=t); c.alignment = WRAP; c.font = BLACK
    rr += 1
widths = [4, 40, 28, 55, 30, 28, 22, 36]
for j, w in enumerate(widths, 1):
    ws.column_dimensions[CL(j)].width = w

# ================================================================ PORTADA
ws = ws_port
ws["A1"] = "Modelo financiero a 3 años · Auro by BFE"; ws["A1"].font = Font(name=FONT, bold=True, size=18, color="1F3864")
ws["A2"] = "Tesorero digital con IA para pequeñas empresas que venden a plazo + cupo rotativo de fomento. Caso ficticio de prueba técnica; datos de mercado reales con fuente. Fecha de corte: 12 de noviembre de 2026."
ws["A2"].alignment = WRAP
ws.merge_cells("A2:F2"); ws.row_dimensions[2].height = 32
ws["A4"] = "Cómo leerlo"; ws["A4"].font = SUB
inst = [
    "1. Elija el escenario en Supuestos!B3 (celda amarilla). Todas las hojas de cálculo usan la columna G (Activo) de Supuestos.",
    "2. Cambie solo celdas en azul (inputs). Todo lo que está en negro es fórmula; en verde, vínculos a otra hoja.",
    "3. Unidades: COP M = millones de pesos colombianos. Tasas en % efectivo anual salvo indicación. Mes 1 = enero de 2027. El caso se evalúa a 3 años (2027-2029); 2030-2031 es una extensión indicativa para payback y valor terminal.",
    "4. Cada supuesto indica si es dato verificado, derivado de un dato o supuesto propio, con su fuente (hoja Fuentes).",
    "5. Escenarios compara pesimista, base y optimista calculados en paralelo (hoja Motor) y muestra el tornado de sensibilidad.",
    "6. Validacion lista los supuestos críticos, el experimento, la métrica y el umbral para escalar.",
]
for i, t in enumerate(inst):
    ws.cell(row=5 + i, column=1, value=t).font = BLACK
ws["A12"] = "Convención de colores"; ws["A12"].font = SUB
ws["A13"] = "Input editable"; ws["B13"] = 123; ws["B13"].font = BLUE
ws["A14"] = "Fórmula"; ws["B14"] = "=B13*2"; ws["B14"].font = BLACK
ws["A15"] = "Vínculo a otra hoja"; ws["B15"] = "=Supuestos!E7"; ws["B15"].font = GREEN
ws["A16"] = "Supuesto clave o resultado"; ws["B16"].fill = KEY_FILL
ws["A17"] = "Selector de escenario"; ws["B17"].fill = YELLOW
ws["A19"] = "Estructura"; ws["A19"].font = SUB
struct = [("Supuestos", "Todos los inputs con escenario, tipo y fuente; tabla de consumo de IA por agente y precios."),
          ("Fuentes", "Referencias con URL y fecha."), ("Mercado", "TAM, SAM, segmento de entrada, SOM y precio frente al mercado."),
          ("Funnel", "36 meses: registros → activos → preaprobados → solicitudes → cupos → utilización → cartera."),
          ("Ingresos_Margen", "Intereses, fondeo, comisión FNG, margen financiero neto, comisiones, pérdida esperada."),
          ("Costos_IA", "Tokens × precio por agente y por perfil de cliente."),
          ("Costos", "Inversión amortizada, personas por volumen, IA, infraestructura, datos, adquisición."),
          ("Eficiencia_IA", "Costo por originación con y sin agentes, soporte, tiempo de respuesta y conversión."),
          ("PyG_Flujo", "P&G mensual y anual, flujo para el accionista, VPN, TIR y payback."),
          ("Escenarios", "Pesimista / base / optimista y tornado sobre 6 variables."),
          ("Validacion", "Supuestos críticos y plan de validación."),
          ("Motor_Params / Motor", "Motor de cálculo paralelo para escenarios y sensibilidad (mismas fórmulas).")]
for i, (a, b) in enumerate(struct):
    ws.cell(row=20 + i, column=1, value=a).font = BOLD
    ws.cell(row=20 + i, column=2, value=b).font = BLACK
r = 20 + len(struct) + 1
ws.cell(row=r, column=1, value="Resultados del escenario activo").font = SUB
ws.cell(row=r, column=2, value="=Supuestos!B3").font = BOLD
r += 1
res = [
    ("Inversión inicial (COP M)", f"={sup_active('inv_total')}", "copm"),
    ("Cupos activos a dic-2029", f"=Funnel!{CL(YCOL[3])}{item_loc_main['cupos_activos'][1]}", "int"),
    ("Cartera total a dic-2029 (COP M)", f"=Funnel!{CL(YCOL[3])}{item_loc_main['cartera_total'][1]}", "copm"),
    ("Ingresos netos 3 años (COP M)", f"=Ingresos_Margen!{CL(TCOL)}{item_loc_main['ing_netos'][1]}", "copm"),
    ("Utilidad neta 3 años (COP M)", f"=PyG_Flujo!{CL(TCOL)}{item_loc_main['un'][1]}", "copm"),
    ("Utilidad neta 2029 (COP M)", f"=PyG_Flujo!{CL(YCOL[3])}{item_loc_main['un'][1]}", "copm"),
    ("Costo de IA 3 años (COP M)", f"=Costos!{CL(TCOL)}{item_loc_main['c_ia'][1]}", "copm"),
    ("VPN 3 años sin valor terminal (COP M)", f"=PyG_Flujo!{MAIN_METRICS['vpn'][1]}", "copm"),
    ("Extensión: utilidad neta 2031 (COP M)", f"=PyG_Flujo!{CL(YCOL[5])}{item_loc_main['un'][1]}", "copm"),
    ("VPN 5 años con valor terminal (COP M)", f"=PyG_Flujo!{MAIN_METRICS['vpn_vt'][1]}", "copm"),
    ("Payback operativo (mes)", f"=PyG_Flujo!{MAIN_METRICS['payback_op'][1]}", "int"),
    ("Payback del flujo al accionista (mes)", f"=PyG_Flujo!{MAIN_METRICS['payback'][1]}", "int"),
]
for a, f, fm in res:
    ws.cell(row=r, column=1, value=a).font = BLACK
    c = ws.cell(row=r, column=2, value=f); c.number_format = FMT[fm]; c.font = BOLD
    r += 1
r += 1
ws.cell(row=r, column=1, value="Controles").font = SUB
r += 1
ws.cell(row=r, column=1, value="Motor reproduce el escenario activo")
ws.cell(row=r, column=2, value=f"=Escenarios!D{CHECK_ROW}").font = BOLD
r += 1
ws.cell(row=r, column=1, value="Costo IA por agente cuadra con hoja Costos")
ws.cell(row=r, column=2, value=f"=Costos_IA!D{AG36_TOTAL+1}").font = BOLD
r += 1
sp = item_loc_main["stock_pre"][1]
ws.cell(row=r, column=1, value="Stocks del embudo no negativos")
ws.cell(row=r, column=2, value=f'=IF(MIN(Funnel!C{sp}:{CL(LAST_M_COL)}{sp})>=0,"OK","REVISAR")').font = BOLD
r += 1
ws.cell(row=r, column=1, value="Tasa al cliente bajo la usura vigente")
ws.cell(row=r, column=2, value=f'=IF(Mercado!B{pr0+1}<{sup_active("usura_nov26")},"OK","REVISAR")').font = BOLD
ws.column_dimensions["A"].width = 52
ws.column_dimensions["B"].width = 95

# fuentes por defecto en todas las hojas
for wsx in wb.worksheets:
    for row in wsx.iter_rows():
        for c in row:
            if c.font is None or c.font.name != FONT:
                f0 = c.font
                c.font = Font(name=FONT, size=f0.size or 10, bold=f0.bold, italic=f0.italic, color=f0.color)

from openpyxl.workbook.properties import CalcProperties
wb.calculation = CalcProperties(fullCalcOnLoad=True)
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
wb.save(OUT)
print("OK", OUT)
