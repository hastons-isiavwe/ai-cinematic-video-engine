import os
import shutil

base_dir = os.getcwd()

# Target folder structure
folders = {
    "stories": ["story1.txt"],
    "audio": [],
    "images": ["scene_5.png"],
    "videos": [],
    "scripts": [
        "voice_first_pipeline.py",
        "generate_image.py",
        "generate_story_images.py",
        "prompt_engine.py",
        "script_text.py"
    ]
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Move files
for folder, files in folders.items():
    for file in files:
        src_paths = [
            os.path.join(base_dir, file),
            os.path.join(base_dir, "scripts", file)
        ]

        for src in src_paths:
            if os.path.exists(src):
                dst = os.path.join(base_dir, folder, file)
                if src != dst:
                    shutil.move(src, dst)
                    print(f"Moved {file} -> {folder}")
                break

print("✅ Project reorganized successfully.")