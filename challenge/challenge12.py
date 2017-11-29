import re
f = open(r'evil2.gfx','rb')
content = f.read()
f.close()
for i in range(5):
    f = open(r'result%d.jpg' % i ,'wb')
    f.write(content[i::5])
    f.close()