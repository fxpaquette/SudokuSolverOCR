#Iterer sur les centre des cellules de la grille
#Detecter s'il y a un objet dans la grille
#Si oui, identifier le caractere
#Si non, case vide

import numpy as np
from PIL import Image
import NumbersOCR as ocr
import matplotlib.pyplot as plt
import time

class SudokuMatrix:
    def __init__(self,**kwargs):
        self.ocr = ocr.NumbersOCR()
        self.ocr.decodeNN()
        #self.ocr = 9999

    def ImagetoGrid(self,image_path):
        img = Image.open(image_path).convert('L').resize((504,504))
        width = img.size[0]
        height = img.size[1]
        interval = int(width/9)
        semi_interval = int(interval/2)
        quart_interval = int(interval/3)
        #img = np.array(Image.open(image_path).convert('L').resize((width,height)))
        #plt.imshow(Image.open(image_path).convert('L'))
        output_matrix = np.zeros((9,9),dtype=np.int)
        print("Grille: ")
        for i in range(0,9):
            ma_string = ""
            for j in range(0,9):
                centrex = semi_interval + j*interval
                centrey = semi_interval + i*interval
                xinf = centrex-quart_interval
                xsup = centrex+quart_interval
                yinf = centrey-quart_interval
                ysup = centrey+quart_interval
                #sous_matrice = img[xinf:xsup,yinf:ysup]
                img_processed = img.crop((xinf,yinf,xsup,ysup))
                #sous_matrice = np.array(img_processed.resize((28,28)))
                #sous_matrice = np.array(img_processed.resize((28,28)).crop((0,tupley[0],27,tupley[1])).resize((28,28)))
                #print(sous_matrice)
                
                #Verifier si la case est vide
                sous_matrice = np.array(img_processed)
                liste_pixels_case = sous_matrice.flatten()
                valeur_moyenne = sum(liste_pixels_case)/len(liste_pixels_case)
                if valeur_moyenne >240: #La case est composee de pixels blancs (blanc = 255)
                    ma_string = ma_string + " x"
                    output_matrix[i,j] = 0
                else:
                    #La case n'est pas vide, on recadre l'image pour mieux l'analyser
                    bornes = self.fitNumber(sous_matrice)
                    #print("Bornes : ", bornes)
                    img_cropped = img_processed.crop(bornes)
                    width_cropped = img_cropped.size[0]
                    nouvelle_sous_matrice = np.array(img_cropped.resize((width_cropped,28)))
                    ##plt.imshow(img_cropped.resize((width_cropped,28)))
                    nouvelle_sous_matrice = self.ajusteLargeur(nouvelle_sous_matrice)
                    #print("Shape: ",nouvelle_sous_matrice.shape)
                    #plt.imshow(Image.fromarray(nouvelle_sous_matrice,'L'))
                    temps = str(time.time()).strip('.')
                    #Image.fromarray(nouvelle_sous_matrice,'L').save('data\\real\\'+temps+str(i)+str(j)+'.png')
                    num = self.ocr.analyse(nouvelle_sous_matrice)
                    ma_string = ma_string + " " + str(num)
                    output_matrix[i,j] = int(num)
                #plt.imshow(img_processed.resize((28,28)).crop((0,tupley[0],27,tupley[1])).resize((28,28)))
                #plt.imshow(img_processed.crop(bornes).resize((28,28)))
                #plt.imshow(img_processed.crop(bornes))
                #plt.imshow(img_processed.crop(bornes).resize((bornes[2]-bornes[0],28)))

                #print(sous_matrice)
                #print("centre x et y",centrex," ",centrey)
            print(ma_string)
        #print(output_matrix)
        return output_matrix
    
    def fitNumber(self,matrice):
        #print(matrice)
        width = matrice.shape[0]
        height = matrice.shape[1]
        percent = 0.3
        percent_height = 0.55
        yinf=0
        ysup=height
        found = False
        for j in range(0,int(percent_height*height)):
            if found:
                break
            for i in range(int(percent*width),int((1-percent)*width)):
                if matrice[j,i] < 200:
                    yinf = j
                    found=True
                    break
        found = False
        for j in range(height-1,int((1-percent_height)*height),-1):
            if found:
                break
            for i in range(int(percent*width),int((1-percent)*width)):
                #print("matrice[",i,",",j,"]",matrice[i,j])
                if matrice[j,i] < 200:
                    ysup = j
                    found = True
                    break
        xinf = 0
        xsup = width
        found = False
        percent_width=0.55
        for i in range(0,int(percent_width*width)):
            if found:
                break
            for j in range(int(percent*height),int((1-percent)*height)):
                #print("matrice[",j,",",i,"]",matrice[j,i])
                if matrice[j,i] < 200:
                    xinf = i
                    found = True
                    break
        found = False
        for i in range(width-1,int((1-percent_width)*width),-1):
            if found:
                break
            for j in range(int(percent*height),int((1-percent)*height)):
                #print("matrice[",j,",",i,"]",matrice[j,i])
                if matrice[j,i] < 200:
                    xsup = i
                    found = True
                    break
        #new_matrice = matrice[0:28,yinf:(ysup+1)]
        #print("Yinf,Ysup = ", yinf," , ",ysup)
        return (xinf-2,yinf,xsup+2,ysup)

    def ajusteLargeur(self,matrice):
        new_matrice = matrice
        width = matrice.shape[1]
        nb = 28-width
        #print("nb1 :",nb)
        while nb >0:
            #print("nb2 :",nb)
            new_matrice = np.insert(new_matrice, 0, 255, axis=1)
            nb-=1
            if nb>0:
                #print("nb3 :",nb)
                new_matrice = np.insert(new_matrice,new_matrice.shape[1],255,axis=1)
                nb-=1
        return new_matrice