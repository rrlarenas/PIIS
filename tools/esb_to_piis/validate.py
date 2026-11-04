#!/usr/bin/env python3
"""Local, exploratory ESB inventory and optional PIIS structural validation."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
import zipfile

from adapters import inspect_native

from defusedxml import ElementTree as ET
from defusedxml.common import DefusedXmlException
from jsonschema import Draft202012Validator

SCHEMA = Path(__file__).resolve().parents[2] / "proposals/json-pfd-0.1/piis-pfd-exploratory-0.1.schema.json"
MAX_BYTES = 32 * 1024 * 1024


def local(tag):
    return tag.rsplit("}", 1)[-1]


def read_bounded(path):
    with path.open("rb") as handle:
        data = handle.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError("Input exceeds the 32 MiB limit")
    return data


def load_json(data):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate JSON property")
            result[key] = value
        return result

    def invalid_constant(value):
        raise ValueError("Non-finite JSON number")

    return json.loads(data, object_pairs_hook=pairs, parse_constant=invalid_constant)


def inspect_export(data, suffix=""):
    native = inspect_native(data, suffix)
    if native is not None:
        return native
    root = ET.fromstring(data, forbid_dtd=True)
    tags = Counter(local(node.tag) for node in root.iter())
    root_tag = local(root.tag)
    if root_tag == "SanitizedExport" and root.get("profile") == "PIIS-structural-evidence/0.1":
        profile = "piis-redacted-evidence-0.1"
        components = [n for n in root.iter() if local(n.tag) in {"Input", "Destination", "Definition", "Item"}]
    elif root_tag in {"channel", "list", "channels", "serverConfiguration"} and tags["channel"]:
        profile = "channel-xml-exploratory"
        components = [n for n in root.iter() if local(n.tag) == "channel"]
    elif root_tag == "Export" and tags["Class"]:
        profile = "class-export-xml-exploratory"
        components = [n for n in root.iter() if local(n.tag) == "Class"]
    else:
        raise ValueError("Unsupported XML export structure; no adapter matched")

    inventory = []
    for index, node in enumerate(components, 1):
        # Synthetic locators avoid copying source names, scripts, bindings or secrets.
        inventory.append({"source_ref": f"component-{index:04d}", "element": local(node.tag)})
    findings = [{"code": "SEMANTICS_NOT_ESTABLISHED", "severity": "warning",
                 "message": "Static inventory cannot establish rules, ordering, ACK, errors or side effects."}]
    if profile == "piis-redacted-evidence-0.1":
        findings.append({"code": "REDACTED_SOURCE", "severity": "warning",
                         "message": "Evidence XML is not a native export and cannot support complete migration."})
    # Code presence is evidence of review work, never proof of a reachable effect.
    if any(local(n.tag).lower() in {"script", "code", "method", "sql", "query"}
           for n in root.iter()):
        findings.append({"code": "OPAQUE_LOGIC", "severity": "warning",
                         "message": "Code or query elements require semantic and reachability review."})
    return {"profile": profile, "sha256": hashlib.sha256(data).hexdigest(),
            "component_count": len(inventory), "components": inventory}, findings


def validate_pfd(data):
    document = load_json(data)
    schema = load_json(SCHEMA.read_bytes())
    Draft202012Validator.check_schema(schema)
    errors = list(Draft202012Validator(schema).iter_errors(document))
    # Schema error messages can contain instance values. Report keywords only.
    return {"status": "INVALID" if errors else "VALID",
            "schema": "piis-pfd-exploratory-0.1",
            "errors": [{"keyword": e.validator} for e in errors]}, document


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("export", type=Path, help="ESB XML/XMI, Rhapsody RLC or IBM ESQL artifact")
    parser.add_argument("--piis", type=Path, help="Optional existing PFD JSON to validate structurally")
    parser.add_argument("--output", type=Path, help="Write JSON report (default: stdout)")
    args = parser.parse_args(argv)
    if args.output and args.output.resolve() in {p.resolve() for p in (args.export, args.piis, SCHEMA) if p}:
        parser.error("Output must differ from input and schema paths")
    report = {"tool_version": "0.2", "functional_conformance": "NOT_DEMONSTRATED",
              "migration_readiness": "REQUIRES_REVIEW", "source_target_coverage": "NOT_CHECKED",
              "findings": []}
    exit_code = 0
    try:
        report["export"], report["findings"] = inspect_export(read_bounded(args.export), args.export.suffix)
        if args.piis:
            report["piis"], _ = validate_pfd(read_bounded(args.piis))
            if report["piis"]["status"] == "INVALID":
                exit_code = 1
        else:
            report["piis"] = {"status": "NOT_PROVIDED"}
    except (OSError, ValueError, ET.ParseError, DefusedXmlException, RecursionError,
            zipfile.BadZipFile, NotImplementedError, RuntimeError, EOFError):
        # Do not echo parser exceptions: they may contain confidential source values.
        report["findings"].append({"code": "INPUT_ERROR", "severity": "error",
                                    "message": "Unreadable, malformed, unsafe, oversized or unsupported input."})
        exit_code = 2
    result = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        try:
            args.output.write_text(result, encoding="utf-8")
        except OSError:
            print("Cannot write report.", file=sys.stderr)
            return 2
    else:
        print(result, end="")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
