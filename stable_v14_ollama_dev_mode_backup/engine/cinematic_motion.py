from moviepy.editor import ImageClip
import random

def create_motion_clip(image_path, duration=5):

```
clip = ImageClip(image_path).set_duration(duration)

motion_type = random.choice([
    "zoom_in",
    "zoom_out",
    "pan_left",
    "pan_right"
])

if motion_type == "zoom_in":
    clip = clip.resize(lambda t: 1 + 0.08*t)

elif motion_type == "zoom_out":
    clip = clip.resize(lambda t: 1.08 - 0.08*t)

elif motion_type == "pan_left":
    clip = clip.set_position(lambda t: (-30*t, "center"))

elif motion_type == "pan_right":
    clip = clip.set_position(lambda t: (30*t, "center"))

return clip
```
