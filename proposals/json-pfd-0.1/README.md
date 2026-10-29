# PIIS JSON PFD — First Public Schema Review

**Proposal:** version `0.1` · **Non-normative** · **Not executable** · **Conformance not demonstrated**

This folder is the beginning of a reviewable **JSON representation proposal** for the PIIS Portable Functional Definition (PFD) and its Observable Contract (OC), derived from the two published, anonymized case studies.

**Start here:** [Specification proposal](SPECIFICATION.md) · [Schema](piis-pfd-exploratory-0.1.schema.json) · [Review questions](OPEN_QUESTIONS.md).

### Existing test data (not migrated or changed)

- [Sample 01 — clinical HL7 DFT interface](../../samples/clinical-dft-draft01/PIIS_PFD_DFT_DRAFT01.json)
- [Sample 02 — scheduled financial-document interface](../../samples/tax-documents-draft01/PIIS_PFD_TAX_DOCUMENTS_DRAFT01.json)

The schema is deliberately permissive beyond the fields common to both. It **accepts** the two samples structurally but is not a portable execution language. Treat any warning about unknown/missing semantics as a research question, not as an invitation to fill gaps with invented values.

### Local structural checks

Install a JSON Schema Draft 2020-12 validator, for example:

```sh
python -m pip install "jsonschema>=4.18,<5"
python proposals/json-pfd-0.1/validate_samples.py
```

The validator checks the schema itself, both existing examples, and two deliberately invalid variants. It does **not** execute integration interfaces, compare runtimes or audit confidentiality.

### Scope of review

Please challenge the semantics, names, incompleteness and overlap with existing specifications, not only JSON syntax. The goal is to **avoid inventing a new general-purpose workflow language** if a standards-based model already supplies the required portable behavior.

The original [PIIS Working Draft 02](../../drafts/PIIS_Working_Draft_02_EN.md) and its Zenodo publication remain unchanged.
