# PIIS — Portable Integration Interface Specification

**Working Draft 02 · Open Technical Discussion · 28 October 2026**

> Innovation should be a reason to choose a technology, never a reason to become locked into it.

PIIS proposes a portable functional definition for integration interfaces, allowing different implementations to preserve **the observable behavior, functional outcomes and external effects** specified by a common contract.

Implementations remain free to use their own algorithms, architectures and internal components. PIIS seeks to reduce vendor lock-in and enable transparent, outcome-based comparison of conforming integration engines.

## Read the specification

- [Complete Working Draft 02 (Spanish)](drafts/PIIS_Working_Draft_02.md)
- [English summary](docs/OVERVIEW_EN.md)
- [Conformance and evaluation](docs/CONFORMANCE_AND_BENCHMARKS.md)
- [Related work](docs/PRIOR_WORK.md)
- [How to contribute](CONTRIBUTING.md)

## Scope

PIIS addresses portable interface definitions, required functionality, behavioral contracts, conformance evidence and independently reproducible evaluation. It **does not change, reinterpret or extend** established standards such as HL7, FHIR, DICOM, X12, HTTP(S) or MQTT.

The initial canonical representation is proposed as JSON, with YAML as a possible authoring form. Neither is a substitute for formally specified behavior.

## Status

**Exploratory Working Draft — not an adopted standard, an official Internet-Draft, or an RFC.** The Spanish draft is the authoritative current working text. This repository invites discussion; it does not assert that the proposed portability mechanism has been demonstrated.

## Author and license

**Rodrigo Larenas** — original proponent and author.

Documentation and specification text: [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE.md).

The license does not imply an affiliation with, sponsorship by or endorsement from any organization or manufacturer. Licensing terms for any future implementation code will be determined separately.
