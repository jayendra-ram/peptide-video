"""Scene 2: introduce amino acid reactants.

Two amino acids separated in 3D. Charge halos on key atoms. Slow camera orbit.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCENE_ID = "scene_02_reactants"


def build(scene_ctx: Dict[str, Any]) -> None:
    style = scene_ctx["style"]
    preset = scene_ctx["preset"]
    fps = scene_ctx.get("fps", 30)
    duration = scene_ctx.get("duration_seconds", 22)

    from src.core.blender_scene import (
        _set_bezier_easing,
        add_charge_halo,
        add_curved_arrow,
        add_text_overlay,
        setup_camera,
        setup_lighting,
        setup_scene,
    )
    from src.chemistry.molecules import (
        GLYCINE_A_REACTANT,
        GLYCINE_B_REACTANT,
        draw_molecule,
    )

    setup_scene(preset, style, fps=fps, duration_seconds=duration)
    setup_lighting()

    import bpy

    total_frames = int(fps * duration)

    # Draw both amino acids
    atoms_a = draw_molecule(
        GLYCINE_A_REACTANT, style, offset=(-1.0, 0, 0), label_prefix="A_"
    )
    atoms_b = draw_molecule(
        GLYCINE_B_REACTANT, style, offset=(0, 0, 0), label_prefix="B_"
    )

    # Partial charge halos
    add_charge_halo(atoms_a["C1"], magnitude=0.35, style=style)
    add_charge_halo(atoms_a["O1"], magnitude=-0.6, style=style)
    add_charge_halo(atoms_b["N2"], magnitude=-0.4, style=style)

    # Curved arrow from N2 toward C1
    n2_pos = tuple(atoms_b["N2"].location)
    c1_pos = tuple(atoms_a["C1"].location)
    arrow = add_curved_arrow(n2_pos, c1_pos, color=(1.0, 0.8, 0.0), arc_height=0.8)
    # Fade arrow in
    arrow.scale = (0, 0, 0)
    arrow.keyframe_insert(data_path="scale", frame=int(fps * 4))
    arrow.scale = (1, 1, 1)
    arrow.keyframe_insert(data_path="scale", frame=int(fps * 5.5))

    # Labels
    add_text_overlay("Amine (nucleophile)", location=(1.5, 0, 1.2), size=0.14)
    add_text_overlay("Carbonyl (electrophile)", location=(-2.5, 0, 1.2), size=0.14)

    # Camera: slow orbit
    cam = setup_camera((0.5, -6, 2.5), (0.5, 0, 0), fov_deg=35)
    for i in range(5):
        frame = 1 + int(i * total_frames / 4)
        angle = i * math.pi / 6
        x = 0.5 + 6 * math.sin(angle)
        y = -6 * math.cos(angle)
        z = 2.5 - 0.3 * i
        cam.location = (x, y, z)
        cam.keyframe_insert(data_path="location", frame=frame)

    _set_bezier_easing(cam)

    # Molecule description
    desc = add_text_overlay(
        "Glycine (C-terminus: -CH2-COOH)  +  Glycine (N-terminus: H2N-CH2-)",
        location=(-4.0, 0, -2.2), size=0.09,
    )
    desc.scale = (0, 0, 0)
    desc.keyframe_insert(data_path="scale", frame=1)
    desc.scale = (1, 1, 1)
    desc.keyframe_insert(data_path="scale", frame=int(fps * 1))
