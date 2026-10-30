"""The kings of Israel and Judah: a chart of their reigns, side by side, with the prophets of
their times. Writes kings.html.

    python3 scripts/kings.py

The years are Edwin R. Thiele's (The Mysterious Numbers of the Hebrew Kings, 3rd ed., 1983),
the reckoning most charts follow; other chronologies differ by a few years, and the early dates
by more. A co-regency, when a son reigned beside his father, is the first year given ("co")
before the year the son reigned alone. Each reign's length and verdict are as the Bible gives
them, with the verses.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import webpages                                  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# name, start (BC), co-regency start or None, end (BC), the Bible's length, verdict, verses,
# Chronicles' account. Verdict: good, evil, mixed (both said), none (no verdict given).
UNITED = [
    ("Saul", 1050, None, 1010, "42 years (1 Samuel 13:1, partly lost in the Hebrew)", "mixed", "1 Samuel 9–31", "1 Chronicles 10"),
    ("David", 1010, None, 970, "40 years (2 Samuel 5:4)", "good", "2 Samuel 2–24; 1 Kings 1–2", "1 Chronicles 11–29"),
    ("Solomon", 970, None, 931, "40 years (1 Kings 11:42)", "mixed", "1 Kings 1–11", "2 Chronicles 1–9"),
]
JUDAH = [
    ("Rehoboam", 931, None, 913, "17 years (1 Kings 14:21)", "evil", "1 Kings 12:1–24; 14:21–31", "2 Chronicles 10–12"),
    ("Abijah", 913, None, 911, "3 years (1 Kings 15:2)", "evil", "1 Kings 15:1–8", "2 Chronicles 13"),
    ("Asa", 911, None, 870, "41 years (1 Kings 15:10)", "good", "1 Kings 15:9–24", "2 Chronicles 14–16"),
    ("Jehoshaphat", 870, 873, 848, "25 years (1 Kings 22:42)", "good", "1 Kings 22:1–50", "2 Chronicles 17–20"),
    ("Jehoram", 848, 853, 841, "8 years (2 Kings 8:17)", "evil", "2 Kings 8:16–24", "2 Chronicles 21"),
    ("Ahaziah", 841, None, 841, "1 year (2 Kings 8:26)", "evil", "2 Kings 8:25–29; 9:27–29", "2 Chronicles 22:1–9"),
    ("Athaliah", 841, None, 835, "6 years (2 Kings 11:3)", "evil", "2 Kings 11", "2 Chronicles 22:10–23:21"),
    ("Joash", 835, None, 796, "40 years (2 Kings 12:2)", "good", "2 Kings 12", "2 Chronicles 24"),
    ("Amaziah", 796, None, 767, "29 years (2 Kings 14:2)", "good", "2 Kings 14:1–22", "2 Chronicles 25"),
    ("Uzziah", 767, 792, 740, "52 years (2 Kings 15:2)", "good", "2 Kings 15:1–7", "2 Chronicles 26"),
    ("Jotham", 740, 750, 732, "16 years (2 Kings 15:33)", "good", "2 Kings 15:32–38", "2 Chronicles 27"),
    ("Ahaz", 732, 735, 716, "16 years (2 Kings 16:2)", "evil", "2 Kings 16", "2 Chronicles 28"),
    ("Hezekiah", 716, None, 687, "29 years (2 Kings 18:2)", "good", "2 Kings 18–20", "2 Chronicles 29–32"),
    ("Manasseh", 687, 697, 643, "55 years (2 Kings 21:1)", "evil", "2 Kings 21:1–18", "2 Chronicles 33:1–20"),
    ("Amon", 643, None, 641, "2 years (2 Kings 21:19)", "evil", "2 Kings 21:19–26", "2 Chronicles 33:21–25"),
    ("Josiah", 641, None, 609, "31 years (2 Kings 22:1)", "good", "2 Kings 22:1–23:30", "2 Chronicles 34–35"),
    ("Jehoahaz", 609, None, 609, "3 months (2 Kings 23:31)", "evil", "2 Kings 23:31–34", "2 Chronicles 36:1–4"),
    ("Jehoiakim", 609, None, 598, "11 years (2 Kings 23:36)", "evil", "2 Kings 23:34–24:7", "2 Chronicles 36:5–8"),
    ("Jehoiachin", 598, None, 597, "3 months (2 Kings 24:8)", "evil", "2 Kings 24:8–17; 25:27–30", "2 Chronicles 36:9–10"),
    ("Zedekiah", 597, None, 586, "11 years (2 Kings 24:18)", "evil", "2 Kings 24:18–25:7", "2 Chronicles 36:11–21"),
]
ISRAEL = [
    ("Jeroboam", 931, None, 910, "22 years (1 Kings 14:20)", "evil", "1 Kings 11:26–14:20", "2 Chronicles 10; 13"),
    ("Nadab", 910, None, 909, "2 years (1 Kings 15:25)", "evil", "1 Kings 15:25–31", None),
    ("Baasha", 909, None, 886, "24 years (1 Kings 15:33)", "evil", "1 Kings 15:27–16:7", "2 Chronicles 16:1–6"),
    ("Elah", 886, None, 885, "2 years (1 Kings 16:8)", "evil", "1 Kings 16:8–14", None),
    ("Zimri", 885, None, 885, "7 days (1 Kings 16:15)", "evil", "1 Kings 16:9–20", None),
    ("Tibni", 885, None, 880, "a rival king, with no years given (1 Kings 16:21–22)", "none", "1 Kings 16:21–22", None),
    ("Omri", 880, 885, 874, "12 years (1 Kings 16:23)", "evil", "1 Kings 16:16–28", None),
    ("Ahab", 874, None, 853, "22 years (1 Kings 16:29)", "evil", "1 Kings 16:29–22:40", "2 Chronicles 18"),
    ("Ahaziah of Israel", 853, None, 852, "2 years (1 Kings 22:52)", "evil", "1 Kings 22:51–2 Kings 1:18", "2 Chronicles 20:35–37"),
    ("Joram", 852, None, 841, "12 years (2 Kings 3:1)", "evil", "2 Kings 3; 9:14–26", None),
    ("Jehu", 841, None, 814, "28 years (2 Kings 10:36)", "mixed", "2 Kings 9–10", "2 Chronicles 22:7–9"),
    ("Jehoahaz of Israel", 814, None, 798, "17 years (2 Kings 13:1)", "evil", "2 Kings 13:1–9", None),
    ("Jehoash", 798, None, 782, "16 years (2 Kings 13:10)", "evil", "2 Kings 13:10–25; 14:8–16", "2 Chronicles 25:17–24"),
    ("Jeroboam II", 782, 793, 753, "41 years (2 Kings 14:23)", "evil", "2 Kings 14:23–29", None),
    ("Zechariah", 753, None, 753, "6 months (2 Kings 15:8)", "evil", "2 Kings 15:8–12", None),
    ("Shallum", 752, None, 752, "1 month (2 Kings 15:13)", "none", "2 Kings 15:10–15", None),
    ("Menahem", 752, None, 742, "10 years (2 Kings 15:17)", "evil", "2 Kings 15:14–22", None),
    ("Pekahiah", 742, None, 740, "2 years (2 Kings 15:23)", "evil", "2 Kings 15:23–26", None),
    ("Pekah", 740, 752, 732, "20 years (2 Kings 15:27), counted from a rival reign in Gilead", "evil", "2 Kings 15:25–31; 16:5", "2 Chronicles 28:5–8"),
    ("Hoshea", 732, None, 722, "9 years (2 Kings 17:1)", "evil", "2 Kings 15:30; 17:1–6", None),
]
# The prophets of the kings' times: name, from, to (about), where they are found.
PROPHETS = [
    ("Samuel", 1070, 1015, "1 Samuel 3–25"), ("Nathan", 1000, 965, "2 Samuel 7; 12; 1 Kings 1"),
    ("Ahijah", 935, 910, "1 Kings 11:29–39; 14:1–18"), ("Elijah", 870, 850, "1 Kings 17–2 Kings 2"),
    ("Elisha", 850, 795, "2 Kings 2–13"), ("Jonah", 790, 770, "2 Kings 14:25; Jonah"),
    ("Amos", 765, 755, "Amos 1:1"), ("Hosea", 755, 715, "Hosea 1:1"), ("Isaiah", 740, 685, "Isaiah 1:1; 6:1"),
    ("Micah", 735, 700, "Micah 1:1"), ("Nahum", 660, 630, "Nahum"), ("Zephaniah", 640, 620, "Zephaniah 1:1"),
    ("Jeremiah", 627, 586, "Jeremiah 1:1–3"), ("Habakkuk", 610, 595, "Habakkuk"), ("Huldah", 622, 620, "2 Kings 22:14–20"),
    ("Ezekiel", 593, 571, "Ezekiel 1:1–3"),
]
VERDICT = {
    "good": "Did what was right in the eyes of the LORD",
    "evil": "Did what was evil in the eyes of the LORD",
    "mixed": "Praised and blamed: the account gives both",
    "none": "The account gives no verdict",
}


def rows(lst):
    return [{"n": n, "a": a, "co": co, "z": z, "len": ln, "v": v, "ref": ref, "chr": ch} for n, a, co, z, ln, v, ref, ch in lst]


def main():
    data = {"united": rows(UNITED), "judah": rows(JUDAH), "israel": rows(ISRAEL),
            "prophets": [{"n": n, "a": a, "z": z, "ref": ref} for n, a, z, ref in PROPHETS], "verdict": VERDICT}
    with open(os.path.join(ROOT, "kings.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(webpages.document(webpages.page("kings", data)))
    print(f"{len(UNITED) + len(JUDAH) + len(ISRAEL)} reigns, {len(PROPHETS)} prophets")


if __name__ == "__main__":
    main()
