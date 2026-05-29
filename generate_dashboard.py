import os
import datetime
import subprocess
from collections import defaultdict

# ── CONFIG ──────────────────────────────────────────────
HDLBITS_PROGRESS  = r"C:\Users\laksh\hdlbits-solutions\PROGRESS.md"
LEETCODE_PROGRESS = r"C:\Users\laksh\neetcode-submissions\PROGRESS.md"
OUTPUT_SVG        = r"C:\Users\laksh\lakshhnaa\activity.svg"
# ────────────────────────────────────────────────────────

def read_dates(filepath):
    dates = set()
    try:
        with open(filepath, encoding="utf-8") as f:
            for line in f:
                if line.startswith("|") and "Date" not in line and "---" not in line:
                    parts = [p.strip() for p in line.split("|")]
                    if len(parts) > 1:
                        try:
                            datetime.date.fromisoformat(parts[1])
                            dates.add(parts[1])
                        except:
                            pass
    except FileNotFoundError:
        pass
    return dates

def generate_svg(hdl_dates, leet_dates):
    today     = datetime.date.today()
    start     = today - datetime.timedelta(weeks=26)
    # align to Monday
    start     = start - datetime.timedelta(days=start.weekday())

    CELL      = 14
    GAP       = 3
    COLS      = 27
    ROWS      = 7
    PAD_LEFT  = 30
    PAD_TOP   = 40
    WIDTH     = PAD_LEFT + COLS * (CELL + GAP) + 20
    HEIGHT    = PAD_TOP  + ROWS * (CELL + GAP) + 60

    # colors
    EMPTY     = "#1e1e2e"
    LEET      = "#238636"  # green
    HDL       = "#9333ea"  # purple
    BOTH      = "#3b82f6"  # blue
    TEXT      = "#8b949e"

    days = []
    d = start
    while d <= today:
        days.append(d)
        d += datetime.timedelta(days=1)

    cells = ""
    for i, day in enumerate(days):
        col = i // 7
        row = i %  7
        x   = PAD_LEFT + col * (CELL + GAP)
        y   = PAD_TOP  + row * (CELL + GAP)
        ds  = day.isoformat()
        in_leet = ds in leet_dates
        in_hdl  = ds in hdl_dates
        if in_leet and in_hdl:
            color = BOTH
        elif in_leet:
            color = LEET
        elif in_hdl:
            color = HDL
        else:
            color = EMPTY
        cells += f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="3" fill="{color}"/>\n'

    # month labels
    months = ""
    prev_month = None
    for i, day in enumerate(days):
        if day.month != prev_month:
            col = i // 7
            x   = PAD_LEFT + col * (CELL + GAP)
            months += f'<text x="{x}" y="{PAD_TOP - 6}" font-size="10" fill="{TEXT}" font-family="monospace">{day.strftime("%b")}</text>\n'
            prev_month = day.month

    # legend
    legend_y = PAD_TOP + ROWS * (CELL + GAP) + 16
    legend = f"""
    <rect x="{PAD_LEFT}"      y="{legend_y}" width="12" height="12" rx="2" fill="{LEET}"/>
    <text x="{PAD_LEFT + 16}" y="{legend_y + 10}" font-size="10" fill="{TEXT}" font-family="monospace">LeetCode</text>
    <rect x="{PAD_LEFT + 80}" y="{legend_y}" width="12" height="12" rx="2" fill="{HDL}"/>
    <text x="{PAD_LEFT + 96}" y="{legend_y + 10}" font-size="10" fill="{TEXT}" font-family="monospace">HDLBits</text>
    <rect x="{PAD_LEFT + 160}" y="{legend_y}" width="12" height="12" rx="2" fill="{BOTH}"/>
    <text x="{PAD_LEFT + 176}" y="{legend_y + 10}" font-size="10" fill="{TEXT}" font-family="monospace">Both</text>
    """

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" style="background:#0d1117">
    <text x="{PAD_LEFT}" y="22" font-size="14" fill="white" font-family="monospace" font-weight="bold">📊 Coding Activity</text>
    {months}
    {cells}
    {legend}
    </svg>"""

    with open(OUTPUT_SVG, "w", encoding="utf-8") as f:
        f.write(svg)
    print("✅ activity.svg generated!")

def push():
    os.chdir(r"C:\Users\laksh\lakshhnaa")
    subprocess.run(["git", "add", "activity.svg"])
    subprocess.run(["git", "commit", "-m", "update: activity dashboard"])
    subprocess.run(["git", "push"])
    print("✅ Pushed to GitHub profile!")

if __name__ == "__main__":
    hdl_dates  = read_dates(HDLBITS_PROGRESS)
    leet_dates = read_dates(LEETCODE_PROGRESS)
    generate_svg(hdl_dates, leet_dates)
    push()