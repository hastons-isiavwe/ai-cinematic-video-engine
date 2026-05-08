class CharacterEngine:

    def __init__(self):
        self.character_profile = ""

    def extract_characters(self, scenes):
        story_text = " ".join(scenes).lower()

        if "tortoise" in story_text:
            self.character_profile = (
                "same main character in every shot: a wise old tortoise, "
                "small rounded shell with golden brown patterns, expressive eyes, "
                "gentle face, consistent appearance"
            )

        elif "prince" in story_text:
            self.character_profile = (
                "same main character in every shot: young African prince, "
                "royal blue cloak, gold embroidery, calm noble expression, "
                "consistent face and outfit"
            )

        elif "girl" in story_text:
            self.character_profile = (
                "same main character in every shot: young African girl, "
                "simple worn dress, headscarf, expressive eyes, "
                "consistent face and outfit"
            )

        else:
            self.character_profile = (
                "same main character in every shot, consistent face, "
                "consistent outfit, consistent body shape, consistent visual identity"
            )

    def enhance_prompt(self, scene, prompt):
        if self.character_profile:
            return f"{self.character_profile}, {prompt}"

        return prompt

    def get_character_description(self):
        return self.character_profile








