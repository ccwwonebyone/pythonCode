# -*- coding:utf-8 -*-
import hashlib,time,requests,sys,os,random
from bs4 import BeautifulSoup

class SearchTouTiao:
    base_url = 'http://www.toutiao.com/'
    common_url = 'http://www.toutiao.com/articles_news_beauty/'
    strTime = str(int(time.time()))
    '''
    获取头条文章的搜索链接
    '''
    def get_docLink(self,url):
        res = requests.get(url)
        if res.status_code == 200:
            res.encoding = 'utf-8'
            #print(res)
            html = BeautifulSoup(res.text, "html.parser")
            #print(html)
            doclink = []
            try:
                links = html.select('.title > a')
                for link in links:
                    href = link['href']
                    doclink.append(self.base_url+'a'+href.split('/')[2]+'/')
                return doclink
            except Exception:
                return False
        else:
            return False

    def get_toutiaopage(self):
        res = requests.get(self.common_url)
        totalPage = 1
        if res.status_code == 200:
            res.encoding = 'utf-8'
            #print(res)
            html = BeautifulSoup(res.text, "html.parser")
            pages = html.select('.page_number-next')
            totalPage = pages[-1].text
        return totalPage

    def doc_image(self,url):
        res = requests.get(url)
        imgUrl = []
        if res.status_code == 200:
            res.encoding = 'utf-8'
            #print(res)
            html = BeautifulSoup(res.text, "html.parser")
            imgs = html.select('.article-content > div > p > img')
            for img in imgs:
                imgUrl.append(img['src'])
        return imgUrl

    def do_it(self):
        allpage = self.get_toutiaopage()
        searchPage = int(input('中共有'+allpage+'页文章，搜索多少页：'))
        startPage = int(input('从第几页开始：'))
        userfulPage = []
        totalPage = startPage+searchPage
        images = []
        for page in range(startPage,totalPage):
            if page != 1:
                userfulPage.append(self.common_url+'p'+str(page)+'/')
            else:
                userfulPage.append(self.common_url)
        i = 1
        for docpage in userfulPage:
            print('正在解析第'+str(i)+'页')
            doclinks = self.get_docLink(docpage)
            print('共有'+str(len(doclinks))+'条链接')
            l = 1
            for doclink in doclinks:
                print('正在解析第'+str(i)+'页,第'+str(l)+'条链接')
                images = images + self.doc_image(doclink)
                print('目前有'+str(len(images))+'张图片')
                l = l+1
            i = i+1

        return images

    '''
    下载网上图片到本地
    '''
    def save_Image(self,allUserfulImage):
        filePath = self.strTime
        if os.path.exists(filePath):
            pass
        else:
            os.makedirs(filePath)
        i = 1
        for image in allUserfulImage:
            imageType = image.split('/')[-1]
            ir = requests.get(image)
            if ir.status_code == 200:
                imageName = filePath+'/'+imageType+'_'+self.strTime+'.jpg'
                open(imageName, 'wb').write(ir.content)
                print('已下载第'+str(i)+'张'+':'+imageName)
                if(i == len(allUserfulImage)):
                    print('全部下载完成,实际总共'+str(i)+'张')
                i = i+1

    '''
    开始执行阶段
    '''
    def all_start(self):
        allImages = self.do_it()
        print('总共'+str(len(allImages))+'张')
        self.save_Image(allImages)

if __name__ == '__main__':
    searchs = SearchTouTiao()
    searchs.all_start()