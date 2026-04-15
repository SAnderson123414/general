"""
image_downloader.py

Downloads images from Wikimedia Commons (and falls back to Pillow-generated
illustrations if the download fails or no internet is available).

All images are cached in the images/ sub-folders so they are only generated
once per run.
"""

import os
import io
import math
import hashlib
import requests
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR    = Path(__file__).resolve().parent.parent
IMAGES_DIR  = BASE_DIR / "images"
FAMILY_DIR  = IMAGES_DIR / "family"
HOUSE_DIR   = IMAGES_DIR / "house"
NUMBERS_DIR = IMAGES_DIR / "numbers"

for _d in (FAMILY_DIR, HOUSE_DIR, NUMBERS_DIR):
    _d.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# Wikimedia Commons search helper
# ---------------------------------------------------------------------------
WIKIMEDIA_API = "https://en.wikipedia.org/w/api.php"

def _try_wikimedia(query: str, out_path: Path, size: int = 200) -> bool:
    """Try to fetch an image from Wikimedia Commons. Returns True on success."""
    try:
        params = {
            "action": "query",
            "generator": "search",
            "gsrnamespace": 6,
            "gsrsearch": f"file:{query} clip art",
            "gsrlimit": 1,
            "prop": "imageinfo",
            "iiprop": "url|mime",
            "iiurlwidth": size,
            "format": "json",
        }
        r = requests.get(WIKIMEDIA_API, params=params, timeout=8)
        r.raise_for_status()
        data = r.json()
        pages = data.get("query", {}).get("pages", {})
        for page in pages.values():
            info = page.get("imageinfo", [{}])[0]
            thumb_url = info.get("thumburl") or info.get("url")
            mime = info.get("mime", "")
            if thumb_url and mime.startswith("image/"):
                img_r = requests.get(thumb_url, timeout=10)
                img_r.raise_for_status()
                img = Image.open(io.BytesIO(img_r.content)).convert("RGBA")
                img = img.resize((size, size), Image.LANCZOS)
                img.save(str(out_path))
                return True
    except Exception:
        pass
    return False

# ---------------------------------------------------------------------------
# Pillow fallback generators
# ---------------------------------------------------------------------------
IMG_SIZE = 200

def _font(size: int):
    """Return a font; fall back to the default Pillow bitmap font."""
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except OSError:
        pass
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf", size)
    except OSError:
        pass
    return ImageFont.load_default()

def _text_center(draw, text, y, w, font, color=(50, 50, 50)):
    """Draw text centred horizontally."""
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
    except AttributeError:
        tw, _ = draw.textsize(text, font=font)
    draw.text(((w - tw) // 2, y), text, fill=color, font=font)


def _make_family_image(member: dict, out_path: Path):
    """Draw a simple stick-figure representation of a family member."""
    w = h = IMG_SIZE
    bg = member["color"]
    img = Image.new("RGBA", (w, h), bg + (255,))
    d = ImageDraw.Draw(img)

    tall = member.get("tall", True)
    has_bow = member.get("bow", False)
    has_hat = member.get("hat", False)
    has_glasses = member.get("glasses", False)
    shirt_color = tuple(max(0, c - 60) for c in bg[:3]) + (255,)

    body_top = 60 if tall else 75
    body_bottom = 155 if tall else 160
    cx = w // 2
    head_r = 28 if tall else 22
    head_cy = body_top - head_r - 2

    # Body (rounded rectangle)
    body_w = 50 if tall else 40
    d.rounded_rectangle(
        [cx - body_w // 2, body_top, cx + body_w // 2, body_bottom],
        radius=10,
        fill=shirt_color,
        outline=(80, 80, 80),
        width=2,
    )

    # Head
    d.ellipse(
        [cx - head_r, head_cy - head_r, cx + head_r, head_cy + head_r],
        fill=(255, 222, 173),
        outline=(80, 80, 80),
        width=2,
    )

    # Eyes
    eye_y = head_cy - 5
    d.ellipse([cx - 10, eye_y - 4, cx - 4, eye_y + 2], fill=(40, 40, 40))
    d.ellipse([cx + 4,  eye_y - 4, cx + 10, eye_y + 2], fill=(40, 40, 40))

    # Smile
    d.arc([cx - 10, head_cy - 2, cx + 10, head_cy + 12], start=10, end=170,
          fill=(150, 60, 60), width=2)

    # Glasses
    if has_glasses:
        d.ellipse([cx - 14, eye_y - 8, cx - 2, eye_y + 6], outline=(80, 80, 80), width=2)
        d.ellipse([cx + 2,  eye_y - 8, cx + 14, eye_y + 6], outline=(80, 80, 80), width=2)
        d.line([cx - 2, eye_y - 1, cx + 2, eye_y - 1], fill=(80, 80, 80), width=2)

    # Hat
    if has_hat:
        hat_y = head_cy - head_r
        d.rectangle([cx - 18, hat_y - 18, cx + 18, hat_y], fill=(80, 80, 180), outline=(40, 40, 40), width=2)
        d.rectangle([cx - 24, hat_y - 4, cx + 24, hat_y + 2], fill=(80, 80, 180), outline=(40, 40, 40), width=2)

    # Bow (for female members)
    if has_bow:
        bow_y = head_cy - head_r - 4
        d.polygon(
            [(cx, bow_y), (cx - 14, bow_y - 10), (cx - 14, bow_y + 10)],
            fill=(255, 80, 150),
        )
        d.polygon(
            [(cx, bow_y), (cx + 14, bow_y - 10), (cx + 14, bow_y + 10)],
            fill=(255, 80, 150),
        )
        d.ellipse([cx - 4, bow_y - 4, cx + 4, bow_y + 4], fill=(255, 150, 200))

    # Legs
    leg_y1 = body_bottom
    leg_y2 = body_bottom + 30
    d.line([cx - 12, leg_y1, cx - 12, leg_y2], fill=(80, 80, 80), width=4)
    d.line([cx + 12, leg_y1, cx + 12, leg_y2], fill=(80, 80, 80), width=4)

    # Feet
    d.ellipse([cx - 20, leg_y2 - 4, cx - 4,  leg_y2 + 8], fill=(80, 60, 40))
    d.ellipse([cx + 4,  leg_y2 - 4, cx + 20, leg_y2 + 8], fill=(80, 60, 40))

    # Arms
    arm_y = body_top + 20
    d.line([cx - body_w // 2, arm_y, cx - body_w // 2 - 20, arm_y + 20],
           fill=(255, 222, 173), width=5)
    d.line([cx + body_w // 2, arm_y, cx + body_w // 2 + 20, arm_y + 20],
           fill=(255, 222, 173), width=5)

    # Label
    label_font = _font(18)
    _text_center(d, member["name"], h - 26, w, label_font, color=(60, 60, 60))

    img.save(str(out_path))


def _make_number_image(number: int, label: str, bg: tuple, out_path: Path):
    """Draw a big number with dots representing the count."""
    w = h = IMG_SIZE
    img = Image.new("RGBA", (w, h), bg + (255,))
    d = ImageDraw.Draw(img)

    # Border
    d.rounded_rectangle([4, 4, w - 4, h - 4], radius=20,
                         outline=(80, 80, 80), width=3)

    # Big number
    num_font = _font(72)
    _text_center(d, str(number), 18, w, num_font, color=(50, 50, 150))

    # Word label
    word_font = _font(16)
    _text_center(d, label, 108, w, word_font, color=(80, 80, 80))

    # Dots row(s) representing the count
    dot_r = 7
    cols = min(number, 5)
    rows = math.ceil(number / cols)
    start_x = w // 2 - cols * (dot_r * 2 + 4) // 2
    start_y = 138
    dot_color = (220, 80, 80)
    for i in range(number):
        col = i % cols
        row = i // cols
        cx = start_x + col * (dot_r * 2 + 4) + dot_r
        cy = start_y + row * (dot_r * 2 + 4) + dot_r
        d.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r],
                  fill=dot_color, outline=(160, 40, 40), width=1)

    img.save(str(out_path))


# ---------------------------------------------------------------------------
# House-item shape generator (big switch on shape name)
# ---------------------------------------------------------------------------

def _make_house_image(item_name: str, shape: str, out_path: Path):  # noqa: C901
    """Draw a simple colourful representation of a house item."""
    w = h = IMG_SIZE
    # Background colour per room is not needed here; use white
    img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    d = ImageDraw.Draw(img)
    cx = w // 2

    def _lbl(text, color=(60, 60, 60)):
        f = _font(16)
        _text_center(d, text, h - 28, w, f, color)

    if shape == "stove":
        # Grey box with 4 burner circles
        d.rounded_rectangle([30, 40, 170, 160], radius=8,
                             fill=(160, 160, 160), outline=(80, 80, 80), width=2)
        for bx, by in [(70, 80), (130, 80), (70, 130), (130, 130)]:
            d.ellipse([bx - 18, by - 18, bx + 18, by + 18],
                      fill=(80, 80, 80), outline=(40, 40, 40), width=2)

    elif shape == "fridge":
        d.rounded_rectangle([50, 20, 150, 170], radius=8,
                             fill=(220, 235, 255), outline=(80, 80, 80), width=2)
        # Freezer section
        d.rectangle([50, 20, 150, 75], fill=(190, 210, 240), outline=(80, 80, 80), width=2)
        # Handles
        d.rectangle([130, 40, 138, 55], fill=(120, 120, 120))
        d.rectangle([130, 95, 138, 145], fill=(120, 120, 120))

    elif shape == "pot":
        d.ellipse([50, 60, 150, 160], fill=(80, 80, 80), outline=(40, 40, 40), width=2)
        d.rectangle([50, 80, 150, 130], fill=(80, 80, 80), outline=(40, 40, 40), width=2)
        d.line([100, 60, 100, 35], fill=(80, 80, 80), width=6)
        d.ellipse([90, 28, 110, 48], fill=(60, 60, 60))
        # Handles
        d.arc([25, 80, 55, 120], start=180, end=360, fill=(80, 80, 80), width=5)
        d.arc([145, 80, 175, 120], start=0, end=180, fill=(80, 80, 80), width=5)

    elif shape == "pan":
        d.ellipse([50, 70, 160, 160], fill=(60, 60, 60), outline=(30, 30, 30), width=2)
        d.rectangle([130, 105, 185, 120], fill=(60, 60, 60), outline=(30, 30, 30), width=2)

    elif shape == "plate":
        d.ellipse([30, 40, 170, 170], fill=(240, 240, 255), outline=(80, 80, 80), width=3)
        d.ellipse([55, 65, 145, 145], fill=(255, 255, 255), outline=(150, 150, 150), width=2)

    elif shape == "cup":
        d.rounded_rectangle([60, 50, 140, 160], radius=8,
                             fill=(255, 180, 80), outline=(80, 80, 80), width=2)
        d.arc([125, 80, 165, 130], start=270, end=90, fill=(80, 80, 80), width=5)

    elif shape == "spoon":
        d.ellipse([80, 25, 120, 65], fill=(180, 180, 200), outline=(80, 80, 80), width=2)
        d.rounded_rectangle([96, 60, 104, 170], radius=4,
                             fill=(180, 180, 200), outline=(80, 80, 80), width=2)

    elif shape == "fork":
        for x in [85, 95, 105, 115]:
            d.rounded_rectangle([x - 3, 20, x + 3, 80], radius=3,
                                 fill=(180, 180, 200), outline=(80, 80, 80), width=1)
        d.rounded_rectangle([94, 80, 106, 170], radius=4,
                             fill=(180, 180, 200), outline=(80, 80, 80), width=2)

    elif shape == "bed":
        d.rounded_rectangle([20, 90, 180, 160], radius=8,
                             fill=(180, 130, 80), outline=(80, 60, 40), width=2)
        d.rounded_rectangle([20, 55, 70, 100], radius=6,
                             fill=(255, 240, 200), outline=(80, 60, 40), width=2)
        d.rounded_rectangle([25, 100, 175, 155], radius=8,
                             fill=(200, 220, 255), outline=(120, 140, 200), width=2)

    elif shape == "pillow":
        d.rounded_rectangle([30, 60, 170, 150], radius=20,
                             fill=(255, 255, 220), outline=(180, 180, 120), width=3)
        d.line([100, 70, 100, 140], fill=(220, 220, 180), width=2)
        d.line([40, 105, 160, 105], fill=(220, 220, 180), width=2)

    elif shape == "blanket":
        colors = [(255, 180, 180), (180, 255, 180), (180, 180, 255), (255, 255, 180)]
        strip_w = 40
        for i, col in enumerate(colors):
            d.rectangle([30 + i * strip_w, 40, 30 + (i + 1) * strip_w, 160],
                        fill=col, outline=(200, 200, 200), width=1)
        d.rectangle([30, 40, 170, 160], outline=(80, 80, 80), width=2)

    elif shape == "lamp":
        # Shade
        d.polygon([(cx, 35), (cx - 45, 100), (cx + 45, 100)],
                  fill=(255, 240, 150), outline=(80, 80, 80))
        # Bulb hint
        d.ellipse([cx - 8, 85, cx + 8, 105], fill=(255, 255, 200))
        # Pole
        d.line([cx, 100, cx, 165], fill=(120, 80, 40), width=6)
        # Base
        d.ellipse([cx - 25, 158, cx + 25, 170], fill=(120, 80, 40))

    elif shape == "dresser":
        d.rounded_rectangle([30, 30, 170, 170], radius=6,
                             fill=(180, 140, 90), outline=(100, 70, 40), width=2)
        for row_y in [55, 95, 135]:
            d.rectangle([35, row_y, 165, row_y + 32], fill=(200, 160, 110),
                        outline=(100, 70, 40), width=2)
            d.ellipse([cx - 8, row_y + 10, cx + 8, row_y + 22], fill=(120, 80, 40))

    elif shape == "teddy":
        # Body
        d.ellipse([55, 80, 145, 165], fill=(200, 150, 80), outline=(120, 80, 30), width=2)
        # Head
        d.ellipse([65, 30, 135, 95], fill=(200, 150, 80), outline=(120, 80, 30), width=2)
        # Ears
        d.ellipse([60, 22, 82, 44], fill=(200, 150, 80), outline=(120, 80, 30), width=2)
        d.ellipse([118, 22, 140, 44], fill=(200, 150, 80), outline=(120, 80, 30), width=2)
        d.ellipse([63, 25, 79, 41], fill=(240, 180, 120))
        d.ellipse([121, 25, 137, 41], fill=(240, 180, 120))
        # Eyes
        d.ellipse([80, 50, 92, 62], fill=(40, 40, 40))
        d.ellipse([108, 50, 120, 62], fill=(40, 40, 40))
        # Nose
        d.ellipse([cx - 8, 70, cx + 8, 80], fill=(120, 60, 30))
        # Belly
        d.ellipse([75, 100, 125, 150], fill=(230, 180, 110))

    elif shape == "clock":
        d.ellipse([30, 30, 170, 170], fill=(240, 240, 240), outline=(80, 80, 80), width=3)
        # Tick marks
        for angle_deg in range(0, 360, 30):
            a = math.radians(angle_deg)
            x1 = int(cx + 68 * math.cos(a))
            y1 = int(100 + 68 * math.sin(a))
            x2 = int(cx + 78 * math.cos(a))
            y2 = int(100 + 78 * math.sin(a))
            d.line([x1, y1, x2, y2], fill=(80, 80, 80), width=2)
        # Hands
        d.line([cx, 100, cx - 20, 55], fill=(40, 40, 40), width=4)
        d.line([cx, 100, cx + 35, 115], fill=(40, 40, 40), width=3)
        d.ellipse([cx - 5, 95, cx + 5, 105], fill=(40, 40, 40))
        # "Alarm" legs
        d.line([60, 30, 40, 10], fill=(80, 80, 80), width=4)
        d.line([140, 30, 160, 10], fill=(80, 80, 80), width=4)
        d.ellipse([34, 4, 46, 16], fill=(80, 80, 80))
        d.ellipse([154, 4, 166, 16], fill=(80, 80, 80))

    elif shape == "bathtub":
        d.rounded_rectangle([20, 70, 180, 155], radius=30,
                             fill=(210, 240, 255), outline=(80, 80, 80), width=3)
        d.rectangle([20, 115, 180, 145], fill=(180, 220, 255), outline=(80, 80, 80), width=1)
        # Feet
        for fx in [45, 155]:
            d.rounded_rectangle([fx - 8, 150, fx + 8, 168], radius=4, fill=(180, 180, 180))
        # Faucet
        d.rectangle([cx - 6, 45, cx + 6, 75], fill=(160, 160, 160))
        d.ellipse([cx - 14, 38, cx + 14, 52], fill=(160, 160, 160))

    elif shape == "soap":
        d.rounded_rectangle([40, 60, 160, 140], radius=20,
                             fill=(255, 220, 255), outline=(200, 120, 200), width=3)
        # Bubbles
        for bx, by, br in [(80, 48, 10), (120, 42, 8), (100, 34, 6)]:
            d.ellipse([bx - br, by - br, bx + br, by + br],
                      fill=(200, 180, 255), outline=(180, 140, 220), width=2)

    elif shape == "toothbrush":
        d.rounded_rectangle([cx - 8, 20, cx + 8, 150], radius=6,
                             fill=(80, 180, 255), outline=(40, 120, 200), width=2)
        d.rounded_rectangle([cx - 14, 20, cx + 14, 55], radius=8,
                             fill=(200, 230, 255), outline=(40, 120, 200), width=2)
        for bx in [cx - 8, cx - 2, cx + 4, cx + 10]:
            d.rounded_rectangle([bx - 3, 22, bx + 3, 52], radius=3, fill=(255, 255, 255))

    elif shape == "towel":
        d.rounded_rectangle([25, 40, 175, 155], radius=8,
                             fill=(255, 160, 120), outline=(180, 80, 50), width=2)
        for x in range(30, 175, 20):
            d.line([x, 40, x, 155], fill=(255, 200, 180), width=2)
        d.rectangle([25, 40, 175, 60], fill=(180, 80, 50), outline=(180, 80, 50), width=1)

    elif shape == "mirror":
        d.rounded_rectangle([45, 20, 155, 155], radius=12,
                             fill=(200, 230, 255), outline=(120, 120, 120), width=4)
        # Reflection highlight
        d.line([65, 35, 65, 140], fill=(255, 255, 255), width=4)
        # Handle
        d.rounded_rectangle([cx - 8, 152, cx + 8, 178], radius=4, fill=(120, 120, 120))
        d.rounded_rectangle([cx - 16, 172, cx + 16, 180], radius=4, fill=(120, 120, 120))

    elif shape == "toilet":
        d.rounded_rectangle([45, 100, 155, 170], radius=10,
                             fill=(240, 240, 255), outline=(80, 80, 80), width=2)
        d.ellipse([35, 60, 165, 115], fill=(240, 240, 255), outline=(80, 80, 80), width=2)
        d.rounded_rectangle([55, 20, 145, 65], radius=6,
                             fill=(220, 220, 240), outline=(80, 80, 80), width=2)

    elif shape == "shampoo":
        d.rounded_rectangle([65, 50, 135, 165], radius=10,
                             fill=(180, 255, 180), outline=(80, 180, 80), width=2)
        # Pump
        d.rounded_rectangle([cx - 4, 20, cx + 4, 55], radius=3, fill=(80, 180, 80))
        d.ellipse([cx - 12, 14, cx + 12, 28], fill=(80, 180, 80))
        # Label stripe
        d.rectangle([65, 90, 135, 125], fill=(255, 255, 255), outline=(80, 180, 80), width=1)

    elif shape == "sofa":
        # Seat
        d.rounded_rectangle([15, 100, 185, 165], radius=10,
                             fill=(180, 120, 60), outline=(100, 60, 20), width=2)
        # Back
        d.rounded_rectangle([15, 55, 185, 108], radius=10,
                             fill=(200, 140, 80), outline=(100, 60, 20), width=2)
        # Arms
        for ax in [15, 155]:
            d.rounded_rectangle([ax, 80, ax + 30, 165], radius=8,
                                 fill=(160, 100, 40), outline=(100, 60, 20), width=2)
        # Cushions
        d.line([100, 108, 100, 165], fill=(100, 60, 20), width=2)

    elif shape == "tv":
        d.rounded_rectangle([20, 40, 180, 145], radius=8,
                             fill=(30, 30, 30), outline=(10, 10, 10), width=2)
        d.rounded_rectangle([28, 48, 172, 137], radius=4,
                             fill=(50, 180, 220), outline=(20, 20, 20), width=1)
        # Stand
        d.rectangle([cx - 15, 145, cx + 15, 160], fill=(60, 60, 60))
        d.rectangle([cx - 25, 158, cx + 25, 168], fill=(60, 60, 60))

    elif shape == "bookshelf":
        d.rounded_rectangle([20, 20, 180, 175], radius=4,
                             fill=(160, 120, 70), outline=(100, 70, 30), width=2)
        book_colors = [(255, 80, 80), (80, 160, 255), (255, 200, 60),
                       (100, 220, 100), (220, 80, 220)]
        for shelf_y in [40, 90, 140]:
            d.line([20, shelf_y, 180, shelf_y], fill=(100, 70, 30), width=2)
            bx = 25
            for col in book_colors:
                bw = 22
                d.rounded_rectangle([bx, shelf_y + 3, bx + bw - 2, shelf_y + 44],
                                     radius=2, fill=col, outline=(60, 60, 60), width=1)
                bx += bw + 3

    elif shape == "rug":
        d.rounded_rectangle([15, 55, 185, 155], radius=12,
                             fill=(200, 60, 60), outline=(140, 30, 30), width=3)
        d.rounded_rectangle([30, 70, 170, 140], radius=8,
                             fill=(240, 180, 60), outline=(140, 30, 30), width=2)
        for x in range(45, 170, 20):
            d.ellipse([x - 6, 90, x + 6, 106], fill=(200, 60, 60))

    elif shape == "remote":
        d.rounded_rectangle([70, 20, 130, 175], radius=15,
                             fill=(50, 50, 50), outline=(20, 20, 20), width=2)
        # Screen/indicator
        d.rounded_rectangle([80, 30, 120, 55], radius=4, fill=(30, 180, 30))
        # Buttons
        btn_colors = [(255, 80, 80), (80, 180, 255), (255, 220, 60), (100, 220, 100)]
        bx_list = [(85, 70), (110, 70), (85, 100), (110, 100)]
        for (bx, by), col in zip(bx_list, btn_colors):
            d.ellipse([bx, by, bx + 16, by + 16], fill=col, outline=(20, 20, 20), width=1)
        for y in [130, 148]:
            d.rounded_rectangle([80, y, 120, y + 14], radius=3, fill=(80, 80, 80))

    elif shape == "frame":
        d.rounded_rectangle([20, 20, 180, 175], radius=6,
                             fill=(160, 100, 40), outline=(100, 60, 20), width=6)
        d.rectangle([35, 35, 165, 160], fill=(200, 230, 255))
        # Simple landscape inside
        d.rectangle([35, 115, 165, 160], fill=(100, 200, 80))
        d.ellipse([60, 50, 140, 120], fill=(255, 220, 100))

    elif shape == "flower":
        petal_color = (255, 100, 180)
        for angle_deg in range(0, 360, 60):
            a = math.radians(angle_deg)
            px = int(cx + 32 * math.cos(a))
            py = int(95 + 32 * math.sin(a))
            d.ellipse([px - 18, py - 18, px + 18, py + 18], fill=petal_color)
        d.ellipse([cx - 20, 75, cx + 20, 115], fill=(255, 230, 50))
        d.line([cx, 115, cx, 170], fill=(60, 160, 60), width=5)
        d.line([cx, 148, cx - 20, 130], fill=(60, 160, 60), width=4)

    elif shape == "tree":
        d.rectangle([cx - 10, 130, cx + 10, 175], fill=(140, 90, 40))
        d.polygon([(cx, 20), (cx - 55, 100), (cx + 55, 100)], fill=(60, 180, 60))
        d.polygon([(cx, 45), (cx - 65, 130), (cx + 65, 130)], fill=(80, 200, 80))
        d.polygon([(cx, 70), (cx - 75, 155), (cx + 75, 155)], fill=(100, 220, 100))

    elif shape == "swing":
        # Rope posts
        d.line([40, 20, 40, 130], fill=(140, 100, 50), width=5)
        d.line([160, 20, 160, 130], fill=(140, 100, 50), width=5)
        d.line([40, 20, 160, 20], fill=(140, 100, 50), width=5)
        # Ropes
        d.line([60, 20, 70, 120], fill=(180, 140, 80), width=3)
        d.line([140, 20, 130, 120], fill=(180, 140, 80), width=3)
        # Seat
        d.rounded_rectangle([65, 115, 135, 135], radius=6,
                             fill=(180, 120, 60), outline=(100, 60, 20), width=2)
        # Ground line
        d.line([20, 165, 180, 165], fill=(100, 180, 60), width=4)

    elif shape == "watering_can":
        d.rounded_rectangle([40, 70, 150, 155], radius=10,
                             fill=(80, 160, 220), outline=(40, 100, 160), width=2)
        # Spout
        d.polygon([(150, 100), (185, 70), (185, 85), (150, 115)], fill=(80, 160, 220))
        # Holes in spout
        for hy in [72, 78, 84]:
            d.ellipse([182, hy, 188, hy + 5], fill=(40, 100, 160))
        # Handle
        d.arc([30, 75, 65, 115], start=270, end=90, fill=(40, 100, 160), width=5)
        # Water droplets
        for dx, dy in [(175, 55), (182, 48), (188, 58)]:
            d.ellipse([dx, dy, dx + 6, dy + 9], fill=(80, 160, 220))

    elif shape == "butterfly":
        wing_color = (255, 150, 50)
        spot_color = (255, 240, 100)
        # Wings
        d.ellipse([20, 40, 95, 120], fill=wing_color, outline=(180, 80, 20), width=2)
        d.ellipse([105, 40, 180, 120], fill=wing_color, outline=(180, 80, 20), width=2)
        d.ellipse([30, 100, 90, 155], fill=(255, 180, 80), outline=(180, 80, 20), width=2)
        d.ellipse([110, 100, 170, 155], fill=(255, 180, 80), outline=(180, 80, 20), width=2)
        # Spots
        for sx, sy in [(55, 70), (145, 70), (55, 125), (145, 125)]:
            d.ellipse([sx - 10, sy - 10, sx + 10, sy + 10], fill=spot_color)
        # Body
        d.rounded_rectangle([cx - 6, 40, cx + 6, 158], radius=4,
                             fill=(80, 40, 20), outline=(40, 20, 10), width=2)
        # Antennae
        d.line([cx - 2, 42, cx - 20, 20], fill=(80, 40, 20), width=2)
        d.line([cx + 2, 42, cx + 20, 20], fill=(80, 40, 20), width=2)
        d.ellipse([cx - 25, 14, cx - 15, 24], fill=(255, 150, 50))
        d.ellipse([cx + 15, 14, cx + 25, 24], fill=(255, 150, 50))

    elif shape == "grass":
        # Ground
        d.rectangle([0, 130, w, h], fill=(100, 200, 60))
        # Grass blades
        blade_color = (60, 160, 40)
        for gx in range(15, w - 10, 12):
            tip_x = gx + (4 if (gx % 24) < 12 else -4)
            d.polygon([(gx, 130), (gx - 5, 80), (tip_x, 60), (gx + 5, 80)],
                      fill=blade_color)

    else:
        # Generic coloured box with label
        d.rounded_rectangle([20, 20, 180, 170], radius=12,
                             fill=(200, 200, 200), outline=(80, 80, 80), width=2)
        lf = _font(22)
        _text_center(d, item_name[:10], 75, w, lf, color=(60, 60, 60))

    _lbl(item_name)
    img.save(str(out_path))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def get_family_image(member: dict) -> str:
    """Return the local file path for a family-member image (generate if absent)."""
    name_slug = member["name"].lower().replace(" ", "_")
    out_path = FAMILY_DIR / f"{name_slug}.png"
    if not out_path.exists():
        _make_family_image(member, out_path)
    return str(out_path)


def get_number_image(number_data: dict) -> str:
    """Return the local file path for a number image (generate if absent)."""
    out_path = NUMBERS_DIR / f"num_{number_data['number']}.png"
    if not out_path.exists():
        _make_number_image(
            number_data["number"], number_data["label"], number_data["bg"], out_path
        )
    return str(out_path)


def get_house_image(item: dict) -> str:
    """Return the local file path for a house-item image (generate if absent)."""
    name_slug = item["name"].lower().replace(" ", "_")
    out_path = HOUSE_DIR / f"{name_slug}.png"
    if not out_path.exists():
        _make_house_image(item["name"], item["shape"], out_path)
    return str(out_path)


def pregenerate_all(family_members, number_data_list, house_rooms):
    """Pre-generate every image needed by the exams."""
    print("  Generating family member images …")
    for m in family_members:
        get_family_image(m)

    print("  Generating number images …")
    for nd in number_data_list:
        get_number_image(nd)

    print("  Generating house item images …")
    for room_data in house_rooms.values():
        for item in room_data["items"]:
            get_house_image(item)

    print("  All images ready.")
