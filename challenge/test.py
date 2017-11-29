# -*- coding:utf-8 -*-
import requests,re
url = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing='
content = '90373'
while 1:
    res = requests.get(url+content)
    if res.status_code == 200:
        res.encoding = 'utf-8'
        content = res.text[24:]
        print(res.text)
        content = re.findall(r'[0-9]*$',content)[0]
    else:
        print(content)
        break
#-------------------------------
#pythonchallenge  第四题  正则
# import requests,re
# pattern1 = re.compile('[A-Z]{3}[a-z][A-Z]{3}')
# url = 'http://www.pythonchallenge.com/pc/def/equality.html'
# res = requests.get(url)
# if res.status_code == 200:
#     res.encoding = 'utf-8'
#     content = res.text
#     print(len(content))
#     content = re.findall(r'[^A-Z][A-Z]{3}[a-z][A-Z]{3}[^A-Z]',content,re.S|re.M)      #一个小写字母两遍有且只有3个大写字母
#     print(''.join([i[4:5] for i in content]))
# ----------------------
# pythonchallenge  第三题
# import requests,re
# pattern1 = re.compile('[a-zA-Z0-9]')
# pattern2 = re.compile(r'<!--(.*)-->')
# url = 'http://www.pythonchallenge.com/pc/def/ocr.html'
# res = requests.get(url)
# if res.status_code == 200:
#     res.encoding = 'utf-8'
#     content = res.text
#     print(len(content))
#     content = re.findall(r'<!--(.*)-->',content,re.S|re.M)
#     # content=content[content.find('<!--',800)+4:len(content)-5]
#     nextUrl = ''
#     content = content[0][50:]
#     for i in content:
#       re = pattern1.match(i)
#       if(re):
#         nextUrl += re.string
#     print(nextUrl)
#-----------------------------------
#--------------------------------------------
#pythonchallenge  第二题
#print([chr(2+ord(i)) for i in list('map')])
#--------------------------------------------