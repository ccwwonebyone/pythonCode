# -*- coding=utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#QMainWindow
#QWidget
class Gui(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUi()

    #重写关闭事件
    def closeEvent(self, event):
        reply = QMessageBox.question(self, '消息窗',
            "确定退出么？", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    def button(self):
        #按钮
        qbtn = QPushButton('退出',self)
        qbtn.setToolTip('<b>关闭</b>')
        qbtn.clicked.connect(QCoreApplication.instance().quit) #当self为QWidget时有用
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(175,227)

    #设置居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    #菜单
    def action(self):
        exitAction = QAction(QIcon('arrow_left.png'), '&退出', self)
        exitAction.setShortcut('Ctrl+s')
        exitAction.setStatusTip('退出')
        exitAction.triggered.connect(qApp.quit)

        self.toolbar = self.addToolBar('退出')
        self.toolbar.addAction(exitAction)

        self.statusBar()
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&菜单')
        fileMenu.addAction(exitAction)

    def label(self):
        lbl1 = QLabel('测试一', self)
        lbl1.move(15, 10)

        lbl2 = QLabel('测试二', self)
        lbl2.move(15, 70)

        lbl3 = QLabel('测试三', self)
        lbl3.move(15, 130)

    def layout(self):
        okButton = QPushButton("确定")
        cancelButton = QPushButton("取消")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        #水平框布局
        vbox = QVBoxLayout()
        #拉伸系数
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

    def grid(self):
        grid = QGridLayout()
        self.setLayout(grid)

        names = ['消除', '退格', '', '关闭',
                 '7', '8', '9', '/',
                '4', '5', '6', '*',
                 '1', '2', '3', '-',
                '0', '.', '=', '+']

        positions = [(i,j) for i in range(5) for j in range(4)]

        for position, name in zip(positions, names):

            if name == '':
                continue
            button = QPushButton(name)
            #*position  表示将position存入元组中
            grid.addWidget(button, *position)

    def gridlayout(self):
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)

        self.setLayout(grid)

    def signals(self):
        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)

        self.setLayout(vbox)
        sld.valueChanged.connect(lcd.display)

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.close()


    def but(self):
        btn1 = QPushButton("Button 1", self)
        btn1.move(30, 50)

        btn2 = QPushButton("Button 2", self)
        btn2.move(150, 50)

        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        self.statusBar()

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')

    def diab(self):
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QLineEdit(self)
        self.le.move(130, 22)

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog',
            'Enter your name:')
        if ok:
            self.le.setText(str(text))

    def colordia(self):
        col = QColor(0, 0, 0)

        self.btn = QPushButton('Dialog', self)
        self.btn.move(100, 100)

        self.btn.clicked.connect(self.showcolorDialog)

        self.frm = QFrame(self)
        self.frm.setStyleSheet("QWidget { background-color: %s }"
            % col.name())

    def showcolorDialog(self):

        col = QColorDialog.getColor()

        if col.isValid():
            self.frm.setStyleSheet("QWidget { background-color: %s }"
                % col.name())

    def fontdialog(self):
        vbox = QVBoxLayout()

        btn = QPushButton('Dialog', self)
        btn.setSizePolicy(QSizePolicy.Fixed,
            QSizePolicy.Fixed)

        btn.move(20, 20)

        vbox.addWidget(btn)

        btn.clicked.connect(self.fontshowdialog)

        self.lbl = QLabel('Knowledge only matters', self)
        self.lbl.move(130, 20)

        vbox.addWidget(self.lbl)
        self.setLayout(vbox)


    def fontshowdialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.lbl.setFont(font)

    def filedialog(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.filedialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

    def filedialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.read()
                self.textEdit.setText(data)

     #初始化ui
    def initUi(self):
        #提示
        #QToolTip.setFont(QFont('SansSerif',10))
        #self.setToolTip('这是一个<b>提示</b>')

        #self.button()
        #self.label()
        #self.layout()
        self.filedialog()
        #self.action()  #QMainWindow  使用
        #状态栏
        #self.statusBar().showMessage('准备中...')
        #self.setGeometry(300,300,300,200) #等同于self.resize(300,200) self.move(300,300)
        self.resize(350,300)
        self.center()
        self.setWindowTitle('测试')
        self.setWindowIcon(QIcon('arrow_left.png'))
        self.show()

if __name__ =='__main__':
    app = QApplication(sys.argv)
    gui = Gui()
    sys.exit(app.exec_())
