
import SudokuMatrix as SudokuMatrix
import NumbersOCR
from PIL import Image
import numpy as np
import DancingLinksX
import SudokuSolver

#test = NumbersOCR.NumbersOCR()
#test.train_ocr()

path_img = 'bin/431.jpg'
path_img = 'bin/2003.png'

matrixTool = SudokuMatrix.SudokuMatrix()
grid_imcomplete = matrixTool.ImagetoGrid(path_img)
solverTool = SudokuSolver.SudokuSolver(grid_imcomplete)
solverTool.runSolver()

