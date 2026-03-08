"""Shared Blender helper functions for all scene files.

Every function that uses bpy imports it inside the function body so the module
remains importable outside of Blender for testing.
"""

from __future__ import annotations

import math
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Material cache – reset per-scene via clear_material_cache()
_material_cache: Dict[str, object] = {}


# ── Colour helpers ────────────────────────────────────────────────────────────


def _srgb_to_linear(c: float) -> float:
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def hex_to_linear_rgb(hex_color: str) -> Tuple[float, float, float]:
    """Convert '#RRGGBB' to linear-space float triple."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4))
    return _srgb_to_linear(r), _srgb_to_linear(g), _srgb_to_linear(b)


# ── Scene setup ───────────────────────────────────────────────────────────────


def clear_material_cache() -> None:
    _material_cache.clear()


def setup_scene(
    preset: dict,
    style: dict,
    fps: int = 30,
    duration_seconds: float = 10.0,
) -> None:
    """Clear default scene, configure world + render engine."""
    import bpy

    clear_material_cache()

    # Delete all default objects
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)

    # Remove orphan data
    for block in bpy.data.meshes:
        if block.users == 0:
            bpy.data.meshes.remove(block)

    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = int(fps * duration_seconds)
    scene.render.fps = fps
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = preset.get("resolution_percentage", 50)
    scene.render.image_settings.file_format = "PNG"

    engine = preset.get("engine", "EEVEE")
    if engine == "CYCLES":
        scene.render.engine = "CYCLES"
        scene.cycles.samples = preset.get("samples", 64)
        scene.cycles.use_denoising = preset.get("denoise", True)
        # Try Metal on macOS
        try:
            prefs = bpy.context.preferences.addons["cycles"].preferences
            prefs.compute_device_type = "METAL"
            prefs.get_devices()
            for dev in prefs.devices:
                dev.use = True
            scene.cycles.device = "GPU"
        except Exception:
            pass
    else:
        # EEVEE name varies by Blender version
        try:
            scene.render.engine = "BLENDER_EEVEE_NEXT"
        except TypeError:
            scene.render.engine = "BLENDER_EEVEE"
        try:
            scene.eevee.taa_render_samples = preset.get("samples", 16)
        except AttributeError:
            pass

    # World background
    bg_hex = style.get("colors", {}).get("background", "#05060a")
    r, g, b = hex_to_linear_rgb(bg_hex)
    if scene.world is None:
        scene.world = bpy.data.worlds.new("World")
    world = scene.world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs[0].default_value = (r, g, b, 1.0)
        bg_node.inputs[1].default_value = 1.0


# ── Lighting ──────────────────────────────────────────────────────────────────


def setup_lighting() -> None:
    """Three-point area light rig for molecular visualization."""
    import bpy

    # Key light
    key = bpy.data.lights.new("KeyLight", "AREA")
    key.energy = 800
    key.size = 3.0
    key_obj = bpy.data.objects.new("KeyLight", key)
    bpy.context.collection.objects.link(key_obj)
    key_obj.location = (4, -3, 5)
    key_obj.rotation_euler = (0.8, 0.3, 0.6)

    # Fill light
    fill = bpy.data.lights.new("FillLight", "AREA")
    fill.energy = 300
    fill.size = 5.0
    fill.color = (0.8, 0.9, 1.0)
    fill_obj = bpy.data.objects.new("FillLight", fill)
    bpy.context.collection.objects.link(fill_obj)
    fill_obj.location = (-5, -2, 3)

    # Rim light
    rim = bpy.data.lights.new("RimLight", "SPOT")
    rim.energy = 200
    rim.spot_size = 0.8
    rim_obj = bpy.data.objects.new("RimLight", rim)
    bpy.context.collection.objects.link(rim_obj)
    rim_obj.location = (0, 5, 2)
    rim_obj.rotation_euler = (1.2, 0, 3.14)


# ── Materials ─────────────────────────────────────────────────────────────────


def _principled_bsdf(mat):
    """Return the Principled BSDF node from a material's node tree."""
    for node in mat.node_tree.nodes:
        if node.type == "BSDF_PRINCIPLED":
            return node
    return None


def get_or_create_atom_material(symbol: str, style: dict):
    """Cached Principled BSDF material for an atom type."""
    import bpy

    name = f"Atom_{symbol}"
    if name in _material_cache and name in bpy.data.materials:
        return _material_cache[name]

    hex_color = style.get("colors", {}).get(f"atom_{symbol.lower()}", "#ffffff")
    r, g, b = hex_to_linear_rgb(hex_color)

    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = _principled_bsdf(mat)
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (r, g, b, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.35
        bsdf.inputs["Metallic"].default_value = 0.0
    _material_cache[name] = mat
    return mat


def _get_bond_material():
    """Shared grey bond material."""
    import bpy

    name = "Bond_Mat"
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = _principled_bsdf(mat)
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1.0)
        bsdf.inputs["Roughness"].default_value = 0.6
    return mat


# ── Atoms ─────────────────────────────────────────────────────────────────────


def add_atom(
    symbol: str,
    position: Tuple[float, float, float],
    style: dict,
    name: str = "",
) -> object:
    """Create a UV sphere for an atom at the given position."""
    import bpy

    radii = style.get("materials", {}).get("atom_radius", {})
    radius = radii.get(symbol, 0.2)

    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=radius,
        location=position,
        segments=24,
        ring_count=16,
    )
    obj = bpy.context.active_object
    obj.name = name or f"{symbol}_{id(obj)}"

    mat = get_or_create_atom_material(symbol, style)
    obj.data.materials.append(mat)

    bpy.ops.object.shade_smooth()
    return obj


# ── Bonds ─────────────────────────────────────────────────────────────────────


def add_bond(
    pos_a: Tuple[float, float, float],
    pos_b: Tuple[float, float, float],
    order: float = 1.0,
    style: Optional[dict] = None,
    name: str = "Bond",
) -> List[object]:
    """Create oriented cylinder(s) between two atom positions."""
    import bpy
    import mathutils

    va = mathutils.Vector(pos_a)
    vb = mathutils.Vector(pos_b)
    mid = (va + vb) / 2
    direction = vb - va
    length = direction.length
    if length < 1e-6:
        return []

    z_axis = mathutils.Vector((0, 0, 1))
    rot_quat = z_axis.rotation_difference(direction)

    objects: List[object] = []

    if order >= 1.5:
        # Double bond: two thinner cylinders offset
        radius = 0.04
        perp = direction.cross(z_axis)
        if perp.length < 1e-6:
            perp = direction.cross(mathutils.Vector((1, 0, 0)))
        perp.normalize()
        for i, off in enumerate([0.06, -0.06]):
            offset_vec = perp * off
            bpy.ops.mesh.primitive_cylinder_add(
                radius=radius,
                depth=length,
                location=(mid + offset_vec)[:],
                rotation=rot_quat.to_euler(),
            )
            obj = bpy.context.active_object
            obj.name = f"{name}_d{i}"
            obj.data.materials.append(_get_bond_material())
            bpy.ops.object.shade_smooth()
            objects.append(obj)
    else:
        radius = 0.06
        bpy.ops.mesh.primitive_cylinder_add(
            radius=radius,
            depth=length,
            location=mid[:],
            rotation=rot_quat.to_euler(),
        )
        obj = bpy.context.active_object
        obj.name = name
        obj.data.materials.append(_get_bond_material())
        bpy.ops.object.shade_smooth()
        objects.append(obj)

    return objects


# ── Orbitals ──────────────────────────────────────────────────────────────────


def add_orbital_lobe(
    position: Tuple[float, float, float],
    role: str,
    scale: Tuple[float, float, float],
    style: dict,
    name: str = "Orbital",
) -> object:
    """Semi-transparent emission ellipsoid for donor/acceptor lobes."""
    import bpy

    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=1.0, location=position, segments=20, ring_count=12
    )
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale

    color_key = "orbital_donor" if role == "donor" else "orbital_acceptor"
    hex_color = style.get("colors", {}).get(color_key, "#aaaaaa")
    r, g, b = hex_to_linear_rgb(hex_color)
    emission_strength = 4.0 if role == "donor" else 2.5

    mat_name = f"Orbital_{role}"
    if mat_name not in bpy.data.materials:
        mat = bpy.data.materials.new(mat_name)
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()

        output = nodes.new("ShaderNodeOutputMaterial")
        mix = nodes.new("ShaderNodeMixShader")
        transparent = nodes.new("ShaderNodeBsdfTransparent")
        emission = nodes.new("ShaderNodeEmission")
        emission.inputs["Color"].default_value = (r, g, b, 1.0)
        emission.inputs["Strength"].default_value = emission_strength

        mix.inputs[0].default_value = 0.65
        links.new(transparent.outputs[0], mix.inputs[1])
        links.new(emission.outputs[0], mix.inputs[2])
        links.new(mix.outputs[0], output.inputs[0])

    obj.data.materials.append(bpy.data.materials[mat_name])
    bpy.ops.object.shade_smooth()
    return obj


# ── Charge halos ──────────────────────────────────────────────────────────────


def add_charge_halo(atom_obj, magnitude: float, style: dict) -> object:
    """Translucent sphere indicating partial charge."""
    import bpy

    color_key = "charge_positive" if magnitude > 0 else "charge_negative"
    hex_color = style.get("colors", {}).get(color_key, "#ffffff")
    r, g, b = hex_to_linear_rgb(hex_color)
    alpha = min(abs(magnitude) * 0.8, 0.6)

    bpy.ops.mesh.primitive_ico_sphere_add(
        radius=0.45, location=atom_obj.location, subdivisions=2
    )
    halo = bpy.context.active_object
    halo.name = f"Halo_{atom_obj.name}"

    mat = bpy.data.materials.new(f"Halo_{atom_obj.name}")
    mat.use_nodes = True
    bsdf = _principled_bsdf(mat)
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (r, g, b, 1.0)
        bsdf.inputs["Alpha"].default_value = alpha
        bsdf.inputs["Roughness"].default_value = 1.0
        # Emission glow
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (r, g, b, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 0.5
    mat.surface_render_method = "BLENDED"
    halo.data.materials.append(mat)
    bpy.ops.object.shade_smooth()
    return halo


# ── Curved arrows ─────────────────────────────────────────────────────────────


def add_curved_arrow(
    start: Tuple[float, float, float],
    end: Tuple[float, float, float],
    color: Tuple[float, float, float] = (1.0, 0.8, 0.0),
    arc_height: float = 0.5,
) -> object:
    """Bezier curve with emission material representing electron flow."""
    import bpy
    import mathutils

    curve_data = bpy.data.curves.new("Arrow", "CURVE")
    curve_data.dimensions = "3D"
    curve_data.bevel_depth = 0.02

    spline = curve_data.splines.new("BEZIER")
    spline.bezier_points.add(1)

    p0 = spline.bezier_points[0]
    p0.co = mathutils.Vector(start)
    p0.handle_right_type = "AUTO"
    p0.handle_left_type = "AUTO"

    p1 = spline.bezier_points[1]
    p1.co = mathutils.Vector(end)
    p1.handle_right_type = "AUTO"
    p1.handle_left_type = "AUTO"

    # Arch the control handles upward
    mid_y = (start[1] + end[1]) / 2 + arc_height
    p0.handle_right = mathutils.Vector(
        ((start[0] + end[0]) / 2, mid_y, (start[2] + end[2]) / 2 + arc_height)
    )
    p1.handle_left = mathutils.Vector(
        ((start[0] + end[0]) / 2, mid_y, (start[2] + end[2]) / 2 + arc_height)
    )

    obj = bpy.data.objects.new("CurvedArrow", curve_data)
    bpy.context.collection.objects.link(obj)

    mat = bpy.data.materials.new("ArrowMat")
    mat.use_nodes = True
    bsdf = _principled_bsdf(mat)
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (*color, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 3.0
    obj.data.materials.append(mat)
    return obj


# ── Camera ────────────────────────────────────────────────────────────────────


def _get_or_create_empty(name: str, location: Tuple[float, float, float]):
    import bpy

    if name in bpy.data.objects:
        obj = bpy.data.objects[name]
        obj.location = location
        return obj
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=location)
    obj = bpy.context.active_object
    obj.name = name
    return obj


def setup_camera(
    location: Tuple[float, float, float],
    look_at: Tuple[float, float, float],
    fov_deg: float = 35.0,
) -> object:
    """Create camera pointed at look_at via Track To constraint."""
    import bpy

    bpy.ops.object.camera_add(location=location)
    cam_obj = bpy.context.active_object
    cam_obj.name = "SceneCamera"
    bpy.context.scene.camera = cam_obj

    cam_obj.data.lens_unit = "FOV"
    cam_obj.data.angle = math.radians(fov_deg)

    target = _get_or_create_empty("CameraTarget", look_at)
    constraint = cam_obj.constraints.new(type="TRACK_TO")
    constraint.target = target
    constraint.track_axis = "TRACK_NEGATIVE_Z"
    constraint.up_axis = "UP_Y"

    return cam_obj


def _set_bezier_easing(obj) -> None:
    """Apply Bezier easing to all keyframes on an object (Blender 4/5 safe)."""
    if not obj.animation_data or not obj.animation_data.action:
        return
    action = obj.animation_data.action
    # Blender 5 layered actions don't expose fcurves directly
    fcurves = getattr(action, "fcurves", None)
    if fcurves is None:
        return
    try:
        for fc in fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = "BEZIER"
                kp.easing = "EASE_IN_OUT"
    except Exception:
        pass


def animate_camera(
    cam_obj,
    start_loc: Tuple[float, float, float],
    end_loc: Tuple[float, float, float],
    start_frame: int,
    end_frame: int,
) -> None:
    """Keyframe camera location with Bezier easing."""
    cam_obj.location = start_loc
    cam_obj.keyframe_insert(data_path="location", frame=start_frame)

    cam_obj.location = end_loc
    cam_obj.keyframe_insert(data_path="location", frame=end_frame)

    _set_bezier_easing(cam_obj)


# ── Text overlays ─────────────────────────────────────────────────────────────


def add_scene_number(
    scene_num: int,
    total_scenes: int = 9,
    cam_obj=None,
) -> object:
    """Persistent scene number label (e.g. '1/9') parented to the camera."""
    import bpy

    text = f"{scene_num}/{total_scenes}"
    bpy.ops.object.text_add(location=(0, 0, 0))
    obj = bpy.context.active_object
    obj.name = f"SceneNum_{scene_num}"
    obj.data.body = text
    obj.data.size = 0.04
    obj.data.align_x = "RIGHT"
    obj.data.align_y = "TOP"

    mat = bpy.data.materials.new(f"SceneNumMat_{scene_num}")
    mat.use_nodes = True
    bsdf = _principled_bsdf(mat)
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (0.7, 0.7, 0.7, 1.0)
        bsdf.inputs["Alpha"].default_value = 0.7
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (0.7, 0.7, 0.7, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 1.5
    obj.data.materials.append(mat)

    if cam_obj is None:
        cam_obj = bpy.context.scene.camera
    if cam_obj:
        obj.parent = cam_obj
        # Position in camera-local space: top-right corner, slightly in front
        obj.location = (0.27, 0.17, -0.5)

    return obj


def add_text_overlay(
    text: str,
    location: Tuple[float, float, float] = (-3.5, 0, 2.5),
    size: float = 0.18,
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
) -> object:
    """3D text object with emission material."""
    import bpy

    bpy.ops.object.text_add(location=location)
    obj = bpy.context.active_object
    obj.name = f"Text_{text[:20]}"
    obj.data.body = text
    obj.data.size = size
    obj.data.align_x = "LEFT"

    mat = bpy.data.materials.new(f"TextMat_{text[:10]}")
    mat.use_nodes = True
    bsdf = _principled_bsdf(mat)
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (*color, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 2.0
    obj.data.materials.append(mat)
    return obj


# ── Energy curve ──────────────────────────────────────────────────────────────


def add_energy_curve(
    points: List[Tuple[float, float]],
    style: dict,
    x_scale: float = 8.0,
    x_offset: float = -4.0,
    y_offset: float = -3.0,
    z_scale: float = 0.3,
) -> object:
    """Create a Bezier spline for a reaction coordinate energy diagram."""
    import bpy
    import mathutils

    hex_color = style.get("colors", {}).get("energy_curve", "#f1c40f")
    r, g, b = hex_to_linear_rgb(hex_color)

    curve_data = bpy.data.curves.new("EnergyCurve", "CURVE")
    curve_data.dimensions = "3D"
    curve_data.bevel_depth = 0.03

    spline = curve_data.splines.new("BEZIER")
    if len(points) > 1:
        spline.bezier_points.add(len(points) - 1)

    for i, (progress, energy) in enumerate(points):
        bp = spline.bezier_points[i]
        bp.co = mathutils.Vector(
            (progress * x_scale + x_offset, y_offset, energy * z_scale)
        )
        bp.handle_right_type = "AUTO"
        bp.handle_left_type = "AUTO"

    obj = bpy.data.objects.new("EnergyCurve", curve_data)
    bpy.context.collection.objects.link(obj)

    mat = bpy.data.materials.new("EnergyCurveMat")
    mat.use_nodes = True
    bsdf = _principled_bsdf(mat)
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (r, g, b, 1.0)
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (r, g, b, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 3.0
    obj.data.materials.append(mat)
    return obj


def add_pointer_sphere(
    curve_obj,
    color: Tuple[float, float, float] = (1.0, 1.0, 0.0),
    radius: float = 0.12,
) -> object:
    """Sphere that follows a curve via Follow Path constraint."""
    import bpy

    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=(0, 0, 0))
    pointer = bpy.context.active_object
    pointer.name = "EnergyPointer"

    mat = bpy.data.materials.new("PointerMat")
    mat.use_nodes = True
    bsdf = _principled_bsdf(mat)
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        if "Emission Color" in bsdf.inputs:
            bsdf.inputs["Emission Color"].default_value = (*color, 1.0)
            bsdf.inputs["Emission Strength"].default_value = 5.0
    pointer.data.materials.append(mat)
    bpy.ops.object.shade_smooth()

    constraint = pointer.constraints.new(type="FOLLOW_PATH")
    constraint.target = curve_obj
    constraint.use_curve_follow = True

    # Animate offset: 0 at frame 1, -100 at last frame
    scene = bpy.context.scene
    constraint.offset = 0
    pointer.keyframe_insert(
        data_path='constraints["Follow Path"].offset', frame=scene.frame_start
    )
    constraint.offset = -100
    pointer.keyframe_insert(
        data_path='constraints["Follow Path"].offset', frame=scene.frame_end
    )

    return pointer
