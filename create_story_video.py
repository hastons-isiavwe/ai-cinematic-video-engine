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
# PROJECT JSON HELPERS
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
        "joy": 1.25, "happy": 1.20, "love": 1.15,
        "sad": 0.85, "fear": 0.80, "lonely": 0.75,
        "action": 1.30, "intense": 1.35, "dramatic": 1.40,
        "peaceful": 0.90, "reflective": 0.95,
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


def get_emotional_voice_weights(emotion):
    emotion = str(emotion).lower()

    routing = {
        "joy": {"soprano": 1.4, "alto": 0.8, "tenor": 1.0, "bass": 0.7},
        "happy": {"soprano": 1.3, "alto": 0.9, "tenor": 1.0, "bass": 0.8},
        "love": {"soprano": 1.2, "alto": 1.0, "tenor": 1.3, "bass": 0.8},
        "sad": {"soprano": 0.7, "alto": 1.5, "tenor": 1.0, "bass": 0.9},
        "reflective": {"soprano": 0.9, "alto": 1.3, "tenor": 1.1, "bass": 0.9},
        "fear": {"soprano": 0.6, "alto": 0.8, "tenor": 1.0, "bass": 1.5},
        "dramatic": {"soprano": 0.8, "alto": 1.0, "tenor": 1.1, "bass": 1.6},
        "neutral": {"soprano": 1.0, "alto": 1.0, "tenor": 1.0, "bass": 1.0},
    }

    return routing.get(emotion, routing["neutral"])


def get_story_curve_multiplier(shot_data_list, satb_config):
    if not satb_config.get("curve_enabled", True):
        return 1.0
    if not shot_data_list:
        return 1.0

    curve_start = satb_config.get("curve_start", 0.75)
    curve_mid = satb_config.get("curve_mid", 1.0)
    curve_peak = satb_config.get("curve_peak", 1.35)
    curve_end = satb_config.get("curve_end", 0.85)

    total = len(shot_data_list)
    values = []

    for index, _shot in enumerate(shot_data_list):
        progress = index / max(total - 1, 1)

        if progress < 0.33:
            multiplier = curve_start + ((curve_mid - curve_start) * (progress / 0.33))
        elif progress < 0.75:
            multiplier = curve_mid + ((curve_peak - curve_mid) * ((progress - 0.33) / 0.42))
        else:
            multiplier = curve_peak + ((curve_end - curve_peak) * ((progress - 0.75) / 0.25))

        values.append(multiplier)

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
    project_data["video_assets"]["final_video"] = f"exports/{Path(final_video_path).name}"

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
        clip = clip.resize(1.20).set_position(lambda t: (-120 * (t / duration), "center"))
    elif motion_type == "pan_right":
        clip = clip.resize(1.20).set_position(lambda t: (-120 + 120 * (t / duration), "center"))
    elif motion_type == "slow_pan":
        clip = clip.resize(1.10).set_position(lambda t: (-40 * (t / duration), "center"))
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
# ADAPTIVE SCENE TIMING ENGINE v2 (music-aware / emotion-aware)
# ---------------------------------

class TimingEngine:

    def __init__(self):
        # Base durations (seconds) by narrative phase
        self.base_scene = {
            "intro": 7.0,
            "emotional": 10.0,
            "tense": 5.0,
            "climax": 11.0,
            "resolution": 8.0
        }

        # Emotion → pacing multiplier (higher = longer scenes)
        self.emotion_multiplier = {
            "sad": 1.30,
            "fear": 0.85,
            "joy": 1.10,
            "action": 0.80,
            "reflective": 1.20,
            "peaceful": 1.10,
            "neutral": 1.00
        }

        # Emotion → shot distribution bias
        # Values are relative weights for [shot1, shot2, shot3]
        self.shot_bias = {
            "sad":        [1.2, 1.4, 0.6],   # linger on character
            "reflective": [1.1, 1.3, 0.8],
            "peaceful":   [1.1, 1.2, 0.7],
            "fear":       [0.9, 1.0, 1.3],   # more emphasis on detail / tension
            "action":     [0.8, 1.0, 1.4],
            "joy":        [1.0, 1.2, 0.8],
            "neutral":    [1.0, 1.1, 0.9],
        }

    def classify_scene_phase(self, index, total):
        progress = index / max(total - 1, 1)

        if progress < 0.15:
            return "intro"
        elif progress < 0.55:
            return "emotional"
        elif progress < 0.80:
            return "climax"
        else:
            return "resolution"

    def _scene_emotion(self, scene_index, shots_per_scene, shot_data_list):
        """
        Use the first shot as anchor, but peek at the rest of the scene
        to get a better emotional 'energy' estimate.
        """
        start = scene_index * shots_per_scene
        end = min(start + shots_per_scene, len(shot_data_list))

        if start >= len(shot_data_list):
            return "neutral"

        emotions = []
        for i in range(start, end):
            emotions.append(str(shot_data_list[i].get("emotion", "neutral")).lower())

        if not emotions:
            return "neutral"

        # Simple heuristic: prefer non-neutral if present
        for e in emotions:
            if e != "neutral":
                return e

        return emotions[0]

    def build_timing_profile(self, scenes, shot_data_list, shots_per_scene, total_audio_duration):
        total_scenes = len(scenes)
        profile = []

        # 1) Compute scene weights based on phase + emotion
        scene_weights = []
        total_weight = 0.0

        for i in range(total_scenes):
            phase = self.classify_scene_phase(i, total_scenes)
            emotion = self._scene_emotion(i, shots_per_scene, shot_data_list)

            base = self.base_scene.get(phase, 7.0)
            mult = self.emotion_multiplier.get(emotion, 1.0)

            weight = base * mult
            scene_weights.append((weight, emotion))
            total_weight += weight

        if total_weight <= 0:
            # Fallback: uniform timing
            uniform_scene_duration = total_audio_duration / max(total_scenes, 1)
            for _ in range(total_scenes):
                d = uniform_scene_duration
                profile.append({
                    "scene_duration": d,
                    "shot_durations": [d / 3.0] * 3
                })
            return profile

        # 2) Convert weights → actual scene durations
        for i, (weight, emotion) in enumerate(scene_weights):
            scene_duration = (weight / total_weight) * total_audio_duration

            # 3) Shot distribution inside scene, biased by emotion
            bias = self.shot_bias.get(emotion, self.shot_bias["neutral"])
            b1, b2, b3 = bias
            b_total = b1 + b2 + b3

            shot1 = scene_duration * (b1 / b_total)
            shot2 = scene_duration * (b2 / b_total)
            shot3 = scene_duration * (b3 / b_total)

            profile.append({
                "scene_duration": scene_duration,
                "shot_durations": [shot1, shot2, shot3]
            })

        return profile


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

audio = AudioFileClip(audio_path)
total_audio_duration = audio.duration

scene_count = len(scenes)
shots_per_scene = SHOTS_PER_SCENE

print(f"Audio duration: {total_audio_duration:.2f} seconds")

motion_choices = ["zoom_in", "zoom_out", "pan_left", "pan_right", "drift"]

timing_engine = TimingEngine()
timing_profile = timing_engine.build_timing_profile(
    scenes=scenes,
    shot_data_list=shot_data_list,
    shots_per_scene=shots_per_scene,
    total_audio_duration=total_audio_duration
)

clips = []
current_time = 0.0

for scene_index, scene in enumerate(scenes):
    scene_info = timing_profile[scene_index]
    shot_durations = scene_info["shot_durations"]

    for shot_index in range(shots_per_scene):
        global_shot_index = scene_index * shots_per_scene + shot_index
        if global_shot_index >= len(image_paths):
            break

        img = image_paths[global_shot_index]
        shot_data = shot_data_list[global_shot_index]

        duration = shot_durations[shot_index]

        clip = ImageClip(img).set_duration(duration)

        if ENABLE_MOTION:
            mood = shot_data.get("mood", "")
            motion = choose_motion_from_mood(mood, motion_choices)
            clip = add_motion_effect(clip, motion, duration)

        emotion = shot_data.get("emotion", "neutral")

        if emotion == "fear":
            clip = clip.fx(vfx.colorx, 0.75)
        elif emotion == "sad":
            clip = clip.fx(vfx.colorx, 0.85)
        elif emotion == "joy":
            clip = clip.fx(vfx.colorx, 1.15)
        elif emotion == "action":
            clip = clip.fx(vfx.lum_contrast, lum=0, contrast=25, contrast_thr=127)

        clip = (
            clip
            .fx(vfx.fadein, FADE_DURATION)
            .fx(vfx.fadeout, FADE_DURATION)
        )

        clip = clip.set_start(current_time)
        current_time += duration

        w, h = clip.size
        w = w if w % 2 == 0 else w - 1
        h = h if h % 2 == 0 else h - 1
        clip = clip.resize((w, h))

        clips.append(clip)

video = CompositeVideoClip(clips)
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

    satb_curve_multiplier = get_story_curve_multiplier(
        shot_data_list,
        satb_config
    )

    print(f"[RUONEX] SATB curve multiplier: {satb_curve_multiplier:.2f}")

    dominant_emotion = "neutral"

    if shot_data_list:
        dominant_emotion = str(
            shot_data_list[0].get("emotion", "neutral")
        ).lower()

    voice_weights = get_emotional_voice_weights(dominant_emotion)

    print(f"[RUONEX] Dominant emotion: {dominant_emotion}")

    for part, path in satb_stems.items():

        voice_multiplier = voice_weights.get(part, 1.0)

        try:
            choir_clip = AudioFileClip(str(path))

            choir_volume = (
                satb_ducking_volume
                * satb_intensity
                * satb_curve_multiplier
                * voice_multiplier
            )

            choir_clip = choir_clip.volumex(choir_volume)
            choir_clip = choir_clip.audio_fadein(satb_fade_in)
            choir_clip = choir_clip.audio_fadeout(satb_fade_out)

            satb_audio_clips.append(choir_clip)

            print(
                f"[RUONEX] Loaded {part} soundtrack "
                f"(x{voice_multiplier})"
            )

        except Exception as e:
            print(f"[RUONEX] Failed loading {part}: {e}")

else:
    print("[RUONEX] SATB soundtrack disabled")

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
            duration=timing_profile[i]["scene_duration"] + 1
        )

        music_clip = AudioFileClip(music_path).volumex(0.08)
        music_clip = music_clip.set_start(
            sum(t["scene_duration"] for t in timing_profile[:i])
        )

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




