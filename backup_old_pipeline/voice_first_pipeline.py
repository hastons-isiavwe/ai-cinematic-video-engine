import os
import requests
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip

from scripts.cinematic_orchestrator import CinematicOrchestrator
from scripts.generate_image import generate_image
from scripts.cinematic_motion import create_motion_clip
from scripts.character_engine import extract_characters, generate_character_profiles

from scripts.audio_scene_splitter import split_story_into_scene_audio_payloads
from scripts.scene_audio_generator import generate_scene_audio
from scripts.pipeline_governor import PipelineGovernor
from scripts.cinematic_timing_core import CinematicTimingCore
from scripts.sync_validator import SceneAudioSyncValidator


# -----------------------------
# PROJECT FOLDERS
# -----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STORIES_DIR = os.path.join(BASE_DIR, "scripts")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
IMAGE_DIR = os.path.join(OUTPUT_DIR, "images")
VIDEO_DIR = os.path.join(OUTPUT_DIR, "videos")

os.makedirs(IMAGE_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)


# -----------------------------
# EXPORT QUALITY MENU
# -----------------------------

print("\nSelect Export Quality\n")
print("1 = TikTok / Shorts (1080x1920)")
print("2 = YouTube HD (1920x1080)")
print("3 = Cinema 4K (3840x2160)")

choice = input("\nEnter option: ")

if choice == "1":
    WIDTH, HEIGHT = 1080, 1920
elif choice == "2":
    WIDTH, HEIGHT = 1920, 1080
elif choice == "3":
    WIDTH, HEIGHT = 3840, 2160
else:
    WIDTH, HEIGHT = 1280, 720

print(f"\nRendering at {WIDTH}x{HEIGHT}\n")


# -----------------------------
# LOAD STORY
# -----------------------------

all_scripts = [
    os.path.join(STORIES_DIR, f)
    for f in os.listdir(STORIES_DIR)
    if f.endswith(".txt")
]

if not all_scripts:
    raise Exception("No story scripts found in scripts folder.")

script_file = all_scripts[0]

with open(script_file, "r", encoding="utf-8") as f:
    story_text = f.read()

print(f"Loaded story: {script_file}")


# -----------------------------
# CINEMATIC TIMELINE
# -----------------------------

orchestrator = CinematicOrchestrator()
timeline = orchestrator.build(story_text)

if not timeline:
    raise Exception("Timeline generation failed.")

print(f"{len(timeline)} timeline segments created")


# -----------------------------
# PIPELINE GOVERNOR (CLEANUP LAYER)
# -----------------------------

governor = PipelineGovernor()
governor.validate_timeline(timeline)
timeline = governor.sanitize(timeline)


# -----------------------------
# CHARACTER ENGINE
# -----------------------------

try:
    characters = extract_characters(story_text)
    character_profiles = generate_character_profiles(characters)
except Exception:
    character_profiles = {}

print("\nDetected Characters:")
for name, profile in character_profiles.items():
    print(f"{name} → {profile}")


# -----------------------------
# IMAGE GENERATION
# -----------------------------

image_assets = []

for item in timeline:

    prompt = item["text"]

    # cinematic enhancement
    prompt = f"{item.get('camera','')}, {item.get('lighting','')}, {prompt}"

    # character consistency
    for name, profile in character_profiles.items():
        if name.lower() in item["text"].lower():
            prompt = f"{profile}, {prompt}"

    output_image = os.path.join(
        IMAGE_DIR,
        f"{item['type']}_{item['id']}.png"
    )

    print(f"Generating {item['type']} {item['id']}")

    generate_image(
        prompt,
        output_image,
        width=WIDTH,
        height=HEIGHT
    )

    image_assets.append({
        "path": output_image,
        "duration": max(2, item.get("duration", 6)),
        "id": str(item["id"])
    })


# -----------------------------
# AUDIO GENERATION (SCENE-BASED + FALLBACK)
# -----------------------------

ELEVENLABS_API_KEY = "YOUR_API_KEY"
VOICE_ID = "YOUR_VOICE_ID"

audio_units = split_story_into_scene_audio_payloads(timeline)

audio_map = generate_scene_audio(
    audio_units,
    ELEVENLABS_API_KEY,
    VOICE_ID,
    os.path.join(OUTPUT_DIR, "audio")
)

# fallback full narration
voice_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

response = requests.post(
    voice_url,
    headers={
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    },
    json={
        "text": story_text,
        "voice_settings": {
            "stability": 0.75,
            "similarity_boost": 0.75
        }
    }
)

if response.status_code != 200:
    raise Exception(f"TTS failed: {response.text}")

audio_file = os.path.join(OUTPUT_DIR, "voice.mp3")

with open(audio_file, "wb") as f:
    f.write(response.content)

print("Voice narration generated")


# -----------------------------
# SYNC VALIDATION (IMPORTANT FIX)
# -----------------------------

timing_core = CinematicTimingCore()

timeline = timing_core.build_master_clock(
    timeline,
    audio_map
)


# -----------------------------
# VIDEO CREATION
# -----------------------------

video_clips = []

for item in image_assets:

    scene = next(
    s for s in timeline
    if str(s["id"]) == item["id"]
)

clip = create_motion_clip(
    item["path"],
    duration=scene["duration"]
)

    scene_audio = next(
        (a["audio_path"] for a in audio_map
         if str(a["scene_id"]) == item["id"]),
        None
    )

    if scene_audio:
        clip = clip.set_audio(AudioFileClip(scene_audio))

    video_clips.append(clip)


# -----------------------------
# FINAL COMBINE
# -----------------------------

video = concatenate_videoclips(video_clips, method="compose")


# APPLY FALLBACK ONLY IF NO SCENE AUDIO EXISTS
if not any("audio_path" in a for a in audio_map):
    audio = AudioFileClip(audio_file)
    video = video.set_audio(audio)


# -----------------------------
# EXPORT
# -----------------------------

output_video = os.path.join(VIDEO_DIR, "final_story_video.mp4")

video.write_videofile(
    output_video,
    fps=24,
    codec="libx264"
)

print("\nFINAL VIDEO GENERATED")
print(output_video)