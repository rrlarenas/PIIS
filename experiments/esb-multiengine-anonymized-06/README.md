# Experimento 06: cuatro casos estáticos anonimizados

Primera comparación realizada el **4 de noviembre de 2026** con PIIS ESB Inspector 0.2. Cada caso corresponde, en orden, a una fuente del manifiesto de `samplesESB`: Rhapsody, IBM ACE, Apache Camel y WSO2 Micro Integrator. Son integraciones con objetivos distintos; no tienen un contrato funcional común y no representan implementaciones equivalentes.

| Caso | Artefactos inspeccionados | Componentes | SQL explícito | Lógica opaca | Referencias externas |
| --- | ---: | ---: | ---: | ---: | ---: |
| case-01 | 1 RLC | 11 | 1 SELECT, 2 INSERT | 4 | 0 |
| case-02 | 14 flujos, subflujos, módulos y mapas | 45 | 0 detectado | 7 | 20 |
| case-03 | 6 XML de contextos, rutas y plantillas | 25 | 0 detectado | 2 | 5 |
| case-04 | 6 XML Synapse | 15 | 0 detectado | 0 | 3 |

Cada `case-NN/` contiene `inventory_anonymized.json` y `sql_evidence_anonymized.json`. La [matriz CSV](comparison_matrix.csv) y el [informe JSON](comparison_report.json) permiten revisar los resultados en conjunto.

## Qué permite observar

- **case-01:** tres rutas, cuatro puntos de comunicación y cuatro filtros. El RLC contiene tres configuraciones SQL. La consulta de lectura y una inserción comparten `table-0001` y `field-0001`; la segunda inserción refiere a `table-0002`, con otros dos campos. En total se representan dos tablas y cuatro campos sintéticos. Esto es evidencia de texto SQL, no de ejecución ni de actividad de las rutas.
- **case-02:** se recuperan nodos y conexiones de los flujos, además de evidencia de transformación y módulos ESQL. Hay JavaCompute y dependencias a otros subflujos. No se incluyeron las clases Java que implementan los accesos a base de datos; los nombres de nodos o archivos no bastan para afirmar lectura/escritura. No detectar SQL en esta selección no prueba que la integración carezca de efectos SQL.
- **case-03:** se detectan entradas y salidas, rutas, una plantilla y configuración de failover. Las instancias declaradas también aparecen en el XML de prueba incluido: se cuentan declaraciones por archivo, no rutas activas únicas. Los beans y las referencias entre contextos requieren análisis adicional.
- **case-04:** se reconocen API, proxy, endpoint, almacenamiento y procesamiento programado. Las secuencias y servicios referenciados no se resuelven. Un componente de almacenamiento no demuestra por sí mismo uso de SQL.

Las diferencias de recuento reflejan formatos y selecciones heterogéneas. No son puntuaciones de portabilidad, cobertura funcional ni calidad. En todos los casos, conformidad funcional permanece `NOT_DEMONSTRATED` y cobertura origen/destino `NOT_CHECKED`. No se generó un PFD ejecutable ni se verificaron ACK, errores, transacciones, orden o reintentos.

## Anonimización

Los resultados se construyen por lista de categorías permitidas. No se copian nombres de flujo, identificadores originales, rutas de archivos, clases, scripts, consultas, tablas, campos, hosts, URI, credenciales ni valores de mensajes. Las conexiones XMI solo conservan referencias sintéticas entre nodos.

Las referencias SQL tienen alcance **por caso y artefacto**. `table-0001` en dos artefactos diferentes no implica la misma tabla. El mapa original/sintético existe únicamente en memoria durante el análisis y no se guarda. SQL complejo o dinámico queda parcial o sin resolver; no se presume una extracción exhaustiva de campos.

Los perfiles técnicos y SHA-256 de archivos completos se conservan para trazabilidad con las fuentes públicas. La anonimización elimina identificadores de configuración del resultado, pero no pretende ocultar qué productos o ejemplos públicos se estudiaron. Los originales permanecen en `samplesESB`; no se copian a este experimento.

## Reproducción

Desde la raíz del repositorio, con Python 3.10+ y las dependencias de `tools/esb_to_piis/requirements.txt`:

```powershell
python experiments/esb-multiengine-anonymized-06/build_experiment.py
python -m unittest discover -s tools/esb_to_piis -p "test_*.py"
```

La reconstrucción verifica SHA-256 de las 66 fuentes fijadas en el manifiesto, inspecciona 27 artefactos y contabiliza 39 archivos auxiliares excluidos. No requiere acceso de red, runtime ESB ni bases de datos. Las salidas son deterministas para esas fuentes y versión de herramienta.

Validación realizada: **13 pruebas aprobadas**, incluyendo regresión de los perfiles anteriores, los artefactos públicos nuevos, canarios de anonimización, SQL complejo sin resolver y rechazo de archivos ZIP/XML inseguros. Se comprobó que una segunda construcción conserva los hashes de los diez archivos de resultados, que los nombres originales de las dos tablas y cuatro campos SQL no aparecen en esos resultados y que la CLI procesa RLC y ESQL con salida exitosa.
