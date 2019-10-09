"""
针对https://18h.animezilla.com网站的漫画下载程序
制作人   YH
制作时间 2019-10-9
版本     5.0
1.0 下载指定图片
2.0 单独页面内图片下载
3.0 系列图片下载
4.0 模块化代码、增加多线程下载添加输入模块 直接输入链接开始下载
5.0 加入位置存储及文件夹自动创建
"""

import requests
from lxml import etree
import time
import os
from concurrent import futures
url_base = input('请输入起始链接：' )
url = str(url_base+'/')
headers = {
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}


def download_img(src,dirname,filename):

    dirnames = 'f:/漫画/'+ dirname +'/'
    if not os.path.exists(dirnames):
        os.makedirs(dirnames)
    img = requests.get(src,headers=headers)
    with open(dirnames+filename +'.jpg', 'wb') as fd:         #因在url中截取的real_ad末尾并没有格式故在文件名后加入“.jpg”以添加固定格式
         fd.write(img.content)

def get_page(url):

    resp=requests.get(url,headers=headers)
    filename = url.split('/')[-1]
    print(url)
    html = etree.HTML(resp.text)
    title = str(html.xpath('/html/head/title/text()'))
    dirnames = title.split('- 成人H漫畫')[0]
    dirname2 = dirnames.replace('/', '-')
    dirname = dirname2.replace("['", '')
    scrs = html.xpath('//*[@id="comic"]/@src')
    ex = futures.ThreadPoolExecutor(111)
    for scr in scrs:
        ex.submit(download_img,scr,dirname,filename)
    next_link = html.xpath('//*[@class="nextpostslink"]/@href')
    return next_link

def main():

    link = url
    print(link)
    next_link_base = str(link)
    current_num = 0
    next_link = [str(link)]
    while next_link:
        time.sleep(1)
        current_num = current_num + 1
        next_link = get_page(next_link_base+str(current_num))


if __name__ == "__main__":
    main()
