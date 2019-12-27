import os
import mysql.connector

from dotenv import load_dotenv
from pathlib import Path


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

user = os.getenv("User")
password = os.getenv('Password')

def conn_sql():
    mydb = mysql.connector.connect(
        host="alpha.ponddy-one.com",
        database="engwebdata",
        user=user,
        password=password,
        port=3306,
        charset='utf8'
    )
    return mydb


def insert_sql(mydb, data_list):
    for data in data_list:

        cursor = mydb.cursor()

        sql = """INSERT INTO chrecords(title,url,content,keyword,category,date)
            VALUES (%s,%s,%s,%s,%s,%s)"""
        try:

            cursor.execute(sql, (data['title'],data['url'],data['content'],'',data['category'],data['date']))

            mydb.commit()
        except Exception as e:

            print('Add data error, url：{}'.format(data['url']))
            print(data)
            print(e)
            print('------------------------------------------------------')
            mydb.rollback()

def select_sql(mydb, url):
    cursor = mydb.cursor()
    
    sql = """SELECT * FROM chrecords WHERE url='{}'""".format(url)
    cursor.execute(sql)
    test = cursor.fetchall()
    if test == []:
        return True
    else:
        return False