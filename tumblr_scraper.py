import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin

BASE_URL = "https://iolite36.tumblr.com"
OUTPUT_FILE = "timeline.md"

headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_post_links():
    urls = set()

    page = BASE_URL
    for _ in range(5):
        res = requests.get(page, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        for a in soup.find_all("a", href=True):
            if "/post/" in a["href"]:
                urls.add(urljoin(BASE_URL, a["href"]))

        next_page = soup.find("a", {"class": "next"})
        if next_page and next_page.get("href"):
            page = urljoin(BASE_URL, next_page["href"])
        else:
            break

    return list(urls)


# 投稿ページ解析
def parse_post(url):
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")

    # 画像
    img = soup.find("img")
    img_url = img["src"] if img else ""

    # 本文
    ps = soup.find_all("p")
    caption = "\n".join([p.get_text(strip=True) for p in ps])

    # タグ
    tags = [t.get_text(strip=True) for t in soup.find_all("a") if "tagged" in t.get("href", "")]

    # 日付（かなりラフ）
    time_tag = soup.find("time")
    date = time_tag.get_text(strip=True) if time_tag else ""

    return {
        "url": url,
        "img": img_url,
        "caption": caption,
        "tags": tags,
        "date": date
    }


def to_md(post):
    tag_md = "".join([f'  {{< badge >}}{t}{{< /badge >}}\n' for t in post["tags"]])

    return f"""
{{{{< timelineItem icon="tumblr" subheader="{post['date']}" >}}}}
  <img src="{post['img']}">
  {post['caption']}
{tag_md}{{{{< /timelineItem >}}}}
"""


posts = []

print("collecting links...")
links = get_post_links()

print("found:", len(links))

for i, url in enumerate(links):
    try:
        print(f"[{i+1}/{len(links)}] {url}")
        post = parse_post(url)
        posts.append(to_md(post))
        time.sleep(0.5)
    except Exception as e:
        print("error:", url, e)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(posts))

print("DONE → timeline.md")