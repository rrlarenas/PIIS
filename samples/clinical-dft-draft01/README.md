# Sample 01 — Clinical DFT integration (anonymized)

**Status:** Exploratory PIIS case study. **Not normative, not executable, not validated and not conformant by claim.**  
**Reference:** [PIIS Working Draft 02](../../drafts/PIIS_Working_Draft_02_EN.md) (English translation; Spanish original is the reference text).  
**Related review:** [Portable functional model and observable contract — issue #2](https://github.com/rrlarenas/PIIS/issues/2).

## Purpose

A concrete first exercise in describing an integration interface **by functional obligations and observable effects**, rather than by the internals of its original engine.

The source material consisted of two private XML exports: a configured HL7 v2 DFT integration channel and a generated conversion to another integration engine. **These exports are not published and are not independent proof of behavioral equivalence.**

## Published files

| File | Purpose |
| --- | --- |
| [PIIS_PFD_DFT_DRAFT01.json](PIIS_PFD_DFT_DRAFT01.json) | Proposed, partial and anonymized portable functional definition, including source, rules, operations, enabled destinations, observable contract and candidate test scenarios |
| [PIIS_ANALISIS_COMPARATIVO_DRAFT01.md](PIIS_ANALISIS_COMPARATIVO_DRAFT01.md) | Spanish evidence-based comparison, limitations and unresolved differences |
| [PIIS_BINDINGS_PRIVATE_TEMPLATE.json](PIIS_BINDINGS_PRIVATE_TEMPLATE.json) | **Empty placeholders only** for private endpoint and business-policy bindings; do not fill or commit operational values |

## What the exports support

- An HL7 v2 DFT-family interface over MLLP/TCP.
- Source acceptance logic, transformations and external lookups.
- Eight originally enabled logical destinations with message, file, internal dispatch, notification and database effects.
- A candidate observable contract and nine **proposed but unexecuted** conformance scenarios.

## What they do **not** establish

- Independently implemented systems meeting an identical functional contract.
- Executed conformance tests, output equivalence or successful end-to-end migration.
- Complete public reconstruction: institutional business mappings, endpoint configuration and SQL rules are deliberately absent.
- Approved PIIS syntax or a validated normative JSON Schema.

Two issues require specific investigation: **one enabled internal dispatch in the original lacks a visible match in the converted export**, and **some destination evaluation order differs**. Neither discrepancy alone constitutes execution evidence.

## Security and distribution

The published sample deliberately excludes the raw exports, IP addresses, ports, credentials, email addresses, operational paths, private SQL and institution-specific identifiers. **The blank bindings template contains no values and must remain unpopulated in public.** Abstracted business-process structure may still deserve an owner's confidentiality review before reuse elsewhere.

External standards such as HL7 v2, MLLP and TCP are reused, not redefined.

## Next experiment

With **synthetic** messages and a **private**, locally bound policy, run identical cases on both engines and compare every required external effect, errors and acknowledgment behavior. Record passing, failing and not-demonstrated outcomes independently; do not infer equivalence from converted XML.

---

### Español

Primer caso práctico anonimizado de PIIS: una interfaz HL7 DFT descrita mediante funciones, reglas y efectos observables, sin publicar los XML de origen ni los parámetros de implementación. **No es un esquema normativo, no es ejecutable, no demuestra conformidad ni equivalencia entre motores.** El [análisis comparativo](PIIS_ANALISIS_COMPARATIVO_DRAFT01.md) detalla los hallazgos y las diferencias pendientes.
