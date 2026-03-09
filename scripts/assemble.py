#!/usr/bin/env python3
"""Use FFmpeg to combine shots, narration, and burned-in subtitles."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.io.ffmpeg_runner import FFMpegRunner  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Assemble final video")
    parser.add_argument("project_dir", type=Path, help="Path to the project directory")
    parser.add_argument("--no-subs", action="store_true", help="Skip burning subtitles")
    parser.add_argument("--out-name", default="video.mp4", help="Output filename")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_dir = args.project_dir if args.project_dir.is_absolute() else ROOT / args.project_dir

    shots_dir = project_dir / "output" / "shots"
    shot_paths = sorted(shots_dir.glob("*.mp4"))
    if not shot_paths:
        raise SystemExit(f"No shots found in {shots_dir}")

    audio_path = project_dir / "output" / "audio" / "narration.wav"
    subtitle_path = None if args.no_subs else project_dir / "output" / "captions.srt"
    if subtitle_path and not subtitle_path.exists():
        print(f"[warn] Subtitle file not found: {subtitle_path}, skipping subs")
        subtitle_path = None

    output_path = project_dir / "output" / "final" / args.out_name

    runner = FFMpegRunner()
    runner.assemble(
        shot_paths,
        audio_path,
        output_path,
        subtitle_path=subtitle_path,
    )
    print(f"Final video: {output_path}")


if __name__ == "__main__":
    main()
