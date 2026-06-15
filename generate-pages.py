import os

PHONE = "010-4393-2414"
DOMAIN = "https://waste.allbarunclean.com"

SEOUL = [
    ("서울", "index"),
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
    ("경기", "index"),
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

def html(region, slug, group):
    path = f"/{group}/" if slug == "index" else f"/{group}/{slug}.html"
    title_region = "서울" if group == "seoul" and slug == "index" else "경기" if group == "gyeonggi" and slug == "index" else region

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">

  <title>{title_region} 폐기물처리 | 올바른수거</title>
  <meta name="description" content="{title_region} 폐기물처리 전문. 쓰레기집청소, 빈집정리, 가정폐기물처리, 이사폐기물처리, 폐업폐기물처리 상담 가능. 일반폐기물 30만원부터.">
  <link rel="canonical" href="{DOMAIN}{path}">
  <link rel="stylesheet" href="../style.css">
  <link rel="icon" type="image/png" href="../favicon-allbarun.png">
</head>

<body>
<header class="site-header">
  <div class="container header-inner">
    <a href="../index.html" class="logo">올바른수거 <span>폐기물처리</span></a>
    <nav>
      <a href="../index.html#services">서비스</a>
      <a href="../index.html#price">비용</a>
      <a href="../index.html#contact">상담접수</a>
    </nav>
  </div>
</header>

<section class="hero">
  <div class="container hero-grid">
    <div class="hero-text">
      <p class="badge">{title_region} 지역 방문 가능</p>
      <h1>{title_region} 폐기물처리<br>정리부터 상차까지</h1>
      <p class="hero-desc">
        {title_region} 쓰레기집청소, 빈집정리, 가정폐기물처리, 이사폐기물처리, 폐업폐기물처리까지
        현장 상황에 맞춰 빠르게 상담합니다.
      </p>
      <div class="hero-buttons">
        <a href="tel:{PHONE}" class="btn primary">전화상담 {PHONE}</a>
        <a href="../index.html#contact" class="btn secondary">상담접수하기</a>
      </div>
    </div>

    <div class="hero-photo">
      <img src="../images/after-01.jpg" alt="{title_region} 폐기물처리 작업 완료 현장">
    </div>
  </div>
</section>

<section class="section seo-content">
  <div class="container">
    <p class="section-label">LOCAL SERVICE</p>
    <h2>{title_region} 폐기물처리 안내</h2>

    <p>
      {title_region}에서 생활공간이나 사업장을 정리하다 보면 예상보다 많은 폐기물이 발생할 수 있습니다.
      오래된 가구, 사용하지 않는 생활용품, 이사 과정에서 나온 짐, 폐업 후 남은 집기류는
      혼자 처리하기 어려운 경우가 많습니다.
    </p>

    <h3>{title_region} 쓰레기집청소</h3>
    <p>
      장기간 방치된 생활폐기물은 악취와 위생 문제를 만들 수 있어 빠른 정리가 중요합니다.
      현장 상황에 맞춰 분류, 운반, 상차를 함께 진행합니다.
    </p>

    <h3>{title_region} 빈집정리</h3>
    <p>
      매매, 임대, 리모델링 전 남아 있는 가구와 생활폐기물을 정리하면 다음 작업이 수월해집니다.
      공간 상태와 폐기물 양을 확인한 뒤 작업 방향을 안내합니다.
    </p>

    <h3>{title_region} 이사폐기물처리 · 가정폐기물처리</h3>
    <p>
      이사 전후 버릴 물건, 오래된 가구, 생활용품, 대형폐기물 등은 한 번에 정리하는 것이 효율적입니다.
      일반폐기물은 30만원부터 시작하며 실제 비용은 양과 현장 조건에 따라 달라집니다.
    </p>

    <h3>{title_region} 폐업폐기물처리</h3>
    <p>
      사무실, 매장, 창고 폐업 후 남은 집기와 폐기물은 종류와 양이 다양합니다.
      차량 진입 여부, 층수, 엘리베이터 유무, 분리 작업 난이도에 따라 작업 계획이 달라집니다.
    </p>
  </div>
</section>

<section class="section services">
  <div class="container">
    <p class="section-label">SERVICE</p>
    <h2>{title_region} 주요 서비스</h2>
    <div class="service-grid">
      <article><h3>쓰레기집청소</h3><p>방치된 생활폐기물과 정리하기 어려운 공간을 처리합니다.</p></article>
      <article><h3>빈집정리</h3><p>비어 있는 집이나 매매·임대 전 공간을 정리합니다.</p></article>
      <article><h3>가정폐기물처리</h3><p>가구, 생활용품, 대형폐기물을 수거합니다.</p></article>
      <article><h3>이사폐기물처리</h3><p>이사 전후 불필요한 짐을 한 번에 정리합니다.</p></article>
      <article><h3>폐업폐기물처리</h3><p>업장 정리 후 남은 집기와 폐기물을 처리합니다.</p></article>
    </div>
  </div>
</section>

<section class="section price">
  <div class="container price-box">
    <div>
      <p class="section-label">PRICE</p>
      <h2>{title_region} 폐기물처리 비용</h2>
    </div>
    <div class="price-info">
      <p>일반폐기물은 30만원부터 시작합니다.</p>
      <strong>정확한 비용은 폐기물 양과 현장 조건 확인 후 안내드립니다.</strong>
    </div>
  </div>
</section>

<section class="section faq">
  <div class="container">
    <p class="section-label">FAQ</p>
    <h2>{title_region} 폐기물처리 자주 묻는 질문</h2>
    <div class="faq-list">
      <details><summary>{title_region} 폐기물처리 비용은 얼마인가요?</summary><p>일반폐기물은 30만원부터이며 양, 층수, 차량 진입 여부에 따라 달라집니다.</p></details>
      <details><summary>사진만 보내도 상담 가능한가요?</summary><p>가능합니다. 폐기물 양과 현장 구조를 볼 수 있는 사진이면 좋습니다.</p></details>
      <details><summary>쓰레기집청소도 가능한가요?</summary><p>가능합니다. 생활폐기물 정리, 운반, 상차까지 현장 상황에 맞춰 진행합니다.</p></details>
    </div>
  </div>
</section>

<section class="section contact">
  <div class="container contact-box">
    <h2>{title_region} 폐기물처리 상담</h2>
    <p>빠른 상담은 전화 문의가 가장 정확합니다.</p>
    <div class="hero-buttons" style="margin-top:25px;">
      <a href="tel:{PHONE}" class="btn primary">전화상담 {PHONE}</a>
      <a href="../index.html#contact" class="btn secondary">상담접수하기</a>
    </div>
  </div>
</section>

<footer>
  <div class="container">
    <strong>올바른수거 폐기물처리</strong>
    <p>서울·경기 폐기물처리 전문 | {PHONE}</p>
    <p style="margin-top:15px;font-size:13px;opacity:.7;">© 올바른수거 폐기물처리 All Rights Reserved.</p>
  </div>
</footer>

</body>
</html>
"""

def make_pages(group, items):
    os.makedirs(group, exist_ok=True)

    for region, slug in items:
        filename = "index.html" if slug == "index" else f"{slug}.html"
        filepath = os.path.join(group, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html(region, slug, group))

        print(f"created: {filepath}")

make_pages("seoul", SEOUL)
make_pages("gyeonggi", GYEONGGI)

print("완료: 서울 26개, 경기 32개 = 총 58페이지 생성")