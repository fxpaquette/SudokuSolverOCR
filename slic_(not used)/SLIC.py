import math
import numpy as np


class SLIC:
    def __init__(self, image, nb_segments, compactness,max_iter, **kwargs):
        self.image = image #Matrice numpy de tuple RGB
        self.k = nb_segments #int
        self.m = compactness #int
        self.N = image.shape[0]*image.shape[1] #Nombre de pixels
        self.width = image.shape[0]
        self.height = image.shape[1]
        self.S = int(math.sqrt(self.N/self.k)) #step size
        self.half_step = int(self.S/2)
        self.MAX_ITER = max_iter

        #Appel pour convetir l'image en lab
        self.image_rgb2lab()

    def computeSuperPixels(self):
        #Appel pour initialiser les centroides
        self.init_centroides()
        for itr in range(self.MAX_ITER):
            self.distances = 1000000*np.ones(self.lab_img.shape[:2])
            for c in range(len(self.centres)):
                centre_c = self.centres[c]
                #Determine les coins inferieurs et superierus de la region 2Sx2S autour du centre
                xinf = max(0,centre_c[3]-self.S)
                xsup = min(self.width,centre_c[3]+self.S)
                yinf = max(0,centre_c[4]-self.S)
                ysup = min(self.height,centre_c[4]+self.S)
                #print("centre",centre_c[4],"step :",self.S)
                #print("ysup",ysup)
                
                #Calcul en batch la distance entre les pixels labxy de la region et le centre
                region_lab = self.lab_img[xinf:xsup,yinf:ysup]
                diff_lab = region_lab-self.lab_img[centre_c[3],centre_c[4]]
                dist_lab = np.sqrt(np.sum(np.square(diff_lab), axis=2))

                xx, yy = np.ogrid[xinf : xsup, yinf : ysup] #Deux array de suite xinf,xinf+1,...xsup-1 et yinf,yinf+1,...ysup-1
                dist_xy = np.sqrt((xx-centre_c[3])**2 + (yy-centre_c[4])**2)
                new_dist = dist_lab + dist_xy * self.m/self.S

                #Compare les distances avec les distances actuelles et les actualise
                distance_region = self.distances[xinf:xsup,yinf:ysup]
                index = new_dist < distance_region
                distance_region[index] = new_dist[index]
                self.distances[xinf:xsup,yinf:ysup] = distance_region
                self.mat_cluster[xinf:xsup,yinf:ysup][index] = c
            
            #Recalcule les centres des clusters (moyenne des composantes labxy)
            centre_comptes = []
            for c in range(len(self.centres)):
                self.centres[c][0] = self.centres[c][1] = self.centres[c][2] = self.centres[c][3] = self.centres[c][4] = 0
                centre_comptes.append(0)
            for i in range(0,self.image.shape[0]):
                for j in range(0,self.image.shape[1]):
                    cluster_id = self.mat_cluster[i,j]
                    if cluster_id != -1:
                        self.centres[cluster_id][0]+=self.lab_img[i,j][0]
                        self.centres[cluster_id][1]+=self.lab_img[i,j][1]
                        self.centres[cluster_id][2]+=self.lab_img[i,j][2]
                        self.centres[cluster_id][3]+=i
                        self.centres[cluster_id][4]+=j

                        centre_comptes[cluster_id]+=1
            for c in range(len(self.centres)):
                self.centres[c][0] = int(self.centres[c][0]/centre_comptes[c])
                self.centres[c][1] = int(self.centres[c][1]/centre_comptes[c])
                self.centres[c][2] = int(self.centres[c][2]/centre_comptes[c])
                self.centres[c][3] = int(self.centres[c][3]/centre_comptes[c])
                self.centres[c][4] = int(self.centres[c][4]/centre_comptes[c])
    
    #Verifie que les pixels proches n'appartiennent pas a des cluster trop disparate
    #Ajuste les cluster
    def renforceConnectivite(self):
        cluster_label = 0
        cluster_label_adj = 0
        threshold = int(self.width*self.height/self.k)
        voisinage = [(-1,0),(1,0),(0,1),(0,-1)]
        new_mat_cluster = -1*np.ones(self.lab_img.shape[:2],dtype=int)
        elements = []
        for i in range(0,self.image.shape[0]):
            for j in range(0,self.image.shape[1]):
                if new_mat_cluster[i,j] == -1:
                    elements = []
                    elements.append((i,j))
                    for d in voisinage:
                        x=elements[0][0]+d[0]
                        y=elements[0][1]+d[1]
                        if x>=0 and x<self.width and y>=0 and y<self.height and new_mat_cluster[x,y]>=0: #Si pas en dehorsh de l'image
                            cluster_label_adj = new_mat_cluster[x,y]
                count = 1
                c = 0
                while c < count:
                    for d in voisinage:
                        x=elements[c][0]+d[0]
                        y=elements[c][1]+d[1]
                        if x>=0 and x<self.width and y>=0 and y<self.height:
                            if (new_mat_cluster[x,y] == -1 and self.mat_cluster[i,j] == self.mat_cluster[x,y]):
                                elements.append((x, y))
                                new_mat_cluster[x,y] = cluster_label
                                count+=1
                    c+=1
                if (count <= threshold >> 2):
                    for c in range(count):
                        new_mat_cluster[elements[c]] = cluster_label_adj
                    cluster_label-=1
                cluster_label+=1
        self.mat_cluster = new_mat_cluster
                        

    def addContours(self,colorvec):
        pixels_autour = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)] #Coordonnees relatives des 8 pixels qui touchent a un pixel particulier
        estContour = np.zeros(self.lab_img.shape[:2],dtype=np.bool)
        posContour = []
        for i in range(0,self.image.shape[0]):
            for j in range(0,self.image.shape[1]):
                count = 0
                for d in pixels_autour: #iter sur les 8 pixels autour
                    x = i + d[0]
                    y = j + d[1]
                    if x>=0 and x<self.width and y>=0 and y<self.height: #Si pas en dehorsh de l'image
                        if (estContour[x,y] == False and self.mat_cluster[i,j] != self.mat_cluster[x,y]):
                            count+=1
                if count >=2:
                    estContour[i,j] = True
                    posContour.append((i,j))
        for pixel in posContour:
            self.image[pixel[0],pixel[1]] = colorvec
        return self.image

    def rgb2lab(self, vec_couleur):
        r = vec_couleur[0]/255
        g = vec_couleur[1]/255
        b = vec_couleur[2]/255

        r = math.pow((r + 0.055) / 1.055, 2.4) if (r > 0.04045) else (r / 12.92)
        g = math.pow((g + 0.055) / 1.055, 2.4) if (g > 0.04045) else (g / 12.92)
        b = math.pow((b + 0.055) / 1.055, 2.4) if (b > 0.04045) else (b / 12.92)

        x = (r * 0.4124 + g * 0.3576 + b * 0.1805) / 0.95047
        y = (r * 0.2126 + g * 0.7152 + b * 0.0722) / 1.00000
        z = (r * 0.0193 + g * 0.1192 + b * 0.9505) / 1.08883

        x = math.pow(x, 1/3) if (x>0.008856) else ((7.787 * x) + 16/116)
        y = math.pow(y, 1/3) if (y>0.008856) else ((7.787 * y) + 16/116)
        z = math.pow(z, 1/3) if (z>0.008856) else ((7.787 * z) + 16/116)

        return ((116 * y) - 16, 500 * (x - y), 200 * (y - z))
    
    def image_rgb2lab(self):
        self.lab_img = np.copy(self.image)
        for i in range(0,self.image.shape[0]):
            for j in range(0,self.image.shape[1]):
                self.lab_img[i,j] = self.rgb2lab(tuple(self.image[i,j]))
    
    def init_centroides(self):
        self.mat_cluster = -1*np.ones(self.lab_img.shape[:2],dtype=int) #Matrice de forme LargeurxHauteur (Donne le cluster pour chaque pixel)
        self.centres = []
        for i in range(self.half_step,self.width,self.S):
            for j in range(self.half_step,self.height,self.S):
                pos = self.findClusterPosInArea((i,j))
                couleur = self.lab_img[pos[0],pos[1]]
                centre = [couleur[0],couleur[1],couleur[2],pos[0],pos[1]]
                self.centres.append(centre[:])
                #print("i,j = ",i," , ",j)

    def distance(self, labxy1,labxy2):
        dlab = math.pow(labxy2[0]-labxy1[0],2) + math.pow(labxy2[1]-labxy1[1],2) + math.pow(labxy2[2]-labxy1[2],2)
        dlab = math.sqrt(dlab)

        dxy = math.pow(labxy2[3]-labxy1[3],2) + math.pow(labxy2[4]-labxy1[4],2)
        dxy = math.sqrt(dxy)

        return dlab + (self.m/self.S)*dxy
    
    def l2norm(self,vec):
        somme = 0
        for i in range(0,len(vec)):
            somme += vec[i]**2
        return somme**0.5

    def l2norm2(self,vec):
        somme = 0
        for i in range(0,len(vec)):
            somme += vec[i]**2
        return somme

    def sous_tuple(self,vec1,vec2):
        return (vec1[0]-vec2[0],vec1[1]-vec2[1],vec1[2]-vec2[2])

    def findClusterPosInArea(self,center):
        pos = center
        min_gradient = 1000000
        for i in range(center[0]-1,center[0]+2):
            for j in range(center[1]-1,center[1]+2):
                c1 = self.lab_img[i+1,j]
                c2 = self.lab_img[i-1,j]
                c3 = self.lab_img[i,j+1]
                c4 = self.lab_img[i,j-1]
                gradient = self.l2norm2(self.sous_tuple(c1,c2)) + self.l2norm2(self.sous_tuple(c3,c4))
                if gradient < min_gradient:
                    min_gradient = gradient
                    pos = (i,j)
        #print("pos : ",pos)
        return pos


