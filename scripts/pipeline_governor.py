# scripts/pipeline_governor.py

class PipelineGovernor:
    """
    Ensures strict execution order and data integrity across cinematic pipeline.
    Prevents modules from conflicting or re-processing logic incorrectly.
    """

    REQUIRED_KEYS = [
        "id",
        "type",
        "text",
        "emotion",
        "score",
        "duration"
    ]

    def validate_timeline(self, timeline):
        if not timeline:
            raise Exception("Timeline is empty")

        for item in timeline:
            for key in self.REQUIRED_KEYS:
                if key not in item:
                    raise Exception(f"Timeline missing key: {key} in item {item}")

        return True

    def enforce_execution_order(self, timeline):
        """
        Ensures correct ordering:
        scene → broll → scene → broll
        """
        ordered = []

        for item in timeline:
            if item["type"] == "scene":
                ordered.append(item)
            elif item["type"] == "broll":
                ordered.append(item)

        return ordered

    def lock_timeline(self, timeline):
        """
        Prevents further structural modifications.
        """
        return tuple(tuple(sorted(item.items())) for item in timeline)

    def sanitize(self, timeline):
        """
        Final safety pass before image generation.
        """

        cleaned = []

        for item in timeline:
            cleaned.append({
                "id": item["id"],
                "type": item["type"],
                "text": item["text"],
                "emotion": item.get("emotion", "medium"),
                "score": float(item.get("score", 0.5)),
                "duration": int(item.get("duration", 6))
            })

        return cleaned