# PIIS — Experimento 05: revisión de SQL anonimizado

**Estado:** evidencia de configuración, no conformidad ni equivalencia de comportamiento.

## Objetivo

Retener dentro de `PIIS.json` la **estructura de consultas SQL** identificadas en la configuración de ESB-A, sin revelar tablas, columnas, esquemas, alias, valores, parámetros originales, credenciales o contenido de scripts. La vinculación con ESB-B sigue siendo un elemento **pendiente de revisión**, no una confirmación de la misma consulta.

## Datos incluidos

- `PIIS.json#/SQLEvidence`: **263 entradas** con `id`, `flowRef`, `componentRef`, `esb`, `origin`, `capture`, `query_redacted` y estado de revisión.
- **44** entradas recuperadas desde campos de configuración SQL completos. *Completo* se refiere al contenido estático de ese campo, no a la semántica ni al resultado de su ejecución.
- **219** fragmentos literales SQL encontrados en scripts de ESB-A, marcados expresamente `PARTIAL_STATIC_LITERAL_FRAGMENT` y `FRAGMENT_NOT_EXECUTABLE`.
- **75 flujos** con al menos una entrada SQL; otros flujos pueden contener SQL construido dinámicamente no recuperable mediante inspección estática.
- **1** propiedad de consulta dinámica sin fragmento SQL extraíble de forma segura.
- `FlowCandidates[*].sql_evidence_refs` y `flow_reviews[*].sql_evidence_refs` conservan la trazabilidad con identificadores sintéticos.

## Reglas de anonimización

| Elemento en SQL | Sustitución | Qué se mantiene |
| --- | --- | --- |
| Nombres de tablas / esquemas | `TABLE_001`, etc. (identificadores genéricos) | Ubicación relativa en FROM/JOIN/UPDATE/INTO |
| Columnas / expresiones de identificador | `FIELD_001`, etc. | Selección, comparaciones, relación entre referencias repetidas |
| Alias | `ALIAS_001`, etc. | Referencias y calificación de campos cuando se detectan |
| Funciones no estándar | `FUNCTION_001`, etc. | Estructura de llamada y argumentos; funciones SQL comunes se conservan |
| Constantes de texto | `'VALUE_001'`, etc. | Tipo léxico de cadena y lugar del literal |
| Constantes numéricas | `:NUMBER_001`, etc. | Posición de la constante; no su valor original |
| Parámetros y variables | `:PARAM_001`, etc. | Posición del parámetro; no nombre ni valor |
| Comentarios SQL | eliminados | Ninguna anotación privada |

Las sustituciones son **estables dentro de cada consulta**, pero no se pretende un diccionario de equivalencia entre consultas diferentes. La transformación es deliberadamente no reversible. **No ejecutar estas plantillas**: el valor de constantes y parámetros se ha suprimido y puede cambiar la semántica. Para conservar reglas funcionales comparables se requieren escenarios sintéticos con expectativas explícitas.

## Ejemplo publicado (solo forma anonimizada)

```sql
SELECT FIELD_001, FIELD_002
FROM TABLE_001
WHERE FIELD_003 = :PARAM_001
ORDER BY FIELD_002
```

## Limitaciones y decisiones pendientes

1. Los scripts pueden construir SQL concatenando texto, funciones y variables; una porción literal no es una consulta completa. No se inventan partes faltantes ni se interpreta su lógica.
2. ESB-B fue generado desde ESB-A. El análisis **no reconstruye ni empareja todavía sentencias SQL ejecutadas en ESB-B**: no existe evidencia independiente suficiente para declarar igualdad semántica.
3. Las plantillas conservan la estructura **reconocible** de SQL, no garantizan sintaxis compilable ni el comportamiento de funciones de un dialecto particular.
4. La anonimización automatizada es una protección adicional, **no** certifica ausencia de secretos, cumplimiento contractual, ni ausencia de información sensible.
5. Estado PIIS: `NOT_DEMONSTRATED`. No se aplicó un test funcional de consultas, se ejecutó ninguna sentencia real, ni se certificó conformance.

Para continuar: seleccionar consultas estáticas y un flujo dinámico, diseñar tablas y datos **totalmente sintéticos**, y comparar observables (resultado, orden, estados de error) en un entorno controlado.