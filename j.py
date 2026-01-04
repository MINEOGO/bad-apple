import os
import json
import subprocess

VIDEO = "【東方】Bad Apple!! ＰＶ【影絵】.mp4"

FRAMES_DIR = "frames"
CHUNKS_DIR = "chunks"

TOTAL_FRAMES = 6500
CHUNK_COUNT = 65
FRAMES_PER_CHUNK = TOTAL_FRAMES // CHUNK_COUNT  # 100

os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(CHUNKS_DIR, exist_ok=True)

print("extracting frames...")
subprocess.run([
    "ffmpeg",
    "-i", VIDEO,
    "-vf", "fps=30",
    f"{FRAMES_DIR}/frame_%05d.png"
], check=True)

frames = sorted(
    f for f in os.listdir(FRAMES_DIR)
    if f.endswith(".png")
)[:TOTAL_FRAMES]

print("creating json chunks...")
for i in range(CHUNK_COUNT):
    start = i * FRAMES_PER_CHUNK
    end = start + FRAMES_PER_CHUNK

    chunk_frames = frames[start:end]

    chunk_path = os.path.join(CHUNKS_DIR, f"chunk_{i+1:02d}.json")
    with open(chunk_path, "w", encoding="utf-8") as f:
        json.dump(chunk_frames, f)

    print(f"chunk_{i+1:02d}.json → {len(chunk_frames)} frames")

print("done. sybau ❤️‍🩹🥀")
