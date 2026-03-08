"""Scene 7: amide resonance and planarity.

Pulsing orbital-like glow on the C-N bond shows resonance character.
Camera orbits to reveal planarity.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCENE_ID = "scene_07_resonance"


def build(scene_ctx: Dict[str, Any]) -> None:
    style = scene_ctx["style"]
    preset = scene_ctx["preset"]
    fps = scene_ctx.get("fps", 30)
    duration = scene_ctx.get("duration_seconds", 22)

    from src.core.blender_scene import (
        _set_bezier_easing,
        add_orbital_lobe,
        add_text_overlay,
        hex_to_linear_rgb,
        setup_camera,
        setup_lighting,
        setup_scene,
    )
    from src.chemistry.molecules import AMIDE_PRODUCT, draw_molecule

    setup_scene(preset, style, fps=fps, duration_seconds=duration)
    setup_lighting()

    import bpy

    total_frames = int(fps * duration)

    # Draw amide product
    atoms = draw_molecule(AMIDE_PRODUCT, style, label_prefix="S7_")

    c1_pos = atoms["C1"].location
    n2_pos = atoms["N2"].location
    o1_pos = atoms["O1"].location

    # --- Resonance glow: large pulsing lobe between C1 and N2 ---
    cn_mid = tuple((c1_pos[i] + n2_pos[i]) / 2 for i in range(3))
    co_mid = tuple((c1_pos[i] + o1_pos[i]) / 2 for i in range(3))

    # Donor-side lobe on C-N (purple, pulsing)
    cn_lobe = add_orbital_lobe(
        position=cn_mid,
        role="donor",
        scale=(0.35, 0.2, 0.25),
        style=style,
        name="CN_Resonance_Lobe",
    )

    # Acceptor-side lobe on C=O (orange, counter-pulsing)
    co_lobe = add_orbital_lobe(
        position=co_mid,
        role="acceptor",
        scale=(0.25, 0.2, 0.2),
        style=style,
        name="CO_Resonance_Lobe",
    )

    # --- Animate resonance: CN lobe grows as CO lobe shrinks, and vice versa ---
    cycle_frames = int(fps * 2.0)  # 2-second cycle (faster)
    num_cycles = int(total_frames / cycle_frames) + 1

    for cycle in range(num_cycles):
        f_a = 1 + cycle * cycle_frames
        f_b = f_a + cycle_frames // 2

        cn_lobe.scale = (0.4, 0.25, 0.3)
        cn_lobe.keyframe_insert(data_path="scale", frame=f_a)
        cn_lobe.scale = (0.15, 0.1, 0.12)
        cn_lobe.keyframe_insert(data_path="scale", frame=f_b)

        co_lobe.scale = (0.15, 0.1, 0.12)
        co_lobe.keyframe_insert(data_path="scale", frame=f_a)
        co_lobe.scale = (0.35, 0.25, 0.25)
        co_lobe.keyframe_insert(data_path="scale", frame=f_b)

    # --- Animate N2 flattening to show planarity ---
    n2_obj = atoms["N2"]
    orig_n2 = tuple(n2_pos)
    flat_n2 = (orig_n2[0], orig_n2[1], 0.0)

    n2_obj.location = orig_n2
    n2_obj.keyframe_insert(data_path="location", frame=1)
    n2_obj.keyframe_insert(data_path="location", frame=int(total_frames * 0.2))
    n2_obj.location = flat_n2
    n2_obj.keyframe_insert(data_path="location", frame=int(total_frames * 0.5))
    n2_obj.keyframe_insert(data_path="location", frame=total_frames)

    # --- Camera: orbit around the molecule to show planarity ---
    cam = setup_camera((0.3, -5.5, 1.5), (0.3, 0, -0.3), fov_deg=35)

    num_keyframes = 8
    for i in range(num_keyframes + 1):
        frame = 1 + int(i * total_frames / num_keyframes)
        angle = i * math.pi * 0.6 / num_keyframes  # ~108° arc
        radius = 5.5
        x = 0.3 + radius * math.sin(angle)
        y = -radius * math.cos(angle)
        z_dip = -0.8 * math.sin(math.pi * i / num_keyframes)
        z = 1.5 + z_dip
        cam.location = (x, y, z)
        cam.keyframe_insert(data_path="location", frame=frame)

    _set_bezier_easing(cam)

    # --- Labels ---
    label1 = add_text_overlay(
        "C=O / C-N Resonance", location=(-2.5, 0, 2.2), size=0.16
    )
    label1.scale = (0, 0, 0)
    label1.keyframe_insert(data_path="scale", frame=1)
    label1.scale = (1, 1, 1)
    label1.keyframe_insert(data_path="scale", frame=int(fps * 0.5))
    label1.keyframe_insert(data_path="scale", frame=int(fps * 3))
    label1.scale = (0, 0, 0)
    label1.keyframe_insert(data_path="scale", frame=int(fps * 4))

    label2 = add_text_overlay(
        "Planar Amide Bond", location=(-2.0, 0, -2.0), size=0.14
    )
    label2.scale = (0, 0, 0)
    label2.keyframe_insert(data_path="scale", frame=int(total_frames * 0.4))
    label2.scale = (1, 1, 1)
    label2.keyframe_insert(data_path="scale", frame=int(total_frames * 0.45))
    label2.keyframe_insert(data_path="scale", frame=int(total_frames * 0.75))
    label2.scale = (0, 0, 0)
    label2.keyframe_insert(data_path="scale", frame=int(total_frames * 0.8))

    # Molecule description
    add_text_overlay(
        "Amide product: Gly-CO-NH-Gly (partial C=N double bond)",
        location=(-3.5, 0, -2.8), size=0.09,
    )
