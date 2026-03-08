"""Scene 5: nucleophilic attack.

N2 approaches C1. Atoms animate from reactant to tetrahedral intermediate.
Bonds skipped to avoid static-cylinder artifacts during animation.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCENE_ID = "scene_05_attack"


def build(scene_ctx: Dict[str, Any]) -> None:
    style = scene_ctx["style"]
    preset = scene_ctx["preset"]
    fps = scene_ctx.get("fps", 30)
    duration = scene_ctx.get("duration_seconds", 12)

    from src.core.blender_scene import (
        _set_bezier_easing,
        add_text_overlay,
        animate_camera,
        setup_camera,
        setup_lighting,
        setup_scene,
    )
    from src.chemistry.molecules import (
        GLYCINE_A_REACTANT,
        GLYCINE_B_REACTANT,
        TETRAHEDRAL_TS,
        draw_molecule,
    )

    setup_scene(preset, style, fps=fps, duration_seconds=duration)
    setup_lighting()

    import bpy

    total_frames = int(fps * duration)
    mid_frame = total_frames // 2

    # Draw reactants — skip bonds since atoms will animate
    atoms_a = draw_molecule(
        GLYCINE_A_REACTANT, style, offset=(-0.5, 0, 0), label_prefix="ATK_",
        skip_bonds=True,
    )
    atoms_b = draw_molecule(
        GLYCINE_B_REACTANT, style, offset=(0, 0, 0), label_prefix="ATK_",
        skip_bonds=True,
    )
    all_atoms = {**atoms_a, **atoms_b}

    # Keyframe reactant positions at frame 1
    for label, obj in all_atoms.items():
        obj.keyframe_insert(data_path="location", frame=1)

    # Build TS position lookup
    ts_positions = {label: pos for label, sym, pos in TETRAHEDRAL_TS.atoms}

    # Keyframe TS positions at mid_frame
    for label, obj in all_atoms.items():
        if label in ts_positions:
            obj.location = ts_positions[label]
            obj.keyframe_insert(data_path="location", frame=mid_frame)

    # Ease all keyframes
    for label, obj in all_atoms.items():
        _set_bezier_easing(obj)

    # Labels
    label_obj = add_text_overlay(
        "Nucleophilic Attack", location=(-2.5, 0, 2.5), size=0.18
    )
    label_obj.scale = (0, 0, 0)
    label_obj.keyframe_insert(data_path="scale", frame=1)
    label_obj.scale = (1, 1, 1)
    label_obj.keyframe_insert(data_path="scale", frame=int(fps * 0.5))
    label_obj.keyframe_insert(data_path="scale", frame=int(fps * 4))
    label_obj.scale = (0, 0, 0)
    label_obj.keyframe_insert(data_path="scale", frame=int(fps * 5))

    # Molecule description
    desc = add_text_overlay(
        "Gly-COOH + H2N-Gly  -->  tetrahedral intermediate",
        location=(-3.5, 0, -2.2), size=0.10,
    )
    desc.scale = (0, 0, 0)
    desc.keyframe_insert(data_path="scale", frame=1)
    desc.scale = (1, 1, 1)
    desc.keyframe_insert(data_path="scale", frame=int(fps * 1))

    # Camera: follow the approach
    cam = setup_camera((1, -6, 2), (0.3, 0, -0.2), fov_deg=35)
    animate_camera(cam, (1, -6, 2), (0.3, -4, 0.5), 1, total_frames)
