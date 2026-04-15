"""
image_downloader.py
Downloads images from free/open-licensed internet sources.
Falls back to Pillow-generated illustrations when downloads fail.
"""

import os
import logging
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    requests = None  # type: ignore

from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Direct URLs for free/public-domain images
# (Wikimedia Commons CC0/PD images)
# ---------------------------------------------------------------------------

IMAGE_URLS: dict[str, str] = {
    # Family members – use Pillow-generated illustrations (reliable, age-appropriate)
    "mom":     "",
    "dad":     "",
    "grandma": "",
    "grandpa": "",
    "brother": "",
    "sister":  "",
    "baby":    "",
    "uncle":   "",
    "aunt":    "",
    "cousin":  "",
    # Numbers – Pillow-generated number cards
    **{str(n): "" for n in range(1, 11)},
    # House items – Kitchen
    "stove":        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/GasStove.jpg/320px-GasStove.jpg",
    "refrigerator": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/SMEG_refrigerator.jpg/320px-SMEG_refrigerator.jpg",
    "pot":          "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c1/Pot_of_soup.jpg/320px-Pot_of_soup.jpg",
    "pan":          "",
    "plate":        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/50/Dinner_plate_icon.svg/320px-Dinner_plate_icon.svg.png",
    "cup":          "https://upload.wikimedia.org/wikipedia/commons/thumb/4/45/A_small_cup_of_coffee.JPG/320px-A_small_cup_of_coffee.JPG",
    "spoon":        "",
    "fork":         "",
    # House items – Bedroom
    "bed":          "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Bed_in_a_Room.jpg/320px-Bed_in_a_Room.jpg",
    "pillow":       "",
    "blanket":      "",
    "lamp":         "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Floor_lamp.jpg/320px-Floor_lamp.jpg",
    "dresser":      "",
    "teddy bear":   "",
    "alarm clock":  "",
    # House items – Bathroom
    "bathtub":      "",
    "soap":         "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2a/Hand_soap.jpg/320px-Hand_soap.jpg",
    "toothbrush":   "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Toothbrush_with_toothpaste.jpg/320px-Toothbrush_with_toothpaste.jpg",
    "towel":        "",
    "mirror":       "",
    "toilet":       "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Toilet_raleigh_nc.jpg/320px-Toilet_raleigh_nc.jpg",
    "shampoo":      "",
    # House items – Living Room
    "sofa":         "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Sofa_chair.jpg/320px-Sofa_chair.jpg",
    "TV":           "",
    "bookshelf":    "https://upload.wikimedia.org/wikipedia/commons/thumb/7/71/Bookshelf_in_library.jpg/320px-Bookshelf_in_library.jpg",
    "rug":          "",
    "remote control": "",
    "picture frame":  "",
    # Garden
    "flowers":      "",
    "tree":         "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/24701-nature-natural-beauty.jpg/320px-24701-nature-natural-beauty.jpg",
    "swing":        "",
    "watering can": "",
    "butterfly":    "",
    "grass":        "",
}

# Fallback colors for each concept (used when drawing shapes)
FALLBACK_COLORS: dict[str, tuple] = {
    # Family – skin/clothing palette
    "mom":     (255, 192, 203),   # pink
    "dad":     (100, 149, 237),   # cornflower blue
    "grandma": (255, 218, 185),   # peach
    "grandpa": (144, 238, 144),   # light green
    "brother": (135, 206, 235),   # sky blue
    "sister":  (255, 160, 122),   # light salmon
    "baby":    (255, 255, 153),   # light yellow
    "uncle":   (173, 216, 230),   # light blue
    "aunt":    (255, 182, 193),   # light pink
    "cousin":  (152, 251, 152),   # pale green
    # Numbers
    **{str(n): (
        (255, int(255 * (1 - n / 10)), int(255 * n / 10))
    ) for n in range(1, 11)},
    # Rooms / items
    "stove":         (200, 200, 200),
    "refrigerator":  (220, 240, 255),
    "pot":           (180, 120, 80),
    "pan":           (160, 160, 160),
    "plate":         (255, 255, 255),
    "cup":           (255, 200, 100),
    "spoon":         (200, 180, 140),
    "fork":          (200, 180, 140),
    "bed":           (100, 180, 255),
    "pillow":        (255, 240, 220),
    "blanket":       (180, 140, 220),
    "lamp":          (255, 220, 100),
    "dresser":       (180, 140, 100),
    "teddy bear":    (210, 170, 110),
    "alarm clock":   (255, 100, 100),
    "bathtub":       (200, 230, 255),
    "soap":          (200, 255, 200),
    "toothbrush":    (100, 200, 255),
    "towel":         (255, 180, 100),
    "mirror":        (220, 240, 255),
    "toilet":        (240, 240, 240),
    "shampoo":       (255, 200, 220),
    "sofa":          (180, 140, 100),
    "TV":            (50, 50, 50),
    "bookshelf":     (160, 120, 80),
    "rug":           (200, 100, 100),
    "remote control": (80, 80, 80),
    "picture frame": (200, 180, 140),
    "flowers":       (255, 150, 200),
    "tree":          (80, 160, 80),
    "swing":         (200, 160, 120),
    "watering can":  (100, 180, 255),
    "butterfly":     (255, 150, 50),
    "grass":         (100, 200, 100),
}

IMG_SIZE = (200, 200)


def get_image_path(concept: str, images_dir: Path) -> Path:
    """
    Return a local path to an image for *concept*.
    Tries to download it; falls back to generating one with Pillow.
    """
    safe_name = concept.replace(" ", "_").replace("/", "_")
    subdir = _get_subdir(concept, images_dir)
    subdir.mkdir(parents=True, exist_ok=True)
    dest = subdir / f"{safe_name}.png"

    if dest.exists():
        return dest

    # Try downloading
    url = IMAGE_URLS.get(concept, "")
    if url:
        downloaded = _download_image(url, dest)
        if downloaded:
            return dest

    # Fall back to Pillow-generated illustration
    _generate_fallback(concept, dest)
    return dest


def _get_subdir(concept: str, images_dir: Path) -> Path:
    from utils.exam_content import FAMILY_MEMBERS, ROOMS
    if concept in FAMILY_MEMBERS:
        return images_dir / "family"
    room_items = {item for items in ROOMS.values() for item in items}
    if concept in room_items:
        return images_dir / "house"
    return images_dir / "numbers"


def _download_image(url: str, dest: Path) -> bool:
    if requests is None:
        return False
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "ToddlerExamBot/1.0"})
        if resp.status_code == 200 and len(resp.content) > 1000:
            dest.write_bytes(resp.content)
            # Validate and normalise
            img = Image.open(dest).convert("RGBA")
            img = img.resize(IMG_SIZE, Image.LANCZOS)
            img.save(dest)
            logger.info("Downloaded %s -> %s", url, dest)
            return True
    except Exception as exc:
        logger.debug("Download failed for %s: %s", url, exc)
    return False


# ---------------------------------------------------------------------------
# Pillow fallback drawing helpers
# ---------------------------------------------------------------------------

def _generate_fallback(concept: str, dest: Path) -> None:
    """Generate a recognisable coloured illustration for *concept*."""
    img = Image.new("RGBA", IMG_SIZE, (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)
    color = FALLBACK_COLORS.get(concept, (180, 180, 180))

    if concept in ("mom", "aunt", "grandma", "sister"):
        _draw_person(draw, color, female=True)
    elif concept in ("dad", "uncle", "grandpa", "brother", "cousin"):
        _draw_person(draw, color, female=False)
    elif concept == "baby":
        _draw_baby(draw, color)
    elif concept == "bed":
        _draw_bed(draw, color)
    elif concept == "bathtub":
        _draw_bathtub(draw, color)
    elif concept == "sofa":
        _draw_sofa(draw, color)
    elif concept == "stove":
        _draw_stove(draw, color)
    elif concept == "refrigerator":
        _draw_fridge(draw, color)
    elif concept == "TV":
        _draw_tv(draw, color)
    elif concept == "tree":
        _draw_tree(draw, color)
    elif concept == "flowers":
        _draw_flowers(draw, color)
    elif concept == "lamp":
        _draw_lamp(draw, color)
    elif concept == "toilet":
        _draw_toilet(draw, color)
    elif concept == "toothbrush":
        _draw_toothbrush(draw, color)
    elif concept == "swing":
        _draw_swing(draw, color)
    elif concept == "butterfly":
        _draw_butterfly(draw, color)
    elif concept == "bookshelf":
        _draw_bookshelf(draw, color)
    elif concept == "cup":
        _draw_cup(draw, color)
    elif concept == "pot":
        _draw_pot(draw, color)
    elif concept == "teddy bear":
        _draw_teddy(draw, color)
    elif concept.isdigit():
        _draw_number_card(draw, int(concept))
    else:
        _draw_generic(draw, concept, color)

    # Label at the bottom
    _add_label(draw, concept)
    img.save(dest)


# ---------------------------------------------------------------------------
# Drawing primitives
# ---------------------------------------------------------------------------

def _draw_person(draw: ImageDraw.ImageDraw, color: tuple, female: bool = False) -> None:
    w, h = IMG_SIZE
    # Body
    draw.rectangle([70, 90, 130, 160], fill=color, outline=(0, 0, 0), width=2)
    # Head
    draw.ellipse([75, 40, 125, 90], fill=(255, 220, 180), outline=(0, 0, 0), width=2)
    # Legs
    draw.rectangle([70, 160, 95, 185], fill=color, outline=(0, 0, 0), width=2)
    draw.rectangle([105, 160, 130, 185], fill=color, outline=(0, 0, 0), width=2)
    # Arms
    draw.rectangle([45, 95, 70, 120], fill=color, outline=(0, 0, 0), width=2)
    draw.rectangle([130, 95, 155, 120], fill=color, outline=(0, 0, 0), width=2)
    if female:
        # Skirt / dress triangle
        draw.polygon([(60, 155), (140, 155), (150, 185), (50, 185)], fill=color, outline=(0, 0, 0))
    # Smile
    draw.arc([85, 65, 115, 85], start=0, end=180, fill=(100, 60, 40), width=2)
    # Eyes
    draw.ellipse([88, 55, 96, 63], fill=(50, 50, 50))
    draw.ellipse([104, 55, 112, 63], fill=(50, 50, 50))


def _draw_baby(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.ellipse([65, 30, 135, 100], fill=(255, 220, 180), outline=(0, 0, 0), width=2)
    draw.rectangle([75, 100, 125, 150], fill=color, outline=(0, 0, 0), width=2)
    draw.arc([80, 65, 120, 90], start=0, end=180, fill=(100, 60, 40), width=2)
    draw.ellipse([83, 52, 93, 62], fill=(50, 50, 50))
    draw.ellipse([107, 52, 117, 62], fill=(50, 50, 50))
    # Tiny arms
    draw.rectangle([50, 105, 75, 120], fill=color, outline=(0, 0, 0), width=2)
    draw.rectangle([125, 105, 150, 120], fill=color, outline=(0, 0, 0), width=2)


def _draw_bed(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.rectangle([20, 100, 180, 170], fill=color, outline=(0, 0, 0), width=2)
    draw.rectangle([20, 80, 60, 110], fill=(220, 180, 140), outline=(0, 0, 0), width=2)
    draw.rectangle([20, 95, 180, 115], fill=(255, 255, 255), outline=(0, 0, 0), width=2)


def _draw_bathtub(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.rectangle([20, 80, 180, 160], fill=color, outline=(0, 0, 0), width=2)
    draw.ellipse([20, 120, 180, 180], fill=color, outline=(0, 0, 0), width=2)
    draw.rectangle([20, 145, 180, 165], fill=(180, 220, 255))
    draw.rectangle([85, 60, 95, 90], fill=(200, 200, 200), outline=(0, 0, 0), width=2)
    draw.rectangle([105, 60, 115, 90], fill=(200, 200, 200), outline=(0, 0, 0), width=2)


def _draw_sofa(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.rectangle([15, 100, 185, 160], fill=color, outline=(0, 0, 0), width=2)
    draw.rectangle([15, 80, 40, 160], fill=color, outline=(0, 0, 0), width=2)
    draw.rectangle([160, 80, 185, 160], fill=color, outline=(0, 0, 0), width=2)
    draw.rectangle([15, 80, 185, 115], fill=(min(color[0]+30, 255), min(color[1]+30, 255), min(color[2]+30, 255)), outline=(0, 0, 0), width=2)


def _draw_stove(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.rectangle([20, 50, 180, 170], fill=color, outline=(0, 0, 0), width=2)
    for cx, cy in [(65, 90), (135, 90), (65, 140), (135, 140)]:
        draw.ellipse([cx-20, cy-20, cx+20, cy+20], fill=(50, 50, 50), outline=(0, 0, 0), width=2)
        draw.ellipse([cx-10, cy-10, cx+10, cy+10], fill=(200, 100, 50))


def _draw_fridge(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.rectangle([40, 30, 160, 180], fill=color, outline=(0, 0, 0), width=2)
    draw.line([(40, 110), (160, 110)], fill=(0, 0, 0), width=3)
    draw.rectangle([145, 60, 155, 90], fill=(150, 150, 150))
    draw.rectangle([145, 125, 155, 155], fill=(150, 150, 150))


def _draw_tv(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.rectangle([20, 40, 180, 145], fill=color, outline=(0, 0, 0), width=2)
    draw.rectangle([30, 50, 170, 135], fill=(100, 180, 255))
    draw.rectangle([85, 145, 115, 170], fill=(100, 100, 100))
    draw.rectangle([60, 168, 140, 178], fill=(80, 80, 80))


def _draw_tree(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.rectangle([88, 140, 112, 185], fill=(160, 100, 60))
    draw.polygon([(100, 20), (30, 100), (170, 100)], fill=color, outline=(0, 0, 0))
    draw.polygon([(100, 40), (40, 110), (160, 110)], fill=(min(color[0]+20, 255), min(color[1]+20, 255), color[2]))


def _draw_flowers(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    for cx, cy in [(60, 100), (100, 80), (140, 100)]:
        for angle_offset, petal_color in [(0, color), (45, (255, 255, 100)), (90, color), (135, (255, 255, 100))]:
            import math
            rad = math.radians(angle_offset)
            px = int(cx + 22 * math.cos(rad))
            py = int(cy + 22 * math.sin(rad))
            draw.ellipse([px-10, py-10, px+10, py+10], fill=petal_color)
        draw.ellipse([cx-12, cy-12, cx+12, cy+12], fill=(255, 220, 50))
    draw.rectangle([55, 140, 65, 175], fill=(80, 160, 80))
    draw.rectangle([95, 155, 105, 175], fill=(80, 160, 80))
    draw.rectangle([135, 140, 145, 175], fill=(80, 160, 80))


def _draw_lamp(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.polygon([(100, 30), (60, 100), (140, 100)], fill=color, outline=(0, 0, 0))
    draw.rectangle([92, 100, 108, 170], fill=(180, 140, 100))
    draw.ellipse([70, 165, 130, 185], fill=(150, 120, 80))


def _draw_toilet(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.rectangle([60, 30, 140, 70], fill=color, outline=(0, 0, 0), width=2)
    draw.ellipse([30, 70, 170, 170], fill=color, outline=(0, 0, 0), width=2)
    draw.ellipse([50, 90, 150, 160], fill=(220, 240, 255))


def _draw_toothbrush(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.rectangle([88, 30, 112, 150], fill=(200, 200, 200), outline=(0, 0, 0), width=2)
    draw.rectangle([80, 30, 120, 70], fill=color, outline=(0, 0, 0), width=2)
    for x in range(84, 118, 6):
        draw.rectangle([x, 25, x+4, 38], fill=(255, 255, 255))


def _draw_swing(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.line([(30, 20), (30, 140)], fill=(160, 100, 60), width=5)
    draw.line([(170, 20), (170, 140)], fill=(160, 100, 60), width=5)
    draw.line([(30, 20), (170, 20)], fill=(160, 100, 60), width=5)
    draw.line([(70, 20), (70, 120)], fill=(120, 80, 40), width=3)
    draw.line([(130, 20), (130, 120)], fill=(120, 80, 40), width=3)
    draw.rectangle([60, 115, 140, 130], fill=color, outline=(0, 0, 0), width=2)
    _draw_person(draw, (255, 200, 150), female=False)


def _draw_butterfly(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.ellipse([20, 50, 95, 130], fill=color, outline=(0, 0, 0), width=2)
    draw.ellipse([105, 50, 180, 130], fill=(255, 200, 50), outline=(0, 0, 0), width=2)
    draw.ellipse([40, 120, 95, 170], fill=color, outline=(0, 0, 0), width=2)
    draw.ellipse([105, 120, 160, 170], fill=(255, 200, 50), outline=(0, 0, 0), width=2)
    draw.rectangle([95, 55, 105, 175], fill=(50, 50, 50))
    draw.line([(100, 55), (80, 30)], fill=(50, 50, 50), width=2)
    draw.line([(100, 55), (120, 30)], fill=(50, 50, 50), width=2)


def _draw_bookshelf(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.rectangle([15, 20, 185, 180], fill=color, outline=(0, 0, 0), width=2)
    for y in [65, 110, 155]:
        draw.line([(15, y), (185, y)], fill=(0, 0, 0), width=3)
    book_colors = [(255, 100, 100), (100, 200, 100), (100, 100, 255), (255, 200, 50), (200, 100, 200)]
    for shelf_y in [25, 70, 115]:
        x = 20
        for bc in book_colors:
            w = 28
            draw.rectangle([x, shelf_y, x+w, shelf_y+38], fill=bc, outline=(0, 0, 0), width=1)
            x += w + 2


def _draw_cup(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.rectangle([50, 60, 150, 160], fill=color, outline=(0, 0, 0), width=2)
    draw.arc([40, 90, 60, 140], start=270, end=90, fill=(0, 0, 0), width=3)
    draw.rectangle([50, 60, 150, 80], fill=(min(color[0]+40, 255), min(color[1]+40, 255), min(color[2]+40, 255)))


def _draw_pot(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.ellipse([30, 70, 170, 170], fill=color, outline=(0, 0, 0), width=2)
    draw.rectangle([30, 70, 170, 120], fill=color, outline=(0, 0, 0), width=2)
    draw.rectangle([15, 95, 40, 110], fill=(150, 150, 150), outline=(0, 0, 0), width=2)
    draw.rectangle([160, 95, 185, 110], fill=(150, 150, 150), outline=(0, 0, 0), width=2)
    draw.rectangle([80, 45, 120, 75], fill=(150, 150, 150), outline=(0, 0, 0), width=2)


def _draw_teddy(draw: ImageDraw.ImageDraw, color: tuple) -> None:
    draw.ellipse([55, 70, 145, 160], fill=color, outline=(0, 0, 0), width=2)
    draw.ellipse([65, 35, 135, 90], fill=color, outline=(0, 0, 0), width=2)
    draw.ellipse([48, 38, 80, 68], fill=color, outline=(0, 0, 0), width=2)
    draw.ellipse([120, 38, 152, 68], fill=color, outline=(0, 0, 0), width=2)
    draw.ellipse([30, 100, 65, 140], fill=color, outline=(0, 0, 0), width=2)
    draw.ellipse([135, 100, 170, 140], fill=color, outline=(0, 0, 0), width=2)
    draw.ellipse([82, 52, 98, 68], fill=(50, 30, 20))
    draw.ellipse([102, 52, 118, 68], fill=(50, 30, 20))
    draw.ellipse([88, 70, 112, 86], fill=(max(color[0]-30, 0), max(color[1]-30, 0), max(color[2]-30, 0)))
    draw.arc([88, 75, 112, 92], start=0, end=180, fill=(80, 40, 20), width=2)


def _draw_number_card(draw: ImageDraw.ImageDraw, number: int) -> None:
    colors = [
        (255, 100, 100), (100, 200, 100), (100, 100, 255),
        (255, 200, 50), (200, 100, 200), (50, 200, 200),
        (255, 150, 50), (150, 255, 50), (50, 150, 255), (255, 50, 150),
    ]
    bg = colors[(number - 1) % len(colors)]
    draw.rectangle([10, 10, 190, 165], fill=bg, outline=(0, 0, 0), width=3)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 120)
    except OSError:
        font = ImageFont.load_default()
    text = str(number)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((100 - tw // 2, 90 - th // 2), text, fill=(255, 255, 255), font=font)

    # Draw small figures matching the number
    figure_color = (255, 255, 255)
    positions = _figure_positions(number)
    for fx, fy in positions:
        draw.ellipse([fx-8, fy-8, fx+8, fy+8], fill=figure_color)
        draw.rectangle([fx-5, fy+8, fx+5, fy+20], fill=figure_color)


def _figure_positions(n: int) -> list:
    """Return (x, y) positions for n small figures in the bottom strip."""
    positions = []
    per_row = min(n, 5)
    rows = (n + per_row - 1) // per_row
    start_y = 170
    for row in range(rows):
        count = min(per_row, n - row * per_row)
        start_x = 100 - (count - 1) * 18
        for col in range(count):
            positions.append((start_x + col * 36, start_y))
        start_y += 30
    return positions


def _draw_generic(draw: ImageDraw.ImageDraw, concept: str, color: tuple) -> None:
    draw.rectangle([20, 30, 180, 160], fill=color, outline=(0, 0, 0), width=3)
    draw.ellipse([80, 50, 120, 90], fill=(255, 255, 255), outline=(0, 0, 0), width=2)


def _add_label(draw: ImageDraw.ImageDraw, text: str) -> None:
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except OSError:
        font = ImageFont.load_default()
    label = text.upper()
    bbox = draw.textbbox((0, 0), label, font=font)
    tw = bbox[2] - bbox[0]
    x = (IMG_SIZE[0] - tw) // 2
    draw.rectangle([0, 175, IMG_SIZE[0], IMG_SIZE[1]], fill=(50, 50, 80))
    draw.text((x, 177), label, fill=(255, 255, 255), font=font)


# ---------------------------------------------------------------------------
# Batch pre-download / pre-generate
# ---------------------------------------------------------------------------

def preload_images(concepts: list[str], images_dir: Path) -> dict[str, Path]:
    """Ensure all *concepts* have a local image; return mapping concept -> path."""
    return {c: get_image_path(c, images_dir) for c in concepts}
