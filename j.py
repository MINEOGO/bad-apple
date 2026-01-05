import os
import json
from PIL import Image

FRAMES_DIR = "frames"
OUT_DIR = "binary-chunks"

FRAMES_PER_CHUNK = 100  # number of frames per JSON file
ASCII_WIDTH = 120       # resize width for uniformity
TOTAL_FRAMES = 6500     # adjust if needed

os.makedirs(OUT_DIR, exist_ok=True)

def img_to_binary(img, width=ASCII_WIDTH):
    """
    Convert an image to binary 0/1 array
    Black = 0, White = 1
    """
    # force pure black and white
    img = img.convert("1")

    # maintain aspect ratio
    w, h = img.size
    aspect = h / w
    img = img.resize((width, int(width * aspect * 0.5)))

    pixels = list(img.getdata())
    binary_frame = []

    for i in range(0, len(pixels), img.width):
        row = [1 if pixels[i+j] else 0 for j in range(img.width)]
        binary_frame.append(row)

    return binary_frame

# get all PNG frames
frames = sorted(f for f in os.listdir(FRAMES_DIR) if f.lower().endswith(".png"))[:TOTAL_FRAMES]

chunk_count = (len(frames) + FRAMES_PER_CHUNK - 1) // FRAMES_PER_CHUNK

print(f"Total frames: {len(frames)}")
print(f"Creating {chunk_count} chunks...")

for c in range(chunk_count):
    start = c * FRAMES_PER_CHUNK
    end = start + FRAMES_PER_CHUNK
    chunk_frames = []

    for fname in frames[start:end]:
        path = os.path.join(FRAMES_DIR, fname)
        with Image.open(path) as im:
            binary_frame = img_to_binary(im)
            chunk_frames.append({
                "frame": fname,
                "binary": binary_frame
            })

    out_path = os.path.join(OUT_DIR, f"chunk_{c+1:02d}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(chunk_frames, f)

    print(f"Saved {out_path} ({len(chunk_frames)} frames)")

print("done")
