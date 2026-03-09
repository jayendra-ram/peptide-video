#!/usr/bin/env python3
"""Generate narration audio via OpenAI TTS, one file per scene."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.script_parser import parse_script  # noqa: E402
from src.core.timeline import TimelineBuilder  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate narration via OpenAI TTS")
    parser.add_argument("project_dir", type=Path, help="Path to the project directory")
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
    """Concatenate per-scene audio files into one WAV."""
    concat_file = output_path.parent / "audio_concat.txt"
    lines = [f"file '{path}'" for path in audio_paths]
    concat_file.write_text("\n".join(lines), encoding="utf-8")

    command = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_file),
        "-ac", "1", "-ar", "48000",
        str(output_path),
    ]
    print("[ffmpeg concat audio]", " ".join(command))
    subprocess.run(command, check=True)


def determine_scene_duration(
    tts_duration: float, script_duration: float, tail_pad: float = 1.5,
) -> float:
    """Scene duration = max(script minimum, tts speech + tail padding)."""
    return max(script_duration, tts_duration + tail_pad)


def make_padded_scene_audio(
    audio_path: Path, target_duration: float, output_path: Path
) -> None:
    """Pad a scene's audio to exactly target_duration seconds (never trims)."""
    probe = subprocess.run(
        [
            "ffprobe", "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "csv=p=0",
            str(audio_path),
        ],
        capture_output=True, text=True,
    )
    actual = float(probe.stdout.strip())

    if actual >= target_duration:
        # Audio is already long enough — just convert format, no trimming
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(audio_path),
                "-ac", "1", "-ar", "48000",
                str(output_path),
            ],
            capture_output=True, check=True,
        )
    else:
        pad_duration = target_duration - actual
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", str(audio_path),
                "-af", f"apad=pad_dur={pad_duration:.2f}",
                "-t", f"{target_duration:.2f}",
                "-ac", "1", "-ar", "48000",
                str(output_path),
            ],
            capture_output=True, check=True,
        )


def assemble_narration(
    cues: list[dict],
    audio_dir: Path,
    scenes,
    output_path: Path,
    speech_durations: dict[str, float] | None = None,
) -> dict[str, dict]:
    """Pad each scene's audio using audio-first durations, then concatenate.

    Returns a duration map: {scene_id: {"tts_seconds": ..., "scene_seconds": ...}}
    """
    padded_dir = audio_dir / "padded"
    padded_dir.mkdir(parents=True, exist_ok=True)

    duration_map = {s.id: s.duration_seconds for s in scenes}
    speech_durations = speech_durations or {}
    padded_paths: list[Path] = []
    result_durations: dict[str, dict] = {}

    for cue in cues:
        scene_id = cue["scene_id"]
        src = audio_dir / f"{scene_id}.mp3"
        dst = padded_dir / f"{scene_id}.wav"
        script_dur = duration_map.get(scene_id, 30)
        tts_dur = speech_durations.get(scene_id, 0.0)

        # Audio-first: use TTS duration to set scene length
        target = determine_scene_duration(tts_dur, script_dur)

        if not src.exists():
            print(f"[warn] No audio for {scene_id}, generating silence")
            subprocess.run(
                [
                    "ffmpeg", "-y",
                    "-f", "lavfi",
                    "-i", "anullsrc=r=48000:cl=mono",
                    "-t", f"{target:.2f}",
                    str(dst),
                ],
                capture_output=True, check=True,
            )
        else:
            make_padded_scene_audio(src, target, dst)

        padded_paths.append(dst)
        result_durations[scene_id] = {
            "tts_seconds": round(tts_dur, 2),
            "scene_seconds": round(target, 2),
        }
        print(f"[pad] {scene_id}: tts={tts_dur:.1f}s -> scene={target:.1f}s -> {dst.name}")

    concatenate_audio(padded_paths, output_path)
    print(f"[done] Full narration: {output_path}")
    return result_durations


def main() -> None:
    import json

    args = parse_args()
    project_dir = args.project_dir if args.project_dir.is_absolute() else ROOT / args.project_dir

    scenes = parse_script(project_dir / "script.md")
    builder = TimelineBuilder(scenes)
    cues = [cue.to_dict() for cue in builder.build()]

    out_dir = project_dir / "output" / "audio"
    out_dir.mkdir(parents=True, exist_ok=True)

    dump_script(cues, out_dir / "narration.txt")
    print(f"Transcript exported to {out_dir / 'narration.txt'}")

    if args.dry_run:
        print("Dry run complete.")
        return

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
    srt_path = project_dir / "output" / "captions.srt"
    write_srt(scene_cues, srt_path, speech_durations=speech_durations)
    print(f"[subs] Synced subtitles written to {srt_path}")

    # Assemble narration with audio-first durations
    result_durations = assemble_narration(
        cues, out_dir, scenes, out_dir / "narration.wav",
        speech_durations=speech_durations,
    )

    # Write durations.json for the render step
    durations_path = project_dir / "output" / "durations.json"
    with durations_path.open("w") as f:
        json.dump(result_durations, f, indent=2)
    print(f"[durations] Written to {durations_path}")


if __name__ == "__main__":
    main()
