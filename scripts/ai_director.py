# ai_director.py

import random

camera_styles = [
"cinematic wide shot",
"dramatic low angle shot",
"epic establishing shot",
"close emotional portrait",
"over the shoulder shot",
"heroic low angle cinematic shot"
]

lighting_styles = [
"dramatic cinematic lighting",
"golden sunset lighting",
"dark moody lighting",
"volumetric god rays",
"soft cinematic glow",
"mysterious fog lighting"
]

film_styles = [
"ultra detailed",
"cinematic color grading",
"film still",
"8k resolution",
"unreal engine cinematic render",
"epic fantasy movie scene"
]

def direct_scene(scene_text):

```
camera = random.choice(camera_styles)
lighting = random.choice(lighting_styles)
style = random.choice(film_styles)

prompt = f"""
```

{camera},
{scene_text},
{lighting},
{style}
"""

```
return prompt.strip()
```
