import numpy as np
import math
import os

# le nom de votre classe
# NeuralNet pour le modèle Réseaux de Neurones
# DecisionTree le modèle des arbres de decision

class NeuralNet: #nom de la class à changer

    def __init__(self,nb_couches,nb_neurones, **kwargs):
        self.nb_couches = nb_couches
        self.nb_neurones = nb_neurones
        
        
    def train(self, train, train_labels,nb_classes,learning_rate,nb_epoch):
        self.train = train
        self.train_labels = train_labels
        self.train_size = len(train)
        self.nb_class = nb_classes
        self.nb_attributs = len(train[0])

        self.const_apprent = learning_rate

        np.random.seed(20190505)
        self.liste_couches = []
        #Chauqe couche est une matrice numpy (les indices de ligne [i,] represente une neuronne
        #et les indices de colonne [,j] represente les connections aux neurone de la couche precedente)
        #Initialise la premiere couche cachee (celle qui est connectee aux attributs)
        self.liste_couches.append(0.05*np.random.randn(self.nb_neurones,self.nb_attributs))
        #Si plus grand que 3, initialise les couches cachees supplementaires
        if(self.nb_couches > 3):
            for i in range(1,self.nb_couches-2):
                self.liste_couches.append(0.05*np.random.randn(self.nb_neurones,self.nb_neurones))
        #Initilise la derniere couche
        if self.nb_class > 2: self.liste_couches.append(0.05*np.random.randn(self.nb_class,self.nb_neurones))
        else: self.liste_couches.append(0.05*np.random.randn(1,self.nb_neurones))
        #print("--------Poids initiaux : -------")
        #for couche in self.liste_couches:
         #   for i in range(0,len(couche)):
          #      print("Poids du neurone ",i," : ",couche[i])
        #print("----------------------------------")

        #Algorithme de retropropagation
        max_iter = nb_epoch
        nb_iter = 0
        while True:
            for t in range(0,self.train_size):
                #print(t)
                #Calcul les valeurs o, pour chaque neuronne, pour cet exemple (c'est la propagation avant)
                attributs = self.train[t]
                label = self.train_labels[t]
                if self.nb_attributs == 2:
                    label_vec = [label]
                else:
                    label_vec = []
                    for j in range(0,self.nb_attributs):
                        label_vec.append(int(label == j))
                noeuds_precedent = attributs
                liste_valeurs_o = []
                for i in range(0,self.nb_couches - 2):
                    valeurs_o = []
                    for j in range(0,self.nb_neurones):
                        valeurs_o.append(self.sigmoid(self.sommeprod(self.liste_couches[i][j,:],noeuds_precedent)))
                    liste_valeurs_o.append(valeurs_o)
                    noeuds_precedent = valeurs_o[:]
                #Calcul les valeurs de la couche de sortie
                if self.nb_class == 2 :
                    output = [self.sigmoid(self.sommeprod(self.liste_couches[-1][0],noeuds_precedent))]
                else:
                    output = []
                    for j in range(0,self.nb_class):
                        output.append(self.sigmoid(self.sommeprod(self.liste_couches[-1][j],noeuds_precedent)))
                liste_valeurs_o.append(output)
                
                #Calcul les deltas (propagation arriere)
                #On commence par calculer les deltas a la couche de sortie
                if self.nb_class == 2 :
                    delta_output = [output[0]*(1-output[0])*(label-output[0])]
                else:
                    delta_output = []
                    for j in range(0,self.nb_class):
                        delta_output.append(output[j]*(1-output[j])*(label_vec[j]-output[j]))
                deltas_precedents = delta_output
                liste_deltas=[deltas_precedents]
                #On commence par la couche qui vient juste avant celle de sortie, puis on iter par en arriere
                for i in range(self.nb_couches-3,-1,-1):
                    deltas = []
                    for j in range(0,len(liste_valeurs_o[i])):
                        valeur = liste_valeurs_o[i][j]
                        liste_w = self.liste_couches[i+1][:,j].tolist()
                        #print("--Liste_w : ",liste_w,"--")
                        #print(deltas_precedents)
                        deltas.append(valeur*(1-valeur)*self.sommeprod(liste_w,deltas_precedents))
                    liste_deltas.append(deltas)
                    deltas_precedents = deltas
                liste_deltas.reverse()
                #print("Liste valeurs: ",liste_valeurs_o)
                #print("Liste couches: ",self.liste_couches)
                #print("Liste delta:",liste_deltas)
                #Mise a jour des poids
                #Met les attributs dans la liste des valeurs o
                liste_valeurs_o = [attributs.tolist()]+liste_valeurs_o
               # print("Liste attribut et valeurs",liste_valeurs_o)
                for i in range(0,self.nb_couches-1):
                    #print("i = ",i)
                    #print("Taille matrice de a couche i ",np.size(self.liste_couches[i],1))
                    for j in range(0,np.size(self.liste_couches[i],0)):
                        #print("j = ", j)
                        for w in range(0,np.size(self.liste_couches[i],1)):
                            #print("w = ",w)
                            #print(self.liste_couches[i][j,w], " + ",self.const_apprent," * ",liste_valeurs_o[i][w]," * ",liste_deltas[i][j])
                            self.liste_couches[i][j,w] = self.liste_couches[i][j,w] + self.const_apprent*liste_valeurs_o[i][w]*liste_deltas[i][j]
                
                #print("--------Poids mis a jour : -------")
                #for couche in self.liste_couches:
                 #   for i in range(0,len(couche)):
                  #      print("Poids du neurone ",i," : ",couche[i])
                #print("----------------------------------")
            '''error = 0
            for i in range(0, self.train_size):
                exemple = self.train[i]
                label = self.train_labels[i]
                noeuds_precedent = exemple.tolist()
                for i in range(0,self.nb_couches - 2):
                    noeuds_nouveau = []
                    for j in range(0,self.nb_neurones):
                        noeuds_nouveau.append(self.sigmoid(self.sommeprod(self.liste_couches[i][j,:],noeuds_precedent)))
                    noeuds_precedent = noeuds_nouveau[:]
                output = self.sigmoid(self.sommeprod(self.liste_couches[-1][0],noeuds_precedent))
                error += (output-label)**2
            error = error/2'''
            nb_iter+=1
            print("Iteration: ",nb_iter)
            self.print_train_test()
            if (nb_iter >= max_iter):
                break
        self.print_train_test()
        print("Nombre d'iteration: ",nb_iter)
        
        #Encoder le reseau dans un fichier txt
        self.encode()


    def predict(self, exemple, label):
        noeuds_precedent = exemple.tolist()
        for i in range(0,self.nb_couches - 2):
            noeuds_nouveau = []
            for j in range(0,self.nb_neurones):
                noeuds_nouveau.append(self.sigmoid(self.sommeprod(self.liste_couches[i][j,:],noeuds_precedent)))
            noeuds_precedent = noeuds_nouveau[:]
        #Calcul valeurs a la sortie
        if self.nb_class == 2 :
            output = round(self.sigmoid(self.sommeprod(self.liste_couches[-1][0],noeuds_precedent)))
        else:
            output_vec = []
            for j in range(0,self.nb_class):
                output_vec.append(self.sigmoid(self.sommeprod(self.liste_couches[-1][j],noeuds_precedent)))
            output = output_vec.index(max(output_vec))
        label_real = label
        return(int(output), int(label_real))
    
    def test(self, test, test_labels):
        """
        """
    
    
    # Vous pouvez rajouter d'autres méthodes et fonctions,
    # il suffit juste de les commenter.

    def sigmoid(self,y):
        #print("Valeur y :", y)
        return 1/(1+math.exp(-y))
    
    def sommeprod(self,vec1,vec2):
        somme = 0
        for i in range(0,len(vec1)):
            somme += vec1[i]*vec2[i]
        #print("Somme de ",vec1," x ",vec2," = ",somme)
        return somme

    def print_train_test(self):
        "Classification"
        mat_confusion = np.zeros((self.nb_class,self.nb_class),dtype=int)
        for i in range(0, self.train_size):
            prediction = self.predict(self.train[i],self.train_labels[i])
            #print(mat_confusion)
            mat_confusion[prediction[1],prediction[0]]+=1
        "Traitement des resultats"
        exactitude = np.sum(mat_confusion.diagonal())/np.sum(mat_confusion)
        print()
        print("Traitement des resultats - Entrainement")
        print("----------------------------------------")
        print("Matrice de confusion : ")
        #print(mat_confusion)
        a_str = np.array2string(mat_confusion, precision=0, separator=' ', max_line_width=25)
        print(' ' + a_str[1:-1])
        #print("----------------------------------------")
        print("Exactitude = ",round(exactitude,2))
        print("----------------------------------------")
    
    def encode(self):
        nn_file = open('neuralnet_saved_3.txt','w')
        #Premiere ligne: nb d'attributs
        #Deuxieme ligne: nb de classes
        nn_file.write(str(self.nb_attributs)+os.linesep)
        nn_file.write(str(self.nb_class)+os.linesep)
        for couche in self.liste_couches:
            my_string = ""
            for i in range(couche.shape[0]):
                for j in range(couche.shape[1]):
                    my_string = my_string + " " + str(couche[i,j])
            nn_file.write(my_string+os.linesep)
        nn_file.close()
    
    def decode(self):
        nn_file = open('neuralnet_saved_3.txt','r')
        list_lines = nn_file.readlines()
        self.nb_attributs = int(list_lines[0])
        self.nb_class = int(list_lines[2])
        self.liste_couches = []
        liste_couche1 = list_lines[4].split()
        self.liste_couches.append(np.zeros((self.nb_neurones,self.nb_attributs)))
        #Premiere couche
        compteur = 0
        for i in range(self.nb_neurones):
            for j in range(self.nb_attributs):
                self.liste_couches[0][i,j] = float(liste_couche1[compteur])
                compteur+=1
        if self. nb_couches > 3:
            for k in range(1,self.nb_couches-2):
                liste_couchek = list_lines[2*k+4].split()
                self.liste_couches.append(np.zeros((self.nb_neurones,self.nb_neurones)))
                compteur = 0
                for i in range(self.nb_neurones):
                    for j in range(self.nb_neurones):
                        print("Compteur = ",compteur," Longueur = ",len(liste_couchek))
                        self.liste_couches[k][i,j] = float(liste_couchek[compteur])
                        compteur+=1
        #Derniere couche
        liste_couchek = list_lines[-2].split()
        nb_classes_temp = 1
        if self.nb_class >2: nb_classes_temp = self.nb_class
        self.liste_couches.append(np.zeros((nb_classes_temp,self.nb_neurones)))
        compteur = 0
        for i in range(nb_classes_temp):
            for j in range(self.nb_neurones):
                self.liste_couches[-1][i,j] = float(liste_couchek[compteur])
                compteur+=1
        nn_file.close()
