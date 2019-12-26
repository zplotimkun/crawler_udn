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

def crawler_m01(mydb, category):
    page = 1
    today = date.today()
    while True:
        data_list = []
        url = 'https://www.mobile01.com/articles.php?c=18&p={}'.format(page)
        session = requests.session()
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36'
        }
        html = session.get(url, headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')
        print('page:{}'.format(page))
        print('※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※')
        article_list = soup.find_all("a", {"class": "c-articleCard"})
        if article_list == []:
            print('On last page, over the App.')
            return

        article_num = 0
        for article in article_list:
            article_title = article.find_all("div", {"class": "l-articleCardDesc"})[0].text.strip()
            article_href = article.get('href')
            article_url = 'https://www.mobile01.com/{}'.format(article_href)
            sel_sql = input_sql.select_sql(mydb, article_url)
            if article_num == 0 and (sel_sql == False or article_title == ''):
                print('Over the App.')
                return
            elif sel_sql == False or article_title == '':
                print('Over the page.')
                break

            article_num += 1
            print('Article number:{}, url:{}'.format(article_num, article_url))
            print('Title:{}'.format(article_title))
            print('-----------------------------------------------------------')
            article_html = session.get(article_url, headers=headers)
            article_soup = BeautifulSoup(article_html.text, 'lxml')

            article_content_list = article_soup.find_all("div", {"itemprop": "articleBody"})
            text_list = []
            for content_text in article_content_list:
                text_list.append(content_text.text)

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


def main():
    mydb = input_sql.conn_sql()
    crawler_m01(mydb, 'travel')


if __name__ == '__main__':
    print('crawler_mobile01 START')
    schedule.every().day.at("{}:{}".format(hour, minute)).do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
    # main()
