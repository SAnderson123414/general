# Toddler Integrated Studies Exam Generator

A Python-based PDF exam generator that produces **multiple printable test/exam PDFs for toddlers** (ages 2–4) on the topic of **Integrated Studies**.

## Exam Topics

The generator creates exams covering 3 core sections:

1. **Identify Different Family Members** – Mom, dad, grandma, grandpa, brother, sister, baby, uncle, aunt, cousin
2. **Associate Numbers with Sets Using Pictures of Families** – Count family members, match numbers 1–10 to groups
3. **Identify Things Found in Different Parts of the House** – Kitchen, bedroom, bathroom, living room, garden

## Features

- 🖼️ Downloads free images from the internet (Wikimedia Commons, etc.)
- 🎨 Auto-generates colorful fallback illustrations using Pillow if downloads fail
- 📏 Toddler-friendly layout — big fonts, lots of pictures, clear instructions
- 🌈 Colorful title pages with space for the child's name
- ⭐ Fun decorative elements: stars, smiley faces, borders

## Project Structure

```
toddler-exams/
├── README.md
├── requirements.txt
├── generate_exams.py          # Main script
├── images/                    # Downloaded/generated images (created at runtime)
│   ├── family/
│   ├── house/
│   └── numbers/
├── output/                    # Generated PDFs go here
│   ├── exam_1_family_members.pdf
│   ├── exam_2_counting_families.pdf
│   ├── exam_3_house_items.pdf
│   ├── exam_4_mixed_review.pdf
│   └── exam_5_fun_challenge.pdf
└── utils/
    ├── __init__.py
    ├── image_downloader.py    # Handles downloading images from free sources
    ├── pdf_builder.py         # PDF generation utilities
    └── exam_content.py        # Exam questions and content data
```

## Setup

1. **Install Python 3.8+** if you haven't already.

2. **Install dependencies:**
   ```bash
   cd toddler-exams
   pip install -r requirements.txt
   ```

3. **Generate exams:**
   ```bash
   python generate_exams.py
   ```
   This will download/generate images and create 5 PDF exams in the `output/` folder.

## Usage

```bash
# Generate the default 5 exams
python generate_exams.py

# Generate a custom number of exams
python generate_exams.py --count 10

# Show help
python generate_exams.py --help
```

## Output

After running, you'll find the following files in `output/`:

| File | Contents |
|------|----------|
| `exam_1_family_members.pdf` | Family member identification exercises |
| `exam_2_counting_families.pdf` | Number and counting exercises |
| `exam_3_house_items.pdf` | Household items and rooms exercises |
| `exam_4_mixed_review.pdf` | Mixed review from all 3 sections |
| `exam_5_fun_challenge.pdf` | Fun challenge with all question types |
| `exam_6_*.pdf` ... | Additional exams (if `--count` > 5) |

## Image Sources

Images are downloaded from freely licensed sources:
- [Wikimedia Commons](https://commons.wikimedia.org/) (public domain / CC licensed)
- Generated using [Pillow](https://python-pillow.org/) as fallback

Downloaded images are cached in the `images/` folder so they don't need to be re-downloaded on subsequent runs.

## Notes

- Internet connection is required for the first run (to download images). Subsequent runs use cached images.
- If all image downloads fail, the generator automatically falls back to creating colorful shape-based illustrations using Pillow.
- PDFs are designed for A4 paper size.
