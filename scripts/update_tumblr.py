import json
import re
import html
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from email.utils import parsedate_to_datetime
from pathlib import Path
from zoneinfo import ZoneInfo


RSS_URL = "https://uilx02.tumblr.com/rss"
OUTPUT_FILE = Path("_data/tumblr.json")
USER_AGENT = "Mozilla/5.0 (compatible; IOLITE Tumblr Feed)"


class ImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.image = None

    def handle_starttag(self, tag, attrs):
        if tag != "meta":
            return

        attrs = dict(attrs)

        if attrs.get("property") == "og:image":
            self.image = attrs.get("content")


def fetch(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT}
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def clean_text(value):
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", value).strip()


def get_image(post_url):
    try:
        page = fetch(post_url).decode("utf-8", errors="replace")
        parser = ImageParser()
        parser.feed(page)
        return parser.image
    except Exception as error:
        print(f"Image fetch failed: {post_url} ({error})")
        return None


def main():
    rss = fetch(RSS_URL)
    root = ET.fromstring(rss)

    items = root.findall("./channel/item")

    # 本文：最新3件
    posts = []

    for item in items[:3]:
        title = clean_text(item.findtext("title", ""))
        description = clean_text(item.findtext("description", ""))
        url = item.findtext("link", "")
        pub_date = item.findtext("pubDate", "")

        try:
            date = parsedate_to_datetime(pub_date)
            date = date.astimezone(ZoneInfo("Asia/Tokyo"))
            date_text = date.strftime("%m/%d - %H:%M")
        except Exception:
            date_text = ""

        text = description or title

        posts.append({
            "date": date_text,
            "text": text[:40],
            "url": url
        })

    # 写真：画像が見つかった投稿から最新3件
    images = []

    for item in items:
        if len(images) >= 3:
            break

        url = item.findtext("link", "")

        if not url:
            continue

        candidate = get_image(url)

        if candidate:
            images.append({
                "image_url": candidate,
                "image_link": url
            })

    # 既存の単数形データも残す
    image_url = images[0]["image_url"] if images else None
    image_link = images[0]["image_link"] if images else None

    data = {
        "image_url": image_url,
        "image_link": image_link,
        "images": images,
        "posts": posts
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print("Tumblr feed updated.")


if __name__ == "__main__":
    main()
