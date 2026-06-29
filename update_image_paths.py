import os
import re

SEOUL = [
    "index.html", "gangnam.html", "gangdong.html", "gangbuk.html", "gangseo.html",
    "gwanak.html", "gwangjin.html", "guro.html", "geumcheon.html", "nowon.html",
    "dobong.html", "dongdaemun.html", "dongjak.html", "mapo.html", "seodaemun.html",
    "seocho.html", "seongdong.html", "seongbuk.html", "songpa.html", "yangcheon.html",
    "yeongdeungpo.html", "yongsan.html", "eunpyeong.html", "jongno.html", "jung.html",
    "jungnang.html",
]

GYEONGGI = [
    "index.html", "suwon.html", "seongnam.html", "goyang.html", "yongin.html",
    "bucheon.html", "ansan.html", "anyang.html", "namyangju.html", "hwaseong.html",
    "pyeongtaek.html", "uijeongbu.html", "siheung.html", "paju.html", "gimpo.html",
    "gwangmyeong.html", "gwangju.html", "gunpo.html", "hanam.html", "osan.html",
    "icheon.html", "anseong.html", "uiwang.html", "yangju.html", "guri.html",
    "pocheon.html", "dongducheon.html", "gwacheon.html", "yeoju.html", "gapyeong.html",
    "yangpyeong.html", "yeoncheon.html",
]


def update_region_file(path, after_num):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    after_tag = f"after-{after_num:02d}.jpg"
    new_hero = f'../images/main/{after_tag}'

    content = re.sub(
        r'\.\./images/(?:main/)?after-\d+\.jpg',
        new_hero,
        content,
        count=1,
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    return after_tag


def run():
    idx = 0
    updated = 0

    for folder, files in [("seoul", SEOUL), ("gyeonggi", GYEONGGI)]:
        for filename in files:
            idx += 1
            after_num = ((idx - 1) % 30) + 1
            path = os.path.join(folder, filename)
            if not os.path.exists(path):
                print(f"skip missing: {path}")
                continue
            tag = update_region_file(path, after_num)
            print(f"updated {path}: {tag}")
            updated += 1

    print(f"\n완료: {updated}개 지역 페이지 → images/main/ 경로 적용")


if __name__ == "__main__":
    run()
