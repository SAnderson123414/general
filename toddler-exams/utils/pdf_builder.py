"""
pdf_builder.py
PDF generation utilities for toddler integrated studies exams.
Uses fpdf2.
"""

import math
import random
from pathlib import Path
from typing import Optional

from fpdf import FPDF

# ---------------------------------------------------------------------------
# Colour palette
# ---------------------------------------------------------------------------

PALETTE = {
    "bg_yellow":  (255, 253, 210),
    "bg_pink":    (255, 220, 235),
    "bg_blue":    (210, 235, 255),
    "bg_green":   (210, 255, 220),
    "bg_orange":  (255, 235, 210),
    "header":     (80,  50, 160),
    "star":       (255, 200, 0),
    "border":     (60,  100, 200),
    "dark_text":  (30,  30,  60),
    "light_text": (255, 255, 255),
    "correct":    (50, 180, 50),
    "box_line":   (120, 120, 200),
    "answer_box": (240, 240, 255),
    "smiley":     (255, 220, 50),
}

PAGE_BG_COLORS = [
    PALETTE["bg_yellow"],
    PALETTE["bg_pink"],
    PALETTE["bg_blue"],
    PALETTE["bg_green"],
    PALETTE["bg_orange"],
]

# Friendly fonts (FPDF built-ins)
FONT_BOLD   = "Helvetica"
FONT_NORMAL = "Helvetica"


class ExamPDF(FPDF):
    """Custom FPDF subclass with helpers for toddler exam layout."""

    def __init__(self, images_dir: Path, page_bg_idx: int = 0):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.images_dir = images_dir
        self.page_bg_idx = page_bg_idx
        self.set_auto_page_break(auto=True, margin=20)
        self._page_number = 0

    # ------------------------------------------------------------------
    # Page hooks
    # ------------------------------------------------------------------

    def header(self):
        pass  # handled per-page

    def footer(self):
        if self._page_number <= 0:
            return
        self.set_y(-15)
        self.set_font(FONT_BOLD, "B", 10)
        self.set_text_color(*PALETTE["header"])
        self.cell(0, 10, f"Page {self._page_number}", align="C")

    def add_page(self, *args, **kwargs):
        super().add_page(*args, **kwargs)
        self._page_number += 1
        self._draw_page_background()

    # ------------------------------------------------------------------
    # Background / decorative helpers
    # ------------------------------------------------------------------

    def _draw_page_background(self):
        bg = PAGE_BG_COLORS[self._page_number % len(PAGE_BG_COLORS)]
        self.set_fill_color(*bg)
        self.rect(0, 0, self.w, self.h, "F")
        self._draw_border()
        self._draw_corner_stars()

    def _draw_border(self):
        r, g, b = PALETTE["border"]
        self.set_draw_color(r, g, b)
        self.set_line_width(1.5)
        self.rect(5, 5, self.w - 10, self.h - 10)
        self.set_draw_color(255, 200, 50)
        self.set_line_width(0.8)
        self.rect(7, 7, self.w - 14, self.h - 14)

    def _draw_corner_stars(self):
        for x, y in [(10, 10), (self.w - 15, 10), (10, self.h - 15), (self.w - 15, self.h - 15)]:
            self._star(x, y, 4, PALETTE["star"])

    def _star(self, cx: float, cy: float, r: float, color: tuple):
        self.set_fill_color(*color)
        points = []
        for i in range(10):
            angle = math.pi / 2 + i * math.pi / 5
            radius = r if i % 2 == 0 else r / 2.5
            points.append((cx + radius * math.cos(angle), cy - radius * math.sin(angle)))
        # Use FPDF polygon-like approach via lines
        self.set_draw_color(*color)
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]
            self.line(x1, y1, x2, y2)

    def _smiley(self, cx: float, cy: float, r: float = 5):
        self.set_fill_color(*PALETTE["smiley"])
        self.ellipse(cx - r, cy - r, r * 2, r * 2, "FD")
        # Eyes
        self.set_fill_color(50, 50, 50)
        self.ellipse(cx - r * 0.35, cy - r * 0.2, r * 0.25, r * 0.25, "F")
        self.ellipse(cx + r * 0.1, cy - r * 0.2, r * 0.25, r * 0.25, "F")
        # Smile arc approximated by a line
        self.set_draw_color(50, 50, 50)
        self.set_line_width(0.6)
        self.arc(cx - r * 0.4, cy + r * 0.05, r * 0.8, r * 0.5, 0, 180)

    # ------------------------------------------------------------------
    # Layout building blocks
    # ------------------------------------------------------------------

    def section_header(self, text: str, y: Optional[float] = None):
        if y is not None:
            self.set_y(y)
        self.set_fill_color(*PALETTE["header"])
        self.set_text_color(*PALETTE["light_text"])
        self.set_font(FONT_BOLD, "B", 16)
        self.cell(0, 10, text, new_x="LMARGIN", new_y="NEXT", align="C", fill=True)
        self.ln(3)
        self.set_text_color(*PALETTE["dark_text"])

    def instruction(self, text: str):
        self.set_font(FONT_BOLD, "B", 14)
        self.set_text_color(*PALETTE["header"])
        self.multi_cell(0, 8, text, align="L")
        self.ln(2)
        self.set_text_color(*PALETTE["dark_text"])

    def answer_box(self, x: float, y: float, w: float, h: float, label: str = ""):
        self.set_fill_color(*PALETTE["answer_box"])
        self.set_draw_color(*PALETTE["box_line"])
        self.set_line_width(1.0)
        self.rect(x, y, w, h, "FD")
        if label:
            self.set_xy(x + 1, y + 1)
            self.set_font(FONT_NORMAL, "", 8)
            self.set_text_color(*PALETTE["header"])
            self.cell(w - 2, 4, label)

    def image_cell(self, img_path: Path, x: float, y: float,
                   w: float, h: float, label: str = ""):
        """Draw an image with an optional label beneath it inside a bordered box."""
        self.set_draw_color(*PALETTE["box_line"])
        self.set_line_width(0.8)
        # White background
        self.set_fill_color(255, 255, 255)
        self.rect(x, y, w, h + (6 if label else 0), "FD")
        try:
            self.image(str(img_path), x=x + 1, y=y + 1, w=w - 2, h=h - 2)
        except Exception:
            # Draw a placeholder if image fails
            self.set_fill_color(200, 200, 220)
            self.rect(x + 1, y + 1, w - 2, h - 2, "F")
        if label:
            self.set_font(FONT_BOLD, "B", 10)
            self.set_text_color(*PALETTE["dark_text"])
            self.set_xy(x, y + h)
            self.cell(w, 6, label.upper(), align="C")

    def circle_option(self, x: float, y: float, size: float):
        """Draw an empty circle for the child to colour/circle."""
        self.set_draw_color(*PALETTE["border"])
        self.set_line_width(1.5)
        self.ellipse(x, y, size, size)

    def dashed_line(self, x1: float, y1: float, x2: float, y2: float):
        """Draw a dashed line (for matching exercises)."""
        self.set_draw_color(180, 180, 200)
        self.set_line_width(0.5)
        dash_len = 3
        dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        steps = int(dist / (2 * dash_len))
        for i in range(steps):
            t1 = 2 * i * dash_len / dist
            t2 = (2 * i + 1) * dash_len / dist
            self.line(
                x1 + t1 * (x2 - x1), y1 + t1 * (y2 - y1),
                x1 + t2 * (x2 - x1), y1 + t2 * (y2 - y1),
            )

    # ------------------------------------------------------------------
    # Title page
    # ------------------------------------------------------------------

    def build_title_page(self, exam_name: str, exam_number: int, images_dir: Path):
        self.add_page()
        # Big colourful banner
        self.set_fill_color(*PALETTE["header"])
        self.rect(10, 10, self.w - 20, 40, "F")
        self.set_text_color(*PALETTE["light_text"])
        self.set_font(FONT_BOLD, "B", 26)
        self.set_xy(10, 18)
        self.cell(self.w - 20, 14, "INTEGRATED STUDIES", align="C")

        self.set_fill_color(*PALETTE["star"])
        self.rect(10, 50, self.w - 20, 20, "F")
        self.set_text_color(*PALETTE["dark_text"])
        self.set_font(FONT_BOLD, "B", 20)
        self.set_xy(10, 54)
        self.cell(self.w - 20, 12, exam_name.upper(), align="C")

        # Cute illustrations row
        self._draw_title_illustrations(images_dir, y=78)

        # Name field
        self.set_y(155)
        self.set_text_color(*PALETTE["dark_text"])
        self.set_font(FONT_BOLD, "B", 18)
        self.cell(0, 10, "Name: ________________________________", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)
        self.set_font(FONT_NORMAL, "", 14)
        self.cell(0, 8, "Date: _______________________   Class: _______________", align="C", new_x="LMARGIN", new_y="NEXT")

        # Stars row
        self.ln(8)
        star_x = 25
        for _ in range(8):
            self._star(star_x, self.get_y() + 4, 5, PALETTE["star"])
            star_x += 22

        # Smiley faces
        self.ln(10)
        for sx in [40, 80, 120, 160]:
            self._smiley(sx, self.get_y(), 6)

        # Footer note
        self.set_y(-30)
        self.set_font(FONT_NORMAL, "I", 10)
        self.set_text_color(*PALETTE["header"])
        self.cell(0, 6, "Fun Learning for Little Ones  *  Ages 2-4", align="C")

    def _draw_title_illustrations(self, images_dir: Path, y: float):
        from utils.exam_content import FAMILY_MEMBERS
        concepts = random.sample(FAMILY_MEMBERS[:6], 4)
        cell_w = 40
        gap = (self.w - 20 - 4 * cell_w) / 5
        x = 10 + gap
        for c in concepts:
            from utils.image_downloader import get_image_path
            img_path = get_image_path(c, images_dir)
            self.image_cell(img_path, x=x, y=y, w=cell_w, h=cell_w, label=c)
            x += cell_w + gap

    # ------------------------------------------------------------------
    # Section 1 – Family members
    # ------------------------------------------------------------------

    def build_circle_family(self, questions: list, images_dir: Path):
        from utils.image_downloader import get_image_path
        for q_text, correct, choices in questions:
            self.add_page()
            self.section_header("Section 1: Identify the Family Member")
            self.instruction(q_text)

            cell_w = 40
            cell_h = 45
            cols = 2
            gap_x = (self.w - 20 - cols * cell_w) / (cols + 1)
            gap_y = 5
            start_x = 10 + gap_x
            x = start_x
            y = self.get_y() + 4

            for idx, member in enumerate(choices):
                img_path = get_image_path(member, images_dir)
                self.image_cell(img_path, x=x, y=y, w=cell_w, h=cell_h, label=member)
                # Circle for ticking
                self.circle_option(x + cell_w - 10, y + 1, 8)
                x += cell_w + gap_x
                if (idx + 1) % cols == 0:
                    x = start_x
                    y += cell_h + gap_y

            # Smileys at bottom
            self.set_y(y + cell_h + 5)
            for sx in [60, 100, 140]:
                self._smiley(sx, self.get_y(), 5)

    def build_who_is_this(self, questions: list, images_dir: Path):
        from utils.image_downloader import get_image_path
        for correct, choices in [(q[1], q[2]) for q in questions]:
            self.add_page()
            self.section_header("Section 1: Who Is This?")
            self.instruction("Who is this?  Circle the correct answer.")

            img_path = get_image_path(correct, images_dir)
            img_x = (self.w - 60) / 2
            self.image_cell(img_path, x=img_x, y=self.get_y(), w=60, h=60)
            self.ln(65)

            self.set_font(FONT_BOLD, "B", 16)
            self.set_text_color(*PALETTE["dark_text"])
            cell_w = (self.w - 30) / len(choices)
            x = 15
            y = self.get_y() + 5
            for choice in choices:
                self.set_fill_color(255, 255, 255)
                self.set_draw_color(*PALETTE["box_line"])
                self.rect(x, y, cell_w - 2, 14, "FD")
                self.set_xy(x, y + 2)
                self.cell(cell_w - 2, 10, choice.upper(), align="C")
                x += cell_w

    def build_match_family(self, matching_set: list, images_dir: Path):
        from utils.image_downloader import get_image_path
        self.add_page()
        self.section_header("Section 1: Draw a Line to Match!")
        self.instruction("Draw a line from the picture to the correct name.")

        left_x = 15
        right_x = self.w - 55
        cell_w = 40
        cell_h = 38
        start_y = self.get_y() + 5
        gap_y = 8

        shuffled = list(matching_set)
        random.shuffle(shuffled)

        left_centers = []
        right_centers = []

        for i, (label, key) in enumerate(matching_set):
            y = start_y + i * (cell_h + gap_y)
            img_path = get_image_path(key, images_dir)
            self.image_cell(img_path, x=left_x, y=y, w=cell_w, h=cell_h)
            left_centers.append((left_x + cell_w, y + cell_h / 2))

        for i, (label, _) in enumerate(shuffled):
            y = start_y + i * (cell_h + gap_y)
            self.set_fill_color(220, 220, 255)
            self.set_draw_color(*PALETTE["box_line"])
            self.rect(right_x, y, cell_w, cell_h, "FD")
            self.set_font(FONT_BOLD, "B", 13)
            self.set_text_color(*PALETTE["dark_text"])
            self.set_xy(right_x, y + cell_h / 2 - 5)
            self.cell(cell_w, 10, label.upper(), align="C")
            right_centers.append((right_x, y + cell_h / 2))

        # Dashed guide lines
        for lc, rc in zip(left_centers, right_centers):
            self.dashed_line(lc[0] + 2, lc[1], rc[0] - 2, rc[1])

    def build_color_family(self, members: list, images_dir: Path):
        from utils.image_downloader import get_image_path
        self.add_page()
        self.section_header("Section 1: Color the Family Members!")
        self.instruction("Use your crayons to color each family member.")

        cell_w = 40
        gap = (self.w - 20 - len(members) * cell_w) / (len(members) + 1)
        x = 10 + gap
        y = self.get_y() + 5
        for m in members:
            img_path = get_image_path(m, images_dir)
            self.image_cell(img_path, x=x, y=y, w=cell_w, h=50, label=m)
            x += cell_w + gap

    # ------------------------------------------------------------------
    # Section 2 – Counting
    # ------------------------------------------------------------------

    def build_count_people(self, questions: list, images_dir: Path):
        from utils.image_downloader import get_image_path
        from utils.exam_content import FAMILY_MEMBERS
        for number, q_text in questions:
            self.add_page()
            self.section_header("Section 2: Count the Family Members!")
            self.instruction(q_text)

            # Draw 'number' stick figures
            figures_per_row = min(5, number)
            fig_w = 28
            fig_h = 35
            gap = 5
            total_w = figures_per_row * (fig_w + gap) - gap
            start_x = (self.w - total_w) / 2
            x = start_x
            y = self.get_y() + 5
            member = random.choice(FAMILY_MEMBERS[:6])
            img_path = get_image_path(member, images_dir)
            for i in range(number):
                self.image_cell(img_path, x=x, y=y, w=fig_w, h=fig_h)
                x += fig_w + gap
                if (i + 1) % figures_per_row == 0:
                    x = start_x
                    y += fig_h + gap

            # Answer choices (numbers)
            choices = list({number, (number % 10) + 1, max(1, number - 1), (number + 3) % 10 + 1})[:4]
            random.shuffle(choices)

            self.set_y(y + fig_h + 8)
            self.set_font(FONT_BOLD, "B", 22)
            self.instruction("How many? Circle the answer:")
            cell_w = 22
            x = (self.w - len(choices) * (cell_w + 6)) / 2
            y2 = self.get_y() + 2
            for ch in choices:
                self.set_fill_color(255, 255, 255)
                self.set_draw_color(*PALETTE["box_line"])
                self.rect(x, y2, cell_w, cell_w, "FD")
                self.set_font(FONT_BOLD, "B", 20)
                self.set_xy(x, y2 + 2)
                self.cell(cell_w, cell_w - 4, str(ch), align="C")
                self.circle_option(x - 1, y2 - 1, cell_w + 2)
                x += cell_w + 6

    def build_circle_group(self, questions: list, images_dir: Path):
        from utils.image_downloader import get_image_path
        from utils.exam_content import FAMILY_MEMBERS
        for correct, q_text, options in questions:
            self.add_page()
            self.section_header("Section 2: Circle the Correct Group!")
            self.instruction(q_text)

            cols = 2
            cell_w = 80
            cell_h = 55
            gap_x = (self.w - 20 - cols * cell_w) / (cols + 1)
            gap_y = 8
            start_x = 10 + gap_x
            x = start_x
            y = self.get_y() + 4
            member = random.choice(FAMILY_MEMBERS[:6])
            img_path = get_image_path(member, images_dir)
            for idx, count in enumerate(options):
                self._draw_group_cell(img_path, count, x, y, cell_w, cell_h)
                self.circle_option(x + cell_w - 10, y + 1, 8)
                x += cell_w + gap_x
                if (idx + 1) % cols == 0:
                    x = start_x
                    y += cell_h + gap_y

    def _draw_group_cell(self, img_path: Path, count: int, x: float, y: float,
                         w: float, h: float):
        self.set_fill_color(255, 255, 255)
        self.set_draw_color(*PALETTE["box_line"])
        self.rect(x, y, w, h, "FD")
        fig_w = min(14, (w - 4) / count)
        for i in range(count):
            fx = x + 2 + i * (fig_w + 1)
            try:
                self.image(str(img_path), x=fx, y=y + 4, w=fig_w, h=h - 12)
            except Exception:
                pass
        self.set_font(FONT_BOLD, "B", 11)
        self.set_xy(x, y + h - 8)
        self.cell(w, 7, f"{count} {'person' if count == 1 else 'people'}", align="C")

    def build_draw_line_numbers(self, pairs: list, images_dir: Path):
        from utils.image_downloader import get_image_path
        self.add_page()
        self.section_header("Section 2: Draw a Line!")
        self.instruction("Draw a line from the number to the correct group of people.")

        left_x = 15
        right_x = self.w - 55
        cell_w = 40
        cell_h = 38
        gap_y = 8
        start_y = self.get_y() + 5

        shuffled_pairs = list(pairs)
        random.shuffle(shuffled_pairs)

        from utils.exam_content import FAMILY_MEMBERS
        member = random.choice(FAMILY_MEMBERS[:4])
        img_path = get_image_path(member, images_dir)

        left_centers = []
        right_centers = []

        for i, (num, _) in enumerate(pairs):
            y = start_y + i * (cell_h + gap_y)
            num_path = get_image_path(str(num), images_dir)
            self.image_cell(num_path, x=left_x, y=y, w=cell_w, h=cell_h, label=f"Number {num}")
            left_centers.append((left_x + cell_w, y + cell_h / 2))

        for i, (num, _) in enumerate(shuffled_pairs):
            y = start_y + i * (cell_h + gap_y)
            self._draw_group_cell(img_path, num, right_x, y, cell_w, cell_h)
            right_centers.append((right_x, y + cell_h / 2))

        for lc, rc in zip(left_centers, right_centers):
            self.dashed_line(lc[0] + 2, lc[1], rc[0] - 2, rc[1])

    def build_count_write(self, questions: list, images_dir: Path):
        from utils.image_downloader import get_image_path
        from utils.exam_content import FAMILY_MEMBERS
        self.add_page()
        self.section_header("Section 2: Count and Write!")
        self.instruction("Count the people and write the number in the box.")

        member = random.choice(FAMILY_MEMBERS[:6])
        img_path = get_image_path(member, images_dir)

        row_h = 40
        y = self.get_y() + 5
        for number, _ in questions:
            fig_w = 20
            for i in range(number):
                fx = 15 + i * (fig_w + 2)
                try:
                    self.image(str(img_path), x=fx, y=y, w=fig_w, h=row_h - 5)
                except Exception:
                    pass
            # Write box
            self.answer_box(self.w - 35, y, 22, 22, "Write:")
            y += row_h + 5

    # ------------------------------------------------------------------
    # Section 3 – House items
    # ------------------------------------------------------------------

    def build_where_belongs(self, questions: list, images_dir: Path):
        from utils.image_downloader import get_image_path
        for item, correct_room, wrong_rooms in questions:
            self.add_page()
            self.section_header("Section 3: Where Does It Belong?")
            self.instruction(f'Where does the "{item.upper()}" belong?  Circle the correct room.')

            img_path = get_image_path(item, images_dir)
            cx = (self.w - 55) / 2
            self.image_cell(img_path, x=cx, y=self.get_y(), w=55, h=55, label=item)
            self.ln(60)

            rooms = [correct_room] + wrong_rooms[:3]
            random.shuffle(rooms)
            self.set_font(FONT_BOLD, "B", 14)
            cell_w = (self.w - 30) / len(rooms)
            x = 15
            y = self.get_y() + 5
            for room in rooms:
                color = (
                    (200, 255, 200) if room == correct_room
                    else (255, 255, 255)
                )
                self.set_fill_color(*color)
                self.set_draw_color(*PALETTE["box_line"])
                self.rect(x, y, cell_w - 3, 14, "FD")
                self.set_xy(x, y + 2)
                self.cell(cell_w - 3, 10, room, align="C")
                self.circle_option(x + (cell_w - 3) / 2 - 5, y + 14, 10)
                x += cell_w

    def build_circle_in_room(self, questions: list, images_dir: Path):
        from utils.image_downloader import get_image_path
        for room, correct_items, wrong_items in questions:
            self.add_page()
            self.section_header(f"Section 3: What's in the {room}?")
            self.instruction(f"Circle ALL the things you find in the {room.upper()}.")

            all_items = correct_items + wrong_items
            random.shuffle(all_items)
            cols = 3
            cell_w = 50
            cell_h = 50
            gap_x = (self.w - 20 - cols * cell_w) / (cols + 1)
            gap_y = 6
            x = 10 + gap_x
            y = self.get_y() + 4

            for idx, item in enumerate(all_items):
                img_path = get_image_path(item, images_dir)
                self.image_cell(img_path, x=x, y=y, w=cell_w, h=cell_h, label=item)
                self.circle_option(x + cell_w - 10, y + 1, 8)
                x += cell_w + gap_x
                if (idx + 1) % cols == 0:
                    x = 10 + gap_x
                    y += cell_h + gap_y

    def build_match_items(self, pairs: list, images_dir: Path):
        from utils.image_downloader import get_image_path
        self.add_page()
        self.section_header("Section 3: Draw a Line to Match!")
        self.instruction("Draw a line from the object to its room.")

        left_x = 15
        right_x = self.w - 55
        cell_w = 40
        cell_h = 40
        gap_y = 6
        start_y = self.get_y() + 5

        shuffled = list(pairs)
        random.shuffle(shuffled)

        left_centers = []
        right_centers = []

        for i, (item, room) in enumerate(pairs):
            y = start_y + i * (cell_h + gap_y)
            img_path = get_image_path(item, images_dir)
            self.image_cell(img_path, x=left_x, y=y, w=cell_w, h=cell_h, label=item)
            left_centers.append((left_x + cell_w, y + cell_h / 2))

        for i, (item, room) in enumerate(shuffled):
            y = start_y + i * (cell_h + gap_y)
            self.set_fill_color(220, 240, 255)
            self.set_draw_color(*PALETTE["box_line"])
            self.rect(right_x, y, cell_w, cell_h, "FD")
            self.set_font(FONT_BOLD, "B", 11)
            self.set_text_color(*PALETTE["dark_text"])
            self.set_xy(right_x, y + cell_h / 2 - 5)
            self.cell(cell_w, 10, room, align="C")
            right_centers.append((right_x, y + cell_h / 2))

        for lc, rc in zip(left_centers, right_centers):
            self.dashed_line(lc[0] + 2, lc[1], rc[0] - 2, rc[1])

    def build_whats_wrong(self, questions: list, images_dir: Path):
        from utils.image_downloader import get_image_path
        for room, items, wrong_item in questions:
            self.add_page()
            self.section_header("Section 3: What's Wrong?")
            self.instruction(
                f"One thing does NOT belong in the {room.upper()}.\n"
                "Circle the thing that is WRONG!"
            )

            cols = 2
            cell_w = 55
            cell_h = 55
            gap_x = (self.w - 20 - cols * cell_w) / (cols + 1)
            gap_y = 6
            x = 10 + gap_x
            y = self.get_y() + 5

            for idx, item in enumerate(items):
                img_path = get_image_path(item, images_dir)
                self.image_cell(img_path, x=x, y=y, w=cell_w, h=cell_h, label=item)
                self.circle_option(x + cell_w - 10, y + 1, 8)
                x += cell_w + gap_x
                if (idx + 1) % cols == 0:
                    x = 10 + gap_x
                    y += cell_h + gap_y
