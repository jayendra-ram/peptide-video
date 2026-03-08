#!/usr/bin/env python3
"""Build preproduction assets: configs, cue sheets, subtitles."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.timeline import TimelineBuilder  # noqa: E402
from src.io.subtitle_writer import write_srt  # noqa: E402


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def main() -> None:
    project_config = load_yaml(ROOT / "config" / "project.yaml")
    builder = TimelineBuilder(project_config)
    cues = builder.build()

    output_dir = ROOT / project_config["project"]["output_root"]
    output_dir.mkdir(parents=True, exist_ok=True)

    timeline_path = output_dir / "timeline.json"
    builder.export_json(cues, timeline_path)

    subtitle_path = output_dir / "captions.srt"
    write_srt(cues, subtitle_path)

    print(f"Timeline written to {timeline_path}")
    print(f"Subtitles written to {subtitle_path}")


if __name__ == "__main__":
    main()
