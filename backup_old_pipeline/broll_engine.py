def extract_broll_prompts(directed_timeline):
    brolls = []

    for item in directed_timeline:

        # 🎯 ONLY USE DIRECTOR DECISION
        if not item.get("needs_broll"):
            continue

        prompt = build_broll_prompt(item)

        brolls.append({
            "id": f"broll_{item['id']}",
            "text": prompt,
            "emotion": item["emotion"],
            "score": item["score"]
        })

    return brolls


def build_broll_prompt(item):

    text = item["text"][:120]
    emotion = item["emotion"]

    camera = item.get("camera", "")
    lighting = item.get("lighting", "")

    if emotion == "high":
        return f"dramatic cinematic b-roll, {camera}, {lighting}, intense atmosphere, {text}"

    if emotion == "medium":
        return f"cinematic narrative b-roll, {camera}, {lighting}, balanced tone, {text}"

    return f"ambient cinematic b-roll, {camera}, {lighting}, calm atmosphere, {text}"