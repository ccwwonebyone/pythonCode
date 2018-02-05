from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys,time,os
from multiprocessing import Process, Pool
from pdf_en_cn import PdfEnCn

class Gui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.openFileButton = QPushButton('打开文件')
        self.startTranButton = QPushButton('开始翻译')
        self.oldText = QTextEdit()
        self.newText = QTextEdit()
        self.fileText = QLineEdit()
        self.progress = QProgressBar()
        self.isTran = False
        self.initUi()

    def initUi(self):
        self.resize(960, 560)
        self.setWindowTitle('翻译')
        self.show()
        self.grid = QGridLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.grid)
        self.file = QFileDialog(self.widget, './', '选择文件')
        #self.file.setFilter("*.pdf;;*.txt;;*.doc;;*.docx")
        self.setCentralWidget(self.widget)
        self.layouts()
        self.buttons()
        self.show()

    def layouts(self):
        self.grid.setSpacing(12)
        self.grid.addWidget(self.openFileButton, 0, 0, 1, 1)
        self.grid.addWidget(self.fileText, 0, 3, 1, 3)
        self.fileText.setReadOnly(True)
        self.grid.addWidget(self.startTranButton,0,6,1,4)
        self.grid.addWidget(QLabel('原文'),1,0,1,1)
        self.grid.addWidget(QLabel('译文'), 1, 5,1,1) 
        self.grid.addWidget(self.oldText, 2, 0,5,5)
        self.grid.addWidget(self.newText, 2, 5,5,5)
        self.grid.addWidget(self.progress,7,0,1,10)
        self.statusBar().showMessage('准备就绪')
    
    def buttons(self):
        #self.openFileButton.setIcon(QIcon('./src/b-1.png'))
        self.openFileButton.clicked.connect(self.openFileDir)
        #self.startTranButton.setIcon(QIcon('./src/b-2.png'))
        self.startTranButton.clicked.connect(self.startTran)
        self.startTranButton.clicked.connect(self.puse)
    def puse(self):
        self.isTran = False

    def do_signal(self):
        t = QTime()
        t.start()
        while(t.elapsed() < 1000):
            QApplication.processEvents()

    def startTran(self):
        if self.isTran:
            self.progress.setValue(0)
            self.isTran = False
            self.startTranButton.setText('开始翻译')
            return
        self.startTranButton.setText('停止翻译')
        self.isTran = True
        fileName = self.fileText.text()
        if fileName == '':
            self.statusBar().showMessage('请选择文件')
            return False
        pdf = PdfEnCn('20180126000118825', 'viZi_BOz82KK1FbIIE8x')
        pdFcontent = pdf.readPdf(fileName)        
        handler = open(fileName +'trans.txt', 'w+',  encoding='utf-8')
        #根据总页数设置翻译进度
        self.progress.setValue(0)
        for i in range(len(pdFcontent)):
            if not self.isTran: break
            self.statusBar().showMessage('共'+str(len(pdFcontent))+'页，翻译第' + str(i+1) + '页')
            reslut = ''
            for j in range(0,len(pdFcontent[i]),1800):                      #百度API一次最多翻译2000字符
                reslut += pdf.get_translate_content(pdFcontent[i][j:j+1800])
                self.do_signal()                                            #百度API长字符串间隔时间3s
            handler.write(reslut)                                           
            self.oldText.append(pdFcontent[i])
            self.newText.append(reslut)
            process = int(((i + 1) / len(pdFcontent)) * 100)
            self.progress.setValue(process)
        handler.close()
        self.isTran = False
        self.startTranButton.setText('开始翻译')
        self.statusBar().showMessage('翻译完成')
    def openFileDir(self):
        fileName,fileType = self.file.getOpenFileName()
        self.fileText.setText(fileName)
        self.statusBar().showMessage('打开文件' + fileName)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())
