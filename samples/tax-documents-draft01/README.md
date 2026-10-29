# Sample 02 — Scheduled financial-document integration (anonymized)

**Status:** Exploratory PIIS Portable Functional Definition (PFD). **NOT_DEMONSTRATED; not executable, not validated, and not a normative PIIS JSON Schema.**

**Reference:** [PIIS Working Draft 02](../../drafts/PIIS_Working_Draft_02_EN.md) · [Sample 01](../clinical-dft-draft01/README.md)

## Purpose

A second case study of PIIS's **proposed JSON functional representation**: a scheduled database poll retrieves rows describing financial/tax documents, maps each row to an XML element, sends data to an external SOAP service, processes its response records, writes back resulting status, and conditionally sends an error notification.

The original source was a configured integration channel; the second export is **a generated conversion** to another engine paradigm, not an independently verified implementation. **The source XML exports and the anonymized engine-native XML copies are intentionally not published here.** The JSON case study is the published artifact.

## Published files

| File | Scope |
| --- | --- |
| [PIIS_PFD_TAX_DOCUMENTS_DRAFT01.json](PIIS_PFD_TAX_DOCUMENTS_DRAFT01.json) | Anonymized proposed functional definition: scheduled trigger, source query, 24 positional field mappings, SOAP request/response, per-record updates, alert selection, dependencies, observable behavior and **nine unexecuted** test scenarios |
| [PIIS_BINDINGS_PRIVATE_TEMPLATE.json](PIIS_BINDINGS_PRIVATE_TEMPLATE.json) | **Unpopulated** binding placeholders for database procedures, private payload tags, SOAP operation and notifications; never commit populated values |
| README.md | Scope, evidence limits, and publication precautions |

## Source-derived functional sequence

1. At the configured interval, invoke a database procedure to obtain rows via an output cursor.
2. Serialize each row into one XML element containing **24 fields**, preserving its positional mapping and observed cursor order.
3. Submit the constructed content through a SOAP 1.1 integration destination.
4. Parse SOAP response records and write back five logical response fields for each record.
5. Collect non-`OK` response statuses, and send an HTML email alert when any are present.

The **underlying XML, SOAP 1.1, SMTP, SQL and transport conventions remain external to PIIS**, which does not redefine them.

## Evidence and known non-equivalence

- The converted export contains a **manual placeholder for the SOAP sender that returns an error**. Its required external send behavior is not implemented in the supplied conversion.
- Source code concatenates sibling XML elements from multiple result rows, with no enclosing root in the observed returned string. Well-formedness and downstream behavior for multi-row batches require runtime testing.
- SOAP operation contract, XML field tags, database procedure contracts, infrastructure and alert recipients are intentionally private. The public PFD is consequently **partial**, not directly realizable from this JSON alone.
- Database errors, retries, timeouts, idempotency, null handling, XML escaping, and end-to-end completion criteria have not been established from execution evidence.

A conversion-generated architecture is **not** proof of functional equivalence between independent engines. The JSON's conformance cases are proposals, **not executed test results**.

## Confidentiality

Published files exclude the XML exports, endpoints, IP addresses, ports, usernames/passwords, recipients, original business identifiers and private SQL definitions. Every environment-specific placeholder is unpopulated. This is a technical anonymization step, **not a certification that abstract business workflows are non-confidential**.

## Next validation exercise

With a privately configured test environment and **synthetic documents**, evaluate identical input and response cases on both implementations. Record each externally observable effect, error and status write-back; classify failures and unknowns explicitly. Do not claim a passing conformance suite or compare performance until required functionality has been shown.

---

### Español

Segundo caso PIIS en **JSON propuesto**: consulta periódica a base de datos, construcción de documentos XML, envío SOAP, actualización de resultados y alerta condicional. Los nombres, campos de negocio y dependencias privadas están ocultos. **El envío SOAP del motor convertido está pendiente de implementación.** No se publican los XML nativos ni se afirma equivalencia, ejecutabilidad o conformidad. Este ejemplo servirá para estudiar qué aspectos faltan en el modelo portable antes de normalizar el esquema.
