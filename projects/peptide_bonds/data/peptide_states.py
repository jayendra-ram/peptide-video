"""Defines reaction states for peptide bond formation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List


@dataclass
class ReactionState:
    t: float
    n_c_distance: float
    c_o_bond_order: float
    c_n_bond_order: float
    tetrahedral_character: float
    proton_transfer_progress: float
    water_departure_progress: float
    amide_resonance: float
    free_energy: float


def prototype_states(samples: int = 10) -> List[ReactionState]:
    if samples < 2:
        raise ValueError("Need at least two samples")
    states: List[ReactionState] = []
    for i in range(samples):
        t = i / (samples - 1)
        states.append(
            ReactionState(
                t=t,
                n_c_distance=2.5 - 0.8 * t,
                c_o_bond_order=1.9 - 0.7 * t,
                c_n_bond_order=0.1 + 0.9 * t,
                tetrahedral_character=min(max((t - 0.3) * 2.0, 0), 1),
                proton_transfer_progress=min(max((t - 0.4) * 1.5, 0), 1),
                water_departure_progress=min(max((t - 0.6) * 2.0, 0), 1),
                amide_resonance=min(max((t - 0.7) * 2.5, 0), 1),
                free_energy=10 * (t - 0.5) ** 2 + (2 if t < 0.2 else 0) - 2 * t,
            )
        )
    return states


def iter_state_pairs(states: Iterable[ReactionState]):
    previous = None
    for state in states:
        if previous is not None:
            yield previous, state
        previous = state
