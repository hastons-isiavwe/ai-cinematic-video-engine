# -----------------------------
# RUNTIME CONFIGURATION
# -----------------------------

PROJECT_NAME = "AI Cinematic Video Engine"

# Story controls
USE_RANDOM_TOPIC = True
CUSTOM_TOPIC = "African folktales"

MAX_SCENES = 3
SHOTS_PER_SCENE = 3
MAX_WORDS_PER_SCENE = 18

# Video controls
OUTPUT_WIDTH = 1280
OUTPUT_HEIGHT = 720
IMAGE_WIDTH = 1280
IMAGE_HEIGHT = 720
FPS = 30

# Rendering controls
FORCE_REGENERATE_IMAGES = False
MIN_SCENE_DURATION = 4
FADE_DURATION = 0.4

# Feature toggles
ENABLE_HOOK = True
ENABLE_CAPTIONS = True
ENABLE_MUSIC = True
ENABLE_SFX = True
ENABLE_BROLL = True
ENABLE_MOTION = True

# Caption controls
CAPTION_MODE = "FAST"
CAPTION_GROUP_SIZE = 3

# Style controls
VIDEO_STYLE = "cinematic"
PROMPT_MAX_WORDS = 55

# Output folders
IMAGE_FOLDER = "images"
AUDIO_FOLDER = "audio"
VIDEO_FOLDER = "videos"
STORY_FILE = "stories/story1.txt"