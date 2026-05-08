import os
import re
import json
from typing import List, Dict

def clean_text(text: str) -> str:
    return re.sub(r'\s+', ' ', text).strip()


def split_story_into_scene_audio_payloads(timeline: List[Dict]) -> List[Dict]:
    """
    Converts timeline into per-scene audio generation units.
    Each unit is ready for ElevenLabs TTS.
    """

    audio_units = []

    for i, item in enumerate(timeline):
        if item["type"] != "scene":
            continue

        audio_units.append({
            "scene_id": item["id"],
            "text": clean_text(item["text"]),
            "duration_hint": item.get("duration", 6),
        })

    return audio_units


def save_audio_manifest(audio_units: List[Dict], output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(audio_units, f, indent=2)

    print(f"Audio manifest saved → {output_path}")