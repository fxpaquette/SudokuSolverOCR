# -*- coding: utf-8 -*-
"""
Created on Thu May  9 11:56:00 2019

@author: F-X
"""

import numpy as np
from PIL import Image
import glob, os
import NeuralNet

class NumbersOCR:
    def __init__(self,**kwargs):
        self.nn = NeuralNet.NeuralNet(3,800) #3,800
    def train_ocr(self):
        train = []
        threshold = 127
        #for number in glob.glob("data/28x28/*"):
        #    for infile in glob.glob(number+'/*'):
        #        file, ext = os.path.splitext(infile)
        #        im = Image.open(infile).convert('L') #convertir en noir et blanc
        #        temp = [int(number[-1])] + (np.array(im).flatten()/255).tolist()
        #        train.append(temp)
        for number in glob.glob("data/real_grouped/*"):
            for infile in glob.glob(number+'/*'):
                file, ext = os.path.splitext(infile)
                im = Image.open(infile).convert('L') #convertir en noir et blanc
                #Convertir en image binaire
                list_binary = np.array(im).flatten().tolist()
                for i in range(0,len(list_binary)):
                    if list_binary[i] > threshold:
                        list_binary[i] = 1
                    else:
                        list_binary[i] = 0
                temp = [int(number[-1])] + list_binary
                train.append(temp)
                if(len(list_binary)>784):print("Stop ",infile)
                #print(temp)
        #print(train)
        train_mat = np.array(train)
        #print(train_mat)
        #print("Shape", train_mat.shape)
        np.random.shuffle(train_mat)
        train_labels = train_mat[:,0].astype(int)
        train_mat = train_mat[:,1:]
        self.nn.train(train_mat,train_labels,10,0.075,10)
    
    def decodeNN(self):
        self.nn.decode()
        #test
        #for infile in glob.glob('bin/test/*'):
        #    file, ext = os.path.splitext(infile)
        #    im = Image.open(infile).convert('L')
        #    box = im.getbbox()
        #    new_box = newtuple = (box[0]+15,box[1]+15,box[2]-15,box[3]-15)
        #    im_processed = im.crop(new_box)
        #    im_array = np.array(im_processed.resize((28,28))).flatten()/255
        #    print(self.nn.predict(im_array,int(file[-1])))

    def analyse(self,matrice_image):
        threshold = 127
        im_array = matrice_image.flatten()
        for i in range(0,784):
                    if im_array[i] > threshold:
                        im_array[i] = 1
                    else:
                        im_array[i] = 0
        #for i in range(len(im_array)):
        #    if im_array[i]>0.05:
        #        im_array[i] = 1 #max(5*im_array[i],1)
        prediction = self.nn.predict(im_array,0)[0]
        return prediction



#image7 = Image.open("bin/7.png").convert('L')
#image7_array = np.array(image7.resize((28,28))).flatten()/255
#print(nn.predict(image7_array,7))
#
#image5 = Image.open("bin/5.png").convert('L')
#image5_array = np.array(image5.resize((28,28))).flatten()/255
#print(nn.predict(image5_array,5))
#
#image6 = Image.open("bin/6.png").convert('L')
#image6_array = np.array(image6.resize((28,28))).flatten()/255
#print(nn.predict(image6_array,6))
#
#image8 = Image.open("bin/8.png").convert('L')
#image8_array = np.array(image8.resize((28,28))).flatten()/255
#print(nn.predict(image8_array,8))
