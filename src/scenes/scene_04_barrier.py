"""Scene 4: free-energy barrier.

Reaction coordinate curve in 3D space with animated pointer. Static molecules.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

SCENE_ID = "scene_04_barrier"


def build(scene_ctx: Dict[str, Any]) -> None:
    style = scene_ctx["style"]
    preset = scene_ctx["preset"]
    fps = scene_ctx.get("fps", 30)
    duration = scene_ctx.get("duration_seconds", 20)

    from src.core.blender_scene import (
        add_energy_curve,
        add_pointer_sphere,
        add_text_overlay,
        setup_camera,
        setup_lighting,
        setup_scene,
    )
    from src.chemistry.molecules import GLYCINE_A_REACTANT, draw_molecule
    from src.chemistry.reaction_coordinate import (
        ReactionCoordinate,
        ReactionCoordinatePoint,
    )

    setup_scene(preset, style, fps=fps, duration_seconds=duration)
    setup_lighting()

    # Build energy profile
    coordinate = ReactionCoordinate(
        points=[
            ReactionCoordinatePoint(progress=0.0, free_energy=1.0),
            ReactionCoordinatePoint(progress=0.2, free_energy=2.0),
            ReactionCoordinatePoint(progress=0.4, free_energy=6.5),
            ReactionCoordinatePoint(progress=0.5, free_energy=7.0),
            ReactionCoordinatePoint(progress=0.6, free_energy=6.5),
            ReactionCoordinatePoint(progress=0.8, free_energy=1.5),
            ReactionCoordinatePoint(progress=1.0, free_energy=0.0),
        ]
    )
    samples = [
        (coordinate.sample(p / 30).progress, coordinate.sample(p / 30).free_energy)
        for p in range(31)
    ]

    curve_obj = add_energy_curve(
        samples, style, x_scale=6.0, x_offset=-3.0, y_offset=0.0, z_scale=0.25
    )
    add_pointer_sphere(curve_obj, radius=0.1)

    # Labels
    add_text_overlay("Reaction Progress →", location=(-2.5, 0, -0.8), size=0.12)
    add_text_overlay("Free Energy ↑", location=(-3.8, 0, 0.5), size=0.10)
    add_text_overlay("Activation\nBarrier", location=(0.0, 0, 2.2), size=0.14)

    # Small static molecule on the left
    draw_molecule(
        GLYCINE_A_REACTANT, style, offset=(-5.5, 0, -1.5), label_prefix="S4_"
    )

    # Molecule description
    add_text_overlay(
        "Gly-COOH + H2N-Gly: dG barrier ~80 kJ/mol in water",
        location=(-4.0, 0, -1.8), size=0.09,
    )

    cam = setup_camera((0, -8, 3), (0, 0, 0.5), fov_deg=35)
