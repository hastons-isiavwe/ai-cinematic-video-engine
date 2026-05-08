import os
from moviepy.editor import AudioFileClip


class CinematicTimingCore:

    def __init__(self, min_scene_length=2.0):
        self.min_scene_length = min_scene_length

    def get_audio_duration(self, audio_path):

        try:
            audio = AudioFileClip(audio_path)
            duration = audio.duration
            audio.close()
            return duration
        except Exception:
            return None

    def attach_audio_to_timeline(self, timeline, audio_map):
        """
        Attach audio file paths directly into timeline
        """

        for scene in timeline:

            if scene["type"] != "scene":
                continue

            audio = next(
                (a["audio_path"] for a in audio_map
                 if str(a["scene_id"]) == str(scene["id"])),
                None
            )

            if audio:
                scene["audio"] = audio

        return timeline

    def compute_true_scene_durations(self, timeline):
        """
        Audio becomes the source of truth for scene timing
        """

        for scene in timeline:

            if scene["type"] != "scene":
                continue

            audio_path = scene.get("audio")

            if not audio_path or not os.path.exists(audio_path):
                scene["duration"] = max(self.min_scene_length, scene.get("duration", 5))
                scene["timing_source"] = "fallback"
                continue

            audio_duration = self.get_audio_duration(audio_path)

            if audio_duration is None:
                scene["duration"] = max(self.min_scene_length, scene.get("duration", 5))
                scene["timing_source"] = "fallback"
                continue

            scene["duration"] = max(self.min_scene_length, audio_duration)
            scene["timing_source"] = "audio"

        return timeline

    def compute_timeline_positions(self, timeline):
        """
        Calculates exact start and end timestamps
        """

        current_time = 0

        for scene in timeline:

            duration = scene.get("duration", 5)

            scene["start_time"] = current_time
            scene["end_time"] = current_time + duration

            current_time += duration

        return timeline

    def build_master_clock(self, timeline, audio_map):

        timeline = self.attach_audio_to_timeline(timeline, audio_map)

        timeline = self.compute_true_scene_durations(timeline)

        timeline = self.compute_timeline_positions(timeline)

        return timeline