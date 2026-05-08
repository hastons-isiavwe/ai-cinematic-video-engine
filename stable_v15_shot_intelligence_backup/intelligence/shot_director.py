class ShotDirector:

    def __init__(self):
        pass

    def detect_emotion(self, scene_text, scene_index, total_scenes):
        text = scene_text.lower()

        if any(word in text for word in [
            "fear", "dark", "shadow", "unknown", "mystery", "nightmare",
            "paranoia", "haunted", "terror", "whisper", "alone"
        ]):
            return "fear"

        if any(word in text for word in [
            "battle", "fight", "attack", "danger", "chase", "run", "storm",
            "escape", "crash", "climax"
        ]):
            return "action"

        if any(word in text for word in [
            "sad", "loss", "tears", "grief", "broken", "silence",
            "forgotten", "rejection", "failure"
        ]):
            return "sad"

        if any(word in text for word in [
            "joy", "happy", "bright", "beautiful", "peace", "hope",
            "miracle", "breakthrough", "smile"
        ]):
            return "joy"

        if any(word in text for word in [
            "realized", "discovered", "truth", "revealed", "understood"
        ]):
            return "reveal"

        if scene_index == 0:
            return "setup"
        elif scene_index < total_scenes * 0.4:
            return "neutral"
        elif scene_index < total_scenes * 0.7:
            return "fear"
        elif scene_index < total_scenes * 0.9:
            return "reveal"
        else:
            return "resolution"

    def decide_shot(self, scene_text, scene_index, total_scenes=10):
        emotion = self.detect_emotion(scene_text, scene_index, total_scenes)

        profiles = {
            "setup": {
                "lighting": "golden cinematic light, soft atmosphere",
                "style": "cinematic, storybook realism",
                "motion": "pan_right"
            },
            "neutral": {
                "lighting": "soft natural lighting, balanced shadows",
                "style": "cinematic realism",
                "motion": "zoom_in"
            },
            "fear": {
                "lighting": "low-key lighting, dramatic shadows, cold blue tone",
                "style": "dark cinematic thriller mood",
                "motion": "zoom_in"
            },
            "sad": {
                "lighting": "dim lighting, soft shadows, muted colors",
                "style": "emotional cinematic drama",
                "motion": "zoom_in"
            },
            "joy": {
                "lighting": "bright natural lighting, warm tones",
                "style": "uplifting cinematic realism",
                "motion": "pan_right"
            },
            "action": {
                "lighting": "high contrast lighting, dramatic atmosphere",
                "style": "dynamic action cinematic",
                "motion": "zoom_in"
            },
            "reveal": {
                "lighting": "dramatic rim light, high contrast shadows",
                "style": "cinematic revelation moment",
                "motion": "zoom_in"
            },
            "resolution": {
                "lighting": "warm sunset light, peaceful atmosphere",
                "style": "emotional cinematic resolution",
                "motion": "zoom_out"
            }
        }

        profile = profiles.get(emotion, profiles["neutral"])

        return {
            "lighting": profile["lighting"],
            "style": profile["style"],
            "motion": profile["motion"],
            "emotion": emotion
        }

    def generate_shot_sequence(self, scene_text, scene_index, total_scenes=10):
        base = self.decide_shot(scene_text, scene_index, total_scenes)
        emotion = base["emotion"]

        if emotion in ["fear", "sad"]:
            return [
                {
                    **base,
                    "shot": "isolated wide shot, subject small in environment",
                    "camera": "slow creeping camera move",
                    "motion": "zoom_in"
                },
                {
                    **base,
                    "shot": "tight close-up on emotional face",
                    "camera": "slow push-in",
                    "motion": "zoom_in"
                },
                {
                    **base,
                    "shot": "over-the-shoulder shot with background tension",
                    "camera": "subtle drifting frame",
                    "motion": "pan_left"
                },
            ]

        elif emotion == "action":
            return [
                {
                    **base,
                    "shot": "dynamic wide shot, dramatic movement",
                    "camera": "fast cinematic push",
                    "motion": "zoom_in"
                },
                {
                    **base,
                    "shot": "low-angle hero shot",
                    "camera": "rising camera feel",
                    "motion": "zoom_in"
                },
                {
                    **base,
                    "shot": "close-up, intense expression",
                    "camera": "urgent push-in",
                    "motion": "zoom_in"
                },
            ]

        elif emotion == "reveal":
            return [
                {
                    **base,
                    "shot": "wide shot revealing hidden truth",
                    "camera": "slow dramatic reveal",
                    "motion": "pan_right"
                },
                {
                    **base,
                    "shot": "medium shot, character realizing something important",
                    "camera": "slow push-in",
                    "motion": "zoom_in"
                },
                {
                    **base,
                    "shot": "close-up on eyes, emotional realization",
                    "camera": "tight cinematic push-in",
                    "motion": "zoom_in"
                },
            ]

        else:
            return [
                {
                    **base,
                    "shot": "wide establishing shot, environmental storytelling",
                    "camera": "slow cinematic pan",
                    "motion": "pan_right"
                },
                {
                    **base,
                    "shot": "medium shot, character within environment",
                    "camera": "gentle push-in",
                    "motion": "zoom_in"
                },
                {
                    **base,
                    "shot": "close-up, emotional focus on subject",
                    "camera": "slow push-in",
                    "motion": "zoom_in"
                },
            ]

    def build_prompt(self, scene_text, shot_data):
        short_scene = scene_text[:90].rsplit(" ", 1)[0]

        return f"""
{shot_data['shot']},
{shot_data['camera']},
{shot_data['lighting']},
{shot_data['style']},
cinematic {shot_data['emotion']} atmosphere,
scene context: {short_scene},
35mm film still,
cinematic composition,
sharp focus
"""