from PIL import Image,ImageDraw

im=Image.open("cave.jpg")

width,height=im.size

even=Image.new(im.mode, (width//2,height//2))
odd=Image.new(im.mode, (width//2,height//2))

for x in range(width):
    for y in range(height):
        pixel=im.getpixel((x,y))
        if x%2^y%2:
            odd.putpixel(((x-1)//2, y//2) if x%2 else (x//2, (y-1)//2) , pixel)
        else:
            even.putpixel((x//2, y//2), pixel)
even.show()
odd.show()