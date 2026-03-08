"""Fallback scene renderer that produces text plates via FFmpeg."""

from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path
from typing import Dict


def escape_drawtext(text: str) -> str:
    """Escape characters for FFmpeg drawtext."""
    escaped = (
        text.replace("\\", r"\\")
        .replace(":", r"\:")
        .replace("'", r"\'")
        .replace("%", r"\%")
    )
    return escaped.replace("\n", r"\n")


def wrap_voiceover(text: str, width: int = 56) -> str:
    lines = textwrap.wrap(text, width)
    return "\n".join(lines)


class PlaceholderRenderer:
    """Render storyboard slides when Blender is unavailable."""

    def __init__(
        self,
        ffmpeg: str,
        resolution: str,
        fps: int,
        background: str,
        fontfile: str | None = None,
    ):
        self.ffmpeg = ffmpeg
        self.resolution = resolution
        self.fps = fps
        self.background = background
        if fontfile and Path(fontfile).exists():
            self.fontfile = fontfile
        else:
            self.fontfile = self._default_font()

    def render_scene(self, scene: Dict, output_path: Path) -> None:
        duration = float(scene["duration_seconds"])
        label = scene.get("label", scene["id"])
        voiceover = wrap_voiceover(scene["voiceover"].strip())

        drawtext_title = (
            "drawtext="
            f"fontfile='{self.fontfile}':"
            f"text='{escape_drawtext(label)}':"
            "fontcolor=white:"
            "fontsize=72:"
            "x=(w-text_w)/2:"
            "y=h*0.08"
        )
        drawtext_body = (
            "drawtext="
            f"fontfile='{self.fontfile}':"
            f"text='{escape_drawtext(voiceover)}':"
            "fontcolor=white:"
            "fontsize=48:"
            "line_spacing=14:"
            "x=(w-text_w)/2:"
            "y=h*0.25"
        )
        filter_str = f"{drawtext_title},{drawtext_body}"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        command = [
            self.ffmpeg,
            "-y",
            "-f",
            "lavfi",
            "-i",
            f"color=c={self.background}:s={self.resolution}:d={duration}",
            "-vf",
            filter_str,
            "-r",
            str(self.fps),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(output_path),
        ]
        print("[placeholder]", " ".join(command))
        subprocess.run(command, check=True)

    def _default_font(self) -> str:
        candidates = [
            Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
            Path("/System/Library/Fonts/Supplemental/Helvetica.ttc"),
        ]
        for candidate in candidates:
            if candidate.exists():
                return str(candidate)
        raise FileNotFoundError("No default font found for placeholder renderer")
