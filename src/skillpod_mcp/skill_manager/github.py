import os
import re
import tarfile
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Iterable

import requests

GITHUB_URL_RE = re.compile(
    r"^https://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)(?:/tree/(?P<ref>[^/]+)(?P<path>/.*)?)?$"
)

# Security limits
MAX_FILE_BYTES = 1_000_000  # 1MB per file
MAX_TOTAL_BYTES = 10_000_000  # 10MB per directory
EXCLUDE_NAMES = {".git", ".env", ".DS_Store", "__pycache__"}


@dataclass
class ParsedGitHubURL:
    owner: str
    repo: str
    ref: str
    path: str  # leading slash or empty

    @property
    def tarball_url(self) -> str:
        return f"https://api.github.com/repos/{self.owner}/{self.repo}/tarball/{self.ref}"

    @property
    def normalized_path(self) -> str:
        return self.path.lstrip("/")


def parse_github_url(url: str) -> ParsedGitHubURL:
    match = GITHUB_URL_RE.match(url.strip())
    if not match:
        raise ValueError("Unsupported GitHub URL. Use https://github.com/<owner>/<repo>[/tree/<ref>/<path>]")

    owner = match.group("owner")
    repo = match.group("repo")
    ref = match.group("ref") or "main"
    path = match.group("path") or ""

    # Reject traversal
    if ".." in path.split("/"):
        raise ValueError("Path traversal detected in URL")

    return ParsedGitHubURL(owner=owner, repo=repo, ref=ref, path=path)


def _iter_members_for_prefix(tar: tarfile.TarFile, prefix: str) -> Iterable[tarfile.TarInfo]:
    for member in tar.getmembers():
        if not member.name.startswith(prefix):
            continue
        # Strip prefix
        member.name = member.name[len(prefix) :].lstrip("/")
        yield member


def download_tarball(parsed: ParsedGitHubURL, token: Optional[str]) -> Path:
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    resp = requests.get(parsed.tarball_url, headers=headers, stream=True, timeout=60)
    if resp.status_code == 404:
        raise ValueError("Repository not found or private. Set GITHUB_TOKEN for private repos.")
    if resp.status_code == 403:
        raise ValueError("GitHub API rate limit. Set GITHUB_TOKEN.")
    if not resp.ok:
        raise ValueError(f"Failed to fetch tarball: HTTP {resp.status_code}")

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".tar.gz")
    total = 0
    try:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                total += len(chunk)
                if total > MAX_TOTAL_BYTES:
                    raise ValueError("Repository exceeds 10MB limit")
                tmp.write(chunk)
        tmp.flush()
        return Path(tmp.name)
    finally:
        tmp.close()


def extract_tarball(tar_path: Path, parsed: ParsedGitHubURL) -> Path:
    target_prefix: Optional[str] = None
    dest_root = Path(tempfile.mkdtemp(prefix="skillpod-gh-"))

    with tarfile.open(tar_path, "r:gz") as tar:
        # Find root folder name first (owner-repo-commit)
        roots = set(member.name.split("/")[0] for member in tar.getmembers() if member.name)
        if not roots:
            raise ValueError("Tarball is empty")
        root = sorted(roots)[0]
        prefix = f"{root}/{parsed.normalized_path}".rstrip("/")

        if parsed.normalized_path:
            target_prefix = prefix + "/"
        else:
            target_prefix = f"{root}/"

        total_bytes = 0
        for member in _iter_members_for_prefix(tar, target_prefix):
            if not member.name:
                continue
            parts = Path(member.name).parts
            if any(p in EXCLUDE_NAMES or p.startswith(".") for p in parts):
                continue

            if member.islnk() or member.issym():
                raise ValueError(f"Symlinks are not allowed in GitHub source: {member.name}")

            dest_path = dest_root / member.name
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            if member.isdir():
                dest_path.mkdir(parents=True, exist_ok=True)
                continue

            if member.size > MAX_FILE_BYTES:
                raise ValueError(f"File too large (>1MB): {member.name}")

            extracted = tar.extractfile(member)
            if not extracted:
                continue
            data = extracted.read()
            total_bytes += len(data)
            if total_bytes > MAX_TOTAL_BYTES:
                raise ValueError("Extracted content exceeds 10MB limit")
            with open(dest_path, "wb") as f:
                f.write(data)

    return dest_root


def fetch_github_source(url: str) -> Path:
    """Download and extract a GitHub source, returning a temp directory path."""
    parsed = parse_github_url(url)
    token = os.getenv("GITHUB_TOKEN")
    tar_path = download_tarball(parsed, token)
    try:
        extracted = extract_tarball(tar_path, parsed)
        return extracted
    finally:
        try:
            tar_path.unlink(missing_ok=True)
        except Exception:
            pass
