import db_conn # db_conn.py 불러오기
import pymysql
from datetime import datetime, timedelta
import pandas as pd

def box_plot_chung(device_id,start,end):  # 시작과 끝 날짜, 원하는 계측기이름을 정해주면 해당 lat,long,heigth,create_time을 가져오는 sql 함수 
    conn = db_conn.get_connection()
    sql ='SELECT Latitude/100,Longitude/100,Height,Create_time FROM rawdata_chung WHERE (device_id=%s) AND (Create_time BETWEEN %s AND %s);'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    values = ('b\''+device_id+'$GNGGA',start,end)
    cursor.execute(sql,values)
    rows = cursor.fetchall()
    conn.close()
    return rows 
def box_plot_ulsan(device_id,start,end):  # 시작과 끝 날짜, 원하는 계측기이름을 정해주면 해당 lat,long,heigth,create_time을 가져오는 sql 함수 
    conn = db_conn.get_connection()
    sql ='SELECT Latitude/100,Longitude/100,Height,Create_time FROM rawdata_ulsan WHERE (device_id=%s) AND (Create_time BETWEEN %s AND %s);'
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    values = (device_id,start,end)
    cursor.execute(sql,values)
    rows = cursor.fetchall()
    conn.close()
    return rows 

def each_plot(df,which,box_num):  # lat,long,heigth 각각의 정해진 기간(box_num)만큼의 통계량 데이터를 뽑는 함수
    box = []
    for i in range(0,box_num):
        data = {'x':0,'low':0,'high':0,'q1':0,'median':0,'q3':0}
        # t_date = datetime.today().date()
        t_date = datetime(2021,4,28).date()
        t_date_minus = t_date - timedelta(days=i)
        data['x'] = str(t_date_minus)
        data['low'] = df.loc[str(t_date_minus)][which].describe()['min']
        data['high'] = df.loc[str(t_date_minus)][which].describe()['max']
        data['q1'] = df.loc[str(t_date_minus)][which].describe()['25%']
        data['median'] = df.loc[str(t_date_minus)][which].describe()['50%']
        data['q3'] = df.loc[str(t_date_minus)][which].describe()['75%']
        box.append(data)
    return box

def plot(device_id,box_num):
    lat = []
    long = []
    height = []
    time = []
    # today = datetime.today()
    today = datetime(2021,4,29).date()
    today_minus = today - timedelta(days=5)
    if device_id =='syntest1':
        data_all = box_plot_chung(device_id,today_minus,today)
    else:
        data_all = box_plot_ulsan(device_id,today_minus,today)

    for data in data_all:
        lat.append(data['Latitude/100'])
        long.append(data['Longitude/100'])
        height.append(data['Height'])
        time.append(data['Create_time'])

    df = pd.DataFrame(data={'lat':lat,'long':long,'height':height},index=time)  
    box_lat = each_plot(df,'lat',box_num)
    box_long = each_plot(df,'long',box_num)
    box_height = each_plot(df,'height',box_num)

    plot_data = {
        'boxplot_data':[
        {
            "value": 'lat',
            "interval":2,
            "box_num" : 7,
            "data" : box_lat
        },
        {
            "value": 'long',
            "interval":2,
            "box_num" : 7,
            "data" : box_long
        },
        {
            "value": 'height',
            "interval":2,
            "box_num" : 7,
            "data" : box_height
        }
        ]
    }
    return plot_data
