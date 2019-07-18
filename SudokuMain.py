
import SudokuMatrix as SudokuMatrix
import NumbersOCR
from PIL import Image
import numpy as np
import DancingLinksX
import SudokuSolver

#test = NumbersOCR.NumbersOCR()
#test.train_ocr()

path_img = 'bin/Examples/2005.png'
#path_img= 'bin/sudo.jpg'

matrixTool = SudokuMatrix.SudokuMatrix()
grid_imcomplete = matrixTool.ImagetoGrid(path_img)
solverTool = SudokuSolver.SudokuSolver(grid_imcomplete)
solverTool.runSolver()
