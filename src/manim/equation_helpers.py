"""Generic equation Text objects for Manim scenes (Unicode, no LaTeX)."""

from __future__ import annotations

from manim import Text, WHITE, ManimColor


def gibbs_equation(
    font_size: int = 32, color: ManimColor | str = WHITE,
) -> Text:
    return Text(
        "\u0394G = \u0394H \u2212 T\u0394S",
        font_size=font_size,
        color=ManimColor(color),
    )


def arrhenius_equation(
    font_size: int = 32, color: ManimColor | str = WHITE,
) -> Text:
    return Text(
        "k = Ae^(\u2212\u0394G\u2021/RT)",
        font_size=font_size,
        color=ManimColor(color),
    )


def equilibrium_equation(
    font_size: int = 32, color: ManimColor | str = WHITE,
) -> Text:
    return Text(
        "\u0394G\u00b0 = \u2212RT ln K\u2091\u2091",
        font_size=font_size,
        color=ManimColor(color),
    )


def fmo_label(
    font_size: int = 26, color: ManimColor | str = WHITE,
) -> Text:
    return Text(
        "Frontier MO Theory: HOMO(donor) \u2192 LUMO(acceptor)",
        font_size=font_size,
        color=ManimColor(color),
    )


def bond_order_annotation(
    label: str, order: str,
    font_size: int = 22, color: ManimColor | str = WHITE,
) -> Text:
    return Text(
        f"{label}: {order}",
        font_size=font_size,
        color=ManimColor(color),
    )
