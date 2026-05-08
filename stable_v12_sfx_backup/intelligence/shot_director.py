class ShotDirector:

    def __init__(self):
        pass

    def detect_emotion(self, scene_text, scene_index, total_scenes):
        text = scene_text.lower()

        if any(word in text for word in ["fear", "dark", "shadow", "unknown", "mystery"]):
            return "fear"

        if any(word in text for word in ["battle", "fight", "attack", "danger"]):
            return "action"

        if any(word in text for word in ["sad", "loss", "alone", "silence"]):
            return "sad"

        if any(word in text for word in ["joy", "happy", "bright", "beautiful", "peace"]):
            return "joy"

        if scene_index == 0:
            return "joy"
        elif scene_index < total_scenes * 0.4:
            return "neutral"
        elif scene_index < total_scenes * 0.7:
            return "fear"
        elif scene_index < total_scenes * 0.9:
            return "action"
        else:
            return "sad"

    def decide_shot(self, scene_text, scene_index, total_scenes=10):
        emotion = self.detect_emotion(scene_text, scene_index, total_scenes)

        if emotion == "fear":
            return {
                "shot": "close-up",
                "lighting": "low-key lighting, dramatic shadows, cold blue tone",
                "camera": "slow push-in",
                "style": "cinematic, moody",
                "motion": "zoom_in",
                "emotion": emotion
            }

        elif emotion == "joy":
            return {
                "shot": "wide shot",
                "lighting": "bright natural lighting, warm tones",
                "camera": "gentle tracking shot",
                "style": "cinematic, uplifting",
                "motion": "pan_right",
                "emotion": emotion
            }

        elif emotion == "action":
            return {
                "shot": "dynamic wide shot",
                "lighting": "high contrast, dramatic",
                "camera": "handheld",
                "style": "action cinematic",
                "motion": "zoom_in",
                "emotion": emotion
            }

        elif emotion == "sad":
            return {
                "shot": "medium close-up",
                "lighting": "dim lighting, soft shadows, muted colors",
                "camera": "slow push-in",
                "style": "emotional cinematic",
                "motion": "zoom_in",
                "emotion": emotion
            }

        else:
            return {
                "shot": "medium shot",
                "lighting": "soft natural lighting",
                "camera": "static",
                "style": "cinematic",
                "motion": "static",
                "emotion": emotion
            }

    def generate_shot_sequence(self, scene_text, scene_index, total_scenes=10):
        base = self.decide_shot(scene_text, scene_index, total_scenes)

        return [
            {
                **base,
                "shot": "wide establishing shot, environmental storytelling",
                "camera": "slow cinematic pan",
                "motion": "pan_right"
            },
            {
                **base,
                "shot": "over-the-shoulder shot, perspective view",
                "camera": "steady framing",
                "motion": "static"
            },
            {
                **base,
                "shot": "close-up, emotional focus on subject",
                "camera": "slow push-in",
                "motion": "zoom_in"
            },
        ]

    def build_prompt(self, scene_text, shot_data):
        short_scene = scene_text[:140]

        return f"""
{shot_data['shot']},
{shot_data['camera']},
{shot_data['lighting']},
{shot_data['style']},
cinematic {shot_data['emotion']} atmosphere,
scene context: {short_scene},
35mm film still,
cinematic composition,
detailed environment,
natural lighting,
shallow depth of field,
sharp focus
"""