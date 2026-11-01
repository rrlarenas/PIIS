#!/usr/bin/env python3
"""PIIS structural checks only; NOT functional, privacy, or runtime certification."""
import csv
import json
import re
from pathlib import Path

base = Path(__file__).resolve().parent
candidate = json.loads((base / "PIIS.json").read_text(encoding="utf-8"))
report = json.loads((base / "review_report.json").read_text(encoding="utf-8"))
with (base / "flow_matrix.csv").open(encoding="utf-8", newline="") as handle:
    rows = list(csv.DictReader(handle))

assert candidate["piis_document"]["conformance_status"] == "NOT_DEMONSTRATED"
assert candidate["Identity"]["workload_executed"] is False
assert candidate["Identity"]["normative"] is False
assert candidate["Identity"]["original_exports_included"] is False
assert report["preconditions"]["equivalent_functional_result_declared"] is False
assert report["preconditions"]["equivalent_implementations_verified"] is False
assert len(candidate["FlowCandidates"]) == len(report["flow_reviews"]) == len(rows) == 136
assert len(candidate["Operation"]) == 136
assert len(candidate["Destination"]) == report["summary"]["esb_a_destination_count"] == 263
assert len(candidate["ConformanceCases"]["evidence"]) == 0
assert len(report["findings"]) == 60
assert len({x["id"] for x in candidate["FlowCandidates"]}) == 136
assert all(x["functional_equivalence_assumption"] == "NOT_ASSERTED" for x in candidate["FlowCandidates"])
assert all(x["review"]["functional_conformance"] == "NOT_DEMONSTRATED" for x in candidate["FlowCandidates"])
checks = {
    "IPv4 address": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "email": re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}"),
    "endpoint URL": re.compile(r"https?://", re.I),
    "native XML export": re.compile(r"<(?:serverConfiguration|Export|channel|Class)\b", re.I),
    "private key": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY"),
}
for filename in ("PIIS.json", "review_report.json", "flow_matrix.csv"):
    text = (base / filename).read_text(encoding="utf-8")
    for label, regex in checks.items():
        assert not regex.search(text), f"{filename}: potential {label}"

print("PASS: static integrity (136 flow candidates, 263 destinations, 60 findings).")
print("PASS: obvious sensitive patterns absent in JSON/CSV; NOT confidentiality certification.")
print("NOT DEMONSTRATED: runtime equivalence, functional conformance, executable PFD.")
