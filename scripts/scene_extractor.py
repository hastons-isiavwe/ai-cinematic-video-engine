import re

def split_into_scenes(text, max_scenes=10):
    """
    Automatically split story text into scenes.
    """

    # Split by paragraph
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    scenes = []

    current_scene = ""

    for paragraph in paragraphs:

        if len(current_scene) < 250:
            current_scene += " " + paragraph
        else:
            scenes.append(current_scene.strip())
            current_scene = paragraph

    if current_scene:
        scenes.append(current_scene.strip())

    return scenes[:max_scenes]