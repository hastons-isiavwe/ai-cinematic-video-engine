# config/settings.py

# -----------------------------
# MODE CONTROL
# -----------------------------

MODE = "DEV"        # DEV | TEST | FINAL
PLATFORM = "SHORTS" # YOUTUBE | SHORTS

# -----------------------------
# BASE MODE SETTINGS
# -----------------------------

if MODE == "DEV":
    MAX_SCENES = 1
    FPS = 24
    FADE_DURATION = 0.4
    FORCE_REGENERATE_IMAGES = False

elif MODE == "TEST":
    MAX_SCENES = 3
    FPS = 24
    FADE_DURATION = 0.5
    FORCE_REGENERATE_IMAGES = False

elif MODE == "FINAL":
    MAX_SCENES = None
    FPS = 24
    FADE_DURATION = 0.8
    FORCE_REGENERATE_IMAGES = True

# -----------------------------
# PLATFORM SETTINGS
# -----------------------------

if PLATFORM == "SHORTS":
    IMAGE_WIDTH = 720
    IMAGE_HEIGHT = 1280
    OUTPUT_WIDTH = 720
    OUTPUT_HEIGHT = 1280
    SHOTS_PER_SCENE = 3
    MIN_SCENE_DURATION = 3.0

elif PLATFORM == "YOUTUBE":
    IMAGE_WIDTH = 1280
    IMAGE_HEIGHT = 720
    OUTPUT_WIDTH = 1280
    OUTPUT_HEIGHT = 720
    SHOTS_PER_SCENE = 3
    MIN_SCENE_DURATION = 4.0

# -----------------------------
# GENERATION SETTINGS
# -----------------------------

USE_BROLL = True
USE_COLOR_GRADING = True
USE_MOTION = True