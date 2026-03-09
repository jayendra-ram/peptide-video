# Rabat — Educational Explainer Video Framework

A framework for creating educational explainer videos from markdown scripts, using
Manim, Blender, video clips, and still images as scene renderers.

## How it works

1. **Write a markdown script** — define scenes, narration, timing, and visuals
2. **Run the pipeline** — the framework renders each scene, generates TTS narration, and assembles the final video

```bash
python scripts/make_video.py projects/peptide_bonds
```

## Repository layout

```
config/              Framework default configs (render presets, style)
scripts/             Pipeline entry points
src/                 Framework package
  core/              Script parser, timeline builder, config loader
  io/                Renderer registry, Manim/FFmpeg/Blender runners
  manim/             Reusable Manim mobjects (molecules, orbitals, energy diagrams)
  chemistry/         Chemistry data models (atoms, bonds, molecules)
projects/            Video projects
  peptide_bonds/     Example project: peptide bond formation explainer
    script.md        The video script (single source of truth)
    scenes/          Manim scene implementations
    data/            Project-specific data (molecules, equations)
```

## Markdown script format

Each scene is defined with a heading, metadata comments, and content sections:

```markdown
## Scene 1: Title
<!-- id: scene_01 -->
<!-- render: manim:MySceneClass -->
**Duration:** 12s

### Narration
The voiceover text goes here.

### Visuals
Free-form visual directions for the scene implementer.

### Text Overlays
- [0.5s-4.0s] "Label text" -- size 0.28, position (-3.0, 0, 3.5)

### Camera
- Start: (0, -12, 6) looking at (0, 0, 0), FOV 35
```

### Render types

| Directive | Description |
|---|---|
| `manim:ClassName` | Auto-discovers the class in `project/scenes/` and renders via Manim |
| `video:path/to/clip.mp4` | Trims a video clip to the scene duration |
| `image:path/to/image.png` | Holds a still image for the scene duration |
| `blender:path/to/file.blend` | Renders via Blender CLI |
| `placeholder` | Generates a text-plate fallback (default if omitted) |

## Pipeline commands

```bash
# Full pipeline
python scripts/make_video.py projects/peptide_bonds --quality=preview

# Individual steps
python scripts/build.py projects/peptide_bonds
python scripts/render_all.py projects/peptide_bonds --quality=preview
python scripts/generate_tts.py projects/peptide_bonds --dry-run
python scripts/assemble.py projects/peptide_bonds
```

## Creating a new project

```bash
mkdir -p projects/my_video/{scenes,data,assets,config,output}
```

Write `projects/my_video/script.md`, implement any Manim scenes in `scenes/`, then run:

```bash
python scripts/make_video.py projects/my_video
```
