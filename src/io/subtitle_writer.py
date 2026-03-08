"""Generate SRT subtitles from timeline cues with sentence-level timing."""

from __future__ import annotations

import re
import subprocess
from datetime import timedelta
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

from ..core.timeline import SceneCue


def format_timestamp(seconds: float) -> str:
    td = timedelta(seconds=max(0, seconds))
    total_seconds = int(td.total_seconds())
    millis = int((td.total_seconds() - total_seconds) * 1000)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds_int = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds_int:02d},{millis:03d}"


def split_sentences(text: str) -> List[str]:
    """Split voiceover text into display-friendly subtitle chunks."""
    text = text.strip().replace("\n", " ")
    raw = re.split(r"(?<=[.!?])\s+", text)
    chunks: List[str] = []
    for sentence in raw:
        sentence = sentence.strip()
        if not sentence:
            continue
        if len(sentence) > 80:
            parts = re.split(r",\s+", sentence)
            buf = ""
            for part in parts:
                if buf and len(buf) + len(part) > 70:
                    chunks.append(buf.rstrip(",").strip())
                    buf = part
                else:
                    buf = f"{buf}, {part}" if buf else part
            if buf:
                chunks.append(buf.strip())
        else:
            chunks.append(sentence)
    return chunks


def probe_duration(path: Path) -> float:
    """Get audio duration in seconds via ffprobe."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "quiet",
            "-show_entries",
            "format=duration",
            "-of",
            "csv=p=0",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def write_srt(
    cues: Iterable[SceneCue],
    path: Path,
    speech_durations: Optional[Dict[str, float]] = None,
) -> None:
    """Write an SRT file with sentence-level subtitle timing.

    If speech_durations is provided (scene_id -> actual speech seconds),
    subtitles are timed within the actual speech window rather than
    spread across the full scene duration.
    """
    entries: List[Tuple[float, float, str]] = []

    for cue in cues:
        sentences = split_sentences(cue.voiceover)
        if not sentences:
            continue

        # Use actual speech duration if available, otherwise full scene duration
        if speech_durations and cue.scene_id in speech_durations:
            speech_dur = speech_durations[cue.scene_id]
        else:
            speech_dur = cue.duration

        # Clamp to scene duration
        speech_dur = min(speech_dur, cue.duration)

        total_chars = sum(len(s) for s in sentences)
        cursor = cue.start_time

        for sentence in sentences:
            fraction = len(sentence) / total_chars if total_chars > 0 else 1.0
            sub_duration = speech_dur * fraction
            sub_duration = max(sub_duration, 1.5)
            end_time = min(
                cursor + sub_duration, cue.start_time + speech_dur
            )
            entries.append((cursor, end_time, sentence))
            cursor = end_time

    lines: List[str] = []
    for index, (start, end, text) in enumerate(entries, start=1):
        lines.append(str(index))
        lines.append(f"{format_timestamp(start)} --> {format_timestamp(end)}")
        lines.append(text)
        lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")
