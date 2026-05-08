import os
import sys
import subprocess
import gradio as gr


PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
VIDEO_DIR = os.path.join(PROJECT_DIR, "videos")


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


def generate_video(topic, mode):

    topic_file = os.path.join(PROJECT_DIR, "stories", "ui_topic.txt")

    os.makedirs(os.path.dirname(topic_file), exist_ok=True)

    with open(topic_file, "w", encoding="utf-8") as f:
        f.write(topic.strip())

    env = os.environ.copy()
    env["UI_TOPIC"] = topic.strip()
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

    for line in process.stdout:
        live_logs += line
        yield None, live_logs

    process.wait()

    latest_video = get_latest_video()

    if process.returncode != 0:
        yield None, "❌ Rendering failed.\n\n" + live_logs
        return

    yield latest_video, "✅ Video generated successfully!\n\n" + live_logs


with gr.Blocks(title="CineForge AI") as demo:
    gr.Markdown("# 🎬 CineForge AI")
    gr.Markdown("Forge cinematic AI stories locally.")
    gr.Markdown("Generate cinematic short-form videos using your local AI pipeline.")

    with gr.Row():
        with gr.Column():
            topic = gr.Textbox(
                label="Video Topic",
                placeholder="Example: African folktale about wisdom",
                value="African folktale about wisdom"
            )

            mode = gr.Dropdown(
                label="Render Mode",
                choices=["DEV", "TEST", "PROD"],
                value="DEV"
            )

            generate_btn = gr.Button("Generate Video", variant="primary")

        with gr.Column():
            video_output = gr.Video(label="Generated Video")
            log_output = gr.Textbox(
                label="System Log",
                lines=18
            )

    generate_btn.click(
        fn=generate_video,
        inputs=[topic, mode],
        outputs=[video_output, log_output]
    )


if __name__ == "__main__":
    demo.launch()