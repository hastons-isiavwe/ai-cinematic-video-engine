import os
import pyttsx3
from config.settings import *
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
import moviepy.video.fx.all as vfx
from engine.generate_image import generate_image
from intelligence.story_engine import StoryEngine
from intelligence.broll_engine import BrollEngine
from intelligence.shot_director import ShotDirector
from intelligence.character_engine import CharacterEngine


# -----------------------------
# Project folders
# -----------------------------

STORY_FILE = "stories/story1.txt"
IMAGE_FOLDER = "images"
AUDIO_FOLDER = "audio"
VIDEO_FOLDER = "videos"

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)

# -----------------------------
# Render Mode
# -----------------------------



# -----------------------------
# 1️⃣ Load Story
# -----------------------------

with open(STORY_FILE, "r", encoding="utf-8") as f:
    user_prompt = f.read()

story_engine = StoryEngine()
story = story_engine.expand_prompt(user_prompt)

print("\nGenerated Story:\n")
print(story)

# -----------------------------
# 2️⃣ Split into scenes
# -----------------------------

raw_sentences = story.replace("\n", " ").split(".")
sentences = [s.strip() for s in raw_sentences if s.strip()]

scenes = []
buffer = ""
MAX_WORDS_PER_SCENE = 18

for sentence in sentences:
    buffer += sentence + ". "

    if len(buffer.split()) >= MAX_WORDS_PER_SCENE:
        scenes.append(buffer.strip())
        buffer = ""

if buffer:
    scenes.append(buffer.strip())

print(f"Detected {len(scenes)} scenes")

if MAX_SCENES:
    scenes = scenes[:MAX_SCENES]

print(f"Rendering {len(scenes)} scenes")

# -----------------------------
# Character Engine Setup
# -----------------------------

character_engine = CharacterEngine()
character_engine.extract_characters(scenes)

# -----------------------------
# 3️⃣ Generate single voice narration
# -----------------------------

engine = pyttsx3.init()

audio_path = os.path.join(AUDIO_FOLDER, "narration.wav")
narration_text = " ".join(scenes)

if os.path.exists(audio_path):
    os.remove(audio_path)

engine.save_to_file(narration_text, audio_path)
engine.runAndWait()

print("Local voice narration created")

# -----------------------------
# 4️⃣ Generate scene images
# -----------------------------

director = ShotDirector()
broll_engine = BrollEngine()

image_paths = []
shot_data_list = []

for i, scene in enumerate(scenes):
    shot_data = director.decide_shot(scene, i)
    shot_data_list.append(shot_data)

    base_prompt = director.build_prompt(scene, shot_data)
    prompt = character_engine.enhance_prompt(scene, base_prompt)

    # B-roll override
    if broll_engine.should_add_broll(scene):
        print(f"Adding B-roll for scene {i+1}")
        prompt = broll_engine.generate_broll_prompt(scene)

    # Debug prompt
    print(f"\n--- SCENE {i+1} PROMPT ---\n{prompt}\n")

    image_file = os.path.join(IMAGE_FOLDER, f"scene_{i+1:02d}.png")

    should_regenerate = FORCE_REGENERATE_IMAGES or not os.path.exists(image_file)

    if not should_regenerate:
        print(f"Using cached image {i+1}/{len(scenes)}: {image_file}")
    else:
        print(f"Generating image {i+1}/{len(scenes)}: {image_file}")

        generate_image(
            prompt=prompt,
            output_path=image_file,
            width=IMAGE_WIDTH,
            height=IMAGE_HEIGHT
        )

    image_paths.append(image_file)

print("Scene images generated")
# -----------------------------
# 5️⃣ Convert images to video clips with motion + color grading
# -----------------------------

clips = []

audio = AudioFileClip(audio_path)
total_audio_duration = audio.duration
scene_duration = total_audio_duration / len(image_paths)

print(f"Audio duration: {total_audio_duration:.2f} seconds")
print(f"Each scene duration: {scene_duration:.2f} seconds")

for i, img in enumerate(image_paths):
    clip = ImageClip(img).set_duration(scene_duration)

    motion = shot_data_list[i].get("motion", "static")

    if motion == "zoom_in":
        clip = clip.resize(lambda t: 1 + 0.03 * (t / scene_duration))

    elif motion == "zoom_out":
        clip = clip.resize(lambda t: 1.03 - 0.03 * (t / scene_duration))

    elif motion == "pan_left":
        clip = clip.resize(1.08).set_position(
            lambda t: (-40 * (t / scene_duration), "center")
        )

    elif motion == "pan_right":
        clip = clip.resize(1.08).set_position(
            lambda t: (-40 + 40 * (t / scene_duration), "center")
        )

    emotion = shot_data_list[i].get("emotion", "neutral")

    if emotion == "fear":
        clip = clip.fx(vfx.colorx, 0.75)

    elif emotion == "sad":
        clip = clip.fx(vfx.colorx, 0.85)

    elif emotion == "joy":
        clip = clip.fx(vfx.colorx, 1.15)

    elif emotion == "action":
        clip = clip.fx(vfx.lum_contrast, lum=0, contrast=25, contrast_thr=127)

    clip = clip.fx(vfx.fadein, FADE_DURATION).fx(vfx.fadeout, FADE_DURATION)

    clips.append(clip)

video = concatenate_videoclips(clips, method="compose")

# -----------------------------
# 6️⃣ Add narration
# -----------------------------

video = video.set_audio(audio)

# -----------------------------
# 7️⃣ Export final video
# -----------------------------

output_file = os.path.join(VIDEO_FOLDER, "story_video.mp4")

video.write_videofile(output_file, fps=24)

print("Final video created:", output_file)




