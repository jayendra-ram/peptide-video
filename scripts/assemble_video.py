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
    parser.add_argument(
        "--shots", default="output/shots", help="Directory with per-scene mp4s"
    )
    parser.add_argument(
        "--audio",
        default="output/audio/narration.wav",
        help="Narration audio path",
    )
    parser.add_argument(
        "--subs",
        default="output/captions.srt",
        help="SRT subtitle file to burn in",
    )
    parser.add_argument(
        "--no-subs",
        action="store_true",
        help="Skip burning subtitles",
    )
    parser.add_argument(
        "--out",
        default="output/final/peptide_video.mp4",
        help="Final video path",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    shots_dir = ROOT / args.shots
    shot_paths = sorted(shots_dir.glob("*.mp4"))
    if not shot_paths:
        raise SystemExit(f"No shots found in {shots_dir}")

    subtitle_path = None if args.no_subs else ROOT / args.subs
    if subtitle_path and not subtitle_path.exists():
        print(f"[warn] Subtitle file not found: {subtitle_path}, skipping subs")
        subtitle_path = None

    runner = FFMpegRunner()
    runner.assemble(
        shot_paths,
        ROOT / args.audio,
        ROOT / args.out,
        subtitle_path=subtitle_path,
    )
    print(f"Final video: {ROOT / args.out}")


if __name__ == "__main__":
    main()
