"""Bond definitions and order animation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Bond:
    atom_a: str
    atom_b: str
    order: float

    def lerp_order(self, other: "Bond", t: float) -> float:
        t = min(max(t, 0.0), 1.0)
        return self.order + (other.order - self.order) * t
