'''
关键QApplication.processEvents()处理未处理的事件实现textEdit的实时显示
学习内容 signal 触发事件  （信号与槽）
'''
# -*- coding=utf-8 -*-
import hashlib,time,requests,sys,os,random
from bs4 import BeautifulSoup
import download360image
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#建立信号
class Communicate(QObject):
    infoText = pyqtSignal()

class Gui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.word = ''
        self.pages = 10
        self.startPage = 1
        self.mark = ''
        self.strTime = str(int(time.time()))
        self.reviewEdit = QTextEdit()
        self.searchEdit = QLineEdit()
        self.sNumEdit = QLineEdit()
        self.stNumEdit = QLineEdit()
        self.markEdit = QLineEdit()
        self.info = ''
        self.isDown = True
        self.initUi()

    def initUi(self):
        self.menu()
        self.resize(1024,760)
        self.setWindowTitle('360下载')
        self.setWindowIcon(QIcon('arrow_left.png'))
        self.layouts()
        self.show()
        self.c = Communicate()
        self.c.infoText.connect(self.appendText)

    def appendText(self):
        self.reviewEdit.append(self.info)

    #菜单
    def menu(self):
        #底部状态栏
        self.statusBar().showMessage('欢迎下载')
        #360搜索下载
        downAction = QAction(QIcon('arrow_left.png'), '&360下载', self)
        #360图书馆下载
        bookAction = QAction(QIcon('arrow_left.png'), '&book下载', self)
        #菜单按钮
        menubar = self.menuBar()
        choose = menubar.addMenu('&选项')
        #添加
        choose.addAction(downAction)
        choose.addAction(bookAction)
        #添加测试按钮
        menubar.addMenu('&测试')

    def do_signal(self,string):
        self.info = string
        #触发信号
        self.c.infoText.emit()
        #处理未处理的事情
        QApplication.processEvents()

    def startSearch(self):
        self.isDown = True
        self.statusBar().showMessage('开始下载啦')
        self.do_signal('开始解析')
        self.word = self.searchEdit.text()
        self.pages = self.sNumEdit.text()
        self.startPage = self.stNumEdit.text()
        self.mark = self.markEdit.text()
        self.do_signal('搜索：{}，中共{}页，从第{}页开始，生成图片标记{},生成目录{}'.format(self.word,self.pages,self.startPage,self.mark,self.word))
        searchs = download360image.Search360(self.word,self.pages,self.startPage,self.mark)
        allUserfulImage = []
        urls = searchs.creat_360SearchUrls()
        l = 1
        for zurl in urls:
            self.do_signal('解析第'+str(l)+'页')
            QApplication.processEvents()
            l = l+1
            links = searchs.get_docLink(zurl)
            for link in links:
                images = searchs.get_ImageUrl(link)
                allUserfulImage = allUserfulImage+images

        self.do_signal('总共约'+str(len(allUserfulImage))+'张图片')
        self.save_Image(allUserfulImage)
        #
    def save_Image(self,allUserfulImage):
        filePath = self.word
        #filePath = filePath.encode('gbk')
        if os.path.exists(filePath):
            pass
        else:
            os.makedirs(filePath)

        i = 1
        bad = 1
        for image in allUserfulImage:
            if self.isDown == False:
                self.do_signal('全部下载完成,实际总共'+str(i)+'张，无效'+str(bad-1)+'张')
                break

            imageType = image.split('.')[-1]
            if(len(imageType) > 10):
                self.do_signal('无效'+str(bad)+'张'+',原图路径：'+image)
                imageType = 'jpg'
                bad = bad + 1

            ir = requests.get(image)
            if ir.status_code == 200:
                imageName = filePath+'/'+str(self.mark)+'_'+str(i)+'_'+self.strTime+'.'+imageType
                open(imageName, 'wb').write(ir.content)
                self.do_signal('已下载第'+str(i)+'张'+':'+imageName+',原图路径：'+image)
                if(i == len(allUserfulImage)):
                    self.do_signal('全部下载完成,实际总共'+str(i)+'张，无效'+str(bad-1)+'张')
                i = i+1

    def layouts(self):
        grid = QGridLayout()

        sButton = QPushButton('开始搜索')
        stopDownButton = QPushButton('停止下载')

        search = QLabel('搜索')
        sNum = QLabel('搜索页数')
        stNum = QLabel('开始页数')
        mark = QLabel('标记')

        self.reviewEdit.setReadOnly(True)
        grid.setSpacing(10)
        grid.addWidget(search, 1, 0)
        grid.addWidget(self.searchEdit, 1, 1)
        grid.addWidget(sNum, 1, 2)
        grid.addWidget(self.sNumEdit, 1, 3)
        grid.addWidget(stNum, 1, 4)
        grid.addWidget(self.stNumEdit, 1, 5)
        grid.addWidget(mark, 1, 6)
        grid.addWidget(self.markEdit, 1, 7)
        grid.addWidget(sButton, 1, 8)
        grid.addWidget(stopDownButton, 1, 9)
        grid.addWidget(self.reviewEdit, 2, 0, 8, 10)  #起始位置 2,0 站位 8,10
        #建立按钮连接
        sButton.clicked.connect(self.startSearch)
        stopDownButton.clicked.connect(self.stopDown)
        #建立widget
        widget = QWidget()

        widget.setLayout(grid)
        self.setCentralWidget(widget)

    def stopDown(self):
        self.isDown = False

if __name__ =='__main__':
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())