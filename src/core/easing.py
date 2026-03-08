"""Common easing curves."""

from typing import Callable


def make_ease_in(power: int) -> Callable[[float], float]:
    def ease(t: float) -> float:
        t = min(max(t, 0.0), 1.0)
        return t ** power

    return ease


def make_ease_out(power: int) -> Callable[[float], float]:
    ease_in = make_ease_in(power)

    def ease(t: float) -> float:
        t = 1 - t
        return 1 - ease_in(t)

    return ease


def ease_in_out_quad(t: float) -> float:
    t = min(max(t, 0.0), 1.0)
    if t < 0.5:
        return 2 * t * t
    t -= 0.5
    return 1 - 2 * t * (t - 0.5)
