import math
from scipy import optimize
import numpy as np
import random
import xlrd
import pandas as pd
import matplotlib.pyplot as plt


#nは歩行者の数
n = 10

cars = np.array([[[5,6],
                  [5,5],
                  [1,5],
                  [1,6]]])
carNn = 1

x = 5

def fiw():
    fiw = 5
    for i in range(n):
        for j in range(carNn):

            if  x >= 10 and x <= 10:

                if y >= 0 and y <= 10:
                    fiw = 5000 * 9.8
