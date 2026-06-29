from pathlib import Path
import random
from datetime import date

BASE_URL = "https://waste.allbarunclean.com"
PHONE = "010-4393-2414"
PHONE_LINK = "01043932414"
BRAND = "올바른 폐기물처리"

REGIONS = [
    ("서울", "강남구", "gangnam"), ("서울", "강동구", "gangdong"), ("서울", "강북구", "gangbuk"),
    ("서울", "강서구", "gangseo"), ("서울", "관악구", "gwanak"), ("서울", "광진구", "gwangjin"),
    ("서울", "구로구", "guro"), ("서울", "금천구", "geumcheon"), ("서울", "노원구", "nowon"),
    ("서울", "도봉구", "dobong"), ("서울", "동대문구", "dongdaemun"), ("서울", "동작구", "dongjak"),
    ("서울", "마포구", "mapo"), ("서울", "서대문구", "seodaemun"), ("서울", "서초구", "seocho"),
    ("서울", "성동구", "seongdong"), ("서울", "성북구", "seongbuk"), ("서울", "송파구", "songpa"),
    ("서울", "양천구", "yangcheon"), ("서울", "영등포구", "yeongdeungpo"), ("서울", "용산구", "yongsan"),
    ("서울", "은평구", "eunpyeong"), ("서울", "종로구", "jongno"), ("서울", "중구", "jung"),
    ("서울", "중랑구", "jungnang"),
    ("경기", "수원시", "suwon"), ("경기", "성남시", "seongnam"), ("경기", "고양시", "goyang"),
    ("경기", "용인시", "yongin"), ("경기", "부천시", "bucheon"), ("경기", "안산시", "ansan"),
    ("경기", "안양시", "anyang"), ("경기", "남양주시", "namyangju"), ("경기", "화성시", "hwaseong"),
    ("경기", "평택시", "pyeongtaek"), ("경기", "의정부시", "uijeongbu"), ("경기", "시흥시", "siheung"),
    ("경기", "파주시", "paju"), ("경기", "김포시", "gimpo"), ("경기", "광명시", "gwangmyeong"),
    ("경기", "광주시", "gwangju"), ("경기", "군포시", "gunpo"), ("경기", "오산시", "osan"),
    ("경기", "이천시", "icheon"), ("경기", "양주시", "yangju"), ("경기", "구리시", "guri"),
    ("경기", "안성시", "anseong"), ("경기", "포천시", "pocheon"), ("경기", "의왕시", "uiwang"),
    ("경기", "하남시", "hanam"), ("경기", "여주시", "yeoju"), ("경기", "동두천시", "dongducheon"),
    ("경기", "과천시", "gwacheon"), ("경기", "가평군", "gapyeong"), ("경기", "양평군", "yangpyeong"),
    ("경기", "연천군", "yeoncheon"),
]

PLACE_TYPES = ["아파트", "빌라", "원룸", "단독주택", "오피스텔", "상가"]

SERVICE_PROFILES = [
    {
        "tag": "가정폐기물",
        "titles": [
            "{name} {place} 가정폐기물처리 작업후기",
            "{name} {place} 생활폐기물 정리 작업후기",
        ],
        "summaries": [
            "가구와 생활용품, 잡동사니를 분류해 반출한 현장입니다.",
            "오래된 짐과 대형폐기물을 현장 조건에 맞춰 정리한 작업후기입니다.",
        ],
        "details": [
            "이번 {name} 현장은 {place}에서 폐기물 양과 반출 동선을 먼저 확인한 뒤 작업 범위를 안내했습니다. 대형가구와 생활폐기물을 구분해 분류·운반·상차 순서로 진행했습니다.",
            "엘리베이터 사용 여부와 차량 진입 가능 여부를 확인한 뒤 작업 인원과 차량을 배치했습니다. 마무리 단계에서 현장 상태를 함께 확인했습니다.",
        ],
    },
    {
        "tag": "이사폐기물",
        "titles": [
            "{name} {place} 이사폐기물처리 작업후기",
            "{name} 이사 전후 폐기물 정리 작업후기",
        ],
        "summaries": [
            "이사 후 남은 생활폐기물과 잔짐을 분류해 반출한 현장입니다.",
            "이사 일정에 맞춰 버릴 가구와 생활용품을 한 번에 정리한 작업후기입니다.",
        ],
        "details": [
            "{name} {place}에서는 이사 일정에 맞춰 정리 범위를 먼저 확인했습니다. 침대, 장롱, 생활용품 등을 분류한 뒤 반출 동선에 맞춰 운반했습니다.",
            "작업 전 사진 상담으로 대략적인 비용을 안내한 뒤 현장에서 최종 확인 후 진행했습니다.",
        ],
    },
    {
        "tag": "쓰레기집청소",
        "titles": [
            "{name} {place} 쓰레기집청소 작업후기",
            "{name} 장기 방치 공간 정리 작업후기",
        ],
        "summaries": [
            "주거공간에 쌓인 생활폐기물을 순서대로 정리한 현장입니다.",
            "혼자 정리하기 어려운 양의 폐기물을 단계적으로 분류·반출한 작업후기입니다.",
        ],
        "details": [
            "{name} {place} 현장은 폐기물이 오랜 기간 쌓여 이동 공간이 부족한 상태였습니다. 악취와 위생 문제를 고려해 분류 순서와 반출 계획을 먼저 안내했습니다.",
            "생활폐기물 정리, 포장, 운반, 상차까지 현장 상황에 맞춰 진행했습니다.",
        ],
    },
    {
        "tag": "빈집정리",
        "titles": [
            "{name} {place} 빈집정리 작업후기",
            "{name} 오래 비운 주택 정리 작업후기",
        ],
        "summaries": [
            "오래 보관된 가구와 생활용품을 정리한 작업후기입니다.",
            "매매·임대 전 남은 짐과 폐가구를 한 번에 정리한 현장입니다.",
        ],
        "details": [
            "{name} {place}에서는 빈집에 남아 있던 가구, 생활용품, 잡동사니의 양을 확인한 뒤 작업 계획을 안내했습니다. 반출 동선과 차량 진입 여부를 함께 점검했습니다.",
            "정리 후 공간 상태를 확인하며 다음 입주나 공사 준비가 가능하도록 마무리했습니다.",
        ],
    },
    {
        "tag": "폐업폐기물",
        "titles": [
            "{name} {place} 폐업폐기물처리 작업후기",
            "{name} 사무실·매장 집기 정리 작업후기",
        ],
        "summaries": [
            "폐업 후 남은 집기와 잡동사니를 현장 확인 후 정리한 작업후기입니다.",
            "사무실·매장 폐기물과 집기류를 분류해 반출한 현장입니다.",
        ],
        "details": [
            "{name} {place}에서는 업종에 따라 다른 집기와 폐기물이 남아 있었습니다. 책상, 의자, 선반 등 부피가 큰 물품의 분해·반출 순서를 먼저 안내했습니다.",
            "현장 확인 후 작업 인원과 차량을 정해 분류, 운반, 상차를 진행했습니다.",
        ],
    },
]

SHARED_CSS = """
    :root {
      --main:#10b981; --dark:#0f172a; --point:#f59e0b; --bg:#f8fafc;
      --card:#ffffff; --text:#1e293b; --muted:#64748b; --line:#e2e8f0; --soft:#ecfdf5;
    }
    * { box-sizing:border-box; }
    html { scroll-behavior:smooth; }
    body {
      margin:0;
      font-family:"Pretendard","Noto Sans KR",Arial,sans-serif;
      background:var(--bg);
      color:var(--text);
      line-height:1.75;
    }
    a { color:inherit; text-decoration:none; }
    header {
      position:sticky; top:0; z-index:100;
      background:rgba(255,255,255,0.95);
      border-bottom:1px solid var(--line);
      backdrop-filter:blur(10px);
    }
    .nav {
      max-width:1180px; margin:0 auto; padding:16px 20px;
      display:flex; justify-content:space-between; align-items:center; gap:18px;
    }
    .logo { font-size:22px; font-weight:900; color:var(--dark); letter-spacing:-0.8px; }
    .logo span { color:var(--main); }
    .nav-links { display:flex; flex-wrap:wrap; gap:16px; font-size:14px; font-weight:700; color:var(--muted); }
    .call-btn {
      background:var(--main); color:#fff; padding:10px 18px; border-radius:999px;
      font-weight:900; white-space:nowrap; font-size:14px;
    }
    .hero {
      padding:84px 20px 72px; color:#fff;
      background:linear-gradient(135deg,#0f172a 0%,#1e293b 60%,#10b981 100%);
    }
    .hero-inner, .wrap { max-width:1180px; margin:0 auto; }
    .badge {
      display:inline-block; padding:8px 15px; border-radius:999px;
      background:rgba(255,255,255,0.14); border:1px solid rgba(255,255,255,0.28);
      font-size:14px; margin-bottom:18px;
    }
    .hero h1 { margin:0 0 16px; font-size:40px; line-height:1.25; letter-spacing:-1.2px; }
    .hero p { max-width:760px; margin:0; font-size:17px; color:rgba(255,255,255,0.9); }
    section { padding:72px 20px; }
    .title { margin-bottom:30px; }
    .title span { color:var(--main); font-size:14px; font-weight:900; letter-spacing:0.5px; }
    .title h2 { margin:8px 0 10px; font-size:32px; line-height:1.3; color:var(--dark); letter-spacing:-1px; }
    .title p { margin:0; color:var(--muted); }
    .breadcrumb { font-size:14px; color:rgba(255,255,255,0.82); margin-bottom:18px; }
    .breadcrumb a { text-decoration:underline; }
    .review-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:18px; }
    .review-card {
      background:var(--card); border:1px solid var(--line); border-radius:22px;
      padding:26px; box-shadow:0 10px 28px rgba(15,23,42,0.06);
      display:flex; flex-direction:column;
    }
    .review-tag {
      display:inline-block; background:var(--soft); color:#047857;
      padding:5px 12px; border-radius:999px; font-size:13px; font-weight:800;
      margin-bottom:14px; align-self:flex-start;
    }
    .review-card h3 { margin:0 0 10px; color:var(--dark); font-size:19px; line-height:1.4; }
    .review-card p { margin:0 0 18px; color:var(--muted); font-size:15px; flex:1; }
    .review-link { color:var(--main); font-weight:900; font-size:15px; }
    .area-block { margin-bottom:42px; }
    .area-block h3 { color:var(--dark); font-size:24px; margin:0 0 18px; }
    .article-box {
      background:var(--card); border:1px solid var(--line); border-radius:28px;
      padding:38px; box-shadow:0 12px 34px rgba(15,23,42,0.06);
    }
    .article-box h1 { margin:0 0 14px; color:var(--dark); font-size:34px; line-height:1.3; letter-spacing:-1px; }
    .article-box .lead { color:var(--muted); font-size:17px; margin:0 0 28px; }
    .article-box p { color:var(--muted); margin:0 0 16px; }
    .photo-block { margin-top:34px; }
    .photo-block h2 { color:var(--dark); font-size:22px; margin:0 0 16px; }
    .photo-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:16px; margin-bottom:28px; }
    .photo-grid img {
      width:100%; height:260px; object-fit:cover; border-radius:18px;
      display:block; background:#e2e8f0; border:1px solid var(--line);
    }
    .cta-box {
      margin-top:34px; padding:28px; border-radius:22px;
      background:var(--soft); border:1px solid #d1fae5;
    }
    .cta-box h2 { margin:0 0 10px; color:var(--dark); font-size:24px; }
    .cta-box p { margin:0 0 16px; color:var(--muted); }
    .btn-row { display:flex; flex-wrap:wrap; gap:12px; }
    .btn {
      display:inline-block; padding:13px 20px; border-radius:12px; font-weight:900;
    }
    .btn-primary { background:var(--main); color:#fff; }
    .btn-outline { background:var(--card); color:var(--dark); border:1px solid var(--line); }
    .related-section { background:var(--soft); }
    .related-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:18px; }
    .related-card {
      display:block; background:var(--card); border:1px solid #d1fae5; border-radius:22px;
      padding:30px; box-shadow:0 10px 28px rgba(16,185,129,0.08);
    }
    .related-card h3 { margin:0 0 10px; color:var(--dark); font-size:22px; }
    .related-card p { margin:0 0 16px; color:var(--muted); font-size:15px; }
    .related-card span { color:var(--main); font-weight:900; font-size:15px; }
    footer { background:#0f172a; color:#cbd5e1; padding:40px 20px; }
    .footer-inner {
      max-width:1180px; margin:0 auto; display:flex;
      justify-content:space-between; gap:24px; flex-wrap:wrap;
    }
    .footer-inner strong { color:#fff; font-size:18px; }
    .footer-links a { display:block; margin-bottom:6px; color:var(--main); font-weight:700; }
    .floating-call {
      position:fixed; right:18px; bottom:18px; z-index:120;
      background:var(--main); color:#fff; padding:14px 18px; border-radius:999px;
      font-weight:900; box-shadow:0 12px 30px rgba(16,185,129,0.28);
    }
    @media (max-width:900px) {
      .nav-links { display:none; }
      .hero h1, .article-box h1 { font-size:30px; }
      .review-grid, .photo-grid, .related-grid { grid-template-columns:1fr; }
      section { padding:58px 20px; }
      .floating-call { left:18px; right:18px; text-align:center; }
    }
"""


def region_page_url(region_type, slug):
    if region_type == "서울":
        return f"/seoul/{slug}.html"
    return f"/gyeonggi/{slug}.html"


def case_image_path(kind, number):
    return f"/images/cases/waste-{kind}-{number:03d}.jpg"


def pick_image_numbers(slug, kind, count):
    rng = random.Random(f"{slug}:{kind}")
    nums = list(range(1, 101))
    rng.shuffle(nums)
    return nums[:count]


def review_content(region_type, name, slug):
    rng = random.Random(slug)
    profile = rng.choice(SERVICE_PROFILES)
    place = rng.choice(PLACE_TYPES)
    title = rng.choice(profile["titles"]).format(name=name, place=place)
    summary = rng.choice(profile["summaries"])
    details = [rng.choice(profile["details"]).format(name=name, place=place) for _ in range(2)]
    before_nums = pick_image_numbers(slug, "before", 2)
    after_nums = pick_image_numbers(slug, "after", 2)
    return {
        "tag": profile["tag"],
        "title": title,
        "summary": summary,
        "details": details,
        "before_nums": before_nums,
        "after_nums": after_nums,
        "region_type": region_type,
        "name": name,
        "slug": slug,
        "region_url": region_page_url(region_type, slug),
    }


def header_html(active=""):
    reviews_style = ' style="color:var(--main)"' if active == "reviews" else ""
    return f"""
<header>
  <div class="nav">
    <a href="/" class="logo">올바른 <span>폐기물처리</span></a>
    <nav class="nav-links">
      <a href="/#services">서비스</a>
      <a href="/reviews/"{reviews_style}>작업후기</a>
      <a href="/#area">지역안내</a>
      <a href="/#contact">상담접수</a>
    </nav>
    <a href="tel:{PHONE_LINK}" class="call-btn">{PHONE}</a>
  </div>
</header>"""


def footer_html():
    return f"""
<footer>
  <div class="footer-inner">
    <div>
      <strong>{BRAND}</strong><br />
      서울·경기 폐기물처리 · 쓰레기집청소 · 빈집정리
    </div>
    <div class="footer-links">
      대표 상담 : <a href="tel:{PHONE_LINK}">{PHONE}</a><br />
      <a href="https://www.allbarunclean.com/" target="_blank" rel="noopener">올바른수거 · allbarunclean.com</a>
      <a href="https://yupum.allbarunclean.com/" target="_blank" rel="noopener">올바른 유품정리 · yupum.allbarunclean.com</a><br />
      <a href="/reviews/">작업후기 모음</a>
    </div>
  </div>
</footer>
<a href="tel:{PHONE_LINK}" class="floating-call">전화 상담 {PHONE}</a>"""


def related_section_html():
    return """
  <section class="related-section">
    <div class="wrap">
      <div class="title">
        <span>올바른 관련 서비스</span>
        <h2>서울·경기 올바른 서비스 바로가기</h2>
      </div>
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
  </section>"""


def review_card_html(content, link_text="자세히 보기"):
    return f"""
        <article class="review-card">
          <span class="review-tag">{content["tag"]}</span>
          <h3>{content["title"]}</h3>
          <p>{content["summary"]}</p>
          <a href="/reviews/{content["slug"]}/" class="review-link">{link_text} →</a>
        </article>"""


def detail_page_html(content):
    before_imgs = "\n".join(
        f'          <img src="{case_image_path("before", n)}" alt="{content["name"]} 폐기물처리 작업 전 현장">'
        for n in content["before_nums"]
    )
    after_imgs = "\n".join(
        f'          <img src="{case_image_path("after", n)}" alt="{content["name"]} 폐기물처리 작업 후 현장">'
        for n in content["after_nums"]
    )
    detail_paragraphs = "\n".join(f"        <p>{p}</p>" for p in content["details"])
    page_url = f"{BASE_URL}/reviews/{content['slug']}/"
    title = f"{content['title']} | {BRAND}"
    desc = content["summary"]

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{desc}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{page_url}" />
  <link rel="icon" href="/favicon-allbarun.png" />
  <style>{SHARED_CSS}</style>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{content['title']}",
    "description": "{desc}",
    "author": {{ "@type": "Organization", "name": "{BRAND}" }},
    "publisher": {{ "@type": "Organization", "name": "{BRAND}" }},
    "mainEntityOfPage": "{page_url}",
    "dateModified": "{date.today().isoformat()}"
  }}
  </script>
</head>
<body>
{header_html()}
<main>
  <section class="hero">
    <div class="hero-inner">
      <div class="breadcrumb"><a href="/">홈</a> · <a href="/reviews/">작업후기</a> · {content["name"]}</div>
      <div class="badge">{content["tag"]}</div>
      <h1>{content["title"]}</h1>
      <p>{content["summary"]}</p>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="article-box">
        <h1>{content["title"]}</h1>
        <p class="lead">{content["summary"]}</p>
{detail_paragraphs}

        <div class="photo-block">
          <h2>작업 전 현장</h2>
          <div class="photo-grid">
{before_imgs}
          </div>

          <h2>작업 후 정리</h2>
          <div class="photo-grid">
{after_imgs}
          </div>
        </div>

        <div class="cta-box">
          <h2>{content["name"]} 폐기물처리 상담</h2>
          <p>비슷한 현장 상담이 필요하시면 사진과 주소를 남겨주시면 확인 후 연락드립니다.</p>
          <div class="btn-row">
            <a href="tel:{PHONE_LINK}" class="btn btn-primary">전화 상담 {PHONE}</a>
            <a href="{content["region_url"]}" class="btn btn-outline">{content["name"]} 폐기물처리 안내</a>
            <a href="/reviews/" class="btn btn-outline">작업후기 목록</a>
            <a href="/#contact" class="btn btn-outline">상담 접수</a>
          </div>
        </div>
      </div>
    </div>
  </section>
{related_section_html()}
</main>
{footer_html()}
</body>
</html>
"""


def list_page_html(seoul_cards, gyeonggi_cards):
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>서울·경기 폐기물처리 작업후기 | {BRAND}</title>
  <meta name="description" content="서울·경기 현장에서 진행한 쓰레기집청소, 빈집정리, 가정·이사·폐업폐기물처리 작업후기를 지역별로 정리했습니다." />
  <meta property="og:title" content="서울·경기 폐기물처리 작업후기 | {BRAND}" />
  <meta property="og:description" content="서울 25개 구·경기 31개 시·군 폐기물처리 작업후기 모음" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="{BASE_URL}/reviews/" />
  <link rel="icon" href="/favicon-allbarun.png" />
  <style>{SHARED_CSS}</style>
</head>
<body>
{header_html("reviews")}
<main>
  <section class="hero">
    <div class="hero-inner">
      <div class="badge">작업후기 모음</div>
      <h1>지역별 폐기물처리 작업후기</h1>
      <p>서울·경기 현장에서 진행한 쓰레기집청소, 빈집정리, 가정·이사·폐업폐기물처리 작업후기를 지역별로 정리했습니다.</p>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="title">
        <span>서울·경기 작업후기</span>
        <h2>실제 폐기물처리 작업후기</h2>
        <p>작업 전 상태와 정리·반출 후 공간이 자연스럽게 보이도록 구성했습니다. 전·후 사진은 현장마다 랜덤 배치됩니다.</p>
      </div>

      <div class="area-block">
        <h3>서울특별시 25개 구</h3>
        <div class="review-grid">
{seoul_cards}
        </div>
      </div>

      <div class="area-block">
        <h3>경기도 31개 시·군</h3>
        <div class="review-grid">
{gyeonggi_cards}
        </div>
      </div>
    </div>
  </section>

  <section class="related-section">
    <div class="wrap">
      <div class="cta-box" style="background:var(--card);">
        <h2>비슷한 현장 상담이 필요하신가요?</h2>
        <p>사진과 주소를 남겨주시면 폐기물 양과 작업 조건을 확인한 뒤 연락드립니다.</p>
        <div class="btn-row">
          <a href="tel:{PHONE_LINK}" class="btn btn-primary">전화 상담 {PHONE}</a>
          <a href="/#contact" class="btn btn-outline">상담 접수하기</a>
        </div>
      </div>
    </div>
  </section>
{related_section_html()}
</main>
{footer_html()}
</body>
</html>
"""


def generate():
    root = Path(__file__).resolve().parent
    reviews_dir = root / "reviews"
    reviews_dir.mkdir(exist_ok=True)

    contents = []
    for region_type, name, slug in REGIONS:
        content = review_content(region_type, name, slug)
        contents.append(content)

        region_dir = reviews_dir / slug
        region_dir.mkdir(exist_ok=True)
        (region_dir / "index.html").write_text(detail_page_html(content), encoding="utf-8")

    seoul_cards = "".join(
        review_card_html(c) for c in contents if c["region_type"] == "서울"
    )
    gyeonggi_cards = "".join(
        review_card_html(c) for c in contents if c["region_type"] == "경기"
    )

    (reviews_dir / "index.html").write_text(
        list_page_html(seoul_cards, gyeonggi_cards),
        encoding="utf-8",
    )

    print("완료: reviews/index.html 생성")
    print(f"완료: 지역별 작업후기 {len(contents)}개 생성")


if __name__ == "__main__":
    generate()
