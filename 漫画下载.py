"""
针对https://18h.animezilla.com网站的漫画下载程序
制作人   YH
制作时间 2019-10-9
版本     6.0
1.0 下载指定图片
2.0 单独页面内图片下载
3.0 系列图片下载
4.0 模块化代码、增加多线程下载添加输入模块 直接输入链接开始下载
5.0 加入位置存储及文件夹自动创建
6.0 创建html网页，将文件名存入网页内，实现网页内查看漫画
"""

import requests
from lxml import etree
import time
import os
from concurrent import futures
url_base = input('\n-----------------------请在下方输入起始链接-----------------------\n' )
url = str(url_base+'/')
headers = {
        'Referer': url,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
#保存位置
downloadname = "F://漫画//"

def download_img(src,dirnames,filename):

    img = requests.get(src, headers=headers)
    os.chdir(dirnames)                          #打开要写入内容的文件夹
    with open(filename,'wb') as fd:             #将图片写入
        fd.write(img.content)
        fd.close()
    with open('快速查看.html','a') as fdd:
         fdd.write("<div align='center'><img src='{}'></div>".format(filename))
         fdd.close()
def get_page(url):
    global dirnames
    print(url)
    resp=requests.get(url,headers=headers)
    filename = url.split('/')[-1]+'.jpg'
    html = etree.HTML(resp.text)
    title = html.xpath('/html/head/title/text()')
    for name in title:
        dirnames = name.split('- 成人H漫畫')[0]
        delname = dirnames.replace('/', '-').replace("['", '').replace('\'', '').replace('<','').replace('>','').replace('?', '').replace('｜', '').replace("'", '').replace('"', '')
        dirnames = os.path.join(downloadname,delname)
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
    if  next_link == next_link:
        print('\n -----------------------已经下载完毕！请打开目录查看.-----------------------------')

if __name__ == "__main__":
    main()
