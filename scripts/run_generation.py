from prompt_engine import build_prompt
import subprocess

topic = "tortoise tricking a crocodile at a jungle river"

prompt = build_prompt(topic)

subprocess.run([
    "python",
    "scripts/generate_image.py",
    "--prompt",
    prompt,
    "--output",
    "scene1.png"
])

