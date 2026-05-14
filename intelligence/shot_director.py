class ShotDirector:

    def __init__(self, video_style="cinematic"):
        self.video_style = video_style

        self.visual_style = (
            "cinematic realistic film still, dramatic lighting, ultra detailed"
        )

        if self.video_style == "music_video":
            self.visual_style = (
                "high-energy cinematic music video still, dramatic contrast, "
                "stylized lighting, dynamic framing, ultra detailed"
            )

        self.story_memory = {
            "locations": set(),
            "objects": set(),
            "relationships": set(),
            "emotions": [],
            "symbols": set(),
        }

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

    def update_story_memory(self, scene_text):
        text = scene_text.lower()

        location_keywords = [
            "forest", "village", "beach", "palace", "kingdom", "river",
            "mountain", "town", "house", "home", "church", "market",
            "road", "school", "moonlit beach"
        ]

        object_keywords = [
            "box", "moon", "necklace", "book", "ring", "letter",
            "lamp", "candle", "sword", "crown", "stone", "photo"
        ]

        relationship_keywords = [
            "mother", "father", "grandmother", "grandfather",
            "brother", "sister", "friend", "wife", "husband"
        ]

        for word in location_keywords:
            if word in text:
                self.story_memory["locations"].add(word)

        for word in object_keywords:
            if word in text:
                self.story_memory["objects"].add(word)

        for word in relationship_keywords:
            if word in text:
                self.story_memory["relationships"].add(word)

        emotion = self.detect_emotion(scene_text)
        self.story_memory["emotions"].append(emotion)

        if "moon" in text:
            self.story_memory["symbols"].add("moonlight symbolism")
        if "light" in text:
            self.story_memory["symbols"].add("guiding light")
        if "darkness" in text:
            self.story_memory["symbols"].add("darkness vs hope")

    def build_continuity_context(self):
        context_parts = []

        if self.story_memory["locations"]:
            locations = ", ".join(list(self.story_memory["locations"])[:3])
            context_parts.append(
                f"consistent cinematic environment inspired by {locations}"
            )

        if self.story_memory["objects"]:
            objects = ", ".join(list(self.story_memory["objects"])[:3])
            context_parts.append(
                f"recurring symbolic objects including {objects}"
            )

        if self.story_memory["relationships"]:
            relationships = ", ".join(list(self.story_memory["relationships"])[:3])
            context_parts.append(
                f"emotionally grounded relationship themes involving {relationships}"
            )

        if self.story_memory["symbols"]:
            symbols = ", ".join(list(self.story_memory["symbols"])[:2])
            context_parts.append(
                f"visual symbolism connected to {symbols}"
            )

        return ", ".join(context_parts)

    def decide_shot(self, scene_text, scene_index=0, total_scenes=1):
        self.update_story_memory(scene_text)

        scene_lower = scene_text.lower()
        phase = self.get_story_phase(scene_index, total_scenes)

        shot_type = "medium cinematic shot"
        camera_motion = "slow cinematic push-in"
        lighting = "soft dramatic lighting"
        mood = "mysterious and emotional"

        if any(word in scene_lower for word in [
            "forest", "village", "kingdom", "palace", "journey", "beach"
        ]):
            shot_type = "wide establishing shot"
            camera_motion = "slow sweeping cinematic camera movement"

        if any(word in scene_lower for word in [
            "fear", "afraid", "cry", "tears", "alone", "dark",
            "grief", "pain", "loss"
        ]):
            shot_type = "close-up emotional shot"
            camera_motion = "slow emotional push-in on the character"
            lighting = "low-key dramatic lighting with deep shadows"
            mood = "sad, emotional, and reflective"

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
            mood = "powerful, dramatic, and emotionally intense"
        elif phase == "resolution":
            lighting = "soft golden cinematic lighting"
            mood = "peaceful, emotional, and reflective"

        if self.video_style == "music_video":
            camera_motion = "dynamic rhythmic camera movement"

            if phase == "setup":
                shot_type = "stylized wide cinematic music-video shot"
                lighting = "colorful atmospheric cinematic lighting"
                mood = "emotional, stylish, and anticipatory"
            elif phase == "rising_tension":
                shot_type = "dynamic close-up music-video shot"
                lighting = "high-contrast moody stylized lighting"
                mood = "intense, emotional, and rhythmic"
            elif phase == "climax":
                shot_type = "dramatic performance-style cinematic shot"
                lighting = "epic flashing high-contrast cinematic lighting"
                mood = "powerful, expressive, and visually explosive"
            elif phase == "resolution":
                shot_type = "soft emotional slow-motion music-video shot"
                lighting = "glowing golden cinematic backlight"
                mood = "emotional, reflective, and triumphant"

        continuity_context = self.build_continuity_context()

        prompt = (
            f"{shot_type}, {scene_text}, {lighting}, {mood}, "
            f"{camera_motion}, {continuity_context}, {self.visual_style}"
        )

        return {
            "phase": phase,
            "shot_type": shot_type,
            "camera_motion": camera_motion,
            "lighting": lighting,
            "mood": mood,
            "style": self.visual_style,
            "continuity_context": continuity_context,
            "prompt": prompt,
            "width": 1280,
            "height": 720
        }

    def generate_shot_sequence(self, scene_text, scene_index=0, total_scenes=1):
        base_shot = self.decide_shot(scene_text, scene_index, total_scenes)
        continuity = base_shot.get("continuity_context", "")
        shot_type = base_shot["shot_type"]

        if self.video_style == "music_video":
            shot_1_type = shot_type
            shot_2_type = shot_type
            shot_3_type = f"{shot_type}, symbolic visual detail"
            shot_1_motion = "rhythmic cinematic pan"
            shot_2_motion = "dynamic push-in"
            shot_3_motion = "stylized rhythmic zoom"
        else:
            shot_1_type = "wide establishing shot"
            shot_2_type = "close-up emotional character shot"
            shot_3_type = "cinematic detail insert shot, symbolic visual detail"
            shot_1_motion = "slow cinematic pan"
            shot_2_motion = "slow push-in"
            shot_3_motion = "subtle cinematic zoom"

        shots = [
            {
                "shot_number": 1,
                "duration": 3,
                "prompt": (
                    f"{shot_1_type}, {scene_text}, "
                    f"{base_shot['lighting']}, {base_shot['mood']}, "
                    f"cinematic environment, atmospheric depth, "
                    f"{continuity}, {self.visual_style}"
                ),
                "phase": base_shot["phase"],
                "shot_type": shot_1_type,
                "camera_motion": shot_1_motion,
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
                    f"{shot_2_type}, {scene_text}, "
                    f"{base_shot['lighting']}, expressive face, "
                    f"dramatic music-video framing, {continuity}, "
                    f"{self.visual_style}"
                ),
                "phase": base_shot["phase"],
                "shot_type": shot_2_type,
                "camera_motion": shot_2_motion,
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
                    f"{shot_3_type}, {scene_text}, "
                    f"{base_shot['lighting']}, high detail, "
                    f"emotional visual rhythm, {continuity}, "
                    f"{self.visual_style}"
                ),
                "phase": base_shot["phase"],
                "shot_type": shot_3_type,
                "camera_motion": shot_3_motion,
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
                f"{shot_data.get('continuity_context', '')}, "
                f"{self.visual_style}"
            )

        words = prompt.split()
        MAX_PROMPT_WORDS = 75

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
            "fight", "run", "danger", "escape", "battle",
            "attack", "urgent"
        ]):
            return "intense"

        elif any(word in text for word in [
            "love", "hope", "success", "peace", "victory",
            "happy", "smile", "joy"
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