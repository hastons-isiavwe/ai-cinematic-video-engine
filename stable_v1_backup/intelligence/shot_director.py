class ShotDirector:

    def __init__(self):
        pass

    def detect_emotion(self, scene_text):
        text = scene_text.lower()

        if any(word in text for word in ["fear", "dark", "scared", "alone"]):
            return "fear"

        elif any(word in text for word in ["happy", "joy", "smile", "laugh"]):
            return "joy"

        elif any(word in text for word in ["fight", "battle", "attack"]):
            return "action"

        elif any(word in text for word in ["sad", "cry", "lost"]):
            return "sad"

        else:
            return "neutral"

    def decide_shot(self, scene_text, scene_index):
        emotion = self.detect_emotion(scene_text)
        scene_text = scene_text.lower()

        if emotion == "fear":
            return {
                "shot": "close-up",
                "lighting": "low-key lighting, dramatic shadows, cold blue tone",
                "camera": "slow push-in",
                "style": "cinematic, moody, high contrast",
                "resolution": (1280, 720),
                "motion": "zoom_in",
                "emotion": emotion
            }

        elif emotion == "joy":
            return {
                "shot": "wide joyful shot",
                "lighting": "bright soft lighting, warm golden tones",
                "camera": "gentle tracking shot",
                "style": "uplifting cinematic realism",
                "resolution": (1280, 720),
                "motion": "pan_right",
                "emotion": emotion
            }

        elif emotion == "action":
            return {
                "shot": "dynamic wide shot",
                "lighting": "high contrast, intense dramatic highlights",
                "camera": "handheld, slight shake",
                "style": "action cinematic",
                "resolution": (1280, 720),
                "motion": "zoom_in",
                "emotion": emotion
            }

        elif emotion == "sad":
            return {
                "shot": "medium close-up",
                "lighting": "dim lighting, desaturated colors, soft shadows",
                "camera": "slow push-in",
                "style": "emotional cinematic realism",
                "resolution": (1280, 720),
                "motion": "zoom_in",
                "emotion": emotion
            }

        elif "portrait" in scene_text:
            return {
                "shot": "close-up portrait",
                "lighting": "soft lighting",
                "camera": "static",
                "style": "cinematic portrait",
                "resolution": (720, 1280),
                "motion": "zoom_in",
                "emotion": emotion
            }

        elif "walk" in scene_text or "enter" in scene_text:
            return {
                "shot": "wide shot",
                "lighting": "natural lighting",
                "camera": "slow tracking shot",
                "style": "cinematic, realistic",
                "resolution": (1280, 720),
                "motion": "pan_right",
                "emotion": emotion
            }

        else:
            return {
                "shot": "medium shot",
                "lighting": "soft lighting",
                "camera": "static",
                "style": "cinematic",
                "resolution": (1280, 720),
                "motion": "static",
                "emotion": emotion
            }

    def build_prompt(self, scene_text, shot_data):
        return f"""
{shot_data['shot']},
{shot_data['camera']},
{shot_data['lighting']},
{shot_data['style']},
{shot_data['emotion']} emotional tone,
{scene_text},
ultra realistic, 4k, cinematic composition
"""














