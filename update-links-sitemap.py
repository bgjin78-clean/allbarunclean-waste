import os
from datetime import date

DOMAIN = "https://waste.allbarunclean.com"

SEOUL = [
    ("강남구", "gangnam"),
    ("강동구", "gangdong"),
    ("강북구", "gangbuk"),
    ("강서구", "gangseo"),
    ("관악구", "gwanak"),
    ("광진구", "gwangjin"),
    ("구로구", "guro"),
    ("금천구", "geumcheon"),
    ("노원구", "nowon"),
    ("도봉구", "dobong"),
    ("동대문구", "dongdaemun"),
    ("동작구", "dongjak"),
    ("마포구", "mapo"),
    ("서대문구", "seodaemun"),
    ("서초구", "seocho"),
    ("성동구", "seongdong"),
    ("성북구", "seongbuk"),
    ("송파구", "songpa"),
    ("양천구", "yangcheon"),
    ("영등포구", "yeongdeungpo"),
    ("용산구", "yongsan"),
    ("은평구", "eunpyeong"),
    ("종로구", "jongno"),
    ("중구", "jung"),
    ("중랑구", "jungnang"),
]

GYEONGGI = [
    ("수원", "suwon"),
    ("성남", "seongnam"),
    ("고양", "goyang"),
    ("용인", "yongin"),
    ("부천", "bucheon"),
    ("안산", "ansan"),
    ("안양", "anyang"),
    ("남양주", "namyangju"),
    ("화성", "hwaseong"),
    ("평택", "pyeongtaek"),
    ("의정부", "uijeongbu"),
    ("시흥", "siheung"),
    ("파주", "paju"),
    ("김포", "gimpo"),
    ("광명", "gwangmyeong"),
    ("광주", "gwangju"),
    ("군포", "gunpo"),
    ("하남", "hanam"),
    ("오산", "osan"),
    ("이천", "icheon"),
    ("안성", "anseong"),
    ("의왕", "uiwang"),
    ("양주", "yangju"),
    ("구리", "guri"),
    ("포천", "pocheon"),
    ("동두천", "dongducheon"),
    ("과천", "gwacheon"),
    ("여주", "yeoju"),
    ("양평", "yangpyeong"),
    ("가평", "gapyeong"),
    ("연천", "yeoncheon"),
]

def make_link_section(title, items, folder):
    links = "\n".join(
        [f'            <a href="./{slug}.html">{name} 폐기물처리</a>' for name, slug in items]
    )

    return f"""
<section class="section region-links">
    <div class="container">
        <p class="section-label">LOCAL AREA</p>
        <h2>{title}</h2>
        <div class="region-grid">
{links}
        </div>
    </div>
</section>
"""

def insert_before_faq(file_path, section_html):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    marker = '<section class="section faq">'
    if section_html.strip() in content:
        print(f"already exists: {file_path}")
        return

    if marker not in content:
        print(f"marker not found: {file_path}")
        return

    content = content.replace(marker, section_html + "\n" + marker)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"updated links: {file_path}")

def update_home_links():
    file_path = "index.html"

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    home_section = """
<section class="section region-links">
    <div class="container">
        <p class="section-label">REGION</p>
        <h2>서울·경기 폐기물처리 지역 안내</h2>
        <div class="region-grid">
            <a href="./seoul/">서울 폐기물처리 대표페이지</a>
            <a href="./gyeonggi/">경기 폐기물처리 대표페이지</a>
            <a href="./gyeonggi/namyangju.html">남양주 폐기물처리</a>
            <a href="./gyeonggi/guri.html">구리 폐기물처리</a>
            <a href="./gyeonggi/hanam.html">하남 폐기물처리</a>
            <a href="./seoul/songpa.html">송파구 폐기물처리</a>
            <a href="./seoul/gangdong.html">강동구 폐기물처리</a>
            <a href="./seoul/nowon.html">노원구 폐기물처리</a>
        </div>
    </div>
</section>
"""

    marker = '<section class="section seo-content">'

    if "서울·경기 폐기물처리 지역 안내" in content:
        print("home region links already exists")
        return

    if marker not in content:
        print("home marker not found")
        return

    content = content.replace(marker, home_section + "\n" + marker)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("updated home links")

def write_sitemap():
    today = date.today().isoformat()

    urls = [
        (f"{DOMAIN}/", "1.0"),
        (f"{DOMAIN}/seoul/", "0.9"),
        (f"{DOMAIN}/gyeonggi/", "0.9"),
    ]

    for name, slug in SEOUL:
        urls.append((f"{DOMAIN}/seoul/{slug}.html", "0.8"))

    for name, slug in GYEONGGI:
        urls.append((f"{DOMAIN}/gyeonggi/{slug}.html", "0.8"))

    xml = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    for loc, priority in urls:
        xml.append("  <url>")
        xml.append(f"    <loc>{loc}</loc>")
        xml.append(f"    <lastmod>{today}</lastmod>")
        xml.append("    <changefreq>weekly</changefreq>")
        xml.append(f"    <priority>{priority}</priority>")
        xml.append("  </url>")

    xml.append("</urlset>")

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml))

    print(f"sitemap updated: {len(urls)} urls")

def main():
    insert_before_faq(
        "seoul/index.html",
        make_link_section("서울 25개 구 폐기물처리", SEOUL, "seoul")
    )

    insert_before_faq(
        "gyeonggi/index.html",
        make_link_section("경기 31개 시군 폐기물처리", GYEONGGI, "gyeonggi")
    )

    update_home_links()
    write_sitemap()

    print("완료: 내부링크와 sitemap.xml 업데이트")

if __name__ == "__main__":
    main()