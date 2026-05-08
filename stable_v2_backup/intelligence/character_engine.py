class CharacterEngine:

    def __init__(self):
        self.characters = {}

    def extract_characters(self, scenes):
        # VERY simple first version
        for scene in scenes:
            words = scene.split()

            for word in words:
                if word.lower() in ["man", "woman", "girl", "boy", "king", "queen"]:
                    if word not in self.characters:
                        self.characters[word] = self.build_identity(word)

        return self.characters

    def build_identity(self, name):
        return {
            "description": f"{name}, consistent appearance, same face, same outfit",
        }

    def enhance_prompt(self, scene, base_prompt):
        for name, data in self.characters.items():
            if name.lower() in scene.lower():
                return base_prompt + f", {data['description']}"

        return base_prompt