#!/usr/bin/env python3
"""Validate independently installable skills and the published collection."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = ("hardy-skill", "skills/hardy-x-review", "skills/hardy-x-writing")


def validate():
    version = (ROOT / "VERSION").read_text().strip()
    assert re.fullmatch(r"\d+\.\d+\.\d+", version), "Invalid release version"
    names = []
    for module in MODULES:
        directory = ROOT / module
        skill = directory / "SKILL.md"
        text = skill.read_text()
        assert text.startswith("---\n"), f"Missing frontmatter: {module}"
        frontmatter = text.split("---", 2)[1]
        match = re.search(r"^name:\s*([a-z0-9-]+)\s*$", frontmatter, re.M)
        assert match, f"Invalid skill name: {module}"
        assert match[1] == directory.name, f"Folder/name mismatch: {module}"
        assert re.search(r"^description:\s*\S", frontmatter, re.M), module
        assert (directory / "agents/openai.yaml").is_file(), module
        assert (directory / "LICENSE").is_file(), f"Missing standalone license: {module}"
        names.append(match[1])
    assert len(names) == len(set(names)), "Duplicate skill names"
    for path in ROOT.rglob("*.md"):
        if "dist" in path.relative_to(ROOT).parts:
            continue
        text = path.read_text()
        assert "/Users/chenhao/" not in text, f"Private path in {path.relative_to(ROOT)}"
        assert not re.search(r"(?:ghp_|github_pat_)[A-Za-z0-9_]{20,}", text), "Credential pattern found"
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", text):
            if "://" in target or target.startswith("#"):
                continue
            relative = target.split("#", 1)[0]
            linked = (path.parent / relative).resolve()
            assert linked.is_relative_to(ROOT), f"Link escapes release: {path.relative_to(ROOT)}"
            assert linked.exists(), f"Missing link {relative} in {path.relative_to(ROOT)}"
            if path.is_relative_to(ROOT / "skills/hardy-x-writing"):
                assert linked.is_relative_to(ROOT / "skills/hardy-x-writing"), "Writing module requires sibling files"
    registry = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    assert registry["metadata"]["version"] == version, "Plugin/release version mismatch"
    assert len(registry["plugins"]) == 1, "Expected a single collection plugin"
    plugin = registry["plugins"][0]
    assert plugin["source"] == "./" and plugin["strict"] is False
    listed = plugin["skills"]
    assert len(listed) == len(set(listed)), "Duplicate plugin registration"
    assert set(listed) == {"./" + value for value in MODULES}, "Registry differs from released modules"
    original = ROOT / "hardy-skill/references/artifact-protocol.md"
    copy = ROOT / "skills/hardy-x-writing/references/artifact-protocol.md"
    assert original.read_bytes() == copy.read_bytes(), "Artifact protocol copies differ"
    assert "x.draft.v1" in original.read_text(), "Missing writing artifact contract"
    return version


if __name__ == "__main__":
    print(f"Hardy-skill {validate()}: skill structure, links, registry and protocol checks passed.")
