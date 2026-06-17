import os
import csv
import re
from datetime import datetime
from bs4 import BeautifulSoup

rows = []

for root, dirs, files in os.walk("html"):

    for file in files:

        if not file.endswith(".html"):
            continue

        path = os.path.join(root, file)

        try:

            with open(path, "r", encoding="utf-8") as f:
                soup = BeautifulSoup(f.read(), "html.parser")

            # 元タイムスタンプ
            timestamp_tag = soup.find("span", id="timestamp")

            timestamp = (
                timestamp_tag.get_text(strip=True)
                if timestamp_tag else ""
            )

            # 表示用日付
            date = ""

            if timestamp:

                try:

                    clean_date = (
                        timestamp.replace("st,", ",")
                                 .replace("nd,", ",")
                                 .replace("rd,", ",")
                                 .replace("th,", ",")
                    )

                    dt = datetime.strptime(
                        clean_date,
                        "%B %d, %Y %I:%M%p"
                    )

                    date = dt.strftime("%Y/%m/%d")

                    year = dt.strftime("%Y")
                    month = dt.strftime("%m")

                except Exception:

                    date = timestamp
                    year = ""
                    month = ""

            else:

                year = ""
                month = ""

            # タイトル
            h1s = soup.find_all("h1")

            title = ""

            for h in h1s:
                txt = h.get_text(strip=True)

                if txt:
                    title = txt
                    break

            # 本文
            text_parts = []

            for tag in soup.find_all(["p", "blockquote"]):

                txt = tag.get_text(" ", strip=True)

                if txt:
                    text_parts.append(txt)

            text = "\n".join(text_parts)


            # タグ
            tags = [
                t.get_text(strip=True)
                for t in soup.find_all("span", class_="tag")
            ]

            # 画像一覧取得
            image_files = []

            for img in soup.find_all("img"):

                src = img.get("src", "")

                if src:
                    image_files.append(
                        os.path.basename(src)
                    )

            image_count = len(image_files)

            rows.append([
                date,
                timestamp,
                year,
                month,
                title,
                text,
                "|".join(tags),
                image_count,
                "|".join(image_files),
                file
            ])

        except Exception as e:

            print("ERROR:", file, e)

# 日付順にソート
rows.sort(key=lambda x: x[0])

with open(
    "catalog.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as f:

    writer = csv.writer(f)

    writer.writerow([
        "date",
        "timestamp",
        "year",
        "month",
        "title",
        "text",
        "tags",
        "image_count",
        "image_files",
        "source_file"
    ])

    writer.writerows(rows)

print(f"DONE: {len(rows)} posts")