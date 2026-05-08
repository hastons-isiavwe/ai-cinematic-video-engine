from scripts.cinematic_orchestrator import CinematicOrchestrator

story = """
A young orphan walks into a forbidden forest at night. Strange lights appear between the trees.
She hears whispers calling her name, but she keeps walking deeper until she finds a glowing ancient object.
"""

orchestrator = CinematicOrchestrator()
timeline = orchestrator.build_timeline(story)

print("\n--- CINEMATIC TIMELINE ---\n")

for item in timeline:
    print(f"ID: {item['id']}")
    print(f"Type: {item['type']}")
    print(f"Emotion: {item['emotion']}")
    print(f"Score: {item['score']}")
    print(f"Camera: {item['camera']}")
    print(f"Lighting: {item['lighting']}")
    print(f"Duration: {item['duration']}")
    print(f"B-roll Allowed: {item['broll_allowed']}")
    print(f"Text: {item['text'][:80]}...")
    print("-" * 50)