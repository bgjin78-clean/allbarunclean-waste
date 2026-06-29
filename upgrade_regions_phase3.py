import os
import re

BRAND = "올바른 폐기물처리"
PHONE = "010-4393-2414"
PHONE_LINK = "01043932414"

SEOUL = [
    ("index.html", "서울", None),
    ("gangnam.html", "강남구", "gangnam"),
    ("gangdong.html", "강동구", "gangdong"),
    ("gangbuk.html", "강북구", "gangbuk"),
    ("gangseo.html", "강서구", "gangseo"),
    ("gwanak.html", "관악구", "gwanak"),
    ("gwangjin.html", "광진구", "gwangjin"),
    ("guro.html", "구로구", "guro"),
    ("geumcheon.html", "금천구", "geumcheon"),
    ("nowon.html", "노원구", "nowon"),
    ("dobong.html", "도봉구", "dobong"),
    ("dongdaemun.html", "동대문구", "dongdaemun"),
    ("dongjak.html", "동작구", "dongjak"),
    ("mapo.html", "마포구", "mapo"),
    ("seodaemun.html", "서대문구", "seodaemun"),
    ("seocho.html", "서초구", "seocho"),
    ("seongdong.html", "성동구", "seongdong"),
    ("seongbuk.html", "성북구", "seongbuk"),
    ("songpa.html", "송파구", "songpa"),
    ("yangcheon.html", "양천구", "yangcheon"),
    ("yeongdeungpo.html", "영등포구", "yeongdeungpo"),
    ("yongsan.html", "용산구", "yongsan"),
    ("eunpyeong.html", "은평구", "eunpyeong"),
    ("jongno.html", "종로구", "jongno"),
    ("jung.html", "중구", "jung"),
    ("jungnang.html", "중랑구", "jungnang"),
]

GYEONGGI = [
    ("index.html", "경기", None),
    ("suwon.html", "수원", "suwon"),
    ("seongnam.html", "성남", "seongnam"),
    ("goyang.html", "고양", "goyang"),
    ("yongin.html", "용인", "yongin"),
    ("bucheon.html", "부천", "bucheon"),
    ("ansan.html", "안산", "ansan"),
    ("anyang.html", "안양", "anyang"),
    ("namyangju.html", "남양주", "namyangju"),
    ("hwaseong.html", "화성", "hwaseong"),
    ("pyeongtaek.html", "평택", "pyeongtaek"),
    ("uijeongbu.html", "의정부", "uijeongbu"),
    ("siheung.html", "시흥", "siheung"),
    ("paju.html", "파주", "paju"),
    ("gimpo.html", "김포", "gimpo"),
    ("gwangmyeong.html", "광명", "gwangmyeong"),
    ("gwangju.html", "광주", "gwangju"),
    ("gunpo.html", "군포", "gunpo"),
    ("hanam.html", "하남", "hanam"),
    ("osan.html", "오산", "osan"),
    ("icheon.html", "이천", "icheon"),
    ("anseong.html", "안성", "anseong"),
    ("uiwang.html", "의왕", "uiwang"),
    ("yangju.html", "양주", "yangju"),
    ("guri.html", "구리", "guri"),
    ("pocheon.html", "포천", "pocheon"),
    ("dongducheon.html", "동두천", "dongducheon"),
    ("gwacheon.html", "과천", "gwacheon"),
    ("yeoju.html", "여주", "yeoju"),
    ("yangpyeong.html", "양평", "yangpyeong"),
    ("gapyeong.html", "가평", "gapyeong"),
    ("yeoncheon.html", "연천", "yeoncheon"),
]


def header_html(slug):
    review_href = f"/reviews/{slug}/" if slug else "/reviews/"
    return f"""<header class="site-header">
  <div class="container header-inner">
    <a href="../index.html" class="logo">올바른 <span>폐기물처리</span></a>
    <nav>
      <a href="../index.html#services">서비스</a>
      <a href="../index.html#price">비용</a>
      <a href="{review_href}">작업후기</a>
      <a href="#contact">상담접수</a>
    </nav>
    <a href="tel:{PHONE_LINK}" class="header-call">{PHONE}</a>
  </div>
</header>"""


def gallery_section(name, before_num, process_num, after_num):
    b, p, a = f"{before_num:02d}", f"{process_num:02d}", f"{after_num:02d}"
    return f"""
<section class="section gallery region-case">
  <div class="container">
    <p class="section-label">PHOTO</p>
    <h2>{name} 폐기물처리 현장 사진</h2>
    <p class="section-desc">작업 전·중·후 현장을 단계별로 확인할 수 있습니다.</p>

    <h3 class="gallery-title">작업 전</h3>
    <div class="photo-grid region-case-grid">
      <img src="../images/main/before-{b}.jpg" alt="{name} 폐기물처리 작업 전 현장" loading="lazy">
    </div>

    <h3 class="gallery-title">작업 중</h3>
    <div class="photo-grid region-case-grid">
      <img src="../images/main/process-{p}.jpg" alt="{name} 폐기물처리 작업 중 현장" loading="lazy">
    </div>

    <h3 class="gallery-title">작업 후</h3>
    <div class="photo-grid region-case-grid">
      <img src="../images/main/after-{a}.jpg" alt="{name} 폐기물처리 작업 후 현장" loading="lazy">
    </div>
  </div>
</section>
"""


def review_section(name, slug):
    review_href = f"/reviews/{slug}/" if slug else "/reviews/"
    review_label = f"{name} 작업후기 보기" if slug else "작업후기 보기"
    return f"""
<section class="section reviews-preview region-review" id="review">
  <div class="container">
    <p class="section-label">REVIEW</p>
    <h2>{name} 폐기물처리 작업후기</h2>
    <p class="section-desc">{name} 현장에서 진행한 쓰레기집청소, 빈집정리, 가정·이사·폐업폐기물처리 작업후기를 확인할 수 있습니다.</p>

    <div class="review-promo">
      <p>작업 전·후 현장 사진과 정리 과정을 {name} 작업후기 페이지에서 확인하세요.</p>
      <div class="review-promo-buttons">
        <a href="{review_href}" class="btn primary">{review_label}</a>
        <a href="/reviews/" class="btn secondary">전체 작업후기</a>
      </div>
    </div>
  </div>
</section>
"""


def related_section_html():
    return """
<section class="section related-section region-related">
  <div class="container">
    <p class="section-label">올바른 관련 서비스</p>
    <h2>서울·경기 올바른 서비스 바로가기</h2>
    <p class="section-desc">폐기물처리와 함께 이용하실 수 있는 올바른 관련 서비스입니다.</p>

    <div class="related-grid">
      <a href="https://www.allbarunclean.com/" class="related-card" target="_blank" rel="noopener">
        <h3>올바른수거</h3>
        <p>서울·경기 전 지역 쓰레기집청소, 빈집정리, 유품·고독사·특수청소 등 종합 정리 서비스를 안내합니다.</p>
        <span>www.allbarunclean.com →</span>
      </a>
      <a href="https://yupum.allbarunclean.com/" class="related-card" target="_blank" rel="noopener">
        <h3>올바른 유품정리</h3>
        <p>서울·경기 전 지역 유품정리, 고독사청소, 특수청소 등 유품·특수청소 서비스를 안내합니다.</p>
        <span>yupum.allbarunclean.com →</span>
      </a>
    </div>
  </div>
</section>
"""


def footer_html(name, slug):
    review_line = ""
    if slug:
        review_line = f'        <a href="/reviews/{slug}/">{name} 작업후기</a>\n'
    return f"""<footer>
  <div class="container footer-inner region-footer">
    <div>
      <strong>{BRAND}</strong>
      <p>{name} 폐기물처리 · 쓰레기집청소 · 빈집정리</p>
    </div>
    <div class="footer-links">
      <p>대표 상담 : <a href="tel:{PHONE_LINK}">{PHONE}</a></p>
      <a href="https://www.allbarunclean.com/" target="_blank" rel="noopener">올바른수거 · allbarunclean.com</a>
      <a href="https://yupum.allbarunclean.com/" target="_blank" rel="noopener">올바른 유품정리 · yupum.allbarunclean.com</a>
      <a href="/reviews/">작업후기 모음</a>
{review_line}      <p class="footer-domain">폐기물처리 : waste.allbarunclean.com</p>
    </div>
  </div>
  <p class="footer-copy">© {BRAND} All Rights Reserved.</p>
</footer>"""


def unify_brand(html):
    html = re.sub(r"\| 올바른수거", f"| {BRAND}", html)
    html = html.replace("올바른수거 <span>폐기물처리</span>", '올바른 <span>폐기물처리</span>')
    html = html.replace("© 올바른수거 폐기물처리", f"© {BRAND}")
    html = re.sub(
        r"<strong>올바른수거 폐기물처리</strong>",
        f"<strong>{BRAND}</strong>",
        html,
    )
    return html


def upgrade_html(html, name, slug, image_idx):
    html = unify_brand(html)

    before_num = ((image_idx - 1) % 30) + 1
    after_num = before_num
    process_num = ((image_idx - 1) % 25) + 1

    html = re.sub(
        r"<header class=\"site-header\">.*?</header>",
        header_html(slug),
        html,
        count=1,
        flags=re.DOTALL,
    )

    if "region-case" not in html:
        marker = '<section class="section contact">'
        if marker in html:
            gallery = gallery_section(name, before_num, process_num, after_num)
            review = review_section(name, slug)
            html = html.replace(
                marker,
                gallery + review + '\n<section id="contact" class="section contact">',
            )
        elif '<section id="contact"' in html:
            gallery = gallery_section(name, before_num, process_num, after_num)
            review = review_section(name, slug)
            html = html.replace(
                '<section id="contact"',
                gallery + review + '\n<section id="contact"',
            )
    elif 'id="review"' not in html:
        marker = '<section id="contact" class="section contact">'
        if marker not in html:
            marker = '<section class="section contact">'
        html = html.replace(marker, review_section(name, slug) + "\n" + marker.replace(
            '<section class="section contact">', '<section id="contact" class="section contact">'
        ))

    if "region-related" not in html:
        html = html.replace("<footer>", related_section_html() + "\n<footer>")

    html = re.sub(r"<footer>.*?</footer>", footer_html(name, slug), html, count=1, flags=re.DOTALL)

    if 'id="contact"' not in html:
        html = html.replace(
            '<section class="section contact">',
            '<section id="contact" class="section contact">',
            1,
        )

    return html


def upgrade():
    idx = 0
    count = 0

    for folder, items in [("seoul", SEOUL), ("gyeonggi", GYEONGGI)]:
        for filename, name, slug in items:
            idx += 1
            path = os.path.join(folder, filename)
            if not os.path.exists(path):
                print(f"건너뜀: {path}")
                continue

            with open(path, "r", encoding="utf-8") as f:
                html = f.read()

            html = upgrade_html(html, name, slug, idx)

            with open(path, "w", encoding="utf-8") as f:
                f.write(html)

            print(f"완료: {folder}/{filename} ({name})")
            count += 1

    print(f"\n총 {count}개 지역 페이지 3단계 업그레이드 완료")


if __name__ == "__main__":
    upgrade()
