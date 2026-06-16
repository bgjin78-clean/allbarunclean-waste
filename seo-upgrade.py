import os
import re

SEOUL = {
    "index.html": "서울",
    "gangnam.html": "서울 강남구",
    "gangdong.html": "서울 강동구",
    "gangbuk.html": "서울 강북구",
    "gangseo.html": "서울 강서구",
    "gwanak.html": "서울 관악구",
    "gwangjin.html": "서울 광진구",
    "guro.html": "서울 구로구",
    "geumcheon.html": "서울 금천구",
    "nowon.html": "서울 노원구",
    "dobong.html": "서울 도봉구",
    "dongdaemun.html": "서울 동대문구",
    "dongjak.html": "서울 동작구",
    "mapo.html": "서울 마포구",
    "seodaemun.html": "서울 서대문구",
    "seocho.html": "서울 서초구",
    "seongdong.html": "서울 성동구",
    "seongbuk.html": "서울 성북구",
    "songpa.html": "서울 송파구",
    "yangcheon.html": "서울 양천구",
    "yeongdeungpo.html": "서울 영등포구",
    "yongsan.html": "서울 용산구",
    "eunpyeong.html": "서울 은평구",
    "jongno.html": "서울 종로구",
    "jung.html": "서울 중구",
    "jungnang.html": "서울 중랑구",
}

GYEONGGI = {
    "index.html": "경기",
    "suwon.html": "경기 수원",
    "seongnam.html": "경기 성남",
    "goyang.html": "경기 고양",
    "yongin.html": "경기 용인",
    "bucheon.html": "경기 부천",
    "ansan.html": "경기 안산",
    "anyang.html": "경기 안양",
    "namyangju.html": "경기 남양주",
    "hwaseong.html": "경기 화성",
    "pyeongtaek.html": "경기 평택",
    "uijeongbu.html": "경기 의정부",
    "siheung.html": "경기 시흥",
    "paju.html": "경기 파주",
    "gimpo.html": "경기 김포",
    "gwangmyeong.html": "경기 광명",
    "gwangju.html": "경기 광주",
    "gunpo.html": "경기 군포",
    "hanam.html": "경기 하남",
    "osan.html": "경기 오산",
    "icheon.html": "경기 이천",
    "anseong.html": "경기 안성",
    "uiwang.html": "경기 의왕",
    "yangju.html": "경기 양주",
    "guri.html": "경기 구리",
    "pocheon.html": "경기 포천",
    "dongducheon.html": "경기 동두천",
    "gwacheon.html": "경기 과천",
    "yeoju.html": "경기 여주",
    "yangpyeong.html": "경기 양평",
    "gapyeong.html": "경기 가평",
    "yeoncheon.html": "경기 연천",
}

def seo_block(region):
    return f"""
<section class="section seo-content local-seo-upgrade">
  <div class="container">
    <p class="section-label">DETAIL GUIDE</p>
    <h2>{region} 폐기물처리 현장별 안내</h2>

    <p>
      {region} 폐기물처리는 단순히 물건을 치우는 작업이 아니라 현장 구조와 폐기물 종류,
      운반 동선, 차량 진입 가능 여부를 함께 확인해야 하는 작업입니다. 같은 폐기물이라도
      아파트, 빌라, 단독주택, 상가, 사무실, 창고 등 현장 조건에 따라 작업 방식과 비용이 달라질 수 있습니다.
    </p>

    <h3>{region} 쓰레기집청소가 필요한 경우</h3>
    <p>
      생활폐기물이 오랜 기간 쌓인 공간은 악취와 위생 문제가 함께 발생할 수 있습니다.
      {region} 쓰레기집청소는 폐기물 분류, 포장, 운반, 상차까지 한 번에 진행하는 것이 중요합니다.
      특히 혼자 정리하기 어려운 양이거나 엘리베이터 사용이 제한되는 현장은 작업 전 상담이 필요합니다.
    </p>

    <h3>{region} 빈집정리와 가정폐기물처리</h3>
    <p>
      빈집정리는 매매, 임대, 리모델링, 이사 준비 과정에서 많이 필요합니다.
      오래된 가구, 침대, 서랍장, 생활용품, 잡동사니 등이 남아 있으면 다음 입주나 공사 진행이 늦어질 수 있습니다.
      {region} 가정폐기물처리는 물건의 양과 종류를 확인한 뒤 적절한 차량과 인원을 배치해 진행합니다.
    </p>

    <h3>{region} 이사폐기물처리</h3>
    <p>
      이사 전후에는 평소보다 많은 불필요한 짐이 나옵니다.
      오래된 가전, 사용하지 않는 가구, 파손된 물품, 계절용품 등이 대표적입니다.
      이사 일정에 맞춰 폐기물을 미리 정리하면 새 공간으로 이동하는 과정이 훨씬 수월해집니다.
    </p>

    <h3>{region} 폐업폐기물처리</h3>
    <p>
      매장, 사무실, 창고 폐업 후에는 업종에 따라 다양한 폐기물이 발생합니다.
      책상, 의자, 진열대, 선반, 집기류, 포장재 등은 양이 많고 부피가 커 일반적인 배출만으로는 처리하기 어렵습니다.
      {region} 폐업폐기물처리는 현장 확인 후 작업 인원과 차량을 정해 진행하는 것이 안전합니다.
    </p>

    <h3>{region} 폐기물처리 비용이 달라지는 이유</h3>
    <p>
      일반폐기물은 30만원부터 시작하지만 실제 비용은 폐기물의 양, 층수, 엘리베이터 유무,
      차량 진입 가능 여부, 분리 작업 난이도, 작업 시간에 따라 달라집니다.
      사진 상담을 통해 대략적인 안내가 가능하며, 양이 많거나 현장 구조가 복잡한 경우에는 추가 확인이 필요할 수 있습니다.
    </p>
  </div>
</section>
"""

def faq_block(region):
    return f"""
<section class="section faq local-faq-upgrade">
  <div class="container">
    <p class="section-label">LOCAL FAQ</p>
    <h2>{region} 폐기물처리 자주 묻는 질문</h2>

    <div class="faq-list">
      <details>
        <summary>{region} 폐기물처리 비용은 얼마부터인가요?</summary>
        <p>일반폐기물은 30만원부터 시작합니다. 실제 비용은 폐기물 양, 층수, 엘리베이터 유무, 차량 진입 여부에 따라 달라집니다.</p>
      </details>

      <details>
        <summary>{region} 쓰레기집청소도 가능한가요?</summary>
        <p>가능합니다. 생활폐기물 정리, 포장, 운반, 상차까지 현장 상황에 맞춰 진행합니다.</p>
      </details>

      <details>
        <summary>사진만 보내도 견적 상담이 가능한가요?</summary>
        <p>가능합니다. 전체 공간 사진, 폐기물 양, 건물 입구와 엘리베이터 여부를 함께 보내주시면 더 빠르게 안내할 수 있습니다.</p>
      </details>

      <details>
        <summary>{region} 빈집정리는 어떤 경우에 필요하나요?</summary>
        <p>매매, 임대, 리모델링, 이사 전후로 남은 가구와 생활폐기물을 정리할 때 필요합니다.</p>
      </details>

      <details>
        <summary>폐업폐기물처리는 어떤 업종이 가능한가요?</summary>
        <p>사무실, 매장, 창고, 소형 업장 등 다양한 현장 상담이 가능합니다. 집기류와 폐기물 양에 따라 비용이 달라집니다.</p>
      </details>
    </div>
  </div>
</section>
"""

def update_file(path, region):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if "local-seo-upgrade" in content:
        print(f"skip already upgraded: {path}")
        return

    # 기존 기본 FAQ 섹션 하나 제거
    content = re.sub(
        r'<section class="section faq">.*?</section>\s*',
        '',
        content,
        count=1,
        flags=re.DOTALL
    )

    marker = '<section class="section contact">'
    if marker not in content:
        print(f"contact marker not found: {path}")
        return

    insert_html = seo_block(region) + "\n" + faq_block(region) + "\n"
    content = content.replace(marker, insert_html + marker)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"upgraded SEO: {path}")

def run():
    for filename, region in SEOUL.items():
        update_file(os.path.join("seoul", filename), region)

    for filename, region in GYEONGGI.items():
        update_file(os.path.join("gyeonggi", filename), region)

    print("완료: 서울·경기 58개 페이지 SEO 강화 완료")

if __name__ == "__main__":
    run()