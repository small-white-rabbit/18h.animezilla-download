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
#保存位置
downloadname = r"F://漫画2//"

def download_img(src,dirnames,filename):

    img = requests.get(src, headers=headers)
    os.chdir(dirnames)                          #打开要写入内容的文件夹
    with open(filename,'wb') as fd:             #将图片写入
        fd.write(img.content)
        fd.close()

def get_page(url):

    resp=requests.get(url,headers=headers)
    filename = url.split('/')[-1]+'.jpg'
    print(url)
    html = etree.HTML(resp.text)
    title = str(html.xpath('/html/head/title/text()'))
    dirnames = title.split('- 成人H漫畫')[0]
    delname_1 = dirnames.replace('/', '-')
    delname_2 = delname_1.replace("['", '')
    delname_3 = delname_2.replace('\'', '')
    delname_4 = delname_3.replace('<','')
    delname_5 = delname_4.replace('>','')
    delname_6 = delname_5.replace('?', '')
    delname_7 = delname_6.replace('｜', '')
    delname_8 = delname_7.replace("'", '')
    delname_9 = delname_8.replace('"', '')
    dirnames = os.path.join(downloadname,delname_9)

    if not os.path.exists(dirnames):
           os.makedirs(dirnames)
    scrs = html.xpath('//*[@id="comic"]/@src')
    ex = futures.ThreadPoolExecutor(10)
    for scr in scrs:
        ex.submit(download_img,scr,dirnames,filename)
    next_link = html.xpath('//*[@class="nextpostslink"]/@href')
    return next_link

def main():

    next_link_base = str(url)
    current_num = 0
    next_link = [str(url)]
    while next_link:
        time.sleep(1)
        current_num = current_num + 1
        next_link = get_page(next_link_base+str(current_num))


if __name__ == "__main__":
    main()
