import os

TOTAL_VIDEOS = 5  # start small

for i in range(TOTAL_VIDEOS):
    print(f"\n=== GENERATING VIDEO {i+1} ===\n")
    os.system("python create_story_video.py")