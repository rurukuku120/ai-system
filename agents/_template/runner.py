#!/usr/bin/env python3
"""Template agent runner."""

from __future__ import annotations

import argparse
import json


def main() -> None:
    parser = argparse.ArgumentParser(description="Template Agent")
    parser.add_argument("--dry-run", action="store_true", help="Validate without side effects")
    args = parser.parse_args()

    result = {
        "agent": "template-agent",
        "dry_run": args.dry_run,
        "status": "ok",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
