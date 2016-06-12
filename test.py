# -*- coding:utf-8 -*-
import urllib2
import re
import zlib

def url_get_html(url):
    res = urllib2.urlopen(url)
    html = res.read()
    gzipped = res.headers.get('Content-Encoding')
    if gzipped:
        html = zlib.decompress(html, 16+zlib.MAX_WBITS)
    html = html.decode('gb2312', 'ignore').encode('utf-8')
    return html


# 根据第一个页面,获得所有页面的网址
# 根据第一章，得到所有的章节名和url
def first2index(html):
    pattern = re.compile(r'<td.*?>.*?<a href="(.*?)" target="_blank">(.*?)</a></td>', re.S)
    result = pattern.findall(html)
    return result


# 获得当前页面的文章
def getCurrentPage(html):
    pattern = re.compile(r'<div class="KD Z_font2">(.*?)</div>', re.S)
    result = pattern.findall(html)
    pattern2 = re.compile(r'<p>(.*?)</p>', re.S)
    result2 = pattern2.findall(result[0])
    return result2


def is_more(html):
    # 根据第一页,判断有无其它页
    pattern = re.compile(r'<div class="pb">(.*?)</div>', re.S)
    result = pattern.findall(html)
    return result.__len__()

# 根据该页面的第一面,获得最大页面的页数(只有一页无用)
def get_max_page_num(html):
    pattern = re.compile(r'<span class=\'pagebox_num\'><a href=\'.*?\'>(.*?)</a>', re.S)
    result = pattern.findall(html)
    return int(result[result.__len__() - 1])

# 根据 url 该章的其它 url
def url_to_other_url(url, size):
    array = []
    for i in range(2, size + 1):
        array.append(url[:-6] + '_' + str(i) + '.shtml')
    return array

# 根据一篇文章的 url ,无论他是不是有很多页,都抓取全文
# @param url #return html
def get_one_chapter(url):
    html = url_get_html(url)
    article = getCurrentPage(html)
    if (is_more(html) != 0):
        # 有很多页
        max_page = get_max_page_num(html)
        array = url_to_other_url(url, max_page)
        for item in array:
            article += getCurrentPage(url_get_html(item))
    content = ''
    for piece in article:
        content += piece + '\n'
    strip = '&nbsp;\n'
    return content.strip(strip).replace('<strong>', '').replace('</strong>', '')

# url = 'http://games.sina.com.cn/o/z/wow/2012-09-16/1617462071.shtml'

# print is_more(url)

# for item in first2index(url_get_html(url)):
#     print item[0], item[1]
# print get_one_chapter(url)

def get_one_novel(url, name):
    novel = ''
    novel += get_one_chapter(url)
    print '正在爬取：' + name
    for item in first2index(url_get_html(url)):
        novel += item[1] + '\n'
        print '正在爬取：' + item[1]
        novel += get_one_chapter(item[0]) + '\n\n'
    f = open(name.decode('utf8') + u'.txt', 'w')
    f.write(novel)
    f.close()


def get_all_novel(url):
    html = url_get_html(url)
    pattern = re.compile(r'<a href="(.*?)".*?title="<span class=ha>(.*?)</span>', re.S)
    result = pattern.findall(html)
    return result


def novel_url_and_name():
    url = 'http://games.sina.com.cn/o/z/wow/xiaoshuo.shtml'
    url_array = []
    name_array = []
    array = []
    for item in get_all_novel(url):
        if url_array.count(item[0].split()[0]) == 0:
            if name_array.count(item[1].split()[0]) == 0:
                if item[0].split()[0].count('http://games.sina.com.cn/o/z/wow/2012') == 1:
                    url_array.append(item[0].split()[0])
                    name_array.append(item[1].split()[0])
                    array.append([item[0].split()[0], item[1]])
    return array

array = novel_url_and_name()
for item in array:
    get_one_novel(item[0], item[1])

# url = 'http://games.sina.com.cn/o/z/wow/2012-09-14/1205461456.shtml'
# url = 'http://games.sina.com.cn/o/z/wow/2012-09-16/1617462071.shtml'
# get_one_novel(url)