#!/usr/bin/env python3
"""
generate_exams.py
Main entry point for the Toddler Integrated Studies PDF Exam Generator.

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
# Paths
# ---------------------------------------------------------------------------

BASE_DIR    = Path(__file__).parent
IMAGES_DIR  = BASE_DIR / "images"
OUTPUT_DIR  = BASE_DIR / "output"


def ensure_dirs():
    for d in [IMAGES_DIR / "family", IMAGES_DIR / "house", IMAGES_DIR / "numbers", OUTPUT_DIR]:
        d.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Pre-load all images that might be needed
# ---------------------------------------------------------------------------

def preload_all_images():
    from utils.exam_content import FAMILY_MEMBERS, ROOMS
    from utils.image_downloader import preload_images

    concepts = list(FAMILY_MEMBERS)
    for items in ROOMS.values():
        concepts.extend(items)
    for n in range(1, 11):
        concepts.append(str(n))

    print("  Preparing images (downloading from internet or generating locally)…")
    paths = preload_images(concepts, IMAGES_DIR)
    print(f"  ✓ {len(paths)} images ready.")
    return paths


# ---------------------------------------------------------------------------
# Build a single exam PDF
# ---------------------------------------------------------------------------

def build_exam(exam_def: dict, output_path: Path):
    from utils.pdf_builder import ExamPDF

    pdf = ExamPDF(images_dir=IMAGES_DIR)

    for section in exam_def["sections"]:
        stype = section["type"]

        if stype == "title_page":
            pdf.build_title_page(
                exam_name=section["exam_name"],
                exam_number=section["exam_number"],
                images_dir=IMAGES_DIR,
            )

        # --- Section 1 ---
        elif stype == "circle_family":
            pdf.build_circle_family(section["questions"], IMAGES_DIR)

        elif stype == "who_is_this":
            pdf.build_who_is_this(section["questions"], IMAGES_DIR)

        elif stype == "match_family":
            from utils.exam_content import FAMILY_MATCHING_SETS
            idx = section.get("set_index", 0) % len(FAMILY_MATCHING_SETS)
            pdf.build_match_family(FAMILY_MATCHING_SETS[idx], IMAGES_DIR)

        elif stype == "color_family":
            pdf.build_color_family(section["members"], IMAGES_DIR)

        # --- Section 2 ---
        elif stype == "count_people":
            pdf.build_count_people(section["questions"], IMAGES_DIR)

        elif stype == "circle_group":
            pdf.build_circle_group(section["questions"], IMAGES_DIR)

        elif stype == "draw_line_numbers":
            pdf.build_draw_line_numbers(section["pairs"], IMAGES_DIR)

        elif stype == "count_write":
            pdf.build_count_write(section["questions"], IMAGES_DIR)

        # --- Section 3 ---
        elif stype == "where_belongs":
            pdf.build_where_belongs(section["questions"], IMAGES_DIR)

        elif stype == "circle_in_room":
            pdf.build_circle_in_room(section["questions"], IMAGES_DIR)

        elif stype == "match_items":
            pdf.build_match_items(section["pairs"], IMAGES_DIR)

        elif stype == "whats_wrong":
            pdf.build_whats_wrong(section["questions"], IMAGES_DIR)

        else:
            print(f"    WARNING: unknown section type '{stype}' — skipped.")

    pdf.output(str(output_path))


# ---------------------------------------------------------------------------
# Extra exam generation (when --count > 5)
# ---------------------------------------------------------------------------

def generate_extra_exam(exam_number: int) -> dict:
    """Create an extra exam definition by sampling from the full content pool."""
    from utils.exam_content import (
        EXTRA_EXAM_TEMPLATE, FAMILY_CIRCLE_QUESTIONS,
        FAMILY_WHO_QUESTIONS, FAMILY_MATCHING_SETS,
        COUNTING_QUESTIONS, CIRCLE_GROUP_QUESTIONS,
        WHERE_BELONGS_QUESTIONS, CIRCLE_IN_ROOM_QUESTIONS,
        WHATS_WRONG_QUESTIONS,
    )

    names = [
        "Family Fun", "Number Time", "Around the House",
        "Let's Count", "Room Explorers", "Meet My Family",
        "House Hunt", "Count with Me", "Family Day",
        "Home Sweet Home",
    ]
    name = names[(exam_number - 6) % len(names)]

    # Randomly sample 4-5 section types
    pool = [
        {"type": "circle_family",
         "questions": random.sample(FAMILY_CIRCLE_QUESTIONS, min(3, len(FAMILY_CIRCLE_QUESTIONS)))},
        {"type": "who_is_this",
         "questions": random.sample(FAMILY_WHO_QUESTIONS, min(2, len(FAMILY_WHO_QUESTIONS)))},
        {"type": "match_family", "set_index": random.randint(0, len(FAMILY_MATCHING_SETS) - 1)},
        {"type": "count_people",
         "questions": random.sample(COUNTING_QUESTIONS, min(3, len(COUNTING_QUESTIONS)))},
        {"type": "circle_group",
         "questions": random.sample(CIRCLE_GROUP_QUESTIONS, min(3, len(CIRCLE_GROUP_QUESTIONS)))},
        {"type": "draw_line_numbers",
         "pairs": list(zip(range(1, 6), range(1, 6)))},
        {"type": "count_write",
         "questions": random.sample(COUNTING_QUESTIONS, min(3, len(COUNTING_QUESTIONS)))},
        {"type": "where_belongs",
         "questions": random.sample(WHERE_BELONGS_QUESTIONS, min(3, len(WHERE_BELONGS_QUESTIONS)))},
        {"type": "circle_in_room",
         "questions": random.sample(CIRCLE_IN_ROOM_QUESTIONS, min(2, len(CIRCLE_IN_ROOM_QUESTIONS)))},
        {"type": "match_items",
         "pairs": [(p[0], p[1]) for p in random.sample(WHERE_BELONGS_QUESTIONS, 4)]},
        {"type": "whats_wrong",
         "questions": random.sample(WHATS_WRONG_QUESTIONS, min(2, len(WHATS_WRONG_QUESTIONS)))},
    ]

    selected = random.sample(pool, min(5, len(pool)))

    return {
        "title": f"Exam {exam_number}: {name}",
        "filename": f"exam_{exam_number}_{name.lower().replace(' ', '_')}.pdf",
        "sections": [
            {"type": "title_page", "exam_name": f"{name} Exam", "exam_number": exam_number},
            *selected,
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
        help="Number of exam PDFs to generate (default: 5)"
    )
    args = parser.parse_args()

    if args.count < 1:
        print("ERROR: --count must be at least 1.")
        sys.exit(1)

    print("=" * 60)
    print("  Toddler Integrated Studies Exam Generator")
    print("=" * 60)

    ensure_dirs()
    preload_all_images()

    from utils.exam_content import EXAM_DEFINITIONS

    print(f"\nGenerating {args.count} exam(s)…\n")

    for i in range(args.count):
        exam_number = i + 1

        if i < len(EXAM_DEFINITIONS):
            exam_def = EXAM_DEFINITIONS[i]
        else:
            exam_def = generate_extra_exam(exam_number)

        filename = exam_def["filename"]
        output_path = OUTPUT_DIR / filename

        print(f"  [{exam_number}/{args.count}] {exam_def['title']} → {filename}")

        try:
            build_exam(exam_def, output_path)
            print(f"         ✓ Saved: output/{filename}")
        except Exception as exc:
            print(f"         ✗ ERROR generating {filename}: {exc}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 60)
    print(f"  Done!  {args.count} exam(s) saved in:  {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
