import os
import random
import time
import pyttsx3
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


STORY_FILE = "stories/story1.txt"
IMAGE_FOLDER = "images"
AUDIO_FOLDER = "audio"
VIDEO_FOLDER = "videos"

os.makedirs(IMAGE_FOLDER, exist_ok=True)
os.makedirs(AUDIO_FOLDER, exist_ok=True)
os.makedirs(VIDEO_FOLDER, exist_ok=True)


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


topic = random.choice(TOPICS)

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

story_engine = StoryEngine()
story = story_engine.expand_prompt(user_prompt)

hook_engine = HookEngine()
hook_text = hook_engine.generate_hook(story)

print("\nGenerated Story:\n")
print(story)
print("Hook:", hook_text)


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


character_engine = CharacterEngine()
character_engine.extract_characters(story)


engine = pyttsx3.init()

audio_path = os.path.join(AUDIO_FOLDER, "narration.wav")
narration_text = hook_text + " " + " ".join(scenes)

if os.path.exists(audio_path):
    os.remove(audio_path)

engine.save_to_file(narration_text, audio_path)
engine.runAndWait()

print("Local voice narration created")


director = ShotDirector()
broll_engine = BrollEngine()

image_paths = []
shot_data_list = []

for i, scene in enumerate(scenes):
    shot_sequence = director.generate_shot_sequence(scene, i, len(scenes))

    for j, shot_data in enumerate(shot_sequence):
        base_prompt = director.build_prompt(scene, shot_data)
        prompt = character_engine.enhance_prompt(scene, base_prompt)

        prompt_words = prompt.split()
        MAX_PROMPT_WORDS = 55

        if len(prompt_words) > MAX_PROMPT_WORDS:
            prompt = " ".join(prompt_words[:MAX_PROMPT_WORDS])

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
                width=IMAGE_WIDTH,
                height=IMAGE_HEIGHT
            )

        image_paths.append(image_file)
        shot_data_list.append(shot_data)

print("Scene images generated")


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


hook_img = create_hook_text(hook_text)

hook_clip = (
    ImageClip(hook_img)
    .set_start(0)
    .set_duration(2.0)
    .set_position(("center", "center"))
)

video = CompositeVideoClip([video, hook_clip])

print("Hook overlay added")


if CAPTION_MODE == "FAST":

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

    group_size = 3
    groups = [
        " ".join(words[i:i + group_size])
        for i in range(0, len(words), group_size)
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

elif CAPTION_MODE == "WHISPER":
    print("Whisper captions not yet implemented")


music_clips = []

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


sfx_clips = []

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


final_audio = CompositeAudioClip(
    [audio.set_start(0.2)] + music_clips + sfx_clips
)

video = video.set_audio(final_audio)


output_file = os.path.join(
    VIDEO_FOLDER,
    f"{topic.replace(' ', '_')}_{int(time.time())}.mp4"
)

video.write_videofile(
    output_file,
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











