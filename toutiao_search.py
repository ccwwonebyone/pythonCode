# -*- coding:utf-8 -*-
import hashlib,time,requests,sys,os,random,json
from bs4 import BeautifulSoup

class SearchTouTiao:
    base_url = 'http://www.toutiao.com/'
    strTime = str(int(time.time()))
    #基础连接
    url = "http://www.toutiao.com/search_content/?offset={}&format=json&keyword={}&autoload=true&count=20&cur_tab=1"
    t_mark = 'group'
    headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
            "Accept-Language":"zh-CN,zh;q=0.8",
            "Referer":"http://www.example.com/",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
            }

    #初始化搜索链接
    def __init__(self,search,start,pages):
        self.mark = search
        start = int(start)
        pages = int(pages)
        self.searchs = []
        for off in range(start,start+pages):
            offset = (off - 1)*20
            self.searchs.append(self.url.format(str(offset),search))

    #获取链接标题，以及修改过的链接地址
    def url_content(self,url):
        res = requests.get(url)
        links_info = []
        if res.status_code == 200 :
            res.encoding = 'utf-8'
            links = json.loads(res.text)
            for link in links['data']:
                try:
                    if self.t_mark in str(link['url']):
                        link_info = dict()
                        link_info['title'] = link['title']
                        link_info['url'] = link['url'].replace('group/','a').replace('//','//www.')
                        links_info.append(link_info)
                except Exception:
                    pass
        return links_info
    #创建目录，返回目录路径及其他信息
    def creat_file(self,links_info):
        links_infos = []
        file_path = self.mark
        if os.path.exists(file_path):
            pass
        else:
            os.makedirs(file_path)

        for link_info in links_info:
            link_path = file_path+'/'+link_info['title']
            if os.path.exists(link_path):
                pass
            else:
                try:
                    os.makedirs(link_path)
                except Exception:
                    link_path = file_path+'/s'
                    os.makedirs(link_path)
            link_info['save_path'] = link_path
            links_infos.append(link_info)

        return links_infos

    def doc_image(self,url):
        try:
            res = requests.get(url,headers=self.headers)
            imgUrl = []
            if res.status_code == 200:
                res.encoding = 'utf-8'
                #print(res)
                html = BeautifulSoup(res.text, "html.parser")
                imgs = html.select('.article-content > div > p > img')
                for img in imgs:
                    imgUrl.append(img['src'])
            return imgUrl
        except Exception:
            return []


    def start_do(self):
        for search in self.searchs:
            all_info = self.creat_file(self.url_content(search))
            i = 1
            print(all_info)
            j = 1
            for info in all_info:
                print('开始解析'+str(j))
                images = self.doc_image(info['url'])
                for image in images:
                    imageType = image.split('/')[-1]
                    ir = requests.get(image)
                    if ir.status_code == 200:
                        imageName = info['save_path']+'/'+imageType+'_'+self.strTime+'.jpg'
                        open(imageName, 'wb').write(ir.content)
                        print('已下载第'+str(i)+'张'+':'+imageName)
                        i = i+1
                j = j+1

if __name__ == '__main__':
    searchs = SearchTouTiao('壁纸',1,1)
    searchs.start_do()