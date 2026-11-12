# Auro by BFE · Proceso de diseño con IA

Cómo se construyó la propuesta, qué decidí yo y qué hizo la IA. El proceso siguió un doble diamante: primero abrir y cerrar el problema, después abrir y cerrar la solución.

## 1. Descubrir: abrir el problema

Antes de proponer nada pedí investigar con método: tamaño de mercado (TAM, SAM, SOM), referentes del mundo y competidores en Colombia. Mis decisiones en esta fase fueron sobre todo descartes y preguntas:

- **Descarté el descuento de facturas** como producto de entrada.
- **Pregunté cómo llega un banco de segundo piso a una pyme que no conoce.** Esa pregunta reorientó la búsqueda.
- **Pedí revisar las microempresas** y las brechas que solo un banco de fomento puede cubrir.

## 2. Definir: cerrar en una apuesta

- **Idea central (mía):** llegar a la pyme resolviéndole un problema de plata y ofrecer el crédito dentro de esa solución.
- **Producto:** un tesorero digital gratuito con un cupo rotativo de fomento. Madura a la empresa y le presta en el proceso.
- **Restricciones:** 100 % digital, software propio del banco y sin competir con el software contable.
- **Segmento:** pequeñas empresas que venden a plazo a otras empresas. Lo propuso la IA; lo acepté después de cuestionarlo.

## 3. Desarrollar: marca

Abrí varias rondas de opciones y cerré cada una con un criterio explícito:

- **Nombre:** descarté los que llevaban "IA" y pedí uno corto, moderno y con personalidad. Elegí **Auro**, con "by BFE" para anclarlo al banco.
- **Personalidad:** un asistente que trata de "tú", neutro en género, previsor, claro y franco. Siempre dice que es una IA y nunca presiona ni promete aprobaciones.
- **Color:** rechacé dos paletas por opacas y elegí lila y oro, "con más luz".
- **Logo:** propuse que el icono fuera parte de una letra. Quedó la "o" con un punto dorado en órbita, que funciona sola como icono y como avatar de Auro.
- **Tipografía:** Outfit en todo el producto, a propuesta de la IA.

## 4. Entregar: producto

Iteré pantalla por pantalla, con criterio de usuaria:

- **Flujo (dictado por mí):** registro con NIT → confirmar o corregir datos → contraseña → carga de información → alertas gratis → preaprobado → activación → uso → plan del mes.
- **Estructura:** menú lateral fijo, fondo blanco e Inicio reorganizado, con el cupo preaprobado junto a la gráfica de caja.
- **Proceso o conversación:** rechacé las primeras versiones porque no se entendía cuál de las dos era. Definí que el agente vive en "Hablar con Auro", a pantalla completa y con historial, y que cada acción abre ahí una conversación con el mensaje ya escrito.
- **Realismo del agente:** mis preguntas sobre la DIAN llevaron a quitar estados que Auro no podría conocer.
- **Responsabilidad:**
  - La aprobación la hace la política del banco desde el primer día.
  - Las anomalías, Auro ayuda a corregirlas o pasa el caso a una persona.
  - Auro redacta, pero no envía mensajes ni mueve plata.
- **Para quien evalúa:** todos los botones tienen acción y los tres casos de excepción están a un clic desde el menú.

## 5. Validar y entregar el paquete

- **Revisión estricta contra la rúbrica.** La primera exportación no cumplía por dos razones: traía una sola pantalla y no era responsive. La segunda traía las 18 pantallas, pero los enlaces entre ellas no funcionaban.
- **Prototipo navegable y responsive:**
  - Convertí la exportación en un sitio estático con una página por pantalla y una capa responsive (menú superior en celular).
  - Lo probé de forma automática: 180 enlaces sin fallas y los tres caminos de excepción recorridos de punta a punta.
  - Lo publiqué en Render.
- **Arquitectura agéntica:**
  - Documenté los agentes, sus permisos, la memoria, los traspasos a personas, los controles, los evals y las integraciones.
  - Mantuve la regla central del prototipo: la IA informa y propone; el crédito y el cumplimiento los deciden la política del banco y las personas.
- **Modelo financiero y resumen ejecutivo:**
  - Están construidos sobre datos de mercado con fuente citada.
  - Separan lo verificado de lo supuesto e incluyen un plan para validar las hipótesis críticas.

## Reparto del trabajo

**Yo decidí** el problema, el producto, las restricciones, la marca, la experiencia y los límites de autonomía del agente.

**La IA** investigó, propuso opciones, redactó textos, construyó las pantallas y los documentos, y automatizó las pruebas. Revisé cada entregable antes de incluirlo.

Varias cifras siguen siendo supuestos sin validar con el banco. Están marcadas como tales en el modelo financiero y en la arquitectura.
