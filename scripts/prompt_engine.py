import random

styles = [
    "cinematic lighting",
    "highly detailed illustration",
    "3D animated film style",
    "storybook art style",
    "documentary realism",
    "epic movie still"
]

camera = [
    "wide shot",
    "dramatic close up",
    "overhead cinematic view",
    "medium shot",
    "low angle hero shot"
]

def build_prompt(topic):
    style = random.choice(styles)
    cam = random.choice(camera)

    prompt = f"{topic}, {style}, {cam}, ultra detailed, 4k resolution, dramatic atmosphere"

    return prompt