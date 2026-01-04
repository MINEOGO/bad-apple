import os
import shutil

FRAMES_DIR = "frames_tmp"      # where your 6500 pngs already are
CHUNKS_DIR = "chunks"

TOTAL_FRAMES = 6500
CHUNK_COUNT = 65
FRAMES_PER_CHUNK = TOTAL_FRAMES // CHUNK_COUNT  # 100

os.makedirs(CHUNKS_DIR, exist_ok=True)

frames = sorted(
    f for f in os.listdir(FRAMES_DIR)
    if f.lower().endswith(".png")
)[:TOTAL_FRAMES]

for i in range(CHUNK_COUNT):
    chunk_path = os.path.join(CHUNKS_DIR, f"chunk_{i+1:02d}")
    os.makedirs(chunk_path, exist_ok=True)

    start = i * FRAMES_PER_CHUNK
    end = start + FRAMES_PER_CHUNK

    for frame in frames[start:end]:
        src = os.path.join(FRAMES_DIR, frame)
        dst = os.path.join(chunk_path, frame)
        shutil.copy2(src, dst)

    print(f"chunk {i+1:02d} done")

print("all pngs chunked. stfu and enjoy ❤️‍🩹🥀")
