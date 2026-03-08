"""Load scene specs from config/scene_specs.yaml.

Scene build() functions call ``load_spec(scene_id)`` to get text overlays,
camera settings, and visual descriptions that originate from script.md.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

ROOT = Path(__file__).resolve().parents[2]
SCENE_SPECS_PATH = ROOT / "config" / "scene_specs.yaml"

_cache: Optional[Dict[str, Any]] = None


def _load_all() -> Dict[str, Any]:
    global _cache
    if _cache is None:
        if SCENE_SPECS_PATH.exists():
            with SCENE_SPECS_PATH.open("r", encoding="utf-8") as f:
                _cache = yaml.safe_load(f) or {}
        else:
            _cache = {}
    return _cache


def load_spec(scene_id: str) -> Dict[str, Any]:
    """Return the spec dict for *scene_id*, or empty dict if missing."""
    return _load_all().get(scene_id, {})


def get_text_overlays(scene_id: str) -> List[Dict[str, Any]]:
    """Return list of text overlay dicts for a scene."""
    return load_spec(scene_id).get("text_overlays", [])


def get_camera(scene_id: str) -> Dict[str, Any]:
    """Return camera dict for a scene."""
    return load_spec(scene_id).get("camera", {})
