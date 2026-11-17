"""Package unmodified upstream binaries and matching runtime files."""

import argparse
import shutil
import tempfile
from pathlib import Path


def build_info(sha):
    return (
        "Unofficial Helix master build (not an official Helix release).\n"
        f"Upstream commit: {sha}\n"
        f"Source: https://github.com/helix-editor/helix/tree/{sha}\n"
        f"Source archive: https://github.com/helix-editor/helix/archive/{sha}.tar.gz\n"
        "Helix license: MPL-2.0; see LICENSE.\n"
        "Bundled grammar components retain their upstream licenses.\n"
        "Language servers are not included.\n"
    )


def package_windows(source, output, sha):
    source, output = Path(source), Path(output)
    if not list((source / "runtime/grammars").glob("*.dll")):
        raise RuntimeError("No compiled grammars found; refusing an incomplete package")
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp) / "helix"
        root.mkdir()
        shutil.copy2(source / "target/release/hx.exe", root / "hx.exe")
        shutil.copytree(
            source / "runtime", root / "runtime", ignore=shutil.ignore_patterns("sources")
        )
        shutil.copytree(source / "contrib/completion", root / "completion")
        for name in ("LICENSE", "README.md"):
            shutil.copy2(source / name, root / name)
        (root / "BUILD-INFO.txt").write_text(build_info(sha), encoding="utf-8")
        (root / "INSTALL.txt").write_text(
            "Extract this entire archive. Keep hx.exe and runtime together.\n"
            "Run hx.exe, or add its directory to your user PATH.\n"
            "Check: hx.exe --version and hx.exe --health\n"
            "Language servers must be installed separately.\n",
            encoding="utf-8",
        )
        return Path(shutil.make_archive(str(output / "helix-windows-x64"), "zip", temp))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--sha", required=True)
    args = parser.parse_args()
    print(package_windows(args.source, args.output, args.sha))
