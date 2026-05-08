import os

# Folder containing the scripts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

# Files we want to remove
FILES_TO_DELETE = [
    "broll_engine_v2.py",
    "timeline_engine.py",
    "timeline_orchestrator.py",
    "timeline_sync_engine.py",
    "sync_validator.py",
    "cinematic_director.py"
]

print("\n--- PIPELINE CLEANUP STARTED ---\n")

deleted = []
missing = []

for filename in FILES_TO_DELETE:

    file_path = os.path.join(SCRIPTS_DIR, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        deleted.append(filename)
        print(f"Deleted: {filename}")

    else:
        missing.append(filename)
        print(f"Not Found: {filename}")

print("\n--- CLEANUP COMPLETE ---\n")

print("Deleted Files:")
for f in deleted:
    print(f" - {f}")

if missing:
    print("\nFiles Already Missing:")
    for f in missing:
        print(f" - {f}")