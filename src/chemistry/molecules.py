"""3D molecular geometries for peptide bond formation animation.

Coordinates are in Blender units (~1 BU ≈ 3 Angstroms).
The forming bond is between C1 (carbonyl C of molecule A) and N2 (amine N of molecule B).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass
class MolGeom:
    """Snapshot of a molecular geometry."""

    atoms: List[Tuple[str, str, Tuple[float, float, float]]]
    # Each: (label, symbol, (x, y, z))
    bonds: List[Tuple[str, str, float]]
    # Each: (label_a, label_b, bond_order)


# ── Molecule A: glycine C-terminus (–CH₂–CO–OH) ──────────────────────────────

GLYCINE_A_REACTANT = MolGeom(
    atoms=[
        ("CA1", "C", (-0.9, 0.0, 0.0)),
        ("C1", "C", (0.0, 0.0, 0.0)),
        ("O1", "O", (0.5, 0.8, 0.0)),
        ("OH1", "O", (0.5, -0.8, 0.0)),
        ("H_OH", "H", (1.0, -0.8, -0.1)),
        ("HA1", "H", (-1.2, 0.5, 0.5)),
        ("HA2", "H", (-1.2, -0.5, -0.5)),
        ("N1", "N", (-1.6, 0.0, 0.6)),
        ("H_N1a", "H", (-2.0, 0.5, 0.6)),
        ("H_N1b", "H", (-2.0, -0.4, 1.0)),
    ],
    bonds=[
        ("CA1", "C1", 1.0),
        ("C1", "O1", 2.0),
        ("C1", "OH1", 1.0),
        ("OH1", "H_OH", 1.0),
        ("CA1", "HA1", 1.0),
        ("CA1", "HA2", 1.0),
        ("CA1", "N1", 1.0),
        ("N1", "H_N1a", 1.0),
        ("N1", "H_N1b", 1.0),
    ],
)


# ── Molecule B: glycine N-terminus (H₂N–CH₂–) ───────────────────────────────

GLYCINE_B_REACTANT = MolGeom(
    atoms=[
        ("N2", "N", (2.2, 0.0, 0.0)),
        ("H_N2a", "H", (2.6, 0.6, 0.3)),
        ("H_N2b", "H", (2.6, -0.6, 0.3)),
        ("CA2", "C", (3.0, 0.0, 0.0)),
        ("HA3", "H", (3.3, 0.5, 0.5)),
        ("HA4", "H", (3.3, -0.5, -0.5)),
        ("C2", "C", (3.8, 0.0, 0.0)),
        ("O2", "O", (4.3, 0.6, 0.0)),
        ("O2H", "O", (4.3, -0.6, 0.0)),
        ("H_C2", "H", (4.8, -0.6, -0.1)),
    ],
    bonds=[
        ("N2", "CA2", 1.0),
        ("N2", "H_N2a", 1.0),
        ("N2", "H_N2b", 1.0),
        ("CA2", "HA3", 1.0),
        ("CA2", "HA4", 1.0),
        ("CA2", "C2", 1.0),
        ("C2", "O2", 2.0),
        ("C2", "O2H", 1.0),
        ("O2H", "H_C2", 1.0),
    ],
)


# ── Tetrahedral intermediate (transition state) ──────────────────────────────

TETRAHEDRAL_TS = MolGeom(
    atoms=[
        ("CA1", "C", (-0.9, 0.0, 0.0)),
        ("C1", "C", (0.0, 0.0, 0.1)),
        ("O1", "O", (0.5, 0.7, 0.4)),
        ("OH1", "O", (0.5, -0.7, 0.0)),
        ("H_OH", "H", (1.0, -0.7, -0.1)),
        ("HA1", "H", (-1.2, 0.5, 0.5)),
        ("HA2", "H", (-1.2, -0.5, -0.5)),
        ("N1", "N", (-1.6, 0.0, 0.6)),
        ("H_N1a", "H", (-2.0, 0.5, 0.6)),
        ("H_N1b", "H", (-2.0, -0.4, 1.0)),
        ("N2", "N", (0.65, 0.0, -0.7)),
        ("H_N2a", "H", (0.8, 0.6, -1.1)),
        ("H_N2b", "H", (0.8, -0.6, -1.1)),
        ("CA2", "C", (1.4, 0.0, -1.2)),
        ("HA3", "H", (1.7, 0.5, -0.7)),
        ("HA4", "H", (1.7, -0.5, -1.7)),
        ("C2", "C", (2.2, 0.0, -1.2)),
        ("O2", "O", (2.7, 0.6, -1.2)),
        ("O2H", "O", (2.7, -0.6, -1.2)),
        ("H_C2", "H", (3.2, -0.6, -1.3)),
    ],
    bonds=[
        ("CA1", "C1", 1.0),
        ("C1", "O1", 1.0),
        ("C1", "OH1", 1.0),
        ("OH1", "H_OH", 1.0),
        ("CA1", "HA1", 1.0),
        ("CA1", "HA2", 1.0),
        ("CA1", "N1", 1.0),
        ("N1", "H_N1a", 1.0),
        ("N1", "H_N1b", 1.0),
        ("C1", "N2", 0.6),
        ("N2", "CA2", 1.0),
        ("N2", "H_N2a", 1.0),
        ("N2", "H_N2b", 1.0),
        ("CA2", "HA3", 1.0),
        ("CA2", "HA4", 1.0),
        ("CA2", "C2", 1.0),
        ("C2", "O2", 2.0),
        ("C2", "O2H", 1.0),
        ("O2H", "H_C2", 1.0),
    ],
)


# ── Amide product (water departed) ───────────────────────────────────────────

AMIDE_PRODUCT = MolGeom(
    atoms=[
        ("CA1", "C", (-0.9, 0.0, 0.0)),
        ("C1", "C", (0.0, 0.0, 0.0)),
        ("O1", "O", (0.5, 0.7, 0.0)),
        ("HA1", "H", (-1.2, 0.5, 0.5)),
        ("HA2", "H", (-1.2, -0.5, -0.5)),
        ("N1", "N", (-1.6, 0.0, 0.6)),
        ("H_N1a", "H", (-2.0, 0.5, 0.6)),
        ("H_N1b", "H", (-2.0, -0.4, 1.0)),
        ("N2", "N", (0.5, 0.0, -0.6)),
        ("H_N2a", "H", (0.8, 0.5, -1.0)),
        ("CA2", "C", (1.4, 0.0, -0.6)),
        ("HA3", "H", (1.7, 0.5, -0.1)),
        ("HA4", "H", (1.7, -0.5, -1.1)),
        ("C2", "C", (2.2, 0.0, -0.6)),
        ("O2", "O", (2.7, 0.6, -0.6)),
        ("O2H", "O", (2.7, -0.6, -0.6)),
        ("H_C2", "H", (3.2, -0.6, -0.7)),
    ],
    bonds=[
        ("CA1", "C1", 1.0),
        ("C1", "O1", 1.5),
        ("CA1", "HA1", 1.0),
        ("CA1", "HA2", 1.0),
        ("CA1", "N1", 1.0),
        ("N1", "H_N1a", 1.0),
        ("N1", "H_N1b", 1.0),
        ("C1", "N2", 1.4),
        ("N2", "CA2", 1.0),
        ("N2", "H_N2a", 1.0),
        ("CA2", "HA3", 1.0),
        ("CA2", "HA4", 1.0),
        ("CA2", "C2", 1.0),
        ("C2", "O2", 2.0),
        ("C2", "O2H", 1.0),
        ("O2H", "H_C2", 1.0),
    ],
)


# ── Departed water ────────────────────────────────────────────────────────────

WATER = MolGeom(
    atoms=[
        ("O_W", "O", (0.0, 0.0, 0.0)),
        ("H_W1", "H", (0.3, 0.3, 0.0)),
        ("H_W2", "H", (-0.3, 0.3, 0.0)),
    ],
    bonds=[
        ("O_W", "H_W1", 1.0),
        ("O_W", "H_W2", 1.0),
    ],
)


# ── Helpers ───────────────────────────────────────────────────────────────────


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


def draw_molecule(
    geom: MolGeom,
    style: dict,
    offset: Tuple[float, float, float] = (0, 0, 0),
    label_prefix: str = "",
    scale: float = 1.0,
    skip_bonds: bool = False,
) -> Dict[str, object]:
    """Instantiate atoms and bonds in the current Blender scene.

    Returns dict mapping atom label -> bpy.types.Object.
    """
    from src.core.blender_scene import add_atom, add_bond

    atom_objects: Dict[str, object] = {}
    for label, symbol, pos in geom.atoms:
        shifted = tuple((p + o) * scale for p, o in zip(pos, offset))
        obj = add_atom(symbol, shifted, style, name=f"{label_prefix}{label}")
        atom_objects[label] = obj

    if not skip_bonds:
        for label_a, label_b, order in geom.bonds:
            if label_a not in atom_objects or label_b not in atom_objects:
                continue
            obj_a = atom_objects[label_a]
            obj_b = atom_objects[label_b]
            pos_a = tuple(obj_a.location)  # type: ignore[union-attr]
            pos_b = tuple(obj_b.location)  # type: ignore[union-attr]
            add_bond(
                pos_a,
                pos_b,
                order=order,
                style=style,
                name=f"{label_prefix}Bond_{label_a}_{label_b}",
            )
    return atom_objects
