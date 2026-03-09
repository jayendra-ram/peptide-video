# Quantum Peptide Bonds — Video Script

> **Edit this file** to change narration, timing, visuals, and text overlays.
> Run `python scripts/make_video.py projects/peptide_bonds` to build the video.

---

## Scene 1: The Question
<!-- id: scene_01_intro -->
<!-- render: manim:IntroScene -->

**Duration:** 12s

### Narration

Everyone learns that peptide bonds hold proteins together, but what is the
bond physically? Let's zoom in from amino acids down to orbitals to find out.

### Visuals

- Draw 4 repeating amide product units as a backbone chain (spaced 2.8 apart along X)
- Golden highlight sphere on the central amide bond (unit 1 C1-N2 midpoint)
  - Semi-transparent emission material, strength 3.0, color #f1c40f

### Text Overlays

- [0.5s–4.0s] "What IS a peptide bond?" — size 0.28, position (-3.0, 0, 3.5)
- [2.0s–end] "Protein backbone: repeating -NH-CO- amide units" — size 0.10, position (-3.5, 0, -2.5)

### Camera

- Start: (0, -12, 6) looking at (0, 0, 0), FOV 35
- End: (0, -4, 1.5) — zoom over 85% of duration

---

## Scene 2: Reactants
<!-- id: scene_02_reactants -->
<!-- render: manim:ReactantsScene -->

**Duration:** 13s

### Narration

We start with two amino acids in water. The amine lone pair is electron rich,
while the carbonyl carbon is electrophilic because its pi electrons are pulled
toward the oxygen.

### Visuals

- Draw glycine A (C-terminus) at offset (-1.0, 0, 0)
- Draw glycine B (N-terminus) at offset (0, 0, 0)
- Charge halos:
  - C1 on glycine A: magnitude +0.35
  - O1 on glycine A: magnitude -0.6
  - N2 on glycine B: magnitude -0.4
- Curved arrow from N2 toward C1, color (1.0, 0.8, 0.0), arc height 0.8
  - Fades in at 4.0s–5.5s

### Text Overlays

- [start–end] "Amine (nucleophile)" — size 0.14, position (1.5, 0, 1.2)
- [start–end] "Carbonyl (electrophile)" — size 0.14, position (-2.5, 0, 1.2)
- [0s–end] "Glycine (C-terminus: -CH2-COOH)  +  Glycine (N-terminus: H2N-CH2-)" — size 0.09, position (-4.0, 0, -2.2)

### Camera

- Start: (0.5, -6, 2.5) looking at (0.5, 0, 0), FOV 35
- Slow orbit: 5 keyframes over duration, sweeping ~30 degrees, descending 0.3 per step

---

## Scene 3: Orbital Logic
<!-- id: scene_03_orbitals -->
<!-- render: manim:OrbitalsScene -->

**Duration:** 13s

### Narration

Think of the nitrogen lone pair as the HOMO donor and the carbonyl pi star as
the LUMO acceptor. When properly aligned, these orbitals overlap to launch the
reaction.

### Visuals

- Draw glycine A at offset (-1.0, 0, 0)
- Draw glycine B at offset (0, 0, 0)
- N lone pair lobe (donor, purple) at N2 position, scale (0.3, 0.3, 0.5)
  - Grows from zero at 2.0s to full at 4.0s
- C=O pi* lobe (acceptor, orange) at C1-O1 midpoint, scale (0.25, 0.4, 0.3)
  - Grows from zero at 4.5s to full at 6.5s

### Text Overlays

- [start–end] "HOMO (N lone pair)" — size 0.12, position (1.5, 0, 1.5)
- [start–end] "LUMO (C=O pi*)" — size 0.12, position (-2.5, 0, 1.5)
- [0s–end] "N lone pair (donor) attacks C=O pi* (acceptor)" — size 0.10, position (-3.5, 0, -2.2)

### Camera

- Start: (0.5, -7, 3) looking at (0.5, 0, 0), FOV 35
- End: (0.5, -4, 1.5) — push-in over full duration

---

## Scene 4: Free-Energy Barrier
<!-- id: scene_04_barrier -->
<!-- render: manim:BarrierScene -->

**Duration:** 12s

### Narration

Products may be favored, but there is still a substantial activation barrier.
Without catalysis, water does not allow spontaneous dehydration and bond
formation.

### Visuals

- Reaction coordinate energy curve with 7 sample points:
  - (0.0, 1.0), (0.2, 2.0), (0.4, 6.5), (0.5, 7.0), (0.6, 6.5), (0.8, 1.5), (1.0, 0.0)
  - x_scale 6.0, x_offset -3.0, z_scale 0.25
- Animated pointer sphere (radius 0.1) tracking along curve
- Small static glycine A at (-5.5, 0, -1.5)

### Text Overlays

- [start–end] "Reaction Progress →" — size 0.12, position (-2.5, 0, -0.8)
- [start–end] "Free Energy ↑" — size 0.10, position (-3.8, 0, 0.5)
- [start–end] "Activation\nBarrier" — size 0.14, position (0.0, 0, 2.2)
- [start–end] "Gly-COOH + H2N-Gly: dG barrier ~80 kJ/mol in water" — size 0.09, position (-4.0, 0, -1.8)

### Camera

- Static: (0, -8, 3) looking at (0, 0, 0.5), FOV 35

---

## Scene 5: Nucleophilic Attack
<!-- id: scene_05_attack -->
<!-- render: manim:AttackScene -->

**Duration:** 12s

### Narration

The nitrogen approaches and shares density with the carbonyl carbon. Bond
orders redistribute as we climb the barrier into a tetrahedral intermediate.

### Visuals

- Draw glycine A at offset (-0.5, 0, 0) — bonds skipped (atoms animate)
- Draw glycine B at offset (0, 0, 0) — bonds skipped
- Atoms animate from reactant positions to tetrahedral TS positions at scene midpoint
  - Bezier easing on all keyframes

### Text Overlays

- [0s–5.0s] "Nucleophilic Attack" — size 0.18, position (-2.5, 0, 2.5)
- [0s–end] "Gly-COOH + H2N-Gly  -->  tetrahedral intermediate" — size 0.10, position (-3.5, 0, -2.2)

### Camera

- Start: (1, -6, 2) looking at (0.3, 0, -0.2), FOV 35
- End: (0.3, -4, 0.5) — follow the approach over full duration

---

## Scene 6: Proton Transfers
<!-- id: scene_06_water_loss -->
<!-- render: manim:WaterLossScene -->

**Duration:** 10s

### Narration

Proton relays sculpt which atoms carry charge. As water leaves, the new amide
grows stronger and geometry begins to flatten.

### Visuals

- Draw tetrahedral TS — bonds skipped (atoms animate)
- Water departure: OH1 and H_OH fly to (3.0, 2.0, 1.5) at 50% of scene, shrink to zero at 70%
- Proton transfer: H_N2b moves toward OH1 position at 35%, then departs with water
- Remaining atoms settle toward amide product geometry at 85%
  - Bezier easing on all keyframes

### Text Overlays

- [start–end] "Water Departure" — size 0.16, position (-2.0, 0, 2.5)
- [0s–end] "Tetrahedral intermediate  -->  amide + H2O" — size 0.10, position (-3.0, 0, -2.2)

### Camera

- Start: (0.5, -6, 2) looking at (0.3, 0, -0.3), FOV 35
- End: (0.3, -5, 0.5) — slight push-in over full duration

---

## Scene 7: Amide Resonance
<!-- id: scene_07_resonance -->
<!-- render: manim:ResonanceScene -->

**Duration:** 11s

### Narration

Resonance between the carbonyl and nitrogen grants partial double-bond
character and enforces planarity, limiting rotation along the backbone.

### Visuals

- Draw amide product
- C-N resonance lobe (donor, purple) at C1-N2 midpoint
  - Pulsing: 2-second cycle, scale oscillates (0.4, 0.25, 0.3) to (0.15, 0.1, 0.12)
- C=O resonance lobe (acceptor, orange) at C1-O1 midpoint
  - Counter-pulsing: shrinks when C-N grows, grows when C-N shrinks
- N2 flattening animation: moves to z=0 between 20%–50% of scene, stays flat

### Text Overlays

- [0s–4.0s] "C=O / C-N Resonance" — size 0.16, position (-2.5, 0, 2.2)
- [40%–80%] "Planar Amide Bond" — size 0.14, position (-2.0, 0, -2.0)
- [start–end] "Amide product: Gly-CO-NH-Gly (partial C=N double bond)" — size 0.09, position (-3.5, 0, -2.8)

### Camera

- Start: (0.3, -5.5, 1.5) looking at (0.3, 0, -0.3), FOV 35
- Orbit: ~108 arc over 8 keyframes, radius 5.5, slight z-dip mid-orbit

---

## Scene 8: Biological Context
<!-- id: scene_08_biology -->
<!-- render: manim:BiologyScene -->

**Duration:** 11s

### Narration

Cells invest ATP to activate amino acids and position them on the ribosome,
allowing peptide bonds to form under physiological conditions.

### Visuals

- Text-card scene (no molecular geometry)
- Three sequential text cards, each filling the middle third of their time window:

### Text Overlays

- [0%–33%] "ATP activates amino acids\nfor peptide bond formation" — size 0.22, position (-3.0, 0, 0.3)
- [37%–70%] "Ribosome aligns substrates\nand lowers activation barrier" — size 0.22, position (-3.0, 0, 0.3)
- [74%–100%] "~1 peptide bond formed\nper second per ribosome" — size 0.22, position (-3.0, 0, 0.3)

### Camera

- Static: (0, -6, 0) looking at (0, 0, 0), FOV 35

---

## Scene 9: Summary
<!-- id: scene_09_summary -->
<!-- render: manim:SummaryScene -->

**Duration:** 12s

### Narration

From orbital overlap to resonance stabilization, a peptide bond is a physical
story about electrons, energy landscapes, and biological orchestration.

### Visuals

- Three molecular states side by side:
  - Glycine A (reactants) at (-4.5, 0, -0.5) labeled "Reactants"
  - Tetrahedral TS at (0.0, 0, -0.5) labeled "Transition State"
  - Amide product at (4.5, 0, -0.5) labeled "Peptide Bond"
- Animated bullet points appearing every 2s starting at 1.5s:

### Text Overlays

- [start–end] "Reactants" — size 0.12, position (-5.5, 0, -2.2)
- [start–end] "Transition State" — size 0.12, position (-1.0, 0, -2.2)
- [start–end] "Peptide Bond" — size 0.12, position (3.5, 0, -2.2)
- [1.5s] "Orbital overlap drives nucleophilic attack" — size 0.13, position (-5.0, 0, 2.0)
- [3.5s] "Activation barrier requires biological catalysis" — size 0.13, position (-5.0, 0, 1.4)
- [5.5s] "Amide resonance enforces backbone planarity" — size 0.13, position (-5.0, 0, 0.8)

### Camera

- Static: (0, -12, 2) looking at (0, 0, -0.5), FOV 40
