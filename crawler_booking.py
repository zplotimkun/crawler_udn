import os
import time
import schedule
import requests
import dataset
import eventlet

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

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
}


def crawler_booking(city):
    all_hotal_data = []
    city_list = []
    city_list.append(city)
    for city in city_list:
        page = 1
        print(city)
        print('※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※')
        hotal_num = 0
        while True:
            hotal_list = []
            
            if city == '深圳':
                number = 588
                url = 'https://www.booking.com/searchresults.zh-tw.html?aid=318615&label=New_Chinese_Traditional_ZH-XT_24509419465-i*COLm9IRc17GLIF2oxDGAS230871981772%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap1t1%3Aneg%3Afi12954032509%3Atidsa-64416090385%3Alp1012825%3Ali%3Adec%3Adm&sid=bc12d3ccc3ac0cec13a99156c3cbbd90&tmpl=searchresults&city=-1925268&class_interval=1&dest_id=-1925268&dest_type=city&dtdisc=0&inac=0&index_postcard=0&label_click=undef&postcard=0&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&srpvid=95ff3b88426a0051&ss_all=0&ssb=empty&sshis=0&top_ufis=1&rows=25&offset={}'.format(page*25)
            if city == '台中':
                number = 213
                url = 'https://www.booking.com/searchresults.zh-tw.html?aid=318615&label=New_Chinese_Traditional_ZH-XT_24509419465-i*COLm9IRc17GLIF2oxDGAS230871981772%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap1t1%3Aneg%3Afi12954032509%3Atidsa-64416090385%3Alp1012825%3Ali%3Adec%3Adm&sid=bc12d3ccc3ac0cec13a99156c3cbbd90&tmpl=searchresults&city=-2637824&class_interval=1&dest_id=-2637824&dest_type=city&dtdisc=0&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&srpvid=0d9f41e7706800a1&ss_all=0&ssb=empty&sshis=0&top_ufis=1&rows=25&offset={}'.format(page*25)
            if city == '高雄':
                number = 396
                url = 'https://www.booking.com/searchresults.zh-tw.html?aid=318615&label=New_Chinese_Traditional_ZH-XT_24509419465-i*COLm9IRc17GLIF2oxDGAS230871981772%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap1t1%3Aneg%3Afi12954032509%3Atidsa-64416090385%3Alp1012825%3Ali%3Adec%3Adm&sid=bc12d3ccc3ac0cec13a99156c3cbbd90&tmpl=searchresults&city=-2632378&class_interval=1&dest_id=-2632378&dest_type=city&dtdisc=0&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&srpvid=1f4d45b536500271&ss_all=0&ssb=empty&sshis=0&top_ufis=1&rows=25&offset={}'.format(page*25)
            if city == '天津':
                number = 303
                url = 'https://www.booking.com/searchresults.zh-tw.html?label=gen173nr-1FCAEoggI46AdIM1gEaOcBiAEBmAEwuAEZyAEM2AEB6AEB-AELiAIBqAIDuAK9vO_wBcACAQ&sid=bc12d3ccc3ac0cec13a99156c3cbbd90&tmpl=searchresults&class_interval=1&dest_id=684&dest_type=region&dtdisc=0&inac=0&index_postcard=0&label_click=undef&postcard=0&region=684&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&srpvid=44bd25484ebd0001&ss_all=0&ssb=empty&sshis=0&top_ufis=1&rows=25&offset={}'.format(page*25)
            if city == '上海':
                url = 'https://www.booking.com/searchresults.zh-tw.html?label=gen173nr-1FCAEoggI46AdIM1gEaOcBiAEBmAEwuAEZyAEM2AEB6AEB-AELiAIBqAIDuAK9vO_wBcACAQ&sid=bc12d3ccc3ac0cec13a99156c3cbbd90&tmpl=searchresults&city=-1924465&class_interval=1&dest_id=-1924465&dest_type=city&dtdisc=0&inac=0&index_postcard=0&label_click=undef&postcard=0&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&srpvid=120124c751d00105&ss_all=0&ssb=empty&sshis=0&top_ufis=1&rows=25&offset={}'.format(page*25)
                number = 1284
            if city == '三亞':
                number = 376
                url = 'https://www.booking.com/searchresults.zh-tw.html?aid=318615&label=New_Chinese_Traditional_ZH-XT_24509419465-i*COLm9IRc17GLIF2oxDGAS230871981772%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap1t1%3Aneg%3Afi12954032509%3Atidsa-64416090385%3Alp1012825%3Ali%3Adec%3Adm&sid=bc12d3ccc3ac0cec13a99156c3cbbd90&tmpl=searchresults&city=-1924026&class_interval=1&dest_id=-1924026&dest_type=city&dtdisc=0&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&srpvid=614c4600b85d00e3&ss_all=0&ssb=empty&sshis=0&top_ufis=1&rows=25&offset={}'.format(page*25)
            if city == '南京':
                number = 362
                url = 'https://www.booking.com/searchresults.zh-tw.html?aid=318615&label=New_Chinese_Traditional_ZH-XT_24509419465-i*COLm9IRc17GLIF2oxDGAS230871981772%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap1t1%3Aneg%3Afi12954032509%3Atidsa-64416090385%3Alp1012825%3Ali%3Adec%3Adm&sid=bc12d3ccc3ac0cec13a99156c3cbbd90&tmpl=searchresults&city=-1919548&class_interval=1&dest_id=-1919548&dest_type=city&dtdisc=0&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&srpvid=163145df79b70145&ss_all=0&ssb=empty&sshis=0&top_ufis=1&rows=25&offset={}'.format(page*25)
            if city == '紐約':
                number = 1457
                url = 'https://www.booking.com/searchresults.zh-tw.html?aid=318615&label=New_Chinese_Traditional_ZH-XT_24509419465-i*COLm9IRc17GLIF2oxDGAS230871981772%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap1t1%3Aneg%3Afi12954032509%3Atidsa-64416090385%3Alp1012825%3Ali%3Adec%3Adm&sid=bc12d3ccc3ac0cec13a99156c3cbbd90&tmpl=searchresults&city=20088325&class_interval=1&dest_id=20088325&dest_type=city&dtdisc=0&group_adults=2&group_children=0&inac=0&index_postcard=0&label_click=undef&no_rooms=1&postcard=0&room1=A%2CA&sb_price_type=total&shw_aparth=1&slp_r_match=0&srpvid=88f24616e2920054&ss_all=0&ssb=empty&sshis=0&top_ufis=1&rows=25&offset={}'.format(page*25)
            # session = get_tor_session()
            session = requests.session()
            

            html = session.get(url, headers=headers)
            print('第{}頁'.format(page))
            soup = BeautifulSoup(html.text, 'lxml')
            hotal_list = soup.find_all('a', {'class':'hotel_name_link url'})
            if hotal_list == [] or len(hotal_list) == 1:
                return all_hotal_data
            
            for hotal in hotal_list:
                
                hotal_name = hotal.span.text.strip()
                hotal_href = hotal.get('href').strip()
                hotal_url = 'https://www.booking.com{}'.format(hotal_href).replace("\n", "")
                hotal_data = {
                    'name' : hotal_name,
                    'url' : hotal_url
                }
                if hotal_data in all_hotal_data or hotal_num > number:
                    return all_hotal_data
                else:
                    print('Hotal number:{}, url:{}'.format(hotal_num, hotal_data['url']))
                    print('Title:{}'.format(hotal_data['name']))
                    print('-----------------------------------------------------------')
                    all_hotal_data.append(hotal_data)
                    hotal_num += 1
            page += 1
    

def hotal_info(mydb, category):
    city_list = ['上海', '三亞', '南京', '紐約']
    today = date.today()
    print('Today is {}'.format(today))
    
    session = requests.session()
    for city in city_list:
        all_hotal_data = crawler_booking(city)

        data_list = []
        for hotal_data in all_hotal_data:
            
            time.sleep(1)
            eventlet.monkey_patch()
            with eventlet.Timeout(60,False):
                headers = {
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
                }
                
                hotal_html = session.get(hotal_data['url'], headers=headers)
                hotal_soup = BeautifulSoup(hotal_html.text, 'lxml')

                hotal_content_list = hotal_soup.find_all("div", {"class": "hp_desc_main_content"})
                text_list = []
                for content_text in hotal_content_list:
                    text_list.append(content_text.text.strip())

                    hotal_content = ''.join(text_list)
                    data = {
                        "title":hotal_data['name'],
                        "url":hotal_data['url'],
                        "content":hotal_content,
                        "keyword":city,
                        "category":category,
                        'date':today.strftime('%Y-%m-%d')
                    }
                    if data in data_list:
                        continue
                    data_list.append(data)
                print('目前總筆數:{}'.format(len(data_list)))
        input_sql.insert_sql(mydb, data_list)




def main():
    mydb = input_sql.conn_sql()
    hotal_info(mydb, 'hotel')


if __name__ == "__main__":
    main()