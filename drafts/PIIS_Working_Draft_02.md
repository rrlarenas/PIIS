# PIIS — Portable Integration Interface Specification

**Working Draft 02 — Documento de discusión técnica**  
**Fecha:** 28 de octubre de 2026  
**Estado:** Propuesta exploratoria; no es un RFC publicado ni un Internet-Draft registrado  
**Idioma de trabajo:** español  
**Nombre y sigla:** provisionales  
**Cambios desde Draft 01:** neutralidad estricta respecto de productos y lenguajes de implementación; primacía del resultado End-to-End completo; medición de CPU, RAM, throughput, recuperación y costo con alcance de solución integral; prohibición de descontar penalizaciones o ventajas arquitectónicas; condiciones de competencia transparentes; motivación explícita en la libertad de elección del usuario y la diferenciación mediante resultados; consolidación de la visión de migración plug-and-play basada en contrato y conformidad.

## Resumen (Abstract)

Este documento propone un marco abierto e independiente de fabricantes para definir interfaces de integración mediante una representación funcional portable y un contrato de comportamiento observable. Su objetivo es que motores, buses o plataformas de integración diferentes puedan interpretar una misma definición y materializarla usando sus tecnologías, lenguajes y arquitecturas propias, preservando la funcionalidad, los resultados y los efectos exigidos por ese contrato.

La propuesta incluye el reconocimiento explícito de capacidades, la evaluación de conformidad, la migración de interfaces existentes y un mecanismo independiente para comparar implementaciones que satisfagan el mismo contrato. La medida prioritaria de experiencia operativa es el tiempo End-to-End completo, desde el estímulo de entrada acordado hasta la constatación de todos los resultados y efectos obligatorios. Se medirán además throughput conforme, CPU, RAM, escalabilidad, recuperación, integridad funcional, costos y esfuerzo de migración. Las diferencias de arquitectura no son desviaciones que deban descontarse: son ventajas o desventajas medibles. El objetivo estratégico es disminuir la dependencia de proveedor, devolver a las organizaciones el control sobre sus definiciones funcionales y fomentar una competencia transparente en la que los fabricantes demuestren sus ventajas mediante resultados, con una visión evolutiva de migración plug-and-play. La especificación no modifica, sustituye ni amplía estándares existentes de comunicación, mensajería, datos ni transporte.

## 1. Estado y lenguaje normativo

Este borrador es una **propuesta técnica para revisión** y no reclama reconocimiento ni estado de estándar. Los términos **MUST**, **MUST NOT**, **SHOULD** y **MAY** se emplean como lenguaje normativo propuesto, según BCP 14 (RFC 2119 y RFC 8174), con el objeto de identificar requisitos sujetos a discusión. Su presencia no implica adopción por una organización de estandarización.

No se ha decidido el organismo de presentación (IETF, OASIS, OMG u otro foro abierto). Si se selecciona IETF, habrá que preparar y presentar un **Internet-Draft** conforme a sus requisitos, sin autodenominarlo RFC.

## 2. Motivación y problema

Los sistemas de integración existentes pueden intercambiar información usando estándares y protocolos establecidos. Sin embargo, la lógica funcional de las interfaces suele permanecer ligada a los conceptos, lenguajes, componentes y modelos de configuración del motor en que se desarrolló.

Migrar una solución a otra plataforma puede exigir reconstruir transformaciones, decisiones, consultas, reglas, orquestación, manejo de excepciones y código particular, aun cuando no cambien las entradas, los destinos ni el comportamiento funcional esperado.

**Problema central:** no se dispone, de forma universalmente adoptada por los motores considerados, de un contrato de definición funcional suficientemente expresivo, portable y verificable para preservar la función de una interfaz con independencia de su implementación.

Esta observación constituye la **hipótesis motivadora** de PIIS. Debe contrastarse con los antecedentes formales existentes antes de afirmar una brecha normativa nueva.

### 2.1. Nota del proponente: libertad de elección y competencia demostrable (informativa)

Esta propuesta nace de más de veinte años de experiencia profesional en integración e interoperabilidad, durante los cuales han evolucionado las arquitecturas y las capacidades de las plataformas, pero ha persistido una barrera: cambiar de motor puede exigir reconstruir interfaces cuya funcionalidad sigue siendo necesaria y válida.

PIIS busca desafiar esa dependencia **sin exigir la divulgación de algoritmos, arquitecturas internas, código ni secretos comerciales**. Cada fabricante debe conservar plena libertad para innovar, optimizar e incorporar capacidades adicionales. Lo que se propone es que pueda **demostrar esas ventajas** a través de contratos funcionales comunes, conformidad verificable y resultados medibles.

La analogía orientativa es un archivo de audio en un formato público como MP3: distintos reproductores compatibles pueden ofrecer prestaciones adicionales, rendimientos y experiencias diferentes, sin exigir al usuario rehacer su biblioteca de audio únicamente para cambiar de reproductor. La analogía es deliberadamente limitada: una interfaz de integración puede incluir estados, transformaciones, efectos externos y dependencias que no existen en la reproducción de un archivo. PIIS debe resolver explícitamente esa complejidad, no suponerla equivalente.

El criterio estratégico es que una organización **elija una solución por lo que demuestra ofrecer**, y no porque el costo de abandonar una implementación previa haga inviable evaluar alternativas. Las capacidades adicionales podrán ser una razón legítima de elección; no deberán convertirse en dependencias funcionales ocultas bajo una declaración de portabilidad completa.

> **La innovación debe ser una razón para elegir una tecnología, nunca una razón para quedar atrapado en ella.**

Esta nota explica la motivación de la propuesta. No crea requisitos normativos ni establece una conclusión anticipada sobre el rendimiento de ninguna implementación.

## 3. Objetivos

PIIS pretende:

1. Representar la funcionalidad de una interfaz sin requerir artefactos internos de un fabricante.
2. Permitir que distintos motores interpreten una misma definición y la implementen de forma nativa.
3. Preservar comportamientos, resultados y efectos observables exigidos por un contrato común.
4. Detectar explícitamente cualquier operación o dependencia que no pueda interpretarse o implementarse con equivalencia demostrable.
5. Facilitar la extracción y migración de interfaces existentes, sin prometer automatización para lógica propietaria arbitraria.
6. Establecer pruebas de conformidad reproducibles y separadas de los benchmarks de rendimiento.
7. Permitir comparaciones objetivas entre soluciones que cumplen el mismo contrato funcional, sin restringir sus medios internos de implementación.
8. Establecer una metodología reproducible centrada en el tiempo End-to-End completo y complementada por throughput conforme, CPU, RAM, escalabilidad, recuperación, integridad funcional, costos y esfuerzo de migración.
9. Reducir barreras al cambio de proveedor y habilitar decisiones transparentes basadas en resultados comprobables, sin imponer una implementación ni garantizar por decreto un resultado de mercado específico.
10. Mantener como visión evolutiva una migración cercana a *plug-and-play* entre implementaciones plenamente conformes, sujeta a las dependencias y condiciones explícitas del despliegue.
11. Dar al titular de una interfaz herramientas portables de definición, evaluación y verificación para escoger o reemplazar una implementación con evidencia técnica, evitando que la permanencia en una plataforma dependa exclusivamente de los costos heredados de migración.
12. Permitir que las capacidades adicionales de cada implementación contribuyan a su diferenciación, sin confundir extensiones particulares con requisitos del núcleo portable ni ocultar su efecto sobre la migrabilidad.

## 4. No objetivos y límites

PIIS **no** pretende:

- Definir, modificar, ampliar, reinterpretar o reemplazar HL7, FHIR, DICOM, X12, ACK, TCP/IP, HTTP, MQTT, MLLP, SOAP, REST u otros estándares, formatos o protocolos establecidos.
- Crear otro ESB, runtime universal, bus de mensajes o producto de integración.
- Obligar a un lenguaje de programación, librería, arquitectura de despliegue, patrón interno de implementación o algoritmo determinado.
- Exigir que las trazas internas, los componentes propietarios, la instrumentación o el rendimiento de dos motores sean idénticos.
- Garantizar la traducción automática de cualquier código existente sin una representación semántica portable o una implementación equivalente.
- Estandarizar credenciales, direcciones físicas, infraestructura o parámetros operacionales específicos de cada instalación.

Los estándares y protocolos existentes son **dependencias externas dadas** y están fuera del alcance normativo de PIIS.

## 5. Principios de diseño

### 5.1. Libertad de implementación

Dos motores conformes **MAY** usar componentes, lenguajes, algoritmos, arquitecturas y secuencias internas completamente diferentes.

### 5.2. Equivalencia observable

La conformidad se evalúa respecto de un mismo contrato funcional, no respecto de la identidad de implementación. Dos ejecuciones son funcionalmente equivalentes cuando satisfacen las mismas obligaciones observables y las variaciones permitidas por el contrato, bajo condiciones equivalentes.

### 5.3. Portabilidad sin pérdida silenciosa

Un intérprete o adaptador **MUST NOT** omitir, degradar o modificar silenciosamente una función obligatoria del contrato. Debe emitir un diagnóstico de incompatibilidad o de equivalencia no demostrada antes de declarar portabilidad completa.

### 5.4. Una interfaz como unidad portable

La unidad mínima es una interfaz funcionalmente identificable. La especificación permitirá referencias entre interfaces y composición de contratos sin obligar a representar inicialmente la producción completa de un motor.

### 5.5. Mínima sobreespecificación

PIIS prescribe condiciones observables y la semántica de sus propios elementos de definición. **MUST NOT** imponer orden, estado, temporización ni algoritmo internos cuando esos aspectos no afectan el contrato.

### 5.6. Transparencia y neutralidad competitiva

La metodología de evaluación **MUST** permitir a múltiples tecnologías implementar el mismo contrato con libertad de diseño y ser comparadas bajo condiciones publicadas y reproducibles. Ninguna métrica de rendimiento será intrínsecamente un criterio de conformidad PIIS, salvo cuando el contrato funcional exija un plazo observable.

### 5.7. Primacía del resultado End-to-End

El tiempo End-to-End **MUST** medir la duración completa del comportamiento observable comprometido, incluyendo las colas, esperas, retransmisiones, persistencias, decisiones y accesos externos involucrados en la solución evaluada. La medición **MUST NOT** detenerse en una aceptación interna ni excluir costos asociados a su arquitectura para mejorar artificialmente sus resultados.

Se deberá asegurar **equivalencia del contrato y de las condiciones externas de prueba**, no equivalencia de arquitectura. Las optimizaciones legítimas **MAY** mejorar el resultado medido siempre que respeten el contrato y las restricciones comunes del perfil de evaluación. Las métricas internas **MAY** incorporarse como diagnóstico, pero **MUST NOT** sustituir ni corregir favorablemente el resultado End-to-End.

### 5.8. Intercambiabilidad como objetivo evolutivo

PIIS busca posibilitar que una definición funcional sea transferible a otro motor conforme sin reescribir su semántica de negocio. Una futura experiencia *plug-and-play* requiere además cobertura de capacidades, configuración explícita de dependencias, seguridad, recursos y despliegue. No se presupone equivalencia automática de código propietario arbitrario.

### 5.9. Libertad de elección y diferenciación demostrable

PIIS **MUST NOT** exigir que las implementaciones ofrezcan idénticas capacidades adicionales, idéntica experiencia de administración o iguales características operativas. El estándar define un núcleo portable y permite diferenciarse por funciones complementarias, eficiencia, confiabilidad, escalabilidad y otros resultados evaluables.

Cuando una extensión adicional pase a ser necesaria para cumplir el contrato funcional de una interfaz concreta, su dependencia **MUST** estar declarada y su portabilidad **MUST** ser evaluada explícitamente. Una extensión no portable **MUST NOT** presentarse como parte de una migración conforme sin adaptación.

La facilidad para importar una definición y la reducción del trabajo necesario para materializarla en otra implementación deberán ser resultados medidos, no afirmaciones comerciales presumidas.

## 6. Terminología

- **Interfaz:** unidad lógica que recibe uno o varios estímulos y produce, de acuerdo con reglas definidas, resultados y/o efectos hacia uno o varios destinos.
- **Definición funcional portable (PFD):** representación independiente del fabricante de operaciones, condiciones, dependencias y composición necesarias para materializar el comportamiento de una interfaz.
- **Contrato observable (OC):** obligaciones verificables sobre entradas admitidas, precondiciones, resultados, efectos externos, fallas y variaciones permitidas.
- **Implementación:** realización de una PFD por un motor específico.
- **Adaptador:** componente que interpreta o transforma una PFD hacia mecanismos nativos de un motor; su existencia no exige que toda plataforma use un traductor separado.
- **Capacidad:** operación o semántica de PIIS que una implementación puede satisfacer.
- **Conformidad:** evidencia de que una implementación satisface el contrato completo para un ámbito definido de entradas, dependencias y condiciones.
- **Dependencia externa:** sistema, servicio, base de datos, recurso o función cuyo comportamiento no está gobernado por PIIS.
- **Traza observable:** secuencia parcial o total de acciones y efectos externamente apreciables relevantes para el contrato.

## 7. Arquitectura conceptual

PIIS propone separar cuatro conceptos, sin imponer una arquitectura física:

1. **Definición funcional portable:** qué operaciones y reglas constituyen la interfaz, y cómo se conectan lógicamente.
2. **Contrato de comportamiento observable:** qué exige la interfaz ante entradas y condiciones determinadas, incluidos resultados, efectos y casos de falla.
3. **Interpretación nativa:** cómo un motor transforma o ejecuta la definición usando sus propias capacidades.
4. **Verificación independiente:** cómo se demuestra la conformidad y se identifican incompatibilidades.

La definición funcional **no puede reducirse** a una lista de ejemplos de entradas y salidas. Debe contener información suficiente para interpretar las funciones declaradas. El contrato observable permite verificar el resultado de esa interpretación, pero por sí solo no reconstruye lógica arbitraria.

## 8. Modelo conceptual mínimo

Una PFD podrá contener los siguientes elementos. Sus nombres son provisionales y **no implican todavía una sintaxis normativa**:

| Elemento | Responsabilidad |
|---|---|
| Identity | Identidad, versión y referencias de la interfaz. |
| Source | Orígenes lógicos, condiciones de entrada y enlaces externos. |
| Destination | Destinos lógicos y efectos requeridos. |
| Channel | Relaciones lógicas de flujo o intercambio entre elementos. |
| Operation | Funciones portables declaradas con semántica identificable. |
| Flow | Dependencias, bifurcaciones, composición y condiciones entre operaciones. |
| Rule | Validaciones, predicados y decisiones funcionales. |
| Transformation | Construcción o modificación de datos con reglas definidas. |
| Function | Lógica especializada con contrato y mecanismo de representación portable o dependencia declarada. |
| Dependency | Sistemas y datos externos requeridos y sus supuestos relevantes. |
| BehaviorContract | Obligaciones y variaciones observables permitidas. |
| ConformanceCases | Casos y evidencia reproducible de verificación. |

Se evitará duplicar conceptos cuando el mismo comportamiento pueda expresarse mediante un conjunto menor de elementos. Se admitirán múltiples orígenes, múltiples destinos, ramas, concurrencia y estados cuando el caso real lo justifique.

### 8.1. Vocabulario funcional inicial, no cerrado

El catálogo a evaluar incluye: recibir, emitir, analizar, validar, transformar, enriquecer, consultar, invocar, filtrar, enrutar, dividir, agregar, correlacionar, esperar y manejar excepciones. Son **candidatos a primitivas semánticas**, no una lista ya aprobada. Se investigará cuáles son necesarias y cuáles pueden componerse a partir de otras.

### 8.2. Conectores y protocolos

Un origen o destino puede identificar un tipo externo (TCP, archivo, base de datos, cola, MQTT, HTTP, etc.) y referenciar su contrato preexistente. PIIS solo modela la **relación funcional** de la interfaz con dicho recurso; no define la especificación técnica del protocolo.

## 9. Contrato de comportamiento observable

Un contrato podrá declarar, cuando correspondan:

- **Entradas:** tipos, condiciones de aceptación y precondiciones funcionales.
- **Resultados:** salidas requeridas y restricciones sobre su contenido.
- **Efectos externos:** escrituras, publicaciones, invocaciones o modificaciones observables.
- **Decisiones:** condiciones que determinan destinos o resultados posibles.
- **Fallas:** efectos y resultados requeridos para errores dentro de los supuestos del contrato.
- **Estado:** cambios persistentes o dependencias entre invocaciones cuando sean funcionalmente significativos.
- **Orden y temporalidad:** solamente las restricciones observables que el contrato exija.
- **Variación permitida:** diferencias válidas, tolerancias o valores no deterministas que no constituyen incumplimiento.
- **Efectos prohibidos:** acciones que no pueden producirse bajo las condiciones declaradas.

La equivalencia **no requiere igualdad byte a byte** si el contrato admite representaciones distintas. Por el contrario, deberá exigir igualdad exacta cuando esa igualdad sea una obligación explícita.

La evaluación debe distinguir diferencias de implementación de incumplimientos funcionales. El estándar no redefine las reglas externas de ACK, transacciones, transporte, etc.; solo permite referenciar las obligaciones que sean relevantes para la interfaz.

## 10. Representación e intercambio

Se propone:

- **JSON** como formato canónico de intercambio de PIIS.
- **YAML** como formato de autoría opcional que pueda normalizarse sin pérdida semántica al modelo JSON definido.
- **JSON Schema** para validar la estructura de la representación, sin confundir validación de esquema con conformidad funcional.
- Versionado explícito y reglas para extensiones.

Las reglas para tipos, referencias, orden, identificadores y extensiones se definirán en una versión futura del esquema. Se evaluará el uso de RFC 8785 si se requiere una serialización JSON canónica para huellas criptográficas, firmas o comparación inequívoca de artefactos.

**Regla propuesta:** campos desconocidos que afecten la funcionalidad requerida **MUST NOT** ignorarse silenciosamente. El manejo de extensiones puramente informativas podrá ser diferente y deberá quedar especificado.

## 11. Funciones y código personalizado

La lógica personalizada constituye un desafío de portabilidad fundamental, pero no justifica imponer un lenguaje de programación particular.

PIIS deberá diferenciar:

1. **Funcionalidad expresable en primitivas portables:** podrá interpretarse mediante mecanismos nativos diferentes.
2. **Funcionalidad representada mediante un mecanismo portable adicional:** su semántica, ejecución y efectos deberán estar especificados antes de permitir una declaración de conformidad.
3. **Dependencia propietaria no representada:** deberá identificarse explícitamente y no podrá certificar portabilidad completa mientras permanezca sin resolver.

Un contrato de entrada/salida de una función no basta para generar automáticamente una implementación semánticamente equivalente. Para migración automática se requerirá una representación interpretable de la lógica, una implementación compatible suministrada o una intervención de adaptación declarada.

Este documento **no elige todavía** una DSL, un lenguaje de expresiones, un bytecode o un entorno de ejecución para los casos personalizados. Esa decisión exige investigación separada.

## 12. Capacidades y compatibilidad

Un motor **MAY** declarar un catálogo de capacidades soportadas, versiones y restricciones. La evaluación de una PFD concreta deberá comprobar el conjunto de capacidades efectivamente exigido por la interfaz.

Se distinguen:

- **Supported:** puede interpretar y materializar el requisito de forma demostrable.
- **Unsupported:** no puede satisfacerlo.
- **Unverified:** no existe evidencia suficiente para afirmar equivalencia.

La compatibilidad parcial es información diagnóstica útil, pero **no equivale** a conformidad del contrato completo.

## 13. Conformidad

Una declaración de conformidad para una interfaz y un motor específicos deberá incluir como mínimo:

1. **Validación de representación:** el artefacto es estructuralmente válido.
2. **Cobertura semántica:** todas las funciones obligatorias tienen interpretación implementable; las extensiones y dependencias relevantes se conocen.
3. **Evaluación de comportamiento:** los resultados y efectos satisfacen el contrato bajo condiciones de prueba reproducibles.
4. **Evidencia y alcance:** versión del contrato, motor, adaptador si aplica, entorno, pruebas, resultados y limitaciones.

No bastará con poder abrir un archivo, importar una ruta o superar un conjunto pequeño de ejemplos para declarar conformidad universal.

Las pruebas deberán incluir casos positivos, límites, fallas, concurrencia, estado y efectos externos, según corresponda. No se pretende que un número finito de casos pruebe equivalencia de cualquier programa arbitrario. La garantía debe estar acotada por las semánticas definidas, los supuestos y la evidencia disponible.

### 13.1. Estados del resultado

- **Conformant:** satisface todas las obligaciones del contrato y el alcance de conformidad declarado, con evidencia suficiente conforme a la metodología acordada.
- **Non-conformant:** se observó un incumplimiento del contrato.
- **Not demonstrated:** no existe evidencia suficiente, o hay dependencias funcionales no resueltas.

Ningún estado deberá permitir presentar como conformante una interfaz que perdió una función obligatoria.

## 14. Evaluación comparativa independiente y orientada a resultados

### 14.1. Principio: competir por resultados, no por arquitectura

Una vez demostrada la conformidad con el mismo contrato, PIIS habilitará la comparación directa entre implementaciones independientes. La implementación interna queda enteramente a criterio de cada motor. El estándar **MUST NOT** exigir algoritmos, componentes, patrones de procesamiento o topologías idénticos para considerar válida una evaluación.

La **métrica operativa primaria** es el **tiempo de finalización End-to-End (E2E)** de una unidad funcional de trabajo conforme. Se mide desde un estímulo de entrada definido en la frontera observable común hasta la confirmación externa de **todos** los efectos y resultados requeridos por el contrato. No se considera finalizada la operación solo porque un componente la haya recibido, colocado en una cola o marcado como aceptada internamente.

El tiempo medido **incluye** lo que la solución necesite para cumplir su función: recepción, espera, cola, análisis, validación, transformación, enrutamiento, escrituras, invocaciones, reintentos y confirmaciones, cuando sean parte del comportamiento evaluado. Ninguno de esos tiempos **MAY** descontarse por ser una particularidad arquitectónica. Si una implementación completa el mismo trabajo antes que otra, bajo iguales condiciones externas y garantías funcionales, presenta una ventaja objetiva **en tiempo E2E para ese escenario**.

Las dependencias externas deben ofrecer **condiciones comparables**, no desaparecer del recorrido medido. Podrán emplearse servicios de prueba controlados, respuestas reproducibles o entornos reales equivalentes; el método elegido **MUST** declararse. Las diferencias de tiempo que la implementación origine al interactuar con ellas forman parte del resultado total. Las mediciones de procesamiento interno y de servicios externos **MAY** registrarse para diagnóstico, sin alterar la cifra E2E observada.

La comparación podrá identificar ventajas diferentes según métrica; PIIS **MUST NOT** proclamar un vencedor universal a partir de una sola prueba. No se impondrán mínimos de velocidad como requisito general de conformidad, excepto si el contrato funcional define límites temporales observables.

### 14.2. Métricas de referencia

El siguiente catálogo constituye un **perfil inicial propuesto**. Los detalles estadísticos y procedimientos serán objeto de especificaciones de prueba posteriores.

| Identificador propuesto | Métrica | Qué mide | Informe mínimo |
|---|---|---|---|
| `e2e_completion_time` | **Tiempo End-to-End (primaria)** | Duración total del resultado funcional completo, desde la entrada común hasta el último efecto obligatorio confirmado | ms; P50, P95 y P99; cantidad de operaciones completadas y no completadas |
| `conformant_throughput` | **Throughput conforme** | Operaciones por segundo que cumplen íntegramente el contrato | ops/s, ventana sostenida, carga y porcentaje de éxito |
| `cpu_consumption` | **Consumo CPU** | Recursos de procesamiento empleados por toda la solución evaluada | CPU promedio/pico, núcleos disponibles y CPU-ms/operación conforme |
| `memory_consumption` | **Consumo RAM** | Memoria utilizada por todos los componentes necesarios para el funcionamiento evaluado | MB o GB; memoria estable y pico |
| `scalability` | **Escalabilidad** | Comportamiento de E2E, throughput y recursos al variar carga o concurrencia | Curvas por nivel de carga y límites observados |
| `recovery_time` | **Recuperación** | Tiempo desde una falla controlada hasta recuperar los efectos funcionales exigidos | segundos; trabajos pendientes, perdidos y duplicados |
| `functional_integrity` | **Integridad funcional** | Resultados correctos e incorrectos, pérdidas, duplicaciones y efectos no permitidos | cantidades, tasas y clasificación de fallas |
| `operational_cost` | **Costo operativo** | Costo de ejecutar un volumen de trabajo conforme bajo un escenario declarado | costo por periodo y por operación conforme; supuestos |
| `migration_effort` | **Esfuerzo de migración** | Intervención necesaria para materializar y validar una definición existente en otra implementación | horas-persona, tareas manuales y automatizadas, bloqueos |
| `internal_diagnostics` | Diagnóstico interno (opcional) | Tiempos parciales, esperas y otras medidas explicativas | desglose y método, **sin descontarlo del E2E** |

**Reglas de contabilización:**

1. El informe **MUST** identificar el instante de inicio, el criterio de finalización y el conjunto de efectos obligatorios del contrato para cada clase de operación.
2. El tiempo E2E **MUST** comprender el recorrido funcional completo en condiciones de prueba comunes; ninguna demora de cola o espera interna puede excluirse por motivos de arquitectura.
3. Una operación incompleta, vencida o no conforme **MUST NOT** contabilizarse como éxito ni desaparecer del conjunto de resultados. Se reportará por separado y se especificará su tratamiento estadístico para evitar sesgo por exclusión de operaciones lentas.
4. El throughput **MUST** contar únicamente operaciones conformes completadas; la aceptación de entradas no constituye finalización funcional.
5. CPU y RAM **MUST** contabilizar el ámbito íntegro de los componentes necesarios para satisfacer el contrato. El perímetro de medición y la agregación de recursos **MUST** publicarse.
6. El costo **MUST** relacionarse con trabajo conforme y declarar supuestos de infraestructura, operación, licencia, consumo y horizonte temporal. No se interpretará como una medida de conformidad.
7. Las métricas de diagnóstico interno **MAY** explicar causas, pero **MUST NOT** utilizarse para justificar una clasificación de E2E distinta de la efectivamente medida.

### 14.3. Condiciones de comparabilidad

La condición de igualdad necesaria no es que los motores estén construidos de forma similar. Es que se les exija **el mismo resultado funcional bajo restricciones externas y cargas equivalentes**.

Toda comparación presentada como PIIS-qualified **MUST** identificar y publicar:

1. Identidad, versión y huella verificable del contrato funcional y de la definición portable evaluados.
2. Versión de cada implementación y de cualquier componente necesario para materializar el contrato, sin privilegiar una arquitectura.
3. Entradas, tamaños, distribución de casos, estados iniciales, tasa de llegada, ráfagas, concurrencia y duración de la prueba.
4. Condiciones externas reproducibles: sistemas de prueba, red, almacenamiento, límites, respuestas, fallas inducidas y tiempos de esos servicios.
5. Garantías funcionales comunes: persistencia, seguridad, confirmación, registro de auditoría y otras obligaciones del contrato.
6. Modalidad de comparación: **igual presupuesto de recursos**, **igual presupuesto económico**, o ambas, informadas por separado.
7. Recursos y topología utilizados efectivamente, incluidas capacidades auxiliares requeridas; optimizaciones habilitadas y sus condiciones.
8. Instrumentación del comienzo y final del proceso, preferentemente independiente de la implementación evaluada, y tratamiento de fallas o muestras incompletas.
9. Datos brutos, resultados agregados, método estadístico, variabilidad, repeticiones, condiciones de calentamiento y limitaciones.

Cada implementación **MAY** elegir su arquitectura, ajustar sus mecanismos y aprovechar optimizaciones propias. Una optimización que incumpla el contrato, reduzca garantías requeridas o transfiera trabajo oculto fuera del perímetro declarado **MUST** invalidar la comparación como prueba de soluciones funcionalmente equivalentes. Un beneficio auténtico de rendimiento o consumo **MUST NOT** eliminarse mediante normalizaciones que pretendan neutralizar diferencias tecnológicas.

### 14.4. Perfiles experimentales mínimos

Se proponen escenarios independientes de producto:

1. **Precalificación:** comprobación funcional completa del contrato y de sus efectos.
2. **Línea base:** carga sostenida baja con instrumentación externa de E2E.
3. **Operación sostenida:** distribución representativa de transacciones, tamaños y concurrencia.
4. **Ráfagas:** incrementos bruscos de carga y evolución de colas hasta su vaciado.
5. **Escalabilidad:** incrementos graduados de carga y/o presupuesto de recursos, informando E2E y operaciones conformes.
6. **Fallas y recuperación:** interrupciones controladas, reinicio, reintentos y confirmación de resultados pendientes, conforme a contrato.
7. **Portabilidad práctica:** materialización de una misma definición en una implementación alternativa y medición del trabajo humano requerido.

Los perfiles **MUST** comparar las mismas obligaciones y restricciones. Los valores numéricos de tamaño, duración y carga deberán acordarse y publicarse antes de ejecutar el benchmark, no ajustarse retrospectivamente a favor de un resultado.

### 14.5. Reporte para decisiones de adopción y migración

Una evaluación publicada **SHOULD** ofrecer un artefacto legible por máquinas y un resumen comprensible para quienes deban adquirir, mantener o migrar sistemas de integración. El reporte debería permitir contestar, sin inferencias comerciales:

- ¿Puede esta implementación cumplir **todo** el contrato funcional?
- ¿Cuánto tarda en producir cada resultado completo, de extremo a extremo?
- ¿Cuántas operaciones conformes sostiene y con qué consumo CPU/RAM?
- ¿Cómo se comporta bajo carga, ráfagas y fallas?
- ¿Cuál es su costo por resultado funcional conforme?
- ¿Cuánto trabajo real se requiere para migrar la definición?

La comparación podrá ilustrar intercambios entre desempeño, recursos, costos y recuperabilidad. **No deberá** ocultar diferencias por motivos arquitectónicos ni presentar como equivalente una solución que ha sacrificado obligaciones funcionales. El beneficio esperado para el mercado —menos dependencia, mayor transparencia y presión competitiva para mejorar— constituye una **hipótesis de impacto que deberá medirse**, no una garantía de adopción.

### 14.6. Independencia y auditabilidad

Una declaración de conformidad o un informe de benchmark **MUST** sustentarse en evidencia reproducible; no basta una afirmación comercial. La afiliación institucional, patrocinio o pago por pruebas **MUST NOT** alterar los criterios técnicos de evaluación. Cuando datos sensibles impidan publicar muestras originales, **SHOULD** facilitarse material sintético representativo, resultados agregados y procedimientos auditables. Se propone desarrollar un paquete abierto de contratos, casos de prueba, generadores de carga y un formato común de reporte.

## 15. Portabilidad de interfaces existentes

El objetivo de migración exige considerar el siguiente proceso conceptual:

1. Inspeccionar la implementación existente y sus dependencias.
2. Extraer o reconstruir su definición funcional portable.
3. Identificar operaciones, efectos y supuestos no representados.
4. Comparar la definición con las capacidades del motor destino.
5. Materializar la implementación destino mediante mecanismos nativos.
6. Ejecutar las pruebas de conformidad y declarar resultados, limitaciones y diferencias.

La extracción automática desde productos existentes será una capacidad deseable de herramientas de ecosistema; no se presupone que todos los motores puedan exportar actualmente su semántica en forma completa.

## 16. Consideraciones de seguridad

Una PFD portable no deberá transportar secretos operacionales como parte de su definición funcional. Las credenciales, autorizaciones, políticas locales y direcciones específicas deberán resolverse mediante asociaciones de despliegue, manteniendo explícitos los permisos y efectos requeridos.

Se deben considerar entradas maliciosas, dependencias externas no confiables, privilegios excesivos, filtración de datos en casos de prueba, código personalizado y efectos accidentales durante migración y benchmarking. Las pruebas de conformidad deberán poder ejecutarse en entornos controlados para evitar modificar sistemas productivos.

## 17. Antecedentes y posición frente al estado del arte

Los antecedentes no se asumen insuficientes por definición; deben analizarse formalmente antes de afirmar novedad:

| Iniciativa | Aporte relevante | Pregunta para PIIS |
|---|---|---|
| WfMC XPDL | Intercambio de modelos de procesos y preservación de extensiones de herramienta | ¿Qué semántica funcional ejecutable puede intercambiarse realmente? |
| OMG BPMN 2.0.2 | Modelado y semántica de ejecución; distintas clases de conformidad | ¿Cómo evitar conformidad nominal sin portabilidad funcional? |
| OMG Model Driven Architecture (MDA) | Separación PIM/PSM, funcionalidad independiente de plataforma y materialización específica | ¿Qué añade PIIS para interfaces ESB concretas, equivalencia observable y migración medida? |
| OASIS WS-BPEL 2.0 | Procesos ejecutables con semántica definida | ¿Qué cubre y qué limita su orientación histórica a servicios web? |
| OASIS SCA | Composición de componentes y separación de implementaciones | ¿Qué parte del ensamblaje es portable entre plataformas ESB concretas? |
| Patrones de integración documentados públicamente | Taxonomía de funciones recurrentes de integración | ¿Qué conceptos pueden formalizarse como primitivas semánticas verificables sin definir otra plataforma? |
| CNCF Open Workflow Specification | DSL neutral, runtimes y Conformance Test Kit | ¿Hasta dónde alcanza el comportamiento contractual de interfaces y qué se puede adoptar directamente? |
| AsyncAPI | Contratos de operaciones y canales asíncronos | ¿Qué descripciones pueden referenciarse sin duplicarlas? |

**Evidencia académica:** estudios de conformidad de BPMN encontraron soporte parcial y diferencias entre motores, lo que respalda la necesidad de medir la ejecución real y no solo la capacidad de lectura de un formato. Estos resultados son históricos y no caracterizan automáticamente el mercado actual.

## 18. Validación inicial propuesta

La prueba de concepto empleará una **interfaz real** que incluya origen, validación, transformación, enriquecimiento externo, decisión de ruteo, dos destinos, manejo de excepciones y al menos una función personalizada.

Entregables:

1. Inventario completo de comportamiento y efectos observables de la interfaz original.
2. Primera PFD independiente de fabricante.
3. Contrato de conformidad y casos reproducibles.
4. Implementaciones nativas en al menos dos motores diferentes.
5. Informe de conformidad de ambas implementaciones.
6. Benchmark comparativo End-to-End y de recursos **solo si ambas superan la conformidad exigida**.
7. Registro de elementos no portables, causas y decisiones de diseño.

**Criterio de éxito:** que ambas implementaciones satisfagan el mismo contrato funcional observable sin obligar a compartir código ni tecnología interna. El esfuerzo manual requerido para materializar la segunda implementación deberá medirse separadamente, puesto que la **reducción efectiva de esfuerzo de migración** también es una hipótesis que debe demostrarse. La prueba generará el reporte completo de la sección 14, dando primacía al resultado End-to-End sin excluir demoras propias de la solución. La velocidad y el costo se evaluarán por separado de la conformidad funcional, salvo que un plazo observable forme parte del contrato.

## 19. Preguntas abiertas que deben resolverse antes de una versión normativa

1. ¿Qué conjunto mínimo de primitivas es suficiente sin perder expresividad?
2. ¿Cómo expresar transformación, condiciones y consultas de forma interpretable sin crear un lenguaje demasiado amplio?
3. ¿Qué debe ser parte de la PFD y qué debe pertenecer al despliegue?
4. ¿Cuál es el modelo formal mínimo de observabilidad y equivalencia?
5. ¿Cómo declarar y probar efectos externos, estado y no determinismo?
6. ¿Cómo portar lógica personalizada sin esconder dependencias propietarias?
7. ¿Qué perfiles de capacidades sirven sin fragmentar la conformidad en dialectos de fabricante?
8. ¿Hasta qué punto BPMN, BPEL, SCA u Open Workflow ya resuelven el problema y podrían servir de base?
9. ¿Cómo medir la mejora de migración en esfuerzo, tiempo y riesgo, además del cumplimiento funcional?
10. ¿Qué foro de estandarización y mecanismo comunitario resulta pertinente?
11. ¿Cómo instrumentar el recorrido End-to-End completo desde fronteras observables comunes, con condiciones externas equivalentes, sin descontar ventajas o penalizaciones de arquitectura?
12. ¿Qué perfiles de carga permiten comparar implementaciones diferentes sin favorecer un estilo arquitectónico?
13. ¿Qué evidencias mínimas debería entregar un proveedor para respaldar una afirmación de *plug-and-play*?

## 20. Plan de trabajo sugerido

**Fase A — Estado del arte y alcance:** comparación crítica de antecedentes, identificación de brecha demostrable y definición de unidad portable.

**Fase B — Modelo y semántica:** inventario de primitivas a partir de interfaces reales y primer modelo de observabilidad.

**Fase C — Representación:** esquema JSON de intercambio, perfil YAML y validadores estructurales.

**Fase D — Conformidad:** contratos de prueba, evidencia, cobertura y estados de resultado.

**Fase E — Prueba entre motores:** implementación independiente, verificación y medición de esfuerzo de migración.

**Fase F — Benchmark reproducible:** publicar definiciones de carga, mediciones End-to-End completas, recursos de toda la solución, resultados funcionales y esfuerzo real de migración en un perfil abierto.

**Fase G — Evaluación externa:** revisión por especialistas, autores de estándares existentes y fabricantes antes de elegir un foro formal de presentación.

## 21. Visión de largo plazo y efectos esperados

**Principio de mercado:** PIIS no neutraliza las ventajas ni las desventajas tecnológicas. Las hace medibles. Su ambición es trasladar la decisión desde la dependencia histórica de una plataforma hacia la evidencia funcional y operativa disponible para su usuario. Una tecnología que entregue el mismo resultado completo en menor tiempo, con menores recursos o menor costo, habrá demostrado esa ventaja en las condiciones evaluadas. El estándar busca que la posibilidad de elegir y migrar dependa de esa evidencia, no de la dificultad de reconstruir interfaces.

### 21.1. *Plug-and-play* como estado objetivo

La visión de PIIS es que una institución pueda trasladar la definición funcional de una interfaz a otro motor conforme, vincular explícitamente sus dependencias de despliegue y verificar automáticamente que no hubo pérdida funcional. El objetivo final es minimizar a tareas declarativas y verificables la intervención necesaria para cambiar de plataforma.

No debe confundirse el **contrato de portabilidad** con una promesa de migración instantánea: permisos, conexiones, credenciales, topología, componentes personalizados no portables y características particulares del destino pueden exigir tareas de adaptación. La aproximación a *plug-and-play* depende de un perfil suficientemente expresivo, cobertura completa de capacidades y herramientas interoperables de importación/exportación. Será un logro medible, no una etiqueta comercial.

### 21.2. Competencia transparente y reducción de lock-in

PIIS aspira a reducir el *vendor lock-in* funcional mediante definiciones, contratos y evidencias portables bajo control de sus titulares, que puedan materializarse en implementaciones alternativas. Ningún fabricante necesita revelar su propiedad intelectual interna para demostrar conformidad o rendimiento; la comparación se establece sobre resultados externamente verificables. La posible reducción de costos, incremento de innovación y dinamización del mercado se tratarán como **hipótesis de impacto** sujetas a observación y evaluación. El estándar no debe favorecer productos ni imponer técnicas de implementación.

## 22. Selección de organismo y estrategia de presentación

La elección de organismo se mantiene abierta. La idoneidad dependerá del alcance real de PIIS, la participación de proveedores interesados y los requisitos de propiedad intelectual.

| Foro | Fortalezas verificadas | Reserva principal |
|---|---|---|
| **IETF** | Proceso de Internet-Drafts, discusión pública y antecedentes de metodologías reproducibles de benchmark; participación sin membresía obligatoria | Su misión se concentra en tecnologías de Internet; un modelo genérico de semántica de procesos/ESB puede quedar fuera de su campo natural. |
| **IHE International** | Organización **sin fines de lucro**, experiencia en perfiles de integración, Connectathon y pruebas de interoperabilidad; marcos técnicos disponibles públicamente | Su foco es interoperabilidad en salud, mientras PIIS pretende ser transversal; usa membresías con cuotas y cobra por ciertos servicios de pruebas. |
| **OASIS Open** | Procesos formales para comités de especificación y experiencia histórica con BPEL y SCA | Requiere explorar un comité interesado, condiciones de membresía y reglas de IPR. |
| **OMG** | Especificaciones transversales y precedente **Model Driven Architecture (MDA)**: separación entre *Platform Independent Model* (PIM) y *Platform Specific Model* (PSM) | Debe distinguirse claramente PIIS de MDA y de estándares OMG ya existentes; gobernanza basada en miembros. |

**Recomendación de trabajo:** no seleccionar organismo aún. Publicar primero el borrador técnico y su matriz de antecedentes, iniciar revisión abierta, lograr al menos dos implementaciones independientes de una PFD y consultar tempranamente a IETF, OASIS, OMG e IHE. IHE puede ser un aliado sectorial para un piloto clínico sin restringir el estándar a salud.

**Antecedente que debe ocupar un lugar prioritario:** OMG MDA. Su esquema PIM/PSM ya formaliza la separación entre funcionalidad independiente de plataforma e implementación específica. La eventual novedad de PIIS deberá encontrarse en la semántica de interfaces de integración concretas, sus efectos observables, conformidad entre motores y portabilidad operativa, no en reclamar por primera vez la idea de independencia de plataforma.

## 23. Referencias

### Antecedentes de portabilidad y ejecución

- WfMC, *XPDL*. https://wfmc.org/xpdl/
- WfMC, *Public Documents / Process Definition Interchange*. https://wfmc.org/public-documents/
- OMG, *Business Process Model and Notation 2.0.2*. https://www.omg.org/spec/BPMN/
- OASIS, *WS-BPEL 2.0*. https://docs.oasis-open.org/wsbpel/2.0/process/executable/index.html
- OASIS Open CSA, *Service Component Architecture*. https://www.oasis-opencsa.org/sca.html
- CNCF, *Open Workflow Specification*. https://github.com/open-workflow-specification/specification
- AsyncAPI, *Adding Operations*. https://www.asyncapi.com/docs/concepts/asyncapi-document/adding-operations
- *BPMN Conformance in Open Source Engines* (2015). https://fis.uni-bamberg.de/entities/publication/546a51ef-9699-4e66-8c94-c64437bc0c1b
- *BPMN 2.0: The State of Support and Implementation* (2018). https://www.sciencedirect.com/science/article/pii/S0167739X17300250

### Benchmark y foros de normalización

- IETF, *Bringing new work to the IETF*. https://www.ietf.org/process/new-work/
- IETF, *Guide to the IETF standards process*. https://www.ietf.org/process/process/
- IETF, RFC 9411, *Benchmarking Methodology for Network Security Device Performance*. https://www.rfc-editor.org/rfc/rfc9411.html
- IETF, *Benchmarking Methodology Working Group (BMWG)*. https://datatracker.ietf.org/wg/bmwg/charter/
- IHE International, *Governance*. https://www.ihe.net/about_ihe/governance/
- IHE International, *Membership*. https://www.ihe.net/membership/
- IHE International, *IHE Process*. https://www.ihe.net/about_ihe/ihe_process/
- OASIS, *Technical Committee Handbook*. https://docs.oasis-open.org/TChandbook/TChandbookIndex.html
- OMG, *Model Driven Architecture FAQ*. https://www.omg.org/mda/faq_mda.htm
- OMG, *Mission & Vision*. https://www.omg.org/about/

### Normativa de representación y autoría

- RFC 8259, *JSON Data Interchange Format*. https://www.rfc-editor.org/rfc/rfc8259.html
- RFC 8785, *JSON Canonicalization Scheme*. https://www.rfc-editor.org/rfc/rfc8785.html
- JSON Schema, *Specification*. https://json-schema.org/specification
- YAML, *Specification 1.2.2*. https://yaml.org/spec/1.2.2/index.html
- RFC 2119 y RFC 8174, *BCP 14*. https://www.rfc-editor.org/info/bcp14/
- RFC Editor, *How RFCs Are Created*. https://www.rfc-editor.org/authors/rfc-how-to/

---

**Nota final:** PIIS es un nombre de trabajo. Este borrador fija los principios acordados, refuerza la evaluación de resultados completos y mantiene abiertas las preguntas de diseño; no pretende haber demostrado todavía portabilidad completa ni equivalencia universal entre productos concretos.