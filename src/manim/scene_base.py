"""Base scene class for all peptide bond Manim scenes."""

from __future__ import annotations

from pathlib import Path

import yaml
from manim import Scene, MovingCameraScene, config, ManimColor


ROOT = Path(__file__).resolve().parents[2]


def _load_style() -> dict:
    path = ROOT / "config" / "style.yaml"
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


class PeptideSceneBase(MovingCameraScene):
    """Shared setup for every scene in the peptide bond video."""

    def setup(self) -> None:
        super().setup()
        self.style = _load_style()
        colors = self.style["colors"]

        self.camera.background_color = ManimColor(colors["background"])

        self.ATOM_COLORS = {
            "C": ManimColor(colors["atom_c"]),
            "H": ManimColor(colors["atom_h"]),
            "O": ManimColor(colors["atom_o"]),
            "N": ManimColor(colors["atom_n"]),
        }
        self.ATOM_RADII = {"H": 0.15, "C": 0.25, "N": 0.23, "O": 0.22}

        self.ORBITAL_DONOR = ManimColor(colors["orbital_donor"])
        self.ORBITAL_ACCEPTOR = ManimColor(colors["orbital_acceptor"])
        self.CHARGE_POS = ManimColor(colors["charge_positive"])
        self.CHARGE_NEG = ManimColor(colors["charge_negative"])
        self.ENERGY_COLOR = ManimColor(colors["energy_curve"])
