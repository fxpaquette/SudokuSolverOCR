#Iterer sur les centre des cellules de la grille
#Detecter s'il y a un objet dans la grille
#Si oui, identifier le caractere
#Si non, case vide

import numpy as np
from PIL import Image
import NumbersOCR as ocr
import matplotlib.pyplot as plt

class SudokuMatrix:
    def __init__(self,**kwargs):
        self.ocr = ocr.NumbersOCR()
        self.ocr.decodeNN()
        #self.ocr = 9999

    def ImagetoGrid(self,image_path):
        width = height = 378
        interval = int(width/9)
        semi_interval = int(interval/2)
        quart_interval = int(14)
        #img = np.array(Image.open(image_path).convert('L').resize((width,height)))
        img = Image.open(image_path).convert('L').resize((width,height))
        #plt.imshow(Image.open(image_path).convert('L'))
        for i in range(0,9):
            ma_string = ""
            for j in range(0,9):
                centrex = semi_interval + j*interval
                centrey = semi_interval + i*interval
                xinf = centrex-10
                xsup = centrex+9
                yinf = centrey-11
                ysup = centrey+12
                #sous_matrice = img[xinf:xsup,yinf:ysup]
                img_processed = img.crop((xinf,yinf,xsup,ysup))
                sous_matrice = np.array(img_processed.resize((28,28)))
                tupley = self.fitNumber(sous_matrice)
                #sous_matrice = np.array(img_processed.resize((28,28)).crop((0,tupley[0],27,tupley[1])).resize((28,28)))
                
                #print(sous_matrice)
                
                #Verifier si la case est vide
                liste_pixels_case = sous_matrice.flatten()
                valeur_moyenne = sum(liste_pixels_case)/len(liste_pixels_case)
                if valeur_moyenne >240: #La case est composee de pixels blancs (blanc = 255)
                    ma_string = ma_string + " x"
                else: 
                    ma_string = ma_string + " " + str(self.ocr.analyse(sous_matrice))
                #plt.imshow(img_processed.resize((28,28)).crop((0,tupley[0],27,tupley[1])).resize((28,28)))
                #plt.imshow(img_processed.resize((28,28)))
                #print(sous_matrice)
                #print("centre x et y",centrex," ",centrey)
            print(ma_string)
    
    def fitNumber(self,matrice):
        #print(matrice)
        yinf=0
        ysup=27
        found = False
        for j in range(0,6):
            if found:
                break
            for i in range(4,20):
                if matrice[j,i] < 200:
                    yinf = j
                    found=True
                    break
        found = False
        for j in range(27,20,-1):
            if found:
                break
            for i in range(4,20):
                #print("matrice[",i,",",j,"]",matrice[i,j])
                if matrice[j,i] < 200:
                    ysup = j
                    found = True
                    break
        #new_matrice = matrice[0:28,yinf:(ysup+1)]
        #print("Yinf,Ysup = ", yinf," , ",ysup)
        return (yinf,ysup)
