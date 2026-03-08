"""Basic atom building blocks for molecules."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass
class Atom:
    symbol: str
    position: Tuple[float, float, float]
    partial_charge: float = 0.0

    def translate(self, dx: float, dy: float, dz: float) -> "Atom":
        x, y, z = self.position
        return Atom(symbol=self.symbol, position=(x + dx, y + dy, z + dz), partial_charge=self.partial_charge)
