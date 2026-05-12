import os
import random
import time
import pyttsx3
from pathlib import Path
import json
from config.settings import *
from config.topics import TOPICS
from config.run_config import *

from moviepy.editor import (
    ImageClip,
    concatenate_videoclips,
    AudioFileClip,
    CompositeAudioClip,
    CompositeVideoClip
)

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import moviepy.video.fx.all as vfx

from engine.generate_image import generate_image
from engine.music_generator import generate_music
from intelligence.story_engine import StoryEngine
from intelligence.broll_engine import BrollEngine
from intelligence.shot_director import ShotDirector
from intelligence.character_engine import CharacterEngine
from intelligence.hook_engine import HookEngine


# ---------------------------------
# RUONEX PROJECT SYSTEM
# ---------------------------------

PROJECT_ID = os.environ.get(
    "PROJECT_ID",
    "african_wisdom_story"
)

RUONEX_ROOT = Path(
    r"C:\Users\14439\OneDrive\Desktop\AI-Tools\RuoNex_AI"
)

PROJECT_DIR = RUONEX_ROOT / "projects" / PROJECT_ID

PROJECT_FILE = PROJECT_DIR / "project.json"

IMAGE_FOLDER = PROJECT_DIR / "images"
AUDIO_FOLDER = PROJECT_DIR / "audio"
VIDEO_FOLDER = PROJECT_DIR / "videos"
EXPORT_FOLDER = PROJECT_DIR / "exports"
STORY_FOLDER = PROJECT_DIR / "story"

STORY_FILE = STORY_FOLDER / "script.txt"

IMAGE_FOLDER.mkdir(parents=True, exist_ok=True)
AUDIO_FOLDER.mkdir(parents=True, exist_ok=True)
VIDEO_FOLDER.mkdir(parents=True, exist_ok=True)
EXPORT_FOLDER.mkdir(parents=True, exist_ok=True)
STORY_FOLDER.mkdir(parents=True, exist_ok=True)

print(f"[RUONEX] Using project: {PROJECT_ID}")
print(f"[RUONEX] Project directory: {PROJECT_DIR}")


# ---------------------------------
# PROJECT JSON HELPERS (MOVED UP)
# ---------------------------------

def load_project_json():
    if not PROJECT_FILE.exists():
        print("[RUONEX] project.json not found")
        return {}

    with open(PROJECT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_satb_stems():
    project_data = load_project_json()

    stems = (
        project_data
        .get("audio_assets", {})
        .get("stems", {})
    )

    required = ["soprano", "alto", "tenor", "bass"]

    detected = {}

    for part in required:
        rel_path = stems.get(part, "")

        if not rel_path:
            continue

        stem_path = PROJECT_DIR / rel_path

        if stem_path.exists():
            detected[part] = stem_path

    if len(detected) == 4:
        print("[RUONEX] SATB stems detected")

        for part, path in detected.items():
            print(f"[RUONEX] {part}: {path}")

    else:
        print("[RUONEX] SATB stems not fully available")

    return detected

def get_satb_intensity_from_shots(shot_data_list):
    intensity_map = {
        "joy": 1.25,
        "happy": 1.20,
        "love": 1.15,
        "sad": 0.85,
        "fear": 0.80,
        "lonely": 0.75,
        "action": 1.30,
        "intense": 1.35,
        "dramatic": 1.40,
        "peaceful": 0.90,
        "reflective": 0.95,
        "neutral": 1.00,
    }

    if not shot_data_list:
        return 1.0

    values = []

    for shot in shot_data_list:
        emotion = str(shot.get("emotion", "neutral")).lower()
        mood = str(shot.get("mood", "neutral")).lower()

        intensity = intensity_map.get(emotion)

        if intensity is None:
            intensity = 1.0

            for key, value in intensity_map.items():
                if key in mood:
                    intensity = value
                    break

        values.append(intensity)

    return sum(values) / len(values)

def update_project_json(final_video_path):
    if not PROJECT_FILE.exists():
        return

    with open(PROJECT_FILE, "r", encoding="utf-8") as f:
        project_data = json.load(f)

    project_data["story"]["topic"] = topic
    project_data["story"]["script_path"] = "story/script.txt"

    project_data["audio_assets"]["narration"] = "audio/narration.wav"

    project_data["video_assets"]["images_dir"] = "images/"
    project_data["video_assets"]["raw_video_dir"] = "videos/raw/"
    project_data["video_assets"]["final_video"] = (
        f"exports/{Path(final_video_path).name}"
    )

    project_data["settings"]["captions"] = ENABLE_CAPTIONS
    project_data["settings"]["mode"] = UI_MODE

    with open(PROJECT_FILE, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=2)


# ---------------------------------
# UTILS
# ---------------------------------

def progress(percent, message):
    print(f"[PROGRESS] {percent} | {message}", flush=True)


def add_motion_effect(clip, motion_type="zoom_in", duration=3):
    if motion_type == "zoom_in":
        clip = clip.resize(lambda t: 1.00 + 0.12 * (t / duration))

    elif motion_type == "zoom_out":
        clip = clip.resize(lambda t: 1.12 - 0.12 * (t / duration))

    elif motion_type == "pan_left":
        clip = clip.resize(1.20).set_position(
            lambda t: (-120 * (t / duration), "center")
        )

    elif motion_type == "pan_right":
        clip = clip.resize(1.20).set_position(
            lambda t: (-120 + 120 * (t / duration), "center")
        )

    elif motion_type == "slow_pan":
        clip = clip.resize(1.10).set_position(
            lambda t: (-40 * (t / duration), "center")
        )

    elif motion_type == "drift":
        clip = clip.resize(lambda t: 1.03 + 0.05 * (t / duration)).set_position(
            lambda t: (-20 + 40 * (t / duration), -10)
        )

    else:
        clip = clip.resize(lambda t: 1.00 + 0.06 * (t / duration))

    return clip


def choose_motion_from_mood(mood, motion_choices):
    mood = mood.lower()

    if "tense" in mood or "intense" in mood:
        return random.choice(["pan_left", "pan_right", "drift"])

    if "peaceful" in mood or "reflective" in mood:
        return random.choice(["zoom_in", "slow_pan"])

    if "sad" in mood or "emotional" in mood:
        return "zoom_in"

    return random.choice(motion_choices)


# ---------------------------------
# START PIPELINE
# ---------------------------------

progress(5, "Starting CineForge pipeline")

# -----------------------------
# LOAD TOPIC
# -----------------------------
ui_topic = os.environ.get("UI_TOPIC", "").strip()

if ui_topic:
    topic = ui_topic
else:
    topic = CUSTOM_TOPIC

user_prompt = f"""
Write a short emotional story about {topic}.

Do NOT mention instructions.
Do NOT repeat this prompt.
Do NOT say "write a script".

Tell a real story with a character, conflict, and resolution.

Start with a strong hook.
End with a powerful message.
Keep it under 60 seconds.
"""

print(f"Selected topic: {topic}")

# -----------------------------
# GENERATE STORY
# -----------------------------
progress(10, "Generating story")

story_engine = StoryEngine()
story = story_engine.expand_prompt(user_prompt)

hook_engine = HookEngine()
hook_text = hook_engine.generate_hook(story)

print("\nGenerated Story:\n")
print(story)
print("Hook:", hook_text)

# -----------------------------
# SPLIT INTO SCENES
# -----------------------------
progress(20, "Splitting story into scenes")

raw_sentences = story.replace("\n", " ").split(".")
sentences = [s.strip() for s in raw_sentences if s.strip()]

scenes = []
buffer = ""

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
# CHARACTER CONSISTENCY
# -----------------------------
progress(25, "Analyzing character identity")

character_engine = CharacterEngine()
character_engine.extract_characters(story)

# -----------------------------
# AUDIO: HOOK + STORY
# -----------------------------
progress(30, "Creating voice narration")

engine = pyttsx3.init()

audio_path = os.path.join(AUDIO_FOLDER, "narration.wav")
narration_text = hook_text + " " + " ".join(scenes)

if os.path.exists(audio_path):
    os.remove(audio_path)

engine.save_to_file(narration_text, audio_path)
engine.runAndWait()

print("Local voice narration created")

# -----------------------------
# GENERATE IMAGES
# -----------------------------
progress(40, "Generating cinematic images")

director = ShotDirector()
broll_engine = BrollEngine()

image_paths = []
shot_data_list = []

total_expected_shots = len(scenes) * SHOTS_PER_SCENE
completed_shots = 0

for i, scene in enumerate(scenes):
    shot_sequence = director.generate_shot_sequence(scene, i, len(scenes))

    for j, shot_data in enumerate(shot_sequence):
        base_prompt = director.build_prompt(scene, shot_data)
        prompt = character_engine.enhance_prompt(scene, base_prompt)

        prompt_words = prompt.split()

        if len(prompt_words) > PROMPT_MAX_WORDS:
            prompt = " ".join(prompt_words[:PROMPT_MAX_WORDS])

        if ENABLE_BROLL and j == 0 and broll_engine.should_add_broll(scene):
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
                width=IMAGE_WIDTH,
                height=IMAGE_HEIGHT
            )

        image_paths.append(image_file)
        shot_data_list.append(shot_data)

        completed_shots += 1
        image_progress = 40 + int((completed_shots / max(total_expected_shots, 1)) * 20)
        progress(image_progress, f"Generated image {i + 1}-{j + 1}")

print("Scene images generated")

# -----------------------------
# VIDEO BUILD
# -----------------------------
progress(65, "Building video timeline")

clips = []

audio = AudioFileClip(audio_path)
total_audio_duration = audio.duration

scene_count = len(scenes)
shots_per_scene = SHOTS_PER_SCENE

scene_duration = max(MIN_SCENE_DURATION, total_audio_duration / scene_count)
shot_duration = scene_duration / shots_per_scene

print(f"Audio duration: {total_audio_duration:.2f} seconds")

motion_choices = ["zoom_in", "zoom_out", "pan_left", "pan_right", "drift"]

for i, img in enumerate(image_paths):
    shot_data = shot_data_list[i]

    clip = ImageClip(img).set_duration(shot_duration)

    if ENABLE_MOTION:
        mood = shot_data.get("mood", "")
        motion = choose_motion_from_mood(mood, motion_choices)
        clip = add_motion_effect(clip, motion, shot_duration)

    emotion = shot_data.get("emotion", "neutral")

    if emotion == "fear":
        clip = clip.fx(vfx.colorx, 0.75)
    elif emotion == "sad":
        clip = clip.fx(vfx.colorx, 0.85)
    elif emotion == "joy":
        clip = clip.fx(vfx.colorx, 1.15)
    elif emotion == "action":
        clip = clip.fx(vfx.lum_contrast, lum=0, contrast=25, contrast_thr=127)

    if i > 0 and emotion in ["sad", "fear"]:
        clip = clip.crossfadein(0.4)

    clip = (
        clip
        .fx(vfx.fadein, FADE_DURATION)
        .fx(vfx.fadeout, FADE_DURATION)
        .crossfadein(0.15)
    )

    w, h = clip.size
    w = w if w % 2 == 0 else w - 1
    h = h if h % 2 == 0 else h - 1
    clip = clip.resize((w, h))

    clips.append(clip)

video = concatenate_videoclips(
    clips,
    method="compose",
    padding=-0.15
)

video = video.resize((OUTPUT_WIDTH, OUTPUT_HEIGHT))

# -----------------------------
# HOOK OVERLAY FUNCTION
# -----------------------------
def create_hook_text(text):
    img = Image.new("RGBA", (OUTPUT_WIDTH, OUTPUT_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 80)
    except:
        font = ImageFont.load_default()

    words = text.upper().split()
    mid = len(words) // 2

    line1 = " ".join(words[:mid])
    line2 = " ".join(words[mid:])

    draw.text(
        (int(OUTPUT_WIDTH * 0.08), int(OUTPUT_HEIGHT * 0.35)),
        line1,
        font=font,
        fill="yellow",
        stroke_width=4,
        stroke_fill="black"
    )

    draw.text(
        (int(OUTPUT_WIDTH * 0.08), int(OUTPUT_HEIGHT * 0.48)),
        line2,
        font=font,
        fill="white",
        stroke_width=4,
        stroke_fill="black"
    )

    return np.array(img)

satb_stems = detect_satb_stems()

# -----------------------------
# HOOK + CAPTIONS
# -----------------------------
progress(75, "Adding hook overlay and captions")

if ENABLE_HOOK:
    hook_img = create_hook_text(hook_text)

    hook_clip = (
        ImageClip(hook_img)
        .set_start(0)
        .set_duration(2.0)
        .set_position(("center", "center"))
    )

    video = CompositeVideoClip([video, hook_clip])

    print("Hook overlay added")

if ENABLE_CAPTIONS and CAPTION_MODE == "FAST":

    def create_caption(text):
        img = Image.new("RGBA", (OUTPUT_WIDTH, 200), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 70)
        except:
            font = ImageFont.load_default()

        draw.text(
            (50, 70),
            text,
            font=font,
            fill="yellow",
            stroke_width=3,
            stroke_fill="black"
        )

        return np.array(img)

    words = narration_text.split()

    groups = [
        " ".join(words[i:i + CAPTION_GROUP_SIZE])
        for i in range(0, len(words), CAPTION_GROUP_SIZE)
    ]

    group_duration = video.duration / len(groups)

    caption_clips = []

    for i, text in enumerate(groups):
        start_time = i * group_duration
        img = create_caption(text)

        txt_clip = (
            ImageClip(img)
            .set_start(start_time)
            .set_duration(group_duration)
            .set_position(("center", OUTPUT_HEIGHT * 0.75))
        )

        txt_clip = txt_clip.resize(lambda t: 1 + 0.05 * (t / group_duration))

        caption_clips.append(txt_clip)

    video = CompositeVideoClip([video] + caption_clips)

    print("Viral captions added")

elif ENABLE_CAPTIONS and CAPTION_MODE == "WHISPER":
    print("Whisper captions not yet implemented")

# -----------------------------
# SATB SOUNDTRACK LAYER
# -----------------------------
satb_audio_clips = []
satb_intensity = get_satb_intensity_from_shots(shot_data_list)
project_data = load_project_json()

use_satb = (
    project_data
    .get("settings", {})
    .get("use_satb_as_soundtrack", False)
)

if use_satb and satb_stems:

    print("[RUONEX] Loading SATB soundtrack")

    satb_config = project_data.get("satb_soundtrack", {})

    satb_volume = satb_config.get("volume", 0.035)
    satb_ducking_volume = satb_config.get("ducking_volume", 0.018)
    satb_fade_in = satb_config.get("fade_in", 2.0)
    satb_fade_out = satb_config.get("fade_out", 2.0)

    for part, path in satb_stems.items():

        try:
            choir_clip = (
                AudioFileClip(str(path))
                .volumex(satb_ducking_volume * satb_intensity)
                .audio_fadein(satb_fade_in)
                .audio_fadeout(satb_fade_out)
            )

            satb_audio_clips.append(choir_clip)

            print(f"[RUONEX] Loaded {part} soundtrack")

        except Exception as e:
            print(f"[RUONEX] Failed loading {part}: {e}")
            

# -----------------------------
# MUSIC
# -----------------------------
progress(85, "Adding music and sound effects")

music_clips = []

if ENABLE_MUSIC:
    for i, scene in enumerate(scenes):
        emotion = director.detect_emotion(scene, i, len(scenes))

        music_path = generate_music(
            emotion=emotion,
            duration=scene_duration + 1
        )

        music_clip = AudioFileClip(music_path).volumex(0.08)
        music_clip = music_clip.set_start(i * scene_duration)

        music_clips.append(music_clip)

    print("Scene-based music generated")
else:
    print("Music disabled")

# -----------------------------
# SOUND EFFECTS
# -----------------------------
sfx_clips = []

if ENABLE_SFX:
    whoosh_path = os.path.join("assets", "sfx", "whoosh.mp3")
    hit_path = os.path.join("assets", "sfx", "hit.mp3")

    if os.path.exists(whoosh_path):
        print("Whoosh SFX loaded")
        whoosh = AudioFileClip(whoosh_path).volumex(0.4).set_start(0)
        sfx_clips.append(whoosh)

    if os.path.exists(hit_path):
        print("Hit SFX loaded")
        hit = AudioFileClip(hit_path).volumex(0.4).set_start(1.5)
        sfx_clips.append(hit)

    print(f"Total SFX: {len(sfx_clips)}")
else:
    print("SFX disabled")

# -----------------------------
# FINAL AUDIO MIX
# -----------------------------
final_audio = CompositeAudioClip(
    [audio.set_start(0.2)]
    + satb_audio_clips
    + music_clips
    + sfx_clips
)
video = video.set_audio(final_audio)

# -----------------------------
# EXPORT
# -----------------------------
progress(95, "Exporting final video")

output_file = EXPORT_FOLDER / (
    f"{topic.replace(' ', '_')}_{int(time.time())}.mp4"
)

video.write_videofile(
    str(output_file),
    fps=FPS,
    codec="h264_nvenc",
    audio_codec="aac",
    temp_audiofile="temp-audio.m4a",
    remove_temp=True,
    preset="fast",
    ffmpeg_params=[
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart"
    ]
)

print("Using codec:", "h264_nvenc")

update_project_json(output_file)
print("[RUONEX] project.json updated")

progress(100, "Video generation complete")








