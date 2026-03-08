#!/usr/bin/env python3
"""Generate narration audio via OpenAI TTS, one file per scene."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.timeline import TimelineBuilder  # noqa: E402


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate narration via OpenAI TTS")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Export transcript only, skip TTS API calls",
    )
    parser.add_argument(
        "--voice",
        default="onyx",
        help="OpenAI TTS voice (alloy, echo, fable, onyx, nova, shimmer)",
    )
    parser.add_argument(
        "--model",
        default="tts-1-hd",
        help="OpenAI TTS model (tts-1 or tts-1-hd)",
    )
    parser.add_argument(
        "--out-dir",
        default="output/audio",
        help="Output directory for audio files",
    )
    return parser.parse_args()


def dump_script(cues, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"[{cue['scene_id']}] {cue['voiceover'].strip()}" for cue in cues]
    path.write_text("\n\n".join(lines), encoding="utf-8")


def generate_tts_per_scene(
    cues: list[dict],
    out_dir: Path,
    voice: str,
    model: str,
) -> list[Path]:
    """Call OpenAI TTS for each scene's voiceover. Returns list of audio paths."""
    from openai import OpenAI

    client = OpenAI()
    audio_paths: list[Path] = []

    for cue in cues:
        scene_id = cue["scene_id"]
        text = cue["voiceover"].strip()
        out_path = out_dir / f"{scene_id}.mp3"

        if out_path.exists():
            print(f"[tts] {scene_id}: already exists, skipping")
            audio_paths.append(out_path)
            continue

        print(f"[tts] {scene_id}: generating ({len(text)} chars)...")
        with client.audio.speech.with_streaming_response.create(
            model=model,
            voice=voice,
            input=text,
            response_format="mp3",
        ) as response:
            response.stream_to_file(str(out_path))
        print(f"[tts] {scene_id}: saved to {out_path}")
        audio_paths.append(out_path)

    return audio_paths


def concatenate_audio(audio_paths: list[Path], output_path: Path) -> None:
    """Concatenate per-scene MP3 files into one WAV with silence padding."""
    concat_file = output_path.parent / "audio_concat.txt"
    # Add a small silence gap between scenes
    lines = []
    for path in audio_paths:
        lines.append(f"file '{path}'")
    concat_file.write_text("\n".join(lines), encoding="utf-8")

    command = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_file),
        "-ac",
        "1",
        "-ar",
        "48000",
        str(output_path),
    ]
    print("[ffmpeg concat audio]", " ".join(command))
    subprocess.run(command, check=True)


def make_padded_scene_audio(
    audio_path: Path, target_duration: float, output_path: Path
) -> None:
    """Pad or trim a scene's audio to exactly target_duration seconds."""
    # Get actual audio duration
    probe = subprocess.run(
        [
            "ffprobe",
            "-v",
            "quiet",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(audio_path),
        ],
        capture_output=True,
        text=True,
    )
    actual = float(probe.stdout.strip())

    if actual >= target_duration:
        # Trim to target duration
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(audio_path),
                "-t",
                f"{target_duration:.2f}",
                "-ac",
                "1",
                "-ar",
                "48000",
                str(output_path),
            ],
            capture_output=True,
            check=True,
        )
    else:
        # Pad with silence to reach target duration
        pad_duration = target_duration - actual
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(audio_path),
                "-af",
                f"apad=pad_dur={pad_duration:.2f}",
                "-t",
                f"{target_duration:.2f}",
                "-ac",
                "1",
                "-ar",
                "48000",
                str(output_path),
            ],
            capture_output=True,
            check=True,
        )


def assemble_narration(
    cues: list[dict],
    audio_dir: Path,
    scenes_config: list[dict],
    output_path: Path,
) -> None:
    """Pad each scene's audio to match scene duration, then concatenate."""
    padded_dir = audio_dir / "padded"
    padded_dir.mkdir(parents=True, exist_ok=True)

    duration_map = {s["id"]: s["duration_seconds"] for s in scenes_config}
    padded_paths: list[Path] = []

    for cue in cues:
        scene_id = cue["scene_id"]
        src = audio_dir / f"{scene_id}.mp3"
        dst = padded_dir / f"{scene_id}.wav"
        target = duration_map.get(scene_id, 30)

        if not src.exists():
            print(f"[warn] No audio for {scene_id}, generating silence")
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "lavfi",
                    "-i",
                    f"anullsrc=r=48000:cl=mono",
                    "-t",
                    f"{target:.2f}",
                    str(dst),
                ],
                capture_output=True,
                check=True,
            )
        else:
            make_padded_scene_audio(src, target, dst)

        padded_paths.append(dst)
        print(f"[pad] {scene_id}: {target:.0f}s → {dst.name}")

    concatenate_audio(padded_paths, output_path)
    print(f"[done] Full narration: {output_path}")


def main() -> None:
    args = parse_args()
    project_config = load_yaml(ROOT / "config" / "project.yaml")
    builder = TimelineBuilder(project_config)
    cues = [cue.to_dict() for cue in builder.build()]

    out_dir = ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    dump_script(cues, out_dir / "narration.txt")
    print(f"Transcript exported to {out_dir / 'narration.txt'}")

    if args.dry_run:
        print("Dry run complete.")
        return

    # Generate TTS for each scene
    audio_paths = generate_tts_per_scene(cues, out_dir, args.voice, args.model)

    # Probe actual speech durations for subtitle sync
    from src.io.subtitle_writer import probe_duration

    speech_durations: dict[str, float] = {}
    for cue, audio_path in zip(cues, audio_paths):
        if audio_path.exists():
            speech_durations[cue["scene_id"]] = probe_duration(audio_path)
            print(
                f"[probe] {cue['scene_id']}: "
                f"{speech_durations[cue['scene_id']]:.1f}s speech"
            )

    # Regenerate subtitles synced to actual speech timing
    from src.io.subtitle_writer import write_srt

    scene_cues = builder.build()
    srt_path = ROOT / "output" / "captions.srt"
    write_srt(scene_cues, srt_path, speech_durations=speech_durations)
    print(f"[subs] Synced subtitles written to {srt_path}")

    # Pad each to scene duration and concatenate
    assemble_narration(
        cues,
        out_dir,
        project_config["scenes"],
        out_dir / "narration.wav",
    )


if __name__ == "__main__":
    main()
