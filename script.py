import re

INPUT_FILE = "output.md"
OUTPUT_FILE = "timeline.md"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# 1投稿ごとに分割（---区切り）
posts = text.split("---")

result = []

for post in posts:
    if "date:" not in post:
        continue

    # date
    date = re.search(r"\*\*date:\*\*\s*(.*)", post)
    date = date.group(1).strip() if date else ""

    # tags
    tags = re.search(r"\*\*tags:\*\*\s*(.*)", post)
    tags = tags.group(1).strip() if tags else ""

    # image
    img = re.search(r"!\[\]\((.*?)\)", post)
    img = img.group(1).strip() if img else ""

    # caption（画像以降）
    caption = re.split(r"\!\[\]\(.*?\)", post)
    caption = caption[1].strip() if len(caption) > 1 else ""

    # timeline形式に変換
    block = f'''{{{{< timelineItem icon="twitter" header="" badge="{tags}" subheader="{date}" >}}}}
  <img src="{img}">
{caption}
{{{{< /timelineItem >}}}}

'''

    result.append(block)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(result))

print("DONE → timeline.md")