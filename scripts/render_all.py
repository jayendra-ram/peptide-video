#!/usr/bin/env python3
"""Batch render every scene using the appropriate renderer backend."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.config import load_config  # noqa: E402
from src.core.script_parser import parse_script  # noqa: E402
from src.io.renderer import RendererRegistry  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render all scenes")
    parser.add_argument("project_dir", type=Path, help="Path to the project directory")
    parser.add_argument(
        "--quality",
        default="preview",
        choices=["preview", "medium", "final"],
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_dir = args.project_dir if args.project_dir.is_absolute() else ROOT / args.project_dir

    scenes = parse_script(project_dir / "script.md")
    render_config = load_config(ROOT, project_dir, "render.yaml")
    style_config = load_config(ROOT, project_dir, "style.yaml")

    quality_flag = (
        render_config.get("manim", {})
        .get("quality_presets", {})
        .get(args.quality, {})
        .get("quality", "-qm")
    )

    shots_root = project_dir / "output" / "shots"
    shots_root.mkdir(parents=True, exist_ok=True)

    registry = RendererRegistry(project_dir, ROOT, render_config, style_config)

    for idx, scene in enumerate(scenes, 1):
        print(f"\n{'='*60}")
        print(f"[{idx}/{len(scenes)}] Rendering {scene.id} ({scene.duration_seconds}s) [{scene.render.type}:{scene.render.ref}]")
        print(f"{'='*60}")

        shot_path = shots_root / f"{scene.id}.mp4"
        registry.render(scene, shot_path, quality=quality_flag)


if __name__ == "__main__":
    main()
