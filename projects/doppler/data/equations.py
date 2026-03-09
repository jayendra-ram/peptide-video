"""Equation helpers for relativistic Doppler effect video.

Uses Text with Unicode math symbols to avoid LaTeX dependency.
"""

from __future__ import annotations

from manim import Text, ManimColor, VGroup


_EQ_FONT_SIZE = 32
_EQ_COLOR = "#ecf0f1"


def _eq(text: str, font_size: int = _EQ_FONT_SIZE) -> Text:
    return Text(text, font_size=font_size, color=ManimColor(_EQ_COLOR))


def classical_doppler() -> Text:
    """f_obs = f_s * v_sound / (v_sound - v_source)"""
    return _eq("f_obs = f_s \u00b7 v_sound / (v_sound \u2212 v_source)")


def classical_doppler_beta() -> Text:
    """Classical formula rewritten with beta: f_obs = f_s / (1 - beta)"""
    return _eq("f_obs = f_s / (1 \u2212 \u03b2)")


def beta_definition() -> Text:
    """beta = v / c"""
    return _eq("\u03b2 = v / c")


def lorentz_factor() -> Text:
    """gamma = 1 / sqrt(1 - beta^2)"""
    return _eq("\u03b3 = 1 / \u221a(1 \u2212 \u03b2\u00b2)")


def relativistic_doppler_step1() -> Text:
    """Classical times 1/gamma."""
    return _eq("f_obs = f_s \u00b7 1/(1 \u2212 \u03b2) \u00b7 \u221a(1 \u2212 \u03b2\u00b2)")


def relativistic_doppler_approach() -> Text:
    """f_obs = f_s * sqrt((1+beta)/(1-beta))"""
    return _eq("f_obs = f_s \u00b7 \u221a[(1 + \u03b2) / (1 \u2212 \u03b2)]")


def relativistic_doppler_recede() -> Text:
    """f_obs = f_s * sqrt((1-beta)/(1+beta))"""
    return _eq("f_obs = f_s \u00b7 \u221a[(1 \u2212 \u03b2) / (1 + \u03b2)]")


def transverse_doppler() -> Text:
    """f_obs = f_s / gamma = f_s * sqrt(1 - beta^2)"""
    return _eq("f_obs = f_s / \u03b3 = f_s \u00b7 \u221a(1 \u2212 \u03b2\u00b2)")


def redshift_z() -> Text:
    """z = sqrt((1+beta)/(1-beta)) - 1"""
    return _eq("z = \u0394\u03bb / \u03bb_s = \u221a[(1 + \u03b2) / (1 \u2212 \u03b2)] \u2212 1")


def wavelength_ratio() -> Text:
    """lambda_obs / lambda_s = sqrt((1+beta)/(1-beta))"""
    return _eq("\u03bb_obs / \u03bb_s = \u221a[(1 + \u03b2) / (1 \u2212 \u03b2)]")
