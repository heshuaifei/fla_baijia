# -*- coding: utf-8 -*-
# @File  : baijia.py
# @Author: KingJX
# @Date  : 2018/11/21 11:24
""""""

import requests
# import json
from pymongo import MongoClient
from lxml import etree

client = MongoClient(host='localhost', port=27017)
db = client.baijia
collection = db.baijia


def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        text = response.content.decode('utf-8')
        return text
    return None


def parse_page_all(html):
    etree_html = etree.HTML(html)
    all = etree_html.xpath('.//div[@class="col-xs-12"]/a')
    all_first_name = {}
    for item in all:
        one_first_name = []
        name_url = item.xpath('.//@href')[0]
        first_name1 = item.xpath('.//text()')[0]
        first_name = str(first_name1).split('姓名')[0]
        all_first_name[first_name] = name_url
    return all_first_name


def parse_page_one_name(html, first_name):
    etree_html = etree.HTML(html)
    all_name = etree_html.xpath('//div[@class="col-xs-12"]/a')
    person_name = {}
    for item in all_name:
        name_url = item.xpath('.//@href')[0]
        name = item.xpath('.//text()')[0]
        name_url = 'http://' + first_name + name_url
        person_name[name] = name_url
    return person_name


def parse_page_name_info(html):
    etree_html = etree.HTML(html)
    name = []
    name_in_one_word = etree_html.xpath('.//div[@class="panel-body"]/strong/text()')
    if not name_in_one_word:
        name_in_one_word = etree_html.xpath('/html/body/div[2]/div/div[4]/div[1]/div[2]/h4/text()')
    name_five_go = etree_html.xpath('/html/body/div[2]/div/div[4]/div[2]/div/div[2]/div[1]/blockquote/text()')[0]
    name_three_abi = etree_html.xpath('/html/body/div[2]/div/div[4]/div[2]/div/div[2]/div[2]/blockquote/text()')[0]
    name_five_table = etree_html.xpath('/html/body/div[2]/div/div[4]/div[2]/div/div[2]/div[4]/blockquote/div/text()')
    name.append(name_in_one_word)
    name.append(name_five_go)
    name.append(name_three_abi)
    name.append(name_five_table)
    return name


def main():
    url = 'http://www.resgain.net/xmdq.html'
    html = get_one_page(url)
    json_info = {}
    i = 1
    all_first_name = parse_page_all(html)
    for k, v in all_first_name.items():
        j = 1
        one_name_url = v.split('/')
        first_name = one_name_url[2]
        json_info['info'] = []

        for _ in range(10):
            one_name_url1 = 'http://' + first_name + '/name_list_' + str(j) + '.html'
            html = get_one_page(one_name_url1)
            person_name = parse_page_one_name(html, first_name)
            j += 1
            for m, n in person_name.items():
                print(n, m)
                html = get_one_page(n)
                name_info = parse_page_name_info(html)
                json_info_person = {}
                json_info_person[m] = {}
                json_info_person[m]['url'] = n
                json_info_person[m]['five_go'] = name_info
                json_info['info'].append(json_info_person)
                json_info['url'] = v
                json_info['first_name'] = k
                i += 1
                print(i)
        # with open('./baijia.json', 'a')as f:
        #     f.write(json.dumps(json_info))
        collection.insert(json_info)


if __name__ == '__main__':
    main()
