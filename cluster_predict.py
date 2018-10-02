import image_test
from itertools import groupby as g
import sys
from PIL import Image
from sklearn.cluster import KMeans
import os
import os.path
import pandas as pd
import numpy as np


X=[[  2.21052632,152.53172228, 123.26473381 ,111.53711299,   0.50853436],
 [  2.5     ,   123.09811287 , 72.39718406 , 56.49452134 ,  0.33304099],
 [  2.375    ,  192.58916947 ,150.44098391 ,126.29092435  , 0.62416507],
 [  2.6      ,  111.61402411 ,109.27180287 ,110.90419508 ,  0.42839212]]

def getEmotion(image):
    #image = r"C:\Users\User\Desktop\friends.jpg"
    result = image_test.test_image(image)
    print(result)
    if not result:
        return 'neutral'
    return (max(set(result), key=result.count))

def calculate_brightness(image):
    greyscale_image = image.convert('L')
    histogram = greyscale_image.histogram()
    #histogram = image.histogram()
    
    pixels = sum(histogram)
    brightness = scale = len(histogram)

    for index in range(0, scale):
        ratio = histogram[index] / pixels
        brightness += ratio * (-scale + index)

    return 1 if brightness == 255 else brightness / scale

def average_colour(image):

  colour_tuple = [None, None, None]
  for channel in range(3):

      # Get data for one channel at a time
      pixels = image.getdata(band=channel)

      values = []
      for pixel in pixels:
          values.append(pixel)

      colour_tuple[channel] = sum(values) / len(values)

  return tuple(colour_tuple)



def getGenre(path):
    list_df = []
    list_emo =['angry','fear', 'sad', 'neutral', 'happy', 'surprise']



    i=path
    image=Image.open(i)
    emotion=getEmotion(i)


    e = list_emo.index(str(emotion))
    avg=average_colour(image)
    r=avg[0]
    g=avg[1]
    b=avg[2]
                                
    brightness = calculate_brightness(image)
    print(e, r, g, b, brightness)

    list_df.append(e)
    list_df.append(r)
    list_df.append(g)
    list_df.append(b)
    list_df.append(brightness)

    distances=[]

    print(len(X))

    for i in range(len(X)):
        s=0
        for j in range(len(list_df)):
            s=s+(X[i][j]-list_df[j])**2
        distances.append(np.sqrt(s))


    print(distances)
    #print(np.argmin(distances))    

    index=np.argmin(distances)

    if(index==0):
        return "Comedy"
    elif (index==1):
        return "Romance"
    elif (index==2):
        return "Action"
    else:
        return "Thriller"
        

