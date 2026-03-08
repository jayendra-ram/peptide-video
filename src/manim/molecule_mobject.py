"""2D ball-and-stick molecule mobject built from MolGeom data."""

from __future__ import annotations

from typing import Dict, Optional, Tuple

from manim import (
    VGroup,
    Circle,
    Line,
    DashedLine,
    Text,
    WHITE,
    GREY,
    ManimColor,
    np,
)

from src.chemistry.molecules import MolGeom

# Default colors & radii (overridden by scene style)
_DEFAULT_COLORS = {
    "C": "#7f8c8d",
    "H": "#ecf0f1",
    "O": "#e74c3c",
    "N": "#3498db",
}
_DEFAULT_RADII = {"H": 0.15, "C": 0.25, "N": 0.23, "O": 0.22}


class MoleculeMobject(VGroup):
    """Draw a 2D ball-and-stick molecule from a ``MolGeom`` dataclass.

    Uses x, y from the 3D coordinates (z is ignored for 2D projection).
    """

    def __init__(
        self,
        geom: MolGeom,
        atom_colors: Optional[Dict[str, ManimColor]] = None,
        atom_radii: Optional[Dict[str, float]] = None,
        show_labels: bool = True,
        show_bonds: bool = True,
        scale_factor: float = 1.0,
        offset: Tuple[float, float, float] = (0, 0, 0),
        label_font_size: int = 18,
    ) -> None:
        super().__init__()
        self._atom_colors = atom_colors or {
            k: ManimColor(v) for k, v in _DEFAULT_COLORS.items()
        }
        self._atom_radii = atom_radii or dict(_DEFAULT_RADII)
        self.atom_mobjects: Dict[str, Circle] = {}
        self.label_mobjects: Dict[str, Text] = {}
        self.bond_mobjects: Dict[Tuple[str, str], VGroup] = {}
        self._geom = geom

        # Build bonds first (so atoms draw on top)
        if show_bonds:
            for label_a, label_b, order in geom.bonds:
                pos_a = self._atom_pos(geom, label_a, offset, scale_factor)
                pos_b = self._atom_pos(geom, label_b, offset, scale_factor)
                bond_group = self._make_bond(pos_a, pos_b, order)
                self.bond_mobjects[(label_a, label_b)] = bond_group
                self.add(bond_group)

        # Build atoms
        for label, symbol, (x, y, _z) in geom.atoms:
            pos = np.array([
                (x + offset[0]) * scale_factor,
                (y + offset[1]) * scale_factor,
                0,
            ])
            radius = self._atom_radii.get(symbol, 0.2) * scale_factor
            color = self._atom_colors.get(symbol, GREY)

            circle = Circle(
                radius=radius,
                fill_color=color,
                fill_opacity=0.9,
                stroke_color=WHITE,
                stroke_width=1.5,
            ).move_to(pos)
            self.atom_mobjects[label] = circle
            self.add(circle)

            if show_labels and symbol != "H":
                txt = Text(
                    symbol,
                    font_size=label_font_size * scale_factor,
                    color=WHITE,
                    weight="BOLD",
                ).move_to(pos)
                self.label_mobjects[label] = txt
                self.add(txt)

    # ── helpers ──────────────────────────────────────────────────────────

    @staticmethod
    def _atom_pos(
        geom: MolGeom,
        label: str,
        offset: Tuple[float, float, float],
        scale: float,
    ) -> np.ndarray:
        for lbl, _sym, (x, y, _z) in geom.atoms:
            if lbl == label:
                return np.array([(x + offset[0]) * scale, (y + offset[1]) * scale, 0])
        return np.array([0, 0, 0])

    @staticmethod
    def _make_bond(
        pos_a: np.ndarray,
        pos_b: np.ndarray,
        order: float,
    ) -> VGroup:
        group = VGroup()
        direction = pos_b - pos_a
        length = float(np.linalg.norm(direction))
        if length < 1e-6:
            return group

        perp = np.array([-direction[1], direction[0], 0])
        perp = perp / (np.linalg.norm(perp) + 1e-9)

        if order >= 1.8:
            # Double bond: two lines offset
            for off in [0.04, -0.04]:
                shift = perp * off
                line = Line(pos_a + shift, pos_b + shift, stroke_width=2.5, color=GREY)
                group.add(line)
        elif 1.3 <= order < 1.8:
            # Partial double bond: one solid + one dashed
            group.add(Line(pos_a, pos_b, stroke_width=2.5, color=GREY))
            shift = perp * 0.06
            group.add(
                DashedLine(
                    pos_a + shift,
                    pos_b + shift,
                    stroke_width=2,
                    color=GREY,
                    dash_length=0.06,
                )
            )
        elif 0.3 <= order < 1.0:
            # Forming bond: dashed
            group.add(
                DashedLine(
                    pos_a,
                    pos_b,
                    stroke_width=2,
                    color=GREY,
                    dash_length=0.08,
                )
            )
        else:
            # Single bond
            group.add(Line(pos_a, pos_b, stroke_width=2.5, color=GREY))

        return group

    def get_atom(self, label: str) -> Circle:
        """Return the Circle mobject for a given atom label."""
        return self.atom_mobjects[label]

    def get_atom_center(self, label: str) -> np.ndarray:
        """Return the center position of an atom."""
        return self.atom_mobjects[label].get_center()
