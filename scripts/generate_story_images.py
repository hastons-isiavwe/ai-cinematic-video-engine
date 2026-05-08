from prompt_engine import build_prompt
import subprocess
import os

# Default generation settings
DEFAULT_RESOLUTION = "720x720"  # use "1280x720" if you prefer widescreen
OUTPUT_DIR = "outputs"
HIGH_RES_OVERRIDE = None  # set e.g., "2048x2048" if you want high-res for specific images

# Example story scenes
scenes = [
    "clever tortoise walking through the jungle",
    "tortoise meeting crocodile beside a river",
    "crocodile trying to trick the tortoise",
    "tortoise outsmarting the crocodile",
    "tortoise celebrating his clever victory"
]

# Make sure output folder exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

for i, scene in enumerate(scenes, start=1):
    prompt = build_prompt(scene)
    filename = f"scene_{i}.png"

    # Allow easy resolution override
    resolution = HIGH_RES_OVERRIDE or DEFAULT_RESOLUTION

    print(f"\nGenerating {filename}")
    print(f"Prompt: {prompt}")
    print(f"Resolution: {resolution}")

    import sys  # add this at the top if not already imported

subprocess.run([
    sys.executable,  # ensures it uses the venv Python
    "scripts/generate_image.py",
    "--prompt", prompt,
    "--output", filename,
    "--resolution", resolution
])