from pathlib import Path
from datetime import datetime, timezone

BASE_URL = "https://waste.allbarunclean.com"
SITE_TITLE = "올바른 폐기물처리"
SITE_DESC = "서울·경기 폐기물처리, 쓰레기집청소, 빈집정리, 가정·이사·폐업폐기물처리 전문 사이트"


def get_title(html, fallback):
    start = html.find("<title>")
    end = html.find("</title>")
    if start != -1 and end != -1:
        return html[start + 7 : end].strip()
    return fallback


def generate():
    root = Path(__file__).resolve().parent
    items = []

    items.append((SITE_TITLE, BASE_URL + "/", SITE_DESC))
    items.append(
        (
            f"서울·경기 폐기물처리 작업후기 | {SITE_TITLE}",
            BASE_URL + "/reviews/",
            "지역별 폐기물처리 작업후기 모음",
        )
    )

    reviews_dir = root / "reviews"
    if reviews_dir.exists():
        for folder in sorted(reviews_dir.iterdir()):
            index_file = folder / "index.html"
            if folder.is_dir() and index_file.exists():
                html = index_file.read_text(encoding="utf-8")
                title = get_title(html, f"{folder.name} 작업후기 | {SITE_TITLE}")
                link = f"{BASE_URL}/reviews/{folder.name}/"
                desc = title.replace(f"| {SITE_TITLE}", "").strip()
                items.append((title, link, desc))

    for group, slugs in [("seoul", [
        "gangnam", "gangdong", "gangbuk", "gangseo", "gwanak", "gwangjin", "guro",
        "geumcheon", "nowon", "dobong", "dongdaemun", "dongjak", "mapo", "seodaemun",
        "seocho", "seongdong", "seongbuk", "songpa", "yangcheon", "yeongdeungpo",
        "yongsan", "eunpyeong", "jongno", "jung", "jungnang",
    ]), ("gyeonggi", [
        "suwon", "seongnam", "goyang", "yongin", "bucheon", "ansan", "anyang",
        "namyangju", "hwaseong", "pyeongtaek", "uijeongbu", "siheung", "paju",
        "gimpo", "gwangmyeong", "gwangju", "gunpo", "hanam", "osan", "icheon",
        "anseong", "uiwang", "yangju", "guri", "pocheon", "dongducheon", "gwacheon",
        "yeoju", "gapyeong", "yangpyeong", "yeoncheon",
    ])]:
        for slug in slugs:
            path = root / group / f"{slug}.html"
            if not path.exists():
                continue
            html = path.read_text(encoding="utf-8")
            title = get_title(html, f"{slug} 폐기물처리 | {SITE_TITLE}")
            link = f"{BASE_URL}/{group}/{slug}.html"
            desc = title.replace("| 올바른수거", "").replace(f"| {SITE_TITLE}", "").strip()
            items.append((title, link, desc))

    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

    rss = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0">',
        "<channel>",
        f"<title>{SITE_TITLE}</title>",
        f"<link>{BASE_URL}/</link>",
        f"<description>{SITE_DESC}</description>",
        "<language>ko</language>",
        f"<lastBuildDate>{now}</lastBuildDate>",
    ]

    for title, link, desc in items:
        rss.extend([
            "<item>",
            f"<title>{title}</title>",
            f"<link>{link}</link>",
            f"<guid>{link}</guid>",
            f"<description>{desc}</description>",
            f"<pubDate>{now}</pubDate>",
            "</item>",
        ])

    rss.extend(["</channel>", "</rss>"])

    (root / "rss.xml").write_text("\n".join(rss), encoding="utf-8")

    print("완료: rss.xml 생성")
    print(f"총 RSS 항목: {len(items)}개")


if __name__ == "__main__":
    generate()
