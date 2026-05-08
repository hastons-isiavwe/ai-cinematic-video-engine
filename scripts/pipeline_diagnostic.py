import os
import traceback

print("\n==============================")
print(" CRYSTAL AI CINEMA DIAGNOSTIC ")
print("==============================\n")

errors = []


def test_import(module_name):
    try:
        __import__(module_name)
        print(f"PASS IMPORT: {module_name}")
    except Exception as e:
        print(f"FAIL IMPORT: {module_name}")
        errors.append((module_name, str(e)))


def test_function(label, func):
    try:
        func()
        print(f"PASS TEST: {label}")
    except Exception as e:
        print(f"FAIL TEST: {label}")
        errors.append((label, traceback.format_exc()))


# -----------------------------
# IMPORT TESTS
# -----------------------------

modules = [
    "scripts.cinematic_orchestrator",
    "scripts.cinematic_timing_core",
    "scripts.pipeline_governor",
    "scripts.character_engine",
    "scripts.generate_image",
    "scripts.cinematic_motion",
    "scripts.audio_scene_splitter",
    "scripts.scene_audio_generator",
    "scripts.sync_validator_v2"
]

for m in modules:
    test_import(m)


# -----------------------------
# PIPELINE TESTS
# -----------------------------

def timeline_test():

    from scripts.cinematic_orchestrator import CinematicOrchestrator

    story = """
    A lonely king walks through the ruins of his fallen kingdom.
    Thunder cracks across the sky as ancient statues crumble.
    """

    orchestrator = CinematicOrchestrator()

    timeline = orchestrator.build(story)

    if not timeline:
        raise Exception("Timeline returned empty")

    print(f"Timeline generated: {len(timeline)} segments")


test_function("Timeline Generation", timeline_test)


def character_test():

    from scripts.character_engine import extract_characters

    story = "King Arin stood alone while Princess Lyra watched from the tower."

    chars = extract_characters(story)

    if not chars:
        raise Exception("No characters detected")

    print(f"Characters detected: {chars}")


test_function("Character Extraction", character_test)


def audio_split_test():

    from scripts.audio_scene_splitter import split_story_into_scene_audio_payloads

    timeline = [
        {"id":1,"type":"scene","text":"The king walks alone","duration":5},
        {"id":2,"type":"scene","text":"Lightning strikes the sky","duration":5},
    ]

    payload = split_story_into_scene_audio_payloads(timeline)

    if not payload:
        raise Exception("Audio payload generation failed")

    print(f"Audio payloads: {len(payload)}")


test_function("Audio Split System", audio_split_test)


def timing_core_test():

    from scripts.cinematic_timing_core import CinematicTimingCore

    timeline = [
        {"id":1,"type":"scene","text":"test scene one","duration":4},
        {"id":2,"type":"scene","text":"test scene two","duration":4},
    ]

    core = CinematicTimingCore()

    result = core.resolve_timing(timeline)

    if not result:
        raise Exception("Timing core failed")

    print("Timing core resolved durations")


test_function("Timing Core", timing_core_test)


# -----------------------------
# RESULTS
# -----------------------------

print("\n==============================")
print(" DIAGNOSTIC RESULTS")
print("==============================\n")

if not errors:
    print("ALL SYSTEMS PASSED\n")
else:

    print("SYSTEM ERRORS DETECTED:\n")

    for err in errors:
        print(f"\n{err[0]}")
        print(err[1])

print("\nDiagnostic complete.\n")