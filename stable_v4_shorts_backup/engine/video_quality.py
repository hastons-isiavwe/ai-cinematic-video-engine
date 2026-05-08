QUALITY_PRESETS = {
    "low": (854, 480),
    "medium": (1280, 720),
    "high": (1920, 1080),
    "ultra": (3840, 2160)
}

def get_resolution(level):
    level = level.lower()

    if level not in QUALITY_PRESETS:
        raise ValueError("Quality must be: low, medium, high, ultra")

    return QUALITY_PRESETS[level]