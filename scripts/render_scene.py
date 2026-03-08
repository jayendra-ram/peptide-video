#!/usr/bin/env python3
"""Executed by Blender for each scene.

Wires bpy, loads configs, calls scene build(), then triggers the render.
"""

from __future__ import annotations

import argparse
import importlib
import json
import site
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Ensure user site-packages is on the path (for pyyaml in Blender's Python)
_user_site = site.getusersitepackages()
if _user_site not in sys.path:
    sys.path.append(_user_site)

import yaml  # noqa: E402


def _load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _detect_bpy():
    try:
        import bpy
        return bpy
    except ImportError:
        return None


def parse_args() -> argparse.Namespace:
    # Blender passes its own args before '--'; we only parse ours
    if "--" in sys.argv:
        our_args = sys.argv[sys.argv.index("--") + 1 :]
    else:
        our_args = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--preset", required=True)
    return parser.parse_args(our_args)


def main() -> None:
    args = parse_args()
    preset: Dict[str, Any] = json.loads(args.preset)

    style = _load_yaml(ROOT / "config" / "style.yaml")
    project = _load_yaml(ROOT / "config" / "project.yaml")

    bpy = _detect_bpy()
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find scene duration from project config
    scene_id = args.scene.split(".")[-1]
    duration = next(
        (s["duration_seconds"] for s in project["scenes"] if s["id"] == scene_id),
        10.0,
    )

    scene_ctx: Dict[str, Any] = {
        "preset": preset,
        "output": str(output_dir),
        "style": style,
        "bpy": bpy,
        "duration_seconds": duration,
        "fps": project["project"]["fps"],
    }

    module = importlib.import_module(args.scene)
    module.build(scene_ctx)

    # Trigger Blender render
    if bpy is not None:
        bpy.context.scene.render.filepath = str(output_dir) + "/frame_"
        bpy.ops.render.render(animation=True)
        print(f"[render_scene] Rendered {args.scene} → {output_dir}")
    else:
        print(f"[render_scene] bpy unavailable; data-only run for {args.scene}")


if __name__ == "__main__":
    main()
