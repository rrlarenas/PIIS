# PIIS JSON PFD 0.1 — Baseline Critical Review 01

**Status:** OPEN findings for public discussion — no decisions adopted.  
**Review date:** 29 October 2026  
**Scope:** The versioned [JSON PFD proposal](SPECIFICATION.md), [exploratory JSON Schema](piis-pfd-exploratory-0.1.schema.json), and the two published anonymized examples.  
**Primary discussion:** [Issue #4](https://github.com/rrlarenas/PIIS/issues/4).  
**No assertion:** Neither case has been executed as a PIIS implementation or independently proven conformant.

## 1. Evidence baseline

These observations come from the **published JSON examples**, not from running their original engines.

| Feature | [Sample 01 — DFT](../../samples/clinical-dft-draft01/PIIS_PFD_DFT_DRAFT01.json) | [Sample 02 — scheduled financial documents](../../samples/tax-documents-draft01/PIIS_PFD_TAX_DOCUMENTS_DRAFT01.json) | Consequence |
| --- | --- | --- | --- |
| Source kind | `inbound_message` | `scheduled_database_poll` | A neutral PFD must represent both externally triggered and scheduled starts |
| Operations | 9 `Operation` entries | 7 `Operation` entries | Common IDs, `sequence` and `type`, but each operation has its own undocumented payload shape |
| Destinations | 8 | 2 | The conceptual model covers multiple effects; their dispatch and completion semantics remain unspecified |
| External dependencies | 6 | 5 | Binding existence does not prove that a target can reproduce dependency behavior |
| Observable contract | `required_effects` (4); `forbidden_effects` (3) | `required_effects` (5); `forbidden_effects` (3) | These fields are currently arrays of human-readable **strings**, not executable assertions |
| Test-case location | `ConformanceCases.scenarios` (9) | `ConformanceCases.cases` (9) | The same proposed concept has different key names |
| Execution evidence | Empty `ConformanceCases.evidence` | Empty `ConformanceCases.evidence` | Conformance is `NOT_DEMONSTRATED` for both |

Both examples also declare `schema_status: PROPOSED_NOT_STANDARDIZED`, `semantic_status: PARTIAL_REDACTED`, and `conformance_status: NOT_DEMONSTRATED`. These are **self-declared metadata**; they are not verified by a JSON Schema check.

## 2. Findings for falsification

### F-01 — Insufficient execution semantics (**blocking for portable implementations**, not blocking for structural review)

**Observed:** `Operation` entries carry a shared identifier, order index and type string, but the semantics and parameter vocabulary of individual operations are not standardized. `Rule` and `Channel` are structurally unrestricted objects. Both samples contain prose obligations and incomplete private policies.

**Inference:** A third-party engine cannot be expected to reconstruct all required behavior *from the published PFD alone*. Schema validation is therefore not a substitute for a portable functional definition.

**Challenge:** Demonstrate, on one fully synthetic and publicly shareable interface, what each operation means, its inputs and outputs, conditional evaluation, state changes, side effects, and failure/rollback rules. Check existing DSLs before proposing proprietary PIIS operators.

**Decision:** OPEN. No new operator vocabulary is approved.

### F-02 — Observable contract is not yet machine-verifiable (**blocking for conformance claims**)

**Observed:** `BehaviorContract.required_effects` and `forbidden_effects` are **arrays of strings**. The two samples also differ in supplementary fields. `ConformanceCases` holds proposed scenarios and empty execution evidence.

**Inference:** Independent evaluators cannot reliably decide pass/fail from string descriptions alone. Error and asynchronous-completion obligations are especially difficult to compare.

**Challenge:** Describe the **minimal typed assertion set** and a shared observation vocabulary (e.g., received, delivered, persisted, rejected, alerted) without prescribing native internal steps. Establish how test oracles distinguish allowed variability from missing effects.

**Decision:** OPEN. No conformance profile or claimed interoperability.

### F-03 — Existing examples use incompatible names (**normalization decision required**)

**Observed:** Sample 01 uses `ConformanceCases.scenarios`; Sample 02 uses `ConformanceCases.cases`. Source trigger shapes, operation details, and several `BehaviorContract` properties also differ.

**Inference:** Accepting either JSON key in proposal 0.1 preserves both inputs but leaves an ambiguous authoring convention.

**Challenge:** Choose one canonical representation for a future revision and document a lossless, reviewed mapping from each sample. Preserve original evidence separately.

**Decision:** OPEN. No rename performed on the archived samples.

### F-04 — Structural validity permits semantically empty or ambiguous models (**scope limitation in 0.1**)

**Observed directly in the schema:** `Operation`, `Destination`, `Dependency`, `required_effects`, and `forbidden_effects` have **no `minItems`**. `Rule` and `Channel` have no required internal keys. Repeated operation/destination IDs are not disallowed. `additionalProperties` is enabled across the envelope.

**Inference:** A document can pass this **structural** schema even with no operations or no required effects, or with duplicate IDs. This is acceptable as an intentionally permissive review shape but unacceptable as a future claim of behavioral completeness.

**Challenge:** Decide which constraints belong to the JSON Schema, which require semantic/cross-reference validation, and which are *profile-specific* (for example, a legitimate no-op interface).

**Decision:** OPEN. Do not tighten the schema simply to make it appear normative.

### F-05 — `sequence` does not settle concurrency and completion (**requires case evidence**)

**Observed:** Each operation carries an integer `sequence`. The source examples feature external dependencies and potentially multiple destinations, but neither supplied JSON defines a general dependency/partial-order graph.

**Inference:** A linear sequence alone may not describe parallel branches, join conditions, transactional boundaries, asynchronous completion, or failure propagation.

**Challenge:** Identify which ordering is externally observable and required, and whether a dependency graph or an existing workflow notation can carry it without introducing a new PIIS execution language.

**Decision:** OPEN. Internal scheduling remains implementation-specific.

### F-06 — Redaction is an intentional public limitation (**do not fill gaps by inference**)

**Observed:** The case studies contain `PRIVATE:...` placeholders and omit original endpoint, database and business-policy details. Sample 02's generated conversion explicitly lacks the SOAP sending implementation.

**Inference:** They are useful research inputs, but **cannot** yet prove lossless migration or functional equivalence. The public PFD cannot be reconstructed into the original private interface without authorized supplementary configuration and clarification.

**Challenge:** Prepare a **new synthetic reference interface** with fully disclosed functional rules and no private operational data. Distinguish *public semantics* from *private deployment bindings* rather than concealing functional meaning inside a secret.

**Decision:** OPEN. The published samples remain as anonymized evidence, not executable reference implementations.

### F-07 — Standardization needs a verified novelty boundary (**standards-body decision deferred**)

**Observed:** [Prior-art assessment](../../research/PRIOR_ART_AND_GAP_ASSESSMENT_01.md) identifies documented overlap with MDA, Open Workflow, BPEL, BPMN, SCA, XPDL and integration pattern catalogs.

**Inference:** PIIS's strongest potential contribution may be a profile/contract/benchmark complement rather than an entirely new general-purpose workflow language. That hypothesis remains unproven.

**Challenge:** Cite exact existing normative clauses and attempt to express the proposed synthetic interface in at least one existing portable specification before inventing any new semantics.

**Decision:** OPEN. No assertion that PIIS is an approved standard or IETF RFC.

## 3. How to review one finding

Please comment in [issue #4](https://github.com/rrlarenas/PIIS/issues/4) using as much of this minimal structure as useful:

> **Finding:** F-0x  
> **Claim challenged:** [exact assertion / key / operation]  
> **Evidence:** [specification and section, code, minimal *synthetic* input, or reproducible observation]  
> **Impact:** [which observable behavior or migration result changes?]  
> **Proposed resolution:** [reuse existing standard / refine PIIS / mark unsupported / reject hypothesis]  
> **Verification:** [how would an independent reviewer falsify or confirm this?]

**No confidential exports, endpoint details, real records, patient information or proprietary secrets.** Participants are welcome to demonstrate that a claimed PIIS gap was already solved elsewhere.

## 4. Gate for 0.2 — no automatic promotion

A next version should only be drafted as an **explicit proposal**, with a traceable changelog and an issue-based rationale, once at least:

- [ ] F-01 and F-02 have *specific proposed semantics* supported by examples or existing standards, or explicitly scoped exclusions.
- [ ] F-03 has a canonical naming decision and a mapping for both current samples.
- [ ] F-04 has a justified structural-versus-semantic validation boundary.
- [ ] F-05 has a documented, falsifiable observable-ordering model or clear scope restriction.
- [ ] F-06 has a fully synthetic, safely publishable **complete** test case.
- [ ] F-07 has a reasoned reuse/profile/extension/new-specification decision.
- [ ] The decisions and counterarguments are recorded publicly, even if only the PIIS maintainer has commented.

**External endorsement is not required to make progress**. Lack of responses is not technical evidence and must not be represented as consensus.

This file is a **baseline critique**, not a passed review, adopted decision, certification, or formal RFC.
