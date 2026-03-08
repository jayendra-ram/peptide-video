"""Scene 3: donor/acceptor orbital logic.

N lone pair (purple donor) and C=O pi* (orange acceptor) lobes animate in.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCENE_ID = "scene_03_orbitals"


def build(scene_ctx: Dict[str, Any]) -> None:
    style = scene_ctx["style"]
    preset = scene_ctx["preset"]
    fps = scene_ctx.get("fps", 30)
    duration = scene_ctx.get("duration_seconds", 25)

    from src.core.blender_scene import (
        add_orbital_lobe,
        add_text_overlay,
        animate_camera,
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

    # Draw molecules
    atoms_a = draw_molecule(
        GLYCINE_A_REACTANT, style, offset=(-1.0, 0, 0), label_prefix="OA_"
    )
    atoms_b = draw_molecule(
        GLYCINE_B_REACTANT, style, offset=(0, 0, 0), label_prefix="OB_"
    )

    # N lone pair lobe (donor, purple) – at N2, elongated toward C1
    n2_pos = tuple(atoms_b["N2"].location)
    n_lobe = add_orbital_lobe(
        position=n2_pos,
        role="donor",
        scale=(0.3, 0.3, 0.5),
        style=style,
        name="N_LonePair",
    )
    # Animate growth
    n_lobe.scale = (0, 0, 0)
    n_lobe.keyframe_insert(data_path="scale", frame=1)
    n_lobe.scale = (0, 0, 0)
    n_lobe.keyframe_insert(data_path="scale", frame=int(fps * 2))
    n_lobe.scale = (0.3, 0.3, 0.5)
    n_lobe.keyframe_insert(data_path="scale", frame=int(fps * 4))

    # C=O pi* lobe (acceptor, orange) – at midpoint of C=O bond
    c1_pos = atoms_a["C1"].location
    o1_pos = atoms_a["O1"].location
    co_mid = tuple((c1_pos[i] + o1_pos[i]) / 2 for i in range(3))
    pi_lobe = add_orbital_lobe(
        position=co_mid,
        role="acceptor",
        scale=(0.25, 0.4, 0.3),
        style=style,
        name="CO_PiStar",
    )
    pi_lobe.scale = (0, 0, 0)
    pi_lobe.keyframe_insert(data_path="scale", frame=int(fps * 4.5))
    pi_lobe.scale = (0.25, 0.4, 0.3)
    pi_lobe.keyframe_insert(data_path="scale", frame=int(fps * 6.5))

    # Labels
    add_text_overlay("HOMO (N lone pair)", location=(1.5, 0, 1.5), size=0.12)
    add_text_overlay("LUMO (C=O pi*)", location=(-2.5, 0, 1.5), size=0.12)

    # Molecule description
    desc = add_text_overlay(
        "N lone pair (donor) attacks C=O pi* (acceptor)",
        location=(-3.5, 0, -2.2), size=0.10,
    )
    desc.scale = (0, 0, 0)
    desc.keyframe_insert(data_path="scale", frame=1)
    desc.scale = (1, 1, 1)
    desc.keyframe_insert(data_path="scale", frame=int(fps * 1))

    # Camera push-in
    cam = setup_camera((0.5, -7, 3), (0.5, 0, 0), fov_deg=35)
    animate_camera(cam, (0.5, -7, 3), (0.5, -4, 1.5), 1, total_frames)
