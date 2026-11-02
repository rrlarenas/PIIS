import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import validate
from defusedxml.common import DefusedXmlException


class ValidationTests(unittest.TestCase):
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
