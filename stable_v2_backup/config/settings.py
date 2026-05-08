# config/settings.py

# -----------------------------
# MODE CONTROL
# -----------------------------

FAST_MODE = True   # 🔥 main switch for speed vs quality

# -----------------------------
# RENDER SETTINGS
# -----------------------------

if FAST_MODE:
    MAX_SCENES = 1          # only 1 scene for speed
    IMAGE_WIDTH = 512       # faster generation
    IMAGE_HEIGHT = 512
    FPS = 24
    FADE_DURATION = 0.4
else:
    MAX_SCENES = None       # full story
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
# PERFORMANCE CONTROL
# -----------------------------

# 🔥 HUGE SPEED BOOST
FORCE_REGENERATE_IMAGES = False if FAST_MODE else True