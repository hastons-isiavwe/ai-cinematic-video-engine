import os
import pyttsx3
from config.settings import *
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeAudioClip
import moviepy.video.fx.all as vfx

from engine.generate_image import generate_image
from intelligence.story_engine import StoryEngine
from intelligence.broll_engine import BrollEngine
from intelligence.shot_director import ShotDirector
from intelligence.character_engine import CharacterEngine
from engine.music_generator import generate_music

# -----------------------------
# FAST TEST MODE
# -----------------------------

FAST_MODE = True  # True = fastest testing, False = final-quality render

if FAST_MODE:
    MAX_TEST_SCENES = 1
    TEST_WIDTH = 512
    TEST_HEIGHT = 512
else:
    MAX_TEST_SCENES = MAX_SCENES
    TEST_WIDTH = IMAGE_WIDTH
    TEST_HEIGHT = IMAGE_HEIGHT

# -----------------------------
# Project folders
# -----------------------------

STORY_FILE = "stories/story1.txt"
IMAGE_FOLDER = "images"
AUDIO_FOLDER = "audio"
VIDEO_FOLDER = "videos"
MUSIC_FOLDER = "assets/music"

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)
os.makedirs(MUSIC_FOLDER, exist_ok=True)

# -----------------------------
# 1️⃣ Load Story Prompt
# -----------------------------

with open(STORY_FILE, "r", encoding="utf-8") as f:
    user_prompt = f.read().strip()

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

if MAX_TEST_SCENES:
    scenes = scenes[:MAX_TEST_SCENES]

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
    shot_sequence = director.generate_shot_sequence(scene, i)

    for j, shot_data in enumerate(shot_sequence):
        shot_data_list.append(shot_data)

        base_prompt = director.build_prompt(scene, shot_data)
        prompt = character_engine.enhance_prompt(scene, base_prompt)

        # B-roll (only for first shot)
        if j == 0 and broll_engine.should_add_broll(scene):
            print(f"Adding B-roll for scene {i + 1}")
            prompt = broll_engine.generate_broll_prompt(scene)

        print(f"\n--- SCENE {i + 1} SHOT {j + 1} ---\n{prompt}\n")

        image_file = os.path.join(
            IMAGE_FOLDER,
            f"scene_{i + 1:02d}_shot_{j + 1}.png"
        )

        should_regenerate = FORCE_REGENERATE_IMAGES or not os.path.exists(image_file)

        if not should_regenerate:
            print(f"Using cached image {i + 1}-{j + 1}")
        else:
            print(f"Generating image {i + 1}-{j + 1}")

            generate_image(
                prompt=prompt,
                output_path=image_file,
                width=TEST_WIDTH,
                height=TEST_HEIGHT
            )

        image_paths.append(image_file)

print("Scene images generated")

# -----------------------------
# 5️⃣ Convert images to video clips
# -----------------------------

clips = []

audio = AudioFileClip(audio_path)
total_audio_duration = audio.duration

scene_count = len(scenes)
shots_per_scene = 3

scene_duration = max(4.0, total_audio_duration / scene_count)
shot_duration = scene_duration / shots_per_scene

print(f"Audio duration: {total_audio_duration:.2f} seconds")
print(f"Each scene duration: {scene_duration:.2f} seconds")
print(f"Each shot duration: {shot_duration:.2f} seconds")

for i, img in enumerate(image_paths):
    shot_data = shot_data_list[i]

    clip = ImageClip(img).set_duration(shot_duration)

    motion = shot_data.get("motion", "static")

    if motion == "zoom_in":
        clip = clip.resize(lambda t: 1 + 0.03 * (t / shot_duration))

    elif motion == "zoom_out":
        clip = clip.resize(lambda t: 1.03 - 0.03 * (t / shot_duration))

    elif motion == "pan_left":
        clip = clip.resize(1.08).set_position(
            lambda t: (-40 * (t / shot_duration), "center")
        )

    elif motion == "pan_right":
        clip = clip.resize(1.08).set_position(
            lambda t: (-40 + 40 * (t / shot_duration), "center")
        )

    emotion = shot_data.get("emotion", "neutral")

    if emotion == "fear":
        clip = clip.fx(vfx.colorx, 0.75)

    elif emotion == "sad":
        clip = clip.fx(vfx.colorx, 0.85)

    elif emotion == "joy":
        clip = clip.fx(vfx.colorx, 1.15)

    elif emotion == "action":
        clip = clip.fx(vfx.lum_contrast, lum=0, contrast=25, contrast_thr=127)

    if i > 0:
        if emotion == "action":
            pass
        elif emotion in ["sad", "fear"]:
            clip = clip.crossfadein(0.4)

    clip = clip.fx(vfx.fadein, FADE_DURATION).fx(vfx.fadeout, FADE_DURATION)

    w, h = clip.size
    w = w if w % 2 == 0 else w - 1
    h = h if h % 2 == 0 else h - 1
    clip = clip.resize((w, h))

    clips.append(clip)

video = concatenate_videoclips(clips, method="compose")

# -----------------------------
# 6️⃣ Add narration + optional background music
# -----------------------------

# -----------------------------
# 🎧 Generated Emotion-Based Music
# -----------------------------

from engine.music_generator import generate_music

first_emotion = shot_data_list[0].get("emotion", "neutral")

music_path = generate_music(
    emotion=first_emotion,
    duration=video.duration + 1
)

print(f"Generated music for emotion: {first_emotion}")

music = AudioFileClip(music_path).volumex(0.1)

final_audio = CompositeAudioClip([
    audio.set_start(0.2),
    music.set_duration(video.duration)
])

video = video.set_audio(final_audio)

# -----------------------------
# 7️⃣ Export final video
# -----------------------------

output_file = os.path.join(VIDEO_FOLDER, "story_video.mp4")

video.write_videofile(
    output_file,
    fps=24,
    codec="libx264",
    audio_codec="aac",
    temp_audiofile="temp-audio.m4a",
    remove_temp=True,
    ffmpeg_params=[
        "-pix_fmt", "yuv420p",
        "-profile:v", "baseline",
        "-level", "3.0",
        "-movflags", "+faststart"
    ]
)

print("Final video created:", output_file)













