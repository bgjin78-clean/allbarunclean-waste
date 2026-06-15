import os
import re

PHONE = "010-4393-2414"

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

def contact_section(region):
    return f"""
<section class="section contact">
  <div class="container contact-box">
    <h2>{region} 폐기물처리 상담접수</h2>
    <p>사진을 준비해두시면 더 빠르게 안내받을 수 있습니다.</p>

    <form id="contactForm">
      <input type="text" placeholder="이름" required>
      <input type="tel" placeholder="연락처" required>
      <input type="text" placeholder="작업 지역" value="{region}" required>

      <select required>
        <option value="">서비스 선택</option>
        <option>쓰레기집청소</option>
        <option>빈집정리</option>
        <option>가정폐기물처리</option>
        <option>이사폐기물처리</option>
        <option>폐업폐기물처리</option>
        <option>기타 폐기물처리</option>
      </select>

      <textarea placeholder="폐기물 양, 건물 형태, 엘리베이터 유무 등을 적어주세요."></textarea>

      <div class="privacy-box">
        <label>
          <input type="checkbox" required>
          개인정보 수집 및 이용에 동의합니다.
        </label>

        <div class="privacy-text">
          수집항목 : 이름, 연락처, 작업지역<br>
          수집목적 : 상담 및 견적 안내<br>
          보유기간 : 상담 종료 후 즉시 파기
        </div>
      </div>

      <button type="submit">상담 접수하기</button>
      <p id="formMessage" class="form-message"></p>
    </form>
  </div>
</section>
"""

def ensure_scripts(content):
    if "emailjs/browser@4" not in content:
        content = content.replace(
            '<script src="../script.js"></script>',
            '<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>\n<script src="../script.js"></script>'
        )

    if '<script src="../script.js"></script>' not in content:
        content = content.replace(
            "</body>",
            '<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>\n<script src="../script.js"></script>\n</body>'
        )

    return content

def update_file(path, region):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    if 'id="contactForm"' in content:
        print(f"skip existing form: {path}")
        return

    # 기존 전화상담용 contact 섹션이 있으면 삭제
    content = re.sub(
        r'<section class="section contact">.*?</section>\s*',
        '',
        content,
        flags=re.DOTALL
    )

    form_html = contact_section(region)

    marker = "<footer>"
    if marker not in content:
        print(f"footer marker not found: {path}")
        return

    content = content.replace(marker, form_html + "\n" + marker)
    content = ensure_scripts(content)

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"updated contact form: {path}")

def run():
    for filename, region in SEOUL.items():
        update_file(os.path.join("seoul", filename), region)

    for filename, region in GYEONGGI.items():
        update_file(os.path.join("gyeonggi", filename), region)

    print("완료: 서울·경기 58개 페이지 상담폼 추가")

if __name__ == "__main__":
    run()