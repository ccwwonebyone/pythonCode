from PIL import Image
im = Image.open('oxygen.png')
# for x in range(width):
#     for y in range(height):
#         r,g,b,h = im.getpixel((x,y))
#         if r==g==b:         #灰色  r=g=b
#             info += chr(r)   #我也不知道为什么要用chr 估计是数字变成字母吧
#print(info)
#print(dir(im))
str = ''.join([chr(i[0]) for i in [im.getpixel((j,im.size[1]/2)) for j in range(0,im.size[0],7)]])
info = str[43:86]
print(''.join([chr(int(i.strip())) for i in info.split(',')]))