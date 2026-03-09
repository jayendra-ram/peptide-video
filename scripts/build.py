#!/usr/bin/env python3
"""Build preproduction assets: timeline cue sheet and subtitles."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.script_parser import parse_script  # noqa: E402
from src.core.timeline import TimelineBuilder  # noqa: E402
from src.io.subtitle_writer import write_srt  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build timeline + subtitles from script.md")
    parser.add_argument("project_dir", type=Path, help="Path to the project directory")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_dir = args.project_dir if args.project_dir.is_absolute() else ROOT / args.project_dir
    script_path = project_dir / "script.md"

    scenes = parse_script(script_path)
    builder = TimelineBuilder(scenes)
    cues = builder.build()

    output_dir = project_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    timeline_path = output_dir / "timeline.json"
    builder.export_json(cues, timeline_path)

    subtitle_path = output_dir / "captions.srt"
    write_srt(cues, subtitle_path)

    print(f"Timeline written to {timeline_path}")
    print(f"Subtitles written to {subtitle_path}")


if __name__ == "__main__":
    main()
