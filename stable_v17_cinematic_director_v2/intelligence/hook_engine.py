class HookEngine:

    def generate_hook(self, story_text):
        text = story_text.lower()

        if "magic" in text or "mystical" in text:
            return "What if something magical changed your life forever?"

        elif "battle" in text or "fight" in text:
            return "This moment changed everything..."

        elif "mystery" in text or "unknown" in text:
            return "Nobody saw this coming..."

        elif "decision" in text:
            return "One decision can change everything..."

        else:
            return "What happened next will surprise you..."