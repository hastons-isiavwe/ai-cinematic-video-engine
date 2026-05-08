class ShotDirector:
    def __init__(self):
        self.visual_style = (
    "cinematic realistic film still, dramatic lighting, ultra detailed"
)

    def get_story_phase(self, scene_index, total_scenes):
        if total_scenes <= 1:
            return "setup"

        progress = scene_index / max(total_scenes - 1, 1)

        if progress < 0.25:
            return "setup"
        elif progress < 0.50:
            return "rising_tension"
        elif progress < 0.75:
            return "climax"
        else:
            return "resolution"

    def decide_shot(self, scene_text, scene_index=0, total_scenes=1):
        scene_lower = scene_text.lower()
        phase = self.get_story_phase(scene_index, total_scenes)

        shot_type = "medium cinematic shot"
        camera_motion = "slow cinematic push-in"
        lighting = "soft dramatic lighting"
        mood = "mysterious and emotional"

        if any(word in scene_lower for word in [
            "forest", "village", "kingdom", "palace", "journey"
        ]):
            shot_type = "wide establishing shot"
            camera_motion = "slow sweeping camera movement"

        if any(word in scene_lower for word in [
            "fear", "afraid", "cry", "tears", "alone", "dark"
        ]):
            shot_type = "close-up emotional shot"
            camera_motion = "slow push-in on the character"
            lighting = "low-key dramatic lighting with deep shadows"
            mood = "sad, tense, and emotional"

        if any(word in scene_lower for word in [
            "run", "fight", "escape", "chase", "attack", "danger"
        ]):
            shot_type = "dynamic action shot"
            camera_motion = "fast handheld cinematic motion"
            lighting = "high contrast dramatic lighting"
            mood = "urgent and intense"

        if phase == "setup":
            lighting = "warm natural cinematic lighting"
            mood = "curious and atmospheric"

        elif phase == "rising_tension":
            lighting = "moody dramatic lighting with growing shadows"
            mood = "tense and suspenseful"

        elif phase == "climax":
            lighting = "epic high-contrast cinematic lighting"
            mood = "powerful, dramatic, and intense"

        elif phase == "resolution":
            lighting = "soft golden cinematic lighting"
            mood = "peaceful, emotional, and reflective"

        prompt = (
            f"{shot_type}, "
            f"{scene_text}, "
            f"{lighting}, "
            f"{mood}, "
            f"{camera_motion}, "
            f"{self.visual_style}"
        )

        return {
            "phase": phase,
            "shot_type": shot_type,
            "camera_motion": camera_motion,
            "lighting": lighting,
            "mood": mood,
            "style": self.visual_style,
            "prompt": prompt,
            "width": 1280,
            "height": 720
        }

    def generate_shot_sequence(
        self,
        scene_text,
        scene_index=0,
        total_scenes=1
    ):
        base_shot = self.decide_shot(scene_text, scene_index, total_scenes)

        shots = [
            {
                "shot_number": 1,
                "duration": 3,
                "prompt": (
                    f"wide establishing shot, {scene_text}, "
                    f"{base_shot['lighting']}, {base_shot['mood']}, "
                    f"cinematic environment, atmospheric depth, "
                    f"{self.visual_style}"
                ),
                "phase": base_shot["phase"],
                "shot_type": "wide establishing shot",
                "camera_motion": "slow cinematic pan",
                "lighting": base_shot["lighting"],
                "mood": base_shot["mood"],
                "style": base_shot["style"],
                "width": 1280,
                "height": 720
            },
            {
                "shot_number": 2,
                "duration": 3,
                "prompt": (
                    f"close-up emotional character shot, {scene_text}, "
                    f"{base_shot['lighting']}, expressive face, "
                    f"dramatic cinematic framing, {self.visual_style}"
                ),
                "phase": base_shot["phase"],
                "shot_type": "close-up emotional shot",
                "camera_motion": "slow push-in",
                "lighting": base_shot["lighting"],
                "mood": base_shot["mood"],
                "style": base_shot["style"],
                "width": 1280,
                "height": 720
            },
            {
                "shot_number": 3,
                "duration": 3,
                "prompt": (
                    f"cinematic detail insert shot, symbolic visual detail, "
                    f"{scene_text}, {base_shot['lighting']}, "
                    f"high detail, emotional storytelling, {self.visual_style}"
                ),
                "phase": base_shot["phase"],
                "shot_type": "detail insert shot",
                "camera_motion": "subtle cinematic zoom",
                "lighting": base_shot["lighting"],
                "mood": base_shot["mood"],
                "style": base_shot["style"],
                "width": 1280,
                "height": 720
            }
        ]

        return shots

    def build_prompt(self, scene_text, shot_data):
        prompt = shot_data.get("prompt", "")

        if not prompt:
            prompt = (
                f"{shot_data.get('shot_type', 'cinematic shot')}, "
                f"{scene_text}, "
                f"{shot_data.get('lighting', 'dramatic lighting')}, "
                f"{shot_data.get('mood', 'emotional mood')}, "
                f"{shot_data.get('camera_motion', 'slow cinematic motion')}, "
                f"{self.visual_style}"
            )

                # CLIP token safety
        words = prompt.split()

        MAX_PROMPT_WORDS = 60

        if len(words) > MAX_PROMPT_WORDS:
            prompt = " ".join(words[:MAX_PROMPT_WORDS])

        return prompt

    def detect_emotion(self, scene_text, scene_index=0, total_scenes=1):
        text = scene_text.lower()

        if any(word in text for word in [
            "cry", "sad", "loss", "alone", "heartbroken",
            "grief", "pain", "collapse", "fear"
        ]):
            return "sad"

        elif any(word in text for word in [
            "fight", "run", "danger", "escape",
            "battle", "attack", "urgent"
        ]):
            return "intense"

        elif any(word in text for word in [
            "love", "hope", "success", "peace",
            "victory", "happy", "smile", "joy"
        ]):
            return "uplifting"

        phase = self.get_story_phase(scene_index, total_scenes)

        if phase == "setup":
            return "curious"

        elif phase == "rising_tension":
            return "suspenseful"

        elif phase == "climax":
            return "intense"

        elif phase == "resolution":
            return "uplifting"

        return "cinematic"








