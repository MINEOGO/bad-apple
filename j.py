import os
import json
import base64
import subprocess
from PIL import Image

VIDEO = "【東方】Bad Apple!! ＰＶ【影絵】.mp4"

FRAMES_DIR = "frames"
CHUNKS_DIR = "chunks"

TOTAL_FRAMES = 6500
FRAMES_PER_CHUNK = 100
CHUNK_COUNT = TOTAL_FRAMES // FRAMES_PER_CHUNK  # 65

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
    if f.lower().endswith(".png")
)[:TOTAL_FRAMES]

def png_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

print("packing pngs into json...")
for i in range(CHUNK_COUNT):
    start = i * FRAMES_PER_CHUNK
    end = start + FRAMES_PER_CHUNK

    chunk = []

    for fname in frames[start:end]:
        fpath = os.path.join(FRAMES_DIR, fname)
        with Image.open(fpath) as im:
            w, h = im.size

        chunk.append({
            "name": fname,
            "width": w,
            "height": h,
            "data": png_to_base64(fpath)
        })

    out = os.path.join(CHUNKS_DIR, f"chunk_{i+1:02d}.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(chunk, f)

    print(f"chunk_{i+1:02d}.json -> {len(chunk)} frames")

print("done. whole pngs inside json, happy now 🥀")
