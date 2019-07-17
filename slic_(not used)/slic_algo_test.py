# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 13:19:03 2019

@author: F-X
"""

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import SLIC

#path_img = 'bin/test.PNG'
path_img = 'bin/sudoku_book.jpg'
#path_img = 'bin/dog.png'

# charger une image
img = np.array(Image.open(path_img).convert('RGB'),dtype='int64')
plt.imshow(img)

slic = SLIC.SLIC(img,2,50,10)
slic.computeSuperPixels()
#slic.renforceConnectivite()
img_segmenter = slic.addContours(np.array([255,0,0]))
plt.imshow(img_segmenter)

##path_img = 'bin/test.PNG'
#path_img = 'bin/dog.png'
#
## charger une image
#img = np.array(Image.open(path_img).convert('RGB'),dtype='int64')
#plt.imshow(img)
#
#slic = SLIC.SLIC(img,40,40,10)
#slic.computeSuperPixels()
#slic.renforceConnectivite()
#img_segmenter = slic.addContours(np.array([255,0,0]))
#plt.imshow(img_segmenter)


import glob, os
for infile in glob.glob('bin/test/*'):
   file, ext = os.path.splitext(infile)
   im = Image.open(infile).convert('L')
   box = im.getbbox()
   new_box = newtuple = (box[0]+15,box[1]+15,box[2]-15,box[3]-15)
   im_processed = im.crop(new_box)
   im_array = np.array(im_processed.resize((28,28)))
   print(im_array)