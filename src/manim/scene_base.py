"""Base scene class for educational explainer Manim scenes."""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Optional

import yaml
from manim import MovingCameraScene, ManimColor


def _find_style_yaml(start: Path) -> Optional[Path]:
    """Walk up from *start* looking for config/style.yaml."""
    current = start
    for _ in range(10):
        candidate = current / "config" / "style.yaml"
        if candidate.exists():
            return candidate
        parent = current.parent
        if parent == current:
            break
        current = parent
    return None


class ExplainerSceneBase(MovingCameraScene):
    """Shared setup for educational explainer videos.

    Loads style.yaml from the nearest ``config/`` directory (searching
    upward from the scene file) and exposes color/radius constants.

    Subclasses override ``construct()`` to define the animation.
    """

    style_path: ClassVar[Optional[Path]] = None

    def setup(self) -> None:
        super().setup()
        path = self.style_path or _find_style_yaml(
            Path(__file__).resolve().parent
        )
        if path and path.exists():
            with path.open("r", encoding="utf-8") as fh:
                self.style = yaml.safe_load(fh)
        else:
            self.style = {}

        colors = self.style.get("colors", {})

        self.camera.background_color = ManimColor(
            colors.get("background", "#05060a")
        )

        self.ATOM_COLORS = {
            "C": ManimColor(colors.get("atom_c", "#7f8c8d")),
            "H": ManimColor(colors.get("atom_h", "#ecf0f1")),
            "O": ManimColor(colors.get("atom_o", "#e74c3c")),
            "N": ManimColor(colors.get("atom_n", "#3498db")),
        }
        self.ATOM_RADII = {"H": 0.15, "C": 0.25, "N": 0.23, "O": 0.22}

        self.ORBITAL_DONOR = ManimColor(colors.get("orbital_donor", "#6c5ce7"))
        self.ORBITAL_ACCEPTOR = ManimColor(colors.get("orbital_acceptor", "#f39c12"))
        self.CHARGE_POS = ManimColor(colors.get("charge_positive", "#f5b041"))
        self.CHARGE_NEG = ManimColor(colors.get("charge_negative", "#5dade2"))
        self.ENERGY_COLOR = ManimColor(colors.get("energy_curve", "#f1c40f"))


# Backward-compatible alias
PeptideSceneBase = ExplainerSceneBase
