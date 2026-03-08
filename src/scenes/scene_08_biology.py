"""Scene 8: biological context.

Text-card scene about ATP, ribosome, and rate. No molecular geometry.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCENE_ID = "scene_08_biology"


def build(scene_ctx: Dict[str, Any]) -> None:
    style = scene_ctx["style"]
    preset = scene_ctx["preset"]
    fps = scene_ctx.get("fps", 30)
    duration = scene_ctx.get("duration_seconds", 18)

    from src.core.blender_scene import (
        add_text_overlay,
        setup_camera,
        setup_lighting,
        setup_scene,
    )

    setup_scene(preset, style, fps=fps, duration_seconds=duration)
    setup_lighting()

    total_frames = int(fps * duration)

    texts = [
        ("ATP activates amino acids\nfor peptide bond formation", 1, int(total_frames * 0.33)),
        ("Ribosome aligns substrates\nand lowers activation barrier", int(total_frames * 0.37), int(total_frames * 0.7)),
        ("~1 peptide bond formed\nper second per ribosome", int(total_frames * 0.74), total_frames),
    ]

    cam = setup_camera((0, -6, 0), (0, 0, 0), fov_deg=35)

    for text, start_f, end_f in texts:
        obj = add_text_overlay(text, location=(-3.0, 0, 0.3), size=0.22)
        obj.scale = (0, 0, 0)
        obj.keyframe_insert(data_path="scale", frame=max(1, start_f - 1))
        obj.scale = (1, 1, 1)
        obj.keyframe_insert(data_path="scale", frame=start_f + 10)
        obj.keyframe_insert(data_path="scale", frame=max(start_f + 10, end_f - 10))
        obj.scale = (0, 0, 0)
        obj.keyframe_insert(data_path="scale", frame=end_f)
