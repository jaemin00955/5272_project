from db_query import insert_ulsan
import time 


def insert():
    # 재귀함수로 계측기 멈췄을 때 다시 실행하도록..
    try:
        insert_ulsan()
        insert()
    except:
        time.sleep(3000)
        print("***********ReStart************")
        insert()
        

if __name__ == '__main__':
    insert()