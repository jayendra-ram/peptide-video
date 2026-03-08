#!/usr/bin/env python3
"""Batch render every storyboarded scene via Blender CLI."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.io.blender_runner import BlenderRunner  # noqa: E402
from src.io.ffmpeg_runner import FFMpegRunner  # noqa: E402
from src.io.placeholder_renderer import PlaceholderRenderer  # noqa: E402


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render all scenes")
    parser.add_argument(
        "--quality", default="preview", choices=["eevee", "preview", "final"]
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_config = load_yaml(ROOT / "config" / "project.yaml")
    render_config = load_yaml(ROOT / "config" / "render.yaml")
    style_config = load_yaml(ROOT / "config" / "style.yaml")
    preset = render_config["render_presets"].get(args.quality)
    if not preset:
        raise SystemExit(f"Unknown quality preset {args.quality}")

    scenes = project_config["scenes"]
    project_meta = project_config["project"]
    output_root = ROOT / project_meta["output_root"]
    frames_root = output_root / "frames"
    shots_root = output_root / "shots"
    shots_root.mkdir(parents=True, exist_ok=True)

    blender_exec = render_config["blender"]["executable"]
    blender_available = shutil.which(blender_exec) is not None

    fps = project_meta["fps"]
    crf = 18 if args.quality == "final" else 23

    if blender_available:
        runner = BlenderRunner(render_config["blender"], ROOT)
        ffmpeg = FFMpegRunner(render_config["ffmpeg"]["executable"])

        total_scenes = len(scenes)
        for idx, scene in enumerate(scenes, 1):
            module = f"src.scenes.{scene['id']}"
            scene_frames = frames_root / scene["id"]
            print(f"\n{'='*60}")
            print(f"Rendering {scene['id']} ({scene['duration_seconds']}s)")
            print(f"{'='*60}")

            runner.render_scene(
                scene_module=module, output_dir=scene_frames, preset=preset
            )

            # Convert frame sequence to shot MP4 with scene label
            shot_path = shots_root / f"{scene['id']}.mp4"
            scene_label = f"{idx}/{total_scenes}"
            ffmpeg.frames_to_shot(
                scene_frames, shot_path, fps=fps, crf=crf,
                scene_label=scene_label,
            )
            print(f"Shot saved: {shot_path}")
    else:
        placeholder = PlaceholderRenderer(
            ffmpeg=render_config["ffmpeg"]["executable"],
            resolution=project_meta["resolution"],
            fps=fps,
            background=style_config["colors"]["background"],
            fontfile=style_config["fonts"].get("primary"),
        )
        for scene in scenes:
            output_path = shots_root / f"{scene['id']}.mp4"
            placeholder.render_scene(scene, output_path)
        print(
            "Blender not found; rendered placeholder storyboard shots instead."
        )


if __name__ == "__main__":
    main()
