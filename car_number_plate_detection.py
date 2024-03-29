# -*- coding: utf-8 -*-
"""Car number plate detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/19MG-HXVRff4UgbxixpA7RE9Dyyg01SMD
"""

import cv2 as cv 
import cv2
!pip install nms
import numpy as np
import matplotlib.pyplot as plt

def crop_rect(img, rect):
    # get the parameter of the small rectangle
    center = rect[0]
    size = rect[1]
    angle = rect[2]
    change = False
    if(abs(angle)>40):
      angle = 90+angle
      change=True
    center, size = tuple(map(int, center)), tuple(map(int, size))

    # get row and col num in img
    height, width = img.shape[0], img.shape[1]
    # print("width: {}, height: {}".format(width, height))
    # print(f"angle = ",angle)
    M = cv.getRotationMatrix2D(center, angle, 1)
    # print(M)
    img_rot = cv.warpAffine(img, M, (width, height))
    # img_rot = img_rot.transpose((1, 0, 2))
    # print(img_rot)
    # plt.imshow(img_rot)
    # size = [size[1],size[0]]
    if(change):
      size = size[::-1]
    
    img_crop = cv.getRectSubPix(img_rot, size, center)
    # print(f"size of cropped = ",img_crop.shape)
    # # img_crop = np.reshape(img_crop,(43,273,-1))
    # # img_crop = img_crop.transpose((1, 0, 2))
    # print(f"size of cropped = ",img_crop.shape)
    # print(f"size of rot = ",img_rot.shape)
    return img_crop, img_rot
# imgrot,_ = crop_rect(img,rect)
# plt.imshow(imgrot)

import nms.nms as nms
curr_path = "plate.png"
image = cv.imread(curr_path)
# image = cv.copyMakeBorder( image, 5,5,5,5,cv.BORDER_CONSTANT,None, (255,255,255))
image = cv2.resize(image, None, fx = 3, fy = 3, interpolation = cv2.INTER_CUBIC)
gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
gray = cv.GaussianBlur(gray,(3,3),0)
th3 = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
# th3_erode = cv.erode(th3,kernel,iterations=1)

th3_canny = cv.Canny(th3,80,100)
kernel = np.ones((5,5),np.uint8)
# th3 = cv.copyMakeBorder( th3, 5,5,5,5,cv.BORDER_CONSTANT,None, (255,255,255))
plt.imshow(th3_canny,cmap='gray')
# erode = cv.dilate(th3_canny,kernel,iterations =1)
# plt.imshow(erode,cmap='gray')
contours, hierarchy = cv2.findContours(th3_canny,cv2.RETR_LIST , cv2.CHAIN_APPROX_NONE)# cv2.RETR_EXTERNAL use if anythign else not worl with th3_canny
print(len(contours))

row,col=th3_canny.shape[0],th3_canny.shape[1]
# print(f"Area Threshold-",(np.sqrt(row*col)*0.8))
t=0 
width_def = []
boxes = []
rects_all=[]
scores = []
indi_char_aligned=[]
for cnt in contours:
  rect = cv.minAreaRect(cnt)
  box = cv.boxPoints(rect)  
  box = np.int0(box)
  cv.drawContours(image,[box],0,(0,0,255),2)
#   print(f"area of cnt-",cv.contourArea(cnt))
  # cv.rectangle(image,(x,y),(x+w,y+h),(255,0,0),1)
  if cv.contourArea(cnt) < (row*col*0.3) and cv.contourArea(cnt)>(np.sqrt(row*col)*1.8): #ptimum for 0.005(row*col)   np.sqrt(row*col)*1 
    # print("=== yes")
    # print(f"area of cnt-",cv.contourArea(cnt))
    # print("CNt")
    x,y,w,h = cv.boundingRect(cnt)
    # cv.rectangle(image,(x,y),(x+w,y+h),(255,0,0),3) 
    rect = cv.minAreaRect(cnt)
    #testing rotation
    # cv.drawContours(th3,cnt,0,(0,255,0),3)
    box = cv.boxPoints(rect)  
    box = np.int0(box)
    # print(box)


    # print(box.shape, box)
    dup = False
    # for boxB in boxes :    
    #     iou = bb_intersection_over_union(box, boxB)
    #     if iou> -1.07:
    #         dup = True
    #     print(iou)
    
    boxes.append(box)
    rects_all.append(rect)
    scores.append(cv.contourArea(cnt))
    # cv.drawContours(image,[box],0,(255,0,0),2)
    
    
    # plt.imshow(img_cropped,cmap='gray')
    # plt.figure(figsize=(10,10))
    # plt.axis('off')
    # plt.axis('off')
    # plt.imshow(fax,cmap='gray')
    
    # cv.imwrite("bigm_"+str(i)+".png",img_cropped)
    #testing rotatrion
    width_def.append(rect[0][0])
    # save_cropped(cnt,th3,i)
    t=t+1
indicies = nms.rboxes(rects_all, scores) 
# ind = nms.
# indicies = nms.nms.rboxes(rects_all, scores)
# cv.drawContours(image, contours, -1, (0,255,0), )
for i in indicies:
  # print(indicies[i])
  box = cv.boxPoints(rects_all[i])  
  box = np.int0(box)
  cv.drawContours(image,[box],0,(255,0,0),2)
  img_cropped,_ = crop_rect(th3, rects_all[i])
  indi_char_aligned.append([rects_all[i][0][0],img_cropped])

k=0
t = len(indicies)
print(t)
indi_char_aligned = sorted(indi_char_aligned)
for i in indi_char_aligned:
  y,x = i[1].shape
  max_dim = max(x,y,64)
  x = (max_dim - x )//2
  y = (max_dim - y)//2
  img = cv.copyMakeBorder(i[1], y, y, x, x,cv.BORDER_CONSTANT,None, (0,0,0))
  cv.imwrite("test_"+str(k)+".png",img)
  k=k+1
print("Total images =",k)
plt.imshow(image)
#this way i m able to extract al cropps in proper rotation but no able to order them in correct order

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from keras.models import model_from_json
json_file = open('model (2).json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model(weights) (1).h5")
print("Loaded model from disk")

import tensorflow as tf
import keras
import cv2 as cv
import matplotlib.pyplot as plt
ans =[]
n_char = t
labels = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

for i in range(n_char):
    path = 'test_'+str(i)+'.png'
    
    img2 = tf.keras.preprocessing.image.load_img(
        path, color_mode="grayscale", target_size=(64,64), interpolation="nearest") 
    input_arr = keras.preprocessing.image.img_to_array(img2)
    invert = input_arr/255.0
    # invert = 255 - input_arr
    # invert = invert/255.0

    # pred = model.predict(input_arr)
    t= np.expand_dims(invert,axis =0)
    p = loaded_model.predict(t,batch_size=1)
    ind = np.argmax(p)
    print(labels[ind],end =' ')