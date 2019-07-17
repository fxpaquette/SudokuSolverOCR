# -*- coding: utf-8 -*-
"""
Created on Thu May  9 19:18:34 2019

@author: F-X
"""

from skimage.segmentation import mark_boundaries
from skimage.segmentation import slic
import matplotlib.pyplot as plt
import scipy.misc as im
from sklearn import svm
import seaborn as sns
import numpy as np
from PIL import Image

path_img = 'bin/test.PNG'

# charger une image
#img = im.imread(path_img)
img = np.array(Image.open(path_img).convert('RGB'))

# utilisation de l'algorithme SLIC
superpixel_labels = slic(img, n_segments=81, compactness=100)

# récupérer les canaux de couleur de l'image
red = img[:, :, 0]
green = img[:, :, 1]
blue = img[:, :, 2]

# recuperer le nombre de superpixels
nb_superpixels = np.max(superpixel_labels) + 1

# attribuer la couleur moyenne de chaque superpixel
# aux pixels lui appartenant
for label in range(nb_superpixels):
    idx = superpixel_labels == label
    red[idx] = np.mean(red[idx])
    green[idx] = np.mean(green[idx])
    blue[idx] = np.mean(blue[idx])

# dessiner les bordures des superpixels en noir et blanc
img1 = mark_boundaries(img, superpixel_labels, color=(1, 1, 1), outline_color=(0, 0, 0),mode='outer')
#img1 = mark_boundaries(img, superpixel_labels)

# afficher le résultat
plt.imshow(img1)
plt.show()
