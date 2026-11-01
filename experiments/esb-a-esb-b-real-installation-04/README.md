# PIIS — Experimento 04 (ESB-A / ESB-B)

**Estado:** propuesta exploratoria de definición funcional portable (PFD), elaborada a partir de dos configuraciones históricas procedentes de una instalación real. **No se declara equivalencia funcional, conformidad, ni una implementación independiente verificable.**

## Alcance y privacidad

- ESB-A: exportación de configuración de origen.
- ESB-B: exportación generada mediante un proceso de conversión con acciones sugeridas, tareas manuales y verificaciones pendientes.
- Solo se publican **artefactos derivados**, con identificadores sintéticos y familias funcionales. **Los XML originales no forman parte de este paquete.**
- Se omiten nombres comerciales, identificadores de instituciones o canales, consultas SQL, scripts, mensajes de pacientes, plantillas, rutas, direcciones, puertos, nombres de credenciales y valores de conexión.
- Los nombres externos son únicamente ESB-A y ESB-B. Se utiliza **componente** para cualquier unidad de implementación, sin denominar sus estructuras internas.

## Artefactos

| Archivo | Propósito |
| --- | --- |
| `PIIS.json` | Candidato de la representación común para todas las interfaces y sus destinos lógicos, sobre el perfil exploratorio PIIS 0.1 |
| `review_report.json` | Hallazgos observables de configuración, trazabilidad de correspondencias, salvedades y acciones globales pendientes declaradas por el conversor |
| `flow_matrix.csv` | Matriz de correspondencia sintética y prioridades de revisión por interfaz |
| `validate_outputs.py` | Validaciones de integridad de los artefactos, **no** prueba de conformidad funcional |

## Lectura crítica

El número de componentes no puede compararse 1:1 con el número de canales: las arquitecturas son diferentes. La correspondencia utiliza metadatos de procedencia y puede ser ambigua o ausente. La activación de un componente tampoco demuestra que el efecto externo esperado ocurra.

Las cantidades de tareas manuales, ajustes de entorno y verificaciones se toman de la declaración de ESB-B; **no acreditan tareas realizadas**. Los indicadores de lenguaje y rutas de campos estandarizados son pistas lexicográficas, no equivalencias semánticas. Diferencias de campos referenciados no son automáticamente errores.

El `PIIS.json` conserva `NOT_DEMONSTRATED` y la lista de pruebas es solo una propuesta. **El esquema PIIS 0.1 valida la estructura básica del documento, no el contenido funcional ni un contrato observable verificable.**

## Próximo paso

Seleccionar 2–3 flujos con correspondencia identificable y diferente complejidad; reconstruir localmente sus reglas y efectos con datos sintéticos, sin publicar lógica institucional. Completar o acotar las tareas manuales, verificar comportamiento y solo entonces desarrollar assertions del contrato observable.

**No publicar los originales, ni asumir que una revisión automática garantiza anonimización contractual o legal.**
