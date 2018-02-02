# -*- coding: utf-8 -*-
from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams, LTTextBox
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import hashlib
import random
import requests
import json,time
from urllib.parse import quote

class PdfEnCn():
    appId = '' #百度翻译应用Id
    baidu_key = ''  # 百度翻译密钥
    fromLang = 'auto'
    toLang = 'zh'
    def __init__(self,appId,baidu_key):
            self.appId = appId
            self.baidu_key = baidu_key
    def readPdf(self,pdfPath):
        fp = open(pdfPath, 'rb')  # 以二进制读模式打开
        praser = PDFParser(fp)  # 用文件对象来创建一个pdf文档分析器
        doc = PDFDocument()  # 创建一个PDF文档
        # 连接分析器 与文档对象
        praser.set_document(doc)
        doc.set_parser(praser)
        # 提供初始化密码
        # 如果没有密码 就创建一个空的字符串
        doc.initialize()
        content = []
        # 检测文档是否提供txt转换，不提供就忽略
        if not doc.is_extractable:
            raise PDFTextExtractionNotAllowed
        else:
             # 创建PDf 资源管理器 来管理共享资源
            rsrcmgr = PDFResourceManager()
            # 创建一个PDF设备对象
            laparams = LAParams()
            device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            # 创建一个PDF解释器对象
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            # 循环遍历列表，每次处理一个page的内容
            for page in doc.get_pages():  # doc.get_pages() 获取page列表
                interpreter.process_page(page)
                # 接受该页面的LTPage对象
                layout = device.get_result()
                # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等 想要获取文本就获得对象的text属性，
                # handler = open('./test.txt', 'w+',  encoding='utf-8')
                onePageContent = ''
                for x in layout:
                    if (isinstance(x, LTTextBoxHorizontal)):
                        onePageContent += x.get_text()
                        # handler.write(result)
                # handler.close()
                content += [onePageContent]
        return content
    def get_translate_content(self,content):
        if len(content) > 1900: return False
        salt = random.randint(32768, 65536)
        sign = self.appId + content + str(salt) + self.baidu_key
        m1 = hashlib.md5()
        m1.update(sign.encode('utf-8'))
        sign = m1.hexdigest()
        myurl = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
        myurl = myurl+'?appid='+self.appId+'&q='+quote(content)+'&from='+self.fromLang+'&to='+self.toLang+'&salt='+str(salt)+'&sign='+sign
        content = ''
        ir = requests.get(myurl)
        if ir.status_code == 200:
            ir.encoding = 'utf-8'
            result = json.loads(ir.content.decode('utf-8'))
            if 'error_code' in result.keys() and result['error_code'] != '52000':
                content += result['error_msg'] + '\n'
            else:
                for trans in result['trans_result']:
                    content += trans['dst'] + '\n'
        else:
            content += 'not success\n'
        return content

