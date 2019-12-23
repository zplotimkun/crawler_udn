import requests

from bs4 import BeautifulSoup
from lxml import etree

import input_sql


def crawler_m01(mydb, category):
    page = 1
    article_num = 0
    while True:
        data_list = []
        url = 'https://www.mobile01.com/articles.php?c=18&p={}'.format(page)
        session = requests.session()
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.79 Chrome/79.0.3945.79 Safari/537.36'
        }
        html = session.get(url, headers=headers)
        soup = BeautifulSoup(html.text, 'lxml')
        print('第{}頁'.format(page))
        print('※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※')
        article_list = soup.find_all("a", {"class": "c-articleCard"})
        for article in article_list:
            article_title = article.find_all("div", {"class": "l-articleCardDesc"})[0].text.strip()
            article_href = article.get('href')
            article_url = 'https://www.mobile01.com/{}'.format(article_href)
            sel_sql = input_sql.select_sql(mydb, article_url)
            if sel_sql == False or article_title == '':
                print('已到重複文章，結束此段程式')
                return

            article_num += 1
            print('第{}篇文章, url:{}'.format(article_num, article_url))
            print('文章標題:{}'.format(article_title))
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
                "category":category
            }
            data_list.append(data)
        input_sql.insert_sql(mydb, data_list)
        page += 1


def main():
    mydb = input_sql.conn_sql()
    crawler_m01(mydb, 'travel')


if __name__ == '__main__':
    main()