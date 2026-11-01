# PIIS — Experimento 05: evidencia SQL anonimizada (ESB-A / ESB-B)

**Estado:** candidato exploratorio; análisis estático, **no** conformance ni equivalencia funcional demostrada.

Este experimento amplía los hallazgos del [Experimento 04](../esb-a-esb-b-real-installation-04/README.md) para conservar la **estructura de las consultas SQL** dentro de la definición PIIS candidata. Se origina en dos configuraciones de una instalación real: ESB-A y una configuración ESB-B generada mediante conversión, con acciones manuales, ajustes y verificaciones pendientes. **No se presupone ni se demuestra que ambas produzcan los mismos resultados funcionales**.

## Resultados

| Evidencia estática | Cantidad |
| --- | ---: |
| Interfaces candidatas ESB-A | 136 |
| Destinos lógicos ESB-A | 263 |
| Flujos con evidencia SQL | 75 |
| Registros SQL anonimizados | **263** |
| Consultas de propiedades configuradas | **44** |
| Fragmentos SQL literales de scripts | **219** |
| Propiedades con SQL dinámico no reconstruido | 1 |
| Hallazgos generales de revisión | 60 |

**Importante:** las 44 consultas provienen de campos de configuración recuperados íntegramente de su propiedad, pero están anonimizadas y **no** se consideran semánticamente completas o ejecutables. Los 219 fragmentos extraídos de scripts se marcan como `PARTIAL_STATIC_LITERAL_FRAGMENT` y requieren reconstrucción manual con evidencia adicional. La configuración ESB-B permanece sin verificación de comportamiento SQL equivalente.

## Archivos publicados

- [`PIIS.json`](PIIS.json): definición candidata para 136 flujos, con `SQLEvidence` y referencias desde cada flujo; estado `NOT_DEMONSTRATED`.
- [`review_report.json`](review_report.json): hallazgos, correspondencias y resumen de extracción SQL.
- [`SQL_EVIDENCE.csv`](SQL_EVIDENCE.csv): 263 consultas o fragmentos SQL anonimizados, vinculados a flujos y componentes sintéticos.
- [`flow_matrix.csv`](flow_matrix.csv): correspondencia estática de las 136 interfaces.
- [`SQL_ANALYSIS.md`](SQL_ANALYSIS.md): reglas de anonimización, alcance y límites de la extracción.
- [`validate_outputs.py`](validate_outputs.py): comprobaciones estructurales y búsqueda básica de patrones sensibles; **no** certificación de anonimización ni conformidad funcional.

## Protección de información

**No se publican los XML originales**, conexiones, credenciales, datos de pacientes, scripts fuente ni nombres de instalaciones. Las consultas sustituyen tablas, esquemas, columnas, alias, funciones propias, valores y parámetros por marcadores genéricos. Se conserva la estructura SQL reconocible, pero no se intenta conservar el SQL ejecutable. Los nombres externos son únicamente **ESB-A / ESB-B** y las unidades de implementación se denominan **componentes**.

La ausencia de patrones sensibles conocidos en la validación automática **no certifica** anonimización contractual o legal. La publicación es un conjunto derivado para revisión técnica, no una exportación reutilizable del sistema original.

## Validación y siguiente paso

Ejecutar en esta carpeta:

```sh
python validate_outputs.py
```

La validación revisa integridad de referencias, cantidades y patrones evidentes. No utiliza motores ni bases de datos. Para evaluar comportamiento en una etapa posterior deberán construirse tablas, datos, respuestas y pruebas **totalmente sintéticos**, y resolver las acciones pendientes de ESB-B antes de emitir juicios de equivalencia.

Debate de la especificación: [PIIS JSON 0.1 — issue #4](https://github.com/rrlarenas/PIIS/issues/4). **El Experimento 05 no cambia el esquema normativo ni sustituye las evidencias del Experimento 04.**
