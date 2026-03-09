"""Generic molecular geometry dataclass and utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class MolGeom:
    """Snapshot of a molecular geometry."""

    atoms: List[Tuple[str, str, Tuple[float, float, float]]]
    # Each: (label, symbol, (x, y, z))
    bonds: List[Tuple[str, str, float]]
    # Each: (label_a, label_b, bond_order)


def interpolate_geometry(start: MolGeom, end: MolGeom, t: float) -> MolGeom:
    """Linearly interpolate atom positions between two geometry snapshots."""
    t = min(max(t, 0.0), 1.0)
    end_map: Dict[str, Tuple[str, Tuple[float, float, float]]] = {
        label: (sym, pos) for label, sym, pos in end.atoms
    }
    interp_atoms: List[Tuple[str, str, Tuple[float, float, float]]] = []
    for label, symbol, pos_s in start.atoms:
        if label in end_map:
            _, pos_e = end_map[label]
            pos = tuple(s + t * (e - s) for s, e in zip(pos_s, pos_e))
            interp_atoms.append((label, symbol, pos))  # type: ignore[arg-type]
        else:
            interp_atoms.append((label, symbol, pos_s))
    return MolGeom(atoms=interp_atoms, bonds=start.bonds)
