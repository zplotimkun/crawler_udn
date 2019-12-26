import os
import time
import json
import requests
import schedule

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path
from datetime import date

import input_sql

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
hour = os.getenv("Hour")
minute = os.getenv('Min')

def crawler_lehman(mydb, category):
    page = 1
    today = date.today()
    while True:
        data_list = []
        url = 'http://123.57.143.90/art/articleHomeShows.htm'
        session = requests.Session()
        headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36'
        }
        post_data = {
            'pageSize':'15',
            'curPage':'{}'.format(page)
        }
        data = session.post(url, data=post_data, headers=headers)
        data_json = json.loads(data.text)
        article_list = data_json['rows']
        print('第{}頁'.format(page))
        print('※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※')

        if article_list == []:
            print('已到達最終頁數')
            return

        article_num = 0
        for article in article_list:
            article_href = article['id']
            article_url = 'http://123.57.143.90/art/show.htm?id={}'.format(article_href)
            article_title = article['name']
            sel_sql = input_sql.select_sql(mydb, article_url)
            if article_num == 0 and (sel_sql == False or article_title.strip() == ''):
                print('已到重複文章，結束此程式')
                return
            elif sel_sql == False or article_title == '':
                print('已到重複文章，結束此頁')
                break
            article_num += 1
            print('第{}篇文章, url:{}'.format(article_num, article_url))
            print('文章標題:{}'.format(article_title))
            print('-----------------------------------------------------------')
            article_html = session.get(article_url, headers=headers)
            article_soup = BeautifulSoup(article_html.text, 'lxml')
            article_content_list = article_soup.find_all("p")
            text_list = []
            for content_text in article_content_list:
                if content_text.text.strip() == '' or '雷曼军事网' in content_text.text:
                    continue
                text_list.append(content_text.text.strip())

            article_content = ''.join(text_list)
            data = {
                "title":article_title,
                "url":article_url,
                "content":article_content,
                "category":category,
                'date':today.strftime('%Y-%m-%d')
            }
            if data in data_list:
                continue
            data_list.append(data)
        input_sql.insert_sql(mydb, data_list)
        page += 1
        time.sleep(5)


def main():
    mydb = input_sql.conn_sql()
    crawler_lehman(mydb, 'military')


if __name__ == '__main__':
    try:
        print('crawler_lehman 程式啟動')
        schedule.every().day.at("{}:{}".format(hour, minute)).do(main)
        while True:
            schedule.run_pending()
            time.sleep(1)
        # main()
    except Exception as e:
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        print(e)
        print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')