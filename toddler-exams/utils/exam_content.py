"""
Exam content data: questions, answers, and metadata for all three sections.
"""

# ---------------------------------------------------------------------------
# Section 1 – Family Members
# ---------------------------------------------------------------------------

FAMILY_MEMBERS = [
    {"name": "Mom",     "color": (255, 182, 193), "hat": False, "glasses": False, "bow": True,  "tall": True},
    {"name": "Dad",     "color": (173, 216, 230), "hat": True,  "glasses": False, "bow": False, "tall": True},
    {"name": "Baby",    "color": (255, 255, 153), "hat": False, "glasses": False, "bow": False, "tall": False},
    {"name": "Brother", "color": (144, 238, 144), "hat": True,  "glasses": False, "bow": False, "tall": False},
    {"name": "Sister",  "color": (255, 200, 150), "hat": False, "glasses": False, "bow": True,  "tall": False},
    {"name": "Grandma", "color": (221, 160, 221), "hat": False, "glasses": True,  "bow": True,  "tall": True},
    {"name": "Grandpa", "color": (176, 196, 222), "hat": True,  "glasses": True,  "bow": False, "tall": True},
    {"name": "Uncle",   "color": (152, 251, 152), "hat": False, "glasses": False, "bow": False, "tall": True},
    {"name": "Aunt",    "color": (255, 218, 185), "hat": False, "glasses": False, "bow": True,  "tall": True},
    {"name": "Cousin",  "color": (135, 206, 235), "hat": False, "glasses": False, "bow": False, "tall": False},
]

# ---------------------------------------------------------------------------
# Section 2 – Numbers & Sets (1-10)
# ---------------------------------------------------------------------------

NUMBER_DATA = [
    {"number": 1,  "label": "ONE",   "bg": (255, 200, 200)},
    {"number": 2,  "label": "TWO",   "bg": (255, 220, 150)},
    {"number": 3,  "label": "THREE", "bg": (255, 255, 150)},
    {"number": 4,  "label": "FOUR",  "bg": (200, 255, 200)},
    {"number": 5,  "label": "FIVE",  "bg": (150, 230, 255)},
    {"number": 6,  "label": "SIX",   "bg": (210, 180, 255)},
    {"number": 7,  "label": "SEVEN", "bg": (255, 182, 230)},
    {"number": 8,  "label": "EIGHT", "bg": (200, 240, 210)},
    {"number": 9,  "label": "NINE",  "bg": (255, 200, 170)},
    {"number": 10, "label": "TEN",   "bg": (180, 220, 255)},
]

# ---------------------------------------------------------------------------
# Section 3 – House Items by Room
# ---------------------------------------------------------------------------

HOUSE_ROOMS = {
    "Kitchen": {
        "color": (255, 220, 160),
        "emoji_color": (230, 120, 50),
        "items": [
            {"name": "Stove",        "shape": "stove"},
            {"name": "Refrigerator", "shape": "fridge"},
            {"name": "Pot",          "shape": "pot"},
            {"name": "Pan",          "shape": "pan"},
            {"name": "Plate",        "shape": "plate"},
            {"name": "Cup",          "shape": "cup"},
            {"name": "Spoon",        "shape": "spoon"},
            {"name": "Fork",         "shape": "fork"},
        ],
    },
    "Bedroom": {
        "color": (220, 200, 255),
        "emoji_color": (140, 90, 200),
        "items": [
            {"name": "Bed",         "shape": "bed"},
            {"name": "Pillow",      "shape": "pillow"},
            {"name": "Blanket",     "shape": "blanket"},
            {"name": "Lamp",        "shape": "lamp"},
            {"name": "Dresser",     "shape": "dresser"},
            {"name": "Teddy Bear",  "shape": "teddy"},
            {"name": "Alarm Clock", "shape": "clock"},
        ],
    },
    "Bathroom": {
        "color": (180, 230, 255),
        "emoji_color": (50, 130, 200),
        "items": [
            {"name": "Bathtub",    "shape": "bathtub"},
            {"name": "Soap",       "shape": "soap"},
            {"name": "Toothbrush", "shape": "toothbrush"},
            {"name": "Towel",      "shape": "towel"},
            {"name": "Mirror",     "shape": "mirror"},
            {"name": "Toilet",     "shape": "toilet"},
            {"name": "Shampoo",    "shape": "shampoo"},
        ],
    },
    "Living Room": {
        "color": (220, 255, 210),
        "emoji_color": (60, 160, 80),
        "items": [
            {"name": "Sofa",          "shape": "sofa"},
            {"name": "TV",            "shape": "tv"},
            {"name": "Bookshelf",     "shape": "bookshelf"},
            {"name": "Rug",           "shape": "rug"},
            {"name": "Remote Control","shape": "remote"},
            {"name": "Picture Frame", "shape": "frame"},
        ],
    },
    "Garden": {
        "color": (200, 255, 200),
        "emoji_color": (60, 170, 60),
        "items": [
            {"name": "Flowers",      "shape": "flower"},
            {"name": "Tree",         "shape": "tree"},
            {"name": "Swing",        "shape": "swing"},
            {"name": "Watering Can", "shape": "watering_can"},
            {"name": "Butterfly",    "shape": "butterfly"},
            {"name": "Grass",        "shape": "grass"},
        ],
    },
}

# ---------------------------------------------------------------------------
# Exam definitions  (5 exams)
# ---------------------------------------------------------------------------

EXAMS = [
    {
        "id": 1,
        "filename": "exam_1_family_members.pdf",
        "title": "Meet My Family!",
        "subtitle": "Integrated Studies – Exam 1",
        "cover_color": (255, 200, 220),
        "sections": [
            {
                "section_num": 1,
                "title": "Identify Family Members",
                "pages": [
                    {
                        "type": "circle_correct",
                        "instruction": "Circle the MOM!",
                        "target": "Mom",
                        "choices": ["Dad", "Baby", "Mom", "Sister"],
                    },
                    {
                        "type": "circle_correct",
                        "instruction": "Circle the DAD!",
                        "target": "Dad",
                        "choices": ["Mom", "Dad", "Grandma", "Brother"],
                    },
                    {
                        "type": "who_is_this",
                        "instruction": "Who is this? Circle the correct answer!",
                        "target": "Grandma",
                        "choices": ["Grandpa", "Grandma", "Aunt", "Mom"],
                    },
                    {
                        "type": "matching",
                        "instruction": "Draw a line to match the name to the picture!",
                        "pairs": [
                            ("Mom", "Mom"),
                            ("Dad", "Dad"),
                            ("Baby", "Baby"),
                            ("Sister", "Sister"),
                        ],
                    },
                ],
            },
            {
                "section_num": 2,
                "title": "Count the Family!",
                "pages": [
                    {
                        "type": "count_family",
                        "instruction": "How many family members do you see? Circle the number!",
                        "count": 3,
                        "member": "Brother",
                        "choices": [1, 2, 3, 4],
                    },
                    {
                        "type": "count_family",
                        "instruction": "How many family members do you see? Circle the number!",
                        "count": 5,
                        "member": "Sister",
                        "choices": [3, 4, 5, 6],
                    },
                ],
            },
        ],
    },
    {
        "id": 2,
        "filename": "exam_2_counting_families.pdf",
        "title": "Count With My Family!",
        "subtitle": "Integrated Studies – Exam 2",
        "cover_color": (200, 230, 255),
        "sections": [
            {
                "section_num": 2,
                "title": "Numbers and Families",
                "pages": [
                    {
                        "type": "count_family",
                        "instruction": "How many people do you see? Circle the number!",
                        "count": 2,
                        "member": "Baby",
                        "choices": [1, 2, 3, 4],
                    },
                    {
                        "type": "count_family",
                        "instruction": "How many people do you see? Circle the number!",
                        "count": 4,
                        "member": "Mom",
                        "choices": [2, 3, 4, 5],
                    },
                    {
                        "type": "count_family",
                        "instruction": "How many people do you see? Circle the number!",
                        "count": 6,
                        "member": "Dad",
                        "choices": [4, 5, 6, 7],
                    },
                    {
                        "type": "number_matching",
                        "instruction": "Draw a line from the number to the correct group!",
                        "pairs": [
                            (1, "Mom", 1),
                            (3, "Baby", 3),
                            (5, "Sister", 5),
                        ],
                    },
                    {
                        "type": "write_number",
                        "instruction": "Count and write the number in the box!",
                        "items": [
                            {"count": 2, "member": "Brother"},
                            {"count": 4, "member": "Cousin"},
                            {"count": 7, "member": "Baby"},
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": 3,
        "filename": "exam_3_house_items.pdf",
        "title": "Things in My House!",
        "subtitle": "Integrated Studies – Exam 3",
        "cover_color": (220, 255, 220),
        "sections": [
            {
                "section_num": 3,
                "title": "Items in the House",
                "pages": [
                    {
                        "type": "where_belongs",
                        "instruction": "Where does this belong? Circle the correct room!",
                        "item": "Stove",
                        "correct_room": "Kitchen",
                        "choices": ["Kitchen", "Bedroom", "Bathroom", "Garden"],
                    },
                    {
                        "type": "where_belongs",
                        "instruction": "Where does this belong? Circle the correct room!",
                        "item": "Bed",
                        "correct_room": "Bedroom",
                        "choices": ["Kitchen", "Bedroom", "Bathroom", "Living Room"],
                    },
                    {
                        "type": "where_belongs",
                        "instruction": "Where does this belong? Circle the correct room!",
                        "item": "Toothbrush",
                        "correct_room": "Bathroom",
                        "choices": ["Kitchen", "Bedroom", "Bathroom", "Garden"],
                    },
                    {
                        "type": "circle_room_items",
                        "instruction": "Circle ALL the things you find in the KITCHEN!",
                        "room": "Kitchen",
                        "correct_items": ["Stove", "Pot", "Cup"],
                        "wrong_items": ["Bed", "Flowers", "Toilet"],
                    },
                    {
                        "type": "room_matching",
                        "instruction": "Draw a line to match each item to its room!",
                        "pairs": [
                            ("Stove", "Kitchen"),
                            ("Bed", "Bedroom"),
                            ("Bathtub", "Bathroom"),
                            ("Sofa", "Living Room"),
                        ],
                    },
                ],
            },
        ],
    },
    {
        "id": 4,
        "filename": "exam_4_mixed_review.pdf",
        "title": "Mixed Review Fun!",
        "subtitle": "Integrated Studies – Exam 4",
        "cover_color": (255, 240, 200),
        "sections": [
            {
                "section_num": 1,
                "title": "Family Members",
                "pages": [
                    {
                        "type": "circle_correct",
                        "instruction": "Circle the GRANDPA!",
                        "target": "Grandpa",
                        "choices": ["Uncle", "Grandpa", "Dad", "Brother"],
                    },
                    {
                        "type": "who_is_this",
                        "instruction": "Who is this? Circle the correct answer!",
                        "target": "Uncle",
                        "choices": ["Dad", "Uncle", "Grandpa", "Brother"],
                    },
                ],
            },
            {
                "section_num": 2,
                "title": "Counting Families",
                "pages": [
                    {
                        "type": "count_family",
                        "instruction": "How many family members do you see? Circle the number!",
                        "count": 8,
                        "member": "Cousin",
                        "choices": [6, 7, 8, 9],
                    },
                    {
                        "type": "write_number",
                        "instruction": "Count and write the number in the box!",
                        "items": [
                            {"count": 3, "member": "Aunt"},
                            {"count": 5, "member": "Uncle"},
                        ],
                    },
                ],
            },
            {
                "section_num": 3,
                "title": "House Items",
                "pages": [
                    {
                        "type": "where_belongs",
                        "instruction": "Where does this belong? Circle the correct room!",
                        "item": "Flowers",
                        "correct_room": "Garden",
                        "choices": ["Kitchen", "Bedroom", "Bathroom", "Garden"],
                    },
                    {
                        "type": "circle_room_items",
                        "instruction": "Circle ALL the things you find in the BEDROOM!",
                        "room": "Bedroom",
                        "correct_items": ["Bed", "Lamp", "Pillow"],
                        "wrong_items": ["Stove", "Bathtub", "TV"],
                    },
                ],
            },
        ],
    },
    {
        "id": 5,
        "filename": "exam_5_fun_challenge.pdf",
        "title": "Fun Challenge Time!",
        "subtitle": "Integrated Studies – Exam 5",
        "cover_color": (255, 210, 255),
        "sections": [
            {
                "section_num": 1,
                "title": "Super Family Challenge",
                "pages": [
                    {
                        "type": "matching",
                        "instruction": "Draw a line to match the name to the picture!",
                        "pairs": [
                            ("Grandma", "Grandma"),
                            ("Grandpa", "Grandpa"),
                            ("Uncle",   "Uncle"),
                            ("Aunt",    "Aunt"),
                        ],
                    },
                    {
                        "type": "circle_correct",
                        "instruction": "Circle the AUNT!",
                        "target": "Aunt",
                        "choices": ["Mom", "Sister", "Aunt", "Cousin"],
                    },
                ],
            },
            {
                "section_num": 2,
                "title": "Counting Challenge",
                "pages": [
                    {
                        "type": "count_family",
                        "instruction": "How many people do you see? Circle the number!",
                        "count": 10,
                        "member": "Baby",
                        "choices": [8, 9, 10, 11],
                    },
                    {
                        "type": "number_matching",
                        "instruction": "Draw a line from the number to the correct group!",
                        "pairs": [
                            (2, "Grandma", 2),
                            (4, "Grandpa", 4),
                            (6, "Aunt",    6),
                        ],
                    },
                ],
            },
            {
                "section_num": 3,
                "title": "House Challenge",
                "pages": [
                    {
                        "type": "room_matching",
                        "instruction": "Draw a line to match each item to its room!",
                        "pairs": [
                            ("Flowers",    "Garden"),
                            ("Sofa",       "Living Room"),
                            ("Shampoo",    "Bathroom"),
                            ("Alarm Clock","Bedroom"),
                        ],
                    },
                    {
                        "type": "where_belongs",
                        "instruction": "Where does this belong? Circle the correct room!",
                        "item": "TV",
                        "correct_room": "Living Room",
                        "choices": ["Kitchen", "Bedroom", "Bathroom", "Living Room"],
                    },
                    {
                        "type": "circle_room_items",
                        "instruction": "Circle ALL the things you find in the BATHROOM!",
                        "room": "Bathroom",
                        "correct_items": ["Soap", "Towel", "Shampoo"],
                        "wrong_items": ["Fork", "Tree", "Teddy Bear"],
                    },
                ],
            },
        ],
    },
]
