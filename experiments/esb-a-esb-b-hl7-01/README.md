# PIIS — Experimental interface pair 01 (ESB-A / ESB-B)

**Public, non-executable, anonymized structural evidence.** This case uses two configuration exports for the **same intended functional result**, implemented using different ESB paradigms. Functional equivalence is an **experiment precondition provided by the contributor**, not a result of testing.

## Published evidence

- `ESB-A_export_redacted.xml` — redacted structural evidence extracted from the first source export. Retains generic input transport, HL7 field references, filter/transform counts, active/inactive output descriptions and selected generic framing properties.
- `ESB-B_export_redacted.xml` — redacted structural evidence extracted from the second export. Retains only generic definitions, transformation statement counts, process node categories and active/inactive deployment items.
- `PIIS.json` — machine-readable **candidate** based on a local static extractor; not a sufficient portable executable definition.
- `review_report.json` — static comparison and unresolved findings.

**These two redacted XML files are NOT valid native engine exports**, cannot be imported by any ESB and **cannot be used to reconstruct the original interfaces**. To remove confidential material and vendor names, scripts, original class/connector identities, queries, hostnames, addresses, WSDLs, credentials, comments, embedded clinical messages, Base64 templates and all free-text metadata were deliberately omitted. The source exports have NOT been published. The XML describes the evidence structure retained from each source, not its original byte-for-byte content. A future research implementation should use privately held originals to reproduce these outputs, without publishing them.

## Scope and current observations

- The source configurations describe an **inbound HL7 v2 interface using MLLP/TCP**; this protocol information is preserved as public technical facts, not a PIIS-specific transport definition.
- The initial extractor found a shared `message_send` effect category and a database-read signal. **Matching categories are insufficient to prove identical semantics.**
- One database destination in ESB-A is disabled in the provided export.
- The extraction reported a `database_write` category in ESB-B only. **This can be a false-positive** arising from generic shared SQL helper code. Nothing here proves that an active interface branch writes to a database. The distinction remains **unresolved**.
- Neither configuration was executed for this analysis. No patient or financial record is included in the published files.

## Experiment contract

- **Assumption:** both source configurations target the same functional intent, though they use distinct implementation paradigms.
- **Output:** `PIIS.json` candidate plus comparative evidence; **not** a conformance result.
- **What is proven:** the four public files can be inspected as XML/JSON; structural elements were recovered without publishing scripts or payloads.
- **What is not proven:** equivalence, compliance, execution correctness, complete portable semantics, field-level rules, or response/ACK behavior.
- **Next step:** construct a completely synthetic reference interface and verify observable effects and ACK/failure behavior under identical test stimuli on independent implementations.

The profile and data fields remain **proposed**; PIIS JSON Schema 0.1 is only a structural review schema. See [the public review](https://github.com/rrlarenas/PIIS/issues/4), [schema proposal](../../proposals/json-pfd-0.1/README.md), and [PIIS Working Draft 02](../../drafts/PIIS_Working_Draft_02_EN.md).

**Data handling:** do not publish original exports, private binding values, scripts, real messages or organization-specific mappings. The two public XML artifacts intentionally contain no vendor brand names. Do not assume that automatic anonymization alone is an approval to disclose third-party IP.