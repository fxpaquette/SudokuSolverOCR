
import SudokuMatrix as SudokuMatrix
import NumbersOCR
from PIL import Image
import numpy as np
import DancingLinksX
import SudokuSolver

#test = NumbersOCR.NumbersOCR()
#test.train_ocr()
#test.nn.decode()
#test.nn.liste_couches


#path_img = 'bin/test.PNG'
path_img = 'bin/431.jpg'
path_img = 'bin/2003.png'
#path_img = 'bin/train/train2.jpg'

matrixTool = SudokuMatrix.SudokuMatrix()
grid_imcomplete = matrixTool.ImagetoGrid(path_img)
solverTool = SudokuSolver.SudokuSolver(grid_imcomplete)
solverTool.runSolver()


#test.nn.liste_couches

#test_image = np.array(Image.open(path_img).convert('L').resize((504,504)))
#for i in range(0,504):
#	print(test_image[i])

