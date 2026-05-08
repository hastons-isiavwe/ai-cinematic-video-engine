import re


class CharacterEngine:

    def __init__(self):
        self.character_profile = ""

    def extract_characters(self, story):
        story_lower = story.lower()

        # -----------------------------
        # FIRST PERSON STORY HANDLING
        # -----------------------------
        if " i " in f" {story_lower} " or " my " in f" {story_lower} ":
            self.character_profile = """
same main character in every shot: emotionally expressive adult woman,
natural skin tone,
modern clothing,
cinematic lighting,
consistent identity across all shots
"""
            return

        # -----------------------------
        # SPECIAL CASES
        # -----------------------------
        if "village elder" in story_lower or "elder" in story_lower:
            self.character_profile = """
same main character in every shot: wise elderly African woman,
weathered expressive face,
traditional clothing and headscarf,
cinematic lighting,
consistent identity across all shots
"""
            return

        if "tortoise" in story_lower:
            self.character_profile = """
same main character in every shot: wise old tortoise,
small rounded shell with golden brown patterns,
expressive eyes,
consistent appearance across all shots
"""
            return

        if "boy" in story_lower or "grandson" in story_lower:
            self.character_profile = """
same main character in every shot: young boy,
curious expressive eyes,
simple clothing,
natural skin tone,
consistent identity across all shots
"""
            return

        # -----------------------------
        # GENERIC NAME EXTRACTION
        # -----------------------------
        ignore_words = [
            "The", "As", "But", "And", "With", "That",
            "Anansi", "Nana", "God", "When", "Every", "Then",
            "His", "Her", "She", "He", "They", "Their",
            "My", "We", "Our", "One", "No", "For", "In", "It"
        ]

        matches = re.findall(r"\b[A-Z][a-z]{2,}\b", story)

        name = None
        for word in matches:
            if word not in ignore_words:
                name = word
                break

        if name:
            self.character_profile = f"""
same main character in every shot: {name},
adult human character,
expressive face,
natural skin tone,
cinematic clothing suitable to the story,
cinematic lighting,
consistent identity across all shots
"""
        else:
            self.character_profile = """
same main character in every shot,
consistent face,
consistent outfit,
consistent identity across all shots
"""

    def enhance_prompt(self, scene, prompt):
        return f"{self.character_profile}, {prompt}"

    def get_character_description(self):
        return self.character_profile










