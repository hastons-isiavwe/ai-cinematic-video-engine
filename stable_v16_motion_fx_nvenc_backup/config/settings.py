# config/settings.py

# -----------------------------
# MODE CONTROL
# -----------------------------

MODE = "TEST"        # DEV | TEST | PROD
PLATFORM = "SHORTS" # YOUTUBE | SHORTS
CAPTION_MODE = "FAST"

# -----------------------------
# MODE SETTINGS
# -----------------------------

if MODE == "DEV":
    MAX_SCENES = 1
    FORCE_REGENERATE_IMAGES = False
    FPS = 24
    FADE_DURATION = 0.3

elif MODE == "TEST":
    MAX_SCENES = 3
    FORCE_REGENERATE_IMAGES = True
    FPS = 24
    FADE_DURATION = 0.3

elif MODE == "PROD":
    MAX_SCENES = None
    FORCE_REGENERATE_IMAGES = True
    FPS = 24
    FADE_DURATION = 0.4

else:
    MAX_SCENES = 1
    FORCE_REGENERATE_IMAGES = False
    FPS = 24
    FADE_DURATION = 0.3

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

# -----------------------------
# VIDEO FX SETTINGS
# -----------------------------

FPS = 24
FADE_DURATION = 0.3










