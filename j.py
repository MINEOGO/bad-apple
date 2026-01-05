import os
import json
from PIL import Image

FRAMES_DIR = "frames"
OUT_DIR = "ascii01-chunks"

FRAMES_PER_CHUNK = 100
WIDTH = 120
THRESHOLD = 128  # brightness cutoff

os.makedirs(OUT_DIR, exist_ok=True)

def img_to_ascii01(img):
    # grayscale
    img = img.convert("L")

    # resize, keep aspect (terminal correction)
    w, h = img.size
    aspect = h / w
    img = img.resize((WIDTH, int(WIDTH * aspect * 0.5)))

    pixels = list(img.getdata())
    lines = []

    for y in range(img.height):
        row = []
        for x in range(img.width):
            px = pixels[y * img.width + x]
            row.append("1" if px >= THRESHOLD else "0")
        lines.append("".join(row))

    return "\n".join(lines)

frames = sorted(
    f for f in os.listdir(FRAMES_DIR)
    if f.lower().endswith(".png")
)

chunk_idx = 1
for i in range(0, len(frames), FRAMES_PER_CHUNK):
    chunk = []

    for fname in frames[i:i + FRAMES_PER_CHUNK]:
        with Image.open(os.path.join(FRAMES_DIR, fname)) as im:
            chunk.append({
                "frame": fname,
                "ascii": img_to_ascii01(im)
            })

    out_path = os.path.join(OUT_DIR, f"chunk_{chunk_idx:02d}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(chunk, f)

    print(f"saved {out_path}")
    chunk_idx += 1

print("done")
