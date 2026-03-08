"""Wrapper around Manim CLI rendering."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from typing import Optional


# Scene class lookup: scene_id -> (module_path_relative_to_project, class_name)
SCENE_CLASS_MAP = {
    "scene_01_intro": ("src/scenes/scene_01_intro.py", "IntroScene"),
    "scene_02_reactants": ("src/scenes/scene_02_reactants.py", "ReactantsScene"),
    "scene_03_orbitals": ("src/scenes/scene_03_orbitals.py", "OrbitalsScene"),
    "scene_04_barrier": ("src/scenes/scene_04_barrier.py", "BarrierScene"),
    "scene_05_attack": ("src/scenes/scene_05_attack.py", "AttackScene"),
    "scene_06_water_loss": ("src/scenes/scene_06_water_loss.py", "WaterLossScene"),
    "scene_07_resonance": ("src/scenes/scene_07_resonance.py", "ResonanceScene"),
    "scene_08_biology": ("src/scenes/scene_08_biology.py", "BiologyScene"),
    "scene_09_summary": ("src/scenes/scene_09_summary.py", "SummaryScene"),
}


class ManimRunner:
    def __init__(self, project_root: Path):
        self.project_root = project_root

    def render_scene(
        self,
        scene_id: str,
        output_path: Path,
        quality: str = "-qm",
    ) -> Optional[Path]:
        """Render a single scene and copy the output to *output_path*.

        Returns the final output path on success, None on failure.
        """
        if scene_id not in SCENE_CLASS_MAP:
            print(f"[manim] Unknown scene_id: {scene_id}")
            return None

        module_file, class_name = SCENE_CLASS_MAP[scene_id]
        media_dir = self.project_root / "output" / "media"

        command = [
            "manim",
            "render",
            quality,
            "--media_dir",
            str(media_dir),
            str(self.project_root / module_file),
            class_name,
        ]
        print(f"[manim] {' '.join(command)}")
        subprocess.run(command, check=True, cwd=str(self.project_root))

        # Locate the rendered .mp4 — Manim places it under
        # media_dir/videos/<module_name>/<quality_dir>/<ClassName>.mp4
        rendered = self._find_rendered_file(media_dir, class_name)
        if rendered is None:
            print(f"[manim] Could not locate rendered file for {class_name}")
            return None

        output_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(rendered, output_path)
        print(f"[manim] Output: {output_path}")
        return output_path

    @staticmethod
    def _find_rendered_file(media_dir: Path, class_name: str) -> Optional[Path]:
        """Search the Manim media tree for the most recently rendered .mp4."""
        pattern = f"**/{class_name}.mp4"
        candidates = sorted(
            media_dir.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True
        )
        return candidates[0] if candidates else None
