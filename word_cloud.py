from nltk import word_tokenize
from nltk import pos_tag

from itertools import groupby as gb
from collections import Counter

import matplotlib.pyplot as plt
# from PIL import Image
import wordcloud
from wordcloud import WordCloud

from collections import Counter

from nltk import pos_tag, word_tokenize
from collections import Counter

from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud.tone_analyzer_v3 import ToneInput

def getEmotion(text):
    
    print(text)
    service = ToneAnalyzerV3(username='your-username',password='your-password',version='2017-09-21')
    service.set_detailed_response(True)
    tone_input = ToneInput(text)
    tone = service.tone(tone_input=tone_input, content_type="application/json")

    emo_score=[]
    for emotion in tone.result["document_tone"]["tones"]:
        print(emotion["score"])
        print(emotion["tone_name"])
        emo_score.append(emotion["score"])
    if not emo_score:
        print('Neutral')
        return 'Neutral'
    else:
        print(tone.result["document_tone"]["tones"][emo_score.index(max(emo_score))]["tone_name"])
        return(tone.result["document_tone"]["tones"][emo_score.index(max(emo_score))]["tone_name"])  



def find_characters(text):
    tokenized = word_tokenize(text)
    print(tokenized)
    tagged = pos_tag(tokenized)
    print(tagged)
    proper_nouns = []
    i = 0
    while i < len(tagged):
        if tagged[i][1] == 'NNP':
            if tagged[i+1][1] == 'NNP':
                proper_nouns.append(tagged[i][0].lower() +
                                    " " + tagged[i+1][0].lower())
                i+=1 
            else:
                proper_nouns.append(tagged[i][0].lower())
        i+=1 
    print(proper_nouns)
    summarize = dict(Counter(proper_nouns).most_common(3))
    return list(summarize.keys())









def tokenize_lower_text(text):
    tokenized = word_tokenize(text)
    tokenized = [word.lower() for word in tokenized]
    return tokenized



def parse_text(t):
    open_q = '``'
    close_q = "''"
    found_q = False # this will be used to break the while loop below
    # current will hold words until an open quote is found
    current = []
    
    parsed_dialog = [] 
    parsed_narrative = []
    length = len(t)
    i = 0

    while i < length:
        word = t[i]
        
        if word != open_q and word != close_q:
            current.append(word)

        elif word == open_q or word == close_q:
            parsed_narrative.append(current)

            current = []
            current.append(word)

            while found_q == False and i < length-1:
                i += 1
                if t[i] != close_q:
                    current.append(t[i])
                else:
                    current.append(t[i])
                    parsed_dialog.append(current)
                    current = []
                    found_q = True
        
        found_q = False
        i += 1
        
    return (parsed_dialog, parsed_narrative)





def split_sent(t):
    sent_list = []
    for sent in t:
        k = [list(sent) for i, sent in gb(sent, lambda item: item=='.')]
        for i in k:
            if len(i) > 1:
                sent_list.append(i)
    return (sent_list)

def protagonist(n, p_list):
    protagonist_narrative = {}
    for p in p_list:
        protagonist_narrative[p] = []

    for i in n:
        for word in i:
            
            if word in p_list:
                if word == p_list[0]:
                    protagonist_narrative[word].append(i)
                if word == p_list[1] :
                    protagonist_narrative[word].append(i)
                if word == p_list[2]:
                    protagonist_narrative[word].append(i)
                    
    return protagonist_narrative
        



def tagged_text(i):
    tagged = [pos_tag(word) for word in i]
    return tagged

def parse_tagged(protagonist_dict):
    tagged_dict = {}
    
    for k, v in protagonist_dict.items():
        tagged_dict[k] = tagged_text(v)
    return tagged_dict
    



def descriptor_verbs_adverbs(td):
    descriptor_words = {}
    descriptor_count = {}
    
    for k, v in td.items():
        # Create a key in the dictionary for the protagonist.
        descriptor_words[k] = []
        
        # Loop through each sentence in the list
        for s in v:
            for i in range(len(s)):
                
                # Cases of VERB - NOUN (e.g. "said Ron")
                if 'VB' in s[i][1]: 
                    try:
                        if s[i+1][0] == k:
                            descriptor_words[k].append(s[i][0])
                            
                            # Subset of cases where VERB - NOUN is followed by an ADVERB (e.g. "said Ron angrily")
                            try:
                                if 'RB' in s[i+2][1]:
                                    descriptor_words[k].append(s[i+2][0])
                            except:
                                continue
                            
                    except:
                        continue
                if 'NN' in s[i][1]: 
                    try:
                        if 'VB' in s[i+1][1]:
                            descriptor_words[k].append(s[i+1][0])
                            cnt[word] += 1
                            # Subset of cases where NOUN - VERB is followed by an ADVERB (e.g. 
                            #"Hermione explained patiently")
                            try:
                                if 'RB' in s[i+2][1]:
                                    descriptor_words[k].append(s[i+2][0])
                            except:
                                continue
                            
                    except:
                        continue
        
        descriptor_count[k] = Counter(descriptor_words[k])
      
        
    return (descriptor_words, descriptor_count)

def word_cloud(text):
    return_list = []
    file = open(text, "r")
    text = file.read() + '''"'''
    ending = text[-400:]
    print("The emotion of the ending of the movie is:")
    #print(getEmotion(ending))
    return_list.append(getEmotion(ending))
    tokenized = tokenize_lower_text(text)
    parsed_dialog, parsed_narrative = parse_text(tokenized)
    p_list = find_characters(text)
    #print(tokenized)

    narrative_split_sent = split_sent(parsed_narrative)
    protagonist_dict = protagonist(narrative_split_sent, p_list)

    print(narrative_split_sent)#,protagonist_dict)
    for p in p_list:
        print("Sample from %s key:" % p.title())
        print(protagonist_dict[p][:5])
    # Call the function and save the results in a variable called tagged_dict.
    tagged_dict = parse_tagged(protagonist_dict)


    # Let's see what these look like by printing the first two sentences in each key.
    for p in p_list:
            print("%s : " % p.title())
            print(tagged_dict[p][:2])
    descriptor_words, descriptor_count= descriptor_verbs_adverbs(tagged_dict)
    print(descriptor_words)
    wc = WordCloud(background_color="white", 
                   max_words=50, 
                   min_font_size =5, 
                   max_font_size=40, 
                   relative_scaling = 0.4, 
                   normalize_plurals= True)

    fig_sz = (20,20)

    i=0
    for name in p_list:
        print ("*" * 20, name, "*" * 20)
        wc.generate(' '.join(descriptor_words[name])+getEmotion(' '.join(descriptor_words[name])))
        return_list.append(name)
        return_list.append(getEmotion(' '.join(descriptor_words[name])))
        plt.figure(figsize=fig_sz)
        plt.imshow(wc)
        plt.axis("off")
        plt.savefig(r'C:\Users\User\Desktop\Facial_emotion_recognition_using_Keras-master/static/images/WordCloud' + str(i) + '.jpg')
        i = i+1

        plt.show()
    return return_list





