class BrollEngine:

    def __init__(self):
        pass

    def should_add_broll(self, scene_text):
        text = scene_text.lower()

        keywords = ["silent", "alone", "empty", "night", "waiting", "watching"]

        return any(word in text for word in keywords)

    def generate_broll_prompt(self, scene_text):
        return f"""
cinematic b-roll, environment shot,
{scene_text},
no people, atmospheric, ultra realistic, 4k
"""