#!/usr/bin/env python3
"""One-button pipeline orchestrator."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build + render + assemble pipeline")
    parser.add_argument("--quality", default="preview", choices=["preview", "medium", "final"])
    parser.add_argument("--skip-render", action="store_true")
    parser.add_argument("--skip-tts", action="store_true")
    parser.add_argument("--tts-dry-run", action="store_true")
    parser.add_argument("--skip-assemble", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    subprocess.run(["python", "scripts/build.py"], check=True, cwd=ROOT)

    if not args.skip_render:
        subprocess.run(["python", "scripts/render_all.py", f"--quality={args.quality}"], check=True, cwd=ROOT)

    if not args.skip_tts:
        cmd = ["python", "scripts/generate_tts.py"]
        if args.tts_dry_run:
            cmd.append("--dry-run")
        subprocess.run(cmd, check=True, cwd=ROOT)

    if not args.skip_assemble:
        subprocess.run(["python", "scripts/assemble_video.py"], check=True, cwd=ROOT)


if __name__ == "__main__":
    main()
