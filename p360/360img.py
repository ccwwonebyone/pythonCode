# -*- coding:utf-8 -*-
import time,requests,sys,os,random,json
from bs4 import BeautifulSoup

class Search360:
    word = ''
    pages = 50
    startPage = 1
    common_url = 'http://image.so.com/j?q=虞成敬&src=srp&correct=虞成敬&sn=0&pn=50'
    mark = ''
    strTime = str(int(time.time()))
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
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

    def creat_url(self):
        total = self.pages * int(self.page)
        urls = []
        for i in range(0,total,self.pages):
            if i >= self.pages * (self.startPage-1):
                url = 'http://image.so.com/j?q={}&src=srp&correct={}&sn={}&pn={}'.format(self.word,self.word,i,i+50)
                urls.append(url)
        return urls

    def get_360Json(self,link):
        re = requests.get(link)
        if re.status_code == 200 :
            re.encoding = 'utf-8'
            jsonData = BeautifulSoup(re.text, "html.parser")
            jsonData = str(jsonData).replace('</em>','')
            dicts = json.loads(jsonData)
            lists = dicts['list']
        else:
            pass

        return lists

    def get_images(self,lists):
        imgs = []
        for jo in lists:
            imgs.append(jo['img'])

        return imgs

    def save_Image(self,allUserfulImage):
        filePath = self.word
        if os.path.exists(filePath):
            pass
        else:
            os.makedirs(filePath)
        i = 1
        bad = 0
        fail = 0
        for image in allUserfulImage:
            imageType = image.split('.')[-1]
            if(len(imageType) > 10):
                bad = bad + 1
                print('无效'+str(bad)+'张')

            else:
                try:
                    ir = requests.get(image, headers=self.headers, timeout=1)
                except:
                    ir = False
                if ir == False:
                    fail = fail+1
                    print(str(fail)+'张下载失败')

                    pass
                else:
                    if ir.status_code == 200:
                        imageName = filePath+'/'+str(self.mark)+'_'+str(i)+'_'+self.strTime+'.'+imageType
                        open(imageName, 'wb').write(ir.content)
                        print('已下载第'+str(i)+'张'+':'+imageName)
                        if(i+bad == len(allUserfulImage)):
                            print('全部下载完成,实际总共'+str(i)+'张，无效'+str(bad)+'张','失败'+str(fail)+'张')

                        i = i+1

    '''
    开始执行阶段
    '''
    def all_start(self):
        links = self.creat_url()
        lists = []
        for link in links:
            lists = lists + self.get_360Json(link)
        images = self.get_images(lists)
        #print(images)
        print('总共约'+str(len(images))+'图片')
        self.save_Image(images)

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

    print('搜索：{}，总共{}页，从第{}页开始，生成图片标记{},生成目录{}'.format(word,page,startPage,mark,word))
    searchs = Search360(word,page,startPage,mark)
    searchs.all_start()
