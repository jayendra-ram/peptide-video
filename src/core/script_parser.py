"""Parse a project's script.md into structured scene data.

This is the single source of truth parser -- it replaces sync_script.py,
scene_spec.py, and project.yaml. The markdown file defines everything:
narration, timing, visuals, overlays, camera, and render backend.

Usage:
    from src.core.script_parser import parse_script
    scenes = parse_script(Path("projects/my_video/script.md"))
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class RenderDirective:
    """Which backend renders this scene's visuals."""
    type: str   # "manim", "video", "image", "blender", "placeholder"
    ref: str    # class name, file path, etc.


@dataclass
class TextOverlay:
    start_time: float
    end_time: float
    text: str
    size: float
    position: Optional[tuple[float, float, float]] = None


@dataclass
class CameraSpec:
    start_location: Optional[tuple[float, float, float]] = None
    end_location: Optional[tuple[float, float, float]] = None
    look_at: Optional[tuple[float, float, float]] = None
    fov_deg: Optional[float] = None


@dataclass
class ParsedScene:
    number: int
    id: str
    label: str
    duration_seconds: float
    render: RenderDirective
    voiceover: str = ""
    visuals: str = ""
    text_overlays: List[TextOverlay] = field(default_factory=list)
    camera: CameraSpec = field(default_factory=CameraSpec)


# ---------------------------------------------------------------------------
# Regex patterns
# ---------------------------------------------------------------------------

_SCENE_HEADING = re.compile(
    r"^##\s+Scene\s+(\d+):\s+(.+)$", re.MULTILINE
)
_ID_COMMENT = re.compile(r"<!--\s*id:\s*(\S+)\s*-->")
_RENDER_COMMENT = re.compile(r"<!--\s*render:\s*(\S+?)(?::(\S+))?\s*-->")
_DURATION = re.compile(r"\*\*Duration:\*\*\s*([\d.]+)\s*s")

_OVERLAY = re.compile(
    r'-\s*\[([^\]]+)\]\s*"([^"]+)"\s*(?:—|--)\s*size\s+([\d.]+)'
    r"(?:,\s*position\s*\(([^)]+)\))?"
)

_CAM_START = re.compile(
    r"(?:Start|Static):\s*\(([^)]+)\)\s*looking\s+at\s*\(([^)]+)\)"
    r"(?:.*?FOV\s*([\d.]+))?",
    re.IGNORECASE,
)
_CAM_END = re.compile(r"End:\s*\(([^)]+)\)", re.IGNORECASE)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_tuple(s: str) -> tuple[float, float, float]:
    vals = [float(x.strip()) for x in s.split(",")]
    while len(vals) < 3:
        vals.append(0.0)
    return (vals[0], vals[1], vals[2])


def _parse_time_range(raw: str, duration: float) -> tuple[float, float]:
    raw = raw.strip()
    parts = re.split(r"[–\-]", raw, maxsplit=1)

    def _to_seconds(token: str) -> float:
        token = token.strip().lower()
        if token in ("start", ""):
            return 0.0
        if token == "end":
            return duration
        if token.endswith("%"):
            return duration * float(token[:-1]) / 100.0
        if token.endswith("s"):
            return float(token[:-1])
        return float(token)

    start = _to_seconds(parts[0])
    end = _to_seconds(parts[1]) if len(parts) > 1 else duration
    return (round(start, 2), round(end, 2))


def _extract_section(block: str, heading: str) -> str:
    """Extract raw text from a ### section within a scene block."""
    pattern = rf"###\s*{re.escape(heading)}\s*\n(.*?)(?=\n###|\n---|\Z)"
    match = re.search(pattern, block, re.DOTALL)
    return match.group(1).strip() if match else ""


# ---------------------------------------------------------------------------
# Main parser
# ---------------------------------------------------------------------------

def parse_script(script_path: Path) -> List[ParsedScene]:
    """Parse a script.md file into a list of ParsedScene objects."""
    text = script_path.read_text(encoding="utf-8")
    heading_matches = list(_SCENE_HEADING.finditer(text))
    scenes: List[ParsedScene] = []

    for idx, match in enumerate(heading_matches):
        start = match.start()
        end = (
            heading_matches[idx + 1].start()
            if idx + 1 < len(heading_matches)
            else len(text)
        )
        block = text[start:end]

        # Scene ID
        id_match = _ID_COMMENT.search(block)
        scene_id = id_match.group(1) if id_match else f"scene_{match.group(1):>02s}"

        # Render directive
        render_match = _RENDER_COMMENT.search(block)
        if render_match:
            render = RenderDirective(
                type=render_match.group(1),
                ref=render_match.group(2) or "",
            )
        else:
            render = RenderDirective(type="placeholder", ref="")

        # Duration
        dur_match = _DURATION.search(block)
        duration = float(dur_match.group(1)) if dur_match else 10.0

        # Narration
        voiceover = _extract_section(block, "Narration")
        if voiceover:
            voiceover += "\n"

        # Visuals
        visuals = _extract_section(block, "Visuals")

        # Text Overlays
        overlay_section = _extract_section(block, "Text Overlays")
        overlays: List[TextOverlay] = []
        for m in _OVERLAY.finditer(overlay_section):
            start_t, end_t = _parse_time_range(m.group(1), duration)
            overlay = TextOverlay(
                start_time=start_t,
                end_time=end_t,
                text=m.group(2),
                size=float(m.group(3)),
                position=_parse_tuple(m.group(4)) if m.group(4) else None,
            )
            overlays.append(overlay)

        # Camera
        cam_text = _extract_section(block, "Camera")
        camera = CameraSpec()
        if cam_text:
            sm = _CAM_START.search(cam_text)
            if sm:
                camera.start_location = _parse_tuple(sm.group(1))
                camera.look_at = _parse_tuple(sm.group(2))
                if sm.group(3):
                    camera.fov_deg = float(sm.group(3))
            em = _CAM_END.search(cam_text)
            if em:
                camera.end_location = _parse_tuple(em.group(1))

        scenes.append(ParsedScene(
            number=int(match.group(1)),
            id=scene_id,
            label=match.group(2).strip(),
            duration_seconds=duration,
            render=render,
            voiceover=voiceover,
            visuals=visuals,
            text_overlays=overlays,
            camera=camera,
        ))

    return scenes
