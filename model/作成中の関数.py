import math
from scipy import optimize
import numpy as np
import random
import xlrd
import pandas as pd
import matplotlib.pyplot as plt


def sinin(alpha, syudan, v_2d, n) :
    #それぞれのエージェントがお互いの存在を視認
    #各エージェントに対し，距離が10未満の関数を採用
    syudan_ato = syudan + v_2d
    for i in range(n):
        #この処理で，各エージェントを中心としたxy座標に置き換えられる
        soutai = syudan_ato - syudan_ato[i]
        soutai_ireru = np.empty((0,2))
        #相対化した各エージェントと他の同志のの処理
        if (abs(soutai[i,0])**2 + abs(soutai[i,0])**2)**0.5 <= 10:
            for j in range(360):

            if
                soutai_hairu = np.array([soutai[i,0], soutai[i,1]])
            soutai_ireu = np.append(soutai_ireru, soutai_hairu, axis=0)