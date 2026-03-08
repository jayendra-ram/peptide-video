#!/usr/bin/env python3
"""Parse script.md and sync narration/duration/visuals into the animation pipeline.

Reads the markdown script file and:
  1. Updates config/project.yaml  (voiceover text + duration per scene)
  2. Writes  config/scene_specs.yaml  (structured visual descriptions for scene code)

Usage:
    python scripts/sync_script.py                 # sync everything
    python scripts/sync_script.py --dry-run       # show what would change
    python scripts/sync_script.py --spec-only     # only write scene_specs.yaml
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "script.md"
PROJECT_YAML = ROOT / "config" / "project.yaml"
SCENE_SPECS_YAML = ROOT / "config" / "scene_specs.yaml"


# ---------------------------------------------------------------------------
# Markdown parser
# ---------------------------------------------------------------------------

_SCENE_HEADING = re.compile(
    r"^##\s+Scene\s+(\d+):\s+(.+)$", re.MULTILINE
)
_ID_COMMENT = re.compile(r"<!--\s*id:\s*(\S+)\s*-->")
_DURATION = re.compile(r"\*\*Duration:\*\*\s*([\d.]+)\s*s")

# Overlay line:  - [0.5s–4.0s] "text" — size 0.14, position (x, y, z)
# Also handles percentage notation like [40%–80%] and bare [1.5s]
_OVERLAY = re.compile(
    r'-\s*\[([^\]]+)\]\s*"([^"]+)"\s*(?:—|--)\s*size\s+([\d.]+)'
    r'(?:,\s*position\s*\(([^)]+)\))?'
)

# Camera lines
_CAM_START = re.compile(
    r'(?:Start|Static):\s*\(([^)]+)\)\s*looking\s+at\s*\(([^)]+)\)'
    r'(?:.*?FOV\s*([\d.]+))?',
    re.IGNORECASE,
)
_CAM_END = re.compile(
    r'End:\s*\(([^)]+)\)', re.IGNORECASE
)


def _parse_tuple(s: str) -> List[float]:
    return [float(x.strip()) for x in s.split(",")]


def _parse_time_range(raw: str, duration: float) -> dict:
    """Parse time range like '0.5s–4.0s', '40%–80%', '1.5s', 'start–end'."""
    raw = raw.strip()
    parts = re.split(r"[–\-]", raw, maxsplit=1)

    def _to_seconds(token: str) -> Optional[float]:
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
    return {"start_time": round(start, 2), "end_time": round(end, 2)}


def parse_script(text: str) -> List[Dict[str, Any]]:
    """Split script.md into a list of scene dicts."""
    # Split on scene headings
    heading_matches = list(_SCENE_HEADING.finditer(text))
    scenes: List[Dict[str, Any]] = []

    for idx, match in enumerate(heading_matches):
        start = match.start()
        end = heading_matches[idx + 1].start() if idx + 1 < len(heading_matches) else len(text)
        block = text[start:end]

        scene: Dict[str, Any] = {
            "number": int(match.group(1)),
            "label": match.group(2).strip(),
        }

        # Scene ID
        id_match = _ID_COMMENT.search(block)
        if id_match:
            scene["id"] = id_match.group(1)

        # Duration
        dur_match = _DURATION.search(block)
        if dur_match:
            scene["duration_seconds"] = float(dur_match.group(1))
        duration = scene.get("duration_seconds", 10.0)

        # Narration — text between ### Narration and the next ###
        narr_match = re.search(
            r"###\s*Narration\s*\n(.*?)(?=\n###|\n---|\Z)",
            block, re.DOTALL,
        )
        if narr_match:
            scene["voiceover"] = narr_match.group(1).strip() + "\n"

        # Visuals — raw text between ### Visuals and next ###
        vis_match = re.search(
            r"###\s*Visuals\s*\n(.*?)(?=\n###|\n---|\Z)",
            block, re.DOTALL,
        )
        if vis_match:
            scene["visuals"] = vis_match.group(1).strip()

        # Text Overlays — structured parse
        overlay_section = re.search(
            r"###\s*Text Overlays\s*\n(.*?)(?=\n###|\n---|\Z)",
            block, re.DOTALL,
        )
        overlays = []
        if overlay_section:
            for m in _OVERLAY.finditer(overlay_section.group(1)):
                overlay: Dict[str, Any] = {
                    **_parse_time_range(m.group(1), duration),
                    "text": m.group(2),
                    "size": float(m.group(3)),
                }
                if m.group(4):
                    overlay["position"] = _parse_tuple(m.group(4))
                overlays.append(overlay)
        scene["text_overlays"] = overlays

        # Camera
        cam_section = re.search(
            r"###\s*Camera\s*\n(.*?)(?=\n###|\n---|\Z)",
            block, re.DOTALL,
        )
        camera: Dict[str, Any] = {}
        if cam_section:
            cam_text = cam_section.group(1)
            sm = _CAM_START.search(cam_text)
            if sm:
                camera["start_location"] = _parse_tuple(sm.group(1))
                camera["look_at"] = _parse_tuple(sm.group(2))
                if sm.group(3):
                    camera["fov_deg"] = float(sm.group(3))
            em = _CAM_END.search(cam_text)
            if em:
                camera["end_location"] = _parse_tuple(em.group(1))
        scene["camera"] = camera

        scenes.append(scene)

    return scenes


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------

def update_project_yaml(scenes: List[Dict[str, Any]], dry_run: bool = False) -> List[str]:
    """Update config/project.yaml voiceover and duration from parsed scenes."""
    with PROJECT_YAML.open("r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)

    changes: List[str] = []
    yaml_scenes = doc.get("scenes", [])
    scene_map = {s["id"]: s for s in yaml_scenes}

    for parsed in scenes:
        sid = parsed.get("id")
        if not sid or sid not in scene_map:
            continue
        target = scene_map[sid]

        # Voiceover
        new_vo = parsed.get("voiceover", "")
        old_vo = target.get("voiceover", "")
        if new_vo.strip() != old_vo.strip():
            changes.append(f"  {sid}: voiceover updated")
            if not dry_run:
                target["voiceover"] = new_vo

        # Duration
        new_dur = parsed.get("duration_seconds")
        old_dur = target.get("duration_seconds")
        if new_dur and new_dur != old_dur:
            changes.append(f"  {sid}: duration {old_dur}s -> {new_dur}s")
            if not dry_run:
                target["duration_seconds"] = int(new_dur) if new_dur == int(new_dur) else new_dur

        # Label
        new_label = parsed.get("label")
        old_label = target.get("label")
        if new_label and new_label != old_label:
            changes.append(f"  {sid}: label '{old_label}' -> '{new_label}'")
            if not dry_run:
                target["label"] = new_label

    if not dry_run and changes:
        with PROJECT_YAML.open("w", encoding="utf-8") as f:
            yaml.dump(doc, f, default_flow_style=False, sort_keys=False, allow_unicode=True, width=100)

    return changes


def write_scene_specs(scenes: List[Dict[str, Any]], dry_run: bool = False) -> Path:
    """Write config/scene_specs.yaml with structured visual descriptions."""
    specs: Dict[str, Any] = {}

    for parsed in scenes:
        sid = parsed.get("id")
        if not sid:
            continue

        spec: Dict[str, Any] = {
            "label": parsed.get("label", ""),
            "duration_seconds": parsed.get("duration_seconds", 10),
        }

        if parsed.get("visuals"):
            spec["visuals"] = parsed["visuals"]

        if parsed.get("text_overlays"):
            spec["text_overlays"] = parsed["text_overlays"]

        if parsed.get("camera"):
            spec["camera"] = parsed["camera"]

        specs[sid] = spec

    if not dry_run:
        SCENE_SPECS_YAML.parent.mkdir(parents=True, exist_ok=True)
        with SCENE_SPECS_YAML.open("w", encoding="utf-8") as f:
            yaml.dump(
                specs, f,
                default_flow_style=False,
                sort_keys=False,
                allow_unicode=True,
                width=120,
            )

    return SCENE_SPECS_YAML


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Sync script.md -> animation pipeline")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument("--spec-only", action="store_true", help="Only write scene_specs.yaml")
    args = parser.parse_args()

    if not SCRIPT_PATH.exists():
        print(f"Error: {SCRIPT_PATH} not found", file=sys.stderr)
        sys.exit(1)

    text = SCRIPT_PATH.read_text(encoding="utf-8")
    scenes = parse_script(text)
    print(f"Parsed {len(scenes)} scenes from script.md")

    if args.dry_run:
        print("\n--- DRY RUN ---")

    # 1. Update project.yaml (voiceover + duration)
    if not args.spec_only:
        changes = update_project_yaml(scenes, dry_run=args.dry_run)
        if changes:
            print(f"\nproject.yaml changes:")
            for c in changes:
                print(c)
        else:
            print("\nproject.yaml: no changes needed")

    # 2. Write scene_specs.yaml
    path = write_scene_specs(scenes, dry_run=args.dry_run)
    if not args.dry_run:
        print(f"\nScene specs written to {path}")
    else:
        print(f"\nWould write scene specs to {path}")

    print("\nDone.")


if __name__ == "__main__":
    main()
