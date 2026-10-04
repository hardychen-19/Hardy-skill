#!/usr/bin/env python3
"""Build allowlisted skill ZIPs without user data or optional local settings."""
import zipfile
from pathlib import Path

from validate import ILLUSTRATION_ASSETS, MODULES, ROOT, validate


def skill_files(directory):
    for path in sorted(directory.rglob("*")):
        if path.is_file() and path.name != ".DS_Store" and "__pycache__" not in path.parts:
            if path.name == "LICENSE" or path.suffix in {".md", ".yaml"} or path in ILLUSTRATION_ASSETS:
                yield path


def write_archive(destination, files, relative_to):
    entries = []
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            name = str(path.relative_to(relative_to))
            archive.write(path, name)
            entries.append(name)
    with zipfile.ZipFile(destination) as archive:
        assert archive.testzip() is None, "Corrupt archive"
        assert len(archive.namelist()) == len(set(entries)), "Duplicate archive entry"
        assert set(archive.namelist()) == set(entries), "Archive contents differ"
        assert not any("EXTEND.md" in name or "sources/" in name or "artifacts/" in name for name in entries)
    print(destination.name)


def main():
    version = validate()
    output = ROOT / "dist"
    output.mkdir(exist_ok=True)
    bundle = []
    for module in MODULES:
        directory = ROOT / module
        files = list(skill_files(directory))
        write_archive(output / f"{directory.name}-{version}.zip", files, directory.parent)
        bundle.extend(files)
    bundle.extend(ROOT / name for name in ("README.md", "RELEASE.md", "VERSION", "LICENSE", ".claude-plugin/marketplace.json"))
    bundle.extend(ROOT / "scripts" / name for name in ("validate.py", "package.py"))
    write_archive(output / f"Hardy-skill-bundle-{version}.zip", bundle, ROOT)


if __name__ == "__main__":
    main()
