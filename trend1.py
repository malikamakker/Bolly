import pandas as pd
import numpy as np
import scipy.interpolate as interpolate
import scipy.optimize as optimize
def plot_climax(text):
    list_emo = ['angry', 'fear', 'sad', 'neutral', 'happy','surprise']
    df= pd.read_csv(text, sep=',', encoding='utf-8')
    df= df.sort_values(by='frame_number')
    max_val = df.iloc[-1].frame_number

    df["emotion"] = df['emotion'].map(lambda emotion: list_emo.index(emotion))
    man_df = df.loc[df['man/woman'] == 'man']
    woman_df = df.loc[df['man/woman'] == 'woman']
    print(woman_df)

    subset = man_df[['frame_number', 'emotion']]
    tuples = [tuple(x) for x in subset.values]
    subset2 = woman_df[['frame_number', 'emotion']]
    tuples2 = [tuple(x) for x in subset2.values]
    #print(tuples)
    print(tuples2)
            
    from shapely.geometry import LineString

    l1 = LineString(tuples)
    l2 = LineString(tuples2)

    intersection = l1.intersection(l2)
    intersect_points = [list(p.coords)[0] for p in intersection]
    #print(intersect_points)
    import matplotlib.pyplot as plt
    from matplotlib import style
    style.use('ggplot')
    plt.plot(man_df["frame_number"],man_df["emotion"],'g',label='Man', linewidth=5)
    plt.plot(woman_df["frame_number"],woman_df["emotion"],'c',label='Woman',linewidth=5)
    plt.xlabel('Frame number')
    plt.ylabel('Emotion')
    plt.title('Emotion')
    i=0
    for item in intersect_points:
        if item[0] > 3*max_val/4:
            if i==0:
                plt.plot(item[0], item[1], 'ro', label='Possible climax')
            else:
                plt.plot(item[0], item[1], 'ro')
            i=i+1
    plt.legend()
    plt.grid(True,color='k')
    plt.savefig(r'C:\Users\User\Desktop\Facial_emotion_recognition_using_Keras-master/static/images/trend.jpg')
    plt.show()

