from PIL import Image as im
from os import path
from math import log
from random import randint
from copy import deepcopy
import pickle as pk

class Gens():
    """
    docstring for Gens
    图片路径
    一代个体数
    """
    def __init__(self, img_path, numbers):
        try:
            with open("data.tmp","rb") as fd:
                data = pk.load(fd)
                self.numbers = data['numbers']
                self.img_path = data['img_path']
                self.size = data['size']
                self.col = data['col']
                self.gens = data['gens']
                self.min_gen = data['min_gen']
                self.times = data['times']
        except:
            self.numbers = numbers
            self.img_path = img_path
            img = im.open(img_path)
            self.size = img.size
            iw,ih = self.size
            self.col  = []
            self.gens = []
            self.min_gen = []
            self.times = 0
            for w in range(iw):
                for h in range(ih):
                    self.col.append(img.getpixel((w,h))[:3])
    #目标信息
    def get_img_info(self):
        return self.gens
    def draw_img(self):
        col = self.col
        img = im.open(self.img_path)
        iw,ih = self.size
        i = 0
        total = []
        for w in range(iw):
            for h in range(ih):
                r,g,b = col[i]
                br,bg,bb = self.col[i]
                total.append(abs(br-r)+abs(bg-g)+abs(bb-b))
                img.putpixel((w,h),col[i])
                i += 1
        print("模拟第"+str(self.times)+"代")
        print("每个像素点差异:"+str(total))
        print("最小差异率:"+str(sum(total)))
        img.save(str(self.times)+".png")

    #初始随机个体
    def rand_gens(self):
        iw,ih = self.size
        for x in range(self.numbers):
            one_gen = []
            for w in range(iw):
                for h in range(ih):
                    one_gen.append((randint(0,255),randint(0,255),randint(0,255)))
            self.gens.append(one_gen)
    #适度比对,保留最合适的一代个体数的gen
    def forecast(self):
        def sort_gen(gen):
            diffTotal = 0
            for j,clo in enumerate(gen):
                r,g,b = clo
                br,bg,bb = self.col[j]
                diffTotal += abs(br-r)+abs(bg-g)+abs(bb-b)
            return diffTotal
        self.gens = sorted(self.gens,key=lambda gen:sort_gen(gen))
        self.min_gen = self.gens[0]
        self.gens = self.gens[:self.numbers]
    #模拟基因交换
    def merge_gen(self):
        w,h = self.size
        higth = len(self.gens)
        for i in range(higth):
            if i == len(self.gens)-1:break
            left_one_gen = self.gens[i]
            right_one_gen = self.gens[i+1]
            new_gen = []
            for i in range(w*h):
                new_gen.append(left_one_gen[i] if [-1,1][randint(0,1)] == 1 else right_one_gen[i])
            self.gens.append(new_gen)
    #模拟基因突变
    def variation(self):
        rate = 0.5
        for i,gen in enumerate(self.gens[self.numbers:]):
            for j,rgb in enumerate(gen):
                if randint(1,100)/100 <= rate:
                    r,g,b = self.gens[i][j]
                    r += [-1,1][randint(0,1)]*randint(3,10)
                    g += [-1,1][randint(0,1)]*randint(3,10)
                    b += [-1,1][randint(0,1)]*randint(3,10)
                    r = 255 if r > 255 else r
                    g = 255 if g > 255 else g
                    b = 255 if b > 255 else b
                    self.gens[i][j] = (abs(r),abs(g),abs(b))

    def draw_min_diff(self):
        col  = self.min_gen
        img = im.open(self.img_path)
        iw,ih = self.size
        i = 0
        total = []
        for w in range(iw):
            for h in range(ih):
                r,g,b = col[i]
                br,bg,bb = self.col[i]
                total.append(abs(br-r)+abs(bg-g)+abs(bb-b))
                img.putpixel((w,h),col[i])
                i += 1
        print("模拟第"+str(self.times)+"代")
        print("每个像素点差异:"+str(total))
        print("最小差异率:"+str(sum(total)))
        img.save(str(self.times)+".png")
        print("存储信息")
        with open("data.tmp","wb") as fd:
            data = {}
            data['numbers'] = self.numbers
            data['img_path'] = self.img_path
            data['size'] = self.size
            data['col'] = self.col
            data['gens'] = self.gens
            data['min_gen'] = self.min_gen
            data['times'] = self.times
            pk.dump(data,fd)
    def start(self):
        self.rand_gens()
        while True:
            self.merge_gen()
            self.variation()
            self.forecast()
            self.times += 1
            if int(self.times%10) == 0:
                self.draw_min_diff()
if __name__ == '__main__':
    gens = Gens('test1.png',100)
    gens.draw_img()
    gens.start()