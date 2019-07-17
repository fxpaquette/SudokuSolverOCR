# SudokuSolverOCR
NeuralNet.py: Used to train the OCR
NumbersOCR.py: Interface to use for numbers recognition
SudokuMatrix.py: Takes image of sudoku grid and returns a numpy array

DancingLinksX.py: Implements Knuth's Algorithm X with the "dancing nodes" data structure
SudokuSolver.py: Takes sudoku Array, converts the sudoku to an exact cover solvable problem, returns solution using DancingLinksX.py

SudokuMain.py: Takes hi-res image of sudoku, prints solution

neuralnet_saved_2.txt: stores weights for neural network (already trained)
