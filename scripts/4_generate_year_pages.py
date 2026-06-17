import csv
import os
import re
from collections import defaultdict

CSV_FILE = "data/murmur/catalog.csv"
OUTPUT_DIR = "content/murmur/generated"

os.makedirs(OUTPUT_DIR, exist_ok=True)

posts_by_year = defaultdict(list)

with open(CSV_FILE, encoding="utf-8-sig") as f:

    reader = csv.DictReader(f)

    for row in reader:
        posts_by_year[row["year"]].append(row)

for year, posts in posts_by_year.items():

    md = f"""---
title: "{year}"

date: {year}-01-01

categories: ["murmur"]

tags: [""]

summary: ""

showSummary: false

draft: false
---

{{{{< timeline >}}}}

"""

    for post in posts:

        title = post["title"].strip()
        date = post["date"]

        if title:
            md += (
                f'{{{{< timelineItem icon="tumblr" '
                f'header="{title}" '
                f'subheader="{date}" >}}}}\n'
            )
        else:
            md += (
                f'{{{{< timelineItem icon="tumblr" '
                f'subheader="{date}" >}}}}\n'
            )

        image_files = [
            x for x in post["image_files"].split("|")
            if x.strip()
        ]

        if image_files:

            md += "{{< gallery >}}\n"

            for img in image_files:

                md += (
                    f'<img src="/murmur/{img}" '
                    f'class="grid-w50">\n'
                )

            md += "{{< /gallery >}}\n\n"

        text = post["text"].strip()

        if text:
            md += text + "\n\n"

        tags = []

        for tag in post["tags"].split("|"):

            tag = tag.strip()

            if not tag:
                continue

            # 年タグ除外
            if re.fullmatch(r"\d{4}", tag):
                continue

            tags.append(tag)

        if tags:

            for tag in tags:
                md += (
                    f"{{{{< badge >}}}}"
                    f"{tag}"
                    f"{{{{< /badge >}}}} "
                )

            md += "\n\n"

        md += "{{< /timelineItem >}}\n\n"

    md += "{{< /timeline >}}\n"

    with open(
        os.path.join(
            OUTPUT_DIR,
            f"{year}.md"
        ),
        "w",
        encoding="utf-8"
    ) as f:

        f.write(md)

    print("generated", year)