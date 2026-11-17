import importlib.util
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "package.py"
spec = importlib.util.spec_from_file_location("package", SCRIPT)
package = importlib.util.module_from_spec(spec)
spec.loader.exec_module(package)


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "upstream"
        files = {
            "target/release/hx.exe": "binary",
            "runtime/grammars/rust.dll": "compiled grammar",
            "runtime/grammars/sources/rust/parser.c": "excluded source",
            "runtime/queries/rust/highlights.scm": "query",
            "runtime/themes/default.toml": "theme",
            "contrib/completion/hx.ps1": "completion",
            "LICENSE": "MPL-2.0",
            "README.md": "upstream readme",
        }
        for name, contents in files.items():
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(contents, encoding="utf-8")

    def test_windows_zip_is_portable_and_excludes_grammar_sources(self):
        archive = package.package_windows(self.source, self.root / "dist", "a" * 40)
        with zipfile.ZipFile(archive) as bundle:
            names = bundle.namelist()
            self.assertIn("helix/hx.exe", names)
            self.assertIn("helix/runtime/grammars/rust.dll", names)
            self.assertIn("helix/runtime/queries/rust/highlights.scm", names)
            self.assertIn("helix/LICENSE", names)
            self.assertFalse(any("grammars/sources" in name for name in names))
            self.assertIn("a" * 40, bundle.read("helix/BUILD-INFO.txt").decode())
        self.assertTrue((self.source / "runtime/grammars/sources/rust/parser.c").exists())

    def test_missing_compiled_grammars_is_an_error(self):
        (self.source / "runtime/grammars/rust.dll").unlink()
        with self.assertRaisesRegex(RuntimeError, "compiled grammars"):
            package.package_windows(self.source, self.root / "dist", "a" * 40)

    def test_build_info_includes_exact_source_and_no_local_paths(self):
        info = package.build_info("b" * 40)
        self.assertIn("https://github.com/helix-editor/helix/tree/" + "b" * 40, info)
        self.assertIn("Unofficial", info)
        self.assertNotIn(str(self.root), info)


if __name__ == "__main__":
    unittest.main()
