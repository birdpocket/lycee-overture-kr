# -*- coding: utf-8 -*-

import os
import urllib.request
import requests
from bs4 import BeautifulSoup
import json


def get_info(url):
    card_info = {}

    req = requests.get(url)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    contents = soup.find('div', {'id':'contents'})

    cardno = contents.findAll('tr')[0].findAll('td')[1].text.strip()
    body = contents.findAll('tr')[3].find('td')
    body.find('a').decompose()
    desc = body.text.strip()
    img = 'https://lycee-tcg.com/card/{}'.format(contents.find('img')['src'][2:])

    qna_list = contents.findAll('div', recursive=False)
    card_info['qna'] = []
    for qna in qna_list:
        qna_body = qna.findAll('div', recursive=False)[-1].text.strip().replace('\t', '').replace('\n\n', '\n')
        card_info['qna'].append(qna_body)

    card_info['id'] = cardno
    card_info['desc'] = desc
    card_info['img'] = img
    return card_info


for i in reversed(range(0, 182)):
    print(i)
    req = requests.get('https://lycee-tcg.com/card/?page={}&deck=&smenu=1'.format(i))
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')

    lnk_table_list = soup.find('table').findAll('table')
    for lnk_table in lnk_table_list:
        lnk = lnk_table.find('a')['href']
        card_info = get_info('https://lycee-tcg.com/card/{}'.format(lnk[2:]))

        json.dumps(card_info)
        with open('../card_db/info/{}.json'.format(card_info['id']), 'w', encoding='utf-8') as f:
            f.write(json.dumps(card_info, ensure_ascii=False)+'\n')
        try:
            urllib.request.urlretrieve(card_info['img'], '../card_db/img/{}'.format(os.path.basename(card_info['img'])))
        except:
            pass

