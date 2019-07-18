import numpy as np

class OneNode:
    def __init__(self,columnNode = None,row = None):
        self.r= self
        self.l = self
        self.u = self
        self.d = self

        self.row = row

        self.c = columnNode

    def setRight(self,rightNode):
        rightNode.r = self.r
        rightNode.r.l = rightNode
        self.r = rightNode
        rightNode.l = self
        return rightNode
    def setDown(self,downNode):
        #if(self.c != downNode.c)
        downNode.d = self.d
        downNode.d.u = downNode
        self.d = downNode
        downNode.u = self
        return downNode
    def detachLR(self):
        self.l.r=self.r
        self.r.l =self.l
    def reattachLR(self):
        self.l.r = self.r.l = self
    def detachUD(self):
        self.u.d = self.d
        self.d.u = self.u
    def reattachUD(self):
        self.u.d = self.d.u = self

class ColumnNode(OneNode):
    def __init__(self,nom):
        super().__init__(columnNode = self)
        self.size = 0
        self.name = nom
    
    def cover(self):
        self.detachLR()
        i = self.d
        while(i != self):
            j = i.r
            while (j != i):
                j.detachUD()
                j.c.size-=1
                j = j.r
            i = i.d
        ##
    
    def uncover(self):
        i = self.u
        while(i != self):
            j = i.l
            while(j != i):
                j.c.size+=1
                j.reattachUD()
                j = j.l
            i = i.u
        self.reattachLR()
        ##

class DancingLinks:
    def __init__(self,matrice):
        self.solutions = 0
        self.answer = []
        self.header = self.makeNodes(matrice)
    
    def search(self,k):
        #S'il n'y a plus de colonne
        if (self.header.r == self.header):
            #print("Solution trouvee")
            #Traiter le resultat
            #print(self.storeSolutionDefault())
            self.solutions+=1
            return
        else:
            #print("Nb solutions ", self.solutions)
            c = self.selectColumn()
            c.cover()
            x=c.d
            while(x!=c):
                self.answer.append(x)
                #print(self.answer)
                j=x.r
                while(j!=x):
                    j.c.cover()
                    j=j.r
                self.search(k+1)
                #
                if (self.solutions >0):
                    return
                #
                x=self.answer[-1]
                self.answer = self.answer[:-1]
                #print(self.answer)

                c = x.c
                
                j=x.l
                while(j!=x):
                    j.c.uncover()
                    j=j.l
                x=x.d
            c.uncover()
    
    def selectColumn(self):
        min_val = 100000
        colonne = None
        c = self.header.r
        while(c!=self.header):
            if c.size < min_val:
                min_val = c.size
                colonne = c
            c = c.r
        return colonne
    
    def makeNodes(self,matrice):
        nbRows = matrice.shape[0]
        nbCols = matrice.shape[1]
        header = ColumnNode(nom = "header")

        listColumnNodes = []
        for i in range(nbCols):
            n = ColumnNode(nom=str(i))
            listColumnNodes.append(n)
            header = header.setRight(n) #header sert de variable pour conserver la node precedent dans la boucle
        #Durant la boucle le r de header reste toujours le header original donc on ne le perd pas
        #On le reassigne a la fin de la boucle
        header = header.r.c
        for i in range(nbRows):
            prev = None
            for j in range(nbCols):
                if (matrice[i,j] == 1):
                    col = listColumnNodes[j]
                    newNode= OneNode(col,i)
                    if (prev == None):
                        prev = newNode
                    col.u.setDown(newNode) #Car le u de col est le dernier element de la colonne, on met newNode a la suite de ce dernier element
                    prev = prev.setRight(newNode)
                    col.size+=1
        header.size= nbCols
        return header
    
    def runDLX(self):
        self.search(0)
        #if self.solutions>0:
            #print(self.getSolutionDefault())
        return self.getSolutionDefault()
    
    def getSolutionDefault(self):
        solution = []
        rows = []
        for node in self.answer:
            temp = []
            row_temp = []
            row_temp.append(node.row)
            temp.append(node.c.name)
            rnode = node.r
            while (rnode != node):
                temp.append(rnode.c.name)
                #row_temp.append(rnode.row)
                rnode = rnode.r
            #print(temp)
            #rows.append(row_temp)
            rows.append(node.row)
            solution.append(temp[:])
        #print("Rows: ",rows)
        return rows
    
    def printMatrix(self):
        print("----------------------------")
        temp1 = self.header.r
        while(temp1 != self.header):
            print("----Colonne----")
            temp2 = temp1.d
            while(temp2 != temp1):
                my_string = ""
                my_string+= temp2.c.name + " --> "
                temp3 = temp2.r
                while(temp3!=temp2):
                    my_string+=temp3.c.name+" --> "
                    temp3 = temp3.r
                print(my_string)
                temp2 = temp2.d
            temp1 = temp1.r

#matrice_test = np.array([[1,0,0,1,0,0,1],[1,0,0,1,0,0,0],[0,0,0,1,1,0,1],[0,0,1,0,1,1,0],[0,1,1,0,0,1,1],[0,1,0,0,0,0,1]])
#solver_test = DancingLinks(matrice_test)
#solver_test.printMatrix()
#solver_test.runDLX()






