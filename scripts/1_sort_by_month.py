import os
import re
import shutil
from bs4 import BeautifulSoup
from datetime import datetime

HTML_DIR = "html"

for filename in os.listdir(HTML_DIR):

    if not filename.endswith(".html"):
        continue

    path = os.path.join(HTML_DIR, filename)

    with open(path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    timestamp = soup.find("span", id="timestamp")

    if not timestamp:
        print(f"SKIP: {filename}")
        continue

    text = timestamp.get_text(strip=True)

    # May 8th, 2025 1:39am
    text = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', text)

    dt = datetime.strptime(text, "%B %d, %Y %I:%M%p")

    folder = dt.strftime("%Y-%m")

    os.makedirs(folder, exist_ok=True)

    shutil.move(
        path,
        os.path.join(folder, filename)
    )

    print(f"{filename} -> {folder}")