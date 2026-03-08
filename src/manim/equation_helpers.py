"""Helper functions returning MathTex/Tex objects for chemical equations."""

from __future__ import annotations

from manim import MathTex, WHITE, ManimColor


def peptide_formation_equation(
    font_size: int = 30, color: ManimColor | str = WHITE,
) -> MathTex:
    """Overall condensation reaction for glycine dipeptide."""
    return MathTex(
        r"\text{H}_2\text{N-CH}_2\text{-COOH}",
        r"+",
        r"\text{H}_2\text{N-CH}_2\text{-COOH}",
        r"\rightarrow",
        r"\text{Gly-Gly}",
        r"+",
        r"\text{H}_2\text{O}",
        font_size=font_size,
        color=ManimColor(color),
    )


def condensation_short(
    font_size: int = 28, color: ManimColor | str = WHITE,
) -> MathTex:
    """Short form: 2 Gly -> Gly-Gly + H2O."""
    return MathTex(
        r"2\;\text{Gly}",
        r"\rightarrow",
        r"\text{Gly-Gly}",
        r"+",
        r"\text{H}_2\text{O}",
        font_size=font_size,
        color=ManimColor(color),
    )


def gibbs_equation(
    font_size: int = 32, color: ManimColor | str = WHITE,
) -> MathTex:
    return MathTex(
        r"\Delta G = \Delta H - T\Delta S",
        font_size=font_size,
        color=ManimColor(color),
    )


def arrhenius_equation(
    font_size: int = 32, color: ManimColor | str = WHITE,
) -> MathTex:
    return MathTex(
        r"k = A \, e^{-\Delta G^{\ddagger}/RT}",
        font_size=font_size,
        color=ManimColor(color),
    )


def equilibrium_equation(
    font_size: int = 32, color: ManimColor | str = WHITE,
) -> MathTex:
    return MathTex(
        r"\Delta G^{\circ} = -RT \ln K_{\text{eq}}",
        font_size=font_size,
        color=ManimColor(color),
    )


def atp_activation_equation(
    font_size: int = 26, color: ManimColor | str = WHITE,
) -> MathTex:
    return MathTex(
        r"\text{AA} + \text{ATP}",
        r"\xrightarrow{\text{synthetase}}",
        r"\text{aminoacyl-tRNA} + \text{AMP} + \text{PP}_i",
        font_size=font_size,
        color=ManimColor(color),
    )


def water_departure_equation(
    font_size: int = 28, color: ManimColor | str = WHITE,
) -> MathTex:
    return MathTex(
        r"\text{tetrahedral intermediate}",
        r"\xrightarrow{-\text{H}_2\text{O}}",
        r"\text{amide product}",
        font_size=font_size,
        color=ManimColor(color),
    )


def fmo_label(
    font_size: int = 26, color: ManimColor | str = WHITE,
) -> MathTex:
    return MathTex(
        r"\text{Frontier MO Theory: HOMO}_{\text{donor}}"
        r"\rightarrow \text{LUMO}_{\text{acceptor}}",
        font_size=font_size,
        color=ManimColor(color),
    )


def bond_order_annotation(
    label: str, order: str,
    font_size: int = 22, color: ManimColor | str = WHITE,
) -> MathTex:
    return MathTex(
        rf"\text{{{label}}}: {order}",
        font_size=font_size,
        color=ManimColor(color),
    )
