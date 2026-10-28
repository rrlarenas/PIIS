# PIIS — Portable Integration Interface Specification

*Informative English overview of Working Draft 02; the full Spanish draft remains the working reference.*

## Problem

Integration interfaces are routinely implemented with product-specific building blocks and programming paradigms. Migrating an interface can require extensive redevelopment even though its communication protocols and data formats are well-established, mature standards.

## Proposal

PIIS aims to describe **what an integration interface does** independently of **how a particular engine implements it**. A portable interface definition should include the information required to reproduce its intended functional behavior; an observable contract should establish how conformance is determined.

Possible elements include origins, destinations, channels, analysis, validation, transformation, routing, dependencies, custom logic, error handling, externally visible state and side effects.

## Central rule

Implementations MAY differ in architecture, language, algorithms, components, and execution strategies. Conformance is about satisfying the **same declared observable functional contract**, not internal uniformity.

Existing communication, messaging, transport, and data standards are taken as established. PIIS does not alter them.

## Objective performance evaluation

Only after functional conformance is demonstrated should competing implementations be compared. The main outcome metric is **complete end-to-end time**, including queueing and other time spent delivering the contractual outcome. Throughput, CPU, RAM, latency distributions, scalability, resilience, total operational cost, and human migration effort are supporting metrics. Internal architectural differences must not be normalized away.

Equivalent external test conditions, workload and resource budgets should be disclosed. Internal implementation mechanisms need not be equal.

## Vision and limitations

The long-term aspiration is near plug-and-play migration of an interface based on a contract and a verifiable conformance profile. Custom logic that cannot be represented or reconstructed portably is an explicit limitation; conformance tests alone cannot prove equivalence of arbitrary programs.

## Project status

Working Draft 02, exploratory. Open discussion is welcome through repository issues. No platform, organization or manufacturer is implied to endorse PIIS.
