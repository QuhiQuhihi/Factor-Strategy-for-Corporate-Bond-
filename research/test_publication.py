"""Publication boundaries tested with small synthetic files in temporary repositories."""
import contextlib
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import zipfile

import check_publication as publication


class PublicationChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="bond-publication-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)/"repo"
        self.root.mkdir()
        self.git("init", "--quiet", "-b", "main")
        self.patch = patch.object(publication, "ROOT", self.root)
        self.patch.start()
        self.addCleanup(self.patch.stop)
        self.write("README.md", "# Synthetic publication fixture\n")
        self.write(".gitignore", "private/\n")
        self.git("add", ".")
        self.commit()

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.root, check=True, capture_output=True)

    def commit(self):
        self.git("-c", "user.name=Publication Test", "-c", "user.email=test@example.invalid",
                 "commit", "--quiet", "-m", "Synthetic test fixture")

    def write(self, name, text):
        path = self.root/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def test_tracked_ignored_file_is_rejected(self):
        self.write("private/sample.csv", "synthetic,value\na,1\n")
        self.git("add", "-f", "private/sample.csv")
        with self.assertRaisesRegex(SystemExit, "Tracked file matches an exclusion"):
            publication.audit()

    def test_document_link_to_ignored_file_is_rejected(self):
        self.write("private/sample.csv", "synthetic,value\na,1\n")
        self.write("README.md", "[Unpublished input](private/sample.csv)\n")
        with self.assertRaisesRegex(SystemExit, "link target is absent"):
            publication.audit()

    def test_export_includes_public_files_only_and_valid_checksums(self):
        self.write("private/sample.csv", "synthetic,value\na,1\n")
        destination = Path(self.temp.name)/"export"
        with contextlib.redirect_stdout(io.StringIO()):
            files = publication.audit()
            publication.export(files, destination)
        hashes = json.loads((destination/"SHA256SUMS.json").read_text())
        with zipfile.ZipFile(destination/"public-research.zip") as archive:
            self.assertEqual(set(archive.namelist()), {"public-research/README.md", "public-research/.gitignore"})
            for name, digest in hashes.items():
                self.assertEqual(hashlib.sha256(archive.read("public-research/"+name)).hexdigest(), digest)

    def test_deleted_historical_input_is_still_detected(self):
        with contextlib.redirect_stdout(io.StringIO()):
            publication.check_history()
        name = publication.HISTORY_RISK_PATHS[1]
        self.write(name, "synthetic,value\na,1\n")
        self.git("add", name)
        self.commit()
        self.git("rm", name)
        self.commit()
        self.assertFalse((self.root/name).exists())
        with self.assertRaisesRegex(SystemExit, "remain in reachable Git history"):
            publication.check_history()

    def test_symlink_is_rejected_before_reading_target(self):
        (self.root/"linked.md").symlink_to(Path(self.temp.name)/"not-read.md")
        with self.assertRaisesRegex(SystemExit, "missing file or symlink requires review"):
            publication.audit()


if __name__ == "__main__":
    unittest.main()
