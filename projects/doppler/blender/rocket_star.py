"""Blender Python script: Cute rocket ship observing stellar Doppler shift.

Run headlessly via:
    blender -b --python rocket_star.py -- --output out.mp4 --duration 14 --fps 30

The rocket approaches a star (starlight shifts blue) then recedes (shifts red).
"""

from __future__ import annotations

import argparse
import math
import os
import subprocess
import sys
import tempfile

import bpy
import bmesh
from mathutils import Vector, Matrix


# ---------------------------------------------------------------------------
# CLI argument parsing (everything after --)
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    # Blender passes everything after '--' in sys.argv
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, help="Output mp4 path")
    parser.add_argument("--duration", type=float, default=14.0)
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--resolution", default="1920x1080")
    return parser.parse_args(argv)


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def clear_scene():
    """Remove all default objects."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    # Remove orphan data
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)
    for block in bpy.data.materials:
        if block.users == 0:
            bpy.data.materials.remove(block)


def make_material(name: str, color: tuple, emission: float = 0.0,
                  alpha: float = 1.0) -> bpy.types.Material:
    mat = bpy.data.materials.new(name)
    if not mat.use_nodes:
        mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    if emission > 0:
        bsdf.inputs["Emission Color"].default_value = (*color, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission
    if alpha < 1.0:
        mat.blend_method = 'BLEND' if hasattr(mat, 'blend_method') else None
        bsdf.inputs["Alpha"].default_value = alpha
    return mat


def make_emission_material(name: str, color: tuple,
                           strength: float = 5.0) -> bpy.types.Material:
    mat = bpy.data.materials.new(name)
    if not mat.use_nodes:
        mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    # Clear default nodes
    for n in nodes:
        nodes.remove(n)
    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Color"].default_value = (*color, 1.0)
    emission.inputs["Strength"].default_value = strength
    links.new(emission.outputs["Emission"], output.inputs["Surface"])
    return mat


def smooth_shade(obj):
    """Apply smooth shading to an object."""
    for poly in obj.data.polygons:
        poly.use_smooth = True


def set_origin_to_geometry(obj):
    """Set origin to geometry center."""
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    obj.select_set(False)


# ---------------------------------------------------------------------------
# Rocket ship builder
# ---------------------------------------------------------------------------

def create_rocket(location: Vector = Vector((0, 0, 0))) -> bpy.types.Object:
    """Build a cute rocket ship from primitives, parented to an empty."""

    # Parent empty for the whole rocket
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=location)
    rocket_parent = bpy.context.object
    rocket_parent.name = "Rocket"

    # Colors — pastel / cute
    body_color = (0.95, 0.93, 0.88)       # cream white
    nose_color = (0.90, 0.35, 0.35)        # coral red
    fin_color = (0.90, 0.35, 0.35)         # matching red
    window_color = (0.3, 0.6, 0.9)         # sky blue
    engine_color = (1.0, 0.55, 0.1)        # orange glow

    # ── Body: cylinder ────────────────────────────────────────────
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.35, depth=1.6, location=(0, 0, 0),
    )
    body = bpy.context.object
    body.name = "RocketBody"
    smooth_shade(body)

    # Add subdivision surface for roundness
    sub = body.modifiers.new("Subsurf", 'SUBSURF')
    sub.levels = 2
    sub.render_levels = 2

    body_mat = make_material("BodyMat", body_color)
    body.data.materials.append(body_mat)
    body.parent = rocket_parent

    # ── Nose cone ─────────────────────────────────────────────────
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.35, radius2=0.0, depth=0.6,
        location=(0, 0, 1.1),
    )
    nose = bpy.context.object
    nose.name = "RocketNose"
    smooth_shade(nose)

    sub = nose.modifiers.new("Subsurf", 'SUBSURF')
    sub.levels = 2
    sub.render_levels = 2

    nose_mat = make_material("NoseMat", nose_color)
    nose.data.materials.append(nose_mat)
    nose.parent = rocket_parent

    # ── Porthole window ───────────────────────────────────────────
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.12, location=(0, -0.34, 0.25),
    )
    window = bpy.context.object
    window.name = "Porthole"
    smooth_shade(window)

    window_mat = make_material("WindowMat", window_color, emission=1.0)
    window.data.materials.append(window_mat)
    window.parent = rocket_parent

    # Second porthole lower
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.09, location=(0, -0.34, -0.1),
    )
    window2 = bpy.context.object
    window2.name = "Porthole2"
    smooth_shade(window2)
    window2.data.materials.append(window_mat)
    window2.parent = rocket_parent

    # ── Tail fins (3 around the base) ─────────────────────────────
    fin_mat = make_material("FinMat", fin_color)
    for i in range(3):
        angle = i * (2 * math.pi / 3)

        bpy.ops.mesh.primitive_cube_add(
            size=1, location=(0, 0, 0),
        )
        fin = bpy.context.object
        fin.name = f"Fin_{i}"
        fin.scale = (0.04, 0.25, 0.35)
        fin.location = (
            math.sin(angle) * 0.35,
            math.cos(angle) * 0.35,
            -0.65,
        )
        fin.rotation_euler = (0, 0, -angle)

        sub = fin.modifiers.new("Subsurf", 'SUBSURF')
        sub.levels = 1
        sub.render_levels = 1

        smooth_shade(fin)
        fin.data.materials.append(fin_mat)
        fin.parent = rocket_parent

    # ── Engine glow ───────────────────────────────────────────────
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.2, location=(0, 0, -0.95),
    )
    engine = bpy.context.object
    engine.name = "EngineGlow"
    smooth_shade(engine)
    engine.scale = (1, 1, 0.6)

    engine_mat = make_emission_material("EngineMat", engine_color, strength=8.0)
    engine.data.materials.append(engine_mat)
    engine.parent = rocket_parent

    # ── Flame trail ───────────────────────────────────────────────
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.15, radius2=0.0, depth=0.6,
        location=(0, 0, -1.3),
    )
    flame = bpy.context.object
    flame.name = "Flame"
    flame.rotation_euler = (math.pi, 0, 0)  # point downward
    smooth_shade(flame)

    flame_mat = make_emission_material("FlameMat", (1.0, 0.7, 0.2), strength=12.0)
    flame.data.materials.append(flame_mat)
    flame.parent = rocket_parent

    # Orient rocket to fly along X axis (nose pointing +X)
    rocket_parent.rotation_euler = (0, -math.pi / 2, 0)

    return rocket_parent


# ---------------------------------------------------------------------------
# Star builder
# ---------------------------------------------------------------------------

def create_star(location: Vector = Vector((0, 0, 0)),
                name: str = "Star") -> bpy.types.Object:
    """Create a glowing star with animated color."""
    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=4, radius=1.2, location=location,
    )
    star = bpy.context.object
    star.name = name
    smooth_shade(star)

    # Emission material with keyframeable color
    mat = bpy.data.materials.new("StarMat")
    if not mat.use_nodes:
        mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links

    for n in nodes:
        nodes.remove(n)

    output = nodes.new("ShaderNodeOutputMaterial")
    emission = nodes.new("ShaderNodeEmission")
    emission.inputs["Strength"].default_value = 15.0
    links.new(emission.outputs["Emission"], output.inputs["Surface"])

    star.data.materials.append(mat)

    return star


def keyframe_star_color(star: bpy.types.Object, total_frames: int):
    """Animate star color: yellow → blue (approach) → red (recession)."""
    mat = star.data.materials[0]
    emission_node = None
    for node in mat.node_tree.nodes:
        if node.type == 'EMISSION':
            emission_node = node
            break
    if not emission_node:
        return

    color_input = emission_node.inputs["Color"]

    # Color keyframes (RGBA)
    yellow = (1.0, 0.85, 0.2, 1.0)     # warm star yellow
    blue = (0.2, 0.5, 1.0, 1.0)         # blueshift
    red = (1.0, 0.25, 0.15, 1.0)        # redshift

    # Phase timing (as fraction of total frames)
    keyframes = [
        (1,                        yellow),   # start: warm yellow
        (int(total_frames * 0.15), yellow),   # hold yellow
        (int(total_frames * 0.50), blue),     # peak approach → blueshift
        (int(total_frames * 0.60), yellow),   # crossing point
        (int(total_frames * 0.90), red),      # receding → redshift
        (total_frames,             red),      # hold red
    ]

    for frame, color in keyframes:
        color_input.default_value = color
        color_input.keyframe_insert(data_path="default_value", frame=frame)


# ---------------------------------------------------------------------------
# Background stars
# ---------------------------------------------------------------------------

def create_background_stars(count: int = 80):
    """Scatter small emissive dots for the star field."""
    import random
    random.seed(42)

    star_mat = make_emission_material("BgStarMat", (0.9, 0.9, 1.0), strength=3.0)

    mesh = bpy.data.meshes.new("BgStarMesh")
    bm = bmesh.new()
    for _ in range(count):
        x = random.uniform(-25, 25)
        y = random.uniform(-25, 25)
        z = random.uniform(-15, 15)
        bmesh.ops.create_icosphere(
            bm, subdivisions=1, radius=0.03,
            matrix=Matrix.Translation((x, y, z)),
        )
    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new("BackgroundStars", mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(star_mat)


# ---------------------------------------------------------------------------
# Labels (Blender text objects)
# ---------------------------------------------------------------------------

def create_label(text: str, location: tuple, color: tuple,
                 size: float = 0.4) -> bpy.types.Object:
    bpy.ops.object.text_add(location=location)
    obj = bpy.context.object
    obj.data.body = text
    obj.data.size = size
    obj.data.align_x = 'CENTER'
    obj.data.align_y = 'CENTER'

    mat = make_emission_material(f"Label_{text}", color, strength=3.0)
    obj.data.materials.append(mat)

    # Face toward camera (billboard) — rotate to face -Y
    obj.rotation_euler = (math.pi / 2, 0, 0)

    return obj


def keyframe_label_visibility(obj: bpy.types.Object,
                              show_start: int, show_end: int):
    """Make a label appear and disappear at specific frames."""
    # Hide before show_start
    obj.hide_render = True
    obj.hide_viewport = True
    obj.keyframe_insert(data_path="hide_render", frame=show_start - 1)
    obj.keyframe_insert(data_path="hide_viewport", frame=show_start - 1)

    # Show during range
    obj.hide_render = False
    obj.hide_viewport = False
    obj.keyframe_insert(data_path="hide_render", frame=show_start)
    obj.keyframe_insert(data_path="hide_viewport", frame=show_start)

    # Hide after show_end
    obj.hide_render = True
    obj.hide_viewport = True
    obj.keyframe_insert(data_path="hide_render", frame=show_end)
    obj.keyframe_insert(data_path="hide_viewport", frame=show_end)


# ---------------------------------------------------------------------------
# Camera & lighting
# ---------------------------------------------------------------------------

def setup_camera(total_frames: int) -> bpy.types.Object:
    bpy.ops.object.camera_add(location=(0, -12, 2))
    cam = bpy.context.object
    cam.name = "MainCamera"
    cam.data.lens = 35
    cam.data.clip_end = 200

    # Point at the scene center
    bpy.ops.object.constraint_add(type='TRACK_TO')
    constraint = cam.constraints["Track To"]

    # Create a tracking target that follows the midpoint
    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(3, 0, 0))
    target = bpy.context.object
    target.name = "CamTarget"
    constraint.target = target
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'

    bpy.context.scene.camera = cam
    return cam


def setup_lighting():
    # Key light
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 8))
    sun = bpy.context.object
    sun.name = "KeyLight"
    sun.data.energy = 2.0
    sun.data.color = (1.0, 0.95, 0.85)

    # Fill light (dimmer, from the other side)
    bpy.ops.object.light_add(type='SUN', location=(-3, -3, 4))
    fill = bpy.context.object
    fill.name = "FillLight"
    fill.data.energy = 0.5
    fill.data.color = (0.7, 0.8, 1.0)


# ---------------------------------------------------------------------------
# Animation
# ---------------------------------------------------------------------------

def animate_rocket(rocket: bpy.types.Object, total_frames: int):
    """Animate rocket: approach the star then recede."""
    # Rocket starts at x=-6, approaches star at x=8, gets close, then recedes

    keyframes = [
        (1,                          (-6, 0, 0)),    # start position (far left)
        (int(total_frames * 0.15),   (-4, 0, 0)),    # begin approach
        (int(total_frames * 0.50),   (4, 0, 0.3)),   # close to star
        (int(total_frames * 0.60),   (5, 0, 0)),     # closest point
        (int(total_frames * 0.65),   (4.5, 0, -0.2)),# turning
        (int(total_frames * 0.90),   (-3, 0, 0)),    # receded
        (total_frames,               (-5, 0, 0)),    # final position
    ]

    for frame, loc in keyframes:
        rocket.location = Vector(loc)
        rocket.keyframe_insert(data_path="location", frame=frame)

    # Ease the keyframes (Blender 4.4+ uses layered actions)
    if rocket.animation_data and rocket.animation_data.action:
        action = rocket.animation_data.action
        try:
            # Blender 4.4+ layered action API
            for layer in action.layers:
                for strip in layer.strips:
                    for bag in strip.channelbags:
                        for fc in bag.fcurves:
                            for kp in fc.keyframe_points:
                                kp.interpolation = 'BEZIER'
                                kp.handle_left_type = 'AUTO_CLAMPED'
                                kp.handle_right_type = 'AUTO_CLAMPED'
        except AttributeError:
            pass  # Skip easing on unsupported Blender versions


# ---------------------------------------------------------------------------
# Title text
# ---------------------------------------------------------------------------

def create_title(total_frames: int):
    """Add a title and subtitle that appear at the start."""
    title = create_label(
        "Rocket & Starlight",
        location=(0, 5, 4),
        color=(0.9, 0.9, 0.95),
        size=0.6,
    )
    keyframe_label_visibility(title, 1, int(total_frames * 0.25))

    subtitle = create_label(
        "How motion changes the color of light",
        location=(0, 5, 3.2),
        color=(0.7, 0.75, 0.85),
        size=0.3,
    )
    keyframe_label_visibility(subtitle, int(total_frames * 0.05), int(total_frames * 0.25))

    # Blueshift label
    blue_label = create_label(
        "BLUESHIFT",
        location=(2, 5, 2.5),
        color=(0.3, 0.5, 1.0),
        size=0.5,
    )
    keyframe_label_visibility(
        blue_label,
        int(total_frames * 0.35),
        int(total_frames * 0.55),
    )

    # Redshift label
    red_label = create_label(
        "REDSHIFT",
        location=(0, 5, 2.5),
        color=(1.0, 0.3, 0.2),
        size=0.5,
    )
    keyframe_label_visibility(
        red_label,
        int(total_frames * 0.70),
        int(total_frames * 0.92),
    )


# ---------------------------------------------------------------------------
# Render settings & output
# ---------------------------------------------------------------------------

def configure_render(fps: int, res_x: int, res_y: int, total_frames: int):
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.render.resolution_x = res_x
    scene.render.resolution_y = res_y
    scene.render.resolution_percentage = 100
    scene.render.fps = fps
    scene.frame_start = 1
    scene.frame_end = total_frames
    scene.render.image_settings.file_format = 'PNG'

    # EEVEE settings for quality/speed balance
    scene.render.film_transparent = False
    if scene.world is None:
        scene.world = bpy.data.worlds.new("World")
    if not scene.world.use_nodes:
        scene.world.use_nodes = True
    bg_node = scene.world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs["Color"].default_value = (0.02, 0.023, 0.04, 1.0)
        bg_node.inputs["Strength"].default_value = 1.0

    # Bloom for glow effects
    if hasattr(scene, 'eevee'):
        eevee = scene.eevee
        # Blender 4.x+ bloom is a compositor effect; set up basic settings
        if hasattr(eevee, 'use_bloom'):
            eevee.use_bloom = True
            eevee.bloom_threshold = 0.8
            eevee.bloom_intensity = 0.5


def render_animation(output_mp4: str, fps: int):
    """Render frames to a temp dir, then encode to MP4 with FFmpeg."""
    with tempfile.TemporaryDirectory(prefix="blender_rocket_") as tmpdir:
        frame_path = os.path.join(tmpdir, "frame_")
        bpy.context.scene.render.filepath = frame_path

        print(f"[blender] Rendering frames to {tmpdir} ...")
        bpy.ops.render.render(animation=True)

        # Encode frames to MP4
        output_dir = os.path.dirname(output_mp4)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-framerate", str(fps),
            "-i", os.path.join(tmpdir, "frame_%04d.png"),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-preset", "fast",
            str(output_mp4),
        ]
        print(f"[ffmpeg] {' '.join(ffmpeg_cmd)}")
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"[blender] Output: {output_mp4}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()

    res_parts = args.resolution.split("x")
    res_x, res_y = int(res_parts[0]), int(res_parts[1])
    total_frames = int(args.duration * args.fps)

    # Build the scene
    clear_scene()

    star = create_star(location=Vector((8, 0, 0)))
    keyframe_star_color(star, total_frames)

    rocket = create_rocket(location=Vector((-6, 0, 0)))
    animate_rocket(rocket, total_frames)

    create_background_stars(count=100)
    create_title(total_frames)

    setup_camera(total_frames)
    setup_lighting()
    configure_render(args.fps, res_x, res_y, total_frames)

    # Render
    render_animation(args.output, args.fps)


if __name__ == "__main__":
    main()
