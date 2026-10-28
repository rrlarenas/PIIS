# PIIS — Portable Integration Interface Specification

**Working Draft 02 — Technical Discussion Document**  
**Date:** October 28, 2026  
**Status:** Exploratory proposal; neither a published RFC nor a registered Internet-Draft  
**Working language:** Spanish (original reference text); English (complete translation)  
**Name and acronym:** Provisional  
**Changes since Draft 01:** Strict neutrality regarding products and implementation languages; primacy of the complete end-to-end result; measurement of CPU, RAM, throughput, recovery and cost across the entire solution; no exclusion of architectural advantages or penalties; transparent competition conditions; explicit motivation in users' freedom of choice and differentiation through results; consolidated vision of contract- and conformance-based plug-and-play migration.

*Translation notice: This document is the full English translation of [PIIS Working Draft 02 (Spanish)](PIIS_Working_Draft_02.md). The Spanish text is the original reference during this review stage. If a translation discrepancy is detected, it should be discussed and corrected in an open revision.*

## Abstract

This document proposes an open, vendor-independent framework for defining integration interfaces through a portable functional representation and an observable-behavior contract. Its purpose is to enable different integration engines, buses, or platforms to interpret a common definition and realize it using their own technologies, languages and architectures while preserving the functionality, outcomes and effects required by that contract.

The proposal includes explicit capability recognition, conformance assessment, migration of existing interfaces, and an independent mechanism for comparing implementations that meet the same contract. The primary measure of operational experience is complete end-to-end time, from the agreed input stimulus to confirmation of all required outcomes and effects. Conforming throughput, CPU, RAM, scalability, recovery, functional integrity, costs and migration effort are also measured. Architectural differences are not deviations to be subtracted: they are measurable advantages or disadvantages. The strategic objective is to reduce vendor dependence, return control over functional definitions to organizations, and foster transparent competition in which providers demonstrate their advantages through outcomes, with an evolving vision of plug-and-play migration. The specification does not modify, replace or extend existing standards for communication, messaging, data or transport.

## 1. Status and Normative Language

This draft is a **technical proposal for review** and claims neither recognition nor the status of an approved standard. The terms **MUST**, **MUST NOT**, **SHOULD** and **MAY** are used as proposed normative language in the sense of BCP 14 (RFC 2119 and RFC 8174), to identify requirements subject to discussion. Their presence does not imply adoption by a standards-development organization.

No submission body (IETF, OASIS, OMG or another open forum) has been selected. If IETF is selected, an **Internet-Draft** will have to be prepared and submitted under its requirements, without calling this draft an RFC.

## 2. Motivation and Problem Statement

Existing integration systems can exchange information using established standards and protocols. Nevertheless, the functional logic of interfaces often remains tied to the concepts, languages, components and configuration models of the engine on which it was developed.

Migrating a solution to another platform may require rebuilding transformations, decisions, queries, rules, orchestration, exception handling and specialized code even when inputs, destinations and the expected functional behavior remain unchanged.

**Core problem:** there is no universally adopted, sufficiently expressive, portable and verifiable functional definition contract across the engines under consideration that preserves the function of an interface independently of its implementation.

This observation is the **motivating hypothesis** behind PIIS. It must be assessed against existing formal work before asserting a new standards gap.

### 2.1. Proponent's Note: Freedom of Choice and Demonstrable Competition (Informative)

This proposal arises from more than twenty years of professional experience in integration and interoperability. During this time, architectures and platform capabilities have evolved, yet a barrier has persisted: changing engines can require rebuilding interfaces whose functionality remains necessary and valid.

PIIS seeks to challenge that dependence **without requiring disclosure of algorithms, internal architectures, code or trade secrets**. Each provider should retain full freedom to innovate, optimize and add capabilities. What is proposed is the ability to **demonstrate those advantages** through common functional contracts, verifiable conformance and measurable outcomes.

An illustrative analogy is an audio file in a public format such as MP3: different compatible players may offer additional features, performance and experiences without requiring the user to rebuild a media library merely to change players. The analogy is deliberately limited: an integration interface may include state, transformations, external effects and dependencies that do not arise when playing a file. PIIS must explicitly address that complexity rather than assume technical equivalence.

The strategic criterion is that an organization **choose a solution for what it demonstrably delivers**, not because the cost of leaving an existing implementation makes alternatives impossible to evaluate. Additional features may be legitimate reasons for choosing a solution; they must not become hidden functional dependencies behind a declaration of complete portability.

> **Innovation should be a reason to choose a technology, never a reason to become locked into it.**

This note explains the proposal's motivation. It creates no normative requirements and predetermines no conclusions about the performance of any implementation.

## 3. Objectives

PIIS aims to:

1. Represent interface functionality without requiring internal artifacts from a particular vendor.
2. Enable different engines to interpret the same definition and implement it natively.
3. Preserve the behavior, results and observable effects required by a common contract.
4. Explicitly detect any operation or dependency that cannot be interpreted or implemented with demonstrable equivalence.
5. Facilitate extraction and migration of existing interfaces without promising automation for arbitrary proprietary logic.
6. Establish reproducible conformance tests separate from performance benchmarks.
7. Enable objective comparison of solutions meeting the same functional contract without restricting their internal implementation mechanisms.
8. Establish a reproducible methodology centered on complete end-to-end time and complemented by conforming throughput, CPU, RAM, scalability, recovery, functional integrity, costs and migration effort.
9. Reduce barriers to changing vendors and support transparent decisions based on verifiable results, without prescribing an implementation or guaranteeing a particular market outcome by decree.
10. Maintain a long-term vision of near **plug-and-play** migration between fully conforming implementations, subject to explicit deployment conditions and dependencies.
11. Provide interface owners with portable definition, assessment and verification tools to select or replace an implementation on the basis of technical evidence, rather than remain bound exclusively by inherited migration costs.
12. Allow the additional capabilities of each implementation to contribute to differentiation, without confusing proprietary extensions with portable-core requirements or hiding their impact on migration.

## 4. Non-Goals and Boundaries

PIIS does **not** intend to:

- Define, modify, extend, reinterpret or replace HL7, FHIR, DICOM, X12, ACK, TCP/IP, HTTP, MQTT, MLLP, SOAP, REST or other established standards, formats or protocols.
- Build another ESB, universal runtime, messaging bus or integration product.
- Require any particular programming language, library, deployment architecture, internal implementation pattern or algorithm.
- Require identical internal traces, proprietary components, instrumentation or performance across different engines.
- Guarantee automatic translation of arbitrary existing code without a portable semantic representation or equivalent implementation.
- Standardize credentials, physical addresses, infrastructure or operational parameters specific to a deployment.

Existing protocols and standards are **assumed external dependencies** and are outside PIIS's normative scope.

## 5. Design Principles

### 5.1. Implementation Freedom

Two conforming engines **MAY** use entirely different components, languages, algorithms, architectures and internal execution sequences.

### 5.2. Observable Equivalence

Conformance is evaluated against a common functional contract, not against identical implementation. Two executions are functionally equivalent when they meet the same observable obligations and permitted contractual variations under equivalent conditions.

### 5.3. Portability Without Silent Loss

An interpreter or adapter **MUST NOT** silently omit, degrade or modify a mandatory contractual function. It must report an incompatibility or unproven equivalence before declaring complete portability.

### 5.4. One Interface as the Portable Unit

The smallest unit is a functionally identifiable interface. The specification will support references across interfaces and contract composition without initially requiring representation of an engine's entire production environment.

### 5.5. Minimal Overspecification

PIIS prescribes observable conditions and the semantics of its own definition elements. It **MUST NOT** prescribe internal order, state, timing or algorithms where those aspects do not affect the contract.

### 5.6. Transparency and Competitive Neutrality

The evaluation methodology **MUST** allow multiple technologies to implement the same contract with design freedom and to be compared under published, reproducible conditions. No performance measure shall inherently be a PIIS conformance criterion unless the functional contract imposes an observable deadline.

### 5.7. Primacy of the End-to-End Result

End-to-end time **MUST** measure the complete duration of the committed observable behavior, including queues, waits, retransmissions, persistence, decisions and external accesses involved in the evaluated solution. Measurement **MUST NOT** stop at internal acceptance or exclude architecture-related costs to artificially improve results.

The requirement is **equivalence of the contract and external test conditions**, not equivalent architecture. Legitimate optimizations **MAY** improve the measured outcome as long as they honor the contract and common evaluation-profile restrictions. Internal metrics **MAY** be used for diagnosis, but **MUST NOT** replace or favorably adjust the observed end-to-end result.

### 5.8. Interchangeability as an Evolutionary Goal

PIIS seeks to enable the transfer of an interface's functional definition to another conforming engine without rewriting its business semantics. Future plug-and-play operation also requires capability coverage, explicit configuration of dependencies, security, resources and deployment. Automatic equivalence of arbitrary proprietary code is not assumed.

### 5.9. Freedom of Choice and Demonstrable Differentiation

PIIS **MUST NOT** require implementations to offer identical extra capabilities, administration experiences or operational characteristics. The standard defines a portable core and allows differentiation through complementary functions, efficiency, reliability, scalability and other measurable outcomes.

When an extra capability becomes necessary to meet a particular interface's functional contract, that dependency **MUST** be declared and its portability **MUST** be explicitly evaluated. A non-portable extension **MUST NOT** be represented as part of a conforming migration without adaptation.

Ease of importing a definition and reduced work to realize it in another implementation must be measured outcomes, not assumed marketing claims.

## 6. Terminology

- **Interface:** a logical unit receiving one or more stimuli and producing results and/or effects toward one or more destinations according to defined rules.
- **Portable Functional Definition (PFD):** a vendor-independent representation of the operations, conditions, dependencies and composition needed to materialize an interface's behavior.
- **Observable Contract (OC):** verifiable obligations concerning accepted inputs, preconditions, outcomes, external effects, failures and permitted variations.
- **Implementation:** realization of a PFD by a specific engine.
- **Adapter:** component interpreting or transforming a PFD into an engine's native mechanisms; not every platform needs a separate translator.
- **Capability:** a PIIS operation or semantic behavior that an implementation can satisfy.
- **Conformance:** evidence that an implementation meets the complete contract for a defined scope of inputs, dependencies and conditions.
- **External Dependency:** a system, service, database, resource or function whose behavior is not governed by PIIS.
- **Observable Trace:** a partial or complete sequence of externally visible actions and effects relevant to the contract.

## 7. Conceptual Architecture

PIIS proposes separating four concepts without imposing a physical architecture:

1. **Portable functional definition:** what operations and rules make up the interface and how they are logically connected.
2. **Observable-behavior contract:** what the interface requires for particular inputs and conditions, including outcomes, effects and failures.
3. **Native interpretation:** how an engine transforms or executes the definition using its own capabilities.
4. **Independent verification:** how conformance is demonstrated and incompatibilities are identified.

The functional definition **cannot be reduced** to a list of example inputs and outputs. It must contain enough information to interpret the declared functions. The observable contract verifies the result of that interpretation, but cannot by itself reconstruct arbitrary logic.

## 8. Minimum Conceptual Model

A PFD may contain the following elements. Their names are provisional and **do not yet imply normative syntax**:

| Element | Responsibility |
|---|---|
| Identity | Identity, version and interface references. |
| Source | Logical sources, input conditions and external bindings. |
| Destination | Logical destinations and required effects. |
| Channel | Logical flow or exchange relationships between elements. |
| Operation | Declared portable functions with identifiable semantics. |
| Flow | Dependencies, branching, composition and conditions between operations. |
| Rule | Validations, predicates and functional decisions. |
| Transformation | Construction or modification of data according to defined rules. |
| Function | Specialized logic with a contract and either a portable representation mechanism or a declared dependency. |
| Dependency | Required external systems and data, including relevant assumptions. |
| BehaviorContract | Observable obligations and permitted variations. |
| ConformanceCases | Cases and reproducible evidence for verification. |

Duplicated concepts will be avoided when the same behavior can be expressed using fewer elements. Multiple sources and destinations, branches, concurrency and state will be supported when justified by real cases.

### 8.1. Initial Functional Vocabulary — Not Closed

The candidate catalog includes receive, emit, parse, validate, transform, enrich, query, invoke, filter, route, split, aggregate, correlate, wait and handle exceptions. These are **candidate semantic primitives**, not an approved list. Research will determine which are necessary and which can be composed from others.

### 8.2. Connectors and Protocols

A source or destination may identify an external type (TCP, file, database, queue, MQTT, HTTP, etc.) and reference its pre-existing contract. PIIS models only the interface's **functional relationship** with that resource; it does not define the protocol's technical specification.

## 9. Observable-Behavior Contract

A contract may declare, where applicable:

- **Inputs:** types, acceptance conditions and functional preconditions.
- **Outcomes:** required outputs and constraints on their content.
- **External effects:** observable writes, publications, invocations or modifications.
- **Decisions:** conditions determining destinations or possible outcomes.
- **Failures:** required effects and outcomes for errors within the contract's assumptions.
- **State:** persistent changes or dependencies across invocations when functionally meaningful.
- **Ordering and timing:** only the observable constraints expressly required by the contract.
- **Permitted variation:** valid differences, tolerances or nondeterministic values that do not constitute nonconformance.
- **Forbidden effects:** actions that must not occur under the declared conditions.

Equivalence **does not require byte-for-byte equality** if the contract permits different representations. Conversely, exact equality must be required where it is an explicit obligation.

Evaluation must distinguish implementation differences from functional nonconformance. The standard does not redefine external ACK, transaction or transport rules; it only allows reference to obligations relevant to the interface.

## 10. Representation and Interchange

The proposal is to use:

- **JSON** as PIIS's canonical interchange format.
- **YAML** as an optional authoring format that can be normalized to the defined JSON model without semantic loss.
- **JSON Schema** to validate structural representation without confusing schema validation with functional conformance.
- Explicit versioning and rules for extensions.

Rules governing types, references, ordering, identifiers and extensions will be specified in a future schema version. The use of RFC 8785 will be considered if canonical JSON serialization is required for cryptographic hashes, signatures or unambiguous artifact comparison.

**Proposed rule:** unknown fields that affect required functionality **MUST NOT** be silently ignored. Handling of purely informative extensions may differ and must be specified.

## 11. Custom Functions and Code

Custom logic is a fundamental portability challenge, but does not justify imposing a particular programming language.

PIIS will distinguish:

1. **Functionality expressible through portable primitives:** this may be interpreted through different native mechanisms.
2. **Functionality represented by an additional portable mechanism:** its semantics, execution and effects must be specified before a claim of conformance is permitted.
3. **Unrepresented proprietary dependency:** this must be explicitly identified and cannot support a full portability certification while unresolved.

A function's input/output contract alone is insufficient to automatically generate a semantically equivalent implementation. Automatic migration requires an interpretable representation of the logic, a supplied compatible implementation, or explicitly declared adaptation.

This document **does not yet choose** a DSL, expression language, bytecode or execution environment for custom cases. That decision requires separate research.

## 12. Capabilities and Compatibility

An engine **MAY** declare a catalog of supported capabilities, versions and restrictions. Assessment of a particular PFD must check the capability set actually required by the interface.

The distinctions are:

- **Supported:** the requirement can demonstrably be interpreted and realized.
- **Unsupported:** the requirement cannot be met.
- **Unverified:** evidence is insufficient to assert equivalence.

Partial compatibility provides useful diagnostic information but **is not equivalent** to conformance with the complete contract.

## 13. Conformance

A declaration of conformance for a specific interface and engine must include at least:

1. **Representation validation:** the artifact is structurally valid.
2. **Semantic coverage:** every mandatory function has an implementable interpretation; relevant extensions and dependencies are known.
3. **Behavioral assessment:** outcomes and effects satisfy the contract under reproducible test conditions.
4. **Evidence and scope:** contract version, engine, adapter where applicable, environment, tests, results and limitations.

Opening a file, importing a route or passing a small set of examples is not sufficient to declare universal conformance.

Tests must cover positive cases, boundary cases, failures, concurrency, state and external effects as appropriate. No finite set of cases is claimed to prove equivalence for arbitrary programs. Guarantees must be limited by defined semantics, assumptions and available evidence.

### 13.1. Result States

- **Conformant:** satisfies all obligations within the declared contract and conformance scope, with adequate evidence under the agreed methodology.
- **Non-conformant:** a breach of the contract has been observed.
- **Not demonstrated:** sufficient evidence is unavailable or mandatory functional dependencies remain unresolved.

No result state may be used to represent as conformant an interface that has lost a mandatory function.

## 14. Independent, Outcome-Driven Comparative Evaluation

### 14.1. Principle: Compete on Outcomes, Not Architecture

After conformance to the same contract has been demonstrated, PIIS enables direct comparison across independent implementations. Internal implementation is entirely at the discretion of each engine. The standard **MUST NOT** demand identical algorithms, components, processing patterns or topologies for a valid evaluation.

The **primary operational metric** is **end-to-end (E2E) completion time** for one conforming functional unit of work. It is measured from a defined input stimulus at the shared observable boundary to external confirmation of **all** effects and outcomes required by the contract. An operation is not complete merely because a component received it, queued it or marked it as internally accepted.

Measured time **includes** everything the solution needs to fulfill its function: reception, waiting, queueing, parsing, validation, transformation, routing, writes, invocations, retries and acknowledgments, when part of the behavior under evaluation. None of these times **MAY** be subtracted merely because they arise from a particular architecture. If one implementation completes the same work sooner than another under equal external conditions and functional guarantees, it has demonstrated an objective advantage **in E2E time for that scenario**.

External dependencies must provide **comparable conditions**, not disappear from the measured path. Controlled test services, reproducible responses or equivalent real environments may be used; the chosen method **MUST** be declared. Timing differences caused by an implementation's interactions with those dependencies are part of the total outcome. Internal processing and external service timings **MAY** be recorded for diagnosis without changing the observed E2E figure.

A comparison may identify different advantages depending on the metric; PIIS **MUST NOT** proclaim a universal winner based on a single test. No general speed minima are imposed as conformance requirements unless the functional contract specifies observable time limits.

### 14.2. Reference Metrics

The following catalog is a **proposed initial profile**. Statistical details and procedures will be specified in later test specifications.

| Proposed identifier | Metric | What it measures | Minimum report |
|---|---|---|---|
| `e2e_completion_time` | **End-to-end time (primary)** | Total duration of the complete functional result, from common input to confirmation of the last mandatory effect | ms; P50, P95 and P99; counts of complete and incomplete operations |
| `conformant_throughput` | **Conforming throughput** | Operations per second that fully satisfy the contract | ops/s, sustained window, workload and success percentage |
| `cpu_consumption` | **CPU consumption** | Processing resources used by the entire evaluated solution | Average/peak CPU, available cores and CPU-ms per conforming operation |
| `memory_consumption` | **RAM consumption** | Memory used by all components necessary for the evaluated operation | MB or GB; steady-state and peak memory |
| `scalability` | **Scalability** | E2E, throughput and resource behavior as load or concurrency changes | Curves by load level and observed limits |
| `recovery_time` | **Recovery** | Time from controlled failure until required functional effects are restored | Seconds; pending, lost and duplicate work |
| `functional_integrity` | **Functional integrity** | Correct and incorrect results, losses, duplicates and prohibited effects | Counts, rates and failure classification |
| `operational_cost` | **Operational cost** | Cost of executing a conforming volume of work under a declared scenario | Cost per period and conforming operation; assumptions |
| `migration_effort` | **Migration effort** | Intervention required to materialize and validate an existing definition on another implementation | Person-hours, manual and automated tasks, blockers |
| `internal_diagnostics` | Internal diagnostics (optional) | Partial timings, waits and other explanatory measures | Breakdown and method, **without subtracting from E2E** |

**Accounting rules:**

1. The report **MUST** identify the starting instant, completion criterion and set of contractual mandatory effects for each class of operation.
2. E2E time **MUST** encompass the complete functional path under common test conditions; no queueing delay or internal waiting may be excluded on architectural grounds.
3. An incomplete, timed-out or non-conforming operation **MUST NOT** count as a success or disappear from the result set. It must be reported separately, with statistical treatment specified to prevent bias from excluding slow operations.
4. Throughput **MUST** count only completed conforming operations; accepting an input is not functional completion.
5. CPU and RAM **MUST** cover the full set of components needed to satisfy the contract. Measurement boundaries and resource aggregation **MUST** be disclosed.
6. Cost **MUST** be related to conforming work and disclose assumptions about infrastructure, operations, licensing, consumption and time horizon. It is not a measure of conformance.
7. Internal diagnostic metrics **MAY** explain causes but **MUST NOT** justify an E2E classification different from the one actually measured.

### 14.3. Conditions for Comparability

The necessary condition of equality is not that engines have similar designs. It is that they be required to deliver **the same functional outcome under equivalent external constraints and workloads**.

Any comparison presented as PIIS-qualified **MUST** identify and publish:

1. Identity, version and verifiable fingerprint of the functional contract and portable definition evaluated.
2. Version of each implementation and any components needed to realize the contract, without privileging any architecture.
3. Inputs, sizes, case distribution, initial states, arrival rates, bursts, concurrency and test duration.
4. Reproducible external conditions: test systems, network, storage, limits, responses, induced failures and service timings.
5. Common functional guarantees: persistence, security, confirmation, audit records and other contractual obligations.
6. Comparison mode: **equal resource budget**, **equal economic budget**, or both, reported separately.
7. Resources and topology actually used, including required supporting capabilities; enabled optimizations and their conditions.
8. Instrumentation of process start and completion, preferably independent of the tested implementation, and treatment of failures and incomplete samples.
9. Raw data, aggregated results, statistical methods, variability, repetitions, warm-up conditions and limitations.

Each implementation **MAY** choose its architecture, tune its mechanisms and exploit its optimizations. An optimization that breaches the contract, weakens required guarantees or transfers hidden work outside the disclosed measurement boundary **MUST** invalidate the comparison as evidence of functionally equivalent solutions. Genuine performance or consumption benefits **MUST NOT** be removed through normalizations designed to neutralize technological differences.

### 14.4. Minimum Experimental Profiles

Product-independent scenarios are proposed:

1. **Prequalification:** complete functional verification of the contract and its effects.
2. **Baseline:** sustained low load with external E2E instrumentation.
3. **Sustained operation:** representative distribution of transactions, sizes and concurrency.
4. **Bursts:** sudden increases in load and queue evolution until draining.
5. **Scalability:** gradual changes in workload and/or resource budget, reporting E2E and conforming operations.
6. **Failure and recovery:** controlled interruptions, restart, retries and confirmation of pending outcomes, according to the contract.
7. **Practical portability:** realization of the same definition in an alternative implementation and measurement of required human effort.

Profiles **MUST** compare the same obligations and restrictions. Numerical values for sizes, durations and loads must be agreed and published before a benchmark is executed, not adjusted retrospectively to favor a result.

### 14.5. Reporting for Adoption and Migration Decisions

A published assessment **SHOULD** provide a machine-readable artifact and an understandable summary for those responsible for purchasing, maintaining or migrating integration systems. Without relying on marketing inferences, the report should answer:

- Can this implementation satisfy **the entire** functional contract?
- How long does each complete outcome take end to end?
- How many conforming operations can it sustain, and at what CPU/RAM consumption?
- How does it behave under load, bursts and failures?
- What is its cost per conforming functional result?
- How much actual work is needed to migrate the definition?

A comparison may illustrate tradeoffs among performance, resources, cost and recoverability. It **must not** hide architectural differences or treat as equivalent a solution that sacrificed required functional obligations. The expected market benefit — reduced dependence, improved transparency and competitive pressure to improve — is an **impact hypothesis to be measured**, not a guarantee of adoption.

### 14.6. Independence and Auditability

A declaration of conformance or benchmark report **MUST** rely on reproducible evidence; a commercial claim alone is insufficient. Institutional affiliation, sponsorship or fees for testing **MUST NOT** change the technical evaluation criteria. When sensitive data prevents publication of original samples, representative synthetic material, aggregated results and auditable procedures **SHOULD** be provided. An open package of contracts, test cases, load generators and a common report format is proposed.

## 15. Portability of Existing Interfaces

The migration objective requires considering the following conceptual process:

1. Inspect the existing implementation and its dependencies.
2. Extract or reconstruct its portable functional definition.
3. Identify unrepresented operations, effects and assumptions.
4. Compare the definition with the destination engine's capabilities.
5. Realize the target implementation using native mechanisms.
6. Run conformance tests and declare results, limitations and differences.

Automatic extraction from existing products is a desirable ecosystem-tool capability; it is not assumed that every engine can currently export its semantics completely.

## 16. Security Considerations

A portable PFD must not carry operational secrets as part of its functional definition. Credentials, authorization, local policies and site-specific addresses should be resolved through deployment bindings, while explicitly preserving the required permissions and effects.

Malicious inputs, untrusted external dependencies, excessive privileges, data leakage in test cases, custom code and accidental effects during migration and benchmarking must be considered. Conformance tests should be executable in controlled environments so that production systems are not unintentionally modified.

## 17. Prior Work and Position Relative to the State of the Art

Prior work must not be assumed insufficient by definition; it must be formally assessed before any claim of novelty:

| Initiative | Relevant contribution | Question for PIIS |
|---|---|---|
| WfMC XPDL | Exchange of process models and preservation of tool extensions | What executable functional semantics can actually be exchanged? |
| OMG BPMN 2.0.2 | Modeling and execution semantics; different conformance classes | How can nominal conformance without functional portability be avoided? |
| OMG Model Driven Architecture (MDA) | PIM/PSM separation, platform-independent functionality and specific realization | What does PIIS add for concrete ESB interfaces, observable equivalence and measured migration? |
| OASIS WS-BPEL 2.0 | Executable processes with defined semantics | What does it cover, and what is limited by its historical orientation toward web services? |
| OASIS SCA | Component composition and separation of implementations | Which parts of an assembly are portable between concrete ESB platforms? |
| Publicly documented integration patterns | Taxonomy of recurring integration functions | Which concepts can be formalized as verifiable semantic primitives without defining another platform? |
| CNCF Open Workflow Specification | Neutral DSL, runtimes and Conformance Test Kit | How far does its contractual behavior for interfaces extend, and what can be adopted directly? |
| AsyncAPI | Contracts for asynchronous operations and channels | Which descriptions can be referenced without duplication? |

**Academic evidence:** studies of BPMN conformance have identified partial support and differences between engines. These findings support the need to evaluate actual execution rather than merely the ability to read a format. They are historical results and do not automatically characterize today's market.

## 18. Proposed Initial Validation

The proof of concept will use a **real interface** with an origin, validation, transformation, external enrichment, routing decision, two destinations, exception handling and at least one custom function.

Deliverables:

1. Complete inventory of behavior and observable effects of the original interface.
2. Initial vendor-independent PFD.
3. Conformance contract and reproducible cases.
4. Native implementations in at least two different engines.
5. Conformance report for both implementations.
6. Comparative end-to-end and resource benchmark **only if both pass the required conformance assessment**.
7. Record of non-portable elements, causes and design decisions.

**Success criterion:** both implementations satisfy the same observable functional contract without sharing code or internal technology. The manual effort needed to realize the second implementation must be measured separately, because the **actual reduction in migration effort** is also a hypothesis to be demonstrated. The trial will produce the complete Section 14 report, prioritizing E2E outcomes without excluding delays originating within the solution. Speed and cost will be evaluated separately from functional conformance unless an observable deadline forms part of the contract.

