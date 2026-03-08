"""Screen overlay label scheduling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class LabelCue:
    text: str
    start: float
    end: float
    anchor: str = "top_left"


class LabelScheduler:
    def __init__(self, default_duration: float = 3.0):
        self.default_duration = default_duration

    def from_voiceover(self, transcript: str) -> List[LabelCue]:
        lines = [line.strip() for line in transcript.splitlines() if line.strip()]
        cues: List[LabelCue] = []
        cursor = 0.0
        for line in lines:
            cues.append(LabelCue(text=line, start=cursor, end=cursor + self.default_duration))
            cursor += self.default_duration
        return cues
