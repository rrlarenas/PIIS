#!/usr/bin/env python3
"""Structural JSON Schema checks only. NOT integration conformance tests."""
import copy
import json
from pathlib import Path
from jsonschema import Draft202012Validator

repo = Path(__file__).resolve().parents[2]
base = Path(__file__).resolve().parent
schema = json.loads((base / "piis-pfd-exploratory-0.1.schema.json").read_text(encoding="utf-8"))
Draft202012Validator.check_schema(schema)
check = Draft202012Validator(schema)
samples = [
    repo / "samples/clinical-dft-draft01/PIIS_PFD_DFT_DRAFT01.json",
    repo / "samples/tax-documents-draft01/PIIS_PFD_TAX_DOCUMENTS_DRAFT01.json",
]
for file in samples:
    doc = json.loads(file.read_text(encoding="utf-8"))
    errors = sorted(check.iter_errors(doc), key=lambda x: str(x.path))
    if errors:
        for err in errors:
            print(f"FAIL: {file}: {list(err.path)}: {err.message}")
        raise SystemExit(1)
    print(f"PASS (structural only): {file.relative_to(repo)}")

    # A missing observable contract must fail.
    invalid = copy.deepcopy(doc)
    del invalid["BehaviorContract"]
    assert not check.is_valid(invalid), "Missing BehaviorContract was accepted"

    # A missing operation type must fail.
    if invalid["Operation"]:
        invalid = copy.deepcopy(doc)
        del invalid["Operation"][0]["type"]
        assert not check.is_valid(invalid), "Missing operation type was accepted"

print("Structural validation and negative checks passed.")
print("No claim of executable semantics, functional equivalence, privacy certification or conformance.")
