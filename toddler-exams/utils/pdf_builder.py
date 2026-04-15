"""
pdf_builder.py

Low-level helpers and high-level page builders for the toddler exam PDFs.
Uses fpdf2 for PDF generation.
"""

import math
import random
from pathlib import Path
from fpdf import FPDF

# ---------------------------------------------------------------------------
# Colours (R, G, B) tuples used throughout
# ---------------------------------------------------------------------------
WHITE       = (255, 255, 255)
BLACK       = (20,  20,  20)
DARK_GREY   = (80,  80,  80)
STAR_YELLOW = (255, 220, 0)
STAR_ORANGE = (255, 140, 0)
SMILE_YELLOW= (255, 200, 0)
BORDER_COLORS = [
    (255, 100, 100),
    (100, 180, 255),
    (100, 220, 100),
    (255, 180, 50),
    (220, 100, 255),
]

# A4 page in mm
PAGE_W = 210
PAGE_H = 297
MARGIN = 15

# ---------------------------------------------------------------------------
# Helper: font loader
# ---------------------------------------------------------------------------
_FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
]
_FONT_PATH = None
for _p in _FONT_PATHS:
    if Path(_p).exists():
        _FONT_PATH = _p
        break


# ---------------------------------------------------------------------------
# Base PDF class with extra helpers
# ---------------------------------------------------------------------------
class ToddlerPDF(FPDF):
    """FPDF subclass with toddler-exam helpers."""

    def __init__(self, exam_title: str, border_color_idx: int = 0):
        super().__init__(orientation="P", unit="mm", format="A4")
        self.exam_title = exam_title
        self.border_color = BORDER_COLORS[border_color_idx % len(BORDER_COLORS)]
        self._page_color = WHITE
        self._setup_fonts()
        self.set_auto_page_break(auto=True, margin=MARGIN + 5)

    def _setup_fonts(self):
        if _FONT_PATH:
            self.add_font("Toddler", "", _FONT_PATH)
            self.add_font("Toddler", "B", _FONT_PATH)
            self._font_name = "Toddler"
        else:
            self._font_name = "Helvetica"

    def tf(self, size: int, bold: bool = False):
        """Set the toddler font at the given size."""
        style = "B" if (bold or self._font_name == "Toddler") else ""
        self.set_font(self._font_name, style=style, size=size)

    # ------------------------------------------------------------------
    # Decorative helpers
    # ------------------------------------------------------------------
    def draw_star(self, x, y, r, color=STAR_YELLOW):
        """Draw a filled 5-pointed star centred at (x, y) with outer radius r."""
        points = []
        for i in range(10):
            angle = math.radians(i * 36 - 90)
            radius = r if i % 2 == 0 else r * 0.42
            points.append((x + radius * math.cos(angle), y + radius * math.sin(angle)))
        self.set_fill_color(*color)
        self.set_draw_color(*STAR_ORANGE)
        self.polygon(points, style="DF")

    def draw_smiley(self, x, y, r):
        """Draw a simple smiley face centred at (x, y) with radius r."""
        self.set_fill_color(*SMILE_YELLOW)
        self.set_draw_color(*DARK_GREY)
        self.circle(x, y, r, style="DF")
        # Eyes
        eye_r = r * 0.15
        self.set_fill_color(*BLACK)
        self.circle(x - r * 0.35, y - r * 0.2, eye_r, style="F")
        self.circle(x + r * 0.35, y - r * 0.2, eye_r, style="F")
        # Smile arc (approximated as a polyline)
        self.set_draw_color(180, 80, 0)
        self.set_line_width(0.8)
        pts = []
        for deg in range(200, 341, 10):
            a = math.radians(deg)
            pts.append((x + r * 0.55 * math.cos(a), y + r * 0.55 * math.sin(a)))
        for i in range(len(pts) - 1):
            self.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1])

    def draw_colored_border(self):
        """Draw a fun multi-coloured dotted border around the page."""
        r, g, b = self.border_color
        self.set_draw_color(r, g, b)
        self.set_line_width(2.5)
        self.rect(MARGIN - 5, MARGIN - 5, PAGE_W - 2 * (MARGIN - 5),
                  PAGE_H - 2 * (MARGIN - 5), style="D")
        # Inner thin border
        self.set_line_width(0.5)
        self.set_draw_color(r, g, b)
        self.rect(MARGIN - 2, MARGIN - 2, PAGE_W - 2 * (MARGIN - 2),
                  PAGE_H - 2 * (MARGIN - 2), style="D")

    def draw_stars_corners(self):
        """Place a star in each page corner."""
        positions = [
            (MARGIN + 2, MARGIN + 2),
            (PAGE_W - MARGIN - 2, MARGIN + 2),
            (MARGIN + 2, PAGE_H - MARGIN - 2),
            (PAGE_W - MARGIN - 2, PAGE_H - MARGIN - 2),
        ]
        for x, y in positions:
            self.draw_star(x, y, r=5)

    def section_header(self, section_num: int, title: str, color):
        """Draw a coloured section header bar."""
        self.set_fill_color(*color)
        self.set_draw_color(*DARK_GREY)
        self.set_line_width(0.5)
        bar_y = self.get_y()
        self.rect(MARGIN, bar_y, PAGE_W - 2 * MARGIN, 12, style="DF")
        self.set_text_color(*WHITE)
        self.tf(13, bold=True)
        self.set_xy(MARGIN + 2, bar_y + 2)
        self.cell(PAGE_W - 2 * MARGIN - 4, 8,
                  f"Section {section_num}: {title}", align="L")
        self.set_text_color(*BLACK)
        self.ln(14)

    def page_number_footer(self):
        """Called by fpdf2 automatically for each page."""
        pass  # We add page numbers manually per page for toddler-friendliness

    def header(self):
        pass  # Custom headers per page

    # ------------------------------------------------------------------
    # Image helper
    # ------------------------------------------------------------------
    def place_image(self, path: str, x: float, y: float, w: float):
        """Place an image at (x, y) with width w; maintain aspect ratio."""
        try:
            self.image(path, x=x, y=y, w=w)
        except Exception:
            # Fallback: draw a labelled box
            self.set_fill_color(200, 200, 200)
            self.rect(x, y, w, w, style="F")
            self.set_text_color(*DARK_GREY)
            self.tf(8)
            self.set_xy(x, y + w / 2 - 3)
            self.cell(w, 6, Path(path).stem.replace("_", " ").title(), align="C")
            self.set_text_color(*BLACK)

    # ------------------------------------------------------------------
    # Instruction box
    # ------------------------------------------------------------------
    def instruction_box(self, text: str, color=(255, 240, 180)):
        """Draw a coloured instruction box."""
        self.set_fill_color(*color)
        self.set_draw_color(*DARK_GREY)
        self.set_line_width(0.8)
        box_y = self.get_y()
        self.rect(MARGIN, box_y, PAGE_W - 2 * MARGIN, 14, style="DF")
        self.set_text_color(*BLACK)
        self.tf(14, bold=True)
        self.set_xy(MARGIN + 3, box_y + 2)
        self.multi_cell(PAGE_W - 2 * MARGIN - 6, 9, text, align="L")
        self.ln(3)

    # ------------------------------------------------------------------
    # Answer-circle decoration
    # ------------------------------------------------------------------
    def draw_answer_circle(self, x: float, y: float, r: float = 5):
        """Draw a dashed circle for the child to trace/colour."""
        self.set_draw_color(200, 80, 80)
        self.set_line_width(1.5)
        self.circle(x, y, r, style="D")

    def rounded_rect(self, x: float, y: float, w: float, h: float,
                     r: float, style=None):
        """Draw a rectangle with rounded corners."""
        self.rect(x, y, w, h, style=style, round_corners=True, corner_radius=r)

    def name_line(self):
        """Add a 'Name: ______' line."""
        y = self.get_y()
        self.set_draw_color(*DARK_GREY)
        self.set_line_width(0.5)
        self.tf(12)
        self.set_xy(MARGIN, y)
        self.cell(30, 8, "Name:", align="L")
        self.line(MARGIN + 32, y + 7, PAGE_W - MARGIN, y + 7)
        self.ln(10)

    def date_line(self):
        """Add a 'Date: ______' line."""
        y = self.get_y()
        self.tf(12)
        self.set_xy(MARGIN, y)
        self.cell(30, 8, "Date:", align="L")
        self.line(MARGIN + 32, y + 7, MARGIN + 90, y + 7)
        self.ln(10)


# ---------------------------------------------------------------------------
# Page builders
# ---------------------------------------------------------------------------

def add_cover_page(pdf: ToddlerPDF, exam_title: str, subtitle: str,
                   cover_color: tuple, cover_image_paths: list):
    """Add a colourful cover/title page."""
    pdf.add_page()
    pdf.draw_colored_border()
    pdf.draw_stars_corners()

    # Background tint
    pdf.set_fill_color(*cover_color)
    pdf.rect(MARGIN - 4, MARGIN - 4,
             PAGE_W - 2 * (MARGIN - 4), PAGE_H - 2 * (MARGIN - 4), style="F")
    pdf.draw_colored_border()
    pdf.draw_stars_corners()

    # Big smileys
    for sx, sy in [(30, 40), (180, 40), (30, 260), (180, 260)]:
        pdf.draw_smiley(sx, sy, 10)

    # Stars scattered
    star_positions = [(50, 55), (100, 30), (155, 52), (70, 248), (130, 252)]
    for sp_x, sp_y in star_positions:
        pdf.draw_star(sp_x, sp_y, r=6,
                      color=(255, 220, 0) if sp_x % 2 == 0 else (255, 140, 0))

    # Title
    pdf.set_text_color(60, 60, 150)
    pdf.tf(32, bold=True)
    pdf.set_xy(MARGIN, 60)
    pdf.multi_cell(PAGE_W - 2 * MARGIN, 16, exam_title, align="C")

    # Subtitle
    pdf.set_text_color(100, 60, 160)
    pdf.tf(18)
    pdf.set_xy(MARGIN, pdf.get_y() + 4)
    pdf.multi_cell(PAGE_W - 2 * MARGIN, 10, subtitle, align="C")

    # Cover images (up to 3)
    img_w = 50
    img_gap = (PAGE_W - 2 * MARGIN - len(cover_image_paths[:3]) * img_w) / (len(cover_image_paths[:3]) + 1)
    img_y = 135
    for i, img_path in enumerate(cover_image_paths[:3]):
        img_x = MARGIN + img_gap + i * (img_w + img_gap)
        pdf.place_image(img_path, img_x, img_y, img_w)

    # Name / Date fields
    pdf.set_xy(MARGIN, 215)
    pdf.set_fill_color(255, 255, 255)
    pdf.set_draw_color(*DARK_GREY)
    pdf.rect(MARGIN, 215, PAGE_W - 2 * MARGIN, 55, style="DF")
    pdf.set_xy(MARGIN + 5, 220)
    pdf.set_text_color(*BLACK)
    pdf.tf(16, bold=True)
    pdf.cell(PAGE_W - 2 * MARGIN - 10, 10, "My name is:", align="L")
    pdf.set_xy(MARGIN + 5, 232)
    pdf.set_line_width(1)
    pdf.line(MARGIN + 5, 242, PAGE_W - MARGIN - 5, 242)
    pdf.set_xy(MARGIN + 5, 247)
    pdf.tf(16, bold=True)
    pdf.cell(PAGE_W - 2 * MARGIN - 10, 10, "Today's date is:", align="L")
    pdf.line(MARGIN + 5, 259, PAGE_W - MARGIN - 5, 259)

    # Bottom note
    pdf.set_text_color(120, 60, 160)
    pdf.tf(11)
    pdf.set_xy(MARGIN, 270)
    pdf.multi_cell(PAGE_W - 2 * MARGIN, 7,
                   "*** Do your best and have fun! ***", align="C")


def _page_header(pdf: ToddlerPDF, section_title: str, section_num: int,
                 section_color: tuple, page_label: str = ""):
    """Add a standard page header with section info."""
    pdf.add_page()
    pdf.draw_colored_border()
    pdf.draw_stars_corners()

    # Tiny exam title top-right
    pdf.set_text_color(140, 140, 140)
    pdf.tf(9)
    pdf.set_xy(MARGIN, MARGIN)
    pdf.cell(PAGE_W - 2 * MARGIN, 6, pdf.exam_title, align="R")
    pdf.ln(3)

    # Section header bar
    header_colors = {
        1: (255, 120, 140),
        2: (80,  160, 255),
        3: (80,  200, 120),
    }
    color = header_colors.get(section_num, (180, 180, 180))
    pdf.section_header(section_num, section_title, color)

    if page_label:
        pdf.set_text_color(100, 100, 100)
        pdf.tf(9)
        pdf.set_xy(PAGE_W - MARGIN - 30, MARGIN + 1)
        pdf.cell(28, 6, page_label, align="R")

    pdf.set_text_color(*BLACK)


# ---------------------------------------------------------------------------
# Question-type page builders
# ---------------------------------------------------------------------------

def add_circle_correct_page(pdf, page_data, family_images, section_title, section_num):
    """
    Section 1: "Circle the [family member]"
    Shows 4 images in a 2×2 grid; child circles the correct one.
    """
    _page_header(pdf, section_title, section_num, (255, 120, 140))
    pdf.instruction_box(page_data["instruction"], color=(255, 240, 200))

    target = page_data["target"]
    choices = page_data["choices"]

    img_w = 60
    img_gap = (PAGE_W - 2 * MARGIN - 2 * img_w) / 3
    start_y = pdf.get_y() + 4

    for idx, choice in enumerate(choices[:4]):
        col = idx % 2
        row = idx // 2
        x = MARGIN + img_gap + col * (img_w + img_gap)
        y = start_y + row * (img_w + 22)

        # Image
        if choice in family_images:
            pdf.place_image(family_images[choice], x, y, img_w)

        # Name label below image
        pdf.set_text_color(*DARK_GREY)
        pdf.tf(13)
        pdf.set_xy(x, y + img_w + 1)
        pdf.cell(img_w, 8, choice, align="C")

        # "Correct" hint: a dotted circle placeholder
        if choice == target:
            pdf.set_draw_color(200, 60, 60)
            pdf.set_line_width(0.3)
            # Draw a light outer ring hint (child draws the actual circle)
        else:
            pdf.set_draw_color(180, 180, 180)
        pdf.set_line_width(1.0)
        pdf.circle(x + img_w / 2, y + img_w / 2, img_w / 2 + 3, style="D")

    # Footer note
    foot_y = start_y + 2 * (img_w + 22) + 8
    pdf.set_xy(MARGIN, foot_y)
    pdf.set_text_color(180, 60, 60)
    pdf.tf(14, bold=True)
    pdf.cell(PAGE_W - 2 * MARGIN, 10, f"Circle the {target}!", align="C")

    # Decorative stars
    for sx in [MARGIN + 5, PAGE_W - MARGIN - 5]:
        pdf.draw_star(sx, foot_y + 5, r=5)


def add_who_is_this_page(pdf, page_data, family_images, section_title, section_num):
    """
    Section 1: "Who is this?" – show one large image, 4 text choices.
    """
    _page_header(pdf, section_title, section_num, (255, 120, 140))
    pdf.instruction_box(page_data["instruction"], color=(255, 240, 200))

    target = page_data["target"]
    choices = page_data["choices"]

    # Large centre image
    img_w = 75
    img_x = (PAGE_W - img_w) / 2
    img_y = pdf.get_y() + 4
    if target in family_images:
        pdf.place_image(family_images[target], img_x, img_y, img_w)

    # Big question mark frame
    pdf.set_draw_color(*pdf.border_color)
    pdf.set_line_width(2)
    pdf.rect(img_x - 3, img_y - 3, img_w + 6, img_w + 6, style="D")

    # Choices as large buttons
    btn_y = img_y + img_w + 10
    btn_w = (PAGE_W - 2 * MARGIN - 3 * 6) / 4
    for i, choice in enumerate(choices[:4]):
        bx = MARGIN + i * (btn_w + 6)
        # Box
        is_correct = choice == target
        fill_col = (220, 255, 220) if is_correct else (240, 240, 255)
        pdf.set_fill_color(*fill_col)
        pdf.set_draw_color(100, 100, 200)
        pdf.set_line_width(1.5)
        pdf.rounded_rect(bx, btn_y, btn_w, 18, 4, style="DF")
        # Text
        pdf.set_text_color(*BLACK)
        pdf.tf(13, bold=True)
        pdf.set_xy(bx, btn_y + 3)
        letter = chr(ord("A") + i)
        pdf.cell(btn_w, 12, f"{letter}. {choice}", align="C")

    # Footer stars
    for sx in [MARGIN + 5, PAGE_W - MARGIN - 5]:
        pdf.draw_star(sx, btn_y + 28, r=5)


def add_matching_page(pdf, page_data, family_images, section_title, section_num):
    """
    Section 1: "Draw a line to match"
    Left column: name labels.  Right column: shuffled images.
    """
    _page_header(pdf, section_title, section_num, (255, 120, 140))
    pdf.instruction_box(page_data["instruction"], color=(200, 240, 255))

    pairs = page_data["pairs"]
    n = len(pairs)
    img_w = 38
    row_h = img_w + 10
    start_y = pdf.get_y() + 6

    left_x  = MARGIN + 5
    right_x = PAGE_W - MARGIN - img_w - 5
    mid_x   = (left_x + right_x) / 2

    # Shuffle right side
    right_order = list(range(n))
    random.shuffle(right_order)

    for i, (name, _pic) in enumerate(pairs):
        y = start_y + i * row_h
        # Left: coloured label box
        pdf.set_fill_color(255, 240, 200)
        pdf.set_draw_color(200, 120, 0)
        pdf.set_line_width(1)
        pdf.rounded_rect(left_x, y, 55, img_w, 6, style="DF")
        pdf.set_text_color(*BLACK)
        pdf.tf(14, bold=True)
        pdf.set_xy(left_x, y + img_w / 2 - 5)
        pdf.cell(55, 10, name, align="C")

        # Dotted line placeholder for child to draw
        pdf.set_draw_color(180, 180, 180)
        pdf.set_line_width(0.4)
        for dash_x in range(int(left_x + 58), int(right_x - 3), 5):
            pdf.line(dash_x, y + img_w / 2, dash_x + 3, y + img_w / 2)

    for j, orig_idx in enumerate(right_order):
        name, _pic = pairs[orig_idx]
        y = start_y + j * row_h
        if name in family_images:
            pdf.place_image(family_images[name], right_x, y, img_w)
        pdf.set_draw_color(100, 100, 200)
        pdf.set_line_width(1)
        pdf.rect(right_x - 1, y - 1, img_w + 2, img_w + 2, style="D")


def add_count_family_page(pdf, page_data, family_images, section_title, section_num):
    """
    Section 2: "How many family members do you see?"
    Shows N copies of the member image in a grid, then choice numbers.
    """
    _page_header(pdf, section_title, section_num, (80, 160, 255))
    pdf.instruction_box(page_data["instruction"], color=(220, 240, 255))

    count  = page_data["count"]
    member = page_data["member"]
    choices = page_data["choices"]

    # Show N small images in a grid
    img_w = min(30, int((PAGE_W - 2 * MARGIN - 10) / min(count, 5)) - 4)
    cols  = min(count, 5)
    rows  = math.ceil(count / cols)
    total_grid_w = cols * img_w + (cols - 1) * 4
    gx0 = (PAGE_W - total_grid_w) / 2
    gy0 = pdf.get_y() + 4

    if member in family_images:
        for i in range(count):
            col = i % cols
            row = i // cols
            gx = gx0 + col * (img_w + 4)
            gy = gy0 + row * (img_w + 4)
            pdf.place_image(family_images[member], gx, gy, img_w)

    # Number choices as big coloured buttons
    btn_y = gy0 + rows * (img_w + 4) + 12
    btn_w = (PAGE_W - 2 * MARGIN - (len(choices) - 1) * 8) / len(choices)
    choice_colors = [(255, 180, 180), (180, 220, 255), (180, 255, 200), (255, 240, 180)]

    pdf.set_text_color(*BLACK)
    for i, num in enumerate(choices):
        bx = MARGIN + i * (btn_w + 8)
        pdf.set_fill_color(*choice_colors[i % len(choice_colors)])
        pdf.set_draw_color(80, 80, 80)
        pdf.set_line_width(1.5)
        pdf.rounded_rect(bx, btn_y, btn_w, 22, 8, style="DF")
        pdf.tf(22, bold=True)
        pdf.set_xy(bx, btn_y + 4)
        pdf.cell(btn_w, 14, str(num), align="C")

    # Footer
    foot_y = btn_y + 28
    pdf.set_xy(MARGIN, foot_y)
    pdf.set_text_color(60, 100, 180)
    pdf.tf(13)
    pdf.cell(PAGE_W - 2 * MARGIN, 10, f"Count the {member}s and circle the number!", align="C")
    for sx in [MARGIN + 5, PAGE_W - MARGIN - 5]:
        pdf.draw_star(sx, foot_y + 5, r=5)


def add_number_matching_page(pdf, page_data, family_images, number_images,
                              section_title, section_num):
    """
    Section 2: "Draw a line from the number to the correct family group"
    Left: number card.  Right: shuffled group of family images.
    """
    _page_header(pdf, section_title, section_num, (80, 160, 255))
    pdf.instruction_box(page_data["instruction"], color=(220, 240, 255))

    pairs = page_data["pairs"]  # list of (number, member_name, count)
    n = len(pairs)
    card_w  = 30
    group_w = 90
    row_h   = 45
    start_y = pdf.get_y() + 6

    left_x  = MARGIN + 5
    right_x = PAGE_W - MARGIN - group_w - 5

    right_order = list(range(n))
    random.shuffle(right_order)

    for i, (number, member, count) in enumerate(pairs):
        y = start_y + i * row_h
        # Number card
        num_img = number_images.get(number)
        if num_img:
            pdf.place_image(num_img, left_x, y, card_w)
        else:
            pdf.set_fill_color(200, 220, 255)
            pdf.rounded_rect(left_x, y, card_w, card_w, 4, style="DF")
            pdf.tf(20, bold=True)
            pdf.set_xy(left_x, y + 7)
            pdf.cell(card_w, 16, str(number), align="C")

        # Dotted line
        pdf.set_draw_color(180, 180, 180)
        pdf.set_line_width(0.4)
        for dash_x in range(int(left_x + card_w + 3), int(right_x - 3), 5):
            pdf.line(dash_x, y + card_w / 2, dash_x + 3, y + card_w / 2)

    for j, orig_idx in enumerate(right_order):
        number, member, count = pairs[orig_idx]
        y = start_y + j * row_h
        sm_w = min(25, int((group_w - (count - 1) * 2) / count))
        if member in family_images:
            for k in range(count):
                kx = right_x + k * (sm_w + 2)
                if kx + sm_w <= PAGE_W - MARGIN:
                    pdf.place_image(family_images[member], kx, y, sm_w)


def add_write_number_page(pdf, page_data, family_images, section_title, section_num):
    """
    Section 2: "Count and write the number"
    Shows a group, with a box to write the number.
    """
    _page_header(pdf, section_title, section_num, (80, 160, 255))
    pdf.instruction_box(page_data["instruction"], color=(220, 240, 255))

    items = page_data["items"]
    row_h = 58
    start_y = pdf.get_y() + 6

    for i, item in enumerate(items):
        count  = item["count"]
        member = item["member"]
        y = start_y + i * row_h

        # Row background
        row_color = [(255, 240, 200), (220, 240, 255), (220, 255, 220)][i % 3]
        pdf.set_fill_color(*row_color)
        pdf.set_draw_color(180, 180, 180)
        pdf.rounded_rect(MARGIN, y, PAGE_W - 2 * MARGIN, row_h - 4, 6, style="DF")

        # Small images
        sm_w = min(28, int((PAGE_W - 2 * MARGIN - 50) / count) - 4)
        if member in family_images:
            for k in range(count):
                kx = MARGIN + 8 + k * (sm_w + 3)
                if kx + sm_w < PAGE_W - MARGIN - 45:
                    pdf.place_image(family_images[member], kx, y + 8, sm_w)

        # Write-box
        box_x = PAGE_W - MARGIN - 38
        box_y = y + 8
        pdf.set_fill_color(255, 255, 255)
        pdf.set_draw_color(80, 80, 200)
        pdf.set_line_width(2)
        pdf.rect(box_x, box_y, 30, 30, style="DF")
        pdf.set_text_color(180, 180, 180)
        pdf.tf(9)
        pdf.set_xy(box_x, box_y + 16)
        pdf.cell(30, 8, "write here", align="C")
        pdf.set_text_color(*BLACK)

        # "= ?" label
        pdf.tf(14)
        pdf.set_xy(PAGE_W - MARGIN - 42, y + 14)
        pdf.cell(6, 10, "=", align="C")


def add_where_belongs_page(pdf, page_data, house_images, section_title, section_num):
    """
    Section 3: "Where does this belong?" – show 1 item, 4 room choices.
    """
    _page_header(pdf, section_title, section_num, (80, 200, 120))
    pdf.instruction_box(page_data["instruction"], color=(220, 255, 220))

    item_name    = page_data["item"]
    correct_room = page_data["correct_room"]
    choices      = page_data["choices"]

    # Large item image
    img_w = 70
    img_x = (PAGE_W - img_w) / 2
    img_y = pdf.get_y() + 6
    if item_name in house_images:
        pdf.place_image(house_images[item_name], img_x, img_y, img_w)
    pdf.set_draw_color(*pdf.border_color)
    pdf.set_line_width(2)
    pdf.rect(img_x - 3, img_y - 3, img_w + 6, img_w + 6, style="D")

    # Item name label
    pdf.set_text_color(*BLACK)
    pdf.tf(18, bold=True)
    pdf.set_xy(MARGIN, img_y + img_w + 4)
    pdf.cell(PAGE_W - 2 * MARGIN, 12, item_name, align="C")

    # Room choices
    btn_y = img_y + img_w + 20
    btn_w = (PAGE_W - 2 * MARGIN - (len(choices) - 1) * 6) / len(choices)
    room_colors = {
        "Kitchen":     (255, 220, 160),
        "Bedroom":     (220, 200, 255),
        "Bathroom":    (180, 230, 255),
        "Living Room": (220, 255, 210),
        "Garden":      (200, 255, 200),
    }
    for i, room in enumerate(choices):
        bx = MARGIN + i * (btn_w + 6)
        pdf.set_fill_color(*room_colors.get(room, (240, 240, 240)))
        pdf.set_draw_color(80, 80, 80)
        pdf.set_line_width(1.5)
        pdf.rounded_rect(bx, btn_y, btn_w, 22, 6, style="DF")
        pdf.set_text_color(*BLACK)
        pdf.tf(11, bold=True)
        pdf.set_xy(bx, btn_y + 5)
        pdf.cell(btn_w, 12, room, align="C")

    # Footer
    foot_y = btn_y + 28
    pdf.set_xy(MARGIN, foot_y)
    pdf.set_text_color(40, 140, 60)
    pdf.tf(13)
    pdf.cell(PAGE_W - 2 * MARGIN, 10,
             f"The {item_name} belongs in the {correct_room}!", align="C")
    for sx in [MARGIN + 5, PAGE_W - MARGIN - 5]:
        pdf.draw_star(sx, foot_y + 5, r=5)


def add_circle_room_items_page(pdf, page_data, house_images, section_title, section_num):
    """
    Section 3: "Circle all the things you find in the [room]"
    Shows a grid of items (correct + wrong mixed).
    """
    _page_header(pdf, section_title, section_num, (80, 200, 120))
    pdf.instruction_box(page_data["instruction"], color=(220, 255, 220))

    room          = page_data["room"]
    correct_items = page_data["correct_items"]
    wrong_items   = page_data["wrong_items"]
    all_items     = correct_items + wrong_items
    random.shuffle(all_items)

    img_w  = 45
    cols   = 3
    gap_x  = (PAGE_W - 2 * MARGIN - cols * img_w) / (cols + 1)
    start_y = pdf.get_y() + 6
    row_h  = img_w + 14

    for idx, item_name in enumerate(all_items):
        col = idx % cols
        row = idx // cols
        x   = MARGIN + gap_x + col * (img_w + gap_x)
        y   = start_y + row * row_h

        if item_name in house_images:
            pdf.place_image(house_images[item_name], x, y, img_w)

        # Green tint for correct items, neutral for wrong
        if item_name in correct_items:
            pdf.set_draw_color(60, 180, 60)
            pdf.set_line_width(1.5)
        else:
            pdf.set_draw_color(180, 180, 180)
            pdf.set_line_width(0.8)
        pdf.circle(x + img_w / 2, y + img_w / 2, img_w / 2 + 3, style="D")

        # Label
        pdf.set_text_color(*DARK_GREY)
        pdf.tf(10)
        pdf.set_xy(x, y + img_w + 1)
        pdf.cell(img_w, 6, item_name, align="C")
        pdf.set_text_color(*BLACK)


def add_room_matching_page(pdf, page_data, house_images, section_title, section_num):
    """
    Section 3: "Draw a line to match item to its room"
    """
    _page_header(pdf, section_title, section_num, (80, 200, 120))
    pdf.instruction_box(page_data["instruction"], color=(220, 255, 220))

    pairs = page_data["pairs"]
    n     = len(pairs)
    img_w = 38
    row_h = img_w + 10
    start_y = pdf.get_y() + 6

    left_x  = MARGIN + 5
    right_x = PAGE_W - MARGIN - 55

    right_order = list(range(n))
    random.shuffle(right_order)

    room_colors = {
        "Kitchen":     (255, 220, 160),
        "Bedroom":     (220, 200, 255),
        "Bathroom":    (180, 230, 255),
        "Living Room": (220, 255, 210),
        "Garden":      (200, 255, 200),
    }

    for i, (item_name, room) in enumerate(pairs):
        y = start_y + i * row_h
        # Item image on left
        if item_name in house_images:
            pdf.place_image(house_images[item_name], left_x, y, img_w)
        pdf.set_text_color(*DARK_GREY)
        pdf.tf(10)
        pdf.set_xy(left_x, y + img_w + 1)
        pdf.cell(img_w, 6, item_name, align="C")

        # Dotted line
        pdf.set_draw_color(180, 180, 180)
        pdf.set_line_width(0.4)
        for dash_x in range(int(left_x + img_w + 3), int(right_x - 3), 5):
            pdf.line(dash_x, y + img_w / 2, dash_x + 3, y + img_w / 2)

    for j, orig_idx in enumerate(right_order):
        item_name, room = pairs[orig_idx]
        y = start_y + j * row_h
        col = room_colors.get(room, (240, 240, 240))
        pdf.set_fill_color(*col)
        pdf.set_draw_color(80, 80, 80)
        pdf.set_line_width(1)
        pdf.rounded_rect(right_x, y, 52, img_w, 5, style="DF")
        pdf.set_text_color(*BLACK)
        pdf.tf(11, bold=True)
        pdf.set_xy(right_x, y + img_w / 2 - 5)
        pdf.cell(52, 10, room, align="C")

    pdf.set_text_color(*BLACK)
