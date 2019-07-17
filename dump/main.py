import numpy as np
import matplotlib.pyplot as plt
import random
import sys
#import load_datasets as loader
import NeuralNet  # importer la classe du Réseau de Neurones
#import DecisionTree  # importer la classe de l'Arbre de Décision
# importer d'autres fichiers et classes si vous en avez développés
# importer d'autres bibliothèques au besoin, sauf celles qui font du machine learning

nn = NeuralNet.NeuralNet(4,3)

test_data_location = 'data/mnist_test.csv'
train_data_location = 'data/mnist_train.csv'

test1 = np.loadtxt(test_data_location, encoding = 'utf-8',dtype=int,skiprows = 1,delimiter = ',')
train1 = np.loadtxt(train_data_location, encoding = 'utf-8',dtype=int, skiprows = 1,delimiter = ',')

test_labels1 = test1[:,0].astype(int)
train_labels1 = train1[:,0].astype(int)
train1 = train1[:,1:]/255
test1 = test1[:,1:]/255

nn = NeuralNet.NeuralNet(3,300)
nn.train1(train1[0:1000],train_labels1[0:1000],10)

import PIL
image7 = PIL.Image.open("bin/7.png").convert('L')
image7.resize((28,28))
image7_array = np.array(image7.resize((28,28)))
image7_array = np.subtract(np.array([255]),image7_array).flatten()/255

print(nn.predict(image7_array,7))

image5 = PIL.Image.open("bin/5.png").convert('L')
image5.resize((28,28))
image5_array = np.array(image5.resize((28,28)))
image5_array = np.subtract(np.array([255]),image5_array).flatten()/255

print(nn.predict(image5_array,5))

image6 = PIL.Image.open("bin/6.png").convert('L')
image6.resize((28,28))
image6_array = np.array(image6.resize((28,28)))
image6_array = np.subtract(np.array([255]),image6_array).flatten()/255

print(nn.predict(image6_array,6))

image8 = PIL.Image.open("bin/8.png").convert('L')
image8.resize((28,28))
image8_array = np.array(image8.resize((28,28)))
image8_array = np.subtract(np.array([255]),image8_array).flatten()/255

print(nn.predict(image8_array,8))

t=0
for j in range(0,100):
	temp = nn.predict(test[j],test_labels[j])
	if temp[0] == temp[1]:
		t+=1
print(t/100)

