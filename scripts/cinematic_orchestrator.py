# scripts/cinematic_orchestrator.py

from scripts.scene_extractor import split_into_scenes
from scripts.emotion_analyzer import analyze_emotion


class CinematicOrchestrator:

    def build_timeline(self, story_text, max_scenes=8):
        scenes = split_into_scenes(story_text, max_scenes=max_scenes)

        timeline = []

        for i, scene_text in enumerate(scenes):

            emotion, score = analyze_emotion(scene_text)

            scene = {
                "id": i + 1,
                "type": "scene",
                "text": scene_text,
                "emotion": emotion,
                "score": score,
                "camera": self._camera(emotion),
                "lighting": self._lighting(emotion),
                "duration": self._duration(score),
                "broll_allowed": score > 0.55,
                "broll_hint": self._broll_hint(scene_text, emotion)
            }

            timeline.append(scene)

        return timeline

    # --------------------------
    # DECISION SYSTEMS
    # --------------------------

    def _camera(self, emotion):
        if emotion == "high":
            return "handheld cinematic shake, fast push-in"
        if emotion == "medium":
            return "steady tracking shot"
        return "slow wide establishing shot"

    def _lighting(self, emotion):
        if emotion == "high":
            return "high contrast dramatic lighting"
        if emotion == "medium":
            return "balanced cinematic lighting"
        return "soft natural ambient lighting"

    def _duration(self, score):
        if score > 0.7:
            return 4
        if score > 0.4:
            return 6
        return 8

    def _broll_hint(self, text, emotion):
        base = text[:120]

        if emotion == "high":
            return f"dramatic cinematic b-roll, intense atmosphere, {base}"
        if emotion == "medium":
            return f"cinematic storytelling b-roll, balanced tone, {base}"
        return f"calm ambient cinematic b-roll, soft mood, {base}"