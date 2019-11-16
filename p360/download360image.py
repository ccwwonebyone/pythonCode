# -*- coding:utf-8 -*-
import hashlib,time,requests,sys,os,random
from bs4 import BeautifulSoup

class Search360:
    word = ''
    pages = 10
    startPage = 1
    common_url = 'http://www.360doc.com/search/searchArt.ashx?'
    mark = ''
    strTime = str(int(time.time()))
    headers = {'Referer':'http://www.360doc.com/content/14/1114/01/5846940_424958086.shtml'}
    '''
    word搜索内容
    page搜索页数
    startPage开始页数
    mark 搜索标记
    '''
    def __init__(self,word,page,startPage,mark):
        self.word = word
        self.page = int(page)
        self.startPage = int(startPage)
        self.mark = mark
    '''
    创建360搜索的sign参数
    '''
    def creat_360Sign(self,word,sort,start,end):
        s = "word="+word+"&sort="+sort+"&start="+start+"&end="+end
        s_arr = s.split('&')
        s_arr = sorted(s_arr)
        final_str = ''
        for i in s_arr:
            final_str += i

        s = final_str.lower()
        m = hashlib.md5()
        m.update(s.encode("utf8"))
        return m.hexdigest()
    '''
    创建360搜索的url
    '''
    def creat_360SearchUrls(self):
        word = self.word
        sort = 3
        total = 10*self.page
        searchUrls = []
        urlHeard = 'http://www.360doc.com/search/searchArt.ashx?'
        for i in range(1,total,10):
            ticks = int(time.time()*1000)
            start = i
            if i > 10*(self.startPage-1):
                end = i+9
                sign = self.creat_360Sign(word,str(sort),str(start),str(end))
                searchUrl = urlHeard+'word={}&sort={}&start={}&end={}&sign={}&_={}'.format(word,sort,start,end,sign,ticks)
                searchUrls.append(searchUrl)

        return searchUrls
    '''
    获取360文章的搜索链接
    '''
    def get_docLink(self,zurl):
        res = requests.get(zurl)
        if res.status_code == 200:
            res.encoding = 'utf-8'
            #print(res)
            html = BeautifulSoup(res.text, "html.parser")
            #print(html)
            try:
                links = html.select('.wzbtlista > a')
                return links
            except Exception:
                print('解析数据系错误')
                return False
        else:
            print('请求源地址出错')
            return False
    '''
    获取文章的图片
    '''
    def get_ImageUrl(self,link):
        href = link['href']
        #allUserfulImage = []
        allUserfulImage = {href:[]}
        imgHtml = requests.get(href)
        if imgHtml.status_code == 200:
            imgHtml.encoding = 'utf-8'
            imga = BeautifulSoup(imgHtml.text, "html.parser")
            images = imga.select('img')
            for image in images:
                try:
                    if str(image['src']).find('DownloadImg') == -1:
                        pass
                    else:
                        allUserfulImage[href].append(image['src'])
                except Exception:
                    pass

            return allUserfulImage
        else:
            return False
    '''
    下载网上图片到本地
    '''
    def save_Image(self,allUserfulImage):
        filePath = self.word
        if os.path.exists(filePath):
            pass
        else:
            os.makedirs(filePath)
        i = 1
        bad = 1
        for key,images in allUserfulImage.items():
            self.headers['Referer'] = key
            print(key+'共有'+str(len(images))+'张图片')
            for image in images:
                imageType = image.split('.')[-1]

                if(len(imageType) > 10):
                    print('无效'+str(bad)+'张')
                    bad = bad + 1
                else:
                    ir = requests.get(image,headers=self.headers)
                    if ir.status_code == 200:
                        imageName = filePath+'/'+str(self.mark)+'_'+str(i)+'_'+self.strTime+'.'+imageType
                        open(imageName, 'wb').write(ir.content)
                        print('已下载第'+str(i)+'张'+':'+imageName)
                        if(i+bad == len(allUserfulImage)+1):
                            print('全部下载完成,实际总共'+str(i)+'张，无效'+str(bad)+'张')

                        i = i+1

    '''
    开始执行阶段
    '''
    def all_start(self):
        print('正在解析。。。获取图片中')
        allUserfulImage = {}
        urls = self.creat_360SearchUrls()
        l = 1
        for zurl in urls:
            print('解析第'+str(l)+'页')
            l = l+1
            links = self.get_docLink(zurl)
            for link in links:
                href = link['href']
                images = self.get_ImageUrl(link)
                allUserfulImage[href] = images[href]

        #print(allUserfulImage)
        #print('总共约'+str(len(allUserfulImage))+'张图片')
        self.save_Image(allUserfulImage)

if __name__ == '__main__':
    word = input("搜索：")
    page = input("共100页，搜索页数：")
    startPage = input("开始页数：")
    mark = input("保存标记：")
    while word == '':
        print('搜索内容不能为空')
        word = input("搜索：")

    if page == '':
        page = 5

    if startPage == '':
        startPage = 1

    if mark == '':
        mark = chr(random.randint(97, 122))

    print('搜索：{}，中共{}页，从第{}页开始，生成图片标记{},生成目录{}'.format(word,page,startPage,mark,word))
    searchs = Search360(word,page,startPage,mark)
    searchs.all_start()
