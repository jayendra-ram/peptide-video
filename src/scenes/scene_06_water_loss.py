"""Scene 6: proton transfers and water loss.

Start from tetrahedral intermediate. Water departs. Proton transfers.
Bonds skipped to avoid static-cylinder artifacts during animation.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCENE_ID = "scene_06_water_loss"


def build(scene_ctx: Dict[str, Any]) -> None:
    style = scene_ctx["style"]
    preset = scene_ctx["preset"]
    fps = scene_ctx.get("fps", 30)
    duration = scene_ctx.get("duration_seconds", 10)

    from src.core.blender_scene import (
        _set_bezier_easing,
        add_text_overlay,
        animate_camera,
        setup_camera,
        setup_lighting,
        setup_scene,
    )
    from src.chemistry.molecules import (
        AMIDE_PRODUCT,
        TETRAHEDRAL_TS,
        draw_molecule,
    )

    setup_scene(preset, style, fps=fps, duration_seconds=duration)
    setup_lighting()

    import bpy

    total_frames = int(fps * duration)

    # Draw tetrahedral intermediate — skip bonds since atoms will animate
    atoms = draw_molecule(TETRAHEDRAL_TS, style, label_prefix="S6_", skip_bonds=True)

    # Keyframe starting positions
    for label, obj in atoms.items():
        obj.keyframe_insert(data_path="location", frame=1)

    # Build product position lookup
    product_positions = {label: pos for label, sym, pos in AMIDE_PRODUCT.atoms}

    # Water departure: OH1 and H_OH fly away
    water_labels = ["OH1", "H_OH"]
    depart_frame = int(total_frames * 0.5)
    gone_frame = int(total_frames * 0.7)

    for label in water_labels:
        obj = atoms.get(label)
        if obj:
            obj.keyframe_insert(data_path="location", frame=1)
            obj.location = (3.0, 2.0, 1.5)
            obj.keyframe_insert(data_path="location", frame=depart_frame)
            obj.scale = (1, 1, 1)
            obj.keyframe_insert(data_path="scale", frame=depart_frame)
            obj.scale = (0, 0, 0)
            obj.keyframe_insert(data_path="scale", frame=gone_frame)

    # Proton transfer: H_N2b moves toward water
    h_transfer = atoms.get("H_N2b")
    if h_transfer:
        h_transfer.keyframe_insert(data_path="location", frame=1)
        transfer_frame = int(total_frames * 0.35)
        oh1_obj = atoms.get("OH1")
        if oh1_obj:
            h_transfer.location = tuple(oh1_obj.location)
        h_transfer.keyframe_insert(data_path="location", frame=transfer_frame)
        h_transfer.location = (3.3, 2.3, 1.5)
        h_transfer.keyframe_insert(data_path="location", frame=depart_frame)
        h_transfer.scale = (1, 1, 1)
        h_transfer.keyframe_insert(data_path="scale", frame=depart_frame)
        h_transfer.scale = (0, 0, 0)
        h_transfer.keyframe_insert(data_path="scale", frame=gone_frame)

    # Remaining atoms settle toward product geometry
    settle_frame = int(total_frames * 0.85)
    for label, obj in atoms.items():
        if label in water_labels or label == "H_N2b":
            continue
        if label in product_positions:
            obj.location = product_positions[label]
            obj.keyframe_insert(data_path="location", frame=settle_frame)

    # Ease keyframes
    for label, obj in atoms.items():
        _set_bezier_easing(obj)

    # Labels
    add_text_overlay("Water Departure", location=(-2.0, 0, 2.5), size=0.16)

    # Molecule description
    desc = add_text_overlay(
        "Tetrahedral intermediate  -->  amide + H2O",
        location=(-3.0, 0, -2.2), size=0.10,
    )
    desc.scale = (0, 0, 0)
    desc.keyframe_insert(data_path="scale", frame=1)
    desc.scale = (1, 1, 1)
    desc.keyframe_insert(data_path="scale", frame=int(fps * 0.5))

    cam = setup_camera((0.5, -6, 2), (0.3, 0, -0.3), fov_deg=35)
    animate_camera(cam, (0.5, -6, 2), (0.3, -5, 0.5), 1, total_frames)
