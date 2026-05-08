class StoryEngine:

    def __init__(self):
        pass

    def expand_prompt(self, prompt):
        prompt = prompt.strip()

        story = f"""
{prompt}

The scene begins in a visually rich environment, filled with detail and atmosphere.

The main character is introduced naturally within this world, interacting with the environment in a way that reveals personality and intention.

A shift occurs. Something changes — tension rises, uncertainty grows, and the emotional tone deepens.

The environment reacts subtly: lighting shifts, silence expands, movement slows or intensifies.

The character now faces a decision, one that pushes the story forward and reveals internal conflict.

The moment builds toward a cinematic peak — visually striking, emotionally charged.

The scene settles into a resolution, leaving a lasting impression and hinting at what comes next.
"""
        return story.strip()