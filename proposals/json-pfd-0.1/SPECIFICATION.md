# PIIS JSON PFD — Review Proposal 0.1

**Status:** OPEN TECHNICAL PROPOSAL — **NOT A STANDARD, NOT AN IETF RFC, NOT A PIIS CONFORMANCE PROFILE**  
**Date:** 29 October 2026  
**Author of original PIIS proposal:** Rodrigo Larenas  
**License:** CC BY 4.0 for authored documentation  
**Basis:** [Working Draft 02](../../drafts/PIIS_Working_Draft_02_EN.md), [Sample 01](../../samples/clinical-dft-draft01/README.md), [Sample 02](../../samples/tax-documents-draft01/README.md)

## 1. Purpose and scope

This document starts a public, falsifiable review of a **JSON representation for PIIS Portable Functional Definitions (PFDs)** and their **Observable Contracts (OCs)**. It is not an attempt to prescribe native engine components, internal workflow, programming languages or transport standards.

The immediate deliverable is a **structural validation profile** covering the shared envelope of the two existing exploratory samples. It is intentionally *not* a complete, executable, interoperable language.

**A machine-validated JSON document is not evidence that an interface works, that a conversion is equivalent, or that a platform is conformant.** Those claims require separately specified semantics and independent test results.

## 2. Sources and extraction method

The following elements occur in **both** published sample JSON files and are therefore the current candidates for a common PFD envelope:

| Candidate key (case-sensitive for 0.1 compatibility) | Proposed meaning at review stage | Status |
| --- | --- | --- |
| `piis_document` | Document type, declared draft/profile and evidence states | Shared; metadata state values are not standardized |
| `Identity` | Logical identity, provenance and execution/evidence declarations | Shared |
| `ExternalStandards` | References to existing standards; no replacement or redefinition | Shared |
| `Source` | Logical input or schedule; never a requirement for a native receiver class | Shared; trigger shape differs |
| `Rule` | Functional conditions and decisions | Shared; machine-readable rule vocabulary unresolved |
| `Operation` | Proposed sequence of operations and functional intent | Shared; operation-specific payloads differ |
| `Destination` | Logical external outputs/effects and private bindings | Shared |
| `Channel` | Relations among destinations and processing outcomes | Shared; concurrency/delivery semantics incomplete |
| `Dependency` | Named, logical external capabilities and resources | Shared |
| `BehaviorContract` | Required and forbidden observable effects and other obligations | Shared; obligations presently mostly prose |
| `ConformanceCases` | Candidate test scenarios and separate evidence | Shared; field names differ |
| `KnownLimitations` | Explicit omissions, incompatibilities and unknowns | Shared |

This is a **derived proposal**, not a claim that each field already has universal semantics.

## 3. Structural schema

See [`piis-pfd-exploratory-0.1.schema.json`](piis-pfd-exploratory-0.1.schema.json).

- Based on **JSON Schema Draft 2020-12**, which is an existing, independently maintained validation standard.
- Requires the shared top-level envelope and basic types of IDs, lists, metadata, and test cases.
- Keeps unreviewed fields via `additionalProperties: true`; rejecting unknown fields now risks silently losing source-derived information.
- Accepts **either** `ConformanceCases.scenarios` or `ConformanceCases.cases`, since the two current examples differ. **Both names are provisional**.
- Does **not** validate expressions, rule execution, field mapping semantics, cross-references, secret leakage, delivery guarantees, or compatibility between engines.
- Does **not** claim support for arbitrary, complete transformation languages or source-code portability.
- Does **not** redefine HL7, SOAP, SQL, MLLP, XML, SMTP or any other external standard.

The schema is intentionally tolerant, to invite falsification and comparison. A stronger schema must follow demonstrated semantic agreement, not precede it.

## 4. Functional definitions versus observed outcomes

### Portable Functional Definition (PFD)

A PFD must eventually carry *enough functional meaning* for an independent implementation to realize an interface — not merely a channel inventory or a finite list of test examples.

The samples expose candidate elements: logical sources, ordered operations, conditional rules, external queries, transformations, routing, logical destinations, private dependencies, and observable side effects.

**Unresolved:** operation vocabulary; expressions and evaluation order; handling of state and nondeterminism; allowed custom-function portability; exact interaction with external protocols; capability negotiation and unsupported-operation handling.

### Observable Contract (OC)

An OC states externally verifiable obligations, including required and forbidden outcomes and, where relevant, ordering, state, failures and acknowledgments. It is **distinct** from the algorithm or product-specific implementation.

The sample `BehaviorContract.required_effects` and `forbidden_effects` are **text descriptions**, not yet executable assertions. Proposed test cases have no execution evidence. Turning them into a typed, machine-verifiable contract is a separate specification task.

**Unresolved:** assertion language and scope of observations, oracle/test fixture format, tolerance for legitimate nondeterminism, recovery/error obligations, and what constitutes complete E2E completion.

## 5. Evidence and claim levels

Document status is **self-reported metadata**. A JSON Schema validator can check its type; it cannot establish its truth.

The following remain separate:

1. **JSON syntactic validity** — file parses as JSON.
2. **Structural validity** — shape passes this exploratory JSON Schema.
3. **Semantic completeness** — every required function/effect is described in a portable form; **not demonstrated**.
4. **Implementation capability** — a target engine can realize all required obligations or reports explicit gaps; **not demonstrated**.
5. **Functional conformance** — independent tests show the actual outcomes meet the OC; **not demonstrated** for either sample.
6. **Comparative benchmarking** — only of implementations with demonstrated conformance, measuring the **complete** end-to-end result; not performed.

**Rule under discussion:** an implementation must never silently omit required behaviors because an operation or dependency is unsupported. Missing or unverified behavior must remain visible. The exact compatibility-state model remains to be specified.

## 6. Security and privacy

Infrastructure endpoints, secrets, real organization names, confidential rules, patient data and financial documents must not enter public review examples. Private bindings remain separate. `PRIVATE:...` placeholders are a convention *observed in these samples*, not a finalized PIIS binding syntax.

A JSON Schema **cannot guarantee absence of secrets or institutional intellectual property**. Publication needs separate scrutiny, even for apparently anonymized rules.

## 7. Explicitly deferred questions

- Canonical naming: current `Identity`/`BehaviorContract` casing vs lowerCamelCase.
- Canonical test collection: `cases` vs `scenarios`.
- Representing trigger types (message input, scheduled polls, others) without adopting any engine's execution model.
- Portable decision/expression semantics, including fallback priority, failure conditions and data type handling.
- Atomic versus multiple observable effects, and dependency/capability declaration.
- Typed OC assertions vs current prose fields.
- Reliable error and recovery specifications; correlation, retries, idempotency and message acknowledgment.
- Private binding syntax and mandatory failure for unresolved bindings.
- Conformance profiles and required independent evidence.
- Relationship with existing modeling/workflow standards; reuse or profile them where sufficient.

See [Review Questions](OPEN_QUESTIONS.md). No decision is approved by publication of this proposal.

## 8. Acceptance criteria for a subsequent proposal

Before adopting a canonical 0.2 representation, reviewers should be able to:

- Represent **both** current case studies without dropping a known source-derived requirement, even if currently marked unresolved/private.
- Explain the semantics of every mandatory field unambiguously.
- Give a counterexample for at least one real-world integration interface the proposed model cannot represent.
- Separate structurally valid instances from semantically incomplete instances.
- Derive a runnable OC scenario without asserting success before tests execute.
- Trace every proposed extension to an explicit gap in prior art.

**Decision point:** if an existing public specification already covers a need, document it and prefer reuse over inventing a parallel language.

## References

- [PIIS Working Draft 02 (English)](../../drafts/PIIS_Working_Draft_02_EN.md)
- [Original Spanish Working Draft 02](../../drafts/PIIS_Working_Draft_02.md)
- [First sample](../../samples/clinical-dft-draft01/README.md)
- [Second sample](../../samples/tax-documents-draft01/README.md)
- [Prior-art assessment](../../research/PRIOR_ART_AND_GAP_ASSESSMENT_01.md)
- JSON Schema Core 2020-12: https://json-schema.org/draft/2020-12/json-schema-core
- JSON Schema Validation 2020-12: https://json-schema.org/draft/2020-12/json-schema-validation
