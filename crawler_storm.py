import time
import schedule
import requests

from bs4 import BeautifulSoup
from lxml import etree
from datetime import date

import input_sql


def crawler_storm(mydb, category):
    page = 1
    today = date.today()
    while True:
        data_list = []
        url = 'https://www.storm.mg/authors/126954/%E9%A2%A8%E4%BA%91%E8%BB%8D%E4%BA%8B/{}'.format(page)
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')

        print('第{}頁'.format(page))
        print('※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※')

        article_list = soup.find_all('a', {'class':'card_link link_title'})
        if article_list == []:
            print('已到達最終頁數')
            return

        article_num = 0
        for article in article_list:
            article_title = article.text.strip()
            article_href = article.get('href')
            article_url = 'https://www.storm.mg{}'.format(article_href)
            sel_sql = input_sql.select_sql(mydb, article_url)
            print(article_title)
            if article_num == 0 and (sel_sql == False or article_title == ''):
                print('已到重複文章，結束此程式')
                return
            elif sel_sql == False or article_title == '':
                print('已到重複文章，結束此頁')
                break
            article_num += 1
            print('第{}篇文章, url:{}'.format(article_num, article_url))
            print('文章標題:{}'.format(article_title))
            print('-----------------------------------------------------------')
            article_html = requests.get(article_url)
            article_soup = BeautifulSoup(article_html.text)
            article_content_list = article_soup.find_all('p')
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
    crawler_storm(mydb, 'military')


if __name__ == '__main__':
    schedule.every().day.at("09:00").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
    # main()
