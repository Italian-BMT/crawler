# request api
import requests
import json
from datetime import datetime

with open('subway.json', 'r', encoding='utf-8') as f:
    # Load the contents of the file as a Python object
    data = json.load(f)

auth_key = '4a47556a54726c6138334578595a50'

line_1 = []
line_2 = []
line_3 = []
line_4 = []
line_5 = []
line_6 = []
line_7 = []
line_8 = []
line_9 = []
line_bundang = []
line_gyeongui = []
line_airport = []
line_sinbundang = []
line_wui = []
line_gyeongchun = []


for i in data['DATA']:
    if i['line_num'] == '01호선':
        line_1.append((i['station_cd'], i['station_nm']))
    elif i['line_num'] == '02호선':
        line_2.append((i['station_cd'], i['station_nm']))
    elif i['line_num'] == '03호선':
        line_3.append((i['station_cd'], i['station_nm']))
    elif i['line_num'] == '04호선':
        line_4.append((i['station_cd'], i['station_nm']))
    elif i['line_num'] == '05호선':
        line_5.append((i['station_cd'], i['station_nm']))
    elif i['line_num'] == '06호선':
        line_6.append((i['station_cd'], i['station_nm']))
    elif i['line_num'] == '07호선':
        line_7.append((i['station_cd'], i['station_nm']))
    elif i['line_num'] == '08호선':
        line_8.append((i['station_cd'], i['station_nm']))
    elif i['line_num'] == '09호선':
        line_9.append((i['station_cd'], i['station_nm']))
    elif i['line_num'] == '수인분당선':
        line_bundang.append((i['station_cd'], i['station_nm']))
    elif i['line_num'] == '경의선':
        line_gyeongui.append((i['station_cd'], i['station_nm']))
    elif i['line_num'] == '공항철도':
        line_airport.append((i['station_cd'], i['station_nm']))
    elif i['line_num'] == '신분당선':
        line_sinbundang.append((i['station_cd'], i['station_nm']))
    elif i['line_num'] == '경춘선':
        line_gyeongchun.append((i['station_cd'], i['station_nm']))
    elif i['line_num'] == '우이신설경전철':
        line_wui.append((i['station_cd'], i['station_nm']))

# sort line_* by station_cd
line_1.sort(key=lambda x: x[0])
line_2.sort(key=lambda x: x[0])
line_3.sort(key=lambda x: x[0])
line_4.sort(key=lambda x: x[0])
line_5.sort(key=lambda x: x[0])
line_6.sort(key=lambda x: x[0])
line_7.sort(key=lambda x: x[0])
line_8.sort(key=lambda x: x[0])
line_9.sort(key=lambda x: x[0])
line_bundang.sort(key=lambda x: x[0])
line_gyeongui.sort(key=lambda x: x[0])
line_airport.sort(key=lambda x: x[0])
line_sinbundang.sort(key=lambda x: x[0])
line_gyeongchun.sort(key=lambda x: x[0])
line_wui.sort(key=lambda x: x[0])

lines_1_9 = [line_1, line_2, line_3, line_4, line_5, line_6, line_7, line_8, line_9]

# get data from api
for i in range(1,10):
    for (station_cd, station_nm) in lines_1_9[i-1]:
        new_data = []
        # get data from api
        for j in range(1,3+1):
            for k in range(1,2+1):
                # code : 역 코드, day_id : 요일(1:평일,2:토요일,3:공휴일), inout_tag : 상행(1)/하행(2)
                url = "http://openAPI.seoul.go.kr:8088/{key}/json/SearchSTNTimeTableByIDService/1/500/{code}/{day_id}/{inout_tag}/".format(
                    key=auth_key, code=station_cd, day_id=j, inout_tag=k)

                response = requests.get(url)

                if response.status_code == 200:
                    # str to json
                    jsons = json.loads(response.text)
                    #print(station_nm)
                    
                    # 역코드가 있음에도 api가 작동하지 않으면 continue
                    if "SearchSTNTimeTableByIDService" not in jsons:    
                        print("No data")
                        continue

                    data = jsons["SearchSTNTimeTableByIDService"]["row"]

                    # list append LINE_NUM, STATION_NM, STATION_CD, WEEK_TAG, INOUT_TAG, ARRIVETIME in data
                    for l in data:
                        subway = {}
                        subway['line_num'] = l['LINE_NUM']
                        subway['week_tag'] = l['WEEK_TAG']
                        subway['inout_tag'] = l['INOUT_TAG']
                        subway['station_nm'] = l['STATION_NM']
                        subway['arrive_time'] = l['ARRIVETIME']
                        
                        if subway not in new_data:
                            new_data.append(subway) 

                else:
                    print(f'The request failed with status code {response.status_code}.')
        now = datetime.now().strftime('%Y_%m_%d')
        with open(f'{now}_timetable_{i}.json', 'a', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
        print(f'{i}호선',lines_1_9[i-1].index((station_cd, station_nm)), station_nm, "done")
    
