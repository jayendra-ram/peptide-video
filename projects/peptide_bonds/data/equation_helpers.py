"""Peptide-bond-specific equation Text objects for Manim scenes."""

from __future__ import annotations

from manim import Text, WHITE, ManimColor


def peptide_formation_equation(
    font_size: int = 30, color: ManimColor | str = WHITE,
) -> Text:
    """Overall condensation reaction for glycine dipeptide."""
    return Text(
        "H\u2082N-CH\u2082-COOH + H\u2082N-CH\u2082-COOH \u2192 Gly-Gly + H\u2082O",
        font_size=font_size,
        color=ManimColor(color),
    )


def condensation_short(
    font_size: int = 28, color: ManimColor | str = WHITE,
) -> Text:
    """Short form: 2 Gly -> Gly-Gly + H2O."""
    return Text(
        "2 Gly \u2192 Gly-Gly + H\u2082O",
        font_size=font_size,
        color=ManimColor(color),
    )


def atp_activation_equation(
    font_size: int = 26, color: ManimColor | str = WHITE,
) -> Text:
    return Text(
        "AA + ATP \u2192[synthetase] aminoacyl-tRNA + AMP + PP\u1d62",
        font_size=font_size,
        color=ManimColor(color),
    )


def water_departure_equation(
    font_size: int = 28, color: ManimColor | str = WHITE,
) -> Text:
    return Text(
        "tetrahedral intermediate \u2192[\u2212H\u2082O] amide product",
        font_size=font_size,
        color=ManimColor(color),
    )
