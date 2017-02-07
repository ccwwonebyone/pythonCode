# -*- coding=utf-8 -*-
import sys,download360image
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Gui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.reviewEdit = QTextEdit()
        self.initUi()

    def initUi(self):
        self.menu()
        self.resize(1024,760)
        self.setWindowTitle('360下载')
        self.setWindowIcon(QIcon('arrow_left.png'))
        self.layouts()
        self.show()

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

    def startSearch(self):
        self.statusBar().showMessage('开始下载啦')
        searchs = download360image.Search360('虞成敬',2,1,'y')
        allUserfulImage = []
        urls = searchs.creat_360SearchUrls()
        l = 1
        for zurl in urls:
            self.reviewEdit.append('解析第'+str(l)+'页')
            l = l+1
            links = searchs.get_docLink(zurl)
            for link in links:
                images = searchs.get_ImageUrl(link)
                allUserfulImage = allUserfulImage+images

        self.reviewEdit.append('总共约'+str(len(allUserfulImage))+'张图片')
        self.save_Image(allUserfulImage)

    def save_Image(self,allUserfulImage):
        filePath = self.word
        if os.path.exists(filePath):
            pass
        else:
            os.makedirs(filePath)
        i = 1
        bad = 1
        for image in allUserfulImage:
            imageType = image.split('.')[-1]
            if(len(imageType) > 10):
                self.reviewEdit.append('无效'+str(bad)+'张')
                bad = bad + 1
            else:
                ir = requests.get(image)
                if ir.status_code == 200:
                    imageName = filePath+'/'+str(self.mark)+'_'+str(i)+'_'+self.strTime+'.'+imageType
                    open(imageName, 'wb').write(ir.content)
                    self.reviewEdit.append('已下载第'+str(i)+'张'+':'+imageName)
                    if(i+bad == len(allUserfulImage)+1):
                        self.reviewEdit.append('全部下载完成,实际总共'+str(i)+'张，无效'+str(bad)+'张')

                    i = i+1

    def layouts(self):
        grid = QGridLayout()

        sButton = QPushButton('开始搜索')

        search = QLabel('搜索')
        sNum = QLabel('搜索页数')
        stNum = QLabel('开始页数')
        mark = QLabel('标记')

        searchEdit = QLineEdit()
        sNumEdit = QLineEdit()
        stNumEdit = QLineEdit()
        markEdit = QLineEdit()

        self.reviewEdit.setReadOnly(True)
        grid.setSpacing(10)
        grid.addWidget(search, 1, 0)
        grid.addWidget(searchEdit, 1, 1)
        grid.addWidget(sNum, 1, 2)
        grid.addWidget(sNumEdit, 1, 3)
        grid.addWidget(stNum, 1, 4)
        grid.addWidget(stNumEdit, 1, 5)
        grid.addWidget(mark, 1, 6)
        grid.addWidget(markEdit, 1, 7)
        grid.addWidget(sButton, 1, 8)

        grid.addWidget(self.reviewEdit, 2, 0, 8, 10)  #起始位置 2,0 站位 5,2
        #建立按钮连接
        sButton.clicked.connect(self.startSearch)
        #建立widget
        widget = QWidget()

        widget.setLayout(grid)
        self.setCentralWidget(widget)


if __name__ =='__main__':
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())