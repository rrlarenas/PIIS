"""Static adapters. Output is an allowlisted inventory, never source text."""
from collections import Counter
import hashlib
import io
import re
import zipfile

from defusedxml import ElementTree as ET

LIMIT = 32 * 1024 * 1024
CAMEL = "http://camel.apache.org/schema/spring"
SYNAPSE = "http://ws.apache.org/ns/synapse"
RHAPSODY = "urn:www.yourcompany.com/Rhapsody/Schema.xml"
XMI = "{http://www.omg.org/XMI}"


def local(tag):
    return tag.rsplit("}", 1)[-1]


def namespace(tag):
    return tag[1:].split("}", 1)[0] if tag.startswith("{") else ""


class Inventory:
    def __init__(self, profile, data):
        self.report = {"profile": profile, "sha256": hashlib.sha256(data).hexdigest(),
                       "components": [], "signals": {}, "sql_evidence": [],
                       "analysis_scope": "STATIC_SINGLE_ARTIFACT_NO_DEPENDENCY_RESOLUTION"}
        self.signals = Counter()
        self.tables = {}
        self.fields = {}

    def add(self, element, category="opaque_logic"):
        ref = f"component-{len(self.report['components']) + 1:04d}"
        self.report["components"].append({"source_ref": ref, "element": element, "category": category})
        self.signals[category] += 1
        return ref

    def sql(self, text):
        # Deliberately limited SQL recognizer. Unsupported expressions stay unresolved.
        # No identifier, literal, query, hash of identifier, or reversible map is emitted.
        text = re.sub(r"/\*.*?\*/|--[^\r\n]*", " ", text, flags=re.S)
        text = re.sub(r"'(?:''|[^'])*'", " ? ", text)
        ident = r'(?:\[[^\]\r\n]+\]|"[^"\r\n]+"|[A-Za-z_][\w$]*)(?:\s*\.\s*(?:\[[^\]\r\n]+\]|"[^"\r\n]+"|[A-Za-z_][\w$]*))*'
        operation = re.match(r"\s*(SELECT|INSERT|UPDATE|DELETE)\b", text, re.I)
        kind = operation[1].lower() if operation else "unknown"
        record = {"source_ref": f"query-{len(self.report['sql_evidence']) + 1:04d}",
                  "operation": kind, "tables": [], "fields": [],
                  "coverage": "PARTIAL_LEXICAL_SINGLE_TABLE", "reachability": "NOT_CHECKED"}
        table_pattern = {"select": "FROM", "insert": r"INSERT\s+INTO", "update": "UPDATE", "delete": r"DELETE\s+FROM"}.get(kind)
        match = re.search(rf"\b(?:{table_pattern})\s+({ident})", text, re.I) if table_pattern else None
        ambiguous = re.search(r"\b(JOIN|UNION|WITH)\b", text, re.I) or len(re.findall(r"\bSELECT\b", text, re.I)) > 1
        ambiguous = ambiguous or ';' in text.strip().rstrip(';')
        if kind == 'select' and match:
            from_clause = re.split(r'\b(?:WHERE|ORDER|GROUP|HAVING)\b', text[match.end():], maxsplit=1, flags=re.I)[0]
            ambiguous = ambiguous or ',' in from_clause
        if match and not ambiguous:
            key = re.sub(r'[\[\]"\s]', '', match[1]).lower()
            table_ref = self.tables.setdefault(key, f"table-{len(self.tables) + 1:04d}")
            record['tables'] = [table_ref]
            candidates = []
            if kind == 'insert':
                columns = re.match(r"\s*\(([^)]+)\)", text[match.end():])
                if columns:
                    candidates += columns[1].split(',')
            elif kind == 'select':
                projection = re.sub(r'^\s*SELECT\s+(?:DISTINCT\s+)?(?:TOP\s*\(?\d+\)?\s*)?', '', text[:match.start()], flags=re.I)
                candidates += projection.split(',')
            # Only plain identifiers on the left of a comparison/assignment and ORDER BY.
            candidates += re.findall(rf'({ident})\s*(?:>=|<=|<>|!=|=|>|<|\bIS\s+NULL\b)', text[match.end():], flags=re.I)
            order = re.search(r'\bORDER\s+BY\s+(.+)', text, re.I | re.S)
            if order:
                candidates += [re.sub(r'\s+(ASC|DESC)\s*$', '', c.strip(), flags=re.I) for c in order[1].split(',')]
            for candidate in candidates:
                if re.fullmatch(ident, candidate.strip()):
                    field_key = (key, re.sub(r'[\[\]"\s]', '', candidate).lower().split('.')[-1])
                    field_ref = self.fields.setdefault(field_key, f"field-{len(self.fields) + 1:04d}")
                    item = {"table_ref": table_ref, "field_ref": field_ref}
                    if item not in record['fields']:
                        record['fields'].append(item)
        else:
            record['coverage'] = 'UNRESOLVED'
        self.report['sql_evidence'].append(record)
        self.signals['sql_read_candidate' if kind == 'select' else 'sql_write_candidate' if kind in {'insert', 'update', 'delete'} else 'sql_unknown'] += 1

    def finish(self):
        self.report['component_count'] = len(self.report['components'])
        self.report['signals'] = dict(sorted(self.signals.items()))
        findings = [{"code": "SEMANTICS_NOT_ESTABLISHED", "severity": "warning",
                     "message": "Static evidence does not prove execution, reachability, equivalence or migration readiness."},
                    {"code": "DEPENDENCIES_NOT_RESOLVED", "severity": "warning",
                     "message": "External code, templates, references and bindings require separate review."}]
        if self.report['sql_evidence']:
            findings.append({"code": "SQL_PARTIAL_ANALYSIS", "severity": "warning",
                             "message": "SQL identifiers are replaced by artifact-local synthetic references; expressions, parameters and dynamic SQL remain unresolved."})
        return self.report, findings


def inspect_native(data, suffix=""):
    if len(data) > LIMIT:
        raise ValueError('Oversized input')
    if data.startswith(b'PK'):
        inv = Inventory('rhapsody-rlc-exploratory', data)
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            entries = archive.infolist()
            if len(entries) > 512 or sum(e.file_size for e in entries) > LIMIT:
                raise ValueError('Oversized archive')
            if len({e.filename for e in entries}) != len(entries):
                raise ValueError('Duplicate archive entries')
            roots = []
            for entry in entries:
                if entry.is_dir():
                    continue
                if not entry.filename.lower().endswith('.xml') or entry.flag_bits & 1:
                    raise ValueError('Unsupported archive entry')
                with archive.open(entry) as handle:
                    content = handle.read(LIMIT + 1)
                if len(content) > LIMIT:
                    raise ValueError('Oversized archive entry')
                roots.append(ET.fromstring(content, forbid_dtd=True))
            engines = [r for r in roots if r.tag == f'{{{RHAPSODY}}}Engine']
            if len(engines) != 1:
                raise ValueError('Not a recognized Rhapsody archive')
            for root in roots:
                if root not in engines and (root.tag != 'config' or not any(local(k) == 'schemaName' and namespace(k) == 'http://www.orionhealth.com/Rhapsody/IDE' for k in root.attrib)):
                    raise ValueError('Unrecognized Rhapsody companion')
                rhapsody(root, inv)
        return inv.finish()
    if suffix.lower() == '.esql':
        text = data.decode('utf-8-sig')
        # Modules are logic evidence, not SQL effects. Message-tree SELECT/SET is not database SQL.
        clean = re.sub(r'/\*.*?\*/|--[^\r\n]*', ' ', text, flags=re.S)
        if not re.search(r'\bCREATE\s+(COMPUTE|FILTER|DATABASE)\s+MODULE\b', clean, re.I):
            raise ValueError('Unsupported ESQL structure')
        inv = Inventory('ibm-esql-exploratory', data)
        inv.add('module', 'opaque_logic')
        if re.search(r'\b(PASSTHRU|Database)\b', clean, re.I):
            inv.signals['database_logic_unresolved'] += 1
        return inv.finish()
    root = ET.fromstring(data, forbid_dtd=True)
    nodes = list(root.iter())
    if root.tag == '{http://www.eclipse.org/emf/2002/Ecore}EPackage' and any(n.tag == 'eClassifiers' and n.get(XMI+'type') == 'eflow:FCMComposite' for n in nodes):
        inv = Inventory('ibm-flow-xmi-exploratory', data)
        mapping = {'FCMSource': 'input', 'FCMSink': 'output', 'ComIbmWSInput.msgnode': 'input',
                   'ComIbmWSReply.msgnode': 'output', 'ComIbmFilter.msgnode': 'filter',
                   'ComIbmCompute.msgnode': 'opaque_logic', 'ComIbmJavaCompute.msgnode': 'opaque_logic',
                   'ComIbmMapping.msgnode': 'transform'}
        refs = {}
        for node in nodes:
            if node.tag == 'nodes':
                typ = node.get(XMI+'type', '')
                prefix, _, name = typ.partition(':')
                category = mapping.get(prefix, mapping.get(name, 'external_reference'))
                identity = node.get(XMI+'id')
                if not identity or identity in refs:
                    raise ValueError('Missing or duplicate node identity')
                refs[identity] = inv.add('node', category)
        inv.report['connections'] = []
        for node in nodes:
            if node.tag == 'connections':
                source, target = refs.get(node.get('sourceNode')), refs.get(node.get('targetNode'))
                inv.report['connections'].append({'source_ref': source, 'target_ref': target,
                                                   'resolution': 'RESOLVED' if source and target else 'UNRESOLVED'})
        return inv.finish()
    if namespace(root.tag) == 'http://www.ibm.com/2008/ccl/Mapping' and local(root.tag) == 'mappingRoot':
        inv = Inventory('ibm-map-exploratory', data)
        inv.add('mapping', 'transform')
        return inv.finish()
    if any(namespace(n.tag) == CAMEL and local(n.tag) in {'camelContext', 'routeContext', 'routeTemplateContext', 'routes', 'route'} for n in nodes):
        inv = Inventory('camel-spring-xml-exploratory', data)
        categories = {'route': 'route', 'routeTemplate': 'template', 'templatedRoute': 'template_instance',
                      'from': 'input', 'to': 'output', 'toD': 'output', 'bean': 'opaque_logic',
                      'setHeader': 'transform', 'setBody': 'transform', 'log': 'logging',
                      'loadBalance': 'routing', 'failoverLoadBalancer': 'failover', 'roundRobin': 'routing',
                      'choice': 'filter', 'routeContextRef': 'external_reference', 'routeTemplateContextRef': 'external_reference'}
        schemes = {'timer', 'direct', 'mina', 'http', 'https', 'file', 'jdbc', 'sql', 'jms', 'kafka'}
        for node in nodes:
            name = local(node.tag)
            if namespace(node.tag) == CAMEL and name in categories:
                inv.add(name, categories[name])
                if name in {'from', 'to', 'toD'}:
                    scheme = node.get('uri', '').split(':', 1)[0]
                    inv.signals['transport_' + (scheme if scheme in schemes else 'other')] += 1
                    if scheme in {'sql', 'jdbc'}:
                        inv.signals['database_logic_unresolved'] += 1
        return inv.finish()
    if namespace(root.tag) == SYNAPSE and local(root.tag) in {'api', 'proxy', 'endpoint', 'localEntry', 'messageStore', 'messageProcessor', 'sequence'}:
        inv = Inventory('synapse-xml-exploratory', data)
        categories = {'api': 'input', 'proxy': 'input', 'resource': 'route', 'endpoint': 'external_reference',
                      'send': 'output', 'call': 'output', 'respond': 'output', 'log': 'logging',
                      'localEntry': 'configuration', 'messageStore': 'storage', 'messageProcessor': 'scheduling',
                      'filter': 'filter', 'switch': 'filter', 'payloadFactory': 'transform',
                      'dblookup': 'database_logic_unresolved', 'dbreport': 'database_logic_unresolved'}
        for node in nodes:
            name = local(node.tag)
            if namespace(node.tag) == SYNAPSE and name in categories:
                inv.add(name, categories[name])
            if namespace(node.tag) == SYNAPSE and name == 'sql' and node.text:
                inv.sql(node.text)
        return inv.finish()
    if root.tag == f'{{{RHAPSODY}}}Engine':
        inv = Inventory('rhapsody-engine-xml-exploratory', data)
        rhapsody(root, inv)
        return inv.finish()
    if root.tag == 'config' and any(local(k) == 'schemaName' and namespace(k) == 'http://www.orionhealth.com/Rhapsody/IDE' for k in root.attrib):
        inv = Inventory('rhapsody-sql-config-exploratory', data)
        inv.add('configuration', 'configuration')
        rhapsody(root, inv)
        return inv.finish()
    return None


def rhapsody(root, inv):
    for node in root.iter():
        name = local(node.tag)
        if namespace(node.tag) == RHAPSODY and name in {'Route', 'Filter', 'CommPoint'}:
            inv.add(name, {'Route': 'route', 'Filter': 'opaque_logic', 'CommPoint': 'transport'}[name])
        if name == 'sql' and namespace(node.tag) in {'', RHAPSODY} and node.text:
            inv.sql(node.text)
