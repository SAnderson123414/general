#!/usr/bin/env python3
"""
generate_exams.py

Main script for generating toddler-friendly Integrated Studies PDF exams.

Usage:
    python generate_exams.py               # generate 5 exams (default)
    python generate_exams.py --count 10    # generate 10 exams
"""

import argparse
import copy
import random
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Ensure project root is on sys.path when run directly
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parent))

from utils.exam_content import (
    FAMILY_MEMBERS,
    NUMBER_DATA,
    HOUSE_ROOMS,
    EXAMS,
)
from utils.image_downloader import (
    get_family_image,
    get_house_image,
    get_number_image,
    pregenerate_all,
)
from utils.pdf_builder import (
    ToddlerPDF,
    add_cover_page,
    add_circle_correct_page,
    add_who_is_this_page,
    add_matching_page,
    add_count_family_page,
    add_number_matching_page,
    add_write_number_page,
    add_where_belongs_page,
    add_circle_room_items_page,
    add_room_matching_page,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# Build lookup dictionaries for images
# ---------------------------------------------------------------------------

def build_image_maps():
    """Return dicts: family_images[name] -> path, house_images[name] -> path,
    number_images[n] -> path."""
    family_images = {}
    for m in FAMILY_MEMBERS:
        family_images[m["name"]] = get_family_image(m)

    house_images = {}
    for room_data in HOUSE_ROOMS.values():
        for item in room_data["items"]:
            house_images[item["name"]] = get_house_image(item)

    number_images = {}
    for nd in NUMBER_DATA:
        number_images[nd["number"]] = get_number_image(nd)

    return family_images, house_images, number_images


# ---------------------------------------------------------------------------
# Dispatch: render one question page
# ---------------------------------------------------------------------------

def render_page(pdf, page_data, section_title, section_num,
                family_images, house_images, number_images):
    ptype = page_data["type"]

    if ptype == "circle_correct":
        add_circle_correct_page(pdf, page_data, family_images, section_title, section_num)

    elif ptype == "who_is_this":
        add_who_is_this_page(pdf, page_data, family_images, section_title, section_num)

    elif ptype == "matching":
        add_matching_page(pdf, page_data, family_images, section_title, section_num)

    elif ptype == "count_family":
        add_count_family_page(pdf, page_data, family_images, section_title, section_num)

    elif ptype == "number_matching":
        add_number_matching_page(
            pdf, page_data, family_images, number_images, section_title, section_num
        )

    elif ptype == "write_number":
        add_write_number_page(pdf, page_data, family_images, section_title, section_num)

    elif ptype == "where_belongs":
        add_where_belongs_page(pdf, page_data, house_images, section_title, section_num)

    elif ptype == "circle_room_items":
        add_circle_room_items_page(pdf, page_data, house_images, section_title, section_num)

    elif ptype == "room_matching":
        add_room_matching_page(pdf, page_data, house_images, section_title, section_num)

    else:
        print(f"  [warn] Unknown page type: {ptype}")


# ---------------------------------------------------------------------------
# Generate one exam PDF
# ---------------------------------------------------------------------------

def generate_exam(exam_def: dict, exam_index: int,
                  family_images, house_images, number_images):
    """Generate a single PDF exam and return the output path."""
    exam_id     = exam_def["id"]
    title       = exam_def["title"]
    subtitle    = exam_def["subtitle"]
    cover_color = exam_def["cover_color"]
    filename    = exam_def["filename"]
    sections    = exam_def["sections"]

    print(f"  Building {filename} …")

    pdf = ToddlerPDF(exam_title=title, border_color_idx=exam_index)

    # ---- Cover page ----
    # Pick a few sample images for the cover
    cover_imgs = []
    all_family = list(family_images.values())
    random.shuffle(all_family)
    cover_imgs.extend(all_family[:2])
    all_house = list(house_images.values())
    random.shuffle(all_house)
    cover_imgs.extend(all_house[:1])
    cover_imgs = cover_imgs[:3]

    add_cover_page(pdf, title, subtitle, cover_color, cover_imgs)

    # ---- Section pages ----
    for section in sections:
        sec_num   = section["section_num"]
        sec_title = section["title"]
        pages     = section["pages"]

        for page_data in pages:
            render_page(
                pdf, page_data, sec_title, sec_num,
                family_images, house_images, number_images
            )

    out_path = OUTPUT_DIR / filename
    pdf.output(str(out_path))
    return out_path


# ---------------------------------------------------------------------------
# Extra exam generator (for --count > 5)
# ---------------------------------------------------------------------------

_EXTRA_MEMBERS   = ["Mom", "Dad", "Baby", "Brother", "Sister",
                    "Grandma", "Grandpa", "Uncle", "Aunt", "Cousin"]
_EXTRA_COUNTS    = list(range(1, 11))
_EXTRA_ITEMS     = {
    "Kitchen":     ["Stove", "Pot", "Cup"],
    "Bedroom":     ["Bed", "Lamp", "Teddy Bear"],
    "Bathroom":    ["Bathtub", "Soap", "Toothbrush"],
    "Living Room": ["Sofa", "TV", "Bookshelf"],
    "Garden":      ["Flowers", "Tree", "Butterfly"],
}
_WRONG_ITEMS_POOL = ["Fork", "Pillow", "Shampoo", "Remote Control", "Swing", "Blanket"]


def _make_extra_exam(exam_num: int):
    """Procedurally generate an extra exam definition for exam_num > 5."""
    rng = random.Random(exam_num)

    # Pick random members and questions
    target_member = rng.choice(_EXTRA_MEMBERS)
    other_members = [m for m in _EXTRA_MEMBERS if m != target_member]
    choices_4     = rng.sample(other_members, 3) + [target_member]
    rng.shuffle(choices_4)

    count = rng.randint(1, 10)
    num_choices = sorted(rng.sample(
        [n for n in _EXTRA_COUNTS if n != count][:6], 3
    ) + [count])

    room      = rng.choice(list(_EXTRA_ITEMS.keys()))
    room_item = rng.choice(_EXTRA_ITEMS[room])
    room_choices_other = rng.sample([r for r in _EXTRA_ITEMS if r != room], 3)
    room_choices = room_choices_other + [room]
    rng.shuffle(room_choices)

    matching_members = rng.sample(_EXTRA_MEMBERS, 4)
    room_pairs_rooms = rng.sample(list(_EXTRA_ITEMS.keys()), 4)
    room_pairs = [(rng.choice(_EXTRA_ITEMS[r]), r) for r in room_pairs_rooms]

    correct_items = _EXTRA_ITEMS[room][:3]
    wrong_items   = rng.sample(_WRONG_ITEMS_POOL, 3)

    cover_colors = [
        (255, 220, 200),
        (200, 255, 220),
        (220, 200, 255),
        (255, 255, 200),
        (200, 230, 255),
    ]
    cover_color = cover_colors[exam_num % len(cover_colors)]

    return {
        "id":          exam_num,
        "filename":    f"exam_{exam_num}_practice.pdf",
        "title":       f"Practice Exam {exam_num}!",
        "subtitle":    f"Integrated Studies – Exam {exam_num}",
        "cover_color": cover_color,
        "sections": [
            {
                "section_num": 1,
                "title": "Family Members",
                "pages": [
                    {
                        "type":        "circle_correct",
                        "instruction": f"Circle the {target_member}!",
                        "target":      target_member,
                        "choices":     choices_4,
                    },
                    {
                        "type":        "matching",
                        "instruction": "Draw a line to match the name to the picture!",
                        "pairs":       [(m, m) for m in matching_members],
                    },
                ],
            },
            {
                "section_num": 2,
                "title": "Count the Family",
                "pages": [
                    {
                        "type":        "count_family",
                        "instruction": "How many people do you see? Circle the number!",
                        "count":       count,
                        "member":      target_member,
                        "choices":     num_choices,
                    },
                ],
            },
            {
                "section_num": 3,
                "title": "House Items",
                "pages": [
                    {
                        "type":         "where_belongs",
                        "instruction":  "Where does this belong? Circle the correct room!",
                        "item":         room_item,
                        "correct_room": room,
                        "choices":      room_choices,
                    },
                    {
                        "type":          "circle_room_items",
                        "instruction":   f"Circle ALL the things you find in the {room}!",
                        "room":          room,
                        "correct_items": correct_items,
                        "wrong_items":   wrong_items,
                    },
                    {
                        "type":        "room_matching",
                        "instruction": "Draw a line to match each item to its room!",
                        "pairs":       room_pairs,
                    },
                ],
            },
        ],
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate toddler Integrated Studies PDF exams."
    )
    parser.add_argument(
        "--count", type=int, default=5,
        help="Number of exam PDFs to generate (default: 5)."
    )
    args = parser.parse_args()
    count = max(1, args.count)

    print("=" * 60)
    print("  Toddler Integrated Studies – PDF Exam Generator")
    print("=" * 60)

    # Step 1: Pre-generate / cache all images
    print("\n[Step 1] Preparing images …")
    pregenerate_all(FAMILY_MEMBERS, NUMBER_DATA, HOUSE_ROOMS)

    # Step 2: Build image lookup maps
    print("\n[Step 2] Building image maps …")
    family_images, house_images, number_images = build_image_maps()

    # Step 3: Generate PDFs
    print(f"\n[Step 3] Generating {count} exam PDF(s) into '{OUTPUT_DIR}/' …\n")

    generated = []
    for i in range(count):
        exam_num = i + 1
        if exam_num <= len(EXAMS):
            exam_def = EXAMS[exam_num - 1]
        else:
            exam_def = _make_extra_exam(exam_num)

        out_path = generate_exam(
            exam_def, i, family_images, house_images, number_images
        )
        generated.append(out_path)
        print(f"    ✅  {out_path.name}")

    print(f"\n[Done] {len(generated)} PDF exam(s) saved to '{OUTPUT_DIR}/'")
    print("=" * 60)


if __name__ == "__main__":
    main()
