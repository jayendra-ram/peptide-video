#!/usr/bin/env python3
"""Batch render every storyboarded scene via Manim CLI."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.io.manim_runner import ManimRunner  # noqa: E402


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render all scenes with Manim")
    parser.add_argument(
        "--quality",
        default="preview",
        choices=["preview", "medium", "final"],
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_config = load_yaml(ROOT / "config" / "project.yaml")
    render_config = load_yaml(ROOT / "config" / "render.yaml")

    quality_flag = (
        render_config.get("manim", {})
        .get("quality_presets", {})
        .get(args.quality, {})
        .get("quality", "-qm")
    )

    scenes = project_config["scenes"]
    project_meta = project_config["project"]
    output_root = ROOT / project_meta["output_root"]
    shots_root = output_root / "shots"
    shots_root.mkdir(parents=True, exist_ok=True)

    runner = ManimRunner(ROOT)

    for idx, scene in enumerate(scenes, 1):
        scene_id = scene["id"]
        duration = scene["duration_seconds"]
        print(f"\n{'='*60}")
        print(f"[{idx}/{len(scenes)}] Rendering {scene_id} ({duration}s)")
        print(f"{'='*60}")

        shot_path = shots_root / f"{scene_id}.mp4"
        runner.render_scene(scene_id, shot_path, quality=quality_flag)


if __name__ == "__main__":
    main()
