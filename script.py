import os
from bs4 import BeautifulSoup

INPUT_DIR = "html"
OUTPUT_FILE = "output.md"

posts = []

for file in os.listdir(INPUT_DIR):
    if not file.endswith(".html"):
        continue

    path = os.path.join(INPUT_DIR, file)

    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # timestamp
    ts = soup.find("span", id="timestamp")
    timestamp = ts.get_text(strip=True) if ts else ""

    # tags
    tags = [t.get_text(strip=True) for t in soup.find_all("span", class_="tag")]

    # caption
    captions = []
    for p in soup.find_all("p"):
        text = p.get_text(strip=True)
        if text:
            captions.append(text)

    caption = "\n".join(captions)

    # image
    img = soup.find("img")
    img_url = img["src"] if img else ""

    md = f"""
## {file}

**date:** {timestamp}

**tags:** {", ".join(tags)}

![]({img_url})

{caption}

---
"""

    posts.append(md)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(posts))

print("DONE → output.md")