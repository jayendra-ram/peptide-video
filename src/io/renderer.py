"""Renderer registry -- dispatches scene rendering to the appropriate backend.

Supported render types:
  manim:ClassName     Auto-discovers ClassName in project/scenes/, renders via Manim CLI
  video:path.mp4      Trims or re-encodes a video clip to match scene duration
  image:path.png      Holds a still image for the scene duration
  blender:path.blend  Renders via Blender CLI
  placeholder         Text-plate fallback for prototyping
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

from src.core.script_parser import ParsedScene
from src.io.manim_runner import ManimRunner
from src.io.placeholder_renderer import PlaceholderRenderer


class RendererRegistry:
    """Dispatch scene rendering to the right backend."""

    def __init__(
        self,
        project_dir: Path,
        framework_root: Path,
        render_config: dict,
        style_config: dict,
    ):
        self.project_dir = project_dir
        self.framework_root = framework_root
        self.render_config = render_config
        self.style_config = style_config
        self._manim_runner = ManimRunner(framework_root)

    def render(
        self,
        scene: ParsedScene,
        output_path: Path,
        quality: str = "-qm",
        target_duration: Optional[float] = None,
    ) -> Optional[Path]:
        render_type = scene.render.type
        if render_type == "manim":
            return self._render_manim(scene, output_path, quality, target_duration=target_duration)
        elif render_type == "video":
            return self._render_video_clip(scene, output_path)
        elif render_type == "image":
            return self._render_image(scene, output_path)
        elif render_type == "blender":
            return self._render_blender(scene, output_path)
        elif render_type == "placeholder":
            return self._render_placeholder(scene, output_path)
        else:
            print(f"[renderer] Unknown render type: {render_type}, falling back to placeholder")
            return self._render_placeholder(scene, output_path)

    # -- Manim ----------------------------------------------------------------

    def _render_manim(
        self, scene: ParsedScene, output_path: Path, quality: str,
        target_duration: Optional[float] = None,
    ) -> Optional[Path]:
        class_name = scene.render.ref
        scene_file = self._discover_manim_scene(class_name)
        if scene_file is None:
            print(f"[renderer] Could not find Manim class '{class_name}', using placeholder")
            return self._render_placeholder(scene, output_path)

        media_dir = self.project_dir / "output" / "media"
        return self._manim_runner.render_scene(
            scene_file=scene_file,
            class_name=class_name,
            output_path=output_path,
            quality=quality,
            media_dir=media_dir,
            extra_python_paths=[self.project_dir],
            target_duration=target_duration,
        )

    def _discover_manim_scene(self, class_name: str) -> Optional[Path]:
        """Search project_dir/scenes/*.py for a class by name."""
        scenes_dir = self.project_dir / "scenes"
        if not scenes_dir.is_dir():
            return None
        for py_file in sorted(scenes_dir.glob("*.py")):
            if py_file.name.startswith("_"):
                continue
            source = py_file.read_text(encoding="utf-8")
            if f"class {class_name}" in source:
                return py_file
        return None

    # -- Video clip -----------------------------------------------------------

    def _render_video_clip(
        self, scene: ParsedScene, output_path: Path
    ) -> Optional[Path]:
        clip_path = self.project_dir / scene.render.ref
        if not clip_path.exists():
            print(f"[renderer] Video clip not found: {clip_path}, using placeholder")
            return self._render_placeholder(scene, output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        command = [
            "ffmpeg", "-y",
            "-i", str(clip_path),
            "-t", f"{scene.duration_seconds:.2f}",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-an",
            str(output_path),
        ]
        print(f"[video] {' '.join(command)}")
        subprocess.run(command, check=True)
        return output_path

    # -- Still image ----------------------------------------------------------

    def _render_image(
        self, scene: ParsedScene, output_path: Path
    ) -> Optional[Path]:
        image_path = self.project_dir / scene.render.ref
        if not image_path.exists():
            print(f"[renderer] Image not found: {image_path}, using placeholder")
            return self._render_placeholder(scene, output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        resolution = "1920x1080"
        fps = self.render_config.get("ffmpeg", {}).get("frame_rate", 30)
        command = [
            "ffmpeg", "-y",
            "-loop", "1",
            "-i", str(image_path),
            "-t", f"{scene.duration_seconds:.2f}",
            "-vf", f"scale={resolution.replace('x', ':')}:force_original_aspect_ratio=decrease,pad={resolution.replace('x', ':')}:(ow-iw)/2:(oh-ih)/2",
            "-r", str(fps),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(output_path),
        ]
        print(f"[image] {' '.join(command)}")
        subprocess.run(command, check=True)
        return output_path

    # -- Blender --------------------------------------------------------------

    def _render_blender(
        self, scene: ParsedScene, output_path: Path
    ) -> Optional[Path]:
        blend_path = self.project_dir / scene.render.ref
        if not blend_path.exists():
            print(f"[renderer] Blender file not found: {blend_path}, using placeholder")
            return self._render_placeholder(scene, output_path)

        from src.io.blender_runner import BlenderRunner
        runner = BlenderRunner()
        return runner.render(str(blend_path), str(output_path))

    # -- Placeholder ----------------------------------------------------------

    def _render_placeholder(
        self, scene: ParsedScene, output_path: Path
    ) -> Optional[Path]:
        bg = self.style_config.get("colors", {}).get("background", "#05060a")
        renderer = PlaceholderRenderer(
            ffmpeg="ffmpeg",
            resolution="1920x1080",
            fps=self.render_config.get("ffmpeg", {}).get("frame_rate", 30),
            background=bg,
        )
        scene_dict = {
            "id": scene.id,
            "label": scene.label,
            "duration_seconds": scene.duration_seconds,
            "voiceover": scene.voiceover,
        }
        renderer.render_scene(scene_dict, output_path)
        return output_path
