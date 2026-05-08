import re
import random

def extract_characters(script_text):

    # Simple detection of capitalized names
    names = re.findall(r"\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)?\b", script_text)

    unique_names = list(set(names))

    # Remove common false positives
    blacklist = ["The", "A", "In", "On", "At"]

    characters = [n for n in unique_names if n not in blacklist]

    return characters


def generate_character_profiles(characters):

    profiles = {}

    style_pool = [
        "cinematic fantasy character",
        "historical warrior",
        "African folklore hero",
        "biblical era character",
        "ancient kingdom ruler"
    ]

    for c in characters:

        style = random.choice(style_pool)

        profiles[c] = f"{c}, detailed {style}, dramatic lighting, ultra cinematic"

    return profiles