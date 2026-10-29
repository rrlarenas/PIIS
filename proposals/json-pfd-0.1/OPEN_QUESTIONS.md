# PIIS JSON PFD — Questions for External Review (Proposal 0.1)

This is a request for **specific counterexamples and proposed semantics**, not approval of a finished standard.

1. **PFD completeness:** Is the information in `Source`, `Rule`, `Operation`, `Destination` and `Dependency` sufficient to implement the same interface without referring to the source engine? Provide a concrete omission.
2. **Existing solutions:** Which published, versioned workflow/modeling standards already describe that missing behavior? Cite clauses or reproducible implementations.
3. **Operation model:** Should operations be composable typed primitives, a declarative expression graph, or references to existing interoperable languages? What is the minimum expressive set?
4. **Observables:** Which externally observable events must OC include for messages, DB writes, files, notifications and errors? What is required to compare an asynchronous outcome?
5. **Ordering and concurrency:** Can a simple `sequence` key represent meaningful behavior, or do we require explicit dependency edges and ordering constraints?
6. **Capabilities and failures:** How does an implementation report that it cannot satisfy a required function, *before* migration?
7. **Contracts:** What is the smallest typed assertion format that a genuinely independent conformance runner can evaluate?
8. **Privacy and bindings:** How should deployment-specific values be referenced without leaking secrets or business IP? Which semantics belong in the public PFD versus a private deployment profile?
9. **Canonicalization:** Should we preserve the current uppercase keys or introduce lowerCamelCase in a clean next version? How should we map both existing samples?
10. **Falsification:** What is the smallest real integration scenario that disproves the proposed portability model?

**Evidence request:** include sample snippets with synthetic data, exact specification/version references, and observed results where possible. Do not include real patient or client data, credentials, endpoints or proprietary implementation code.

Use [issue #2](https://github.com/rrlarenas/PIIS/issues/2) for the functional model discussion; the dedicated review thread is [Issue #4 — JSON PFD Proposal 0.1](https://github.com/rrlarenas/PIIS/issues/4).
