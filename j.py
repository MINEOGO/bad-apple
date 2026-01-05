import os, json
from PIL import Image

FRAMES_DIR = "frames"
OUT_DIR = "binary-chunks"

FRAMES_PER_CHUNK = 100
WIDTH = 120
THRESHOLD = 90   # LOWER = more filled shapes

os.makedirs(OUT_DIR, exist_ok=True)

def img_to_ascii01(img):
    # grayscale first
    img = img.convert("L")

    # threshold FIRST (important)
    img = img.point(lambda p: 255 if p >= THRESHOLD else 0, mode="1")

    # THEN resize (keeps fills)
    w, h = img.size
    aspect = h / w
    img = img.resize((WIDTH, int(WIDTH * aspect * 0.5)))

    pixels = list(img.getdata())
    lines = []

    for y in range(img.height):
        row = []
        for x in range(img.width):
            row.append("1" if pixels[y * img.width + x] else "0")
        lines.append("".join(row))

    return "\n".join(lines)

frames = sorted(f for f in os.listdir(FRAMES_DIR) if f.endswith(".png"))

chunk_i = 1
for i in range(0, len(frames), FRAMES_PER_CHUNK):
    chunk = []

    for fname in frames[i:i + FRAMES_PER_CHUNK]:
        with Image.open(os.path.join(FRAMES_DIR, fname)) as im:
            chunk.append({
                "frame": fname,
                "ascii": img_to_ascii01(im)
            })

    with open(f"{OUT_DIR}/chunk_{chunk_i:02d}.json", "w") as f:
        json.dump(chunk, f)

    print(f"saved chunk_{chunk_i:02d}.json")
    chunk_i += 1

print("done. no more outline-only garbage 🫩")
