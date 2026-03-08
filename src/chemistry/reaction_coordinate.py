"""Reaction coordinate utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class ReactionCoordinatePoint:
    progress: float
    free_energy: float


class ReactionCoordinate:
    def __init__(self, points: List[ReactionCoordinatePoint]):
        self.points = sorted(points, key=lambda p: p.progress)

    def sample(self, progress: float) -> ReactionCoordinatePoint:
        if not self.points:
            raise ValueError("No reaction coordinate defined")
        progress = min(max(progress, 0.0), 1.0)
        for i in range(1, len(self.points)):
            prev_pt = self.points[i - 1]
            next_pt = self.points[i]
            if progress <= next_pt.progress:
                span = next_pt.progress - prev_pt.progress or 1e-6
                alpha = (progress - prev_pt.progress) / span
                energy = prev_pt.free_energy + alpha * (next_pt.free_energy - prev_pt.free_energy)
                return ReactionCoordinatePoint(progress=progress, free_energy=energy)
        return self.points[-1]
