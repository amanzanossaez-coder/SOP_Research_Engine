#!/usr/bin/env python3
"""
SOP Research Engine
Core Validation Suite

Valida la arquitectura del Core.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


# ==========================================================
# Helpers
# ==========================================================

def exists(relative_path: str) -> bool:
    return (ROOT / relative_path).exists()


def validate(title: str, required: list[str]) -> bool:
    print()
    print(title)
    print("-" * len(title))

    ok = True

    for item in required:
        if exists(item):
            print(f"✓ {item}")
        else:
            print(f"✗ {item}")
            ok = False

    return ok


# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("SOP RESEARCH ENGINE")
    print("CORE VALIDATION SUITE")
    print("=" * 60)

    checks = []

    checks.append(
        validate(
            "Architecture",
            [
                "core",
                "engine",
                "models",
                "loaders",
                "docs",
                "tests",
            ],
        )
    )

    checks.append(
        validate(
            "Core",
            [
                "core/constants.py",
                "core/contracts.py",
                "core/dataset_builder.py",
                "core/normalization.py",
                "core/exceptions.py",
            ],
        )
    )

    checks.append(
        validate(
            "Engines",
            [
                "engine/snapshot_engine.py",
                "engine/similarity_engine.py",
                "engine/validation_harness.py",
                "engine/validation_metrics.py",
                "engine/evidence_engine.py",
                "engine/assessment_engine.py",
                "engine/inference_engine.py",
            ],
        )
    )

    checks.append(
        validate(
            "Models",
            [
                "models/dataset.py",
                "models/episode.py",
                "models/snapshot.py",
                "models/similarity.py",
                "models/evidence.py",
                "models/inference.py",
                "models/confidence.py",
            ],
        )
    )

    checks.append(
        validate(
            "Documentation",
            [
                "docs/CONSTITUTION.md",
                "docs/PROJECT_STATE.md",
                "docs/ROADMAP.md",
                "docs/GOVERNANCE",
                "docs/ARCHITECTURE",
                "docs/RESEARCH",
                "docs/VALIDATION",
            ],
        )
    )

    checks.append(
        validate(
            "Repository",
            [
                ".git",
            ],
        )
    )

    print()
    print("=" * 60)

    passed = sum(checks)
    total = len(checks)

    print(f"Checks passed: {passed}/{total}")

    duplicates = []

    if exists(".git 2"):
        duplicates.append(".git 2")

    if exists(".git 3"):
        duplicates.append(".git 3")

    if duplicates:
        print()
        print("WARNINGS")
        print("--------")

        for item in duplicates:
            print(f"Unexpected directory: {item}")

    print()

    if passed == total:
        print("CORE STATUS : STABLE")
        sys.exit(0)

    print("CORE STATUS : INVALID")
    sys.exit(1)


if __name__ == "__main__":
    main()
