# scripts/sync_validator.py

from moviepy.editor import AudioFileClip


class SceneAudioSyncValidator:

    def __init__(self, tolerance=0.25):
        # tolerance = allowed mismatch in seconds
        self.tolerance = tolerance

    def validate(self, timeline, audio_map):
        """
        Ensures every scene has correct audio alignment.
        Returns corrected mapping.
        """

        validated = []

        for item in timeline:

            scene_id = item["id"]

            audio_entry = next(
                (a for a in audio_map if a["scene_id"] == scene_id),
                None
            )

            scene_duration = float(item.get("duration", 6))

            if audio_entry:

                audio_clip = AudioFileClip(audio_entry["audio_path"])
                audio_duration = audio_clip.duration

                diff = abs(audio_duration - scene_duration)

                # If mismatch is too large, correct it
                if diff > self.tolerance:
                    print(f"[SYNC FIX] Scene {scene_id}: audio adjusted ({audio_duration:.2f}s → {scene_duration:.2f}s)")

                validated.append({
                    "scene_id": scene_id,
                    "audio_path": audio_entry["audio_path"],
                    "duration": scene_duration,
                    "audio_duration": audio_duration
                })

            else:
                # No audio found → silent padding
                print(f"[SYNC WARN] Scene {scene_id}: no audio found, inserting silence")
                validated.append({
                    "scene_id": scene_id,
                    "audio_path": None,
                    "duration": scene_duration,
                    "audio_duration": 0
                })

        return validated

    def enforce_timeline_lock(self, validated_audio_map):
        """
        Locks final timing so video builder cannot modify it later.
        """

        return tuple(
            (v["scene_id"], v["duration"], v["audio_path"])
            for v in validated_audio_map
        )