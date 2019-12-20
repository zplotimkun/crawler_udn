import requests

from bs4 import BeautifulSoup
from lxml import etree

import input_sql


def crawler_ltn(mydb, category):
    page = 1
    article_num = 0
    while True:
        data_list = []
        url = 'https://playing.ltn.com.tw/list/travel/{}'.format(page)

        print('第{}頁'.format(page))

        
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        article_list = soup.find_all("a", {"class": "tit"})
        
        for article in article_list:
            article_title = article.text.strip()
            article_href = article.get('href')
            article_url = 'https:{}'.format(article_href)
            sel_sql = input_sql.select_sql(mydb, article_url)
            if sel_sql == False:
                return
            article_num += 1
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
                "category":category
            }

            data_list.append(data)
            print('第{}篇文章, url:{}'.format(article_num, article_url))
            print('-----------------------------------------------------------')
        input_sql.insert_sql(mydb, data_list)
        page += 1






def main():
    mydb = input_sql.conn_sql()
    crawler_ltn(mydb, 'travel')


if __name__ == '__main__':
    main()