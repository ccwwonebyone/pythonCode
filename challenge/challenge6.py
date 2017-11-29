import re,os
import zipfile as zp

z = zp.ZipFile("channel.zip")
str = '90052'
ll = []
while True:
    try:
        info = z.read(str+'.txt').decode()
        ll.append(z.getinfo(str+'.txt').comment.decode())
        str = info[16:]
        print(str)
    except Exception as e:
        print(info)
        print(''.join(ll))
        break