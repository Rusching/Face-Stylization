import re
import urllib.request
import os
import requests
import argparse

# download images from caoliu
# it's better to examine the regular expression of name of picture and name to title
# be careful about utf-8 and gbk


def get_html(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    html=urllib.request.urlopen(req).read().decode('gbk')
    return html


def extract_jpgs(html):
    jpg_re = re.compile(r'data-src="(.*?\.jpg)"')
    jpg_list = re.findall(jpg_re, html)
    print("extracted {} jpgs".format(len(jpg_list)))
    return jpg_list


def extract_gifs(html):
    gif_re = re.compile(r"ess-data='(.*?\.gif)'")
    gif_list = re.findall(gif_re, html)
    if len(gif_list) > 0:
        if ' ' in gif_list[0]:
            redundant = gif_list[0]
            gif_list.pop(0)
            redundant = redundant.split(' ')[-1] + '\''
            redundant = re.findall(gif_re, redundant)[0]
            gif_list.append(redundant)
    print("extracted {} gifs".format(len(gif_list)))
    return gif_list


def extract_titles(html):
    title_re = re.compile(r'<tr><td class="h"> --> <b>本頁主題:</b>(.*?)</td>')
    title = re.findall(title_re, html)[0].lstrip().rstrip()

    author_re = re.compile(r'<th width="230" rowspan="2" style="min-width:100px;"><b>(.*?)</b>')
    author = re.findall(author_re, html)[0]

    article_name = author + '_' + title
    print("extracted title: {}".format(article_name))
    return article_name


def get_img(html):
    jpg_list = extract_jpgs(html)
    # gif_list = extract_gifs(html)
    # jpg_list.extend(gif_list)

    os.chdir('/home/attheendlof')

    article_name = 'WPAP'
    if not os.path.exists(article_name):
        os.mkdir(article_name)

    with open(article_name + '/' + 'url.txt', 'w') as f:
        f.write(url)

    for imgurl in jpg_list:
        file_name = imgurl.split('/')[-1]  # 文件命名
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
        response = requests.get(imgurl, headers=headers)
        with open(article_name + '/' + file_name, 'wb') as f:  # 以2进制形式写入文件名
            f.write(response.content)
        print("write {}".format(file_name))


url = 'https://stars-onart.pixels.com/collections/geometric+portraits'
html = get_html(url)
get_img(html)


