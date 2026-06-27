#!/usr/bin/env python3
"""微信读书推荐脚本 - read-with-me skill 专用
用法: python3 recommend_book.py <bookId> [--search "关键词1"] [--search "关键词2"]
输出: JSON 格式的候选书籍列表（已去重，按来源排序）
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_book_data import get_api_key, call_weread


def parse_recommend(api_key):
    """调用 /book/recommend 获取个性化推荐。"""
    data = call_weread(api_key, "/book/recommend", "0")
    candidates = []
    for book in data.get("books", []):
        candidates.append({
            "bookId": str(book.get("bookId", "")),
            "title": book.get("title", ""),
            "author": book.get("author", ""),
            "category": book.get("category", ""),
            "intro": book.get("intro", ""),
            "rating": book.get("newRating", 0),
            "ratingCount": book.get("newRatingCount", 0),
            "ratingLabel": book.get("newRatingDetail", {}).get("title", ""),
            "readingCount": book.get("readingCount", 0),
            "cover": book.get("cover", ""),
            "source": "recommend",
        })
    return candidates


def parse_similar(api_key, book_id):
    """调用 /book/similar 获取相似书推荐。"""
    data = call_weread(api_key, "/book/similar", book_id)
    candidates = []
    similar = data.get("booksimilar", {})
    for item in similar.get("books", []):
        book = item.get("book", {}).get("bookInfo", {})
        if not book:
            continue
        candidates.append({
            "bookId": str(book.get("bookId", "")),
            "title": book.get("title", ""),
            "author": book.get("author", ""),
            "category": book.get("category", ""),
            "intro": book.get("intro", ""),
            "rating": book.get("newRating", 0),
            "ratingCount": book.get("newRatingCount", 0),
            "ratingLabel": book.get("newRatingDetail", {}).get("title", ""),
            "readingCount": book.get("readingCount", 0),
            "cover": book.get("cover", ""),
            "source": "similar",
        })
    return candidates


def parse_search(api_key, keyword):
    """调用 /store/search 按关键词搜索书籍。"""
    data = call_weread(api_key, "/store/search", "0", extra_params={
        "keyword": keyword,
        "scope": 10,
        "count": 10,
    })
    candidates = []
    for result_group in data.get("results", []):
        for book_item in result_group.get("books", []):
            book = book_item.get("bookInfo", {})
            if not book:
                continue
            candidates.append({
                "bookId": str(book.get("bookId", "")),
                "title": book.get("title", ""),
                "author": book.get("author", ""),
                "category": book.get("category", ""),
                "intro": book.get("intro", ""),
                "rating": book.get("newRating", 0),
                "ratingCount": book.get("newRatingCount", 0),
                "ratingLabel": book.get("newRatingDetail", {}).get("title", ""),
                "readingCount": book.get("readingCount", 0),
                "cover": book.get("cover", ""),
                "source": "search",
                "searchKeyword": keyword,
            })
    return candidates


def parse_reviews(data):
    """解析 /review/list/mine 返回的评论数据。"""
    reviews = []
    review_items = data.get("reviews", [])
    for item in review_items:
        review = item.get("review", {})
        reviews.append({
            "reviewId": review.get("reviewId", ""),
            "chapterName": review.get("chapterName", ""),
            "content": review.get("content", ""),
            "abstract": review.get("abstract", ""),
            "createTime": _format_timestamp(review.get("createTime", 0)),
            "star": review.get("star", 0),
        })
    return reviews


def _format_timestamp(ts):
    try:
        return datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d")
    except (ValueError, TypeError, OSError):
        return str(ts)


def dedup(candidates):
    """按 bookId 去重，保留优先级最高的来源。"""
    priority = {"recommend": 0, "similar": 1, "search": 2}
    seen = {}
    for c in candidates:
        bid = c["bookId"]
        if bid not in seen or priority.get(c["source"], 99) < priority.get(seen[bid]["source"], 99):
            seen[bid] = c
    return list(seen.values())


def main():
    parser = argparse.ArgumentParser(description="微信读书推荐候选获取")
    parser.add_argument("bookId", help="锚点书的 bookId（最近更新最晚的那本）")
    parser.add_argument("--search", action="append", default=[],
                        help="搜索关键词，可多次指定")
    args = parser.parse_args()

    api_key = get_api_key()
    if not api_key:
        print(json.dumps({"error": "WEREAD_API_KEY 未配置"}))
        sys.exit(1)

    recommend = parse_recommend(api_key)
    similar = parse_similar(api_key, args.bookId)
    reviews_data = call_weread(api_key, "/review/list/mine", args.bookId,
                               extra_params={"bookid": args.bookId, "count": 100})
    reviews = parse_reviews(reviews_data)

    search_results = []
    for kw in args.search:
        search_results.extend(parse_search(api_key, kw))

    all_candidates = dedup(recommend + similar + search_results)
    all_candidates = [c for c in all_candidates if c["bookId"] != args.bookId]

    output = {
        "lastBook": {
            "bookId": args.bookId,
            "userReviews": reviews,
            "userReviewCount": len(reviews),
        },
        "candidates": all_candidates,
        "candidateCount": len(all_candidates),
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
