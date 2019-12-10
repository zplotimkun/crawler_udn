import requests

from bs4 import BeautifulSoup
from lxml import etree

import input_sql

def crawler_udn(category):
    mydb = input_sql.conn_sql()
    
    for crawler_page in range(1,11):
        data_list = []
        if category == 'constellation':
            url = 'https://udn.com/news/get_article/{}/2/6649/7268?_=1575266787923'.format(crawler_page)
        else:
            break
        html = requests.get(url)
        html_et = etree.HTML(html.text)
        for news_list_num in range(1, 21):
            one_news = html_et.xpath('/html/body/dt[{}]/a[2]'.format(news_list_num))
            one_news_title = html_et.xpath('/html/body/dt[{}]/a[2]/h2/text()'.format(news_list_num))
            if one_news == []:
                continue
            for news in one_news:
                news_url = 'http://udn.com{}'.format(news.attrib['href'])
                sel_sql = input_sql.select_sql(mydb, news_url)
                if sel_sql == False:
                    continue
                news_html = requests.get(news_url)
                new_soup = BeautifulSoup(news_html.text, 'lxml')
                new_content = new_soup.findAll('p')
                content_select = []
                for content in new_content:
                    if len(content_select) < 5:
                        content_select.append(content.text)
                    else:
                        break
            dict_content = ''
            content = dict_content.join(content_select)

            data = {
                'title':one_news_title[0],
                'url':news_url,
                'content':content,
                'category':category
            }
            if data in data_list:
                continue

            data_list.append(data)
        input_sql.insert_sql(mydb, data_list)


def main():
    crawler_udn('constellation')
    # print(data_list)
    


if __name__ == "__main__":
    main()

