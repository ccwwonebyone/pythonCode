# -*- conding=utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt
import random
import os


imgs = cv2.imread('014496w.jpg',3)
img = cv2.imread('014496w.jpg',3)
width,height = imgs.shape[:2]
img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

#设定蓝色阀值|颜色监测
lower_blue = np.array([110,255,50])
upper_blue = np.array([130,255,255])
mask = cv2.inRange(img,lower_blue,upper_blue)
res = cv2.bitwise_and(img,img,mask=mask)

#腐蚀准备
kernel= np.ones((5,5),np.uint8)

#画矩形
ju=np.zeros((512,512,3), np.uint8)
ju = cv2.rectangle(ju,(50,20),(160,70),(0, 255,0),3)
ju = cv2.cvtColor(ju,cv2.COLOR_BGR2GRAY)
rss,csc = cv2.threshold(ju,0,255,cv2.THRESH_BINARY)
#轮廓检测
image,contours,hierarchy = cv2.findContours(csc,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
#需要检测的轮廓
checkcnt = contours[0]

img = cv2.medianBlur(res,5)

#边缘检测
img = cv2.Canny(img,400,500)

#二值化
ret,th1 = cv2.threshold(img,0,255,cv2.THRESH_BINARY)
#膨胀
th1 = cv2.dilate(th1,kernel,iterations= 2)
th1 = cv2.morphologyEx(th1,cv2.MORPH_OPEN, kernel)
th1 = cv2.morphologyEx(th1,cv2.MORPH_CLOSE, kernel)
#腐蚀
th1 = cv2.erode(th1,kernel,iterations= 1)
th1 = cv2.erode(th1,kernel,iterations= 2)

#开运算
th1 = cv2.morphologyEx(th1,cv2.MORPH_OPEN, kernel)
#闭运算
th1 = cv2.morphologyEx(th1,cv2.MORPH_CLOSE, kernel)
th1 = cv2.dilate(th1,kernel,iterations= 2)
th1 = cv2.morphologyEx(th1,cv2.MORPH_CLOSE, kernel)

#轮廓检测
image,contours,hierarchy = cv2.findContours(th1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
#轮廓匹配
cont = contours[0]
res = 0
for cnt in contours:
	res = cv2.matchShapes(checkcnt,cnt,1,0.0)
	print(res)
	if res > ret:
		ret = res
		cont = cnt

x,y,w,h=cv2.boundingRect(cont)
c = imgs[y:y+h+5,x-10:x+w+5]
#print(c.shape)
th1 = cv2.resize(th1,(int(width/2),int(height/3)),interpolation=cv2.INTER_CUBIC)
imgs = cv2.resize(imgs,(int(width/2),int(height/3)),interpolation=cv2.INTER_CUBIC)
print(imgs.shape)
#c = cv2.resize(c,(int(width/2),int(height/3)),interpolation=cv2 .INTER_CUBIC)
#print(x,y,w,h)
cv2.imshow('s',c)
cv2.waitKey(0)
cv2.destroyAllWindows()

'''
height,width=img.shape[:2]
kernel = np.ones((5,5),np.uint8)
#erosion = cv2.erode(img,kernel,iterations = 1)
#膨胀
erosion= cv2.dilate(img,kernel,iterations= 1)
opening = cv2.morphologyEx(erosion,cv2.MORPH_OPEN, kernel)
#边缘监测
#opening = cv2.Canny(opening,30,40)
#图片大小重置
opening = cv2.resize(opening,(int(width/2),int(height/3)),interpolation=cv2 .INTER_CUBIC)

cv2.imshow('s',opening)

cv2.waitKey(0)
cv2.destroyAllWindows()


imgs = cv2.imread('009145w.jpg')
# 将图片从 BGR 空间转换到 HSV 空间
print(imgs.shape)
# 直接读取单通道
gray_img = cv2.imread('009145w.jpg', cv2.COLOR_BGR2HSV)
print(gray_img.shape)

#w,h,c    宽高通道
img=np.zeros((512,512,3), np.uint8)
#b,e.c.w  开始位置,结束位置,颜色,大小
cv2.line(img,(0,0),(511,511),(255,0,0),5)
cv2.rectangle(img,(384,0),(510,128 ),(0, 255,0),3)
cv2.circle(img,(447,63),63,(0, 0,255), -1)
cv2.ellipse(img,(256,256),(100,50 ),0,0,180,255 ,-1)
pts=np.array([[10,5],[20,30],[70,20],[50,10]],np.int32)
#这里reshape的第一个参数为-1,表明这一维的长度是根据后面的维度的计算出来的
pts=pts.reshape((-1,1,2))
font=cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img,'OpenCV',(10,500),font,4,(255,255,255 ),2)
winname= 'example'
# cv2.namedWindow(winname)
# cv2.imshow(winname,img)
# cv2.waitKey(0)
# cv2.destroyWindow(winname)

lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])
mask=cv2.inRange(gray_img,lower_blue,upper_blue)
res = cv2.bitwise_and(gray_img,gray_img,mask=mask)
# cv2.imshow('gray_img',gray_img)
# cv2.imshow('mask',mask)
# cv2.imshow('res',res)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
#
# imgs = cv2.imread('009145w.jpg',0)
# imgs = cv2.medianBlur(imgs,5)
# ret,th1= cv2.threshold(imgs,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# th2 = cv2.adaptiveThreshold(imgs,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
#     cv2.THRESH_BINARY,11,2)
# th3 = cv2.adaptiveThreshold(imgs,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#     cv2.THRESH_BINARY,11,2)
# titles= ['OriginalImage', 'Global Thresholding (v = 127)','Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
# images= [imgs, th1, th2, th3]
# for i in range(4):
#     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])
# plt.show()
imgs = cv2.imread('009145w.jpg')
#kernel= np.ones((5,5),np.float32)/25
'''