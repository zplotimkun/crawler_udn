import os
import time
import schedule
import requests

from bs4 import BeautifulSoup
from lxml import etree
from dotenv import load_dotenv
from pathlib import Path
from datetime import date

import input_sql


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
hour = os.getenv("Hour")
minute = os.getenv('Min')

def test(mydb, category):
    page = 1
    today = date.today()
    print('Today is {}'.format(today))
    while True:
        data_list = []
        url = 'http://www.justlaw.com.tw/TxtSearch.php?keystr=%E6%B3%95%E9%99%A2&page={}'.format(page)
        session = requests.session()
        headers = {
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36'
        }
        html = session.get(url, headers=headers)
        print('連結狀況:{}'.format(html))
        soup = BeautifulSoup(html.text, 'lxml')

        print('page:{}'.format(page))
        print('※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※')

        article_list = soup.find_all('a', {'class':'link1'})

        if article_list == []:
            print('On last page, over the App.')
            return

        article_num = 0
        for article in article_list:
            time.sleep(1)
            article_title = article.text.strip()
            article_href = article.get('href')
            article_url = 'http://www.justlaw.com.tw/{}'.format(article_href)

            sel_sql = input_sql.select_sql(mydb, article_url)
            if article_num == 0 and (sel_sql == False or article_title == ''):
                print('Over the App.')
                return
            elif sel_sql == False or article_title == '':
                print('Over the page.')
                break

            article_num += 1
            print('Article number:{}, url:{}'.format(article_num, article_url))
            print('title:{}'.format(article_title))
            print('-----------------------------------------------------------')
            headers = {
                'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36',
                'Referer':url
            }
            article_content_soup = ''
            article_html = session.get(article_url, headers=headers)
            article_soup = BeautifulSoup(article_html.text, 'lxml')
            article_content = article_soup.find_all('div', {'class':'law_inform_cnt'})
            for content in article_content:
                article_content_soup = BeautifulSoup(content.text, 'lxml')
            if not article_content_soup:
                continue
            article_content = article_content_soup.text
            data = {
                "title":article_title,
                "url":article_url,
                "content":article_content,
                "category":category,
                'date':today.strftime('%Y-%m-%d')
            }
            if data in data_list:
                continue
            print(data)
            print('θθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθθ')
            data_list.append(data)

        # input_sql.insert_sql(mydb, data_list)
        page += 1


def main():
    mydb = input_sql.conn_sql()
    test(mydb, 'law')


if __name__ == '__main__':
    main()
