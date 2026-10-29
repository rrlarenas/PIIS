# PIIS — Portable Integration Interface Specification

**Working Draft 02 | Public technical review | 28 October 2026**

**Author and original proponent:** Rodrigo Larenas  
**License:** [Creative Commons Attribution 4.0 International](LICENSE.md) (CC BY 4.0)  
**Status:** Exploratory proposal. **Not an approved standard, IETF Internet-Draft, or published RFC.**

> **Innovation should be a reason to choose a technology, never a reason to become locked into it.**

## Read PIIS

| Resource | Language | Status |
| --- | --- | --- |
| [Complete Working Draft 02](drafts/PIIS_Working_Draft_02.md) | Spanish | Original reference text |
| [Complete Working Draft 02 — English](drafts/PIIS_Working_Draft_02_EN.md) | English | Full translation for international review |
| [English overview](docs/OVERVIEW_EN.md) | English | Informative short summary |
| [Conformance and benchmark notes](docs/CONFORMANCE_AND_BENCHMARKS.md) | English | Preliminary methodology |
| [Sample 01 — Anonymized clinical DFT interface](samples/clinical-dft-draft01/README.md) | English / Spanish | **Exploratory PFD; not executable or conformance-tested** |
| [Sample 02 — Anonymized financial-document integration](samples/tax-documents-draft01/README.md) | English / Spanish | **Exploratory JSON PFD; conformance not demonstrated** |
| [Research and prior work](docs/PRIOR_WORK.md) | English | Comparison agenda |
| [Contributing](CONTRIBUTING.md) | English | Review and contribution rules |
| [Citation metadata](CITATION.cff) | English | Attribution and release metadata |

The Spanish draft is the original reference; the English text is a translation for international technical review. No alternative text supersedes the original unless explicitly accepted in a subsequent public revision.

## Open international technical review

**The Working Draft 02 is archived and unchanged.** New research is recorded separately so objections and proposed revisions remain traceable.

- **[Prior Art and Gap Assessment 01](research/PRIOR_ART_AND_GAP_ASSESSMENT_01.md)** — requirement-by-requirement comparison with earlier standards, explicit unknowns, and falsifiable experiments.
- **[Review #1: Prior art and possible duplication](https://github.com/rrlarenas/PIIS/issues/1)** — challenge the novelty claim; reuse or extend existing standards where possible.
- **[Review #2: Minimal portable functional model](https://github.com/rrlarenas/PIIS/issues/2)** — define sufficient functional semantics and observable contracts without prescribing internal execution.
- **[Review #3: Complete E2E comparison](https://github.com/rrlarenas/PIIS/issues/3)** — compare only conforming implementations, including all architecture-dependent time and resources.

**Review invitation:** Please cite an exact specification version and normative section, propose a reproducible counterexample, or share independent conformance evidence. Demonstrating that an existing standard already solves part or all of PIIS's problem is a valuable contribution.

## 1. Problem statement

Integration systems rely on well-established protocols and data standards. Nevertheless, interfaces often remain bound to an individual platform's internal configuration, programming model, components, and execution paradigm.

Migrating an interface can require rebuilding validation, transformations, rules, routing, lookups, stateful processing, error handling, and custom functions, even when its functional purpose and expected outcomes do not change.

**PIIS addresses portability of the interface's functional definition, not portability of its original code or the standardization of its communication protocols.**

## 2. The PIIS proposal

PIIS explores a **Portable Functional Definition (PFD)** describing an interface's operations, dependencies, relations and rules, together with an **Observable Contract (OC)** specifying externally verifiable behavior, outcomes, exceptions and side effects.

Independent integration engines may interpret the same portable definition using **completely different internal mechanisms**.

> **Different implementations. One functional contract. Verifiable outcomes.**

An interface must not be described only by a list of test inputs and outputs: the definition needs sufficient functional meaning to support independent realization. Tests and conformance evidence then assess whether the realization meets its obligations.

### Conceptual model

| Concern | PIIS responsibility |
| --- | --- |
| Source / Destination | Logical input and output relationships and required results |
| Channel / Flow | Composition, dependencies, branching, concurrency and observable ordering |
| Operation / Rule | Validations, conditions and functional decisions |
| Transformation | Required mappings and data modifications |
| Custom Function | Portable semantics where possible, otherwise explicit dependencies |
| External Dependency | Resources, constraints and assumptions material to the contract |
| Observable Contract | Inputs, preconditions, outcomes, side effects, failures and permitted variations |
| Conformance Evidence | Reproducible proof of declared functional compatibility |

These are provisional concepts, **not a finalized schema**.

## 3. Non-goals

PIIS **does not redefine, interpret, replace, extend or revise** established standards for communication, data structures, messaging, or transport. Specifications such as HL7, FHIR, DICOM, X12, TCP/IP, HTTP(S), MQTT and MLLP are taken as mature external standards, beyond PIIS's normative scope.

It also does not mandate:
- a particular integration engine, execution architecture, common runtime, algorithm, programming language or library;
- exposure of proprietary implementations, source code, commercial secrets or internal telemetry;
- identical internal behavior, steps, logs, execution paths, or identical performance;
- automatic migration of arbitrary custom code without a portable functional representation or explicitly declared adaptation.

JSON is a **proposed canonical interchange representation**; YAML is a potential readable authoring format. The choice of a format does not itself define semantics or ensure conformance.

## 4. Conformance is about observable outcomes

A conforming implementation must preserve the obligations of its declared contract, including required outcomes, visible state transitions, error behavior and side effects. It may use entirely different internal algorithms and processing architectures.

An importer or engine must **never silently discard mandatory functionality** while claiming full conformity.

Proposed outcomes for a scoped assessment:
- **Conformant:** contract obligations met and supported by adequate evidence.
- **Non-conformant:** a breach of the declared contract was observed.
- **Not demonstrated:** evidence or required semantic coverage is insufficient.

A finite test suite alone does not prove universal equivalence for arbitrary programs. Conformance claims must state their scope, assumptions, version and evidence.

## 5. Independent performance evaluation

The first obligation is functional equivalence; **performance comparison is a separate evaluation**.

Once implementations meet the same functional contract, customers should be able to compare solutions on measurable results using reproducible workloads and disclosed test conditions.

| Measure | Intended comparison |
| --- | --- |
| **Complete end-to-end time** | Elapsed time from defined input stimulus to completion of the *entire* contracted observable result |
| P50 / P95 / P99 | Distribution of contracted end-to-end completion times |
| Conforming throughput | Correct results completed per second |
| CPU and RAM | Resource use for the evaluated solution |
| Scalability | Behavior at increasing loads and concurrency |
| Recovery | Time to restore required behavior after failure |
| Functional integrity | Missing, duplicated or incorrect contractual effects |
| Operational cost | Cost of delivering the required behavior |
| Migration effort | Measured work to reproduce and verify a portable interface |

**Do not subtract internal queueing, persistence, scheduling or other architecture-driven overhead from the primary end-to-end measurement.** These are meaningful technology advantages or disadvantages. Fair comparison requires equivalent external conditions and declared resource budgets, not identical internal implementation.

A solution may outperform another for a specific workload without being universally superior.

## 6. Strategic goals

PIIS seeks to:
1. Return control of functional interface definitions to their owners.
2. Reduce functional vendor lock-in and inherited migration barriers.
3. Let implementers compete transparently on measured outcomes and differentiated capabilities.
4. Progress toward **plug-and-play-like migration** between fully conforming implementations, while explicitly recognizing necessary configuration, environment and unresolved custom logic.
5. Avoid a new vendor-specific or implementation-specific portability dialect.

Plug-and-play is a **long-term objective to be demonstrated**, not an existing PIIS capability.

## 7. Background and adjacent standards

PIIS begins with a critical review of prior work, especially WfMC/XPDL, WS-BPEL, BPMN, OASIS SCA, OMG Model Driven Architecture, CNCF Open Workflow Specification, and Enterprise Integration Patterns.

The independence-of-platform concept is not novel by itself. PIIS's proposed contribution requires a **demonstrable gap** in functional migration, observable conformance, and objective implementation evaluation. See [the prior-work research agenda](docs/PRIOR_WORK.md).

## 8. Roadmap

| Phase | Outcome |
| --- | --- |
| A — State of the art | Identify exactly what the existing standards do and do not cover |
| B — Functional semantics | Define minimal portable operations and observable contracts from real interfaces |
| C — Representation | Specify versioned JSON representation; evaluate YAML authoring |
| D — Conformance | Define evidence, capabilities, test profiles and compatibility states |
| E — Interoperability trial | Materialize one functional definition in two independent implementations |
| F — Comparative benchmark | Measure complete end-to-end outcomes and total migration effort |
| G — Open review and standards engagement | Invite critical external review; assess suitable standards-development organizations |

## 9. Participate

Open a [GitHub Issue](https://github.com/rrlarenas/PIIS/issues) to critique a definition, identify overlap with earlier work, propose an independently verifiable scenario, or challenge the core portability hypothesis. Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting text.

Constructive critical feedback is welcome. A concrete counterexample is more valuable than an unsupported endorsement.

## Working Draft 02 publication

**[PIIS Working Draft 02 — Public Review (ES/EN): official GitHub release](https://github.com/rrlarenas/PIIS/releases/tag/draft-02)**

This is a formally versioned *public working draft* release, **not** an adopted specification, IETF RFC, or certified implementation.

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23748842.svg)](https://doi.org/10.5281/zenodo.23748842)

**Zenodo DOI for Working Draft 02:** [10.5281/zenodo.23748842](https://doi.org/10.5281/zenodo.23748842).

## 10. Publication and attribution

**Rodrigo Larenas** — author and original proponent, 2026.

The original PIIS documentation and specification text in this repository are licensed under [CC BY 4.0](LICENSE.md). Future implementation source code, if any, may use a separate license.

- **Citation:** see [CITATION.cff](CITATION.cff).
- **Publication workflow:** [PUBLICATION_CHECKLIST.md](PUBLICATION_CHECKLIST.md).
- **Archival DOI for Working Draft 02:** [10.5281/zenodo.23748842](https://doi.org/10.5281/zenodo.23748842).

This independent proposal does not assert institutional endorsement or an official standardization status.
