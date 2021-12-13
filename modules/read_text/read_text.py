import cv2
import pytesseract
import numpy as np
import nltk
import pandas as pd
from collections import Counter
from modules.read_text import filters

cereal_words=['havregryn','finvalsede','grovvalsede','cornflakes','granola','økologisk','mysli','glutenfri','frosties']
brand_words=['nestle',"kellogs's","vores","kornkammeret",'quaker','nemlig','axa','urtekram','svansø']

def get_txt(file_name):
    img = cv2.imread(file_name)
    grey=filters.get_grayscale(img)
    word_set=get_word_set(grey)
    cereral_word_set=get_pick_words(word_set,cereal_words)
    brand_set=get_pick_words(word_set,brand_words)
    brand=''
    if len(brand_set)==1:
        brand=brand_set.pop()
    words=' '.join(cereral_word_set)
    return(brand,words)

def isword(word):
    ret=True
    if (len(word)<3):
        ret=False
    if (not(word.isalpha())):
        ret=False
    return ret

def get_word_set(img):
    words=set()
    for thres_value in range(25, 255, 10):
        thres=filters.thresholding(img,thres_value)
        thres_txt=pytesseract.image_to_string(thres,config='--psm 11')
        txt=thres_txt.split()
        these_words=set([word.lower() for word in txt if isword(word)])
        words.update(these_words)  
    return(words)

def get_pick_words (words,pick_list):
    found_words=set()
    for word in words:
        for pick_word in pick_list:
            if nltk.edit_distance(word, pick_word)<3:
                found_words.add(pick_word)
    return found_words