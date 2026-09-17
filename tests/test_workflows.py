"""Run with python3 -m unittest discover -s tests -v (requires PyYAML, bash, zstd, jq)."""
import io
import json
import os
from pathlib import Path
import plistlib
import subprocess
import tarfile
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
UPDATE = yaml.safe_load((ROOT / ".github/workflows/update.yml").read_text())
STEPS = UPDATE["jobs"]["bump"]["steps"]


def step(name):
    return next(s["run"] for s in STEPS if s.get("id") == name)


class Workflows(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.pkg = self.root / "srcpkgs/ayugram-desktop"
        self.pkg.mkdir(parents=True)
        self.template = self.pkg / "template"
        self.template.write_text("version=7.0.9\nrevision=3\n")
        self.marker = self.pkg / "qt6_build_version"
        self.marker.write_text("6.11.2\n")
        self.output = self.root / "output"

    def run_script(self, script, **env):
        self.output.write_text("")
        return subprocess.run(
            ["bash", "-e", "-o", "pipefail", "-c", script], cwd=self.root,
            env={**os.environ, "GITHUB_OUTPUT": str(self.output), **env},
            capture_output=True, text=True,
        )

    def update(self, qt="6.11.2", up="7.0.9"):
        return self.run_script(step("update"), QT=qt, UP=up)

    def test_noop(self):
        self.assertEqual(self.update().returncode, 0)
        self.assertEqual(self.output.read_text(), "changed=false\n")
        self.assertIn("revision=3\n", self.template.read_text())

    def test_qt_bump_and_idempotence(self):
        self.template.write_text("version=7.0.9\nrevision=17\n")
        self.assertEqual(self.update(qt="6.12.0").returncode, 0)
        self.assertIn("revision=18\n", self.template.read_text())
        self.assertEqual(self.marker.read_text(), "6.12.0\n")
        self.assertEqual(self.output.read_text(), "changed=true\n")
        self.assertEqual(self.update(qt="6.12.0").returncode, 0)
        self.assertEqual(self.output.read_text(), "changed=false\n")

    def test_upstream_and_simultaneous_changes(self):
        for qt in ("6.11.2", "6.12.0"):
            with self.subTest(qt=qt):
                self.template.write_text("version=7.0.9\nrevision=3\n")
                self.assertEqual(self.update(qt=qt, up="7.1.0").returncode, 0)
                self.assertEqual(self.template.read_text(), "version=7.1.0\nrevision=1\n")
                self.assertEqual(self.marker.read_text(), qt + "\n")
                self.assertEqual(self.output.read_text(), "changed=true\n")

    def test_empty_and_missing_marker(self):
        for missing in (False, True):
            with self.subTest(missing=missing):
                self.template.write_text("version=7.0.9\nrevision=3\n")
                if missing:
                    self.marker.unlink()
                else:
                    self.marker.write_text("\n")
                self.assertEqual(self.update().returncode, 0)
                self.assertIn("revision=4\n", self.template.read_text())
                self.assertEqual(self.marker.read_text(), "6.11.2\n")

    def test_invalid_input_leaves_files_untouched(self):
        before = self.template.read_bytes(), self.marker.read_bytes()
        for qt, up in (("", "7.0.9"), ("6x11x2", "7.0.9"), ("6.11.2", "null")):
            self.assertNotEqual(self.update(qt=qt, up=up).returncode, 0)
            self.assertEqual(before, (self.template.read_bytes(), self.marker.read_bytes()))
            self.assertEqual(self.output.read_text(), "")

    def fetch(self, pkgver="qt6-core-6.11.2_1", tag="v7.0.9", corrupt=False):
        # A dependency mentioning qt6-core precedes the actual package key.
        index = {"aaa": {"run_depends": ["qt6-core>=0"]}, "qt6-core": {"pkgver": pkgver}}
        archive = io.BytesIO()
        with tarfile.open(fileobj=archive, mode="w") as tar:
            for name, data in (("index.plist", index), ("index-meta.plist", {"ignored": True})):
                body = plistlib.dumps(data)
                info = tarfile.TarInfo(name)
                info.size = len(body)
                tar.addfile(info, io.BytesIO(body))
        compressed = subprocess.run(["zstd", "-q", "-c"], input=archive.getvalue(), capture_output=True, check=True).stdout
        (self.root / "repodata").write_bytes(b"broken" if corrupt else compressed)
        (self.root / "release").write_text(json.dumps({"tag_name": tag}))
        binpath = self.root / "bin"
        binpath.mkdir(exist_ok=True)
        curl = binpath / "curl"
        curl.write_text('#!/usr/bin/env python3\nimport pathlib,sys\na=sys.argv\nif "-o" in a: pathlib.Path(a[a.index("-o")+1]).write_bytes(pathlib.Path("repodata").read_bytes())\nelse: print(pathlib.Path("release").read_text())\n')
        curl.chmod(0o755)
        return self.run_script(step("versions"), PATH=str(binpath) + os.pathsep + os.environ["PATH"])

    def test_actual_fetch_script(self):
        result = self.fetch()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.output.read_text(), "qt6=6.11.2\nupstream=7.0.9\n")

    def test_bad_fetch_cannot_emit_versions(self):
        for kwargs in ({"pkgver": "qt6-core-6x11x2_1"}, {"corrupt": True}, {"tag": None}):
            with self.subTest(kwargs=kwargs):
                self.assertNotEqual(self.fetch(**kwargs).returncode, 0)
                self.assertEqual(self.output.read_text(), "")

    def test_installed_qt_guard(self):
        build = yaml.safe_load((ROOT / ".github/workflows/build.yml").read_text())
        script = next(s["run"] for s in build["jobs"]["build"]["steps"]
                      if s.get("name") == "Install Qt6 build guard")
        hook = script.split("<<'EOF'\n", 1)[1].rsplit("\nEOF", 1)[0]
        shim = """
        msg_error() { printf '%b' "$1" >&2; exit 1; }
        msg_normal() { printf '%b' "$1"; }
        xbps-query() {
            [ "$*" = "-r / -p pkgver qt6-core" ] || exit 99
            [ "$PKG" != missing ] || return 1
            printf '%s\\n' "$PKG"
        }
        """
        for pkg, success in (("qt6-core-6.11.2_9", True),
                             ("qt6-core-6.10.0_1", False), ("missing", False), ("", False)):
            with self.subTest(pkg=pkg):
                result = self.run_script(shim + hook + "\nhook", PKG=pkg,
                                         pkgname="ayugram-desktop", XBPS_MASTERDIR="/",
                                         XBPS_SRCPKGDIR=str(self.pkg.parent))
                self.assertEqual(result.returncode == 0, success, result.stderr)
        self.marker.write_text("")
        self.assertNotEqual(self.run_script(shim + hook + "\nhook", PKG="qt6-core-6.11.2_1",
                            pkgname="ayugram-desktop", XBPS_MASTERDIR="/",
                            XBPS_SRCPKGDIR=str(self.pkg.parent)).returncode, 0)

    def test_workflow_wiring(self):
        triggers = UPDATE.get("on", UPDATE.get(True))  # PyYAML uses YAML 1.1 booleans.
        self.assertEqual(set(triggers), {"schedule", "workflow_dispatch"})
        checkout = next(s for s in STEPS if s.get("uses", "").startswith("actions/checkout@"))
        self.assertEqual(checkout["with"]["token"], "$" + "{{ secrets.BOT_PAT }}")
        commit = STEPS[-1]
        self.assertEqual(commit["if"], "steps.update.outputs.changed == 'true'")
        self.assertIn("git add -A", commit["run"])
        self.assertNotIn("[skip ci]", commit["run"])


if __name__ == "__main__":
    unittest.main()
