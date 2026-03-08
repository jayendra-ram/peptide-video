"""Reusable camera path helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


def ease_in_out(t: float) -> float:
    return t * t * (3 - 2 * t)


@dataclass
class CameraPath:
    """Simple parametric camera path for Blender scripts."""

    start: Tuple[float, float, float]
    end: Tuple[float, float, float]
    look_at: Tuple[float, float, float]

    def position_at(self, t: float) -> Tuple[float, float, float]:
        t = min(max(t, 0.0), 1.0)
        eased = ease_in_out(t)
        return tuple(s + (e - s) * eased for s, e in zip(self.start, self.end))  # type: ignore

    def as_dict(self) -> dict:
        return {
            "start": self.start,
            "end": self.end,
            "look_at": self.look_at,
        }
