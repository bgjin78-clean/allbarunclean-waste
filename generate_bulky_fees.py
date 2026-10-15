# -*- coding: utf-8 -*-
"""지역 페이지에 대형폐기물 품목별 수수료 섹션 생성.

python generate_bulky_fees.py build   # 원본(_bulky_raw.json, _bulky_files/*.csv) → data/bulky_fees.json
python generate_bulky_fees.py render  # data/bulky_fees.json → seoul/*.html, gyeonggi/*.html
"""
from __future__ import annotations

import csv
import html
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "bulky_fees.json"
COLLECTED = "2026-10-15"
MARKER_START = "<!-- bulky-fee:start -->"
MARKER_END = "<!-- bulky-fee:end -->"

STD_URL = "https://www.data.go.kr/data/15114146/standard.do"
STD_LABEL = "공공데이터포털 전국대형폐기물수거수수료정보표준데이터"

GUN = {"연천", "가평", "양평"}

# 표준데이터에 없는 지자체: 개별 공공데이터 파일 또는 지자체 공식 페이지
FILE_SOURCES: dict[str, dict] = {
    "성남시": {"file": "성남시.csv", "label": "공공데이터포털 경기도 성남시_대형폐기물 수거기준정보", "url": "https://www.data.go.kr/data/15032526/fileData.do"},
    "부천시": {"file": "부천시.csv", "label": "공공데이터포털 경기도 부천시_대형폐기물 처리수수료 현황", "url": "https://www.data.go.kr/data/15040943/fileData.do", "date": "2025-07-09"},
    "김포시": {"file": "김포시.csv", "label": "공공데이터포털 경기도 김포시_대형폐기물수수료정보", "url": "https://www.data.go.kr/data/15034879/fileData.do"},
    "포천시": {"file": "포천시.csv", "label": "공공데이터포털 경기도 포천시_대형폐기물수수료현황", "url": "https://www.data.go.kr/data/15061842/fileData.do"},
    "광진구": {"file": "광진구.csv", "label": "공공데이터포털 서울특별시 광진구_대형폐기물수집운반수수료", "url": "https://www.data.go.kr/data/15036341/fileData.do", "date": "2026-08-20"},
    "강북구": {"file": "강북구_부과기준.csv", "label": "공공데이터포털 서울특별시 강북구_대형폐기물 품목별 부과기준", "url": "https://www.data.go.kr/data/15055382/fileData.do"},
}

# 지자체 공식 페이지에서 수집한 자료 (조사 결과로 채움)
SITE_SOURCES: dict[str, dict] = {
    "금천구": {"file": "금천구.csv", "label": "금천구 스마트클린 대형폐기물 수수료 안내", "url": "https://smartclean.geumcheon.go.kr/online/bulky/item"},
    "영등포구": {"file": "영등포구.csv", "label": "영등포구청 대형폐기물 품목 및 수수료", "url": "https://www.ydp.go.kr/reserve/selectWstePrdWebPopList.do?key=4173"},
    "동작구": {"file": "동작구.csv", "label": "동작구 스마트클린 대형폐기물 수수료 안내", "url": "https://smartclean.dongjak.go.kr/online/bulky/item"},
    "송파구": {"file": "송파구.csv", "label": "송파구청 대형폐기물 품목별 수거기준 및 비용", "url": "https://www.songpa.go.kr/www/exhaustPrdlstList.do?key=2118&rep=1", "date_label": "페이지 수정일"},
    "강동구": {"file": "강동구.csv", "label": "강동구청 대형폐기물 수집·운반 수수료", "url": "https://www.gangdong.go.kr/web/newportal/largeWaste/code/list", "date_label": "페이지 수정일"},
    "의정부시": {"file": "의정부시.csv", "label": "공공데이터포털 의정부도시공사_대형폐기물 품목별 수수료", "url": "https://www.data.go.kr/data/15100221/fileData.do", "lookup": "https://www.uiuc.or.kr/businessInfo/environmentPage/bigtrash/list.do"},
    "하남시": {"file": "하남시.csv", "label": "하남시 대형폐기물 배출신고 처리비용안내", "url": "https://www.hanam.go.kr/clean/contents/order_item.php?cIdx=4", "date_label": "수수료 기준표 시행일", "lookup": "https://www.hanam.go.kr/clean/main/index.php"},
    "구리시": {"file": "구리시.csv", "label": "구리시청 대형폐기물 배출 수수료(조례 별표 2)", "url": "https://www.guri.go.kr/downloadContentsFile.do?key=767&fileNo=1021", "date_label": "조례 개정일"},
}

# 자료를 구하지 못한 지자체: 공식 조회 페이지 링크만 안내
LINK_ONLY: dict[str, dict] = {}

TOP_EXCLUDE = {
    "TV": ("장", "받침", "다이", "선반", "케이스", "테이블"),
    "소파": ("탁자", "테이블"),
    "의자": ("안마",),
    "장롱": ("비키니", "부속", "선반"),
    "식탁": ("의자",),
}

TOP_ITEMS = [
    ("장롱", ("장롱", "옷장")),
    ("침대", ("침대",)),
    ("매트리스", ("매트리스",)),
    ("소파", ("소파", "쇼파")),
    ("식탁", ("식탁",)),
    ("책상", ("책상",)),
    ("의자", ("의자",)),
    ("안마의자", ("안마의자",)),
    ("서랍장", ("서랍장",)),
    ("책장·책꽂이", ("책장", "책꽂이")),
    ("화장대", ("화장대",)),
    ("신발장", ("신발장",)),
    ("거실장·장식장", ("거실장", "장식장")),
    ("냉장고", ("냉장고",)),
    ("세탁기", ("세탁기",)),
    ("에어컨", ("에어컨",)),
    ("TV", ("TV", "텔레비전", "티브이", "티비")),
    ("전자레인지", ("전자레인지",)),
    ("피아노", ("피아노",)),
    ("자전거", ("자전거",)),
    ("러닝머신", ("런닝머신", "러닝머신")),
]


def official_name(folder: str, name: str) -> str:
    if folder == "seoul":
        return name
    if name.endswith(("시", "군")):
        return name
    return name + ("군" if name in GUN else "시")


def region_pages() -> list[tuple[Path, str, str]]:
    out = []
    title_re = re.compile(r"<title>(.+?) 폐기물처리")
    for folder, sido in (("seoul", "서울특별시"), ("gyeonggi", "경기도")):
        for path in sorted((ROOT / folder).glob("*.html")):
            if path.name == "index.html":
                continue
            m = title_re.search(path.read_text(encoding="utf-8"))
            if m:
                out.append((path, sido, official_name(folder, m.group(1))))
    return out


def clean(value) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def to_fee(value) -> int | None:
    digits = re.sub(r"[^\d]", "", str(value or ""))
    return int(digits) if digits else None


def pick(row: dict, *names: str) -> str:
    for n in names:
        if n in row and clean(row[n]):
            return clean(row[n])
    return ""


def rows_from_csv(path: Path, default_date: str = "") -> list[dict]:
    text = path.read_text(encoding="utf-8").lstrip("\ufeff")
    rows = []
    for r in csv.DictReader(io.StringIO(text)):
        r = {clean(k): v for k, v in r.items() if k}
        item = pick(r, "품목", "품명", "물품", "페기물품목", "폐기물품목", "대형폐기물명")
        fee = to_fee(pick(r, "수수료", "부과금액", "단가", "수거수수료(원)", "수수료(안)", "금액"))
        if not item or fee is None or item == "없는품목":
            continue
        rows.append({
            "cat": pick(r, "분류", "구분", "대분류", "대형폐기물구분명"),
            "item": item,
            "spec": pick(r, "규격", "대형폐기물규격"),
            "fee": fee,
            "date": pick(r, "기준일", "데이터기준일자", "데이터기준일") or default_date,
        })
    return rows


def dedupe(rows: list[dict]) -> list[dict]:
    seen, out = set(), []
    for r in rows:
        key = (r["item"], r["spec"], r["fee"])
        if key in seen:
            continue
        seen.add(key)
        out.append(r)
    return out


def build() -> None:
    raw = json.loads((ROOT / "_bulky_raw.json").read_text(encoding="utf-8"))
    std_rows = [r for page in raw["pages"] for r in page]
    regions = {}
    for path, sido, name in region_pages():
        key = f"{path.parent.name}/{path.stem}"
        entry = {"sido": sido, "name": name, "rows": [], "source": None}
        std = [r for r in std_rows if r["CTPV_NM"] == sido and r["SGG_NM"] == name]
        if std:
            rows = []
            for r in std:
                fee = 0 if clean(r["PAID_FREE_YN"]) == "무료" else to_fee(r["FEE"])
                if fee is None:
                    continue
                rows.append({
                    "cat": clean(r["LAR_WAS_SE_NM"]),
                    "item": clean(r["LAR_WAS_NM"]),
                    "spec": clean(r["LAR_WAS_SPCFCT"]),
                    "fee": fee,
                    "date": clean(r["CRTR_YMD"]),
                })
            entry["rows"] = rows
            entry["source"] = {"label": f"{STD_LABEL} ({clean(std[0]['MNG_INST_NM'])})", "url": STD_URL}
        elif name in FILE_SOURCES or name in SITE_SOURCES:
            src = FILE_SOURCES.get(name) or SITE_SOURCES[name]
            entry["rows"] = rows_from_csv(ROOT / "_bulky_files" / src["file"], src.get("date", ""))
            entry["source"] = {"label": src["label"], "url": src["url"]}
            if src.get("date_label"):
                entry["date_label"] = src["date_label"]
            if src.get("lookup"):
                entry["lookup"] = src["lookup"]
        if name in LINK_ONLY:
            entry["lookup"] = LINK_ONLY[name]["url"]
            entry["lookup_label"] = LINK_ONLY[name]["label"]
        entry["rows"] = dedupe(entry["rows"])
        dates = sorted({r["date"] for r in entry["rows"] if r["date"]})
        entry["date"] = dates[-1] if dates else ""
        regions[key] = entry
    DATA.parent.mkdir(exist_ok=True)
    DATA.write_text(json.dumps({"collected": COLLECTED, "regions": regions}, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    with open(ROOT / "_build_log.txt", "w", encoding="utf-8") as log:
        for key, e in regions.items():
            log.write(f"{key}\t{e['name']}\t{len(e['rows'])}\t{e['date']}\t{(e['source'] or {}).get('label', 'LINK-ONLY' if e.get('lookup') else 'NONE')}\n")


def won(fee: int) -> str:
    return "무료" if fee == 0 else f"{fee:,}원"


def top_rows(rows: list[dict]) -> list[tuple[str, str, int]]:
    out = []
    for label, keys in TOP_ITEMS:
        skip = TOP_EXCLUDE.get(label, ())
        hits = [
            r for r in rows
            if any(k in r["item"] for k in keys) and not any(s in r["item"] for s in skip)
        ]
        if not hits:
            continue
        lo = min(r["fee"] for r in hits)
        hi = max(r["fee"] for r in hits)
        out.append((label, won(lo) if lo == hi else f"{won(lo)} ~ {won(hi)}", len(hits)))
    return out


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def section_html(e: dict, short: str) -> str:
    name = e["name"]
    rows = e["rows"]
    if rows:
        top = "\n".join(
            f"          <tr><td>{esc(label)}</td><td class=\"fee\">{rng}</td><td>{n}개 규격</td></tr>"
            for label, rng, n in top_rows(rows)
        )
        ordered = sorted(rows, key=lambda r: (r["cat"], r["item"], r["fee"]))
        full = "\n".join(
            f"            <tr><td>{esc(r['cat'])}</td><td>{esc(r['item'])}</td><td>{esc(r['spec'])}</td><td class=\"fee\">{won(r['fee'])}</td></tr>"
            for r in ordered
        )
        src = e["source"]
        meta = (
            f'      <p class="fee-meta"><span><b>자료 수집일</b> {COLLECTED}</span>'
            f'<span><b>{e.get("date_label", "데이터 기준일")}</b> {e["date"] or "출처 미표기"}</span>'
            f'<span><b>출처</b> <a href="{esc(src["url"])}" target="_blank" rel="noopener">{esc(src["label"])}</a></span></p>'
        )
        body = f"""{meta}

      <h3>{esc(name)} 자주 버리는 대형폐기물 수수료</h3>
      <div class="fee-table-wrap">
        <table class="fee-table">
          <thead><tr><th>품목</th><th class="fee">수수료</th><th>규격 수</th></tr></thead>
          <tbody>
{top}
          </tbody>
        </table>
      </div>

      <details class="fee-all">
        <summary>{esc(name)} 대형폐기물 전체 품목 수수료 보기 ({len(rows)}개)</summary>
        <div class="fee-table-wrap">
          <table class="fee-table">
            <thead><tr><th>분류</th><th>품목</th><th>규격</th><th class="fee">수수료</th></tr></thead>
            <tbody>
{full}
            </tbody>
          </table>
        </div>
      </details>"""
    else:
        body = f"""      <p class="fee-meta"><span><b>자료 확인일</b> {COLLECTED}</span><span>{esc(name)}는 품목별 수수료를 공공데이터로 제공하지 않아 공식 조회 페이지로 안내합니다.</span></p>
      <p><a class="fee-link-btn" href="{esc(e['lookup'])}" target="_blank" rel="noopener">{esc(e.get('lookup_label') or name + ' 대형폐기물 수수료 조회')}</a></p>"""

    lookup = ""
    if rows:
        lookup = f'\n        <li>목록에 없는 품목은 보통 크기와 재질이 비슷한 품목 기준으로 부과됩니다.</li>'
    if rows and e.get("lookup"):
        lookup += f'\n        <li>배출 신고와 최종 금액 확인: <a href="{esc(e["lookup"])}" target="_blank" rel="noopener">{esc(name)} 대형폐기물 신고 페이지</a></li>'

    return f"""{MARKER_START}
<section class="section bulky-fee" id="bulky-fee">
  <div class="container">
    <p class="section-label">BULKY WASTE FEE</p>
    <h2>{esc(name)} 대형폐기물 수수료 (품목별)</h2>
    <p class="section-desc">{esc(e['sido'])} {esc(name)}에서 가구·가전 같은 대형폐기물을 내놓을 때 내는 배출 수수료를 품목별로 정리했습니다. 수수료는 지자체가 정하며 바뀔 수 있으니 배출 전 {esc(name)} 신고 화면에서 최종 금액을 확인하세요.</p>
{body}

      <ul class="fee-notes">
        <li>위 금액은 {esc(name)}에 내는 배출 수수료(스티커·인터넷 신고)이며, 집 안에서 지정 장소까지 옮기는 일은 직접 해야 합니다.</li>
        <li>냉장고·세탁기·에어컨·TV 등 대형 가전은 폐가전제품 무상방문수거(1599-0903)로 무료 배출할 수 있습니다.</li>{lookup}
        <li>품목이 많거나 계단·운반이 어렵다면 {BRAND}가 분류·운반·상차까지 한 번에 처리합니다. 일반폐기물 30만원부터.</li>
      </ul>
      <div class="fee-cta">
        <p>{esc(short)} 대형폐기물, 직접 옮기기 어려우신가요? 사진만 보내주시면 바로 견적을 드립니다.</p>
        <a href="tel:01043932414" class="btn primary">전화상담 010-4393-2414</a>
      </div>
  </div>
</section>
{MARKER_END}"""


BRAND = "올바른 폐기물처리"
PRICE_RE = re.compile(r'(<section class="section price">.*?</section>\n)', re.S)
NAV_LINK = '<a href="#bulky-fee">대형폐기물 수수료</a>'


def render() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    done = 0
    for key, e in data["regions"].items():
        if not e["rows"] and not e.get("lookup"):
            continue
        path = ROOT / f"{key}.html"
        page = path.read_text(encoding="utf-8")
        short = re.search(r"<title>(.+?) 폐기물처리", page).group(1)
        block = section_html(e, short)
        if MARKER_START in page:
            page = re.sub(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), lambda _: block, page, count=1, flags=re.S)
        else:
            page, n = PRICE_RE.subn(lambda m: m.group(1) + "\n" + block + "\n", page, count=1)
            if n != 1:
                raise SystemExit(f"price 섹션을 찾지 못했습니다: {path}")
        if NAV_LINK not in page:
            page = page.replace('      <a href="#contact">상담접수</a>\n    </nav>', f'      {NAV_LINK}\n      <a href="#contact">상담접수</a>\n    </nav>', 1)
        path.write_text(page, encoding="utf-8")
        done += 1
    print(f"rendered {done} pages")
    render_hubs(data)


def render_hubs(data: dict) -> None:
    for folder, label in (("seoul", "서울 25개 구"), ("gyeonggi", "경기 31개 시·군")):
        items = [
            (key.split("/")[1], e) for key, e in data["regions"].items()
            if key.startswith(folder + "/") and (e["rows"] or e.get("lookup"))
        ]
        links = "\n".join(
            f'      <a href="./{slug}.html#bulky-fee">{esc(e["name"])} 대형폐기물 수수료</a>' for slug, e in items
        )
        block = f"""{MARKER_START}
<section class="section region-links bulky-fee" id="bulky-fee">
  <div class="container">
    <p class="section-label">BULKY WASTE FEE</p>
    <h2>{label} 대형폐기물 수수료 (품목별)</h2>
    <p class="section-desc">지역을 선택하면 장롱·침대·소파·냉장고 등 대형폐기물 품목별 배출 수수료를 확인할 수 있습니다. 공공데이터와 지자체 공식 자료를 {COLLECTED}에 수집해 지역별 기준일·출처와 함께 정리했습니다.</p>
    <div class="region-grid">
{links}
    </div>
  </div>
</section>
{MARKER_END}"""
        path = ROOT / folder / "index.html"
        page = path.read_text(encoding="utf-8")
        if MARKER_START in page:
            page = re.sub(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), lambda _: block, page, count=1, flags=re.S)
        else:
            page, n = PRICE_RE.subn(lambda m: m.group(1) + "\n" + block + "\n", page, count=1)
            if n != 1:
                raise SystemExit(f"price 섹션을 찾지 못했습니다: {path}")
        if NAV_LINK not in page:
            page = page.replace('      <a href="#contact">상담접수</a>\n    </nav>', f'      {NAV_LINK}\n      <a href="#contact">상담접수</a>\n    </nav>', 1)
        path.write_text(page, encoding="utf-8")
    print("rendered hubs")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "all"
    if cmd in ("build", "all"):
        build()
    if cmd in ("render", "all"):
        render()
