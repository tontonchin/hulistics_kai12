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
        print("soutai",soutai)
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

def fa_car(alpha0, syudan, n , cars, n_cars):
     # cars は一つの始点(xcar, ycar)をもとにした三次元配列
     #ところどころで参照する配列の位置が間違えている
    pi = math.pi
    print("fa_carのためのalpha0",alpha0)
    fa_syucar = np.full(n,10.00)
    l_abc = np.zeros((n, 4, 3))
    fa_abc = np.zeros((n, 3))
    for j in range(n_cars):
        if cars[j,0,0] == cars[j, 1, 0] :
            #一つ目の式
            l_abc[j, 0, 0] = 1 / cars[j, 0, 0]
            l_abc[j, 0, 2] = -1
            #二つ目の式
            l_abc[j , 1, 1] = 1 / cars[j , 1, 1]
            l_abc[j , 1, 2] = -1
            #３つめのしき
            l_abc[j, 2, 0] = 1 / cars[j, 2, 0]
            l_abc[j, 2, 2] = -1
            #４つめのしき
            l_abc[j , 3, 1] = 1 / cars[j , 3, 1]
            l_abc[j , 3, 2] = -1
        else:
            #1
            l_abc[j, 0, 0] = cars[j, 0, 1] - cars[j, 1, 1]
            l_abc[j, 0, 1] = -cars[j, 0, 0] + cars[j, 1, 0]
            l_abc[j, 0, 2] = -cars[j, 0, 1] * cars[j, 1, 0]
            #2
            l_abc[j, 1, 0] = cars[j, 1, 2] - cars[j, 2, 2]
            l_abc[j, 1, 1] = -cars[j, 1, 1] + cars[j, 2, 1]
            l_abc[j, 1, 2] = -cars[j, 1, 2] * cars[j, 2, 1]
            #3
            l_abc[j, 2, 0] = cars[j, 2, 3] - cars[j, 3, 3]
            l_abc[j, 2, 1] = -cars[j, 2, 2] + cars[j, 3, 2]
            l_abc[j, 2, 2] = -cars[j, 2, 3] * cars[j, 3, 2]
            #4
            l_abc[j, 3, 0] = cars[j, 3, 0] - cars[j, 0, 0]
            l_abc[j, 3, 1] = -cars[j, 3, 3] + cars[j, 0, 3]
            l_abc[j, 3, 2] = -cars[j, 3, 0] * cars[j, 0, 3]

    for i in range(n):
        #それぞれの歩行者エージェントが自動車に対してもつfa
        #forループによってnum_carについてのループも行ったほうがいいのではないか
        for k in range(n_cars):

            fa_car_kouho = 10
            #集団は進行方向aをもち，関数になる
            if alpha0[i] == 0 or alpha0[i] == 2 * pi:
                fa_abc[i, 0] = 1/syudan[i,0]
                fa_abc[i, 2] = -1
                if syudan[i, 1] >= cars[k, 0, 1] and syudan[i, 1] <= cars[k, 1, 1]:
                    fa_car_kouho =  abs(syudan[i,0] - cars[k,2,0])
            elif alpha0[i] == pi/2:
                fa_abc[i, 1] = 1/syudan[i,1]
                fa_abc[i, 2] = -1
                print("要チェック",cars[k,1,0])
                if syudan[i, 0] >= cars[k, 0, 0] and syudan[i, 0] <= cars[k, 3, 0]:
                    fa_car_kouho = abs(syudan[i,1] - cars[k,1,1])

            elif alpha0[i] == pi :
                #下二つは間違えている可能性あり
                fa_abc[i, 0] = 1/syudan[i,0]
                fa_abc[i, 2] = -1
                if syudan[i, 1] >= cars[k, 0, 1] and syudan[i, 0] <= cars[k, 1, 1]:
                    fa_car_kouho = abs(syudan[i,0] - cars[k,2,0])
            elif alpha0[i] == 3*(pi/2) :
                print("syudan[i,1]",syudan[i,1])
                fa_abc[i, 1] = 1/syudan[i,1]
                fa_abc[i, 2] = -1
                print("要チェック",cars[k,3,0])
                if syudan[i, 0] >= cars[k, 0, 0] and syudan[i, 0] <= cars[k, 3, 0]:
                    fa_car_kouho = abs(syudan[i,1] - cars[k,3,0])
            else:
                for k in range(4):
                    #forのそれぞれの式に対してのfaを求める
                    fa_abc[i,0] = math.tan(alpha0[i])
                    fa_abc[i,1] = -1
                    fa_abc[i,2] = -math.tan(alpha0[i])*syudan[i,0] + syudan[i,1]
                    kouten_sita = (l_abc[i,k,0] * fa_abc[i,1]) - (fa_abc[i,0] * l_abc[i,k,1])
                    print("kouten_sita",kouten_sita, print(alpha0))
                    kouten_x = ((l_abc[i,k,1] * fa_abc[i,2]) - (fa_abc[i,1] - l_abc[i,k,2] ) )/ kouten_sita
                    kouten_y = ((fa_abc[i, 0] * l_abc[i,k,2]) - (l_abc[i,k,0] *fa_abc[i,2] ) )/ kouten_sita
                    if cars[0,1,0] >= kouten_x and cars[0,2,0] <= kouten_x:
                        #print("確認",cars[k,1,0])
                        #print("確認",cars[k,2,0])
                        if kouten_y <= cars[0,0,1] and kouten_y >= cars[0,1,1]:
                            d =((kouten_x - syudan[i,0])**2 + (kouten_y - syudan[i,1])**2)**0.5
                            print("NaNになるかもしれない",d)
                            if d <= fa_car_kouho:
                                fa_car_kouho = d
            print("faの候補",fa_car_kouho)
            fa_syucar[i] = fa_car_kouho
        print("fa_kouhoについて",fa_syucar)
    return fa_syucar




def fa_dasukai(v_2d, syudan, n):
    # 第一のヒューリスティックに関する計算
    # 周囲のエージェントの存在を認知する
    fa_syudan = np.full(n, 10.00)
    syudan_ato = syudan + v_2d
    for i in range(n):
        #print("i", fa_syudan[i])
        #soutai = syudan_ato - syudan_ato[i]
        soutai = syudan - syudan[i]
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

def fa_kekka( n,fa_syudan,fa_syucar):
    # fa_syudan, fa_carの代償比較
    fa_hontou = np.full(n,10.00)
    for i in range(n):
        if fa_syudan[i] <= fa_syucar[i]:
            fa_hontou[i] = fa_syudan[i]
            fa_hontou[i] = round(fa_hontou[i], 2)
        else:
            fa_hontou[i] = fa_syucar[i]
            fa_hontou[i] = round(fa_hontou[i], 2)

        if fa_hontou[i] == 0:
            fa_hontou[i] = 0.5
            fa_hontou[i] = round(fa_hontou[i], 2)

    return fa_hontou




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

        kakudo_gosa = np.arctan((60/220)/nagasa)

        min1 = optimize.fminbound(fufu, alpha0[i] - math.pi/2, alpha0[i] - kakudo_gosa)
        min2 = optimize.fminbound(fufu, alpha0[i] + kakudo_gosa, alpha0[i] + math.pi/2)

        min_1 = alpha0[i] - abs(alpha0[i] - min1)
        min_2 = alpha0[i] - abs(alpha0[i] - min2)
        #print("min1", "min2", "min3", min1, min2, alpha0[i])
        if min_1 >= min_2:
            alpha0[i] = min1
        else:
            alpha0[i] = min2
        alpha0[i] = round(alpha0[i], 2)
    return alpha0


def cal_fij(n, syudan):
    # この関数は大幅に縮小できる気がする一応実装修了
    fij = np.zeros([n, 2])
    #print("fij", fij)
    for i in range(n):
        fij_i = np.zeros(2)
        soutai = syudan - syudan[i, :]
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
            fiw = 5000 * 9.8 * ( 60 / 220 - diw) * niw
            fiw_i += fiw
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
    v_2d = round(v_2d, 2)

    return v_2d

def dasu_v_1d(v_2d,v_1d,n):
    for i in range(n):
        v_1d[i] = np.linalg.norm(v_2d[i])
    return v_1d

def alpha_dasu(vx, vy):
    if vx ==0 :
        if vy >= 0:
            alpha = (math.pi)/2
        else:
            alpha = 3*(math.pi)/2
    elif vy ==0:
        if vx >= 0:
            alpha = 0
        else:
            alpha = math.pi
    else :
        alpha = math.atan(vy/vx)
    alpha = round(alpha, 2)
    return alpha

