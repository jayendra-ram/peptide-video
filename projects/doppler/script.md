# The Relativistic Doppler Effect — Video Script

> **Edit this file** to change narration, timing, visuals, and text overlays.
> Run `python scripts/make_video.py projects/doppler` to build the video.

---

## Scene 1: Introduction
<!-- id: scene_01_intro -->
<!-- render: manim:IntroScene -->

**Duration:** 12s

### Narration

Every ambulance siren changes pitch as it passes. The same physics governs starlight, but near the speed of light, Einstein's relativity rewrites the rules.

### Visuals

- A dot source emits expanding wavefront circles
- Source starts stationary (symmetric rings), then moves right
- Rings compress ahead and stretch behind
- Title "The Relativistic Doppler Effect" fades in over the animation

### Text Overlays

- [0.5s–4.0s] "Every wave carries information about motion" — size 0.24, position (0, 3.0)
- [6.0s–end] "The Relativistic Doppler Effect" — size 0.40, position (0, 0)

### Camera

- Static: origin, default frame

---

## Scene 2: Classical Doppler
<!-- id: scene_02_classical -->
<!-- render: manim:ClassicalScene -->

**Duration:** 13s

### Narration

For sound, the classical Doppler formula relates observed frequency to the source's speed through the medium. Wavefronts pile up ahead of a moving source and spread out behind it.

### Visuals

- Top half: moving dot emitting rings (labeled "Source")
- Wavefronts compress ahead, stretch behind
- Bottom half: classical Doppler formula written step by step

### Text Overlays

- [0s–end] "Classical Doppler Effect" — size 0.28, position (0, 3.2)
- [start–end] "Source" — size 0.18, label near the moving dot

### Camera

- Static: origin, default frame

---

## Scene 3: Enter Relativity
<!-- id: scene_03_relativity -->
<!-- render: manim:RelativityScene -->

**Duration:** 12s

### Narration

Light needs no medium. Its speed is the same for every observer. This means the classical formula breaks down. We need a new parameter: beta, the source velocity as a fraction of c.

### Visuals

- Show speed of light postulate as text card
- Introduce beta = v/c with a horizontal number line gauge from 0 to 1
- Highlight the regime near beta = 1 where classical fails
- Show classical formula diverging as v approaches c

### Text Overlays

- [0s–4s] "The speed of light is constant\nfor all observers" — size 0.26, position (0, 2.5)

### Camera

- Static: origin, default frame

---

## Scene 4: Time Dilation
<!-- id: scene_04_time_dilation -->
<!-- render: manim:TimeDilationScene -->

**Duration:** 13s

### Narration

A moving clock ticks slower by the Lorentz factor gamma. This means the source emits wave crests less frequently in the observer's frame — an extra frequency shift that classical physics misses.

### Visuals

- Left side: rest-frame clock ticking at normal rate
- Right side: moving-frame clock ticking slower
- Below: plot of gamma vs beta showing the curve shooting up near beta = 1

### Text Overlays

- [start–end] "Rest Frame" — size 0.20, position (-3.5, 2.5)
- [start–end] "Moving Frame" — size 0.20, position (3.5, 2.5)

### Camera

- Static: origin, default frame

---

## Scene 5: The Relativistic Formula
<!-- id: scene_05_formula -->
<!-- render: manim:FormulaScene -->

**Duration:** 14s

### Narration

Multiply the classical Doppler shift by one over gamma for time dilation. Simplify, and you get a single elegant expression. The square root form handles both approach and recession by flipping the sign of beta.

### Visuals

- Three-step derivation:
  1. Start with classical: f_obs = f_s / (1 - beta)
  2. Multiply by 1/gamma: f_obs = f_s * 1/(1-beta) * sqrt(1-beta^2)
  3. Simplify: f_obs = f_s * sqrt((1+beta)/(1-beta))
- Final result gets a yellow box/highlight
- TransformMatchingTex between derivation steps

### Text Overlays

- [0s–end] "Deriving the Relativistic Formula" — size 0.28, position (0, 3.2)

### Camera

- Static: origin, default frame

---

## Scene 6: Blueshift and Redshift
<!-- id: scene_06_spectrum -->
<!-- render: manim:SpectrumScene -->

**Duration:** 12s

### Narration

When a source approaches, wavelengths compress and light shifts blue. When it recedes, wavelengths stretch and light shifts red. At half the speed of light, the observed wavelength nearly doubles.

### Visuals

- Horizontal visible spectrum bar (violet to red)
- Top: approaching source with compressed wavefronts colored blue
- Bottom: receding source with stretched wavefronts colored red
- Arrow marker slides along spectrum bar
- Show wavelength ratio formula

### Text Overlays

- [0s–end] "Blueshift & Redshift" — size 0.28, position (0, 3.2)
- [start–end] "Approaching" — size 0.18, near top wavefronts
- [start–end] "Receding" — size 0.18, near bottom wavefronts

### Camera

- Static: origin, default frame

---

## Scene 7: Transverse Doppler Effect
<!-- id: scene_07_transverse -->
<!-- render: manim:TransverseScene -->

**Duration:** 12s

### Narration

Relativity predicts something classical physics cannot: a frequency shift even when the source moves perpendicular to the observer. This transverse Doppler effect is pure time dilation, and it's always a redshift.

### Visuals

- Source dot moves horizontally across the screen
- Observer dot is below at the closest approach point
- Dashed line marks perpendicular distance
- Arrow shows velocity vector
- Wavefronts arrive with slight redshift
- Display the transverse formula

### Text Overlays

- [0s–end] "Transverse Doppler Effect" — size 0.28, position (0, 3.2)
- [start–end] "Source" — size 0.16, label on moving dot
- [start–end] "Observer" — size 0.16, label on stationary dot

### Camera

- Static: origin, default frame

---

## Scene 8: Cosmological Redshift
<!-- id: scene_08_cosmological -->
<!-- render: manim:CosmologicalScene -->

**Duration:** 11s

### Narration

Distant galaxies are redshifted because space itself is expanding. Astronomers use redshift z to measure recession velocity and map the structure of the cosmos.

### Visuals

- Stylized galaxy (ellipse with glow) moving rightward
- Trailing stretched wavefronts that shift from blue to red
- Show redshift z formula
- Dots representing galaxy clusters receding from each other

### Text Overlays

- [0s–end] "Cosmological Redshift" — size 0.28, position (0, 3.2)

### Camera

- Static: origin, default frame

---

## Scene 9: Summary
<!-- id: scene_09_summary -->
<!-- render: manim:SummaryScene -->

**Duration:** 10s

### Narration

From ambulance sirens to the expanding universe, the Doppler effect reveals how motion reshapes the waves we observe. Relativity adds time dilation, making the formula exact at any speed.

### Visuals

- Three key equations stacked vertically:
  1. Classical Doppler
  2. Relativistic Doppler
  3. Transverse Doppler
- Each equation fades in sequentially
- Final wavefront animation fading out behind the equations

### Text Overlays

- [0s–end] "Key Equations" — size 0.28, position (0, 3.2)
- [start–end] "Classical" — size 0.16, label next to first equation
- [start–end] "Relativistic" — size 0.16, label next to second equation
- [start–end] "Transverse" — size 0.16, label next to third equation

### Camera

- Static: origin, default frame
