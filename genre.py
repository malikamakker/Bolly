import image_test
from itertools import groupby as g
import sys
from PIL import Image
from sklearn.cluster import KMeans
import os
import os.path
import pandas as pd
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

if __name__ == '__main__':
    list_df = []
    list_emo =['angry','fear', 'sad', 'neutral', 'happy', 'surprise']
    #image = r"C:\Users\User\Desktop\friends.jpg"
    for dirpath, dirnames, filenames in os.walk(r"C:\Users\User\Desktop\Facial_emotion_recognition_using_Keras-master\dir_001\\"):
        for filename in [f for f in filenames if f.endswith(".png") or f.endswith(".jpg")]:
            i = os.path.join(dirpath, filename)
            print(i)
            #print(filename)
            i = str(i)
            image=Image.open(i)
            emotion=getEmotion(i)
            print(emotion)
            e = list_emo.index(str(emotion))
            avg=average_colour(image)
            r=avg[0]
            g=avg[1]
            b=avg[2]
            
            brightness = calculate_brightness(image)
            print(e, r, g, b, brightness)
            list_df.append([filename, e, r, g, b, brightness])
    
    

    X = pd.DataFrame(list_df)
    X.to_csv("Images_cluster_X.csv", sep=',', encoding='utf-8')
    
    kmeans = KMeans(n_clusters=4)
    X2=X.drop([0], axis=1)
    print(X2)
    kmeans.fit(X2)
    y_kmeans = kmeans.predict(X2)
    print(y_kmeans)
    print(X[0])
    centers = kmeans.cluster_centers_
    print(centers)
    
    X["cluster_labels"]=y_kmeans
    for i in range(4):
        print(i)
        print(X.query('cluster_labels == ' + str(i))[0])
                
    

    X.to_csv("Images_cluster.csv", sep=',', encoding='utf-8')
