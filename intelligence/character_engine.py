import re
from collections import Counter


class CharacterEngine:
    def __init__(self):
        self.character_profile = ""
        self.profile = {
            "name": "Main Character",
            "gender": "neutral",
            "age_range": "adult",
            "role": "central protagonist",
            "emotional_state": "emotionally expressive",
            "visual_description": (
                "expressive face, natural skin tone, cinematic clothing "
                "suitable to the story, cinematic lighting"
            ),
            "consistency_prompt": "",
        }

    def _clean_story(self, story: str) -> str:
        return story.replace("\n", " ").strip()

    def _extract_candidate_names(self, story: str):
        candidates = re.findall(r"\b[A-Z][a-z]{2,}\b", story)

        blacklist = {
   	    "The", "As", "But", "And", "With", "Hook", "Why", "What",
    	    "Then", "That", "This", "Those", "These", "When", "Where",
    	    "Because", "Suddenly", "After", "Before", "Every", "Even",
    	    "Darkness", "Within", "Light", "Moon", "Night", "Stars",
    	    "Sky", "Sun", "Dawn", "Morning", "Evening", "Village",
    	    "Forest", "Beach", "House", "Home",

   	    # NEW FILTERS
    	    "For", "From", "Into", "Over", "Under",
    	    "During", "Through", "Weeks", "Days",
    	    "Months", "Years"
	}

        names = [name for name in candidates if name not in blacklist]

        return names

    def extract_main_character(self, story: str) -> str:
        names = self._extract_candidate_names(story)

        if not names:
            return "Main Character"

        counts = Counter(names)

        return counts.most_common(1)[0][0]

    def _infer_gender(self, story_lower: str, name: str) -> str:
        female_markers = [
            "she", "her", "hers", "mother", "grandmother", "girl",
            "daughter", "woman", "sister", "queen", "princess", "wife"
        ]

        male_markers = [
            "he", "him", "his", "father", "grandfather", "boy",
            "son", "man", "brother", "king", "prince", "husband"
        ]

        female_score = sum(story_lower.count(f" {m} ") for m in female_markers)
        male_score = sum(story_lower.count(f" {m} ") for m in male_markers)

        if female_score > male_score:
            return "female"

        if male_score > female_score:
            return "male"

        return "neutral"

    def _infer_age_range(self, story_lower: str) -> str:
        if any(word in story_lower for word in ["little girl", "young girl", "girl", "daughter"]):
            return "young girl"

        if any(word in story_lower for word in ["little boy", "young boy", "boy", "son"]):
            return "young boy"

        if any(word in story_lower for word in ["teen", "teenager", "adolescent"]):
            return "teenager"

        if any(word in story_lower for word in ["elder", "elderly", "old woman", "old man", "grandmother", "grandfather"]):
            return "elderly adult"

        if any(word in story_lower for word in ["mother", "father", "woman", "man"]):
            return "adult"

        return "adult"

    def _infer_role(self, story_lower: str, gender: str) -> str:
        if "mother" in story_lower and "passed away" in story_lower:
            return "grieving child remembering their mother"

        if "father" in story_lower and "passed away" in story_lower:
            return "grieving child remembering their father"

        if "grandmother" in story_lower:
            return "grieving grandchild remembering their grandmother"

        if "grandfather" in story_lower:
            return "grieving grandchild remembering their grandfather"

        if "friend" in story_lower or "best friend" in story_lower:
            return "lonely friend processing loss and memory"

        if "village" in story_lower:
            return "brave village protagonist"

        if "princess" in story_lower:
            return "young princess"

        if "prince" in story_lower:
            return "young prince"

        if "king" in story_lower:
            return "noble king"

        if "queen" in story_lower:
            return "noble queen"

        if gender == "female":
            return "female protagonist"

        if gender == "male":
            return "male protagonist"

        return "central protagonist"

    def _infer_emotional_state(self, story_lower: str) -> str:
        if any(word in story_lower for word in ["grief", "grieving", "passed away", "loss", "lost", "tears"]):
            return "grieving but hopeful"

        if any(word in story_lower for word in ["fear", "afraid", "terrified", "darkness"]):
            return "fearful but courageous"

        if any(word in story_lower for word in ["joy", "happy", "celebrated", "smiled"]):
            return "joyful and hopeful"

        if any(word in story_lower for word in ["lonely", "alone", "emptiness"]):
            return "lonely but searching for hope"

        return "emotionally expressive and resilient"

    def _build_visual_description(self, gender: str, age_range: str, role: str) -> str:
        if "tortoise" in role:
            return (
                "wise old tortoise, small rounded shell with golden brown patterns, "
                "expressive eyes, consistent appearance across all shots"
            )

        gender_phrase = {
            "female": "female character",
            "male": "male character",
            "neutral": "human character",
        }.get(gender, "human character")

        return (
            f"{age_range} {gender_phrase}, expressive face, natural skin tone, "
            "cinematic clothing suitable to the story, soft emotional lighting, "
            "consistent face, consistent outfit"
        )

    def _build_consistency_prompt(self):
        name = self.profile["name"]
        age_range = self.profile["age_range"]
        role = self.profile["role"]
        emotional_state = self.profile["emotional_state"]
        visual = self.profile["visual_description"]

        return (
            f"same main character in every shot: {name}, "
            f"{age_range}, {role}, {emotional_state}, {visual}, "
            "consistent identity across all shots"
        )

    def analyze_story(self, story: str):
        story = self._clean_story(story)
        story_lower = story.lower()

        # Animal/special folktale handling
        if "tortoise" in story_lower:
            self.profile = {
                "name": "Tortoise",
                "gender": "neutral",
                "age_range": "old",
                "role": "wise old tortoise",
                "emotional_state": "clever and resilient",
                "visual_description": (
                    "wise old tortoise, small rounded shell with golden brown patterns, "
                    "expressive eyes, consistent appearance across all shots"
                ),
                "consistency_prompt": "",
            }

            self.profile["consistency_prompt"] = self._build_consistency_prompt()
            self.character_profile = self.profile["consistency_prompt"]
            return self.profile

        name = self.extract_main_character(story)

        # Avoid bad protagonist names
        if name.lower() in ["it", "the", "as", "but", "and"]:
            name = "Main Character"

        gender = self._infer_gender(story_lower, name)
        age_range = self._infer_age_range(story_lower)
        role = self._infer_role(story_lower, gender)
        emotional_state = self._infer_emotional_state(story_lower)
        visual_description = self._build_visual_description(
            gender,
            age_range,
            role,
        )

        # First-person stories should not become "I" or "It"
        if name == "Main Character" and (
            " i " in f" {story_lower} " or " my " in f" {story_lower} "
        ):
            if gender == "female":
                name = "the woman"
            elif gender == "male":
                name = "the man"
            else:
                name = "the narrator"

        self.profile = {
            "name": name,
            "gender": gender,
            "age_range": age_range,
            "role": role,
            "emotional_state": emotional_state,
            "visual_description": visual_description,
            "consistency_prompt": "",
        }

        self.profile["consistency_prompt"] = self._build_consistency_prompt()
        self.character_profile = self.profile["consistency_prompt"]

        return self.profile

    def extract_characters(self, story):
        self.analyze_story(story)
        return self.character_profile

    def enhance_prompt(self, scene, prompt):
        if not self.character_profile:
            return prompt

        return f"{self.character_profile}, {prompt}"

    def get_character_description(self):
        return self.character_profile

    def get_profile(self):
        return self.profile








