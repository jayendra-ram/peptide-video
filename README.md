# Peptide Video Pipeline

A reproducible scaffold for a Blender + Python + FFmpeg explainer on peptide bond
formation from a quantum-mechanical perspective. The repository separates science
content, animation logic, and post-production so that narration, visuals, and
assembly remain modular.

## Repository layout

```
config/      Project, render, and style configuration YAML files
scripts/     Command-line entry points that orchestrate the build/render pipeline
src/         Python packages for chemistry states, scene logic, and IO helpers
assets/      Placeholder folders for fonts, textures, narration, music, etc.
output/      Build artifacts such as frames, audio stems, and masters
```

## Command surface

```bash
python scripts/build.py           # validate configs, emit timeline JSON
python scripts/render_all.py      # batch render scene image sequences via Blender
python scripts/generate_tts.py    # prototype narration using OpenAI TTS
python scripts/assemble_video.py  # stitch shots + audio into a final mp4
python scripts/make_video.py      # orchestrator with preview/final quality flags
```

Each script is instrumented with structured logging and placeholder pseudocode to
show where to integrate Blender CLI invocations, FFmpeg filters, or OpenAI calls.

> **No Blender?** `scripts/render_all.py` automatically falls back to an FFmpeg-based
> storyboard renderer that outputs text plates for every scene so the end-to-end
> pipeline still produces a video master.

## Next steps

1. Flesh out the chemistry `ReactionState` sampling in `src/chemistry`.
2. Translate the storyboard scenes into Blender Python scene files under
   `src/scenes`.
3. Lock narration timings in `scripts/build.py` and regenerate subtitles.
4. Swap the placeholder FFmpeg renderer and silent narration with Blender + real
   audio when those assets are ready, then re-run `python scripts/make_video.py`.
