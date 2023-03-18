import requests
from bs4 import BeautifulSoup
import json

# 네이버 지도에서 역 이름과 역 코드 알아내는 함수 작성
# 이 친구는 한 달이나 일주일에 한 번씩 정도만 돌리면 되지 않을까?
def find_code():
    INFO = {}

    for naver_code in range(100, 20000):
        base_query = "https://pts.map.naver.com/end-subway/ends/web/{naver_code}/home".format(naver_code=naver_code)
        page = requests.get(base_query)
        soup = BeautifulSoup(page.text, "html.parser")
        try:
            line_num = soup.select_one('body > div.app > div > div > div > div.place_info_box > div > div.p19g2ytg > div > button > strong.line_no').get_text()
            station_nm = soup.select_one('body > div.app > div > div > div > div.place_info_box > div > div.p19g2ytg > div > button > strong.place_name').get_text()
        except:
            continue

    # 호선 자체가 새로 생기는 경우가 있을 것 같아 호선을 미리 정의하지 않고, 크롤링 결과에 의해 정의되게 함
        if line_num not in INFO:
            INFO[line_num] = []

        block = {"station_nm": station_nm, "naver_code": naver_code}
        INFO[line_num].append(block)


    return INFO


if __name__ == "__main__":
    with open('subway_information.json', 'w', encoding='utf-8') as f:
        json.dump(find_code(), f, ensure_ascii=False, indent=4)
