import os
import json
import math
import subprocess
from PIL import Image

VIDEO_FILE = "【東方】Bad Apple!! ＰＶ【影絵】.mp4"
TOTAL_FRAMES = 6500
CHUNK_COUNT = 65
FRAMES_PER_CHUNK = TOTAL_FRAMES // CHUNK_COUNT

FRAMES_DIR = "frames_tmp"
CHUNKS_DIR = "chunks"

os.makedirs(FRAMES_DIR, exist_ok=True)
os.makedirs(CHUNKS_DIR, exist_ok=True)

# extract frames using ffmpeg
print("extracting frames...")
subprocess.run([
    "ffmpeg",
    "-i", VIDEO_FILE,
    "-vf", f"fps={TOTAL_FRAMES}/219",  # bad apple ~219s
    f"{FRAMES_DIR}/frame_%05d.png"
], check=True)

def image_to_ascii(img, width=80):
    img = img.convert("L")
    w, h = img.size
    aspect = h / w
    img = img.resize((width, int(width * aspect * 0.55)))
    pixels = img.getdata()
    chars = " .:-=+*#%@"
    ascii_str = ""
    for i, p in enumerate(pixels):
        ascii_str += chars[p * len(chars) // 256]
        if (i + 1) % img.width == 0:
            ascii_str += "\n"
    return ascii_str

frames = sorted(os.listdir(FRAMES_DIR))[:TOTAL_FRAMES]

print("processing + chunking...")
for chunk_index in range(CHUNK_COUNT):
    chunk_data = {}
    start = chunk_index * FRAMES_PER_CHUNK
    end = start + FRAMES_PER_CHUNK

    for i in range(start, min(end, len(frames))):
        frame_path = os.path.join(FRAMES_DIR, frames[i])
        with Image.open(frame_path) as im:
            chunk_data[f"frame_{i}"] = image_to_ascii(im)

    chunk_file = os.path.join(CHUNKS_DIR, f"chunk_{chunk_index+1:02d}.json")
    with open(chunk_file, "w", encoding="utf-8") as f:
        json.dump(chunk_data, f)

    print(f"saved {chunk_file}")

print("done. 65 chunks created ❤️‍🩹🥀")
