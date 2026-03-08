"""Orbital proxies used for visualization."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Orbital:
    label: str
    occupancy: float
    energy_level: float
    role: str  # donor or acceptor

    def activation_strength(self) -> float:
        return self.occupancy - self.energy_level if self.role == "donor" else self.energy_level
