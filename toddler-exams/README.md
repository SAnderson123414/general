# 🧒 Toddler Integrated Studies – PDF Exam Generator

A Python script that generates colourful, picture-heavy PDF exam sheets for toddlers (ages 2–4) covering **Integrated Studies** topics:

| Section | Topic |
|---------|-------|
| **1** | Identify Different Family Members |
| **2** | Associate Numbers with Sets using Pictures of Families |
| **3** | Identify Things Found in Different Parts of the House |

---

## 📋 Requirements

- Python 3.8+
- pip

---

## 🚀 Quick Start

```bash
# 1. Navigate into the project folder
cd toddler-exams

# 2. (Recommended) Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # macOS / Linux
.venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate the default 5 exam PDFs
python generate_exams.py

# 5. Open the PDFs from the output/ folder
```

---

## ⚙️ Options

```bash
# Generate a custom number of exams
python generate_exams.py --count 10
```

---

## 📁 Project Structure

```
toddler-exams/
├── README.md
├── requirements.txt
├── generate_exams.py          # Main script – run this!
├── images/                    # Auto-generated images (created at runtime)
│   ├── family/                # Stick-figure family member illustrations
│   ├── house/                 # House-item illustrations
│   └── numbers/               # Number cards with dot representations
├── output/                    # Generated PDF exams appear here
│   ├── exam_1_family_members.pdf
│   ├── exam_2_counting_families.pdf
│   ├── exam_3_house_items.pdf
│   ├── exam_4_mixed_review.pdf
│   └── exam_5_fun_challenge.pdf
└── utils/
    ├── __init__.py
    ├── exam_content.py        # All exam questions and data
    ├── image_downloader.py    # Image generation (Pillow-based fallback illustrations)
    └── pdf_builder.py         # PDF generation utilities (fpdf2)
```

---

## 📄 Exam Contents

### Exam 1 – Family Members (`exam_1_family_members.pdf`)
- Circle the correct family member (Mom, Dad, Baby, …)
- "Who is this?" multiple-choice
- Draw a line matching names to pictures
- Count family members

### Exam 2 – Counting Families (`exam_2_counting_families.pdf`)
- Count family members and circle the number (1–10)
- Match numbers to the correct group size
- Write the number in the box

### Exam 3 – House Items (`exam_3_house_items.pdf`)
- "Where does this belong?" (Kitchen / Bedroom / Bathroom / Living Room / Garden)
- Circle all items in a given room
- Match items to their room

### Exam 4 – Mixed Review (`exam_4_mixed_review.pdf`)
- Questions from all three sections

### Exam 5 – Fun Challenge (`exam_5_fun_challenge.pdf`)
- Harder variants of all question types

---

## 🖼️ Images

All illustrations are auto-generated using **Pillow** (Python Imaging Library):

- **Family members** – colourful stick figures with distinguishing features (hats, bows, glasses, proportions for adults vs. children)
- **House items** – simple but recognisable geometric shapes (stove, bed, bathtub, sofa, …)
- **Number cards** – big digit + word label + dot representation of the count

Images are cached in the `images/` folder so they are only generated once.

---

## 🏗️ Technical Details

| Library | Purpose |
|---------|---------|
| `fpdf2` | PDF generation |
| `Pillow` | Image creation (fallback illustrations) |
| `requests` | (Optional) image downloading from Wikimedia Commons |

---

## 📝 Licence

This project and all generated materials are free to use, print, and share for educational purposes.
