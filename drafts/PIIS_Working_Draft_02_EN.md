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

