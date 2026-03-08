"""FFmpeg automation helpers."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List, Optional


class FFMpegRunner:
    def __init__(self, executable: str = "ffmpeg"):
        self.executable = executable

    def frames_to_shot(
        self,
        frames_dir: Path,
        output_path: Path,
        fps: int = 30,
        crf: int = 23,
        scene_label: str = "",
    ) -> None:
        """Convert a PNG frame sequence to an H.264 MP4."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        input_pattern = str(frames_dir / "frame_%04d.png")
        command = [
            self.executable,
            "-y",
            "-framerate",
            str(fps),
            "-i",
            input_pattern,
        ]
        if scene_label:
            command.extend([
                "-vf",
                f"drawtext=text='{scene_label}'"
                ":fontfile=/System/Library/Fonts/Supplemental/Arial.ttf"
                ":fontsize=28:fontcolor=white@0.8"
                ":borderw=2:bordercolor=black@0.5"
                ":x=w-tw-20:y=20",
            ])
        command.extend([
            "-c:v",
            "libx264",
            "-crf",
            str(crf),
            "-pix_fmt",
            "yuv420p",
            "-movflags",
            "+faststart",
            str(output_path),
        ])
        print("[ffmpeg frames_to_shot]", " ".join(command))
        subprocess.run(command, check=True)

    def assemble(
        self,
        shots: List[Path],
        audio_path: Path,
        output_path: Path,
        subtitle_path: Optional[Path] = None,
    ) -> None:
        """Concatenate shot MP4s with audio and optional burned-in subtitles."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        concat_file = output_path.parent / "shots.txt"
        concat_file.write_text(
            "\n".join(f"file '{shot}'" for shot in shots), encoding="utf-8"
        )

        # Build filter for subtitles
        vf_filters = []
        if subtitle_path and subtitle_path.exists():
            # Escape path for FFmpeg subtitles filter
            escaped = str(subtitle_path).replace("\\", "\\\\").replace(":", "\\:")
            vf_filters.append(
                f"subtitles='{escaped}'"
                ":force_style='FontName=Arial,FontSize=22,"
                "PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&,"
                "Outline=2,Shadow=1,MarginV=30'"
            )

        command = [
            self.executable,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-i",
            str(audio_path),
        ]

        if vf_filters:
            command.extend(["-vf", ",".join(vf_filters)])
            command.extend(["-c:v", "libx264", "-crf", "18"])
        else:
            command.extend(["-c:v", "libx264"])

        command.extend(
            [
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-pix_fmt",
                "yuv420p",
                "-shortest",
                str(output_path),
            ]
        )
        print("[ffmpeg assemble]", " ".join(command))
        subprocess.run(command, check=True)
