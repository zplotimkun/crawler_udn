import os
import mysql.connector

from dotenv import load_dotenv
from pathlib import Path


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

user = os.getenv("User")
password = os.getenv('Password')
host = os.getenv('Host')
port = os.getenv('Post')

def conn_sql():
    mydb = mysql.connector.connect(
        host=host,
        database="engwebdata",
        user=user,
        password=password,
        port=port,
        charset='utf8'
    )
    return mydb


def insert_sql(mydb, data_list):
    insert_sql_list = []
    for data in data_list:
        title = data['title']
        url = data['url']
        content = data['content']
        keyword = ''
        category = data['category']
        date = data['date']
        insert_sql_list.append((title, url, content, keyword, category, date))

    cursor = mydb.cursor()

    sql = """INSERT INTO chrecords(title,url,content,keyword,category,date)
            VALUES (%s,%s,%s,%s,%s,%s)"""
    try:

        cursor.executemany(sql, insert_sql_list)

        mydb.commit()
    except Exception as e:
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