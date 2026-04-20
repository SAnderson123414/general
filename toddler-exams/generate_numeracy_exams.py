#!/usr/bin/env python3
"""
Generate toddler numeracy exam PDFs with playful graphics.

Usage:
    python generate_numeracy_exams.py
"""

from pathlib import Path

from fpdf import FPDF

BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output" / "toddler_numeracy_exams"

NUMBER_NAMES = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
}


class NumeracyPDF(FPDF):
    def __init__(self):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.set_auto_page_break(auto=True, margin=12)

    def add_exam_page(self, title: str):
        self.add_page()
        self.set_fill_color(238, 248, 255)
        self.rect(0, 0, self.w, self.h, "F")
        self.set_fill_color(72, 94, 200)
        self.rect(10, 10, self.w - 20, 18, "F")
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 14)
        self.set_xy(10, 14)
        self.cell(self.w - 20, 10, title, align="C")
        self.set_text_color(30, 30, 40)
        self.set_font("Helvetica", "", 10)
        self.set_xy(12, 31)
        self.cell(0, 7, "Name: _____________________   Date: _____________________")

    def section_title(self, y: float, text: str):
        self.set_fill_color(255, 229, 173)
        self.rect(12, y, self.w - 24, 8, "F")
        self.set_text_color(35, 35, 45)
        self.set_font("Helvetica", "B", 11)
        self.set_xy(14, y + 1)
        self.cell(0, 6, text)

    def draw_ball(self, x: float, y: float, size: float = 7):
        self.set_fill_color(255, 120, 120)
        self.ellipse(x, y, size, size, "F")
        self.set_fill_color(120, 220, 120)
        self.ellipse(x + size * 0.35, y - 2, 2, 3, "F")

    def draw_dot_path(self, points: list[tuple[float, float]]):
        self.set_fill_color(95, 105, 160)
        for px, py in points:
            self.ellipse(px - 1, py - 1, 2, 2, "F")

    def draw_crescent(self, x: float, y: float, w: float, h: float):
        self.set_fill_color(145, 98, 210)
        self.ellipse(x, y, w, h, "F")
        self.set_fill_color(255, 255, 255)
        self.ellipse(x + w * 0.3, y + h * 0.05, w * 0.8, h * 0.9, "F")

    def draw_semicircle(self, x: float, y: float, w: float, h: float):
        self.set_fill_color(255, 170, 70)
        self.ellipse(x, y, w, h, "F")
        self.set_fill_color(255, 255, 255)
        self.rect(x - 0.5, y + (h / 2), w + 1, (h / 2) + 1, "F")
        self.arc(x, y, w, 0, 180, b=h)
        self.line(x, y + (h / 2), x + w, y + (h / 2))


def add_exam_1(pdf: NumeracyPDF):
    pdf.add_exam_page("Toddler Numeracy Exam 1")

    pdf.section_title(42, "A) Interpret the pictograph")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(14, 52)
    pdf.multi_cell(0, 5, "Count the balls in each row. Write the number in the box.")
    rows = [2, 4, 6]
    y = 60
    for count in rows:
        x = 20
        for _ in range(count):
            pdf.draw_ball(x, y, 7)
            x += 10
        pdf.rect(130, y - 1, 16, 10)
        y += 14

    pdf.section_title(105, "B) Match numbers 1-4 to number names")
    pdf.set_font("Helvetica", "B", 12)
    left_y = 115
    for idx, number in enumerate([1, 2, 3, 4]):
        y = left_y + idx * 11
        pdf.set_xy(20, y)
        pdf.cell(10, 7, str(number))
        pdf.line(31, y + 4, 95, y + 4)
    right_words = ["three", "one", "four", "two"]
    pdf.set_font("Helvetica", "", 11)
    for idx, word in enumerate(right_words):
        y = left_y + idx * 11
        pdf.set_xy(105, y)
        pdf.cell(0, 7, word.upper())

    pdf.section_title(166, "C) Identify lines and colours")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(14, 176)
    pdf.cell(0, 6, "Circle the curved line, straight line, and zigzag line:")
    pdf.set_draw_color(40, 40, 40)
    pdf.arc(20, 186, 30, 0, 180, b=8)
    pdf.line(70, 190, 110, 190)
    pdf.line(125, 194, 133, 186)
    pdf.line(133, 186, 141, 194)
    pdf.line(141, 194, 149, 186)
    pdf.line(149, 186, 157, 194)

    pdf.set_xy(14, 200)
    pdf.cell(0, 6, "Colour check: point to BLACK, BROWN, PINK, PURPLE.")
    swatches = [
        ((20, 20, 20), "BLACK"),
        ((139, 90, 43), "BROWN"),
        ((255, 105, 180), "PINK"),
        ((138, 43, 226), "PURPLE"),
    ]
    x = 18
    for color, label in swatches:
        pdf.set_fill_color(*color)
        pdf.rect(x, 208, 20, 12, "F")
        pdf.set_text_color(35, 35, 45)
        pdf.set_xy(x, 221)
        pdf.set_font("Helvetica", "B", 8)
        pdf.cell(20, 5, label, align="C")
        x += 26


def add_exam_2(pdf: NumeracyPDF):
    pdf.add_exam_page("Toddler Numeracy Exam 2")

    pdf.section_title(42, "A) Match numbers 5-8 to number names")
    pdf.set_font("Helvetica", "B", 12)
    left_y = 52
    for idx, number in enumerate([5, 6, 7, 8]):
        y = left_y + idx * 11
        pdf.set_xy(20, y)
        pdf.cell(10, 7, str(number))
        pdf.line(31, y + 4, 95, y + 4)
    right_words = ["eight", "five", "seven", "six"]
    pdf.set_font("Helvetica", "", 11)
    for idx, word in enumerate(right_words):
        y = left_y + idx * 11
        pdf.set_xy(105, y)
        pdf.cell(0, 7, word.upper())

    pdf.section_title(98, "B) Identify shapes: crescent and semi-circle")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(14, 108)
    pdf.cell(0, 6, "Circle the CRESCENT shape and the SEMI-CIRCLE shape.")
    pdf.draw_crescent(18, 118, 28, 18)
    pdf.draw_semicircle(58, 118, 28, 18)
    pdf.set_draw_color(80, 80, 80)
    pdf.ellipse(98, 118, 28, 18)
    pdf.rect(138, 118, 24, 18)

    pdf.section_title(145, "C) Read simple patterns")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(14, 155)
    pdf.cell(0, 6, "Say the pattern and draw the next shape in each box.")
    pattern_y = 164
    for row in range(2):
        x = 20
        shapes = ["circle", "square", "circle", "square"]
        if row == 1:
            shapes = ["triangle", "triangle", "circle", "triangle"]
        for shape in shapes:
            if shape == "circle":
                pdf.ellipse(x, pattern_y, 10, 10)
            elif shape == "square":
                pdf.rect(x, pattern_y, 10, 10)
            else:
                pdf.line(x + 5, pattern_y, x, pattern_y + 10)
                pdf.line(x + 5, pattern_y, x + 10, pattern_y + 10)
                pdf.line(x, pattern_y + 10, x + 10, pattern_y + 10)
            x += 14
        pdf.rect(x + 2, pattern_y - 1, 12, 12)
        pattern_y += 16

    pdf.section_title(204, "D) Non-numeral concepts: large/small and less/more")
    pdf.set_font("Helvetica", "", 9)
    pdf.set_xy(14, 214)
    pdf.cell(0, 5, "Circle the LARGE star and the SMALL star.")
    pdf.set_fill_color(255, 200, 70)
    pdf.ellipse(24, 221, 12, 12, "F")
    pdf.ellipse(46, 224, 6, 6, "F")
    pdf.set_xy(70, 214)
    pdf.cell(0, 5, "Which group has MORE dots?")
    for i in range(3):
        pdf.ellipse(72 + (i * 5), 222, 3, 3, "F")
    for i in range(6):
        pdf.ellipse(100 + ((i % 3) * 5), 220 + ((i // 3) * 5), 3, 3, "F")


def add_exam_3(pdf: NumeracyPDF):
    pdf.add_exam_page("Toddler Numeracy Exam 3")

    pdf.section_title(42, "A) Visual motor coordination: join broken lines/dots")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(14, 52)
    pdf.cell(0, 6, "Trace each path from START to END.")

    # Straight dotted line
    straight = [(22 + i * 6, 65) for i in range(20)]
    pdf.draw_dot_path(straight)
    pdf.set_xy(15, 60)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(10, 5, "S")
    pdf.set_xy(140, 60)
    pdf.cell(10, 5, "E")

    # Curved dotted line
    curve = [(22 + i * 6, 85 + (5 if i % 2 == 0 else -5)) for i in range(20)]
    pdf.draw_dot_path(curve)
    pdf.set_xy(15, 80)
    pdf.cell(10, 5, "S")
    pdf.set_xy(140, 80)
    pdf.cell(10, 5, "E")

    # Zigzag dotted line
    zigzag = [(22 + i * 6, 105 + (6 if i % 2 == 0 else -6)) for i in range(20)]
    pdf.draw_dot_path(zigzag)
    pdf.set_xy(15, 100)
    pdf.cell(10, 5, "S")
    pdf.set_xy(140, 100)
    pdf.cell(10, 5, "E")

    pdf.section_title(128, "B) Fill in the missing numerals from 1-10")
    pdf.set_font("Helvetica", "", 11)
    sequences = [
        ["1", "", "3", "4", "", "6", "7", "", "9", "10"],
        ["", "2", "3", "", "5", "6", "", "8", "9", ""],
    ]
    y = 139
    for row in sequences:
        x = 16
        for value in row:
            pdf.rect(x, y, 16, 12)
            if value:
                pdf.set_xy(x, y + 2)
                pdf.cell(16, 8, value, align="C")
            x += 18
        y += 18

    pdf.section_title(183, "C) Quick review: pictograph + pattern")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_xy(14, 193)
    pdf.cell(0, 6, "Count the stars and write the number.")
    for i in range(5):
        px = 24 + i * 14
        pdf.line(px, 206, px + 4, 216)
        pdf.line(px + 4, 216, px - 4, 210)
        pdf.line(px - 4, 210, px + 8, 210)
        pdf.line(px + 8, 210, px, 216)
        pdf.line(px, 216, px + 4, 206)
    pdf.rect(108, 205, 16, 10)

    pdf.set_xy(14, 220)
    pdf.cell(0, 6, "Pattern: red, blue, red, blue, ___")
    pdf.set_fill_color(230, 60, 60)
    pdf.ellipse(20, 228, 7, 7, "F")
    pdf.set_fill_color(70, 110, 235)
    pdf.ellipse(30, 228, 7, 7, "F")
    pdf.set_fill_color(230, 60, 60)
    pdf.ellipse(40, 228, 7, 7, "F")
    pdf.set_fill_color(70, 110, 235)
    pdf.ellipse(50, 228, 7, 7, "F")
    pdf.rect(64, 227, 11, 9)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    exams = [
        ("exam_1_numeracy_foundations.pdf", add_exam_1),
        ("exam_2_shapes_patterns_concepts.pdf", add_exam_2),
        ("exam_3_tracing_and_missing_numbers.pdf", add_exam_3),
    ]

    for filename, builder in exams:
        pdf = NumeracyPDF()
        builder(pdf)
        pdf.output(str(OUTPUT_DIR / filename))

    print(f"Saved numeracy exams to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
