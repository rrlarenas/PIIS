#!/usr/bin/env python3
"""Structural tests of sanitized candidate artifacts; NOT conformance tests."""
import json
import re
import sys
from pathlib import Path

p = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
candidate = json.loads((p / "PIIS.json").read_text(encoding="utf-8"))
report = json.loads((p / "review_report.json").read_text(encoding="utf-8"))
assert candidate["piis_document"]["conformance_status"] == "NOT_DEMONSTRATED"
assert candidate["Identity"]["workload_executed"] is False
assert len(candidate["FlowCandidates"]) == 14
assert len(candidate["Operation"]) == 14
assert len(candidate["Destination"]) == 19
assert len(candidate["Dependency"]) == 19
assert len(report["flow_reviews"]) == 14
assert report["evidence"]["esb_b"]["matched_flow_count"] == 14
assert report["evidence"]["esb_b"]["production_item_states"] == {"false": 47, "true": 1}
assert report["evidence"]["esb_b"]["flows_with_manual_incomplete_implementation"] == ["FLOW-08"]
assert candidate["ConformanceCases"]["evidence"] == []
assert len(candidate["ConformanceCases"]["cases"]) == 5
assert len(report["findings"]) == 20

prohibited = [
    ("IPv4 address", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
    ("email address", re.compile(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")),
    ("web endpoint", re.compile(r"https?://", re.IGNORECASE)),
    ("private key", re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY")),
    ("embedded native export", re.compile(r"<(?:serverConfiguration|Export|channel|Class)\b", re.IGNORECASE)),
    ("embedded source script", re.compile(r"<(?:script|Implementation)>|<!\[CDATA\[", re.IGNORECASE)),
]
for filename in ("PIIS.json", "review_report.json", "flow_matrix.csv"):
    payload = (p / filename).read_text(encoding="utf-8")
    for name, regex in prohibited:
        assert not regex.search(payload), f"{filename}: unexpected {name}"
print("PASS: 14 flows; 19 destinations; 14 provenance matches; 20 static findings.")
print("PASS: no obvious endpoint, credential, or native export artifacts in JSON/CSV.")
print("NOT DEMONSTRATED: semantic completeness, confidentiality certification, runtime equivalence or conformance.")
