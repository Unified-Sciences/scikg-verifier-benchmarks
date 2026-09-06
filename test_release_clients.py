"""Check that the released clients reject altered artifacts and row coverage."""
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent


class ReleaseClientTests(unittest.TestCase):
    def run_copy(self, mutation):
        source = ROOT / 'benchmarks/matbench_v0.1_SciKG_Verify'
        with tempfile.TemporaryDirectory() as temporary:
            folder = Path(temporary)
            manifest = json.loads((source / 'ARTIFACT_MANIFEST.json').read_text())
            for name in ('ARTIFACT_MANIFEST.json', *manifest['hashes']):
                shutil.copyfile(source / name, folder / name)
            mutation(folder, manifest)
            return subprocess.run([sys.executable, str(folder / 'submission_client.py')],
                                  capture_output=True, text=True)

    def test_original_bundle_passes(self):
        result = self.run_copy(lambda folder, manifest: None)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_changed_bytes_fail(self):
        def change(folder, manifest):
            with (folder / 'statistics.json').open('ab') as handle:
                handle.write(b' ')
        result = self.run_copy(change)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('artifact hash mismatch', result.stderr)

    def test_missing_row_fails_even_with_updated_hash(self):
        def change(folder, manifest):
            path = folder / 'reference.json.gz'
            value = json.loads(gzip.decompress(path.read_bytes()))
            value['fold_0'].pop()
            path.write_bytes(gzip.compress(json.dumps(value).encode(), mtime=0))
            manifest['hashes'][path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
            (folder / 'ARTIFACT_MANIFEST.json').write_text(json.dumps(manifest))
        result = self.run_copy(change)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('row coverage differs', result.stderr)


if __name__ == '__main__':
    unittest.main()
