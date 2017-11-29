from PIL import Image
im = Image.open("mozart.gif")
for y in range(im.size[1]):
    #获得像素点
    line=[im.getpixel((x, y)) for x in range(im.size[0])]
    idx=line.index(195)
    line=line[idx:]+line[:idx]
    #重新排列像素点
    [im.putpixel((x, y),line[x]) for x in range(len(line))]

im.show()
#new.putpixel((x,y), im.getpixel((count,0)))