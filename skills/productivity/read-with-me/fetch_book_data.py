#!/usr/bin/env python3
"""微信读书取数脚本 - read-with-me skill 专用
用法: python3 fetch_book_data.py <bookId>
输出: JSON 格式，包含 progress、bookmarks、bestbookmarks、bookinfo
"""
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime

API_BASE = "https://i.weread.qq.com/api/agent/gateway"
SKILL_VERSION = "1.0.3"


def get_api_key():
    settings_path = os.path.expanduser("~/.claude/settings.json")
    with open(settings_path, "r") as f:
        settings = json.load(f)
    return settings.get("env", {}).get("WEREAD_API_KEY")


def call_weread(api_key, api_name, book_id):
    payload = json.dumps({
        "api_name": api_name,
        "bookId": book_id,
        "skill_version": SKILL_VERSION,
    }).encode("utf-8")

    req = urllib.request.Request(
        API_BASE,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError) as e:
        print(f"[warn] {api_name} failed: {e}", file=sys.stderr)
        return {}


def format_timestamp(ts):
    try:
        return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d")
    except (ValueError, TypeError, OSError):
        return str(ts)


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "用法: python3 fetch_book_data.py <bookId>"}))
        sys.exit(1)

    book_id = sys.argv[1]
    api_key = get_api_key()
    if not api_key:
        print(json.dumps({"error": "WEREAD_API_KEY 未配置"}))
        sys.exit(1)

    progress_data = call_weread(api_key, "/book/getprogress", book_id)
    bookmarks_data = call_weread(api_key, "/book/bookmarklist", book_id)
    best_data = call_weread(api_key, "/book/bestbookmarks", book_id)
    info_data = call_weread(api_key, "/book/info", book_id)

    progress = progress_data.get("book", {}).get("progress", None)
    chapter_uid = progress_data.get("book", {}).get("chapterUid", None)

    highlights = []
    for item in bookmarks_data.get("updated", []):
        highlights.append({
            "chapterUid": item.get("chapterUid"),
            "markText": item.get("markText", ""),
            "range": item.get("range", ""),
            "createTime": format_timestamp(item.get("createTime", 0)),
        })
    highlights.sort(key=lambda x: x["createTime"], reverse=True)

    popular = []
    for item in best_data.get("items", []):
        popular.append({
            "chapterUid": item.get("chapterUid"),
            "markText": item.get("markText", ""),
            "totalCount": item.get("totalCount", 0),
            "range": item.get("range", ""),
        })

    chapters = {}
    for ch in bookmarks_data.get("chapters", []):
        chapters[str(ch.get("chapterUid"))] = ch.get("title", "")
    for ch in best_data.get("chapters", []):
        chapters[str(ch.get("chapterUid"))] = ch.get("title", "")

    output = {
        "bookId": info_data.get("bookId", book_id),
        "title": info_data.get("title", ""),
        "author": info_data.get("author", ""),
        "progress": progress,
        "currentChapterUid": chapter_uid,
        "userHighlights": highlights,
        "userHighlightCount": len(highlights),
        "popularHighlights": popular,
        "popularTotal": best_data.get("totalCount", 0),
        "chapterMap": chapters,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
