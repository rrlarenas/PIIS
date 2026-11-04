# Validador exploratorio de exports ESB para PIIS

Python 3.10 o superior. Inspecciona un export XML local y, opcionalmente,
valida un PFD JSON contra la propuesta estructural PIIS 0.1 del repositorio.
No genera una conversión ejecutable ni demuestra equivalencia funcional.

Desde la raíz del repositorio:

```powershell
python -m pip install -r tools/esb_to_piis/requirements.txt
python tools/esb_to_piis/validate.py export.xml --piis PIIS.json --output informe.json
```

Ejemplo reproducible con evidencia pública:

```powershell
python tools/esb_to_piis/validate.py experiments/esb-a-esb-b-hl7-01/ESB-A_export_redacted.xml --output informe.json
```

Perfiles (detección estructural, sin certificación del formato nativo):

- XML de canales: raíz `channel`, `list`, `channels` o `serverConfiguration`
  con elementos `channel`.
- XML de clases: raíz `Export` con elementos `Class`.
- Evidencia anonimizada `SanitizedExport` del experimento 01, identificada
  expresamente como incompleta y no importable.
- Rhapsody: archivo `.rlc` ZIP con un `Engine` en el namespace de Rhapsody
  y configuraciones SQL XML asociadas; también XML de Engine o configuración
  SQL reconocida individual. No se extraen archivos al disco. Se limita el
  tamaño descomprimido acumulado a 32 MiB y el archivo a 512 entradas;
  se rechazan archivos cifrados, entradas duplicadas y contenido no XML.
- IBM ACE: `.msgflow` y `.subflow` XMI/Ecore con nodos y conexiones,
  mapas `.map` y módulos `.esql`. Los nodos Java y las referencias a subflujos
  se mantienen como lógica opaca o dependencias externas. Los `SET` y `SELECT`
  sobre árboles de mensajes ESQL no se consideran automáticamente SQL de base de datos.
- Apache Camel: XML DSL de Spring con contextos, rutas y plantillas. Se cuentan
  componentes y transportes reconocidos sin copiar URI, nombres ni parámetros.
- WSO2/Synapse: API, proxy, endpoint, secuencia, entrada local, almacén y
  procesador de mensajes en el namespace de Synapse.

La versión 0.2 conserva la CLI y los códigos de salida. Ejemplo Rhapsody:

```powershell
python tools/esb_to_piis/validate.py samplesESB/rhapsody/upstream/data-ingestion-service/src/main/resources/rhapsody/NBS-Data-Ingestion-ELR-Route.rlc --output informe.json
```

Los adaptadores nuevos emiten categorías permitidas, referencias sintéticas y
señales estáticas. Para SQL explícito se reconoce un subconjunto léxico de
SELECT/INSERT/UPDATE/DELETE de una tabla. Solo se emiten `table-NNNN` y
`field-NNNN`, con identidad consistente dentro del mismo artefacto. No se
publican consultas, literales, parámetros ni mapas reversibles de nombres.
JOIN, UNION, subconsultas y otras construcciones no resueltas quedan parciales
o `UNRESOLVED`. Los campos se extraen de listas simples y ciertas comparaciones;
no es un parser semántico SQL. PASSTHRU y referencias Database en ESQL quedan
como lógica de base de datos pendiente, sin inferir efectos. Ausencia de SQL
detectado no prueba ausencia de efectos de base de datos.

Primera comparación reproducible de los cuatro motores:

```powershell
python experiments/esb-multiengine-anonymized-06/build_experiment.py
```

Los cuatro casos anonimizados, evidencia SQL y matriz están en
[`experiments/esb-multiengine-anonymized-06`](../../experiments/esb-multiengine-anonymized-06/README.md).
El constructor verifica los hashes de las fuentes antes de analizarlas, no
ejecuta integraciones ni requiere red. Los JSON de esquema, descriptores,
Java, POM y otros archivos auxiliares se contabilizan como excluidos, no como
flujos soportados. Las importaciones, clases Java, secuencias referenciadas y
plantillas no se resuelven entre archivos; los recuentos no se deduplican.

Los namespaces XML se admiten. Otros formatos se rechazan explícitamente;
un XML bien formado por sí solo no se acepta como export reconocido.
El inventario usa referencias sintéticas por orden documental y no exporta
nombres, valores, scripts, consultas ni credenciales. Incluye SHA-256 del XML
para identificar la evidencia local. No es un certificador de anonimización.
No ejecuta código del export ni realiza conexiones de red. Rechaza DTD,
entidades y entradas de más de 32 MiB.

`--piis` valida exclusivamente el esquema del PFD; no relaciona automáticamente
sus operaciones con los componentes del ESB. `source_target_coverage` permanece
`NOT_CHECKED`: aún hace falta definir un mapeo verificable por adaptador.
Las brechas semánticas quedan explícitas en `findings` y la conformidad funcional
siempre queda `NOT_DEMONSTRATED`. Los errores de esquema muestran la palabra
clave incumplida sin copiar valores de la configuración.

Códigos de salida:

- `0`: export reconocido y, si fue provisto, PFD estructuralmente válido.
  Puede haber advertencias y trabajo manual pendiente.
- `1`: PFD no válido contra el esquema exploratorio.
- `2`: error de lectura, XML/JSON inválido, formato no soportado, entrada
  insegura o error de escritura/uso de CLI.

Pruebas sintéticas y regresión con los dos XML públicos:

```powershell
python -m unittest discover -s tools/esb_to_piis -p "test_*.py"
```
