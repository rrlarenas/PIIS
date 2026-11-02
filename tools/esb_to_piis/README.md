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

Perfiles iniciales (detección estructural, sin certificación del formato nativo):

- XML de canales: raíz `channel`, `list`, `channels` o `serverConfiguration`
  con elementos `channel`.
- XML de clases: raíz `Export` con elementos `Class`.
- Evidencia anonimizada `SanitizedExport` del experimento 01, identificada
  expresamente como incompleta y no importable.

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
