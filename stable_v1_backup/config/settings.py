# config/settings.py

# -----------------------------
# MODE
# -----------------------------

TEST_MODE = True

# -----------------------------
# RENDER SETTINGS
# -----------------------------

if TEST_MODE:
    MAX_SCENES = 2
    IMAGE_WIDTH = 720
    IMAGE_HEIGHT = 480
    FPS = 24
    FADE_DURATION = 0.6
else:
    MAX_SCENES = None
    IMAGE_WIDTH = 1280
    IMAGE_HEIGHT = 720
    FPS = 24
    FADE_DURATION = 0.8

# -----------------------------
# GENERATION SETTINGS
# -----------------------------

USE_BROLL = True
USE_COLOR_GRADING = True
USE_MOTION = True

# -----------------------------
# PERFORMANCE
# -----------------------------

FORCE_REGENERATE_IMAGES = False