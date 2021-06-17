from urllib.parse import urlencode, unquote
import requests
import json
import pymysql
from db_conn import get_connection

import time
#날씨 API 활용

PTY = [
    {0: "없음"},
    {1: "비"},
    {2: "비/눈"},
    {3: "눈"},
    {4: "소나기"},
    {5: "빗방울"},
    {6: "빗방울/눈날림"},
    {7: "눈날림"}
]  # 강수형태 없음(0), 비(1), 비/눈(2), 눈(3), 소나기(4), 빗방울(5), 빗방울/눈날림(6), 눈날림(7) 여기서 비/눈은 비와 눈이 섞여 오는 것을 의미 (진눈개비) * 빗방울(5), 빗방울/눈날림(6), 눈날림(7)


def get_weather(deviceId: str):
    # urlDongne = " http://apis.data.go.kr/1360000/VilageFcstInfoService/getVilageFcst"
    urlDoneneDangi = "http://apis.data.go.kr/1360000/VilageFcstInfoService/getUltraSrtNcst"
    today = time.strftime('%Y%m%d', time.localtime(time.time()))
    hour = time.strftime('%H', time.localtime(time.time()))
    _hour = int(hour) - 1
    if 1 <= _hour <= 9:
        h = "0" + str(_hour) + "00"
    elif _hour == 0:
        h = str(_hour) + "000"
    else:
        h = str(_hour) + "00"

    print(h)

    location = findLocationByDeviceId(deviceId)['device_location']  # find building location
    if location == "서울특별시 중구 퇴계로36길 2":
        queryString = "?" + urlencode(
            {
                "ServiceKey": unquote(
                    "t37ep6SRC302u2Cb3j9ekd%2B3Kj6HVPsGw11OBaQjfiiOEbQ9dDW0bLWyUomfxFW3%2FHHlGlMjeGiLmE6zExc7GQ%3D%3D"),
                "base_date": today,  # 오늘날짜
                "base_time": h,  # 24시간 기준 ex, 2000
                "nx": 69,
                "ny": 127,
                "numOfRows": "10",
                "pageNo": 1,
                "dataType": "JSON"
            }
        )

        queryURL = urlDoneneDangi + queryString  # 동네예보
        response = requests.get(queryURL)
        print(response.text)
        r_dict = json.loads(response.text).get("response")
        r_body = r_dict.get("body")
        r_items = r_body.get("items")
        r_item = r_items.get("item")

        result = {}
        '''
        POP	강수확률	%
        PTY	강수형태	코드값
        R06	6시간 강수량	범주 (1 mm)
        REH	습도	%
        S06	6시간 신적설	범주(1 cm)
        SKY	하늘상태	코드값
        T3H	3시간 기온	℃
        TMN	아침 최저기온	℃
        TMX	낮 최고기온	℃
        UUU	풍속(동서성분)	m/s
        VVV	풍속(남북성분)	m/s
        WAV	파고	M
        VEC	풍향	deg
        WSD	풍속	m/s
            
        '''

        result['강수확률'] = 0  # 미리 넣어놓음

        for item in r_item:
            # print(item)
            if (item.get("category") == "UUU"):
                result['풍속(동서성분)'] = item['obsrValue']

            if (item.get("category") == "VVV"):
                result['풍속(남북성분)'] = item['obsrValue']

            if (item.get("category") == "POP"):  # 3시간 기온
                result["강수확률"] = item['obsrValue']

            if (item.get("category") == "T1H"):  # 3시간 기온
                result["기온"] = item['obsrValue']

            if (item.get("category") == "RN1"):  # 1시간 강수량
                result["강수량"] = item['obsrValue']

            if(item.get("category") == "WSD"):  # 풍속
                result["풍속"] = item['obsrValue']

            if(item.get("category") == "REH"):  # 습도
                result["습도"] = item['obsrValue']

            if (item.get("category") == "PTY"):  # 강수형태
                name = ''
                if item['obsrValue'] == '0':
                    name = "없음"
                if item['obsrValue'] == '1':
                    name = "비"
                if item['obsrValue'] == '2':
                    name = "비/눈"
                if item['obsrValue'] == '3':
                    name = "눈"
                if item['obsrValue'] == '4':
                    name = "소나기"
                if item['obsrValue'] == '5':
                    name = "빗방울"
                if item['obsrValue'] == '6':
                    name = "눈날림/눈날림"
                if item['obsrValue'] == '7':
                    name = "눈날림"
                result["강수형태"] = name
        result["위치"] = location

        if result['풍속(동서성분)'] == '0' and result['풍속(남북성분)'] != '0':
            print(result['풍속(남북성분)'])
            if float(result['풍속(남북성분)']) > 0:
                result['방향'] = "동쪽"
            if float(result['풍속(남북성분']) < 0:
                result['방향'] = "서쪽"
        elif result['풍속(동서성분)'] != '0' and result['풍속(남북성분)'] == '0':
            print(result['풍속(동서성분)'])
            if float(result['풍속(동서성분)']) > 0:
                result['방향'] = "남쪽"
            if float(result['풍속(동서성분)']) < 0:
                result['방향'] = "북쪽"
        else:
            result['방향'] = "-"


        return result

    elif location == '부산광역시 기장군 일광면 문동리':
        queryString = "?" + urlencode(
            {
                "ServiceKey": unquote(
                    "t37ep6SRC302u2Cb3j9ekd%2B3Kj6HVPsGw11OBaQjfiiOEbQ9dDW0bLWyUomfxFW3%2FHHlGlMjeGiLmE6zExc7GQ%3D%3D"),
                "base_date": today,  # 오늘날짜
                "base_time": h,  # 24시간 기준 ex, 2000
                "nx": 101,
                "ny": 78,
                "numOfRows": "10",
                "pageNo": 1,
                "dataType": "JSON"
            }
        )

        queryURL = urlDoneneDangi + queryString  # 동네예보
        response = requests.get(queryURL)
        print(response.text)
        r_dict = json.loads(response.text).get("response")
        r_body = r_dict.get("body")
        r_items = r_body.get("items")
        r_item = r_items.get("item")

        result = {}
        '''
        POP	강수확률	%
        PTY	강수형태	코드값
        R06	6시간 강수량	범주 (1 mm)
        REH	습도	%
        S06	6시간 신적설	범주(1 cm)
        SKY	하늘상태	코드값
        T3H	3시간 기온	℃
        TMN	아침 최저기온	℃
        TMX	낮 최고기온	℃
        UUU	풍속(동서성분)	m/s
        VVV	풍속(남북성분)	m/s
        WAV	파고	M
        VEC	풍향	deg
        WSD	풍속	m/s

        '''

        result['강수확률'] = 0  # 미리 넣어놓음

        for item in r_item:
            # print(item)
            if (item.get("category") == "UUU"):
                result['풍속(동서성분)'] = item['obsrValue']

            if (item.get("category") == "VVV"):
                result['풍속(남북성분)'] = item['obsrValue']

            if (item.get("category") == "POP"):  # 3시간 기온
                result["강수확률"] = item['obsrValue']

            if (item.get("category") == "T1H"):  # 3시간 기온
                result["기온"] = item['obsrValue']

            if (item.get("category") == "RN1"):  # 1시간 강수량
                result["강수량"] = item['obsrValue']

            if (item.get("category") == "WSD"):  # 풍속
                result["풍속"] = item['obsrValue']

            if (item.get("category") == "REH"):  # 습도
                result["습도"] = item['obsrValue']

            if (item.get("category") == "PTY"):  # 강수형태
                name = ''
                if item['obsrValue'] == '0':
                    name = "없음"
                if item['obsrValue'] == '1':
                    name = "비"
                if item['obsrValue'] == '2':
                    name = "비/눈"
                if item['obsrValue'] == '3':
                    name = "눈"
                if item['obsrValue'] == '4':
                    name = "소나기"
                if item['obsrValue'] == '5':
                    name = "빗방울"
                if item['obsrValue'] == '6':
                    name = "눈날림/눈날림"
                if item['obsrValue'] == '7':
                    name = "눈날림"
                result["강수형태"] = name
        result["위치"] = location

        if result['풍속(동서성분)'] == '0' and result['풍속(남북성분)'] != '0':
            print(result['풍속(남북성분)'])
            if float(result['풍속(남북성분)']) > 0:
                result['방향'] = "동쪽"
            if float(result['풍속(남북성분']) < 0:
                result['방향'] = "서쪽"
        elif result['풍속(동서성분)'] != '0' and result['풍속(남북성분)'] == '0':
            print(result['풍속(동서성분)'])
            if float(result['풍속(동서성분)']) > 0:
                result['방향'] = "남쪽"
            if float(result['풍속(동서성분)']) < 0:
                result['방향'] = "북쪽"
        else:
            result['방향'] = "-"

        return result

        # print(json.dumps(parsed, indent=4, sort_keys=True))

        # RN1 1시간 강수량
        # PTY 강수형태
        # REH 습도
        # T1H 기온
        # UUU 풍속(동서성분) m/s
        # VVV 풍속(남북성분)
        # VEC 풍향 , 단위 deg
        # WSD 풍속 m/s

def findLocationByDeviceId(device_id:str):
    conn = get_connection()
    sql = "select device_location from device where device_id=%s"
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql, device_id)
    device_location = cursor.fetchone()
    print(device_location)
    conn.close()
    return device_location


if __name__ == "__main__":


    # print(findLocationByDeviceId('syntest1'))
    print(get_weather('syntest1'))
    # hour = time.strftime('%H', time.localtime(time.time()))
    # print(hour)
    # print(hour + "00")

