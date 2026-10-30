"""Canonical list of the 66 books.

Each entry: (number, OSIS id, English name, testament).
Numbering follows the common English/Protestant order (1-66).
TANAKH_ORDER gives the traditional Hebrew order used in BHS/BHQ printed editions.
"""

BOOKS = [
    (1, "Gen", "Genesis", "OT"), (2, "Exod", "Exodus", "OT"),
    (3, "Lev", "Leviticus", "OT"), (4, "Num", "Numbers", "OT"),
    (5, "Deut", "Deuteronomy", "OT"), (6, "Josh", "Joshua", "OT"),
    (7, "Judg", "Judges", "OT"), (8, "Ruth", "Ruth", "OT"),
    (9, "1Sam", "1 Samuel", "OT"), (10, "2Sam", "2 Samuel", "OT"),
    (11, "1Kgs", "1 Kings", "OT"), (12, "2Kgs", "2 Kings", "OT"),
    (13, "1Chr", "1 Chronicles", "OT"), (14, "2Chr", "2 Chronicles", "OT"),
    (15, "Ezra", "Ezra", "OT"), (16, "Neh", "Nehemiah", "OT"),
    (17, "Esth", "Esther", "OT"), (18, "Job", "Job", "OT"),
    (19, "Ps", "Psalms", "OT"), (20, "Prov", "Proverbs", "OT"),
    (21, "Eccl", "Ecclesiastes", "OT"), (22, "Song", "Song of Songs", "OT"),
    (23, "Isa", "Isaiah", "OT"), (24, "Jer", "Jeremiah", "OT"),
    (25, "Lam", "Lamentations", "OT"), (26, "Ezek", "Ezekiel", "OT"),
    (27, "Dan", "Daniel", "OT"), (28, "Hos", "Hosea", "OT"),
    (29, "Joel", "Joel", "OT"), (30, "Amos", "Amos", "OT"),
    (31, "Obad", "Obadiah", "OT"), (32, "Jonah", "Jonah", "OT"),
    (33, "Mic", "Micah", "OT"), (34, "Nah", "Nahum", "OT"),
    (35, "Hab", "Habakkuk", "OT"), (36, "Zeph", "Zephaniah", "OT"),
    (37, "Hag", "Haggai", "OT"), (38, "Zech", "Zechariah", "OT"),
    (39, "Mal", "Malachi", "OT"),
    (40, "Matt", "Matthew", "NT"), (41, "Mark", "Mark", "NT"),
    (42, "Luke", "Luke", "NT"), (43, "John", "John", "NT"),
    (44, "Acts", "Acts", "NT"), (45, "Rom", "Romans", "NT"),
    (46, "1Cor", "1 Corinthians", "NT"), (47, "2Cor", "2 Corinthians", "NT"),
    (48, "Gal", "Galatians", "NT"), (49, "Eph", "Ephesians", "NT"),
    (50, "Phil", "Philippians", "NT"), (51, "Col", "Colossians", "NT"),
    (52, "1Thess", "1 Thessalonians", "NT"), (53, "2Thess", "2 Thessalonians", "NT"),
    (54, "1Tim", "1 Timothy", "NT"), (55, "2Tim", "2 Timothy", "NT"),
    (56, "Titus", "Titus", "NT"), (57, "Phlm", "Philemon", "NT"),
    (58, "Heb", "Hebrews", "NT"), (59, "Jas", "James", "NT"),
    (60, "1Pet", "1 Peter", "NT"), (61, "2Pet", "2 Peter", "NT"),
    (62, "1John", "1 John", "NT"), (63, "2John", "2 John", "NT"),
    (64, "3John", "3 John", "NT"), (65, "Jude", "Jude", "NT"),
    (66, "Rev", "Revelation", "NT"),
]

# Torah, Nevi'im, Ketuvim (BHS order).
TANAKH_ORDER = [
    "Gen", "Exod", "Lev", "Num", "Deut",
    "Josh", "Judg", "1Sam", "2Sam", "1Kgs", "2Kgs", "Isa", "Jer", "Ezek",
    "Hos", "Joel", "Amos", "Obad", "Jonah", "Mic", "Nah", "Hab", "Zeph", "Hag", "Zech", "Mal",
    "Ps", "Job", "Prov", "Ruth", "Song", "Eccl", "Lam", "Esth", "Dan", "Ezra", "Neh", "1Chr", "2Chr",
]

# Passages written in Aramaic rather than Hebrew.
ARAMAIC = {
    "Gen": ["31:47 (two words)"],
    "Jer": ["10:11"],
    "Dan": ["2:4b-7:28"],
    "Ezra": ["4:8-6:18", "7:12-26"],
}


def slug(name):
    return name.lower().replace(" ", "-")


def file_stem(num, name):
    return f"{num:02d}-{slug(name)}"

