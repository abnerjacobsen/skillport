import tarfile
import io
from pathlib import Path

import pytest

from skillhub_mcp.skill_manager.github import (
    parse_github_url,
    extract_tarball,
    ParsedGitHubURL,
)


def _make_tar(tmp_path: Path, structure: dict) -> Path:
    """Create a tar.gz with given structure under root folder."""
    tar_path = tmp_path / "repo.tar.gz"
    root = "owner-repo-sha"
    with tarfile.open(tar_path, "w:gz") as tar:
        for rel, content in structure.items():
            full_name = f"{root}/{rel}"
            data = content.encode("utf-8")
            info = tarfile.TarInfo(full_name)
            info.size = len(data)
            tar.addfile(info, fileobj=io.BytesIO(data))
    return tar_path


def test_parse_github_url_root_defaults_to_main():
    parsed = parse_github_url("https://github.com/user/repo")
    assert parsed.owner == "user"
    assert parsed.repo == "repo"
    assert parsed.ref == "main"
    assert parsed.normalized_path == ""


def test_parse_github_url_with_ref_and_path():
    parsed = parse_github_url("https://github.com/user/repo/tree/feat/skills/path")
    assert parsed.ref == "feat"
    assert parsed.normalized_path == "skills/path"


def test_parse_github_url_rejects_traversal():
    with pytest.raises(ValueError):
        parse_github_url("https://github.com/user/repo/tree/main/../secret")


def test_extract_tarball_subpath(tmp_path):
    structure = {
        "skills/a/SKILL.md": "---\nname: a\n---\nbody",
        "skills/b/SKILL.md": "---\nname: b\n---\nbody",
    }
    tar_path = _make_tar(tmp_path, structure)
    parsed = ParsedGitHubURL(owner="user", repo="repo", ref="main", path="/skills")

    dest = extract_tarball(tar_path, parsed)

    assert (dest / "a" / "SKILL.md").exists()
    assert (dest / "b" / "SKILL.md").exists()


def test_extract_tarball_rejects_symlink(tmp_path):
    tar_path = tmp_path / "repo.tar.gz"
    root = "owner-repo-sha"
    with tarfile.open(tar_path, "w:gz") as tar:
        info = tarfile.TarInfo(f"{root}/skills/link")
        info.type = tarfile.SYMTYPE
        info.linkname = "evil"
        tar.addfile(info)

    parsed = ParsedGitHubURL(owner="user", repo="repo", ref="main", path="/skills")
    with pytest.raises(ValueError):
        extract_tarball(tar_path, parsed)
