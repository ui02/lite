
import json
import re
import html
import urllib.request
import xml.etree.ElementTree as ET

from html.parser import HTMLParser
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime


RSS_URL = "https://uilx02.tumblr.com/rss"
OUTPUT_FILE = Path("_data/murmur.json")
IMAGE_DIR = Path("assets/images/murmur")

USER_AGENT = "Mozilla/5.0 (compatible; IOLITE Murmur Feed)"


class ImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        if tag != "meta":
            return

        attrs = dict(attrs)

        # og:imageだけ取得。secure_urlは重複するので取得しない
        if attrs.get("property") == "og:image":
            url = attrs.get("content")

            if url and url not in self.images:
                self.images.append(url)


def fetch(url):
    request = urllib.request.Request(
        url,
        headers={"User-Agent": USER_AGENT}
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read()


def clean_text(value):
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", "", value)
    return re.sub(r"\s+", " ", value).strip()


def get_post_id(url):
    match = re.search(r"/post/(\d+)", url or "")
    return match.group(1) if match else None


def get_images(post_url, post_id, date):
    try:
        page = fetch(post_url).decode("utf-8", errors="replace")

        parser = ImageParser()
        parser.feed(page)

        year, month = date.split("/")[:2]
        folder = IMAGE_DIR / year / month
        folder.mkdir(parents=True, exist_ok=True)

        saved_images = []

        for index, image_url in enumerate(parser.images, start=1):
            parsed = urlparse(image_url)
            extension = Path(parsed.path).suffix.lower()

            if extension not in (
                ".jpg", ".jpeg", ".png", ".gif", ".webp"
            ):
                extension = ".jpg"

            filename = f"{post_id}-{index:02d}{extension}"
            filepath = folder / filename

            if not filepath.exists():
                filepath.write_bytes(fetch(image_url))

            saved_images.append(
                str(filepath).replace("\\", "/")
            )

        return saved_images

    except Exception as error:
        print(f"Image fetch failed: {post_url} ({error})")
        return []


def main():
    # 既存データを読み込む
    if OUTPUT_FILE.exists():
        data = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
    else:
        data = {"posts": []}

    posts = data.get("posts", [])

    # 既存投稿IDを記録
    existing_ids = {
        post["id"] for post in posts
        if post.get("id")
    }

    # Tumblr RSSを取得
    rss = fetch(RSS_URL)
    root = ET.fromstring(rss)

    new_count = 0

    for item in root.findall("./channel/item"):
        url = item.findtext("link", "").strip()
        post_id = get_post_id(
            item.findtext("guid", "") or url
        )

        if not post_id or post_id in existing_ids:
            continue

        # murmursタグの投稿だけを対象にする
        categories = [
            (category.text or "").strip().lower()
            for category in item.findall("category")
        ]

        if "murmurs" not in categories:
            continue

        title = clean_text(item.findtext("title", ""))
        description = clean_text(
            item.findtext("description", "")
        )

        text = description or title

        pub_date = item.findtext("pubDate", "")

        try:
            date = parsedate_to_datetime(pub_date)
            date_text = date.strftime("%Y/%m/%d")
            timestamp = date.timestamp()
        except Exception:
            date_text = ""
            timestamp = 0

        # 投稿ページから画像を取得して保存
        images = get_images(url, post_id, date_text) if date_text else []

        posts.append({
            "id": post_id,
            "date": date_text,
            "timestamp": timestamp,
            "text": text,
            "url": url,
            "images": images
        })

        existing_ids.add(post_id)
        new_count += 1

        print(f"Added: {post_id} ({len(images)} images)")

    # 新しい投稿を先頭にする
    posts.sort(
        key=lambda post: post.get("timestamp", 0),
        reverse=True
    )

    data = {"posts": posts}

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"Murmur updated. New posts: {new_count}")
    print(f"Total posts: {len(posts)}")


if __name__ == "__main__":
    main()
