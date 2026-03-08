"""Scene 9: summary montage.

Three molecular states side by side with bullet text.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCENE_ID = "scene_09_summary"


def build(scene_ctx: Dict[str, Any]) -> None:
    style = scene_ctx["style"]
    preset = scene_ctx["preset"]
    fps = scene_ctx.get("fps", 30)
    duration = scene_ctx.get("duration_seconds", 15)

    from src.core.blender_scene import (
        add_text_overlay,
        setup_camera,
        setup_lighting,
        setup_scene,
    )
    from src.chemistry.molecules import (
        AMIDE_PRODUCT,
        GLYCINE_A_REACTANT,
        TETRAHEDRAL_TS,
        draw_molecule,
    )

    setup_scene(preset, style, fps=fps, duration_seconds=duration)
    setup_lighting()

    total_frames = int(fps * duration)

    # Three states side by side
    configs = [
        (GLYCINE_A_REACTANT, (-4.5, 0, -0.5), "Reactants"),
        (TETRAHEDRAL_TS, (0.0, 0, -0.5), "Transition State"),
        (AMIDE_PRODUCT, (4.5, 0, -0.5), "Peptide Bond"),
    ]
    for geom, offset, label in configs:
        draw_molecule(geom, style, offset=offset, label_prefix=f"S9_{label[:3]}_")
        add_text_overlay(label, location=(offset[0] - 1.0, 0, -2.2), size=0.12)

    # Animated bullet summaries
    bullets = [
        "Orbital overlap drives nucleophilic attack",
        "Activation barrier requires biological catalysis",
        "Amide resonance enforces backbone planarity",
    ]
    for i, bullet in enumerate(bullets):
        frame_in = int(fps * 1.5) + i * int(fps * 2)
        obj = add_text_overlay(
            bullet, location=(-5.0, 0, 2.0 - i * 0.6), size=0.13
        )
        obj.scale = (0, 0, 0)
        obj.keyframe_insert(data_path="scale", frame=max(1, frame_in - 1))
        obj.scale = (1, 1, 1)
        obj.keyframe_insert(data_path="scale", frame=frame_in + 8)

    cam = setup_camera((0, -12, 2), (0, 0, -0.5), fov_deg=40)


