#Prendre une matrice sudoku 9x9 incomplete en entree
#La transformer en matrice de contrainte exact cover 729x324
#Obtenir la solution avec DLX
#Lire la solution pour sortir un matrice sudoku 9x9 complete

import math
import numpy as np
import DancingLinksX as DLX

class SudokuSolver:
    def __init__(self,grille):
        self.grille = grille
    def generateMatrix(self):
        self.matrice = np.zeros((729,324),dtype = np.int)
        for row in range(9):
            for col in range(9):
                rows_start = (row*81 + col*9)
                rows_end = rows_start + 9
                range_rows = range(rows_start,rows_end)
                #Row-Column Constraint
                cols_start = row*9 + col
                self.matrice[rows_start:rows_end,cols_start] = 1
                #Row-Number Constraints
                cols_start = 81+row*9
                for i in range(0,9):
                    self.matrice[range_rows[i],cols_start+i] = 1
                #Column-Number Constraints
                cols_start = 162+col*9
                for i in range(0,9):
                    self.matrice[range_rows[i],cols_start+i] = 1
                #Box-Number Constraints
                box = self.getBox(row,col)
                cols_start = 243+box*9
                for i in range(0,9):
                    self.matrice[range_rows[i],cols_start+i] = 1
        for row in range(9):
            for col in range(9):
                val = self.grille[row,col]
                if(val != 0):
                    rows_start = (row*81 + col*9)
                    rows_end = rows_start + 9
                    range_rows = range(rows_start,rows_end)
                    #Row-Column Constraint
                    #Toute les rows correspondant a la cellule sont mise a 0, sauf pour la valeur
                    for i in range(1,10):
                        if (i!=val):
                            self.matrice[rows_start+i-1,:] = 0
                    #Row-Number Constraints
                    cols_start = 81+(row*9)+val-1
                    self.matrice[:,cols_start] = 0
                    self.matrice[rows_start+val-1,cols_start]=1
                    #--------------------------------------------
                    rows_start_2 = row*81 + val-1
                    for i in range(0,9):
                        if (col != i):
                            self.matrice[rows_start_2 + i*9,:] = 0
                    #Column-Number Constraints
                    cols_start = 162+(col*9)+val-1
                    self.matrice[:,cols_start] = 0
                    self.matrice[rows_start+val-1,cols_start] = 1
                    #--------------------------------------------
                    rows_start_2 = col*9 + val -1
                    for i in range(0,9):
                        if (row != i):
                            self.matrice[rows_start_2 + i*81,:] = 0
                    #Box-Number Constraints
                    box = self.getBox(row,col)
                    cols_start = 243+box*9+val-1
                    self.matrice[:,cols_start] = 0
                    self.matrice[rows_start+val-1,cols_start] = 1
    
    def runSolver(self):
        self.generateMatrix()
        #print(self.matrice)
        solver = DLX.DancingLinks(self.matrice)
        rows_solution = solver.runDLX()
        sol = self.convertSolutionRows(rows_solution)
        #print(sol)
        self.printSol(sol)
    
    def getBox(self,row,col):
        return (math.floor(row/3)*3)+math.floor(col/3)
    
    def convertSolutionRows(self,rows):
        output_matrix = np.zeros((9,9),dtype=np.int)
        for row_sol in rows:
            row = row_sol//81
            col = (row_sol%81)//9
            num = (row_sol%81)%9 + 1
            output_matrix[row,col] = num
        return output_matrix
    def printSol(self,mat):
        print("")
        print("Solution:")
        for i in range(0,9):
            #print("______________________________________")
            string = ""
            for j in range(0,9):
                string += " " + str(mat[i,j])
            print(string)



#Tests#
#grille_test=np.zeros((9,9))
#solver_test = SudokuSolver(grille_test)
#solver_test.generateMatrix()
#np.savetxt("exactcover.csv", solver_test.matrice, delimiter=",")
#print(solver_test.matrice)