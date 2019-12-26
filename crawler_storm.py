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


def crawler_storm(mydb, category):
    page = 1
    today = date.today()
    while True:
        data_list = []
        url = 'https://www.storm.mg/authors/126954/%E9%A2%A8%E4%BA%91%E8%BB%8D%E4%BA%8B/{}'.format(page)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')

        print('page:{}'.format(page))
        print('※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※')

        article_list = soup.find_all('a', {'class':'card_link link_title'})
        if article_list == []:
            print('On last page, over the App.')
            return

        article_num = 0
        for article in article_list:
            article_title = article.text.strip()
            article_href = article.get('href')
            article_url = 'https://www.storm.mg{}'.format(article_href)
            sel_sql = input_sql.select_sql(mydb, article_url)
            print(article_title)
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
            article_html = requests.get(article_url)
            article_soup = BeautifulSoup(article_html.text, 'lxml')
            article_content_list = article_soup.find_all('div', {'id': 'CMS_wrapper'})
            text_list = []
            for content_text in article_content_list:
                all_text = BeautifulSoup(content_text.text, 'lxml').find_all('p')
                for text_p in all_text:
                    text_list.append(text_p.text)
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
    crawler_storm(mydb, 'military')


if __name__ == '__main__':
    print('crawler_storm START')
    schedule.every().day.at("{}:{}".format(hour, minute)).do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
    # main()
