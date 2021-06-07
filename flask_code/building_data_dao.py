import db_conn 
import pymysql
from time import time

# 모든 사용자의 총 건축물 개수
def get_all_building():
    conn = db_conn.get_connection()
    sql = 'select count(distinct(building_name)) from building'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows
    
# 모든 사용자의 건축물 정보 // 건축물 이름, 종류, 건축물 주소, 계측기 개수, 이상 여부
def get_all_building_info():
    conn = db_conn.get_connection()
    sql_b = 'select building.id, building_name,building_type_name,building_address from building order by building.id'
    sql_d = 'select count(*) from device where building_name=%s'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql_b)
    building_info = cursor.fetchall()
    for info in building_info:
        cursor.execute(sql_d,info['building_name'])
        device_num = cursor.fetchone()
        info['device_num'] = device_num['count(*)']
    conn.close()
    return building_info

# 로그인 후 나의 건축물의 수 //예외처리 필요??
def get_user_building(login_user_id):
    conn = db_conn.get_connection()
    sql ='SELECT count(distinct(building.building_type_name)) FROM building LEFT JOIN user ON building.building_user_id = %s'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql,login_user_id)
    counts = cursor.fetchall()
    conn.close()
    return counts

# 로그인한 사용자 ID를 building, device 테이블과 join 시켜서 종류 및 개수 select
# 플라스크 라우팅 할 때 building_name 파라미터를 불러올수가 없어서, login_user_id파라미터만 필요하도록 만들어주세요!
def get_user_building_info(login_user_id):
    conn = db_conn.get_connection()
    sql_b = 'select id,building_name,building_type_name,building_address from building where building_user_id = %s order by building.id'
    sql_d = 'select count(distinct(device_id)) as device_num from device LEFT JOIN building ON device.building_name=building.building_name where device.device_user_id=%s and device.building_name = %s'
    #sql_e = 'select device.device_criteria_latitude, device.device_criteria_longitude, device.device_criteria_height from device where device.device_user_id=%s and device.building_name = %s'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(sql_b, login_user_id)
    building_map = cursor.fetchall()
    for map in building_map:
        values = (login_user_id, map['building_name'])
        cursor.execute(sql_d, values)
        device_num = cursor.fetchone()
        map['device_num'] = device_num['device_num']
        # 위도, 경도, 높이를 select 하여 이상여부를 계산하기 위해서 가져오는 컬럼
        #cursor.execute(sql_e, values)
        #tttt = cursor.fetchone()
        #map['device_criteria_latitude'] = tttt['device_criteria_latitude']
        #map['device_criteria_longitude'] = tttt['device_criteria_longitude']
        #map['device_criteria_height'] = tttt['device_criteria_height']
    conn.close()
    return building_map

# # 지도 - 나의 건축물 위치에 마크 // 1)건축물 이름 2)종류 3)건축물 주소
# def get_my_building_info_map(login_user_id):
#     conn = db_conn.get_connection()
#     sql ='SELECT building.building_name, building.building_type, building_address FROM building LEFT JOIN user ON building.building_user_id=%s'
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     cursor.execute(sql,login_user_id)
#     infos = cursor.fetchall()
#     conn.close()
#     return infos

# # 표 - 그 건축물의 계측기 개수
# def get_my_building_info_table(login_user_id,building_name):
#     conn = db_conn.get_connection()
#     sql ='select count(distinct(device_id)) from device LEFT JOIN building ON device.building_name=building.building_name where device.device_user_id=%s and device.building_name = %s'
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     values = (login_user_id,building_name)
#     cursor.execute(sql,values)
#     infos = cursor.fetchall()
#     conn.close()
#     return infos

# 이상 여부
def decide_criteria(login_user_id,building_name):
    conn = db_conn.get_connection()
    sql ='select device.device_criteria_latitude, device.device_criteria_longitude, device.device_criteria_height from device where device.device_user_id=%s and device.building_name = %s'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    values = (login_user_id,building_name)
    cursor.execute(sql,values)
    infos = cursor.fetchall()
    conn.close()
    return infos