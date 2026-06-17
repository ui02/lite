import csv
from collections import Counter

year_counter = Counter()
tag_counter = Counter()

total_posts = 0
total_images = 0

with open("catalog.csv", encoding="utf-8-sig") as f:

    reader = csv.DictReader(f)

    for row in reader:

        total_posts += 1

        # 年別集計
        year = row["year"]

        if year:
            year_counter[year] += 1

        # 画像数
        try:
            total_images += int(row["images"])
        except:
            pass

        # タグ集計
        tags = row["tags"]

        if tags:
            for tag in tags.split(","):
                tag = tag.strip()

                if tag:
                    tag_counter[tag] += 1

print()
print("========== Tumblr Analysis ==========")
print()

print(f"総投稿数: {total_posts}")
print(f"総画像数: {total_images}")

print()
print("----- 年別投稿数 -----")

for year, count in sorted(year_counter.items()):
    print(f"{year}: {count}")

print()
print("----- タグランキング TOP20 -----")

for tag, count in tag_counter.most_common(20):
    print(f"{count:4d}  {tag}")

print()
print("====================================")