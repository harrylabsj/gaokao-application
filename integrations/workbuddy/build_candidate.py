#!/usr/bin/env python3
"""Build a temporary WorkBuddy ZIP candidate from the allowlisted 1.0.0 source."""

from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = Path(__file__).resolve().parent / "gaokao-advisor-1.0.0"
ARCHIVE_ROOT = "gaokao-advisor"
PACKAGE_FILES = (
    ".codebuddy-plugin/plugin.json",
    "README.md",
    "agents/gaokao-advisor.md",
    "avatars/expert.png",
    "skills/gaokao-application/SKILL.md",
    "skills/gaokao-application/references/data-contract.md",
    "skills/gaokao-application/references/output-templates.md",
    "skills/gaokao-application/references/province-rules.md",
    "skills/gaokao-application/references/risk-policy.md",
    "skills/gaokao-application/references/source-checklist.md",
    "skills/gaokao-application/references/workflow.md",
    "skills/gaokao-application/scripts/normalize_admission_data.py",
    "skills/gaokao-application/scripts/rank_matcher.py",
    "skills/gaokao-application/scripts/risk_scoring.py",
    "skills/gaokao-application/scripts/shortlist_builder.py",
    "skills/gaokao-application/scripts/validate_dataset.py",
)


def validate_package() -> None:
    manifest_path = PACKAGE_ROOT / ".codebuddy-plugin/plugin.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("name") != "gaokao-advisor" or manifest.get("version") != "1.0.0":
        raise SystemExit("Unexpected plugin name or version in plugin.json")

    for relative in PACKAGE_FILES:
        path = PACKAGE_ROOT / relative
        if not path.is_file():
            raise SystemExit(f"Missing allowlisted package file: {relative}")

    for relative in (*manifest.get("agents", []), *manifest.get("skills", [])):
        path = (PACKAGE_ROOT / relative).resolve()
        if not path.is_relative_to(PACKAGE_ROOT.resolve()) or not path.exists():
            raise SystemExit(f"Manifest reference is missing or escapes package: {relative}")


def build(output: Path) -> tuple[Path, str]:
    validate_package()
    output = output.expanduser().resolve()
    try:
        output.relative_to(REPO_ROOT)
    except ValueError:
        pass
    else:
        raise SystemExit("Refusing to write the ZIP inside the Git repository")

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for relative in PACKAGE_FILES:
            info = zipfile.ZipInfo(f"{ARCHIVE_ROOT}/{relative}", date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (PACKAGE_ROOT / relative).read_bytes())

    digest = hashlib.sha256(output.read_bytes()).hexdigest()
    sidecar = output.with_suffix(output.suffix + ".sha256")
    sidecar.write_text(f"{digest}  {output.name}\n", encoding="ascii")
    return output, digest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(tempfile.gettempdir()) / "gaokao-advisor-1.0.0-workbuddy-candidate.zip",
        help="Output ZIP path (must be outside the Git repository).",
    )
    args = parser.parse_args()
    output, digest = build(args.output)
    print(f"Candidate ZIP: {output}")
    print(f"SHA-256: {digest}")
    print(f"Files: {len(PACKAGE_FILES)}")
    print("Identity: locally rebuilt candidate; original platform upload hash unknown")


if __name__ == "__main__":
    main()
