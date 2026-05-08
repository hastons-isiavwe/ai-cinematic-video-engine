import os

def load_script_from_file(folder="scripts"):

    scripts = [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.endswith(".txt")
    ]

    if not scripts:
        raise Exception("No script files found.")

    script_file = scripts[0]

    with open(script_file, "r") as f:
        text = f.read()

    return text


def generate_story_prompt(topic, genre, scenes):

    prompt = f"""
Write a cinematic story.

Topic: {topic}
Genre: {genre}

Break the story into {scenes} scenes.
Each scene must be vivid and visual.
"""

    return prompt