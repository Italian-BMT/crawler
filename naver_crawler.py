import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import json

from datetime import datetime

# 라인, 역이름, 네이버코드 불러오기
with open('subway_information.json', 'r', encoding='utf-8') as f:
    # Load the contents of the file as a Python object
    data = json.load(f)


def crawler(target_line, station_nm, driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # week_tag 알아내기 (평일, 토요일, 공휴일&일요일)
    day = soup.find(attrs={"aria-selected" : "true"}).get_text()
    if day == '평일':
        week_tag = 1
    elif day == '토요일':
        week_tag = 2
    elif day == '공휴일':
        week_tag = 3

    trs = soup.select('.table_schedule > tbody > tr')

    for i in range(0, len(trs)):
        tds = trs[i].select('td')
        for j in range(len(tds)):
            # 도착 시간 구하기
            times = tds[j].select_one('.inner_timeline > .wrap_time > .time')
            # # 시작역, 종착역 구하기
            # locations = tds[j].select_one('.inner_timeline > .wrap_station > em.station')
            if times != None:
                # print(times.text, locations.text)
                arrive_time = times.text + ":00"
                data = {
                    "line_num": target_line,
                    "week_tag": str(week_tag),
                    "inout_tag": str(j+1),  # 1 : 상행, 2 : 하행
                    "station_nm": station_nm,
                    "arrive_time": arrive_time
                }
                # 중복 확인
                if data not in info :
                    info.append(data)
                    data = {}


# 크롤링을 위한 설정 준비
service = Service('/Users/gyum/Downloads/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument('headless')    # chrome 창 안 띄우고 실행
base_url = 'https://pts.map.naver.com/end-subway/ends/web/{naver_code}/home'


# 크롤링할 호선 정리하기
target_lines = data.keys() - ["1호선", "2호선", "3호선", "4호선", "5호선", "6호선", "7호선", "8호선", "9호선"]
print("target_lines: ",target_lines)

# 각 역별 시간표 저장해줄 info 리스트 생성
info = []
# 파일 이름에 사용할 날짜 문자 생성
now = datetime.now().strftime('%Y_%m_%d')

# 각 호선 -> 각 역 별로 for loop 돌며 크롤링
for target_line in target_lines:
    # print(target_line, "입력 시작")
    for tmp in data[target_line]:
        station_nm = tmp['station_nm']
        naver_code = tmp['naver_code']
        # print("station_nm: ", station_nm, "naver_code: ", naver_code)
        # 크롤링할 역 검색
        url = base_url.format(naver_code=naver_code)
        driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(4)

        # naver map 검색 결과로 들어가기
        driver.get(url)
        # '전체 시간표' 부분 클릭
        driver.find_element(By.CSS_SELECTOR, 'body > div.app > div > div > div > div.end_section.station_info_section > div.at_end.sofzqce > div.collapse_group_wrap.contents_collapse > div:nth-child(1)').click()

        # 전체 시간표 부분 접속 완료 후 크롤링 시작
        crawler(target_line, station_nm, driver)

    # open을 w로 할지 a로 할지 / a로 하면 기존 데이터와 새로 쓰이는 데이터가 [][] 이런 식으로 묶이는데
    # 차라리 파일을 생성 -> s3로 데이터 전송하고 -> 덮어씌우기 이런 방식으로 진행? 아 날짜를 입력하면 되는구나

    with open(f'{now}_timetable_{target_line}.json', 'w', encoding='utf-8') as f:
        json.dump(info, f, ensure_ascii=False, indent=4)
    # print(target_line, "입력 완료")
    


