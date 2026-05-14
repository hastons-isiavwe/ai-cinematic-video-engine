class ShotDirector:

    def __init__(self):

        self.visual_style = (
            "cinematic realistic film still, dramatic lighting, ultra detailed"
        )

        # -----------------------------------
        # STORY CONTINUITY MEMORY
        # -----------------------------------
        self.story_memory = {
            "locations": set(),
            "objects": set(),
            "relationships": set(),
            "emotions": [],
            "symbols": set(),
        }

    # -----------------------------------
    # STORY PHASE DETECTION
    # -----------------------------------
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

        return "resolution"

    # -----------------------------------
    # CONTINUITY MEMORY ANALYSIS
    # -----------------------------------
    def update_story_memory(self, scene_text):

        text = scene_text.lower()

        # LOCATIONS
        location_keywords = [
            "forest", "village", "beach", "palace",
            "kingdom", "river", "mountain", "town",
            "house", "home", "church", "market",
            "road", "school", "moonlit beach"
        ]

        # SYMBOLIC OBJECTS
        object_keywords = [
            "box", "moon", "necklace", "book",
            "ring", "letter", "lamp", "candle",
            "sword", "crown", "stone", "photo"
        ]

        # RELATIONSHIPS
        relationship_keywords = [
            "mother", "father", "grandmother",
            "grandfather", "brother", "sister",
            "friend", "wife", "husband"
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

        # SYMBOLIC MEMORY
        if "moon" in text:
            self.story_memory["symbols"].add("moonlight symbolism")

        if "light" in text:
            self.story_memory["symbols"].add("guiding light")

        if "darkness" in text:
            self.story_memory["symbols"].add("darkness vs hope")

    # -----------------------------------
    # BUILD CONTINUITY CONTEXT
    # -----------------------------------
    def build_continuity_context(self):

        context_parts = []

        if self.story_memory["locations"]:
            locations = ", ".join(
                list(self.story_memory["locations"])[:3]
            )

            context_parts.append(
                f"consistent cinematic environment inspired by {locations}"
            )

        if self.story_memory["objects"]:
            objects = ", ".join(
                list(self.story_memory["objects"])[:3]
            )

            context_parts.append(
                f"recurring symbolic objects including {objects}"
            )

        if self.story_memory["relationships"]:
            relationships = ", ".join(
                list(self.story_memory["relationships"])[:3]
            )

            context_parts.append(
                f"emotionally grounded relationship themes involving {relationships}"
            )

        if self.story_memory["symbols"]:
            symbols = ", ".join(
                list(self.story_memory["symbols"])[:2]
            )

            context_parts.append(
                f"visual symbolism connected to {symbols}"
            )

        return ", ".join(context_parts)

    # -----------------------------------
    # SHOT DECISION LOGIC
    # -----------------------------------
    def decide_shot(
        self,
        scene_text,
        scene_index=0,
        total_scenes=1
    ):

        self.update_story_memory(scene_text)

        scene_lower = scene_text.lower()

        phase = self.get_story_phase(
            scene_index,
            total_scenes
        )

        shot_type = "medium cinematic shot"

        camera_motion = "slow cinematic push-in"

        lighting = "soft dramatic lighting"

        mood = "mysterious and emotional"

        # -----------------------------------
        # ENVIRONMENT SHOTS
        # -----------------------------------
        if any(word in scene_lower for word in [
            "forest", "village", "kingdom",
            "palace", "journey", "beach"
        ]):

            shot_type = "wide establishing shot"

            camera_motion = (
                "slow sweeping cinematic camera movement"
            )

        # -----------------------------------
        # EMOTIONAL SCENES
        # -----------------------------------
        if any(word in scene_lower for word in [
            "fear", "afraid", "cry",
            "tears", "alone", "dark",
            "grief", "pain", "loss"
        ]):

            shot_type = "close-up emotional shot"

            camera_motion = (
                "slow emotional push-in on the character"
            )

            lighting = (
                "low-key dramatic lighting with deep shadows"
            )

            mood = "sad, emotional, and reflective"

        # -----------------------------------
        # ACTION SCENES
        # -----------------------------------
        if any(word in scene_lower for word in [
            "run", "fight", "escape",
            "chase", "attack", "danger"
        ]):

            shot_type = "dynamic action shot"

            camera_motion = (
                "fast handheld cinematic motion"
            )

            lighting = (
                "high contrast dramatic lighting"
            )

            mood = "urgent and intense"

        # -----------------------------------
        # STORY ARC PHASE
        # -----------------------------------
        if phase == "setup":

            lighting = "warm natural cinematic lighting"

            mood = "curious and atmospheric"

        elif phase == "rising_tension":

            lighting = (
                "moody dramatic lighting with growing shadows"
            )

            mood = "tense and suspenseful"

        elif phase == "climax":

            lighting = (
                "epic high-contrast cinematic lighting"
            )

            mood = "powerful, dramatic, and emotionally intense"

        elif phase == "resolution":

            lighting = (
                "soft golden cinematic lighting"
            )

            mood = "peaceful, emotional, and reflective"

        continuity_context = self.build_continuity_context()

        prompt = (
            f"{shot_type}, "
            f"{scene_text}, "
            f"{lighting}, "
            f"{mood}, "
            f"{camera_motion}, "
            f"{continuity_context}, "
            f"{self.visual_style}"
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

    # -----------------------------------
    # SHOT SEQUENCE GENERATION
    # -----------------------------------
    def generate_shot_sequence(
        self,
        scene_text,
        scene_index=0,
        total_scenes=1
    ):

        base_shot = self.decide_shot(
            scene_text,
            scene_index,
            total_scenes
        )

        continuity = base_shot.get(
            "continuity_context",
            ""
        )

        shots = [

            {
                "shot_number": 1,
                "duration": 3,
                "prompt": (
                    f"wide establishing shot, "
                    f"{scene_text}, "
                    f"{base_shot['lighting']}, "
                    f"{base_shot['mood']}, "
                    f"cinematic environment, "
                    f"atmospheric depth, "
                    f"{continuity}, "
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
                    f"close-up emotional character shot, "
                    f"{scene_text}, "
                    f"{base_shot['lighting']}, "
                    f"expressive face, "
                    f"dramatic cinematic framing, "
                    f"{continuity}, "
                    f"{self.visual_style}"
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
                    f"cinematic detail insert shot, "
                    f"symbolic visual detail, "
                    f"{scene_text}, "
                    f"{base_shot['lighting']}, "
                    f"high detail, emotional storytelling, "
                    f"{continuity}, "
                    f"{self.visual_style}"
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

    # -----------------------------------
    # FINAL PROMPT BUILDING
    # -----------------------------------
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

        # CLIP token safety
        words = prompt.split()

        MAX_PROMPT_WORDS = 75

        if len(words) > MAX_PROMPT_WORDS:
            prompt = " ".join(words[:MAX_PROMPT_WORDS])

        return prompt

    # -----------------------------------
    # EMOTION DETECTION
    # -----------------------------------
    def detect_emotion(
        self,
        scene_text,
        scene_index=0,
        total_scenes=1
    ):

        text = scene_text.lower()

        if any(word in text for word in [
            "cry", "sad", "loss", "alone",
            "heartbroken", "grief", "pain",
            "collapse", "fear"
        ]):
            return "sad"

        elif any(word in text for word in [
            "fight", "run", "danger",
            "escape", "battle",
            "attack", "urgent"
        ]):
            return "intense"

        elif any(word in text for word in [
            "love", "hope", "success",
            "peace", "victory",
            "happy", "smile", "joy"
        ]):
            return "uplifting"

        phase = self.get_story_phase(
            scene_index,
            total_scenes
        )

        if phase == "setup":
            return "curious"

        elif phase == "rising_tension":
            return "suspenseful"

        elif phase == "climax":
            return "intense"

        elif phase == "resolution":
            return "uplifting"

        return "cinematic"