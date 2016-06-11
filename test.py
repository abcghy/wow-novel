# -*- coding:utf-8 -*-
import urllib2
import re

def url_get_html(url):
    req = urllib2.urlopen(url)
    html = req.read()
    real_encode = html.decode('gb2312').encode('utf8')
    return real_encode


# 根据第一个页面,获得所有页面的网址


def first2index(html):
    pattern = re.compile(r'<td style=".*?"><a href="(.*?)" target="_blank">(.*?)</a></td>', re.S)
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
    return content.strip(strip)

url = 'http://games.sina.com.cn/o/z/wow/2012-09-16/1537462017.shtml'
# url = 'http://games.sina.com.cn/o/z/wow/2012-09-16/1539462018.shtml'
# print is_more(url)


print get_one_chapter(url)

headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'SSCSum=1; U_TRS1=0000006b.fd3a6467.56f94f36.2f381e53; vjuids=27b78d4ed.153bddd700b.0.0f7d9af2cde3; SINAGLOBAL=101.94.165.82_1462326472.602815; sso_info=v02m6alo5qztKWRk5iljpSUpY6TnKWRk5ClkKOgpZCUkKWRk5yljpOkpZCkkKWRk5SlkJSUpZCTiKadlqWkj5OIuIyTjLmMs6S2jaOMwA==; UOR=www.baidu.com,news.sina.com.cn,; SGUID=1464916693260_54584965; ALF=1496976319; Apache=101.94.168.72_1465475689.478977; ULV=1465476467321:7:6:4:101.94.168.72_1465475689.478977:1465475691132; vjlast=1465476633; __utmt=1; __utma=216132608.9047226.1465440901.1465475692.1465520908.4; __utmb=216132608.1.10.1465520908; __utmc=216132608; __utmz=216132608.1465442224.2.2.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); lxlrttp=1465378555',
    'Host':'games.sina.com.cn',
    'if-Modified-Since':'Tue, 26 Feb 2013 12:25:16 GMT',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
}
