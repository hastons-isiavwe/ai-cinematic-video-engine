class ShotDirector:

    def __init__(self):
        pass

    def get_story_phase(self, scene_index, total_scenes):
        progress = scene_index / max(total_scenes - 1, 1)

        if progress <= 0.15:
            return "setup"
        elif progress <= 0.40:
            return "rising_tension"
        elif progress <= 0.70:
            return "crisis"
        elif progress <= 0.90:
            return "reveal"
        else:
            return "resolution"

    def detect_keywords_emotion(self, scene_text):
        text = scene_text.lower()

        if any(word in text for word in [
            "fear", "dark", "shadow", "unknown", "mystery", "nightmare",
            "paranoia", "haunted", "terror", "whisper", "alone", "trapped"
        ]):
            return "fear"

        if any(word in text for word in [
            "battle", "fight", "attack", "danger", "chase", "run", "storm",
            "escape", "crash", "climax", "knife", "collapse"
        ]):
            return "action"

        if any(word in text for word in [
            "sad", "loss", "tears", "grief", "broken", "silence",
            "forgotten", "rejection", "failure", "hospital", "casket"
        ]):
            return "sad"

        if any(word in text for word in [
            "joy", "happy", "bright", "beautiful", "peace", "hope",
            "miracle", "breakthrough", "smile", "healing"
        ]):
            return "joy"

        if any(word in text for word in [
            "realized", "discovered", "truth", "revealed", "understood",
            "suddenly", "shifted"
        ]):
            return "reveal"

        return "neutral"

    def detect_emotion(self, scene_text, scene_index, total_scenes):
        phase = self.get_story_phase(scene_index, total_scenes)
        keyword_emotion = self.detect_keywords_emotion(scene_text)

        if keyword_emotion != "neutral":
            return keyword_emotion

        phase_defaults = {
            "setup": "setup",
            "rising_tension": "sad",
            "crisis": "fear",
            "reveal": "reveal",
            "resolution": "resolution"
        }

        return phase_defaults.get(phase, "neutral")

    def decide_shot(self, scene_text, scene_index, total_scenes=10):
        emotion = self.detect_emotion(scene_text, scene_index, total_scenes)
        phase = self.get_story_phase(scene_index, total_scenes)

        profiles = {
            "setup": {
                "lighting": "golden cinematic light, soft atmosphere",
                "style": "cinematic storybook realism, calm visual introduction",
                "motion": "pan_right",
                "color": "warm and inviting"
            },
            "neutral": {
                "lighting": "soft natural lighting, balanced shadows",
                "style": "cinematic realism, grounded human drama",
                "motion": "zoom_in",
                "color": "natural tones"
            },
            "sad": {
                "lighting": "dim lighting, soft shadows, muted colors",
                "style": "emotional cinematic drama, intimate human sadness",
                "motion": "drift",
                "color": "muted emotional palette"
            },
            "fear": {
                "lighting": "low-key lighting, dramatic shadows, cold blue tone",
                "style": "dark cinematic thriller mood, psychological tension",
                "motion": "zoom_in",
                "color": "cold desaturated palette"
            },
            "action": {
                "lighting": "high contrast lighting, dramatic atmosphere",
                "style": "dynamic action cinematic, urgent visual energy",
                "motion": "zoom_in",
                "color": "high contrast"
            },
            "reveal": {
                "lighting": "dramatic rim light, high contrast shadows",
                "style": "cinematic revelation moment, emotional realization",
                "motion": "zoom_in",
                "color": "dramatic contrast"
            },
            "joy": {
                "lighting": "bright natural lighting, warm tones",
                "style": "uplifting cinematic realism, hopeful atmosphere",
                "motion": "pan_right",
                "color": "warm uplifting palette"
            },
            "resolution": {
                "lighting": "warm sunset light, peaceful atmosphere",
                "style": "emotional cinematic resolution, hopeful ending",
                "motion": "zoom_out",
                "color": "soft golden resolution"
            }
        }

        profile = profiles.get(emotion, profiles["neutral"])

        return {
            "lighting": profile["lighting"],
            "style": profile["style"],
            "motion": profile["motion"],
            "emotion": emotion,
            "phase": phase,
            "color": profile["color"]
        }

    def generate_shot_sequence(self, scene_text, scene_index, total_scenes=10):
        base = self.decide_shot(scene_text, scene_index, total_scenes)
        emotion = base["emotion"]
        phase = base["phase"]

        if phase == "setup":
            return [
                {**base, "shot": "wide establishing shot, subject introduced inside environment", "camera": "slow cinematic pan", "motion": "pan_right"},
                {**base, "shot": "medium shot, character positioned in story world", "camera": "gentle push-in", "motion": "zoom_in"},
                {**base, "shot": "close-up, first emotional connection with character", "camera": "slow push-in", "motion": "zoom_in"},
            ]

        if emotion in ["fear", "sad"]:
            return [
                {**base, "shot": "isolated wide shot, subject small against overwhelming environment", "camera": "slow creeping camera move", "motion": "drift"},
                {**base, "shot": "tight close-up on emotional face, visible inner conflict", "camera": "slow tense push-in", "motion": "zoom_in"},
                {**base, "shot": "over-the-shoulder shot with background tension", "camera": "subtle unstable drifting frame", "motion": "pan_left"},
            ]

        if emotion == "action":
            return [
                {**base, "shot": "dynamic wide shot, dramatic movement and urgency", "camera": "fast cinematic push", "motion": "zoom_in"},
                {**base, "shot": "low-angle hero shot, character under pressure", "camera": "rising camera feel", "motion": "zoom_in"},
                {**base, "shot": "close-up, intense expression and emotional stakes", "camera": "urgent push-in", "motion": "zoom_in"},
            ]

        if emotion == "reveal":
            return [
                {**base, "shot": "wide shot revealing hidden truth or turning point", "camera": "slow dramatic reveal", "motion": "pan_right"},
                {**base, "shot": "medium shot, character realizing something important", "camera": "slow emotional push-in", "motion": "zoom_in"},
                {**base, "shot": "extreme close-up on eyes, emotional realization", "camera": "tight cinematic push-in", "motion": "zoom_in"},
            ]

        if emotion in ["joy", "resolution"]:
            return [
                {**base, "shot": "wide hopeful shot, environment opening up around character", "camera": "smooth cinematic glide", "motion": "pan_right"},
                {**base, "shot": "medium shot, character finding peace or strength", "camera": "gentle floating push", "motion": "drift"},
                {**base, "shot": "close-up, peaceful emotional expression", "camera": "slow pull-back resolution", "motion": "zoom_out"},
            ]

        return [
            {**base, "shot": "wide establishing shot, environmental storytelling", "camera": "slow cinematic pan", "motion": "pan_right"},
            {**base, "shot": "medium shot, character within environment", "camera": "gentle push-in", "motion": "zoom_in"},
            {**base, "shot": "close-up, emotional focus on subject", "camera": "slow push-in", "motion": "zoom_in"},
        ]

    def build_prompt(self, scene_text, shot_data):
        short_scene = scene_text[:90].rsplit(" ", 1)[0]

        return f"""
{shot_data['shot']},
{shot_data['camera']},
{shot_data['lighting']},
{shot_data['style']},
{shot_data['color']},
story phase: {shot_data['phase']},
cinematic {shot_data['emotion']} atmosphere,
scene context: {short_scene},
35mm film still,
cinematic composition,
sharp focus
"""






