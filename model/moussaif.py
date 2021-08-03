import math
from scipy import optimize
import numpy as np
import random
import xlrd
import pandas as pd
import matplotlib.pyplot as plt

pi = math.pi


def fa_dasu(v_2d, syudan, n):
    # 第一のヒューリスティックに関する計算
    # 周囲のエージェントの存在を認知する
    fa_syudan = np.full(n, 10)
    syudan_ato = syudan + v_2d
    for i in range(n):
        #print("i", fa_syudan[i])
        soutai = syudan_ato - syudan_ato[i]
        #soutaiはsyudanから自分の位置を引いたも　and
        #print("soutai", soutai)
        for j in range(n):
            if soutai[j, 0] == 0 and soutai[j, 1] == 0:
                continue
            if abs(soutai[j,0]) <= 60 / 220 and abs(soutai[j,1]) <= 60 / 220:
                kyori = np.linalg.norm(soutai[j])

                #print("距離は",kyori)
                if kyori <= 10:
                    fa_syudan[i] = kyori

    return fa_syudan

def fa_dasukai(v_2d, syudan, n):
    # 第一のヒューリスティックに関する計算
    # 周囲のエージェントの存在を認知する
    fa_syudan = np.full(n, 10)
    syudan_ato = syudan + v_2d
    for i in range(n):
        #print("i", fa_syudan[i])
        soutai = syudan_ato - syudan_ato[i]
        #soutaiはsyudanから自分の位置を引いたも　and
        #print("soutai", soutai)


        for j in range(n):
            if soutai[j, 0] == 0 and soutai[j, 1] == 0:
                continue
            if abs(soutai[j,0]) <= 60/220 and abs(soutai[j,1]) <= 60/220:
                kyori = np.linalg.norm(soutai[j])
                #if kyori<=60/220 and
                #print("距離は",kyori)
                if kyori < 10:
                    fa_syudan[i] = kyori

    return fa_syudan


# 関数を変更位させるnumpyの配列に対応
def hulistics_1(fa, alpha0,n):
    # 目的関数
    Dmax = 10

    """def objective_function(theta, arufa):
        return (Dmax**2)+(fa**2)-(2*Dmax*fa*math.cos(arufa-theta))"""

    #alpha0 = alpha0.astype(np.float32)

    for i in range(n):
        # 歩行者の半径を考慮したものに
        def fufu(theta):
            return (Dmax ** 2) + (fa[i] ** 2) - (2 * Dmax * fa[i] * math.cos(alpha0[i] - theta))

        nagasa =(fa[i]**2 - (60/220)**2)**0.5
        #print("食べたい", nagasa)
        #print("nagasa", type(nagasa), "nagasa", nagasa)


        kakudo_gosa = np.arctan((60/220)/nagasa)
        #print("kakudo_gosa", kakudo_gosa)
        #print("dtype of fa, alpha0,n", type(alpha0), type(fa), type(kakudo_gosa))
        #print("alpha0とはいったい",alpha0[i])
        #alpha0[i] = alpha0.astype(np.float32)
        #min = optimize.fmin(fufu, (alpha0[i] - math.pi/2),(alpha0[i] + math.pi/2) )
        min1 = optimize.fminbound(fufu, alpha0[i] - math.pi/2, alpha0[i] - kakudo_gosa)
        min2 = optimize.fminbound(fufu, alpha0[i] + kakudo_gosa, alpha0[i] + math.pi/2)

        min_1 = alpha0[i] - abs(alpha0[i] - min1)
        min_2 = alpha0[i] - abs(alpha0[i] - min2)
        #print("min1", "min2", "min3", min1, min2, alpha0[i])
        if min_1 >= min_2:
            alpha0[i] = min1
        else:
            alpha0[i] = min2

    return alpha0


def cal_fij(n, syudan):
    # この関数は大幅に縮小できる気がする一応実装修了
    fij = np.zeros([n, 2])
    #print("fij", fij)
    for i in range(n):
        fij_i = np.zeros(2)
        soutai = syudan - syudan[i, :]
        #print("soutaiそうたい", soutai)
        #print("次は", soutai[i, :])
        dij = np.zeros(n)
        for i in range(n):
            dij[i] = np.linalg.norm(soutai[i, :])
        #print("距離は", dij)

        if dij[i] <= 60 / 220 and dij[i] > 0:
            nij = soutai / dij
            fij = 5000 * 9.8 * (60 / 220 + 60 / 220 - dij) * nij
            fij_i += fij
            #print("fijの", i, "番目は", fij_i)

        fij[i, :] += fij_i
    return fij


# 壁との接触する関数 車として考える

wall = np.zeros([4, 2])

for i in range(4):
    wall[i, 0] = 10 * random.random()
    wall[i, 1] = 10 * random.random()


# 人と壁の数が一致しないことに注意
# 壁の数をforループしていく流れにする

def cal_fiw(n, syudan):
    fiw = np.zeros([n, 2])
    for i in range(n):
        fiw_i = np.zeros(2)
        soutai = wall - syudan[i, :]
        diw = np.zeros(n)
        for i in range(n):
            diw[i] = np.linalg.norm(soutai[i, :])

        if diw[i] <= 60 / 220 and diw[i] > 0:
            niw = soutai / diw
            fiw = 5000 * 9.8 * (60 / 220 + 60 / 220 - diw) * niw
            fiw_i += fiw
            #print("fiwの", i, "番目は", fiw_i)

        fiw[i, :] += fiw_i
    return fiw


def dvdt(n, v_2d, alpha,fij):
    #この関数はつかわない
    #print("v_2dの説明",v_2d)
    dvdt = np.zeros([n, 2])

    for i in range(n):
        dvdt[i, 0] = (v_2d[i,0]-1.7*np.cos(alpha[i]))/0.5 + fij[i,0]

        #dvdt[i, 0] = (v_2d[i, 0] - 1.7 * np.cos(alpha(i))) / 0.5 + fij(i, 0) + fiw(i, 0)
        dvdt[i, 1] = (v_2d[i,1]-1.7*np.sin(alpha[i]))/0.5 + fij[i,1]
    v_2d += dvdt

    return v_2d

def dasu_v_1d(v_2d,v_1d,n):
    for i in range(n):
        v_1d[i] = np.linalg.norm(v_2d[i])
    return v_1d


