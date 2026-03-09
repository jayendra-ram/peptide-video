"""Wrapper around Blender CLI rendering.

Runs a Blender Python script in headless mode, passing scene parameters
(output path, duration, fps, resolution) as command-line arguments.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional


class BlenderRunner:
    def __init__(self, executable: str = "blender"):
        self.executable = executable

    def render_script(
        self,
        script_path: Path,
        output_path: Path,
        duration: float,
        fps: int = 30,
        resolution: str = "1920x1080",
    ) -> Optional[Path]:
        output_path = Path(output_path).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)
        command = [
            self.executable,
            "-b",                # background (headless)
            "--python", str(Path(script_path).resolve()),
            "--",                # separator for script args
            "--output", str(output_path),
            "--duration", str(duration),
            "--fps", str(fps),
            "--resolution", resolution,
        ]
        print(f"[blender] {' '.join(command)}")
        result = subprocess.run(command, capture_output=True, text=True)

        # Check for errors in output (Blender may return 0 even on script errors)
        if result.returncode != 0 or "Traceback" in result.stderr or "Error" in result.stderr:
            print(f"[blender] stdout:\n{result.stdout[-2000:]}")
            print(f"[blender] stderr:\n{result.stderr[-2000:]}")
            if not output_path.exists():
                raise RuntimeError(f"Blender script failed: {script_path}")

        if not output_path.exists():
            raise RuntimeError(
                f"Blender script completed but output not found: {output_path}"
            )

        print(f"[blender] Rendered → {output_path}")
        return output_path
