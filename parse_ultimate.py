import pdfplumber
import json

categories = {
    "do_not_draft": [],
    "do_draft": [],
    "schefter_targets": [],
    "more_tds": [],
    "fewer_tds": [],
    "late_round_fliers": [],
    "insurance_rbs": [],
    "draft_day_values": [],
    "fields_favorites": []
}

with pdfplumber.open('NFL26_CS_ULTIMATE.pdf') as pdf:
    page = pdf.pages[0]
    words = page.extract_words(keep_blank_chars=False)

    # We need to cluster words into lines, and then split by x0 coordinate to figure out which column they are in.
    # Actually, a simpler way is to extract text with layout, and then just string slice each line!
    text = page.extract_text(layout=True)
    lines = text.split('\n')

    current_col1 = None
    current_col2 = None
    current_col3 = None
    current_col4 = None

    for line in lines:
        if not line.strip():
            continue
        
        # Determine column boundaries based on typical layout (approximate char indices)
        # Line width is around 120 chars.
        # col1: 0 to 32
        # col2: 33 to 60
        # col3: 61 to 90
        # col4: 91+
        # Let's verify by just printing a sample line
        pass

# Instead of layout text parsing which is brittle, let's use bounding boxes.
# Divide page into 4 columns by x coordinate.
page_width = 792 # 11 inches * 72
col_width = page_width / 4

cols = [[], [], [], []]
with pdfplumber.open('NFL26_CS_ULTIMATE.pdf') as pdf:
    page = pdf.pages[0]
    for word in page.extract_words():
        x0 = word['x0']
        if x0 < col_width:
            cols[0].append(word)
        elif x0 < col_width * 2:
            cols[1].append(word)
        elif x0 < col_width * 3:
            cols[2].append(word)
        else:
            cols[3].append(word)

def extract_names_from_col(words):
    # group words by bottom coordinate (y1) to form lines
    lines = {}
    for w in words:
        # round to nearest 2 to group
        y = round(w['bottom'] / 2) * 2
        if y not in lines:
            lines[y] = []
        lines[y].append(w)
    
    sorted_y = sorted(lines.keys())
    text_lines = []
    for y in sorted_y:
        line_words = sorted(lines[y], key=lambda w: w['x0'])
        text = " ".join([w['text'] for w in line_words])
        text_lines.append(text)
    return text_lines

for i in range(4):
    print(f"--- COL {i} ---")
    lines = extract_names_from_col(cols[i])
    for l in lines[:15]:
        print(l)
    print("...")

