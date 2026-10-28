# PIIS — Prior Art and Gap Assessment 01

**Status:** Open review / research memo (informative; **not** part of the immutable `draft-02` release)  
**Review date:** 28 October 2026  
**Project:** Portable Integration Interface Specification (PIIS)  
**Author of original proposal:** Rodrigo Larenas  
**License:** CC BY 4.0, consistent with the repository

## Executive assessment

PIIS must **not** claim to invent platform-independent functional models, portable process descriptions, executable workflow definitions, or conformance testing. All of these concepts have substantial prior art.

The most serious overlaps are **OMG Model Driven Architecture (MDA)** and **CNCF Open Workflow Specification**, followed by **WS-BPEL**, **BPMN**, **OASIS SCA**, and **WfMC XPDL**.

**Hypothesis to test, not an established gap:** a standardized *portable functional definition* of concrete integration interfaces, together with an *observable functional contract*, explicit handling of non-portable dependencies, an independent conformance assessment, and a reproducible *whole-outcome* end-to-end benchmark may still require domain-specific work. That work might be (a) a profile or extension of an existing specification, (b) a companion conformance/benchmark standard, or (c) an independent PIIS specification. The smallest defensible path should win.

This memo deliberately distinguishes **capabilities positively documented in original sources** from **capabilities not yet established by this review**. “Not established” does **not** mean “does not exist.”

## 1. PIIS requirements used for comparison

These requirements are distilled from [Working Draft 02](../drafts/PIIS_Working_Draft_02_EN.md); they are *proposed*, not normative adoption claims.

| ID | Required outcome | How to falsify PIIS's claimed gap |
| --- | --- | --- |
| R1 | Portable, interpretable definition of integration-interface behavior, including transformations, validation, routing, external calls and relevant state | Show a pre-existing specification with sufficient semantics for a real interface of this kind |
| R2 | Complete observable contract: permitted inputs, results, decisions, external effects, errors, timing/ordering only where relevant | Show existing portable contracts that represent and enforce these obligations without requiring identical internal implementation |
| R3 | Independent native realization across distinct integration engines; no prescribed internal architecture or algorithm | Show two truly independent realizations of one existing definition and contract |
| R4 | Explicit unsupported/unverified capability reporting; no silent loss of required functionality | Show existing capability/conformance rules meeting this criterion |
| R5 | Existing-interface migration path and measured *manual effort*, not merely sharing newly authored definitions | Show traceable real migrations that avoid reconstructing functional logic |
| R6 | Reproducible conformance evidence, including errors, state and side effects | Show a validated test suite and scope-specific conformance profiles covering the contract |
| R7 | Comparable complete end-to-end outcomes plus CPU, RAM, throughput, resilience, integrity, operational cost and migration effort | Show a specified benchmark method applied to contract-conformant implementations without eliminating architectural overhead |
| R8 | Existing transport/messaging/data standards remain untouched | Show a solution meeting the above without redefining the underlying external standards |

**Critical separation:** Passing functional conformance is a prerequisite for meaningful comparative benchmarking; the fastest nonconformant implementation is not a comparable functional alternative.

## 2. What the primary sources actually establish

### 2.1 OMG Model Driven Architecture (MDA) — **highest conceptual overlap**

**Evidence:** OMG describes a platform-independent model (PIM) of business functionality and behavior, platform-specific models (PSMs), transformations to implementations, and preservation of independence across middleware platforms.

Primary sources:
- https://www.omg.org/mda/faq_mda.htm
- https://www.omg.org/mda/
- https://www.omg.org/mda/specs.htm

**Strong overlap:** R1 and R3 at an *architectural/modeling approach* level; it is incorrect to attribute the idea of “define once, realize on many platforms” to PIIS.

**Not established by the review:** a specific, standardized, universally interpreted profile of operational integration-interface primitives; a mandatory interface-level observable contract addressing all external effects; a common complete-E2E performance and migration-effort comparison profile.

**Review challenge:** Determine whether an existing OMG domain model, model transformation or conformance specification already covers these details. If yes, PIIS should extend or apply it rather than compete with it.

### 2.2 CNCF Open Workflow Specification — **highest executable DSL/conformance overlap**

**Evidence:** Open Workflow describes a vendor-neutral workflow DSL and a Conformance Test Kit (CTK) using executable scenarios to test implementation behavior.

Primary sources:
- https://github.com/open-workflow-specification/specification/blob/main/README.md
- https://github.com/open-workflow-specification/specification/blob/main/dsl.md
- https://github.com/open-workflow-specification/specification/blob/main/ctk/README.md

**Strong overlap:** R1, R3 and R6 are at least partly addressed, and capability coverage must be examined in detail.

**Not established by the review:** cross-engine migration of *existing* integration interfaces (R5) or complete-outcome E2E comparison profiles of independently realized interfaces (R7). This is a statement about the reviewed documents, **not** a claim of absence throughout its ecosystem.

**Review challenge:** Build PIIS's first real interface **using the existing Open Workflow DSL and CTK** before authoring any competing PIIS DSL. Record only the elements whose semantics or conformance cannot be expressed or verified. Assess whether a *conformance profile + benchmark companion* is enough.

### 2.3 OASIS WS-BPEL 2.0 — **strong executable-process precedent**

**Evidence:** WS-BPEL defines executable and abstract business processes. It expressly uses Web Service interfaces and includes static analysis/conformance obligations; abstract processes can admit opaque details.

Primary sources:
- https://www.oasis-open.org/standards/
- https://docs.oasis-open.org/wsbpel/2.0/wsbpel-v2.0.html

**Strong overlap:** R1, R2 and R4 for process behavior within its domain. In particular, its handling of unsupported expression/query languages is relevant to avoiding silent functionality loss.

**Documented scope distinction:** the specification models partners and interactions using Web Service interfaces; this affects applicability to the full range of source/destination relationships PIIS aspires to cover.

**Review challenge:** Compare BPEL fault handling, state, orchestration, expressions, opaque activities and conformance tests against a representative PIIS interface. Do not dismiss BPEL because of its publication age.

### 2.4 OMG BPMN 2.0.2 — **execution/conformance precedent**

**Evidence:** BPMN has published normative execution and conformance material (not merely diagrams). Different conformance classes and executable subsets matter.

Primary sources:
- https://www.omg.org/spec/BPMN/
- https://www.omg.org/spec/BPMN/2.0.2/PDF

**Strong overlap:** R1/R2 at the process level and aspects of R6.

**Not established by the review:** portable, implementation-neutral expression of arbitrary concrete integration transformations and external effects together with the full PIIS benchmarking/migration scenario.

**Review challenge:** Identify exactly which subset and conformance class could support the proposed interface; avoid treating support for *a BPMN diagram* as evidence of complete executable conformance.

### 2.5 OASIS Service Component Architecture (SCA) — **assembly/binding precedent**

**Evidence:** SCA describes composite applications assembled from services, with components, references, bindings and a range of access technologies.

Primary sources:
- https://www.oasis-opencsa.org/sca.html
- https://docs.oasis-open.org/opencsa/sca-assembly/sca-assembly-spec-v1.1.html

**Strong overlap:** platform-neutral composition, logical dependencies, implementation/binding separation; portions of R1 and R3.

**Not established by the review:** full internal transformation/rule semantics and independent outcome-based migration benchmarks across integration engines.

**Review challenge:** Decide whether PIIS should merely define a conformance/behavior *profile* over an SCA composite instead of introducing separate Source/Channel/Destination abstractions.

### 2.6 WfMC XML Process Definition Language (XPDL) — **import/export precedent**

**Evidence:** WfMC describes XPDL as a common XML interchange format for process definitions across tools, including an accompanying process-definition meta-model.

Primary source:
- https://wfmc.org/public-documents/

**Strong overlap:** model import/export and tool-independent representation.

**Important distinction:** format interchange by itself is not proof of behavior-preserving execution across native integration engines. This is a **logical distinction**, not a claim that no XPDL ecosystem has addressed behavior.

**Review challenge:** Identify XPDL's executable semantics and extension processing rules, including vendor-specific information that could compromise practical portability.

### 2.7 Enterprise Integration Patterns (EIP) — **semantic vocabulary precedent**

**Evidence:** the published catalog provides technology-independent descriptions of routing, transformation, channel and messaging patterns.

Primary source:
- https://www.enterpriseintegrationpatterns.com/patterns/messaging/

**Strong overlap:** candidate PIIS primitive vocabulary; R1's naming and design intent.

**Key distinction:** a pattern catalog is not in itself an interchange syntax, executable specification or engine conformance test.

**Review challenge:** Derive the **smallest** necessary interoperable operations by composition before creating any new semantics. Cite the source and avoid copying protected explanations or diagrams.

### 2.8 IHE profiles / Connectathon — **conformance-process precedent, sector-specific**

**Evidence:** IHE supplies implementation profiles and structured supervised tests of interoperability between independently developed systems. This is important **methodological** prior art, not an equivalent definition of portable interfaces.

Primary sources:
- https://www.ihe.net/about_ihe/ihe_process/
- https://www.ihe.net/testing/connectathon/

**Strong overlap:** reproducible test organization, cross-implementation interoperability evidence, profiles and publication of results.

**Scope distinction:** testing established healthcare interoperability scenarios is not the same proposition as transferring the functional definition of an existing integration interface between native engines. The underlying healthcare standards remain outside PIIS's remit.

## 3. Evidence-status matrix (reviewed on 28 Oct 2026)

Legend: **D** = positively documented as relevant; **P** = documented partial/domain-specific overlap; **?** = not established from the reviewed primary material (more investigation required); **—** = contextual/methodological rather than a direct candidate. No symbol means “feature absent.”

| Prior work | R1 functional definition | R2 observable contract | R3 independent realization | R4 explicit capability mismatch | R5 existing migration effort | R6 conformance evidence | R7 complete E2E comparisons |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OMG MDA | D | P | D (model-to-platform) | ? | ? | ? | ? |
| Open Workflow | D | P | D (vendor-neutral target) | ? | ? | D (CTK) | ? |
| WS-BPEL 2.0 | D (service domain) | D (defined process behavior) | P | D (selected rejection rules) | ? | P | ? |
| BPMN 2.0.2 | D (process domain) | P | P | P | ? | D (conformance classes) | ? |
| OASIS SCA | P (assembly) | P (service contracts) | D (assembly model) | P | ? | P | ? |
| WfMC XPDL | P (process interchange) | ? | P | ? | P (definition exchange) | ? | ? |
| Enterprise Integration Patterns | P (vocabulary) | — | — | — | — | — | — |
| IHE | — | P (profile behavior) | P (interoperability testing) | P | — | D (structured tests) | — |

**Caution:** “D” does not mean the entire PIIS requirement is already met; it indicates material overlap documented by the cited source. Every entry requires a more detailed traceability study.

## 4. Preliminary conclusion (subject to falsification)

It is **not defensible** to say that no standard already separates business logic from implementation. It is **not defensible** to say that no portable workflow language or conformance kit exists.

The currently plausible contribution of PIIS may instead be a **domain-specific contract and evidence profile** spanning:

- the observable functional effects of concrete integration interfaces, including state and non-portable extensions;
- coverage and explicit incompatibility reporting for migration between independent implementations;
- real migration from an existing source implementation, with measured human effort;
- customer-facing comparisons based on *complete* contracted E2E outcomes, without adjusting away architecture-dependent cost.

**Decision rule:** if an existing standard and its ecosystem already satisfy R1–R8 with sufficiently small adaptation, PIIS should become a documented profile, an interoperability/conformance initiative, or a contribution to that project — **not** a redundant new general-purpose language.

## 5. Proposed falsifiable experiments

**E1 — Existing-language representation test.** Express one real nontrivial integration interface using Open Workflow *without introducing PIIS syntax*. Track unrepresentable or ambiguous semantics, and whether the standard itself or a tool limitation causes the gap.

**E2 — Cross-implementation test.** Produce two independent realizations of the same definition. Verify results, forbidden effects, errors, state and permitted nondeterminism, not internal execution order.

**E3 — Existing-interface migration test.** Begin with a functioning legacy interface; reconstruct/export its portable definition and adapt it into another realization. Report person-hours, unsupported capabilities and code manually recreated.

**E4 — End-to-end comparison test.** Under an equivalent workload and external conditions, measure input-to-*last-required-effect* E2E time, conforming throughput, CPU, RAM, recovery and cost. Do not subtract internal queues, waits or persistence overhead.

**E5 — Falsification challenge.** Invite citations to any extant public specification, conformance profile or toolchain that already achieves R1–R8 for the same interface; update the matrix or retire the redundant part of PIIS accordingly.

## 6. Discussion and review requirements

A reviewer challenging a gap claim should preferably provide:

1. The exact existing specification and **version**.
2. Normative section, implementation guide or test definition.
3. Which PIIS requirement (R1–R8) is already covered.
4. Whether coverage is defined by the standard or by one particular product.
5. Evidence from independent implementations when making portability claims.
6. A concrete counterexample that can be reproduced.

Evidence should take priority over prestige, affiliations or marketing claims.

## 7. Provenance and scope

This memo summarizes primary documentation and explicitly calls out unresolved interpretation. It is **not** a literature systematic review, a certification audit, a market survey, or proof that particular functionality is absent from any specification.

Do not modify the archived Working Draft 02 to retroactively add these findings. Accepted changes belong in subsequent draft work and traceable public review issues.

### Key primary-source index

- OMG MDA: https://www.omg.org/mda/faq_mda.htm
- Open Workflow specification: https://github.com/open-workflow-specification/specification/blob/main/README.md
- Open Workflow CTK: https://github.com/open-workflow-specification/specification/blob/main/ctk/README.md
- WS-BPEL: https://docs.oasis-open.org/wsbpel/2.0/wsbpel-v2.0.html
- BPMN: https://www.omg.org/spec/BPMN/
- SCA: https://docs.oasis-open.org/opencsa/sca-assembly/sca-assembly-spec-v1.1.html
- XPDL: https://wfmc.org/public-documents/
- EIP: https://www.enterpriseintegrationpatterns.com/patterns/messaging/
- IHE: https://www.ihe.net/testing/connectathon/
