"""Scene 1: establish the peptide bond question.

Protein backbone as 4 repeating amide units, camera zooms to isolate one bond.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCENE_ID = "scene_01_intro"


def build(scene_ctx: Dict[str, Any]) -> None:
    style = scene_ctx["style"]
    preset = scene_ctx["preset"]
    fps = scene_ctx.get("fps", 30)
    duration = scene_ctx.get("duration_seconds", 15)

    from src.core.blender_scene import (
        add_text_overlay,
        animate_camera,
        hex_to_linear_rgb,
        setup_camera,
        setup_lighting,
        setup_scene,
    )
    from src.chemistry.molecules import AMIDE_PRODUCT, draw_molecule

    setup_scene(preset, style, fps=fps, duration_seconds=duration)
    setup_lighting()

    import bpy

    # Draw 4 repeating peptide units as a backbone chain
    for i in range(4):
        offset = (i * 2.8 - 4.2, 0, 0)
        draw_molecule(AMIDE_PRODUCT, style, offset=offset, label_prefix=f"U{i}_")

    # Highlight the central amide bond (unit 1 C1-N2 midpoint)
    highlight_pos = (-1.4 + 0.25, 0, -0.3)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.35, location=highlight_pos)
    highlight = bpy.context.active_object
    highlight.name = "AmideBondHighlight"

    hr, hg, hb = hex_to_linear_rgb("#f1c40f")
    mat = bpy.data.materials.new("HighlightMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    mix = nodes.new("ShaderNodeMixShader")
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (hr, hg, hb, 1.0)
    emission.inputs["Strength"].default_value = 3.0
    mix.inputs[0].default_value = 0.5
    links.new(transparent.outputs[0], mix.inputs[1])
    links.new(emission.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs[0])
    highlight.data.materials.append(mat)
    bpy.ops.object.shade_smooth()

    # Camera: zoom from far to close
    total_frames = int(fps * duration)
    cam = setup_camera((0, -12, 6), (0, 0, 0), fov_deg=35)
    animate_camera(cam, (0, -12, 6), (0, -4, 1.5), 1, int(total_frames * 0.85))

    # Title text
    title = add_text_overlay(
        "What IS a peptide bond?", location=(-3.0, 0, 3.5), size=0.28
    )
    title.scale = (0, 0, 0)
    title.keyframe_insert(data_path="scale", frame=1)
    title.scale = (1, 1, 1)
    title.keyframe_insert(data_path="scale", frame=int(fps * 0.5))
    title.keyframe_insert(data_path="scale", frame=int(fps * 3.0))
    title.scale = (0, 0, 0)
    title.keyframe_insert(data_path="scale", frame=int(fps * 4.0))

    # Molecule description
    desc = add_text_overlay(
        "Protein backbone: repeating -NH-CO- amide units",
        location=(-3.5, 0, -2.5), size=0.10,
    )
    desc.scale = (0, 0, 0)
    desc.keyframe_insert(data_path="scale", frame=int(fps * 2))
    desc.scale = (1, 1, 1)
    desc.keyframe_insert(data_path="scale", frame=int(fps * 3))
