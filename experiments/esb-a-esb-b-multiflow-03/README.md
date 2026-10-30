# PIIS — Experimento 03: configuración de 14 flujos (ESB-A / ESB-B)

**Estado:** candidato exploratorio, **NO ejecutable**, **NO conformidad demostrada**. Los artefactos publicados emplean exclusivamente las etiquetas **ESB-A** y **ESB-B**. Los protocolos y estándares abiertos conservan sus nombres técnicos.

## Propósito

Extraer evidencia estática de dos exportaciones comparables y proponer un primer `PIIS.json` que describa **intenciones funcionales**, sin presuponer que la arquitectura interna sea la misma ni afirmar que las ejecuciones sean equivalentes.

**Precondición declarada:** ambas exportaciones pretenden proporcionar resultados funcionales equivalentes. **Evidencia real:** ESB-B indica que fue generado mediante conversión desde ESB-A; por tanto, **no** corresponde a una segunda implementación desarrollada y verificada independientemente.

## Archivos

- [`PIIS.json`](PIIS.json): definición candidata; 14 `FlowCandidates`, 19 destinos lógicos y 5 propuestas de casos de prueba. Se conservan los campos del *envelope* del esquema exploratorio PIIS 0.1, pero **no se define ni demuestra semántica portable ejecutable**.
- [`review_report.json`](review_report.json): evidencia estructural, revisión por flujo, y 20 hallazgos estáticos.
- [`flow_matrix.csv`](flow_matrix.csv): matriz legible de correspondencias sin identificadores de producción.
- [`build_candidate.py`](build_candidate.py): analizador local conservador, únicamente biblioteca estándar; **no** incluye código ni exportaciones originales.
- [`test_outputs.py`](test_outputs.py): pruebas de integridad del paquete generado y comprobaciones de filtración de patrones sensibles.

## Resultados comprobados del análisis estático

| Observación | ESB-A | ESB-B |
| --- | --- | --- |
| Flujos de integración | 14 canales | 14 categorías asociadas de forma unívoca por índice y comentario de procedencia |
| Entradas por tipo | TCP 9; HTTP 3; base de datos 2 | Diferentes componentes de recepción y proceso por flujo |
| Destinos habilitados | 19 (TCP 13; HTTP 5; SOAP 1) | Los **47** componentes funcionales exportados aparecen con `Enabled=false` |
| Componentes auxiliares | — | 1 servicio auxiliar con `Enabled=true` |
| Clases generadas | — | 38 |
| Operación sin implementar | No determinada mediante esta revisión | **FLOW-08**, operación SOAP con `TODO MANUAL` explícito |
| Pruebas de ejecución incluidas | Ninguna | Ninguna |

El estado `Enabled=false` es un **hecho del archivo exportado**, no prueba de un defecto intrínseco del motor; podría existir configuración pendiente del despliegue. No se supone que haya sido activado.

## Extracción

La herramienta reconoce conteos de canales, destinos, filtros y pasos, tipos genéricos de transporte, estado habilitado, referencias léxicas a campos HL7 y componentes de implementación de ESB-B. Verifica internamente la asociación de cada flujo con el comentario de procedencia de los componentes convertidos.

**No interpreta ni ejecuta expresiones, SQL, E4X, DTL, BPL, reglas de ruteo, códigos de error ni ACK.** La presencia coincidente de campos HL7 es una evidencia léxica, no una prueba de equivalencia de sus transformaciones.

## Ejecutar localmente

```bash
python build_candidate.py ESB-A.xml ESB-B.xml ./output
python test_outputs.py ./output
```

**Importante:** `ESB-A.xml` y `ESB-B.xml` representan las exportaciones confidenciales originales; no se incluyen en el paquete y **no** deben publicarse automáticamente. Se recomienda trabajar en un ambiente aislado y auditar por separado cualquier script y dependencia privada.

## Criterios para la siguiente iteración

1. Acordar el conjunto mínimo de semánticas funcionales por flujo y mantener explícitos los estados `UNKNOWN`.
2. Establecer trazabilidad de filtros, transformaciones, destinos, condiciones y errores sin transportar código nativo al PIIS.
3. Desarrollar casos sintéticos abiertos para probar al menos un flujo en dos implementaciones operativas.
4. Definir un contrato observable verificable y luego contrastar el resultado real en condiciones equivalentes.
5. No iniciar benchmarks de rendimiento antes de acreditar conformidad funcional.

## Privacidad y publicación

Las salidas omiten nombres de organizaciones, hostnames, direcciones IP, puertos, destinatarios, contraseñas, SQL, identificadores de los canales, datos de pacientes, scripts nativos y ejemplos de mensajes. Las referencias a campos HL7 se muestran únicamente en forma abstracta, por ejemplo `PID.3`.

La búsqueda automática de patrones sensibles es una **precaución básica, no una certificación de anonimización**. El contenido debe revisarse antes de su publicación en un repositorio público.

**Publicación:** https://github.com/rrlarenas/PIIS/tree/main/experiments/esb-a-esb-b-multiflow-03 — solo se publican derivados anonimizados; los XML confidenciales originales no se incluyen.
