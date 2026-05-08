import os
import requests

ELEVEN_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


def generate_scene_audio(scene_units, api_key, voice_id, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    audio_paths = []

    for unit in scene_units:
        scene_id = unit["scene_id"]
        text = unit["text"]

        url = ELEVEN_URL.format(voice_id=voice_id)

        response = requests.post(
            url,
            headers={
                "xi-api-key": api_key,
                "Content-Type": "application/json"
            },
            json={
                "text": text,
                "voice_settings": {
                    "stability": 0.75,
                    "similarity_boost": 0.75
                }
            }
        )

        if response.status_code != 200:
            raise Exception(f"ElevenLabs failed on scene {scene_id}: {response.text}")

        audio_path = os.path.join(output_dir, f"scene_{scene_id}.mp3")

        with open(audio_path, "wb") as f:
            f.write(response.content)

        audio_paths.append({
            "scene_id": scene_id,
            "audio_path": audio_path
        })

        print(f"Audio generated → Scene {scene_id}")

    return audio_paths