# config/settings.py

# -----------------------------
# MODE CONTROL
# -----------------------------

MODE = "DEV"   # DEV | TEST | FINAL

# -----------------------------
# RENDER SETTINGS
# -----------------------------

if MODE == "DEV":
    MAX_SCENES = 1
    IMAGE_WIDTH = 512
    IMAGE_HEIGHT = 512
    FPS = 24
    FADE_DURATION = 0.4
    FORCE_REGENERATE_IMAGES = False

elif MODE == "TEST":
    MAX_SCENES = 3
    IMAGE_WIDTH = 512
    IMAGE_HEIGHT = 512
    FPS = 24
    FADE_DURATION = 0.5
    FORCE_REGENERATE_IMAGES = False

elif MODE == "FINAL":
    MAX_SCENES = None
    IMAGE_WIDTH = 1280
    IMAGE_HEIGHT = 720
    FPS = 24
    FADE_DURATION = 0.8
    FORCE_REGENERATE_IMAGES = False

# -----------------------------
# GENERATION SETTINGS
# -----------------------------

USE_BROLL = True
USE_COLOR_GRADING = True
USE_MOTION = True