import os
import json
import random
from PIL import Image

FRAMES_DIR = "frames"
OUT_DIR = "py-chunk"

TOTAL_FRAMES = 6500
FRAMES_PER_CHUNK = 100

os.makedirs(OUT_DIR, exist_ok=True)

PY_TOKENS = [
    "if", "else", "elif", "for", "while", "def", "return",
    "True", "False", "None", "and", "or", "not",
    "==", "!=", "<=", ">=", "+=", "-=", "*=", "/=",
    "{}", "[]", "()", ":", "::", "pass", "break", "continue"
]

def img_to_py_ascii(img, width=80):
    img = img.convert("L")
    w, h = img.size
    aspect = h / w
    img = img.resize((width, int(width * aspect * 0.5)))

    pixels = list(img.getdata())
    out = ""
    for i, p in enumerate(pixels):
        token = PY_TOKENS[p % len(PY_TOKENS)]
        out += token.ljust(4)[:4]  # fixed width
        if (i + 1) % img.width == 0:
            out += "\n"
    return out

frames = sorted(
    f for f in os.listdir(FRAMES_DIR)
    if f.lower().endswith(".png")
)[:TOTAL_FRAMES]

chunk_count = (len(frames) + FRAMES_PER_CHUNK - 1) // FRAMES_PER_CHUNK

for c in range(chunk_count):
    start = c * FRAMES_PER_CHUNK
    end = start + FRAMES_PER_CHUNK

    chunk = []

    for fname in frames[start:end]:
        path = os.path.join(FRAMES_DIR, fname)
        with Image.open(path) as im:
            ascii_frame = img_to_py_ascii(im)

        chunk.append({
            "frame": fname,
            "ascii": ascii_frame
        })

    out_path = os.path.join(OUT_DIR, f"chunk_{c+1:02d}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(chunk, f)

    print(f"chunk_{c+1:02d}.json -> {len(chunk)} frames")

print("done. python brainrot video unlocked 🥀")
