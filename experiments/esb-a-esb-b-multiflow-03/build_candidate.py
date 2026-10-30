#!/usr/bin/env python3
"""Conservative ESB-A / ESB-B static evidence extraction.

Inputs are local, confidential XML exports. Outputs deliberately contain NO native
scripts, endpoint addresses, credential details, names, patient data, SQL, IDs,
or raw XML. Semantic equivalence is a declared research assumption, never a result.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path
import xml.etree.ElementTree as ET


def attr(elem, name, default=None):
    return elem.get(name, default) if elem is not None else default


def text(elem, path, default=None):
    return elem.findtext(path, default) if elem is not None else default


def connector_kind(properties):
    # Recognize only broad transport families. Product-specific names are never emitted.
    cls = attr(properties, "class", "").lower()
    if "tcp" in cls:
        return "tcp"
    if "http" in cls:
        return "http"
    if "webservice" in cls or ".ws." in cls:
        return "soap"
    if "database" in cls or "jdbc" in cls or "sql" in cls:
        return "database"
    if "smtp" in cls or "email" in cls:
        return "email"
    if "file" in cls:
        return "file"
    if "javascript" in cls or "js." in cls:
        return "script"
    return "unknown"


def count_steps(root, path):
    transformer = root.find(path)
    if transformer is None:
        return 0
    return len(transformer.findall("./elements/*")) + len(transformer.findall("./steps/step"))


def count_filters(root, path):
    filter_el = root.find(path)
    if filter_el is None:
        return 0
    return len(filter_el.findall("./elements/*")) + len(filter_el.findall("./rules/rule"))


def classify_items(items):
    types = Counter()
    for i in items:
        cls = i.get("ClassName", "")
        low = cls.lower()
        if "service" in low:
            types["source"] += 1
        elif "operation" in low:
            types["destination_or_operation"] += 1
        elif "routingengine" in low or "process" in low:
            types["process_or_routing"] += 1
        else:
            types["other"] += 1
    return dict(types)


def observed_hl7_fields(xml_or_script_text):
    """Returns field references only; not their values, paths or surrounding code."""
    return sorted({f"{segment}.{index}" for segment, index in re.findall(
        r"\b(MSH|PID|PV1|ORC|OBR|OBX|FT1|AL1|NK1|DG1|NTE|EVN|MSA|SCH|RXA|RXR|TXA|MFE|MFI)[.:](\d+)",
        xml_or_script_text, flags=re.IGNORECASE)})


def write_json(path, doc):
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def build(a_path, b_path, outdir):
    a = ET.parse(a_path).getroot()
    b = ET.parse(b_path).getroot()
    if a.tag != "serverConfiguration" or b.tag != "Export":
        raise ValueError("Unexpected XML export roots: cannot apply the comparison profile")
    channels = a.findall("./channels/channel")
    production = next((cls for cls in b.findall("./Class") if text(cls, "Super") == "Ens.Production"), None)
    if production is None:
        raise ValueError("ESB-B export lacks a production definition")
    prod_xml = text(production, "./XData[@name='ProductionDefinition']/Data", "")
    prod = ET.fromstring(prod_xml)
    items = prod.findall("./Item")
    bclasses = b.findall("./Class")

    # The source export contains named channels. The generated export uses Cxx-prefixed
    # implementation categories. Confirm that all categories exist before matching indexes.
    cat_by_num = {}
    for item in items:
        cat = item.get("Category", "")
        m = re.match(r"^C(\d{2})(?=[A-Z])", cat)
        if m:
            cat_by_num.setdefault(int(m.group(1)), set()).add(cat)
    flow_candidates, dep = [], []
    operations, destinations = [], []
    findings = []
    summary_a_src, summary_a_dest = Counter(), Counter()
    summary_b_state = Counter(i.get("Enabled", "UNKNOWN") for i in items)
    manually_incomplete_flow_ids = []
    for idx, channel in enumerate(channels):
        flow_id = f"FLOW-{idx+1:02d}"
        source = channel.find("./sourceConnector")
        dests = channel.findall("./destinationConnectors/connector")
        source_kind = connector_kind(source.find("./properties") if source is not None else None)
        source_transform_steps = count_steps(source, "./transformer")
        source_filter_rules = count_filters(source, "./filter")
        group = sorted(cat_by_num.get(idx, set()))
        bitems = [item for item in items if item.get("Category") in group]
        category_mapping_confirmed = (len(group) == 1 and bool(bitems) and all(
            text(channel,"name", "") in i.get("Comment","") for i in bitems
        ))
        # Avoid copying any original class or connector identifiers into outputs.
        bclass_group = []
        for cl in bclasses:
            name = cl.get("name", "")
            if re.search(rf"\.C{idx:02d}(?=[A-Z])", name):
                bclass_group.append(cl)
        b_proc = sum(text(cl, "Super") == "Ens.BusinessProcessBPL" for cl in bclass_group)
        b_rule = sum(text(cl, "Super") == "Ens.Rule.Definition" for cl in bclass_group)
        b_source_transform = sum(text(cl, "Super") == "Ens.DataTransformDTL" for cl in bclass_group)
        b_manual = 0
        for cl in bclass_group:
            strings = [text(cl, "Description", "")] + [(el.text or "") for el in cl.findall(".//Implementation")]
            # Limiting search to implementation and description avoids counting code duplication.
            if any("TODO MANUAL" in s.upper() for s in strings):
                b_manual += 1
        if b_manual:
            manually_incomplete_flow_ids.append(flow_id)
        a_fields = observed_hl7_fields(ET.tostring(channel, encoding="unicode"))
        b_fields = observed_hl7_fields(" ".join(ET.tostring(cl, encoding="unicode") for cl in bclass_group))
        result = {
            "id": flow_id,
            "functional_intent_equivalence": "ASSUMED_PRECONDITION_NOT_VERIFIED",
            "esb_a": {
                "source_kind": source_kind,
                "source_enabled": text(source, "enabled") == "true",
                "observed_hl7_field_references": a_fields,
                "source_transform_step_count": source_transform_steps,
                "source_filter_rule_count": source_filter_rules,
                "destination_count": len(dests),
                "enabled_destination_count": sum(text(d, "enabled") == "true" for d in dests),
            },
            "esb_b": {
                "category_match": "INDEX_AND_PROVENANCE_COMMENT_MATCH" if category_mapping_confirmed else "NO_UNAMBIGUOUS_MATCH",
                "production_item_count": len(bitems),
                "enabled_production_item_count": sum(i.get("Enabled") == "true" for i in bitems),
                "process_count": b_proc,
                "routing_rule_count": b_rule,
                "transform_class_count": b_source_transform,
                "manual_implementation_class_count": b_manual,
                "observed_hl7_field_references": b_fields,
            },
            "hl7_field_reference_review": {
                "only_in_esb_a": sorted(set(a_fields)-set(b_fields)),
                "only_in_esb_b": sorted(set(b_fields)-set(a_fields)),
                "interpretation": "LEXICAL_REFERENCE_ONLY_NO_BEHAVIORAL_COMPARISON",
            },
            "effect_semantics": "PARTIAL_STATIC_EXTRACTION",
            "implementation_equivalence": "NOT_DEMONSTRATED",
        }
        if not category_mapping_confirmed:
            findings.append({"id":f"F-{idx+1:02d}-MAPPING", "flow":flow_id, "severity":"REVIEW", "observed":"No generated target category matched the source channel index", "conclusion":"NOT_DEMONSTRATED"})
        if bitems and not any(i.get("Enabled") == "true" for i in bitems):
            findings.append({"id":f"F-{idx+1:02d}-DISABLED", "flow":flow_id, "severity":"BLOCKER_FOR_RUNTIME_CONFORMANCE", "observed":"All mapped ESB-B production items are disabled in the supplied export", "conclusion":"NOT_DEMONSTRATED"})
        if b_manual:
            findings.append({"id":f"F-{idx+1:02d}-MANUAL", "flow":flow_id, "severity":"BLOCKER_FOR_RUNTIME_CONFORMANCE", "observed":"Generated ESB-B code explicitly contains an unimplemented manual operation", "conclusion":"NOT_DEMONSTRATED"})
        result["destinations"] = []
        for dest_idx, dest in enumerate(dests, 1):
            d_id = f"DST-{idx+1:02d}-{dest_idx:02d}"
            d_kind = connector_kind(dest.find("./properties"))
            a_active = text(dest, "enabled") == "true"
            summary_a_dest[d_kind] += 1
            result["destinations"].append({
                "id": d_id,
                "kind": d_kind,
                "esb_a_enabled": a_active,
                "esb_a_transform_step_count": count_steps(dest, "./transformer"),
                "esb_a_filter_rule_count": count_filters(dest, "./filter"),
                "esb_b_destination_mapping": "UNRESOLVED_INDIVIDUAL_ITEM" if group else "UNKNOWN",
            })
            destinations.append({
                "id": d_id,
                "kind": "external_effect" if d_kind != "unknown" else "unknown",
                "status_original": "ESB_A_ENABLED_ESB_B_DEPLOYMENT_DISABLED" if a_active and bitems else "REQUIRES_REVIEW",
                "binding": "PRIVATE:DESTINATION_"+d_id,
                "transport_kind":d_kind,
                "observable_result":"NOT_VERIFIED"
            })
            dep.append({"id":"DEP-"+d_id,"role":f"logical_{d_kind}_endpoint","binding":"PRIVATE:DEPENDENCY_"+d_id})
        summary_a_src[source_kind] += 1
        operations.append({
            "id": "OP-"+flow_id,
            "sequence": idx+1,
            "type": "flow_candidate",
            "flowRef":flow_id,
            "presentation_order_only":True,
            "portable_expression_semantics":"NOT_DEFINED",
            "observable_order":"UNVERIFIED"
        })
        flow_candidates.append(result)

    # Safeguard: no native names, scripts, IPs, credentials, or SQL copied to outputs.
    prod_enabled_nonflow = [i for i in items if i.get("Enabled") == "true" and not re.match(r"^C\d{2}", i.get("Category", ""))]
    top_findings = [
      {"id":"F-GLOBAL-01", "severity":"BLOCKER_FOR_RUNTIME_CONFORMANCE", "observed":"Production items corresponding to all 14 integration flows are disabled in the ESB-B export; only one shared auxiliary item is enabled", "conclusion":"CONFIGURATION_GAP_NOT_FUNCTIONAL_TEST"},
      {"id":"F-GLOBAL-02", "severity":"BLOCKER_FOR_RUNTIME_CONFORMANCE", "observed":"One ESB-B SOAP destination is explicitly not implemented; its method returns an error", "conclusion":"STATIC_IMPLEMENTATION_GAP"},
      {"id":"F-GLOBAL-03", "severity":"EVIDENCE_GAP", "observed":"ESB-B reports that its classes were generated from ESB-A; they are not independent implementations", "conclusion":"DO_NOT_CLAIM_INDEPENDENT_CONFORMANCE"},
      {"id":"F-GLOBAL-04", "severity":"EVIDENCE_GAP", "observed":"No runtime inputs, destination observations, response messages or execution measurements were supplied", "conclusion":"NOT_EXECUTED"},
      {"id":"F-GLOBAL-05", "severity":"SEMANTIC_GAP", "observed":"Operation content, filters, business mappings, acknowledgment behavior and error handling require analysis beyond counts and broad transport classifications", "conclusion":"PARTIAL_CANDIDATE"},
    ]
    report = {
      "title":"ESB-A / ESB-B multi-flow static comparison — evidence report",
      "experiment_id":"PIIS-ESB-EXP-03",
      "status":"STATIC_REVIEW_NOT_CONFORMANCE",
      "preconditions":{"functional_intent_equivalence":"ASSUMED_BY_EXPERIMENT_DESIGN_NOT_VERIFIED", "independent_implementations":False},
      "evidence":{
        "esb_a":{"source_channel_count":len(channels),"source_connectors_by_kind":dict(summary_a_src),"destination_count":len(destinations),"destinations_by_kind":dict(summary_a_dest),"enabled_destination_count":sum(1 for v in flow_candidates for d in v["destinations"] if d["esb_a_enabled"])},
        "esb_b":{"generated_classes":len(bclasses),"production_items":len(items),"production_item_states":dict(summary_b_state),"enabled_nonflow_auxiliary_items":len(prod_enabled_nonflow),"matched_flow_count":sum(v["esb_b"]["category_match"]=="INDEX_AND_PROVENANCE_COMMENT_MATCH" for v in flow_candidates),"flows_with_manual_incomplete_implementation":manually_incomplete_flow_ids}
      },
      "findings":top_findings+findings,
      "flow_reviews":flow_candidates,
      "comparison_rules":[
         "Counts and metadata are evidence of configuration structure, not equivalent outcomes.",
         "Every enabled ESB-A destination remains an explicit candidate effect even if ESB-B maps it to a different paradigm.",
         "A disabled runtime item is recorded as supplied, not assumed enabled during deployment.",
         "The output never includes original scripts, SQL, messages, endpoints, names, passwords or production XML.",
         "HL7 field references are lexical hints only; differing sets are not proof of changed behavior.",
         "The original XML exports remain local; generated data is a partial research abstraction."
      ]
    }
    candidate={
      "piis_document":{"kind":"PortableFunctionalDefinition","working_profile":"PIIS-ESB-comparison/0.1-exploratory","schema_status":"PROPOSED_NOT_STANDARDIZED","semantic_status":"PARTIAL_STATIC_EXTRACTION","conformance_status":"NOT_DEMONSTRATED","language":"en","source_of_truth":"static_export_comparison_under_declared_equivalence_of_functional_intent"},
      "Identity":{"id":"PIIS-CANDIDATE-ESB-03","title":"Multi-interface candidate from two architecture paradigms","version":"0.1-candidate","normative":False,"anonymized":True,"workload_executed":False},
      "ExternalStandards":{"status":"NOT_NORMATIVELY_PROFILED","accepted_as_is":["HL7 v2", "MLLP", "TCP", "HTTP", "SOAP", "SQL", "JSON", "XML"],"redefines_existing_standards":False},
      "Source":{"id":"S-AGGREGATE","kind":"multi_flow_configuration","flow_count":len(channels),"per_flow_inputs":"FlowCandidates[].esb_a.source_kind","literal_endpoint_data_included":False},
      "Rule":{"portable_expressions":"NOT_EXTRACTED","cross_engine_rule_equivalence":"NOT_DEMONSTRATED","ack_and_exception_semantics":"REQUIRES_TESTS"},
      "Operation":operations,
      "Destination":destinations,
      "Channel":{"functional_intent_equivalence":"ASSUMED_AS_PRECONDITION_NOT_VERIFIED","flows":len(flow_candidates),"runtime_enabled_esb_b_flow_items":sum(v["esb_b"]["enabled_production_item_count"] for v in flow_candidates),"execution_order":"NOT_ESTABLISHED","routing_and_parallelism":"NOT_ESTABLISHED"},
      "Dependency":dep,
      "BehaviorContract":{"status":"CANDIDATE_NOT_TESTABLE","required_effects":[f"CANDIDATE: {f['id']} has {len(f['destinations'])} logical output(s); exact conditions, payload and runtime effects require review" for f in flow_candidates],"forbidden_effects":[],"failures_and_recovery":"NOT_ESTABLISHED","acknowledgements":"NOT_ESTABLISHED","timing_and_ordering":"NOT_ESTABLISHED"},
      "ConformanceCases":{"status":"NOT_EXECUTED","cases":[
        {"id":"TC-01","scenario":"Synthetic accepted HL7 input on a selected MLLP flow","expected":"Define exact transformed output, recipient selection and ACK before execution"},
        {"id":"TC-02","scenario":"Synthetic rejected HL7 input on a filtered flow","expected":"Define suppression, error response and persistence effects before execution"},
        {"id":"TC-03","scenario":"Synthetic scheduled poll returning no rows","expected":"Define request, output suppression and status behavior before execution"},
        {"id":"TC-04","scenario":"Outbound SOAP operation invoked with synthetic financial data","expected":"ESB-B currently lacks implementation; cannot pass until corrected and verified"},
        {"id":"TC-05","scenario":"Synthetic delivery failure and retry boundary","expected":"Define ACK, queue, retry, timeout and downstream effect obligations before execution"}
      ],"evidence":[]},
      "FlowCandidates":flow_candidates,
      "KnownLimitations":[
        "Assumed functional outcome equivalence is a study precondition, not a verified result.",
        "ESB-B is a generated conversion, not an independent implementation.",
        "All mapped integration items are marked disabled in ESB-B export; one auxiliary service is enabled.",
        "An outbound SOAP implementation remains manually incomplete.",
        "No source scripts, SQL, message templates, passwords, endpoint locations, channel names or patient data were copied.",
        "Field-level transformations, decision/routing semantics, correlation and external contract equivalence remain unresolved.",
        "Top-level Operation sequence denotes flow presentation order, not execution ordering.",
        "Some candidate destination effect categories are too coarse to demonstrate equivalence.",
        "This candidate is structurally informative, not directly executable and not conformance tested.",
        "JSON Schema validation is separate from executable PIIS semantics and runtime conformance.",
      ]
    }
    outdir.mkdir(parents=True,exist_ok=True)
    write_json(outdir/"PIIS.json",candidate)
    write_json(outdir/"review_report.json",report)
    return candidate,report


if __name__=="__main__":
    if len(sys.argv)!=4:
        print("Usage: python build_candidate.py <ESB-A.xml> <ESB-B.xml> <OUTPUT_DIR>",file=sys.stderr)
        raise SystemExit(2)
    candidate,report=build(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
    print(json.dumps({"flows":len(candidate["FlowCandidates"]),"destinations":len(candidate["Destination"]),"findings":len(report["findings"]),"status":candidate["piis_document"]["conformance_status"]},indent=2))
