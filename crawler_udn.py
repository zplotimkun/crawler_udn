import requests

from bs4 import BeautifulSoup
from lxml import etree

import input_sql

def crawler_udn(mydb, category):
    crawler_page = 1
    news_total = 0
    while True:
        print('類別：{},第{}頁'.format(category, crawler_page))

        data_list = []
        if category == 'constellation':
            url = 'https://udn.com/news/get_article/{}/2/6649/7268?_=1575266787923'.format(crawler_page)
        elif category == 'military':
            url = 'https://udn.com/news/get_article/{}/2/6638/10930?_=1575956277623'.format(crawler_page)
        else:
            break

        crawler_page += 1
        html = requests.get(url)
        html_et = etree.HTML(html.text)
        for news_list_num in range(1, 21):
            try:
                article = html_et.xpath('/html/body/dt[{}]/a[2]'.format(news_list_num))
                article_title = html_et.xpath('/html/body/dt[{}]/a[2]/h2/text()'.format(news_list_num))
            except Exception as e:
                print(e)
                return
            if article == []:
                continue
            for news in article:
                news_url = 'http://udn.com{}'.format(news.attrib['href'])
                sel_sql = input_sql.select_sql(mydb, news_url)
                if sel_sql == False or article_title == '':
                    continue
                news_total += 1
                print('第{}則新聞 url:{}'.format(news_total, news_url))
                print('--------------------------------------------------------')

                news_html = requests.get(news_url)
                new_soup = BeautifulSoup(news_html.text, 'lxml')
                new_content = new_soup.findAll('p')
                content_select = []
                for content in new_content:
                    content_select.append(content.text)
                content = ''.join(content_select)

                data = {
                    'title':article_title[0],
                    'url':news_url,
                    'content':content,
                    'category':category
                }
                if data in data_list:
                    continue
                print('----------------------------------------------------------------------------')
                data_list.append(data)
        input_sql.insert_sql(mydb, data_list)

def crawler_udn_opinion(mydb, category):
    data_list = []
    crawler_page = 1
    news_total = 0
    while True:
        print('類別：{},第{}頁'.format(category, crawler_page))

        if category == 'military':
            url = 'https://opinion.udn.com/opinion/ajax_articletag/%E8%BB%8D%E4%BA%8B%E8%A9%95%E8%AB%96/{}?_=1576737799589'.format(crawler_page)
        elif category == 'travel':
            url = 'https://udn.com/rank/ajax_newest/1013/0/{}?_=1576829807430'.format(crawler_page)
        else:
            break
        crawler_page += 1
        html = requests.get(url)
        soup = BeautifulSoup(html.text, 'lxml')
        article_list = soup.find_all('h2')
        for article in article_list:
            article_title = article.a.text
            if category == 'military':
                article_url = 'https://opinion.udn.com{}'.format(article.a.get('href'))
            elif category == 'travel':
                article_url = article.a.get('href')
            sel_sql = input_sql.select_sql(mydb, article_url)
            if sel_sql == False or article_title == '':
                print('已到重複文章，結束此段程式')
                return
            news_total += 1
            print('第{}則新聞 url:{}'.format(news_total, article_url))
            print('--------------------------------------------------------')
            article_html = requests.get(article_url)
            article_soup = BeautifulSoup(article_html.text, 'lxml')
            content_text_list = article_soup.find_all('p')
            text_list = []
            for content_text in content_text_list:
                text_list.append(content_text.text)
            dict_content = ''
            content = dict_content.join(text_list)
            data = {
                    'title':article_title,
                    'url':article_url,
                    'content':content,
                    'category':category
                }
            if data in data_list:
                continue
            data_list.append(data)
        input_sql.insert_sql(mydb, data_list)


def main():
    mydb = input_sql.conn_sql()
    crawler_udn(mydb, 'constellation')
    crawler_udn(mydb, 'military')
    crawler_udn_opinion(mydb, 'military')
    crawler_udn_opinion(mydb, 'travel')
    # print(data_list)



if __name__ == "__main__":
    main()

