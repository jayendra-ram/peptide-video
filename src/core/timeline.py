"""Timeline builder -- generates cue sheets from parsed scenes."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List
import json

from src.core.script_parser import ParsedScene


@dataclass
class SceneCue:
    """Map storyboard info to runtime-friendly cues."""

    scene_id: str
    start_time: float
    duration: float
    voiceover: str
    labels: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "scene_id": self.scene_id,
            "start_time": self.start_time,
            "duration": self.duration,
            "voiceover": self.voiceover.strip(),
            "labels": self.labels,
        }


class TimelineBuilder:
    """Generates structured cue sheets from parsed scenes."""

    def __init__(self, scenes: List[ParsedScene]):
        self.scenes = scenes

    def build(self) -> List[SceneCue]:
        cues: List[SceneCue] = []
        cursor = 0.0
        for scene in self.scenes:
            cue = SceneCue(
                scene_id=scene.id,
                start_time=cursor,
                duration=scene.duration_seconds,
                voiceover=scene.voiceover,
                labels=self._default_labels(scene),
            )
            cues.append(cue)
            cursor += scene.duration_seconds
        return cues

    def export_json(self, cues: List[SceneCue], path: Path) -> None:
        payload = [cue.to_dict() for cue in cues]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _default_labels(self, scene: ParsedScene) -> List[Dict[str, Any]]:
        return [
            {
                "text": scene.label.upper(),
                "start": 0.5,
                "end": min(4.0, scene.duration_seconds - 0.5),
                "anchor": "top_left",
            }
        ]
