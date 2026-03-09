"""Config loading with project-level overrides.

Framework defaults live in config/. A project can override any key by
placing a file with the same name in its own config/ directory.
"""

from __future__ import annotations

import copy
from pathlib import Path
from typing import Any, Dict

import yaml


def deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge *override* into a copy of *base*."""
    merged = copy.deepcopy(base)
    for key, value in override.items():
        if (
            key in merged
            and isinstance(merged[key], dict)
            and isinstance(value, dict)
        ):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = copy.deepcopy(value)
    return merged


def load_config(
    framework_root: Path,
    project_dir: Path,
    filename: str,
) -> Dict[str, Any]:
    """Load a YAML config, merging project overrides on top of framework defaults."""
    default_path = framework_root / "config" / filename
    if not default_path.exists():
        default = {}
    else:
        with default_path.open("r", encoding="utf-8") as fh:
            default = yaml.safe_load(fh) or {}

    project_path = project_dir / "config" / filename
    if project_path.exists():
        with project_path.open("r", encoding="utf-8") as fh:
            override = yaml.safe_load(fh) or {}
        return deep_merge(default, override)

    return default
