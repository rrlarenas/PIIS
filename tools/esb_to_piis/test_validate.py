import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import io
import zipfile

import validate
from defusedxml.common import DefusedXmlException


class ValidationTests(unittest.TestCase):
    def test_new_adapters_do_not_disclose_identifiers(self):
        fixtures = [
            (b'<mappingRoot xmlns="http://www.ibm.com/2008/ccl/Mapping" name="SECRET"/>', '.map', 'ibm-map'),
            (b'CREATE FILTER MODULE SECRET CREATE FUNCTION Main() RETURNS BOOLEAN BEGIN RETURN TRUE; END; END MODULE;', '.esql', 'ibm-esql'),
            (b'<beans xmlns:c="http://camel.apache.org/schema/spring"><c:camelContext><c:route id="SECRET"><c:from uri="http://SECRET:123/a?password=SECRET"/><c:bean ref="SECRET"/></c:route></c:camelContext></beans>', '.xml', 'camel-spring'),
            (b'<api xmlns="http://ws.apache.org/ns/synapse" name="SECRET"><resource><dblookup><statement><sql>SELECT SECRET_FIELD FROM SECRET_TABLE WHERE SECRET_FIELD = \'SECRET\'</sql></statement></dblookup></resource></api>', '.xml', 'synapse'),
            (b'<e:EPackage xmlns:e="http://www.eclipse.org/emf/2002/Ecore" xmlns:xmi="http://www.omg.org/XMI"><eClassifiers xmi:type="eflow:FCMComposite"><composition><nodes xmi:id="SECRET" xmi:type="eflow:FCMSource"/><nodes xmi:id="OTHER" xmi:type="eflow:FCMSink"/><connections sourceNode="SECRET" targetNode="OTHER"/></composition></eClassifiers></e:EPackage>', '.msgflow', 'ibm-flow'),
        ]
        for data, suffix, expected in fixtures:
            with self.subTest(expected=expected):
                inventory, findings = validate.inspect_export(data, suffix)
                self.assertTrue(inventory['profile'].startswith(expected))
                self.assertNotIn('SECRET', json.dumps([inventory, findings]))
                self.assertGreater(inventory['component_count'], 0)

    def test_sql_references_and_esql_message_tree(self):
        from adapters import Inventory
        inv = Inventory('test', b'')
        inv.sql('SELECT TOP (1) private_col FROM private_table WHERE private_time >= DATEADD(HOUR, -1, GETDATE()) ORDER BY private_time DESC')
        inv.sql('INSERT INTO private_table (private_col) VALUES ($private_value)')
        inv.sql('SELECT a.x FROM a JOIN b ON a.x=b.x')
        report, _ = inv.finish()
        read, write, ambiguous = report['sql_evidence']
        self.assertEqual(read['tables'], write['tables'])
        self.assertEqual(read['fields'][0], write['fields'][0])
        self.assertEqual(len(read['fields']), 2)
        self.assertEqual(ambiguous['coverage'], 'UNRESOLVED')
        self.assertNotIn('private', json.dumps(report))
        report, _ = validate.inspect_export(b'CREATE COMPUTE MODULE private_module SET OutputRoot = InputRoot; END MODULE;', '.esql')
        self.assertEqual(report['sql_evidence'], [])

    def test_sql_complex_inputs_stay_unresolved(self):
        from adapters import Inventory
        for query in ['SELECT a.x FROM a, b WHERE a.x=b.x',
                      'SELECT x FROM a; DELETE FROM b',
                      'WITH c AS (SELECT x FROM a) SELECT x FROM c']:
            inv = Inventory('test', b'')
            inv.sql(query)
            record = inv.report['sql_evidence'][0]
            self.assertEqual(record['coverage'], 'UNRESOLVED')
            self.assertEqual(record['tables'], [])

    def test_rhapsody_standalone_config(self):
        data = b'<config xmlns:i="http://www.orionhealth.com/Rhapsody/IDE" i:schemaName="SECRET"><sql>SELECT SECRET_FIELD FROM SECRET_TABLE</sql></config>'
        report, _ = validate.inspect_export(data)
        self.assertEqual(report['profile'], 'rhapsody-sql-config-exploratory')
        self.assertEqual(report['sql_evidence'][0]['tables'], ['table-0001'])
        self.assertNotIn('SECRET', json.dumps(report))

    def test_generated_cases_and_sql_privacy(self):
        root = validate.SCHEMA.parents[2]
        base = root / 'experiments/esb-multiengine-anonymized-06'
        report = json.loads((base / 'comparison_report.json').read_text(encoding='utf-8'))
        self.assertEqual(sum(c['artifacts'] for c in report['cases']), 27)
        self.assertEqual(report['functional_equivalence'], 'NOT_TESTED')
        for path in base.glob('case-*/*.json'):
            data = json.loads(path.read_text(encoding='utf-8'))
            if 'queries' not in data:
                continue
            for query in data['queries']:
                for table in query['tables']:
                    self.assertRegex(table, r'^table-\d{4}$')
                for field in query['fields']:
                    self.assertRegex(field['field_ref'], r'^field-\d{4}$')
                    self.assertIn(field['table_ref'], query['tables'])

    def test_rlc_archive_and_safety(self):
        def archive(files):
            stream = io.BytesIO()
            with zipfile.ZipFile(stream, 'w') as z:
                for name, data in files:
                    z.writestr(name, data)
            return stream.getvalue()
        engine = b'<Engine xmlns="urn:www.yourcompany.com/Rhapsody/Schema.xml"><Route><ID>SECRET</ID></Route></Engine>'
        config = b'<config xmlns:i="http://www.orionhealth.com/Rhapsody/IDE" i:schemaName="SECRET"><statement><sql>INSERT INTO SECRET_TABLE (SECRET_FIELD) VALUES (\'SECRET\')</sql></statement></config>'
        data = archive([('SECRET.xml', engine), ('SECRET/query.xml', config)])
        report, findings = validate.inspect_export(data)
        self.assertEqual(report['signals']['sql_write_candidate'], 1)
        self.assertNotIn('SECRET', json.dumps([report, findings]))
        for files in [[('x.xml', b'<unrelated/>')], [('x.xml', engine), ('nested.zip', b'PK')],
                      [('x.xml', engine), ('bad.xml', b'<!DOCTYPE config><config/>')]]:
            with self.assertRaises((ValueError, DefusedXmlException)):
                validate.inspect_export(archive(files))
        with self.assertRaises(zipfile.BadZipFile):
            validate.inspect_export(b'PKbroken')

    def test_pinned_public_artifacts(self):
        root = validate.SCHEMA.parents[2]
        manifest = json.loads((root / 'samplesESB/manifest.json').read_text(encoding='utf-8'))
        profiles = set()
        for source in manifest['sources']:
            for entry in source['files']:
                path = root / 'samplesESB' / entry['path']
                if path.suffix in {'.rlc', '.msgflow', '.subflow', '.esql', '.map', '.xml'} and path.name not in {'pom.xml', 'build.xml'}:
                    inventory, _ = validate.inspect_export(path.read_bytes(), path.suffix)
                    profiles.add(inventory['profile'])
        self.assertEqual(len(profiles), 6)

    def test_public_evidence(self):
        base = validate.SCHEMA.parents[2] / "experiments/esb-a-esb-b-hl7-01"
        for name in ("ESB-A", "ESB-B"):
            inventory, findings = validate.inspect_export((base / f"{name}_export_redacted.xml").read_bytes())
            self.assertGreater(inventory["component_count"], 0)
            self.assertIn("REDACTED_SOURCE", [f["code"] for f in findings])

    def test_native_profiles_and_namespace(self):
        for xml, expected in ((b'<list xmlns="urn:test"><channel><script>SECRET</script></channel></list>',
                               "channel-xml-exploratory"),
                              (b'<Export><Class name="SECRET"/></Export>', "class-export-xml-exploratory")):
            inventory, findings = validate.inspect_export(xml)
            self.assertEqual(inventory["profile"], expected)
            self.assertNotIn("SECRET", json.dumps([inventory, findings]))

    def test_unknown_and_unsafe_xml(self):
        with self.assertRaises(ValueError):
            validate.inspect_export(b"<unrelated/>")
        with self.assertRaises(DefusedXmlException):
            validate.inspect_export(b'<!DOCTYPE channel [<!ENTITY x "secret">]><channel>&x;</channel>')

    def test_schema_and_negative(self):
        sample = validate.SCHEMA.parents[2] / "samples/clinical-dft-draft01/PIIS_PFD_DFT_DRAFT01.json"
        result, document = validate.validate_pfd(sample.read_bytes())
        self.assertEqual(result["status"], "VALID")
        del document["BehaviorContract"]
        result, _ = validate.validate_pfd(json.dumps(document).encode())
        self.assertEqual(result["status"], "INVALID")

    def test_json_rejects_duplicates_and_nan(self):
        for data in (b'{"a":1,"a":2}', b'{"a":NaN}'):
            with self.assertRaises(ValueError):
                validate.load_json(data)

    def test_cli_exit_codes_and_preserve_input(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "source.xml"
            pfd = Path(directory) / "pfd.json"
            source.write_text("<channel/>", encoding="utf-8")
            pfd.write_text("{}", encoding="utf-8")
            command = [sys.executable, str(Path(validate.__file__)), str(source)]
            for extra, expected in (([], 0), (["--piis", str(pfd)], 1),
                                    (["--output", str(source)], 2)):
                result = subprocess.run(command + extra, capture_output=True, text=True)
                self.assertEqual(result.returncode, expected, result.stderr)
            self.assertEqual(source.read_text(encoding="utf-8"), "<channel/>")
            source.write_text("<unknown/>", encoding="utf-8")
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)["findings"][0]["code"], "INPUT_ERROR")


if __name__ == "__main__":
    unittest.main()
