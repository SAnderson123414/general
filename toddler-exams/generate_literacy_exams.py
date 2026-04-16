#!/usr/bin/env python3
"""
Generate toddler literacy exam PDFs with real picture-based prompts.

Usage:
    python generate_literacy_exams.py
"""

from pathlib import Path

from fpdf import FPDF

from utils.image_downloader import IMAGE_URLS, get_image_path, preload_images

BASE_DIR = Path(__file__).parent
IMAGES_DIR = BASE_DIR / "images"
OUTPUT_DIR = BASE_DIR / "output" / "toddler_literacy_exams"

LETTER_PICTURE_PAIRS = [
    ("Ff", "fish"),
    ("Ll", "leaf"),
    ("Gg", "goat"),
    ("Oo", "orange"),
    ("Uu", "umbrella"),
    ("Dd", "dog"),
]

WORD_FAMILY_ROWS = [
    ("-at", ["cat", "rat"]),
    ("-am", ["ham", "jam"]),
    ("-an", ["can", "fan"]),
]


class LiteracyPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=15)

    def add_toddler_page(self, title: str):
        self.add_page()
        self.set_fill_color(235, 246, 255)
        self.rect(0, 0, self.w, self.h, "F")
        self.set_fill_color(83, 109, 254)
        self.rect(10, 10, self.w - 20, 20, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 15)
        self.set_xy(10, 14)
        self.cell(self.w - 20, 10, title, align="C")
        self.set_text_color(30, 30, 40)
        self.set_font("Helvetica", "", 11)
        self.set_xy(12, 34)
        self.cell(0, 8, "Name: _____________________    Date: _____________________")

    def picture_card(self, x: float, y: float, w: float, h: float, concept: str, label: str = ""):
        img_path = get_image_path(concept, IMAGES_DIR)
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(145, 160, 200)
        self.rect(x, y, w, h, "FD")
        self.image(str(img_path), x=x + 2, y=y + 2, w=w - 4, h=h - 12)
        if label:
            self.set_font("Helvetica", "B", 11)
            self.set_xy(x, y + h - 9)
            self.cell(w, 7, label, align="C")

    def add_image_credits_page(self, concepts: list[str]):
        self.add_page()
        self.set_fill_color(255, 255, 255)
        self.rect(0, 0, self.w, self.h, "F")
        self.set_text_color(20, 20, 30)
        self.set_font("Helvetica", "B", 14)
        self.set_xy(12, 14)
        self.cell(0, 9, "Image Credits")
        self.set_font("Helvetica", "", 10)
        self.set_xy(12, 24)
        self.multi_cell(
            0,
            5,
            "Literacy exam images use free sources, including OpenMoji "
            "(CC BY-SA 4.0) and Wikimedia Commons (openly licensed).",
        )
        self.set_font("Helvetica", "", 8)
        y = 36
        for concept in sorted(set(concepts)):
            url = IMAGE_URLS.get(concept, "")
            if not url:
                continue
            self.set_xy(12, y)
            self.multi_cell(0, 4, f"{concept}: {url}")
            y = self.get_y() + 1
            if y > self.h - 15:
                self.add_page()
                y = 15


def build_exam_1():
    pdf = LiteracyPDF()
    pdf.add_toddler_page("Toddler Literacy Exam 1: Letter Sounds with Pictures")

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_xy(12, 45)
    pdf.cell(0, 8, "A) Say the letter and picture word together.")

    x = 12
    y = 55
    card_w = 30
    card_h = 42
    gap = 3
    for letter, word in LETTER_PICTURE_PAIRS:
        pdf.picture_card(x, y, card_w, card_h, word, letter)
        x += card_w + gap

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_xy(12, 105)
    pdf.cell(0, 8, "B) Circle the correct first letter for each picture.")

    start_x = 12
    start_y = 113
    col_gap = 64
    row_gap = 62
    for idx, (_, word) in enumerate(LETTER_PICTURE_PAIRS):
        col = idx % 3
        row = idx // 3
        x = start_x + col * col_gap
        y = start_y + row * row_gap
        pdf.picture_card(x, y, 42, 34, word)
        correct = word[0].upper()
        options = [f"{correct}{correct.lower()}", "Aa", "Mm"]
        if correct in ("A", "M"):
            options[2] = "Zz"
        option_x = x
        option_y = y + 37
        for opt in options:
            pdf.set_fill_color(255, 255, 255)
            pdf.rect(option_x, option_y, 12, 10, "FD")
            pdf.set_xy(option_x, option_y + 1)
            pdf.set_font("Helvetica", "B", 9)
            pdf.cell(12, 8, opt, align="C")
            option_x += 14

    pdf.add_image_credits_page([word for _, word in LETTER_PICTURE_PAIRS])
    pdf.output(str(OUTPUT_DIR / "exam_1_letter_recognition_and_sound.pdf"))


def build_exam_2():
    pdf = LiteracyPDF()
    pdf.add_toddler_page("Toddler Literacy Exam 2: Word Family Review")

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_xy(12, 45)
    pdf.cell(0, 8, "A) Look, point, and say each picture word.")

    y = 55
    for ending, words in WORD_FAMILY_ROWS:
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_xy(12, y + 12)
        pdf.cell(16, 8, ending)
        x = 30
        for word in words:
            pdf.picture_card(x, y, 46, 32, word, word.upper())
            x += 52
        y += 38

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_xy(12, 171)
    pdf.cell(0, 8, "B) Trace and read these easy sight words:")
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_xy(12, 180)
    pdf.cell(0, 8, "a   I   the   see   can   go")
    pdf.set_font("Helvetica", "", 11)
    pdf.set_xy(12, 191)
    pdf.cell(0, 7, "Review tip: adult says word first, toddler repeats.")
    pdf.add_image_credits_page([word for _, words in WORD_FAMILY_ROWS for word in words])
    pdf.output(str(OUTPUT_DIR / "exam_2_word_endings_and_sight_words.pdf"))


def build_exam_3():
    pdf = LiteracyPDF()
    pdf.add_toddler_page("Toddler Literacy Exam 3: Match Picture to First Letter")

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_xy(12, 45)
    pdf.cell(0, 8, "Draw a line from each picture to its first letter.")

    left_x = 14
    right_x = 150
    y = 58
    row_h = 30
    left_points = []
    right_points = []

    letters = [letter for letter, _ in LETTER_PICTURE_PAIRS]
    for idx, (_, word) in enumerate(LETTER_PICTURE_PAIRS):
        row_y = y + idx * row_h
        pdf.picture_card(left_x, row_y, 48, 24, word, word.upper())
        left_points.append((left_x + 48, row_y + 12))

    for idx, letter in enumerate(letters):
        row_y = y + idx * row_h + 6
        pdf.set_fill_color(255, 255, 255)
        pdf.rect(right_x, row_y, 24, 14, "FD")
        pdf.set_xy(right_x, row_y + 3)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(24, 8, letter, align="C")
        right_points.append((right_x, row_y + 7))

    pdf.set_font("Helvetica", "", 11)
    pdf.set_xy(12, 245)
    pdf.cell(0, 7, "Bonus review: say each first sound out loud with an adult.")
    pdf.add_image_credits_page([word for _, word in LETTER_PICTURE_PAIRS])
    pdf.output(str(OUTPUT_DIR / "exam_3_picture_initial_letter_match.pdf"))


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (IMAGES_DIR / "literacy").mkdir(parents=True, exist_ok=True)

    concepts = [word for _, word in LETTER_PICTURE_PAIRS]
    for _, words in WORD_FAMILY_ROWS:
        concepts.extend(words)

    for concept in concepts:
        safe_name = concept.replace(" ", "_").replace("/", "_")
        cached = IMAGES_DIR / "literacy" / f"{safe_name}.png"
        cached.unlink(missing_ok=True)

    preload_images(concepts, IMAGES_DIR)

    build_exam_1()
    build_exam_2()
    build_exam_3()
    print(f"Saved literacy exams to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
