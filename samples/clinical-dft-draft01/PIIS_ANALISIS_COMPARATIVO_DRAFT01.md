# PIIS — Caso DFT, primera definición funcional anonimizada (Draft 01)

**Estado:** propuesta exploratoria de instancia PIIS; **NO conformante, NO ejecutable y NO validada**.  
**Archivos de trabajo:** `PIIS_PFD_DFT_DRAFT01.json` y `PIIS_BINDINGS_PRIVATE_TEMPLATE.json`.  
**Fuentes:** dos XML entregados en esta conversación, evaluados localmente, **no incluidos** en este paquete.

## 1. Qué se observó (hechos extraídos)

- **Configuración A (canal original):** un receptor TCP/MLLP, seis reglas de aceptación de origen, **nueve** pasos de transformación de origen y **once** destinos configurados (**ocho habilitados; tres deshabilitados**).
- **Configuración B (producción convertida):** un conjunto exportado de **17 clases y 13 elementos de producción**, con una orquestación de procesos, operaciones de salida, transformaciones y dependencias SQL. Su propia cabecera declara que proviene de la **conversión del canal de la configuración A**, con ajustes manuales pendientes.
- La configuración B **no prueba** por sí misma que dos implementaciones independientes tengan comportamiento equivalente. No se entregaron mensajes reales de prueba, resultados, trazas ni evidencia de ejecución.
- La transformación original realiza decisiones funcionales sobre mensajes **HL7 v2 DFT**, con una representación tipo **DFT_P03 versión 2.3 declarada por el modelo convertido**. Eso **no demuestra** automáticamente la versión efectiva de todas las entradas originales.

## 2. Comportamiento preservado conceptualmente

| Etapa | Comportamiento soportado por el XML | Representación PIIS propuesta |
| --- | --- | --- |
| Recepción | TCP con encuadre MLLP; respuesta automática configurada antes de procesar en A | `Source` + obligación de respuesta pendiente de comprobar en B |
| Admisión | Mensaje de tipo DFT; filtros por prestación, tipo de paciente, episodio, guiones y códigos excluidos | `Rule.inbound_acceptance`, conjunción de seis predicados |
| Transformación 1 | Elimina la primera repetición OBX cuando existe | `Operation.OP01` |
| Transformación 2 | Si hay PR1 cambia clasificación de visita y copia campo de centro ejecutor | `Operation.OP02` |
| Enriquecimiento | Selecciona unidad gestora por reglas **ordenadas**, consultas a datos externos y fallback | `Rule.unit_assignment_priority` + `Operation.OP03` |
| Construcción de mensaje | Agrega OBX tras PV1 con el resultado del enriquecimiento | `Operation.OP04` |
| Ajustes de cargo | Anulación, normalización de código, obtención de identificadores, manejo de hora cero | `Operation.OP05`–`OP09` |
| Ruteo | Hasta ocho salidas habilitadas con filtros independientes, transformaciones propias y efectos externos | `Destination.D01`–`D08` |
| Error de unidad no configurada | Genera aviso y registro de base de datos cuando coincide el marcador | `D07`, `D08` y obligación observable |

La definición propuesta **no contiene sentencias SQL**, nombres de tablas, centros, unidades, aplicaciones internas, usuarios, contraseñas, IP, puertos, rutas, correos ni identificadores de pacientes. Esos datos se reemplazaron por referencias `PRIVATE:*`.

## 3. Destinos funcionales (nombres neutralizados)

| ID | Condición funcional | Efecto observado en configuración A | Estado de representación |
| --- | --- | --- | --- |
| D01 | Emisor lógico A y filtro de categoría | Transformación específica; envío MLLP | Parcial: requiere códigos locales |
| D02 | Emisor lógico B y consulta de identificación externa | Envío MLLP si supera filtro | Parcial: dependencia externa |
| D03 | Emisor lógico C | Modificación de campos y envío MLLP al mismo destino lógico de D01 | Parcial: valores de cabecera privados |
| D04 | Contexto de filtro igual a texto `false` | Escritura de archivo de post-procesamiento | **Orden y dependencia pendientes** |
| D05 | DFT y segmento de procedimiento presente | Despacho a otro canal lógico | **Falta correspondencia visible en B** |
| D06 | Emisor lógico B sin identificador externo registrado | Escritura de archivo tras transformación | Parcial: consulta y resultado |
| D07 | Unidad no configurada | Notificación por correo | Plantilla privada |
| D08 | Unidad no configurada | Registro en base de datos | Esquema y consulta privados |

Los **tres destinos deshabilitados** de A no se incluyen como efectos obligatorios del contrato activo; su existencia debe conservarse en el inventario de migración, no suponerse operativa.

## 4. Diferencias y riesgos detectados — no afirmar equivalencia

**D-01 · Salida habilitada sin correspondencia:** la configuración A tiene un destino interno habilitado para mensajes DFT con PR1. En la configuración B no aparece su operación o llamado equivalente dentro de la producción entregada. Esto es una **brecha funcional observable potencial**. No puede darse conformidad completa mientras no se resuelva.

**D-02 · Reordenamiento de destinos:** en A se evalúa D03 antes de D04; en el proceso convertido B se evalúa D04 **antes** de D03. D04 depende del contexto `Filtro`, que los transformadores de destino pueden establecer. Para mensajes que solo alcanzan D03, el resultado de D04 podría cambiar. **Hipótesis de divergencia a comprobar**; no se afirma un resultado runtime sin ejecutar ambos motores.

**D-03 · Conversión no cerrada:** la propia cabecera de B informa **dos asuntos por resolver manualmente**, **cuatro parámetros de entorno** y **diecisiete verificaciones**. También informa credenciales sin contraseña dentro de la exportación. Son advertencias del generador, no evidencia de que todo esté pendiente actualmente en la instalación.

**D-04 · Condiciones generadas:** la expresión de admisión en el proceso B contiene construcciones con comillas y paréntesis generados cuya sintaxis y equivalencia deben compilarse y comprobarse. No puede asumirse ejecución correcta solamente por ser XML estructuralmente válido.

**D-05 · Dependencias externas y temporización:** la resolución de unidad y los filtros consultan datos externos. La recepción A declara respuesta antes del procesamiento; no se aportó prueba de misma respuesta, reintentos, entrega, errores o latencia bajo B.

**D-06 · Códigos y reglas confidenciales:** el orden de las decisiones fue conservado, pero los predicados, listas y resultados institucionales se anonimizaron. Mientras no exista una vinculación local segura de esas reglas, la PFD **no puede reconstruir el comportamiento completo**.

**D-07 · Semántica literal de filtros:** una rama de origen verifica tipos de paciente mediante búsqueda de subcadena sobre una lista delimitada y modifica `PV1.2` **antes** de decidir la exclusión. No es equivalente sin más a una operación abstracta de pertenencia a conjunto. Se preservó la condición literal en D01 para revisión.

**D-08 · Pausa interna de salida:** una ruta a fichero ejecuta una pausa tras eliminar el primer OBX; la versión convertida también contiene una pausa breve. No se impone como semántica normativa de PIIS, pero su costo completo se mide en End-to-End.

**D-09 · Concatenación de consultas:** en A aparecen consultas construidas concatenando campos de mensajes. Es un **riesgo potencial** de seguridad/calidad a revisar; no se infiere explotación ni se copia SQL a la PFD.

## 5. Separación PIIS correcta: definición / contrato / interpretación / evidencia

1. **Definición funcional portable (PFD):** `Rule`, `Operation`, `Destination`, condiciones, efectos y dependencias declaradas. Los ocho destinos habilitados siguen siendo obligaciones lógicas aun si el destino B omite alguno.
2. **Contrato observable:** salidas de red, ficheros, notificaciones, registros y comportamiento de filtros que deben comprobarse, sin exigir la misma arquitectura interna.
3. **Interpretaciones nativas:** las dos configuraciones adjuntas son implementaciones/representaciones candidatas; no forman parte de la PFD anonimizada.
4. **Evidencia de conformidad:** **ninguna entregada**. Los casos `TC01`–`TC09` son escenarios propuestos, no pruebas pasadas.

La representación JSON es **un ejemplo de instancia** siguiendo los conceptos del Draft 02 de PIIS. No hay todavía un JSON Schema normativo, semántica operacional ratificada ni sintaxis aprobada. Validar que este archivo es JSON correcto **no demuestra** que es un estándar portable ni que ambos motores cumplen el contrato.

## 6. Qué necesitamos para la siguiente iteración (sin exponer secretos)

- Completar **localmente**, fuera del repositorio público, la política de códigos/decisiones y las dependencias de `PIIS_BINDINGS_PRIVATE_TEMPLATE.json`.
- Resolver explícitamente la salida D05 y la dependencia de orden de D04.
- Aportar mensajes **sintéticos**, con identificadores clínicos inventados, diseñados para disparar cada rama. Nunca publicar muestras productivas con datos personales.
- Ejecutar los mismos escenarios en ambas implementaciones en un entorno controlado y observar **todos** los efectos, no solo el mensaje principal.
- Registrar la recepción/ACK, exclusiones, tiempos de respuesta y fallas. Con los resultados podremos distinguir `Conformant`, `Non-conformant` y `Not demonstrated` por caso/alcance.

## 7. Política de anonimización aplicada

Se conservaron **solo identificadores públicos de campos HL7**, tipos de efectos, categorías de operaciones, orden de decisiones y algunos valores funcionales breves (`DFT`, `I`, `O`, `C`, `NC`, `D`, `000000`, `000001`, sufijos de archivos). Se ocultaron constantes y tablas institucionales, orígenes y destinos, direcciones, puertos, directorios, correos, usuarios y cualquier contraseña. No se reprodujo ningún mensaje de paciente. **El propio patrón de negocio también puede ser sensible**: el documento necesita revisión humana antes de publicarse fuera de esta conversación.

**Conclusión técnica:** primer PFD PIIS **parcial y anonimizado**, útil para contrastar modelos de implementación, pero todavía **no válido para portabilidad ejecutable ni para afirmar conformidad**.