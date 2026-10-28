# -*- coding: utf-8 -*-
"""남양주·의정부·구리·포천·성남 추가 작업후기(지역별 2개) 생성.

이미 있는 후기 폴더는 다시 쓰지 않는다(게시일 유지). 새 지역을 추가하려면 REGIONS에 항목을 넣고 실행.
"""
from __future__ import annotations

import re
from pathlib import Path

from add_keyword_reviews import detail_page_html, keyword_meta

MARKER_START = "<!-- more-reviews:start -->"
MARKER_END = "<!-- more-reviews:end -->"

REGIONS = [
    {
        "slug": "namyangju",
        "sido": "경기",
        "name": "남양주시",
        "short": "남양주",
        "page": "/gyeonggi/namyangju.html",
        "guide_url": "https://namyangju.allbarunclean.com/",
        "existing_tag": "빈집정리",
        "existing_title": "남양주시 상가 빈집정리 작업후기",
        "reviews": {
            "pyeup": {
                "place": "사무실",
                "dong": "다산동",
                "title": "남양주시 다산 지식산업센터 사무실 폐업폐기물처리 작업후기",
                "summary": "경기 남양주시 다산동 지식산업센터 사무실 폐업 후 남은 책상·의자·사무용품과 진열 선반을 하루에 비운 현장입니다.",
                "desc": "남양주 다산 사무실 폐업폐기물처리 후기. 책상·의자·선반·사무용품을 하루 만에 분류·반출해 원상복구 전 공실로 정리. 30만원부터, 사진 견적.",
                "floor": "6층, 화물 엘리베이터 사용",
                "duration": "약 5시간",
                "vehicle": "2.5톤 트럭 1대",
                "items": ["사무용 책상·의자", "진열 선반·수납장", "복합기·소형 가전", "서류 박스·포장재", "매장 소품·잡자재"],
                "before": [87, 78],
                "after": [87, 78],
                "lead": "남양주시 폐업폐기물처리는 다산·별내 지식산업센터처럼 화물 엘리베이터 예약과 하역장 사용 시간이 정해진 건물이 많습니다. 다산동 사무실은 관리단에 하역장 사용을 신청한 뒤 오전부터 작업했습니다.",
                "story": [
                    "임대 종료일에 맞춰 원상복구 공사가 잡혀 있어 하루 안에 비워야 하는 현장이었습니다. 책상과 의자, 벽면 선반, 박스에 담긴 사무용품이 사무실 전체에 남아 있었습니다.",
                    "책상과 선반은 해체해 부피를 줄였고, 재활용 가능한 금속·종이류와 일반 폐기물을 나눠 상차했습니다. 작업이 끝난 뒤 바닥까지 드러난 빈 사무실 상태로 관리단 확인을 받았습니다.",
                ],
                "faqs": [
                    ("남양주 사무실 폐업폐기물처리, 하루 안에 끝나나요?", "사무실 한 호실 규모는 대부분 하루 안에 끝납니다. 짐 양과 엘리베이터 사용 시간에 따라 인원과 차량을 맞춥니다."),
                    ("원상복구 공사 전에 집기만 먼저 빼 줄 수 있나요?", "가능합니다. 공사 일정에 맞춰 집기·잔여물 반출만 먼저 진행하는 경우가 많습니다."),
                    ("남양주 폐업폐기물처리 비용은 어떻게 정해지나요?", "일반폐기물 30만원부터이며 집기 수량, 층수, 하역 조건에 따라 달라집니다. 사진을 보내주시면 먼저 안내드립니다."),
                ],
            },
            "sseuregi": {
                "place": "빌라",
                "dong": "진접읍",
                "title": "남양주시 진접 빌라 쓰레기집청소 작업후기",
                "summary": "경기 남양주시 진접읍 빌라 방 안까지 쌓인 쓰레기봉투와 생활 잡동사니를 반출하고 바닥이 보이게 정리한 현장입니다.",
                "desc": "남양주 진접 빌라 쓰레기집청소 후기. 방 안을 채운 쓰레기봉투·잡동사니를 봉투째 포장해 계단 반출. 이웃 눈치 걱정 없이 진행, 30만원부터 사진 견적.",
                "floor": "2층, 계단 반출",
                "duration": "약 5시간",
                "vehicle": "1톤 트럭 2회 운반",
                "items": ["쓰레기봉투", "음식물·생활 쓰레기", "옷가지·이불", "박스·잡동사니", "작은 가구"],
                "before": [85, 43],
                "after": [85, 43],
                "lead": "남양주시 쓰레기집청소는 진접·오남처럼 오래된 빌라가 많은 지역에서 계단 반출과 골목 주차를 함께 고려해야 합니다. 진접읍 빌라는 이웃 통행이 적은 오전 시간에 작업을 시작했습니다.",
                "story": [
                    "방 한쪽을 검은 봉투가 채우고 있었고, 다른 방은 옷가지와 잡동사니가 바닥을 덮고 있었습니다. 의뢰인과 남길 물건을 먼저 정한 뒤, 나머지는 봉투째 다시 포장해 계단으로 내렸습니다.",
                    "악취가 퍼지지 않도록 포장한 봉투는 바로 상차했고, 양이 많아 1톤 차량으로 두 번 운반했습니다. 작업 후에는 바닥과 벽이 드러나 청소와 도배 일정을 바로 잡을 수 있었습니다.",
                ],
                "faqs": [
                    ("쓰레기집청소할 때 이웃에게 알려지지 않을까요?", "포장한 상태로 빠르게 반출하고, 통행이 적은 시간에 작업 시간을 맞춰 노출을 줄입니다."),
                    ("남길 물건과 버릴 물건은 어떻게 구분하나요?", "작업 전 의뢰인과 남길 물건을 먼저 정하고, 귀중품·서류가 나오면 따로 모아 전달합니다."),
                    ("남양주 쓰레기집청소 비용은 얼마인가요?", "30만원부터이며 쓰레기 양과 층수, 운반 횟수에 따라 달라집니다. 방별 사진을 보내주시면 먼저 안내드립니다."),
                ],
            },
        },
    },
    {
        "slug": "seongnam",
        "sido": "경기",
        "name": "성남시",
        "short": "성남",
        "page": "/gyeonggi/seongnam.html",
        "guide_url": "https://seongnam.allbarunclean.com/",
        "existing_tag": "빈집정리",
        "existing_title": "성남시 오래 비운 주택 정리 작업후기",
        "reviews": {
            "pyeup": {
                "place": "사무실",
                "dong": "상대원동",
                "title": "성남시 상대원동 사무실 폐업폐기물처리 작업후기",
                "summary": "경기 성남시 중원구 상대원동 사무실 폐업 후 쌓인 박스 재고와 접이식 책상·의자를 반출해 공실로 정리한 현장입니다.",
                "desc": "성남 상대원동 사무실 폐업폐기물처리 후기. 박스 재고·접이식 책상·의자·사무용품을 반나절 만에 반출. 원상복구 일정 맞춤, 30만원부터 사진 견적.",
                "floor": "4층, 엘리베이터 사용",
                "duration": "약 4시간",
                "vehicle": "2.5톤 트럭 1대",
                "items": ["박스 재고·포장재", "접이식 책상", "사무용 의자", "철제 선반", "사무용품·잡자재"],
                "before": [18, 20],
                "after": [18, 20],
                "lead": "성남시 폐업폐기물처리는 상대원동 공단 지역처럼 박스 재고와 집기가 함께 남는 사무실이 많습니다. 상대원동 사무실은 건물 엘리베이터 사용 시간을 확인하고 짐을 층별로 모아 반출했습니다.",
                "story": [
                    "폐업 후 정리하지 못한 재고 박스가 사무실 바닥과 벽면을 따라 쌓여 있었고, 접이식 책상과 의자가 한쪽에 모여 있었습니다.",
                    "박스는 종이류로 따로 모으고, 책상과 의자는 접어 한 번에 상차했습니다. 작업 후 넓은 바닥이 드러나 다음 임차인 입주 전 원상복구를 바로 진행할 수 있었습니다.",
                ],
                "faqs": [
                    ("성남 폐업폐기물처리, 재고 박스도 같이 처리하나요?", "처리합니다. 종이류와 일반 폐기물을 분류해 함께 반출합니다."),
                    ("상대원동·성남하이테크밸리 건물도 작업되나요?", "됩니다. 건물별 엘리베이터·하역 규정을 확인하고 일정을 맞춥니다."),
                    ("성남 사무실 폐업 정리 비용은 얼마부터인가요?", "일반폐기물 30만원부터입니다. 집기 수량과 층수, 차량 대수에 따라 달라집니다."),
                ],
            },
            "sseuregi": {
                "place": "원룸",
                "dong": "태평동",
                "title": "성남시 태평동 원룸 쓰레기집청소 작업후기",
                "summary": "경기 성남시 수정구 태평동 원룸에 쌓인 생활 쓰레기와 잡동사니를 하루에 비우고 바닥까지 정리한 현장입니다.",
                "desc": "성남 태평동 원룸 쓰레기집청소 후기. 바닥을 덮은 생활 쓰레기·잡동사니를 하루에 분류·반출해 퇴거 전 상태로 정리. 비밀 상담 가능, 30만원부터.",
                "floor": "3층, 계단 반출",
                "duration": "약 4시간",
                "vehicle": "1톤 트럭 1대",
                "items": ["생활 쓰레기", "옷가지·침구", "배달 용기·페트병", "소형 가전", "잡동사니"],
                "before": [10, 97],
                "after": [10, 97],
                "lead": "성남시 쓰레기집청소는 태평·수진동처럼 원룸과 다가구 주택이 밀집한 지역에서 많이 진행됩니다. 태평동 원룸은 골목이 좁아 차량을 건물 앞에 짧게 대고 나눠 상차했습니다.",
                "story": [
                    "방 바닥이 옷가지와 생활 쓰레기, 배달 용기로 덮여 있어 출입부터 통로를 확보해야 했습니다. 다른 방에는 공구와 잡동사니가 높게 쌓여 있었습니다.",
                    "재활용품과 일반 쓰레기를 나눠 포장하고, 소형 가전은 따로 모아 반출했습니다. 작업 후 장판이 드러난 빈 방 상태가 되어 집주인 퇴거 확인을 받을 수 있었습니다.",
                ],
                "faqs": [
                    ("성남 쓰레기집청소, 의뢰 내용이 외부에 알려지나요?", "상담 내용과 현장 사진은 견적 외 용도로 쓰지 않으며, 작업도 포장 반출로 조용히 진행합니다."),
                    ("집주인 퇴거 일정에 맞춰 진행할 수 있나요?", "가능합니다. 퇴거일과 집주인 확인 일정을 알려주시면 그 전에 작업을 마칩니다."),
                    ("성남 원룸 쓰레기집청소는 얼마나 걸리나요?", "원룸은 보통 3~5시간입니다. 쓰레기 양과 계단 반출 여부에 따라 달라집니다."),
                ],
            },
        },
    },
    {
        "slug": "uijeongbu",
        "sido": "경기",
        "name": "의정부시",
        "short": "의정부",
        "page": "/gyeonggi/uijeongbu.html",
        "guide_url": "https://uijeongbu.allbarunclean.com/",
        "existing_tag": "이사폐기물",
        "existing_title": "의정부시 오피스텔 이사폐기물처리 작업후기",
        "reviews": {
            "saenghwal": {
                "place": "아파트",
                "dong": "민락동",
                "title": "의정부시 민락동 아파트 생활폐기물처리 작업후기",
                "summary": "경기 의정부시 민락동 아파트 베란다와 작은방에 쌓인 생활용품·소형 가전·잡동사니를 정리한 현장입니다.",
                "desc": "의정부 민락동 아파트 생활폐기물처리 후기. 베란다·작은방에 쌓인 생활용품·소형가전을 3시간 만에 반출. 엘리베이터 반출, 30만원부터 사진 견적.",
                "floor": "9층, 엘리베이터 사용",
                "duration": "약 3시간",
                "vehicle": "1톤 트럭 1대",
                "items": ["베란다 수납용품", "소형 가전", "옷가지·잡화", "플라스틱 통·대야", "생활폐기물 봉투"],
                "before": [2, 72],
                "after": [2, 72],
                "lead": "의정부시 생활폐기물처리는 민락·고산 신축 단지처럼 엘리베이터 보호재 설치와 사용 시간 신청이 필요한 아파트가 많습니다. 민락동 아파트는 관리사무소에 엘리베이터 사용을 신청한 뒤 작업했습니다.",
                "story": [
                    "베란다에는 대야와 플라스틱 통, 수납용품이 창문 높이까지 쌓여 있었고, 작은방에는 쓰지 않는 소형 가전과 잡화가 바닥에 흩어져 있었습니다.",
                    "쓸 물건은 거실로 옮겨 두고 나머지를 분류해 반출했습니다. 작업 후 베란다 바닥과 창이 드러나 환기와 청소를 바로 할 수 있는 상태가 되었습니다.",
                ],
                "faqs": [
                    ("의정부 생활폐기물처리, 베란다 짐만 따로 맡길 수 있나요?", "가능합니다. 베란다·창고처럼 일부 공간만 정리하는 작업도 진행합니다."),
                    ("의정부 아파트는 엘리베이터 신청을 해야 하나요?", "단지마다 다릅니다. 필요하면 일정 확정 후 관리사무소 신청 방법을 함께 안내드립니다."),
                    ("의정부 생활폐기물처리 비용은 얼마부터인가요?", "일반폐기물 30만원부터이며 양과 층수, 엘리베이터 사용 여부에 따라 달라집니다."),
                ],
            },
            "pyeup": {
                "place": "공방·사무실",
                "dong": "의정부동",
                "title": "의정부시 의정부동 공방 폐업폐기물처리 작업후기",
                "summary": "경기 의정부시 의정부동 상가 2층 공방 폐업 후 작업대·선풍기·자재와 가구를 반출해 빈 상가로 정리한 현장입니다.",
                "desc": "의정부동 공방 폐업폐기물처리 후기. 작업대·자재·가구·잡자재를 하루에 분류·반출해 임대 반납 전 빈 상가로 정리. 30만원부터, 사진만 보내면 견적.",
                "floor": "2층, 계단 반출",
                "duration": "약 5시간",
                "vehicle": "1톤 트럭 2회 운반",
                "items": ["작업대·책상", "자재·공구류", "선풍기·소형 가전", "수납 가구", "잡자재·포장재"],
                "before": [99, 100],
                "after": [99, 100],
                "lead": "의정부시 폐업폐기물처리는 의정부역·제일시장 주변처럼 오래된 상가 건물이 많아 계단 반출이 흔합니다. 의정부동 공방은 엘리베이터가 없어 인원을 늘려 계단으로 반출했습니다.",
                "story": [
                    "작업대 위와 바닥에 자재와 공구, 선풍기, 생활용품이 섞여 있었고, 안쪽 방에는 가구와 박스가 함께 쌓여 있었습니다.",
                    "의뢰인이 가져갈 공구를 먼저 따로 모은 뒤 나머지를 품목별로 나눠 내렸습니다. 작업 후 벽면 선반만 남은 빈 상가가 되어 임대 반납 점검을 받을 수 있었습니다.",
                ],
                "faqs": [
                    ("의정부 상가 폐업폐기물처리, 계단만 있어도 되나요?", "됩니다. 계단 반출 인원을 맞춰 진행하며 층수에 따라 비용이 조정될 수 있습니다."),
                    ("가져갈 물건과 버릴 물건이 섞여 있어도 되나요?", "괜찮습니다. 작업 전에 가져갈 물건을 표시해 주시면 따로 모아 두고 나머지만 반출합니다."),
                    ("의정부 폐업 정리 견적은 어떻게 받나요?", "공간 사진과 주소, 층수를 010-4393-2414로 보내주시면 대략 비용을 안내드리고 현장에서 확정합니다."),
                ],
            },
        },
    },
    {
        "slug": "guri",
        "sido": "경기",
        "name": "구리시",
        "short": "구리",
        "page": "/gyeonggi/guri.html",
        "guide_url": "https://www.guri.allbarunclean.com/",
        "existing_tag": "이사폐기물",
        "existing_title": "구리시 이사 전후 폐기물 정리 작업후기",
        "reviews": {
            "saenghwal": {
                "place": "아파트",
                "dong": "인창동",
                "title": "구리시 인창동 아파트 생활폐기물처리 작업후기",
                "summary": "경기 구리시 인창동 아파트 주방·다용도실에 쌓인 생활폐기물과 오래된 식탁·수납장을 정리한 현장입니다.",
                "desc": "구리 인창동 아파트 생활폐기물처리 후기. 주방·다용도실 잡동사니와 식탁·수납장을 3시간 반 만에 반출. 엘리베이터 반출, 30만원부터 사진 견적.",
                "floor": "12층, 엘리베이터 사용",
                "duration": "약 3시간 30분",
                "vehicle": "1톤 트럭 1대",
                "items": ["식탁·의자", "주방 수납장", "다용도실 잡동사니", "소형 가전", "생활폐기물 봉투"],
                "before": [26, 82],
                "after": [26, 82],
                "lead": "구리시 생활폐기물처리는 인창·교문동처럼 오래된 아파트 단지에서 주방과 다용도실 정리를 함께 맡기는 경우가 많습니다. 인창동 아파트는 엘리베이터로 반출하고 단지 내 주차 위치를 미리 확인했습니다.",
                "story": [
                    "다용도실에는 세탁기 주변으로 생활용품과 박스가 쌓여 있었고, 주방 식탁 위와 주변에는 쓰지 않는 집기가 가득했습니다.",
                    "식탁과 수납장은 분해해 반출하고, 생활폐기물은 봉투에 나눠 담았습니다. 작업 후 주방 바닥이 드러나 리모델링 견적을 바로 받을 수 있는 상태가 되었습니다.",
                ],
                "faqs": [
                    ("구리 생활폐기물처리, 주방 집기만 정리해도 되나요?", "됩니다. 주방·다용도실처럼 공간 단위로 범위를 정해 진행할 수 있습니다."),
                    ("오래된 식탁이나 수납장도 같이 가져가나요?", "가능합니다. 분해가 필요한 가구는 현장에서 해체해 함께 반출합니다."),
                    ("구리 생활폐기물처리 비용은 얼마부터인가요?", "일반폐기물 30만원부터입니다. 양과 층수, 가구 해체 여부에 따라 달라집니다."),
                ],
            },
            "binjip": {
                "place": "주택",
                "dong": "수택동",
                "title": "구리시 수택동 오래 비운 주택 빈집정리 작업후기",
                "summary": "경기 구리시 수택동에서 오래 비워 둔 주택의 베란다 짐과 주방 집기, 남은 가구를 모두 비워 매매 준비를 도운 현장입니다.",
                "desc": "구리 수택동 빈집정리 후기. 오래 비운 주택의 베란다 짐·주방 집기·가구를 하루에 비워 매매·임대 준비 완료. 30만원부터, 사진 보내면 바로 견적.",
                "floor": "2층 주택, 계단 반출",
                "duration": "약 6시간",
                "vehicle": "1톤 트럭 2회 운반",
                "items": ["베란다 화분·수납용품", "주방 그릇·집기", "장롱·수납 가구", "이불·옷가지", "생활 잡동사니"],
                "before": [74, 95],
                "after": [74, 95],
                "lead": "구리시 빈집정리는 수택·토평동처럼 오래된 주택이 많은 지역에서 매매나 임대 전에 맡기는 경우가 많습니다. 수택동 주택은 골목 안쪽이라 차량 위치를 정하고 짐을 나눠 반출했습니다.",
                "story": [
                    "몇 년간 비어 있던 집이라 베란다에는 화분과 수납용품이, 주방에는 그릇과 조리도구가 그대로 남아 있었습니다.",
                    "가족이 보관할 사진과 서류를 먼저 찾아 전달한 뒤, 가구와 집기를 차례로 비웠습니다. 작업 후 베란다와 주방이 비워져 매매 사진 촬영과 수리 견적을 바로 진행할 수 있었습니다.",
                ],
                "faqs": [
                    ("구리 빈집정리, 집주인이 현장에 없어도 되나요?", "가능합니다. 출입 방법을 정하고 작업 전후 사진으로 진행 상황을 보내드립니다."),
                    ("빈집정리 중 사진·서류가 나오면 어떻게 하나요?", "버리지 않고 따로 모아 전달합니다. 보관할 물건을 미리 알려주시면 먼저 찾아 둡니다."),
                    ("구리 빈집정리 비용은 어떻게 정해지나요?", "30만원부터이며 집 크기, 남은 짐 양, 반출 동선에 따라 달라집니다."),
                ],
            },
        },
    },
    {
        "slug": "pocheon",
        "sido": "경기",
        "name": "포천시",
        "short": "포천",
        "page": "/gyeonggi/pocheon.html",
        "guide_url": "https://pocheon.allbarunclean.com/",
        "existing_tag": "빈집정리",
        "existing_title": "포천시 오래 비운 주택 정리 작업후기",
        "reviews": {
            "isa": {
                "place": "아파트",
                "dong": "소흘읍",
                "title": "포천시 소흘읍 아파트 이사폐기물처리 작업후기",
                "summary": "경기 포천시 소흘읍 아파트 이사 전, 옷장과 행거·침구, 가져가지 않을 가구를 정리해 퇴거 준비를 마친 현장입니다.",
                "desc": "포천 소흘읍 아파트 이사폐기물처리 후기. 옷장·행거·침구·가구를 이사 전날 3시간 만에 반출. 송우리·소흘 당일 상담, 30만원부터 사진 견적.",
                "floor": "7층, 엘리베이터 사용",
                "duration": "약 3시간",
                "vehicle": "1톤 트럭 1대",
                "items": ["옷장·붙박이장 내부 짐", "행거·옷가지", "침구·매트", "작은 가구", "이사 잔짐 박스"],
                "before": [9, 41],
                "after": [9, 41],
                "lead": "포천시 이사폐기물처리는 소흘읍 송우리 아파트 단지처럼 이사 날짜에 맞춰 하루 전에 버릴 짐을 먼저 빼는 경우가 많습니다. 소흘읍 아파트는 이사 전날 오후에 작업했습니다.",
                "story": [
                    "안방에는 행거와 옷가지, 침구가 바닥에 쌓여 있었고, 작은방 붙박이장 안에도 가져가지 않을 옷과 박스가 남아 있었습니다.",
                    "옷가지와 침구는 포장해 내리고, 행거와 작은 가구는 해체해 상차했습니다. 작업 후 붙박이장과 방이 비워져 다음 날 이삿짐 반출이 수월해졌습니다.",
                ],
                "faqs": [
                    ("포천 이사폐기물처리, 이사 전날에도 예약되나요?", "일정이 비어 있으면 가능합니다. 이사 날짜가 정해지면 미리 사진 상담을 남겨 주세요."),
                    ("송우리·선단동·신읍동도 방문하나요?", "방문합니다. 포천시 전 지역을 상담하며 거리와 일정에 따라 시간을 조율합니다."),
                    ("포천 이사폐기물처리 비용은 얼마부터인가요?", "일반폐기물 30만원부터입니다. 짐 양과 층수, 엘리베이터 여부에 따라 달라집니다."),
                ],
            },
            "saenghwal": {
                "place": "주택",
                "dong": "신읍동",
                "title": "포천시 신읍동 주택 생활폐기물처리 작업후기",
                "summary": "경기 포천시 신읍동 주택 방에 쌓인 이불·옷가지와 오래된 가구, 생활 잡동사니를 정리한 현장입니다.",
                "desc": "포천 신읍동 주택 생활폐기물처리 후기. 방마다 쌓인 이불·옷가지·장롱·잡동사니를 4시간 만에 반출. 30만원부터, 사진만 보내면 바로 견적.",
                "floor": "단층 주택, 마당 반출",
                "duration": "약 4시간",
                "vehicle": "1톤 트럭 1대",
                "items": ["장롱·서랍장", "이불·옷가지", "가방·잡화", "생활용품", "생활폐기물 봉투"],
                "before": [70, 94],
                "after": [70, 94],
                "lead": "포천시 생활폐기물처리는 신읍·어룡동처럼 단독주택이 많은 지역에서 마당까지 차량 진입이 되는지가 작업 시간을 좌우합니다. 신읍동 주택은 대문 앞에 차량을 대고 마당을 거쳐 반출했습니다.",
                "story": [
                    "안방에는 이불과 옷가지, 가방이 침대 주변을 덮고 있었고, 작은방에는 생활용품과 잡동사니가 바닥에 쌓여 있었습니다.",
                    "장롱과 서랍장을 비운 뒤 해체해 내리고, 이불과 옷가지는 봉투에 나눠 담았습니다. 작업 후 방바닥이 드러나 도배·장판 교체를 바로 진행할 수 있었습니다.",
                ],
                "faqs": [
                    ("포천 단독주택 생활폐기물처리도 되나요?", "됩니다. 마당·대문 앞 차량 진입 여부를 확인하고 반출 동선을 정합니다."),
                    ("장롱처럼 큰 가구도 함께 처리하나요?", "처리합니다. 현장에서 해체해 생활폐기물과 함께 반출합니다."),
                    ("포천 생활폐기물처리 상담에 필요한 정보는?", "주소, 방별 사진, 차량 진입 가능 여부입니다. 010-4393-2414로 보내주셔도 됩니다."),
                ],
            },
        },
    },
]


def write_pages(root: Path) -> list[str]:
    created = []
    for region in REGIONS:
        kinds = list(region["reviews"])
        for kind in kinds:
            folder = f"{region['slug']}-{kind}"
            out = root / "reviews" / folder / "index.html"
            if out.exists():
                continue
            sibling_kind = kinds[1] if kind == kinds[0] else kinds[0]
            html = detail_page_html(region, kind, region["reviews"][kind], folder, region["reviews"][sibling_kind], sibling_kind)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html, encoding="utf-8")
            created.append(folder)
    return created


def card(region: dict, kind: str, indent: str = "        ") -> str:
    data = region["reviews"][kind]
    tag = keyword_meta(kind)[0]
    return (
        f'{indent}<article class="review-card">\n'
        f'{indent}  <span class="review-tag">{tag}</span>\n'
        f'{indent}  <h3>{data["title"]}</h3>\n'
        f'{indent}  <p>{data["summary"]}</p>\n'
        f'{indent}  <a href="/reviews/{region["slug"]}-{kind}/" class="review-link">자세히 보기 →</a>\n'
        f'{indent}</article>'
    )


def update_reviews_index(root: Path) -> None:
    path = root / "reviews" / "index.html"
    html = path.read_text(encoding="utf-8")
    cards = "\n".join(card(r, k) for r in REGIONS for k in r["reviews"])
    section = f"""{MARKER_START}
      <div class="area-block">
        <h3>남양주·의정부·구리·포천·성남 최신 작업후기</h3>
        <p style="color:var(--muted);margin:0 0 18px;">경기 동북부와 성남에서 최근 진행한 폐업폐기물처리·쓰레기집청소·생활폐기물처리·이사폐기물처리·빈집정리 후기입니다. 작업 전·후 사진과 처리 품목, 진행 과정을 확인할 수 있습니다.</p>
        <div class="review-grid">
{cards}
        </div>
      </div>
      {MARKER_END}"""
    if MARKER_START in html:
        html = re.sub(re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END), lambda _: section, html, count=1, flags=re.S)
    else:
        anchor = "      <!-- keyword-reviews:start -->"
        if anchor not in html:
            raise SystemExit("reviews/index.html 삽입 위치를 찾지 못했습니다.")
        html = html.replace(anchor, "      " + section + "\n\n" + anchor, 1)
    path.write_text(html, encoding="utf-8")


def update_region_page(root: Path, region: dict) -> None:
    path = root / region["page"].lstrip("/")
    html = path.read_text(encoding="utf-8")
    kinds = list(region["reviews"])
    review_at = html.find('id="review"')
    if review_at < 0:
        raise SystemExit(f"후기 영역을 찾지 못했습니다: {path}")
    head, tail = html[:review_at], html[review_at:]
    if f'/reviews/{region["slug"]}-{kinds[0]}/" class="review-link"' not in tail:
        new_cards = "\n".join(card(region, k, "      ") for k in kinds)
        promo = re.compile(r'    <div class="review-promo">\s*<p>.*?</p>\s*<div class="review-promo-buttons">.*?</div>\s*</div>', re.S)
        if promo.search(tail):
            base = (
                '      <article class="review-card">\n'
                f'        <span class="review-tag">{region["existing_tag"]}</span>\n'
                f'        <h3>{region["existing_title"]}</h3>\n'
                f'        <p>{region["short"]}에서 진행한 {region["existing_tag"]} 작업후기입니다.</p>\n'
                f'        <a href="/reviews/{region["slug"]}/" class="review-link">자세히 보기 →</a>\n'
                '      </article>'
            )
            block = (
                f'    <div class="review-grid">\n{new_cards}\n{base}\n    </div>\n'
                '    <div class="review-more">\n      <a href="/reviews/" class="btn secondary">전체 작업후기</a>\n    </div>'
            )
            tail = promo.sub(lambda _: block, tail, count=1)
        elif '<div class="review-grid">\n' in tail:
            tail = tail.replace('<div class="review-grid">\n', '<div class="review-grid">\n' + new_cards + "\n", 1)
        else:
            raise SystemExit(f"후기 카드 영역을 찾지 못했습니다: {path}")
    html = head + tail

    footer_at = html.find("<footer")
    footer = html[footer_at:]
    base_link = f'<a href="/reviews/{region["slug"]}/">{region["short"]} 작업후기</a>'
    extra = "".join(
        f'\n        <a href="/reviews/{region["slug"]}-{k}/">{region["name"]} {keyword_meta(k)[1]} 후기</a>'
        for k in kinds
        if f'/reviews/{region["slug"]}-{k}/' not in footer
    )
    if extra and base_link in footer:
        footer = footer.replace(base_link, base_link + extra, 1)
    path.write_text(html[:footer_at] + footer, encoding="utf-8")


def patch_existing_review(root: Path, region: dict) -> None:
    path = root / "reviews" / region["slug"] / "index.html"
    html = path.read_text(encoding="utf-8")
    kinds = list(region["reviews"])
    if f'/reviews/{region["slug"]}-{kinds[0]}/' in html:
        return
    cards = "\n".join(
        f"""        <a href="/reviews/{region["slug"]}-{k}/" class="related-card">
          <h3>{region["reviews"][k]["title"]}</h3>
          <p>{region["reviews"][k]["summary"]}</p>
          <span>{keyword_meta(k)[1]} 후기 →</span>
        </a>"""
        for k in kinds
    )
    insert = f"""
  <section class="related-section">
    <div class="wrap">
      <div class="title">
        <span>{region["name"]} 최신 후기</span>
        <h2>{" · ".join(keyword_meta(k)[1] for k in kinds)}</h2>
      </div>
      <div class="related-grid">
{cards}
      </div>
    </div>
  </section>
"""
    anchor = '  <section class="related-section">\n    <div class="wrap">\n      <div class="title">\n        <span>올바른 관련 서비스</span>'
    if anchor not in html:
        raise SystemExit(f"기존 후기 삽입 위치를 찾지 못했습니다: {path}")
    path.write_text(html.replace(anchor, insert + anchor, 1), encoding="utf-8")


def main() -> None:
    root = Path(__file__).resolve().parent
    created = write_pages(root)
    update_reviews_index(root)
    for region in REGIONS:
        update_region_page(root, region)
        patch_existing_review(root, region)
    print("created:", len(created))


if __name__ == "__main__":
    main()
