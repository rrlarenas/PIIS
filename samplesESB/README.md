# Ejemplos públicos de buses y motores de integración

Colección obtenida el **4 de noviembre de 2026** para inspeccionar formatos nativos y estudiar futuros adaptadores de PIIS. Complementa los ejemplos de Mirth y HC ya disponibles en el proyecto. Los archivos de terceros se conservan sin modificar bajo `upstream/`, con sus licencias originales.

| Motor | Ejemplo y archivos principales | Fuente y licencia |
| --- | --- | --- |
| Rhapsody Integration Engine | [Ruta ELR de CDC](rhapsody/upstream/data-ingestion-service/src/main/resources/rhapsody/NBS-Data-Ingestion-ELR-Route.rlc), para recepción de resultados de laboratorio e integración con NBS Data Ingestion. El `.rlc` es un ZIP con cuatro XML; conservar su extensión para importar. | [CDCgov/NEDSS-DataIngestion](https://github.com/CDCgov/NEDSS-DataIngestion), Apache-2.0 |
| IBM App Connect Enterprise (ACE) | API REST de catálogo de té, lectura/escritura en base de datos, transformación y auditoría. Incluye [flujo REST](ibm-ace/upstream/TeaRESTApplication/gen/TeaRESTApplication.msgflow), [subflujos y ESQL](ibm-ace/upstream/TeaSharedLibrary/TeaSharedLibrary), y [aplicación callable](ibm-ace/upstream/TeaCallableApplicationV2). | [ot4i/ace-demo-pipeline](https://github.com/ot4i/ace-demo-pipeline), MIT |
| Apache Camel | [Balanceo de carga TCP con MINA](apache-camel/upstream/loadbalancing): rutas XML de Spring, round robin, failover, clases Java y prueba original del proyecto. | [apache/camel-examples](https://github.com/apache/camel-examples), Apache-2.0 |
| WSO2 Micro Integrator | [Artefactos Synapse](wso2-mi/upstream/integration/management-api-tests/src/test/resources/artifacts/ESB/server/repository/deployment/server/synapse-configs/default): API REST, proxy, endpoint, entrada local, almacén y procesador de mensajes. Son fixtures de pruebas oficiales. | [wso2/product-micro-integrator](https://github.com/wso2/product-micro-integrator), Apache-2.0 |

## Alcance de la selección

- **Rhapsody:** se incluye el archivo nativo publicado por CDC. La [guía de instalación de CDC](https://cdcgov.github.io/NEDSS-SystemAdminGuide/docs/6_microservices_deployment/docs/NM-NBS%207.11%20Data%20Ingestion%20Rhapsody%20Route%20Integration.pdf) explica la importación y las variables de SQL Server y del servicio de ingestión que debe configurar cada instalación. Se trata del motor sanitario Rhapsody, distinto del producto IBM Rational Rhapsody.
- **IBM:** se incluyen los tres proyectos de aplicación/biblioteca seleccionados, conservando descriptores y estructura. El README original referencia ACE Toolkit 13.0.4.0. Se omitieron imágenes y el controlador binario `db2jcc4.jar`; las conexiones a base de datos y otras dependencias de ejecución deben configurarse aparte. El README original contiene direcciones de demostración: no se realizaron conexiones a ellas.
- **Camel:** se incluye el módulo `loadbalancing` y el POM raíz como contexto de versiones. Consultar el [README original](apache-camel/upstream/loadbalancing/README.adoc) para construcción y ejecución. La copia es una selección del repositorio, no un checkout completo de todos sus módulos.
- **WSO2:** los seis artefactos son ejemplos independientes de configuración, no una integración autocontenida. Referencian secuencias, endpoints y servicios externos que no se incluyen; requieren completar esas referencias antes de desplegar.

No se ejecutaron ni desplegaron las integraciones. Tampoco se transformaron a PIIS ni se verificó equivalencia funcional entre ellas. El validador de `tools/esb_to_piis` versión 0.2 agrega inspección estructural de estos formatos. La [primera comparación anonimizada](../experiments/esb-multiengine-anonymized-06/README.md) conserva las brechas semánticas explícitas.

## Trazabilidad y verificación

[`manifest.json`](manifest.json) y el `SOURCE.json` de cada motor registran repositorio, commit fijo, URL de descarga, tamaño y SHA-256 de cada archivo. Se descargaron **66 archivos de origen**: Rhapsody 3, IBM 36, Camel 18 y WSO2 9.

Verificación realizada: los 66 SHA-256 coinciden con el manifiesto; se parsearon los 28 archivos XML/MSGFLOW/SUBFLOW/MAP externos y los cuatro XML internos del RLC; la comprobación CRC del ZIP de Rhapsody pasó. Esto verifica integridad y sintaxis XML, no compatibilidad con un runtime.

Para repetir la descarga de las mismas revisiones, desde la raíz del proyecto y con acceso a GitHub:

```powershell
python samplesESB/collect_samples.py
```

El script sobrescribe únicamente los archivos de esta selección y sus manifiestos. Las licencias de terceros incluidas en cada `upstream/` rigen esos materiales; no se relicencian bajo la licencia documental de PIIS.
