#!/usr/bin/env python3
"""Experiment 05: validate static artifact integrity, NOT functional conformance or privacy certification."""
import csv
import json
import re
from pathlib import Path

base = Path(__file__).resolve().parent
candidate = json.loads((base / "PIIS.json").read_text(encoding="utf-8"))
report = json.loads((base / "review_report.json").read_text(encoding="utf-8"))

def csv_rows(name):
    with (base / name).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))

sql_csv = csv_rows("SQL_EVIDENCE.csv")
flows_csv = csv_rows("flow_matrix.csv")
flows = candidate["FlowCandidates"]
sql = candidate["SQLEvidence"]
summary = report["sql_analysis"]

assert candidate["Identity"]["id"] == "PIIS-EXPERIMENT-05"
assert report["experiment_id"] == "PIIS-EXPERIMENT-05"
assert candidate["piis_document"]["conformance_status"] == "NOT_DEMONSTRATED"
assert candidate["Identity"]["workload_executed"] is False
assert report["preconditions"]["equivalent_functional_result_declared"] is False
assert report["preconditions"]["equivalent_implementations_verified"] is False
assert report["preconditions"]["runtime_execution_performed"] is False
assert len(flows) == len(report["flow_reviews"]) == len(flows_csv) == 136
assert len(candidate["Operation"]) == 136
assert len(candidate["Destination"]) == report["summary"]["esb_a_destination_count"] == 263
assert len(sql) == len(sql_csv) == summary["statement_count"] == 263
assert summary["full_property_count"] == 44
assert summary["partial_literal_fragment_count"] == 219
assert summary["flows_with_sql_evidence"] == 75
assert len(report["findings"]) == 60
assert not candidate["ConformanceCases"]["evidence"]

flow_ids = {flow["id"] for flow in flows}
sql_ids = {entry["id"] for entry in sql}
assert len(flow_ids) == 136 and len(sql_ids) == 263
assert {row["sql_evidence_id"] for row in sql_csv} == sql_ids
assert {row["flow_ref"] for row in sql_csv}.issubset(flow_ids)
assert all(entry["esb"] == "ESB-A" for entry in sql)
assert all(entry["review_required"] for entry in sql)
assert all(entry["runtime_evidence"] == "NONE" for entry in sql)
assert all(not entry["original_semantics_complete"] for entry in sql)
assert sum(x["capture"] == "STATIC_FULL_PROPERTY" for x in sql) == 44
assert sum(x["capture"] == "PARTIAL_STATIC_LITERAL_FRAGMENT" for x in sql) == 219
assert set(ref for flow in flows for ref in flow["sql_evidence_refs"]) == sql_ids
assert all(flow["functional_equivalence_assumption"] == "NOT_ASSERTED" for flow in flows)
assert all(flow["sql_review"]["behavioral_equivalence"] == "NOT_DEMONSTRATED" for flow in flows)
assert all(entry["flowRef"] in flow_ids for entry in sql)

patterns = {
    "IPv4": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
    "email": r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}",
    "endpoint": r"https?://",
    "private key": r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY",
    "credential assignment": r"(?i)(password|pwd|passwd|secret)\s*[=:]\s*\S+",
    "native XML": r"<(?:serverConfiguration|Export|channel|Class)\b",
}
for name in ("PIIS.json", "review_report.json", "flow_matrix.csv", "SQL_EVIDENCE.csv", "SQL_ANALYSIS.md"):
    text = (base / name).read_text(encoding="utf-8")
    for kind, pattern in patterns.items():
        assert not re.search(pattern, text), f"{name}: possible {kind}"

print("PASS: Experiment 05 — 136 flows, 263 destinations, 263 SQL records across 75 flows.")
print("PASS: 44 configured SQL properties, 219 partial fragments; 60 findings.")
print("PASS: obvious sensitive patterns absent (NOT privacy certification).")
print("NOT DEMONSTRATED: SQL executability, cross-engine equivalence, functional conformance.")
