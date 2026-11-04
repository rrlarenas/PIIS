"""Rebuild anonymized static cases from the pinned public samples; no execution."""
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
sys.path.insert(0, str(ROOT / 'tools/esb_to_piis'))
from validate import inspect_export, read_bounded


def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    manifest = json.loads((ROOT / 'samplesESB/manifest.json').read_text(encoding='utf-8'))
    cases, matrix = [], []
    for index, source in enumerate(manifest['sources'], 1):
        case_id = f'case-{index:02d}'
        case_dir = BASE / case_id
        artifacts, excluded, signals = [], Counter(), Counter()
        for entry in source['files']:
            path = ROOT / 'samplesESB' / entry['path']
            data = read_bounded(path)
            if hashlib.sha256(data).hexdigest() != entry['sha256']:
                raise ValueError('Source integrity mismatch')
            if path.suffix.lower() not in {'.xml', '.rlc', '.msgflow', '.subflow', '.esql', '.map'} or path.name in {'pom.xml', 'build.xml'}:
                excluded['auxiliary_or_documentation'] += 1
                continue
            inventory, findings = inspect_export(data, path.suffix)
            artifact_id = f'artifact-{len(artifacts)+1:04d}'
            artifacts.append({'artifact_ref': artifact_id, 'export': inventory, 'findings': findings})
            signals.update(inventory.get('signals', {}))
        case = {'case_ref': case_id, 'tool_version': '0.2',
                'functional_conformance': 'NOT_DEMONSTRATED', 'source_target_coverage': 'NOT_CHECKED',
                'migration_readiness': 'REQUIRES_REVIEW', 'artifact_count': len(artifacts),
                'excluded': dict(excluded), 'signals': dict(sorted(signals.items())), 'artifacts': artifacts}
        cases.append(case)
        case_dir.mkdir(exist_ok=True)
        write_json(case_dir / 'inventory_anonymized.json', case)
        queries = []
        for artifact in artifacts:
            for query in artifact['export'].get('sql_evidence', []):
                queries.append({'artifact_ref': artifact['artifact_ref'], **query})
        write_json(case_dir / 'sql_evidence_anonymized.json', {
            'case_ref': case_id, 'reference_scope': 'ARTIFACT_LOCAL',
            'identifiers': 'SYNTHETIC_NO_REVERSIBLE_MAPPING', 'queries': queries,
            'absence_means': 'NO_SQL_TEXT_DETECTED_IN_INSPECTED_ARTIFACTS_NOT_PROOF_OF_NO_DATABASE_EFFECTS'})
        matrix.append({'case_ref': case_id, 'artifacts': len(artifacts),
                       'components': sum(a['export']['component_count'] for a in artifacts),
                       'sql_queries': len(queries),
                       'sql_read_candidates': signals['sql_read_candidate'],
                       'sql_write_candidates': signals['sql_write_candidate'],
                       'opaque_logic': signals['opaque_logic'],
                       'external_references': signals['external_reference']})
    columns = list(matrix[0])
    with (BASE / 'comparison_matrix.csv').open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(matrix)
    write_json(BASE / 'comparison_report.json', {
        'tool_version': '0.2', 'comparison_kind': 'STATIC_HETEROGENEOUS_ARTIFACT_INVENTORY',
        'functional_equivalence': 'NOT_TESTED', 'shared_functional_contract': 'NOT_DEFINED',
        'scope': 'FOUR_INDEPENDENT_CASES_NOT_EQUIVALENT_IMPLEMENTATIONS',
        'reference_scope': 'CASE_AND_ARTIFACT_LOCAL_NO_CROSS_ENGINE_IDENTITY',
        'cases': matrix,
        'limitations': ['PARTIAL_SOURCE_SELECTION', 'NO_RUNTIME_EXECUTION', 'NO_DEPENDENCY_RESOLUTION',
                        'SQL_LEXICAL_PARTIAL_NOT_SEMANTIC', 'COUNTS_ARE_NOT_PORTABILITY_SCORES']})
    print(json.dumps(matrix, indent=2))


if __name__ == '__main__':
    main()
