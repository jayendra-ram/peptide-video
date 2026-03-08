"""Material helpers for procedural Blender setups."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class MaterialPreset:
    name: str
    color: str
    roughness: float
    emission: float = 0.0


class MaterialLibrary:
    """Holds canonical colors so every scene stays consistent."""

    def __init__(self, style_config: Dict[str, str]):
        self.style = style_config

    def atom_material(self, symbol: str) -> MaterialPreset:
        color_key = f"atom_{symbol.lower()}"
        color = self.style.get("colors", {}).get(color_key, "#ffffff")
        return MaterialPreset(name=f"Atom_{symbol}", color=color, roughness=0.35)

    def orbital_material(self, role: str) -> MaterialPreset:
        color = self.style.get("colors", {}).get(f"orbital_{role}", "#aaaaaa")
        emission = 4.0 if role == "donor" else 2.5
        return MaterialPreset(name=f"Orbital_{role}", color=color, roughness=0.1, emission=emission)
