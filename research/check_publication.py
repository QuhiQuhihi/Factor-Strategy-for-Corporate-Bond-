"""Audit the proposed public working tree; optionally export it without Git history.

This is a limited text-pattern and packaging check, not a rights clearance or a
complete security/history audit. It never prints matched credential values.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
from urllib.parse import unquote
import zipfile

ROOT = Path(__file__).resolve().parents[1]
HISTORY_RISK_PATHS = (
    "(Chapter1)Data/TRACE_DB_link.txt",
    "old/Monthly_Log_Returns.csv",
    "old/analysis.ipynb",
    "(Chapter1)Data/old/OR_factors.ipynb",
)
RETIRED_FILES = {"LEGACY.md", "requirements.txt", "Combined_README.ipynb"}
TEXT_SUFFIXES = {".py", ".ipynb", ".md", ".txt", ".json", ".toml", ".yml", ".yaml", ".sql", ".lock", ".csv"}
SECRET_PATTERNS = {
    "private key": r"-----BEGIN (?:OPENSSH |RSA |EC )?PRIVATE KEY-----",
    "GitHub token": r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,})",
    "AWS access key": r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b",
    "Google API key": r"\bAIza[A-Za-z0-9_-]{30,}",
    "API secret token": r"\bsk-(?:proj-)?[A-Za-z0-9_-]{32,}",
    "Slack token": r"\bxox[baprs]-[A-Za-z0-9-]{20,}",
    "credential assignment": r'''(?i)(?:api[_-]?key|password|passwd|access[_-]?token|client[_-]?secret)\s*[=:]\s*['"][^'"\n]{8,}['"]''',
}


def git_paths(*args: str) -> list[str]:
    result = subprocess.run(["git", *args, "-z"], cwd=ROOT, check=True, capture_output=True)
    return [p for p in result.stdout.decode().split("\0") if p]


def check_links(text: str, base: Path, files: set[str], errors: list[str], owner: str) -> None:
    for target in re.findall(r"!?\[[^\]]*\]\(([^\s)]+)\)", text):
        if target.startswith(("https://", "http://", "mailto:", "#")):
            continue
        try:
            relative = (base/unquote(target.split("#")[0])).resolve().relative_to(ROOT).as_posix()
        except ValueError:
            errors.append(f"{owner}: link escapes repository")
            continue
        if relative not in files and not any(p.startswith(relative.rstrip("/")+"/") for p in files):
            errors.append(f"{owner}: link target is absent from public files: {relative}")


def audit() -> list[str]:
    ignored = set(git_paths("ls-files", "-ci", "--exclude-standard"))
    candidates = sorted(set(git_paths("ls-files", "--cached", "--others", "--exclude-standard")))
    errors = [f"Tracked file matches an exclusion: {p}" for p in sorted(ignored)]
    public = set(candidates)-ignored
    for relative in sorted(public):
        path = ROOT/relative
        if relative in RETIRED_FILES:
            errors.append(f"{relative}: retired artifact must not be published")
        if path.is_symlink() or not path.is_file():
            errors.append(f"{relative}: missing file or symlink requires review")
            continue
        if path.suffix not in TEXT_SUFFIXES and path.name not in {"LICENSE", "NOTICE", ".gitignore"}:
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            errors.append(f"{relative}: unexpected non-UTF-8 text")
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if re.search(pattern, text):
                errors.append(f"{relative}: possible {label}; inspect locally (value withheld)")
        if path.suffix == ".md":
            check_links(text, path.parent, public, errors, relative)
        elif path.suffix == ".ipynb":
            try:
                notebook = json.loads(text)
            except json.JSONDecodeError:
                errors.append(f"{relative}: invalid notebook JSON")
                continue
            for cell in notebook.get("cells", []):
                source = cell.get("source", "")
                if isinstance(source, list):
                    source = "".join(source)
                if cell.get("cell_type") == "markdown":
                    check_links(source, path.parent, public, errors, relative)
                for output in cell.get("outputs", []):
                    if output.get("output_type") == "error":
                        errors.append(f"{relative}: notebook contains an error output")
            if re.search(r"/Users/|/home/|[A-Z]:\\\\Users\\\\", text):
                errors.append(f"{relative}: notebook contains a personal machine path")
    if errors:
        raise SystemExit("Publication checks failed:\n"+"\n".join(errors))
    print(f"Checked {len(public)} proposed public files: no ignored tracked files, broken local document links, or selected credential-pattern matches.")
    print("Scope excludes prior Git history, permissions, binary payload inspection and credentials that do not match these patterns.")
    return sorted(public)


def check_history() -> None:
    shallow = subprocess.run(["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT,
                             check=True, capture_output=True, text=True).stdout.strip()
    if shallow == "true":
        raise SystemExit("History check requires a full clone; shallow history cannot establish absence.")
    exposed = []
    for path in HISTORY_RISK_PATHS:
        result = subprocess.run(["git", "log", "--all", "--format=%H", "--", path],
                                cwd=ROOT, check=True, capture_output=True, text=True)
        if result.stdout.strip():
            exposed.append(path)
    if exposed:
        raise SystemExit("Known restricted paths remain in reachable Git history:\n"+
                         "\n".join(exposed)+
                         "\nUse the history-free export for a new repository, or coordinate a separate history cleanup.")
    print("No known restricted paths found in local reachable history; this is a bounded path check, not a full secret audit.")


def export(files: list[str], destination: Path) -> None:
    destination = destination.resolve()
    if destination.exists():
        raise SystemExit("Export destination already exists; choose a new path to preserve prior exports.")
    destination.mkdir(parents=True)
    tree = destination/"public-research"
    hashes = {}
    for relative in files:
        source, target = ROOT/relative, tree/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        hashes[relative] = hashlib.sha256(target.read_bytes()).hexdigest()
    (destination/"SHA256SUMS.json").write_text(json.dumps(hashes, indent=2)+"\n")
    archive = destination/"public-research.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for relative in files:
            z.write(tree/relative, arcname="public-research/"+relative)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        assert len(z.namelist()) == len(files)
    print(f"Exported {len(files)} working-tree files to {archive}")
    print("Includes reviewed uncommitted files; excludes .git, ignored files and history. Licensing caveats in PUBLICATION.md still apply.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", type=Path, help="Create a new directory containing a history-free tree, ZIP and checksums")
    parser.add_argument("--check-history", action="store_true", help="Fail if known restricted paths remain in full local Git history")
    args = parser.parse_args()
    files = audit()
    if args.check_history:
        check_history()
    if args.export:
        export(files, args.export)


if __name__ == "__main__":
    main()
