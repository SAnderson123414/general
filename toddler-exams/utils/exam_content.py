"""Exam questions and content data for toddler integrated studies exams."""

# ---------------------------------------------------------------------------
# Section 1 – Family Members
# ---------------------------------------------------------------------------

FAMILY_MEMBERS = [
    "mom",
    "dad",
    "grandma",
    "grandpa",
    "brother",
    "sister",
    "baby",
    "uncle",
    "aunt",
    "cousin",
]

# Each entry: (question_text, correct_answer, choices)
FAMILY_CIRCLE_QUESTIONS = [
    ("Circle the MOM", "mom", ["mom", "dad", "grandma", "grandpa"]),
    ("Circle the DAD", "dad", ["dad", "mom", "uncle", "grandpa"]),
    ("Circle the GRANDMA", "grandma", ["grandma", "aunt", "mom", "sister"]),
    ("Circle the GRANDPA", "grandpa", ["grandpa", "dad", "uncle", "brother"]),
    ("Circle the BABY", "baby", ["baby", "sister", "brother", "cousin"]),
    ("Circle the SISTER", "sister", ["sister", "brother", "baby", "cousin"]),
    ("Circle the BROTHER", "brother", ["brother", "dad", "uncle", "grandpa"]),
    ("Circle the UNCLE", "uncle", ["uncle", "dad", "brother", "grandpa"]),
    ("Circle the AUNT", "aunt", ["aunt", "mom", "sister", "grandma"]),
    ("Circle the COUSIN", "cousin", ["cousin", "brother", "sister", "baby"]),
]

# "Who is this?" – show a picture, child picks correct label
FAMILY_WHO_QUESTIONS = [
    ("Who is this?", "mom", ["mom", "aunt", "grandma", "sister"]),
    ("Who is this?", "dad", ["dad", "uncle", "grandpa", "brother"]),
    ("Who is this?", "grandma", ["grandma", "mom", "aunt", "sister"]),
    ("Who is this?", "grandpa", ["grandpa", "dad", "uncle", "brother"]),
    ("Who is this?", "baby", ["baby", "sister", "brother", "cousin"]),
]

# Draw-a-line matching: list of (label, picture_key) pairs
FAMILY_MATCHING_SETS = [
    [("MOM", "mom"), ("DAD", "dad"), ("GRANDMA", "grandma"), ("GRANDPA", "grandpa")],
    [("BABY", "baby"), ("SISTER", "sister"), ("BROTHER", "brother"), ("UNCLE", "uncle")],
    [("AUNT", "aunt"), ("COUSIN", "cousin"), ("MOM", "mom"), ("DAD", "dad")],
]

# ---------------------------------------------------------------------------
# Section 2 – Numbers & Counting with families
# ---------------------------------------------------------------------------

# (number, description displayed on exam)
COUNTING_QUESTIONS = [
    (1, "How many people do you see?"),
    (2, "How many people do you see?"),
    (3, "How many people do you see?"),
    (4, "How many people do you see?"),
    (5, "How many people do you see?"),
    (6, "How many people do you see?"),
    (7, "How many people do you see?"),
    (8, "How many people do you see?"),
    (9, "How many people do you see?"),
    (10, "How many people do you see?"),
]

# "Circle the group that has N people" – sets of 4 options (correct answer first)
CIRCLE_GROUP_QUESTIONS = [
    (3, "Circle the group that has 3 people", [3, 1, 5, 7]),
    (5, "Circle the group that has 5 people", [5, 2, 8, 4]),
    (2, "Circle the group that has 2 people", [2, 6, 4, 9]),
    (4, "Circle the group that has 4 people", [4, 1, 7, 10]),
    (6, "Circle the group that has 6 people", [6, 3, 9, 2]),
    (1, "Circle the group that has 1 person", [1, 4, 6, 3]),
    (8, "Circle the group that has 8 people", [8, 5, 2, 10]),
    (7, "Circle the group that has 7 people", [7, 4, 9, 1]),
    (9, "Circle the group that has 9 people", [9, 6, 3, 7]),
    (10, "Circle the group that has 10 people", [10, 7, 4, 8]),
]

# ---------------------------------------------------------------------------
# Section 3 – Household items and rooms
# ---------------------------------------------------------------------------

ROOMS = {
    "Kitchen": [
        "stove", "refrigerator", "pot", "pan", "plate",
        "cup", "spoon", "fork",
    ],
    "Bedroom": [
        "bed", "pillow", "blanket", "lamp", "dresser",
        "teddy bear", "alarm clock",
    ],
    "Bathroom": [
        "bathtub", "soap", "toothbrush", "towel", "mirror",
        "toilet", "shampoo",
    ],
    "Living Room": [
        "sofa", "TV", "bookshelf", "rug", "remote control",
        "picture frame",
    ],
    "Garden": [
        "flowers", "tree", "swing", "watering can",
        "butterfly", "grass",
    ],
}

# Flat list of (item, room) pairs for convenience
ITEM_ROOM_PAIRS = [
    (item, room)
    for room, items in ROOMS.items()
    for item in items
]

# "Where does this belong?" questions: (item, correct_room, wrong_rooms)
WHERE_BELONGS_QUESTIONS = [
    ("stove",       "Kitchen",     ["Bedroom", "Bathroom", "Garden"]),
    ("bed",         "Bedroom",     ["Kitchen", "Bathroom", "Living Room"]),
    ("bathtub",     "Bathroom",    ["Kitchen", "Bedroom", "Garden"]),
    ("sofa",        "Living Room", ["Kitchen", "Bedroom", "Bathroom"]),
    ("flowers",     "Garden",      ["Kitchen", "Bedroom", "Bathroom"]),
    ("refrigerator","Kitchen",     ["Bedroom", "Living Room", "Garden"]),
    ("pillow",      "Bedroom",     ["Kitchen", "Bathroom", "Living Room"]),
    ("toothbrush",  "Bathroom",    ["Bedroom", "Kitchen", "Garden"]),
    ("TV",          "Living Room", ["Kitchen", "Bedroom", "Garden"]),
    ("tree",        "Garden",      ["Kitchen", "Bedroom", "Bathroom"]),
    ("pot",         "Kitchen",     ["Bedroom", "Bathroom", "Living Room"]),
    ("lamp",        "Bedroom",     ["Kitchen", "Bathroom", "Garden"]),
    ("soap",        "Bathroom",    ["Kitchen", "Bedroom", "Living Room"]),
    ("bookshelf",   "Living Room", ["Kitchen", "Bedroom", "Garden"]),
    ("swing",       "Garden",      ["Kitchen", "Bedroom", "Bathroom"]),
    ("spoon",       "Kitchen",     ["Bedroom", "Bathroom", "Living Room"]),
    ("teddy bear",  "Bedroom",     ["Kitchen", "Bathroom", "Garden"]),
    ("towel",       "Bathroom",    ["Bedroom", "Kitchen", "Living Room"]),
    ("rug",         "Living Room", ["Kitchen", "Bedroom", "Garden"]),
    ("butterfly",   "Garden",      ["Kitchen", "Bedroom", "Bathroom"]),
]

# "Circle all things in [room]" – (room, correct_items, wrong_items)
CIRCLE_IN_ROOM_QUESTIONS = [
    ("Kitchen",     ["stove", "pot", "spoon"],  ["bed", "bathtub", "sofa"]),
    ("Bedroom",     ["bed", "pillow", "lamp"],  ["stove", "toilet", "TV"]),
    ("Bathroom",    ["bathtub", "soap", "towel"], ["bed", "stove", "sofa"]),
    ("Living Room", ["sofa", "TV", "bookshelf"], ["stove", "bathtub", "pillow"]),
    ("Garden",      ["flowers", "tree", "swing"], ["bed", "stove", "sofa"]),
]

# "What's wrong?" – (room, items_shown, wrong_item)
WHATS_WRONG_QUESTIONS = [
    ("Kitchen",     ["stove", "pot", "spoon", "bed"],         "bed"),
    ("Bedroom",     ["bed", "pillow", "lamp", "toilet"],      "toilet"),
    ("Bathroom",    ["bathtub", "soap", "towel", "sofa"],     "sofa"),
    ("Living Room", ["sofa", "TV", "bookshelf", "bathtub"],   "bathtub"),
    ("Garden",      ["flowers", "tree", "swing", "stove"],    "stove"),
]

# ---------------------------------------------------------------------------
# Exam definitions – each exam is a list of (section_type, params) tuples
# ---------------------------------------------------------------------------

EXAM_DEFINITIONS = [
    # Exam 1 – Family Members focus
    {
        "title": "Exam 1: Family Members",
        "filename": "exam_1_family_members.pdf",
        "sections": [
            {"type": "title_page",   "exam_name": "Family Members Exam", "exam_number": 1},
            {"type": "circle_family", "questions": FAMILY_CIRCLE_QUESTIONS[:4]},
            {"type": "who_is_this",   "questions": FAMILY_WHO_QUESTIONS[:3]},
            {"type": "match_family",  "set_index": 0},
            {"type": "color_family",  "members": ["mom", "dad", "grandma", "grandpa"]},
        ],
    },
    # Exam 2 – Counting Families
    {
        "title": "Exam 2: Counting Families",
        "filename": "exam_2_counting_families.pdf",
        "sections": [
            {"type": "title_page",   "exam_name": "Counting Families Exam", "exam_number": 2},
            {"type": "count_people",  "questions": COUNTING_QUESTIONS[:5]},
            {"type": "circle_group",  "questions": CIRCLE_GROUP_QUESTIONS[:4]},
            {"type": "draw_line_numbers", "pairs": list(zip(range(1, 6), range(1, 6)))},
            {"type": "count_write",   "questions": COUNTING_QUESTIONS[5:10]},
        ],
    },
    # Exam 3 – House Items
    {
        "title": "Exam 3: House Items",
        "filename": "exam_3_house_items.pdf",
        "sections": [
            {"type": "title_page",    "exam_name": "House Items Exam", "exam_number": 3},
            {"type": "where_belongs", "questions": WHERE_BELONGS_QUESTIONS[:4]},
            {"type": "circle_in_room","questions": CIRCLE_IN_ROOM_QUESTIONS[:3]},
            {"type": "match_items",   "pairs": [(p[0], p[1]) for p in WHERE_BELONGS_QUESTIONS[4:8]]},
            {"type": "whats_wrong",   "questions": WHATS_WRONG_QUESTIONS[:2]},
        ],
    },
    # Exam 4 – Mixed Review
    {
        "title": "Exam 4: Mixed Review",
        "filename": "exam_4_mixed_review.pdf",
        "sections": [
            {"type": "title_page",    "exam_name": "Mixed Review Exam", "exam_number": 4},
            {"type": "circle_family", "questions": FAMILY_CIRCLE_QUESTIONS[4:8]},
            {"type": "count_people",  "questions": COUNTING_QUESTIONS[:4]},
            {"type": "where_belongs", "questions": WHERE_BELONGS_QUESTIONS[4:8]},
            {"type": "who_is_this",   "questions": FAMILY_WHO_QUESTIONS[2:5]},
            {"type": "circle_group",  "questions": CIRCLE_GROUP_QUESTIONS[4:8]},
        ],
    },
    # Exam 5 – Fun Challenge
    {
        "title": "Exam 5: Fun Challenge",
        "filename": "exam_5_fun_challenge.pdf",
        "sections": [
            {"type": "title_page",    "exam_name": "Fun Challenge Exam", "exam_number": 5},
            {"type": "match_family",  "set_index": 1},
            {"type": "circle_group",  "questions": CIRCLE_GROUP_QUESTIONS[6:10]},
            {"type": "circle_in_room","questions": CIRCLE_IN_ROOM_QUESTIONS[2:5]},
            {"type": "whats_wrong",   "questions": WHATS_WRONG_QUESTIONS[2:5]},
            {"type": "count_write",   "questions": COUNTING_QUESTIONS[:5]},
        ],
    },
]

# Template for extra exams generated when --count > 5
EXTRA_EXAM_TEMPLATE = {
    "sections_pool": [
        {"type": "circle_family", "questions": FAMILY_CIRCLE_QUESTIONS},
        {"type": "who_is_this",   "questions": FAMILY_WHO_QUESTIONS},
        {"type": "count_people",  "questions": COUNTING_QUESTIONS},
        {"type": "circle_group",  "questions": CIRCLE_GROUP_QUESTIONS},
        {"type": "where_belongs", "questions": WHERE_BELONGS_QUESTIONS},
        {"type": "circle_in_room","questions": CIRCLE_IN_ROOM_QUESTIONS},
        {"type": "whats_wrong",   "questions": WHATS_WRONG_QUESTIONS},
        {"type": "match_family",  "set_index": 2},
        {"type": "draw_line_numbers", "pairs": list(zip(range(1, 6), range(1, 6)))},
    ]
}
