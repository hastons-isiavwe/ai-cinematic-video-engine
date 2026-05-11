import os
import sys
import subprocess
import gradio as gr


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(PROJECT_DIR, "videos")
CONFIG_FILE = os.path.join(PROJECT_DIR, "config", "run_config.py")


CUSTOM_CSS = """
body {
    background: radial-gradient(circle at center, #12233f 0%, #070b14 55%, #020409 100%) !important;
}

.gradio-container {
    background: transparent !important;
    color: #f5f7fb !important;
    font-family: Inter, Arial, sans-serif !important;
}

#studio-header {
    background: #05070c;
    padding: 14px 24px;
    border-radius: 0 0 18px 18px;
    border-bottom: 1px solid rgba(0, 255, 255, 0.18);
}

#studio-title {
    font-size: 30px;
    font-weight: 800;
    color: #ffffff;
}

#studio-subtitle {
    color: #9aa7bd;
    font-size: 14px;
}

.panel {
    background: rgba(8, 12, 22, 0.92) !important;
    border: 1px solid rgba(0, 255, 255, 0.12) !important;
    border-radius: 18px !important;
    padding: 18px !important;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.35);
}

.center-panel {
    background: rgba(3, 6, 12, 0.94) !important;
    border: 1px solid rgba(0, 255, 255, 0.16) !important;
    border-radius: 22px !important;
    padding: 18px !important;
}

button.primary {
    background: linear-gradient(135deg, #18e7ff, #22ffc8) !important;
    color: #031016 !important;
    font-weight: 800 !important;
    border-radius: 14px !important;
    border: none !important;
}

textarea, input, select {
    background: #0f1726 !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
}

label {
    color: #cbd5e1 !important;
    font-weight: 600 !important;
}

#timeline-box textarea {
    background: #05070c !important;
    color: #44ffcc !important;
    font-family: Consolas, monospace !important;
}

video {
    border-radius: 18px !important;
    background: #000 !important;
}
"""


def get_latest_video():

    if not os.path.exists(VIDEO_DIR):
        return None

    videos = [
        os.path.join(VIDEO_DIR, f)
        for f in os.listdir(VIDEO_DIR)
        if f.lower().endswith(".mp4")
    ]

    if not videos:
        return None

    return max(videos, key=os.path.getmtime)


def get_mode_settings(mode):

    if mode == "DEV":
        return {
            "max_scenes": 2,
            "shots_per_scene": 2,
            "image_width": 768,
            "image_height": 432,
            "enable_music": False,
            "enable_sfx": False,
            "force_regenerate": False,
        }

    if mode == "TEST":
        return {
            "max_scenes": 3,
            "shots_per_scene": 3,
            "image_width": 1024,
            "image_height": 576,
            "enable_music": True,
            "enable_sfx": False,
            "force_regenerate": False,
        }

    return {
        "max_scenes": 5,
        "shots_per_scene": 5,
        "image_width": 1280,
        "image_height": 720,
        "enable_music": True,
        "enable_sfx": True,
        "force_regenerate": True,
    }


def write_runtime_config(topic, mode, enable_captions):

    settings = get_mode_settings(mode)

    config_text = f'''# -----------------------------
# RUNTIME CONFIGURATION
# -----------------------------

PROJECT_NAME = "AI Cinematic Video Engine"

USE_RANDOM_TOPIC = False
CUSTOM_TOPIC = {topic!r}
UI_MODE = {mode!r}

MAX_SCENES = {settings["max_scenes"]}
SHOTS_PER_SCENE = {settings["shots_per_scene"]}
MAX_WORDS_PER_SCENE = 18

OUTPUT_WIDTH = 1280
OUTPUT_HEIGHT = 720
IMAGE_WIDTH = {settings["image_width"]}
IMAGE_HEIGHT = {settings["image_height"]}
FPS = 30

FORCE_REGENERATE_IMAGES = {settings["force_regenerate"]}
MIN_SCENE_DURATION = 4
FADE_DURATION = 0.4

ENABLE_HOOK = True
ENABLE_CAPTIONS = {bool(enable_captions)}
ENABLE_MUSIC = {settings["enable_music"]}
ENABLE_SFX = {settings["enable_sfx"]}
ENABLE_BROLL = True
ENABLE_MOTION = True

CAPTION_MODE = "FAST"
CAPTION_GROUP_SIZE = 3

VIDEO_STYLE = "cinematic"
PROMPT_MAX_WORDS = 55

IMAGE_FOLDER = "images"
AUDIO_FOLDER = "audio"
VIDEO_FOLDER = "videos"
STORY_FILE = "stories/story1.txt"
'''

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(config_text)


def generate_video(topic, mode, enable_captions):

    topic = topic.strip() or "African folktale about wisdom"

    topic_file = os.path.join(PROJECT_DIR, "stories", "ui_topic.txt")

    os.makedirs(os.path.dirname(topic_file), exist_ok=True)

    with open(topic_file, "w", encoding="utf-8") as f:
        f.write(topic)

    write_runtime_config(topic, mode, enable_captions)

    env = os.environ.copy()
    env["UI_TOPIC"] = topic
    env["UI_MODE"] = mode.strip()

    process = subprocess.Popen(
        [sys.executable, "create_story_video.py"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )

    live_logs = ""
    progress_value = 0
    status_text = "Starting..."

    for line in process.stdout:

        live_logs += line

        if line.startswith("[PROGRESS]"):

            try:
                progress_data = line.replace("[PROGRESS]", "").strip()

                percent_text, message = progress_data.split("|", 1)

                progress_value = int(percent_text.strip())
                status_text = message.strip()

            except Exception:
                pass

        yield (
            None,
            live_logs,
            gr.update(value=progress_value),
            gr.update(value=f"🎬 {status_text}")
        )

    process.wait()

    latest_video = get_latest_video()

    if process.returncode != 0:

        yield (
            None,
            "❌ Rendering failed.\n\n" + live_logs,
            gr.update(value=0),
            gr.update(value="❌ Render Failed")
        )

        return

    yield (
        latest_video,
        "✅ Video generated successfully!\n\n" + live_logs,
        gr.update(value=100),
        gr.update(value="✅ Render Complete")
    )


with gr.Blocks(title="CineForge Studio") as demo:

    with gr.Row(elem_id="studio-header"):

        gr.HTML(
            """
            <div>
                <div id="studio-title">🎬 CineForge Studio</div>
                <div id="studio-subtitle">AI cinematic short-film generator powered by your local pipeline</div>
            </div>
            """
        )

    with gr.Row():

        with gr.Column(scale=1, elem_classes="panel"):

            gr.Markdown("### 🎞️ Project")

            topic = gr.Textbox(
                label="Video Topic",
                placeholder="Example: African folktale about wisdom",
                value="African folktale about wisdom",
                lines=3
            )

            mode = gr.Dropdown(
                label="Render Mode",
                choices=["DEV", "TEST", "PROD"],
                value="DEV"
            )

            enable_captions = gr.Checkbox(
                label="Captions",
                value=True
            )

            generate_btn = gr.Button(
                "🚀 Generate Video",
                variant="primary"
            )

        with gr.Column(scale=3, elem_classes="center-panel"):

            gr.Markdown("### ▶️ Preview Monitor")

            video_output = gr.Video(
                label="Generated Video",
                height=520
            )

        with gr.Column(scale=1, elem_classes="panel"):

            gr.Markdown("### ⚙️ Mode Presets")

            gr.Markdown(
                """
                **DEV**  
                Fast preview: 2 scenes, 2 shots, low resolution, no music/SFX.

                **TEST**  
                Balanced preview: 3 scenes, 3 shots, medium resolution, music on.

                **PROD**  
                Final render: 5 scenes, 5 shots, HD, music/SFX on.
                """
            )

    with gr.Row(elem_id="timeline-box"):

        with gr.Column(elem_classes="panel"):

            gr.Markdown("### 🧵 Timeline / Live System Log")

            progress_status = gr.Markdown(
                "🎬 Waiting to render..."
            )

            progress_bar = gr.Slider(
                minimum=0,
                maximum=100,
                value=0,
                step=1,
                interactive=False,
                label="Render Progress"
            )

            log_output = gr.Textbox(
                label="",
                lines=18,
                max_lines=28
            )

    generate_btn.click(
        fn=generate_video,
        inputs=[
            topic,
            mode,
            enable_captions
        ],
        outputs=[
            video_output,
            log_output,
            progress_bar,
            progress_status
        ]
    )


if __name__ == "__main__":

    demo.launch(
        css=CUSTOM_CSS,
        theme=gr.themes.Base()
    )




