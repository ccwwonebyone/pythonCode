# -*- coding:utf-8 -*-
# 题目解析： 图片嵌入了第4题的图片，图片有很多cookie
#所以需要先获取cookie,页面cookie信息  info ： you+should+have+followed+busynothing...
#将第4题的后缀改为busynothing 然后在获取
from urllib import request,response,parse
import urllib
from http import cookies,cookiejar
import bz2

postdata= urllib.parse.urlencode({
    'Username': 'huge',
    'Password': 'file'
}).encode('utf-8')

header = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    #"Accept-Encoding":"    gzip, deflate, br",
    "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
    "Authorization": "Basic aHVnZTpmaWxl",#授权头，账号密码
    "Connection":"keep-alive",
    "Host":"www.pythonchallenge.com",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/55.0"
}
url = r'http://www.pythonchallenge.com/pc/return/romance.html'
url_linkedlist = r'http://www.pythonchallenge.com/pc/def/linkedlist.php?busynothing='
url_linkedlist1 = r'http://www.pythonchallenge.com/pc/def/linkedlist.php?busynothing=12345'


def getcookie(req):
    #声明一个CookieJar对象实例来保存cookie
    ck = cookiejar.CookieJar()
    #利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
    handler = request.HTTPCookieProcessor(ck)
    #通过CookieHandler创建opener
    opener = request.build_opener(handler, request.HTTPHandler)
    r = opener.open(req)
    htmltext = r.read().decode()
    nothing =htmltext.split(' ')[-1]
    print(htmltext + "-------" + nothing)

    opener.close()
    for item in ck:
        #return (item.name + " : " + item.value)
        return (item.value,nothing)


nothing = '12345'
list = []
# for i in range(400):

#     if nothing != 'it.':
#         req = request.Request(url_linkedlist+nothing,postdata,header)
#         reqcookie = getcookie(req)
#         print(i,end=" ： ")
#         nothing = reqcookie[1]
#         list.append(reqcookie[0])

# answer = "".join(list)
# print("")
# print(bz2.decompress(parse.unquote_to_bytes(answer.replace('+', '%20'))).decode('ascii'))

import xmlrpc.client,httplib2
xmlrpc = xmlrpc.client.ServerProxy('http://www.pythonchallenge.com/pc/phonebook.php')
print(xmlrpc.phone('Leopold'))

h = httplib2.Http('.Cache')
url = 'http://www.pythonchallenge.com/pc/stuff/violin.php'
headers = {'Cookie':'info=the flowers are on their way'}
print(h.request(url,headers=headers)[1].decode('utf-8'))