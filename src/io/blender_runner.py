"""Wrapper around Blender CLI rendering."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Dict, List


class BlenderRunner:
    def __init__(self, blender_config: Dict[str, str], project_root: Path):
        self.blender_config = blender_config
        self.project_root = project_root

    def render_scene(
        self, scene_module: str, output_dir: Path, preset: Dict[str, str]
    ) -> None:
        output_dir.mkdir(parents=True, exist_ok=True)
        command: List[str] = [
            self.blender_config.get("executable", "blender"),
            "-b",
            "--python",
            str(self.project_root / "scripts" / "render_scene.py"),
            "--",
            f"--scene={scene_module}",
            f"--output={output_dir}",
            f"--preset={json.dumps(preset)}",
        ]
        print("[blender]", " ".join(command))
        subprocess.run(command, check=True)
