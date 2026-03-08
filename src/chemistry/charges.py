"""Charge distribution helpers."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PartialCharge:
    atom_label: str
    magnitude: float

    def color_hint(self) -> str:
        return "positive" if self.magnitude > 0 else "negative"
