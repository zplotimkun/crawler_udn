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
        host="192.168.1.100",
        database="engwebdata",
        user=user,
        password=password,
        port=3306,
        charset='utf8'
    )
    return mydb


def insert_sql(mydb, data_list):
    for data in data_list:

        # 使用cursor()方法获取操作游标 
        cursor = mydb.cursor()

        # SQL 插入语句
        sql = """INSERT INTO chrecords(title,url,content,keyword,category)
            VALUES ('{}','{}','{}','{}','{}')""".format(data['title'],data['url'],data['content'],'',data['category'])
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            mydb.commit()
        except:
            # Rollback in case there is any error
            print('新增資料失敗')
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

conn_sql()