"""Wrapper around Manim CLI rendering."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional


class ManimRunner:
    def __init__(self, framework_root: Path):
        self.framework_root = framework_root

    def render_scene(
        self,
        scene_file: Path,
        class_name: str,
        output_path: Path,
        quality: str = "-qm",
        media_dir: Optional[Path] = None,
        extra_python_paths: Optional[list[Path]] = None,
    ) -> Optional[Path]:
        """Render a single Manim scene class and copy the output to *output_path*.

        Parameters
        ----------
        scene_file : Path
            Absolute path to the .py file containing the Scene subclass.
        class_name : str
            Name of the Scene subclass to render.
        output_path : Path
            Where to copy the rendered .mp4.
        quality : str
            Manim quality flag (e.g. ``-ql``, ``-qm``, ``-qh``).
        media_dir : Path, optional
            Where Manim writes intermediate media files.
        extra_python_paths : list[Path], optional
            Additional directories to add to PYTHONPATH.

        Returns the final output path on success, None on failure.
        """
        if media_dir is None:
            media_dir = self.framework_root / "output" / "media"

        paths = [str(self.framework_root)]
        for p in (extra_python_paths or []):
            paths.append(str(p))
        env = {**os.environ, "PYTHONPATH": os.pathsep.join(paths)}

        command = [
            "manim",
            "render",
            quality,
            "--media_dir",
            str(media_dir),
            str(scene_file),
            class_name,
        ]
        print(f"[manim] {' '.join(command)}")
        subprocess.run(command, check=True, cwd=str(self.framework_root), env=env)

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
