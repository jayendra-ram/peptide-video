"""Curly arrow for electron-flow mechanism diagrams."""

from __future__ import annotations

from manim import (
    VGroup,
    ArcBetweenPoints,
    Triangle,
    PI,
    np,
    ManimColor,
)


class CurlyArrow(VGroup):
    """Curved arrow showing electron pair movement in reaction mechanisms.

    Standard organic chemistry convention: tail at electron source, head at
    electron sink.
    """

    def __init__(
        self,
        start: np.ndarray,
        end: np.ndarray,
        color: ManimColor | str = "#f1c40f",
        angle: float = PI / 3,
        stroke_width: float = 3,
        tip_length: float = 0.12,
    ) -> None:
        super().__init__()
        start = np.array(start, dtype=float)
        end = np.array(end, dtype=float)

        arc = ArcBetweenPoints(start, end, angle=angle)
        arc.set_color(ManimColor(color))
        arc.set_stroke(width=stroke_width)
        self.add(arc)

        # Arrowhead at the end of the arc
        tip = Triangle(fill_opacity=1, fill_color=ManimColor(color), stroke_width=0)
        tip.scale(tip_length)

        # Orient the tip along the arc's tangent at the endpoint
        end_tangent = arc.get_end() - arc.point_from_proportion(0.95)
        angle_rad = float(np.arctan2(end_tangent[1], end_tangent[0]))
        tip.rotate(angle_rad - PI / 2)
        tip.move_to(arc.get_end())
        self.add(tip)

        self.arc = arc
        self.tip = tip
