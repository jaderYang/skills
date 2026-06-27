#!/usr/bin/env python3
"""微信读书取数脚本 - read-with-me skill 专用
用法: python3 fetch_book_data.py <bookId>
输出: JSON 格式，包含 progress、bookmarks、bestbookmarks、bookinfo、reviews（个人评论/想法）
"""
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

API_BASE = "https://i.weread.qq.com/api/agent/gateway"
SKILL_VERSION = "1.0.3"


def get_api_key():
    """按优先级链查找 WEREAD_API_KEY，支持多工具、多平台。"""
    # 1. 环境变量（最高优先级，通用契约）
    key = os.environ.get("WEREAD_API_KEY")
    if key:
        return key

    # 2. 工具无关共享位置
    shared = _shared_key_path()
    key = _read_plain_key(shared)
    if key:
        return key

    # 3. 各 AI 工具配置目录（JSON 格式，统一读 env.WEREAD_API_KEY）
    home = Path.home()
    for cfg in [
        home / ".claude" / "settings.json",
        home / ".workbuddy" / "settings.json",
    ]:
        key = _read_json_env_key(cfg)
        if key:
            return key

    return None


def _shared_key_path():
    """工具无关的共享配置路径：Unix ~/.config/weread/key，Windows %APPDATA%\\weread\\key"""
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    else:
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base / "weread" / "key"


def _read_plain_key(path):
    """从纯文本文件读取 key。"""
    try:
        text = Path(path).read_text(encoding="utf-8").strip()
        return text if text else None
    except (OSError, IOError):
        return None


def _read_json_env_key(path):
    """从 JSON 配置文件的 env.WEREAD_API_KEY 读取。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("env", {}).get("WEREAD_API_KEY") or None
    except (OSError, IOError, json.JSONDecodeError, KeyError):
        return None


def call_weread(api_key, api_name, book_id, extra_params=None):
    body = {
        "api_name": api_name,
        "bookId": book_id,
        "skill_version": SKILL_VERSION,
    }
    if extra_params:
        body.update(extra_params)
    payload = json.dumps(body).encode("utf-8")

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
        print(json.dumps({"error": "用法: python3 fetch_book_data.py <bookId> | --check"}))
        sys.exit(1)

    # --check: 只检查 key 是否已配置，不调 API
    if sys.argv[1] == "--check":
        api_key = get_api_key()
        if api_key:
            print(json.dumps({"configured": True}))
        else:
            print(json.dumps({"configured": False}))
        sys.exit(0)

    book_id = sys.argv[1]
    api_key = get_api_key()
    if not api_key:
        print(json.dumps({"error": "WEREAD_API_KEY 未配置"}))
        sys.exit(1)

    progress_data = call_weread(api_key, "/book/getprogress", book_id)
    bookmarks_data = call_weread(api_key, "/book/bookmarklist", book_id)
    best_data = call_weread(api_key, "/book/bestbookmarks", book_id)
    info_data = call_weread(api_key, "/book/info", book_id)
    # 个人评论/想法（深思考，比划线更重要）
    reviews_data = call_weread(
        api_key, "/review/list/mine", book_id,
        extra_params={"bookid": book_id, "count": 100}
    )

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

    # 解析个人评论/想法（深思考）
    reviews = []
    for item in reviews_data.get("reviews", []):
        review = item.get("review", {})
        reviews.append({
            "reviewId": review.get("reviewId", ""),
            "chapterUid": review.get("chapterUid"),
            "chapterName": review.get("chapterName", ""),
            "content": review.get("content", ""),  # 用户的想法/评论
            "abstract": review.get("abstract", ""),  # 对应的划线原文
            "createTime": format_timestamp(review.get("createTime", 0)),
            "star": review.get("star", 0),  # 评分（如有）
        })
    reviews.sort(key=lambda x: x["createTime"], reverse=True)

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
        "userReviews": reviews,  # 个人评论/想法（深思考，优先级高于划线）
        "userReviewCount": len(reviews),
        "userHighlights": highlights,
        "userHighlightCount": len(highlights),
        "popularHighlights": popular,
        "popularTotal": best_data.get("totalCount", 0),
        "chapterMap": chapters,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
