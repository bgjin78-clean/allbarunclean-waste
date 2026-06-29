from pathlib import Path
from datetime import date

BASE_URL = "https://waste.allbarunclean.com"

SEOUL_SLUGS = [
    "gangnam", "gangdong", "gangbuk", "gangseo", "gwanak", "gwangjin", "guro",
    "geumcheon", "nowon", "dobong", "dongdaemun", "dongjak", "mapo", "seodaemun",
    "seocho", "seongdong", "seongbuk", "songpa", "yangcheon", "yeongdeungpo",
    "yongsan", "eunpyeong", "jongno", "jung", "jungnang",
]

GYEONGGI_SLUGS = [
    "suwon", "seongnam", "goyang", "yongin", "bucheon", "ansan", "anyang",
    "namyangju", "hwaseong", "pyeongtaek", "uijeongbu", "siheung", "paju",
    "gimpo", "gwangmyeong", "gwangju", "gunpo", "hanam", "osan", "icheon",
    "anseong", "uiwang", "yangju", "guri", "pocheon", "dongducheon", "gwacheon",
    "yeoju", "gapyeong", "yangpyeong", "yeoncheon",
]


def generate():
    root = Path(__file__).resolve().parent
    today = date.today().isoformat()

    urls = [
        (BASE_URL + "/", "1.0"),
        (BASE_URL + "/reviews/", "0.9"),
        (BASE_URL + "/seoul/", "0.9"),
        (BASE_URL + "/gyeonggi/", "0.9"),
    ]

    for slug in SEOUL_SLUGS:
        urls.append((f"{BASE_URL}/seoul/{slug}.html", "0.8"))

    for slug in GYEONGGI_SLUGS:
        urls.append((f"{BASE_URL}/gyeonggi/{slug}.html", "0.8"))

    reviews_dir = root / "reviews"
    if reviews_dir.exists():
        for folder in sorted(reviews_dir.iterdir()):
            if folder.is_dir() and folder.name != "__pycache__" and (folder / "index.html").exists():
                urls.append((f"{BASE_URL}/reviews/{folder.name}/", "0.7"))

    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>']
    sitemap.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for url, priority in urls:
        sitemap.append("  <url>")
        sitemap.append(f"    <loc>{url}</loc>")
        sitemap.append(f"    <lastmod>{today}</lastmod>")
        sitemap.append("    <changefreq>weekly</changefreq>")
        sitemap.append(f"    <priority>{priority}</priority>")
        sitemap.append("  </url>")

    sitemap.append("</urlset>")

    (root / "sitemap.xml").write_text("\n".join(sitemap), encoding="utf-8")

    robots = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
    (root / "robots.txt").write_text(robots, encoding="utf-8")

    print("완료: sitemap.xml 생성")
    print("완료: robots.txt 생성")
    print(f"총 URL 수: {len(urls)}개")


if __name__ == "__main__":
    generate()
