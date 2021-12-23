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
            #if abs(soutai[j,0]) <= 60 / 220 and abs(soutai[j,1]) <= 60 / 220:
            if ((soutai[j,0])**2 +(soutai[j,1])**2) **0.5 <= 60 / 220:
                kyori = np.linalg.norm(soutai[j])
                kyori = round(kyori,2)

                #print("距離は",kyori)
                if kyori <= 10:
                    fa_syudan[i] = round(kyori,2)


    return fa_syudan

def fa_car(alpha0, syudan, n , cars, n_cars):
     # cars は一つの始点(xcar, ycar)をもとにした三次元配列
     #ところどころで参照する配列の位置が間違えている
    pi = math.pi
    #print("fa_carのためのalpha0",alpha0)
    fa_syucar = np.full(n,10.00)
    l_abc = np.zeros((n_cars, 4, 3))
    fa_abc = np.zeros((n, 3))
    for j in range(n_cars):
        if cars[j,0,0] == cars[j, 1, 0] :
            #一つ目の式
            l_abc[j, 0, 0] = 1
            l_abc[j, 0, 2] = -cars[j,0,1]
            #二つ目の式
            l_abc[j , 1, 1] = 1
            l_abc[j , 1, 2] = -cars[j,1,1]
            #３つめのしき
            ireru = cars[j, 2, 0]
            if ireru == 0:
                ireru = ireru + 0.1
            l_abc[j, 2, 0] = 1
            l_abc[j, 2, 2] = -cars[j,2,0]
            #４つめのしき
            l_abc[j , 3, 1] = 1
            l_abc[j , 3, 2] = -cars[j,2,1]
        else:
            #1
            a = cars[j, 0, 1] - cars[j, 1, 1]
            b = -cars[j, 0, 0] + cars[j, 1, 0]
            c = (-cars[j, 1, 0] * cars[j, 0, 1]) + (cars[j, 0, 0] * cars[j, 1, 1])
            l_abc[j, 0, 0] = cars[j, 0, 1] - cars[j, 1, 1]

            l_abc[j, 0, 1] = -cars[j, 0, 0] + cars[j, 1, 0]
            l_abc[j, 0, 2] = (-cars[j, 1, 0] * cars[j, 0, 1]) + (cars[j, 0, 0] * cars[j, 1, 1])
            #2
            l_abc[j, 1, 0] = cars[j, 1, 1] - cars[j, 2, 1]
            l_abc[j, 1, 1] = -cars[j, 1, 0] + cars[j, 2, 0]
            l_abc[j, 1, 2] = (-cars[j, 2, 0] * cars[j, 1, 1]) + (cars[j, 1, 0] * cars[j, 2, 1])
            #3
            l_abc[j, 2, 0] = cars[j, 2, 1] - cars[j, 3, 1]
            l_abc[j, 2, 1] = -cars[j, 2, 0] + cars[j, 3, 0]
            l_abc[j, 2, 2] = (-cars[j, 3, 0] * cars[j, 2, 1]) + (cars[j, 2, 0] * cars[j, 3, 1])
            #4
            l_abc[j, 3, 0] = cars[j, 3, 1] - cars[j, 0, 1]
            l_abc[j, 3, 1] = -cars[j, 3, 0] + cars[j, 0, 0]
            l_abc[j, 3, 2] = (-cars[j, 0, 0] * cars[j, 3, 1]) + (cars[j, 3, 0] * cars[j, 0, 1])
        print("線の感じ",cars[j], l_abc)
    for i in range(n):
        #それぞれの歩行者エージェントが自動車に対してもつfa
        fa_car_kouho = 10
        #forループによってnum_carについてのループも行ったほうがいいのではないか
        for k in range(n_cars):

            ireruyatu = alpha0[i]
            #if ireruyatu < 0:
                #ireruyatu = 2*pi - ireruyatu
            #fa_car_kouho = 10

            if ireruyatu == pi/2:
                fa_abc[i, 1] = 1/syudan[i,1]
                fa_abc[i, 2] = -1
                #print("要チェック",cars[k,1,0])
                print("syudan[i, 0] >= cars[k, 0, 0] and syudan[i, 0] <= cars[k, 3, 0]",syudan[i, 0],cars[k, 0, 0],syudan[i, 0],cars[k, 3, 0])
                if syudan[i, 0] >= cars[k, 0, 0] and syudan[i, 0] <= cars[k, 3, 0]:
                    fa_car_kouho = abs(syudan[i,1] - cars[k,1,1])

            elif ireruyatu == 3*(pi/2) :
                #print("syudan[i,1]",syudan[i,1])
                fa_abc[i, 1] = 1/syudan[i,1]
                fa_abc[i, 2] = -1
                #print("要チェック",cars[k,3,0])
                if syudan[i, 0] >= cars[k, 0, 0] and syudan[i, 0] <= cars[k, 3, 0]:
                    fa_car_kouho = abs(syudan[i,1] - cars[k,3,1])
            else:
                for l in range(n_cars):
                    #forのそれぞれの式に対してのfaを求める 計算法の全てがわるい
                    fa_abc[i,0] = math.tan(ireruyatu)
                    fa_abc[i,1] = -1
                    fa_abc[i,2] = -math.tan(ireruyatu)*syudan[i,0] + syudan[i,1]
                    kouho = 10
                    fa_hako = np.array([10,10,10,10])
                    for m in range(4):
                        #print(i,"候補は更新されるのか",kouho)
                        """
                        if kouho < 10:
                            print(i,"候補は更新された",kouho)
                        """
                        kouten_sita = (l_abc[l,m,0] * fa_abc[i,1]) - (fa_abc[i,0] * l_abc[l,m,1])
                        #print("kouten_sita",kouten_sita, print(alpha0))

                        kouten_x = ((l_abc[l,m,1] * fa_abc[i,2]) - (fa_abc[i,1] - l_abc[l,m,2] ) )/ kouten_sita
                        kouten_x = round(kouten_x,2)
                        kouten_y = ((fa_abc[i, 0] * l_abc[l,m,2]) - (l_abc[l,m,0] *fa_abc[i,2] ) )/ kouten_sita
                        kouten_y = round(kouten_y,2)
                        d =((kouten_x - syudan[i,0])**2 + (kouten_y - syudan[i,1])**2)**0.5
                        print("線と車までの距離",d,syudan[i])
                        if cars[j,0,0] >= kouten_x and cars[j,3,0] <= kouten_x:
                        #print("確認",cars[k,1,0])
                        #print("確認",cars[k,2,0])

                            if kouten_y <= cars[k,0,1] and kouten_y >= cars[k,1,1]:
                                d =((kouten_x - syudan[i,0])**2 + (kouten_y - syudan[i,1])**2)**0.5
                                fa_hako[l] = d
                                print("syudan",syudan[i])
                                if not kouten_y == 25:
                                    print("交点に対する考察",kouten_x)
                                print("kouten_y <= cars[k,0,1] and kouten_y >= cars[k,1,1]",cars[k,0,1],kouten_y,cars[k,1,1],cars[k,1,0],kouten_x,cars[k,2,0])
                                #print("更新される候補d",d)
                            #print("NaNになるかもしれない",d)
                                if d <= fa_car_kouho:
                                    fa_car_kouho = d
                                    fa_car_kouho = round(fa_car_kouho, 2)

                                    if fa_car_kouho < 10:
                                        print("車までのきょりきょり",fa_car_kouho)
                        print(l,"番目の",fa_car_kouho,"fa_car候補")

            #print("faの候補",fa_car_kouho)
                fa_car_kouho = fa_hako.min()
                fa_car_kouho = round(fa_car_kouho, 2)
                if fa_car_kouho< 10:
                    print(fa_car_kouho,"はもくひょうを達成した")
                print("車までのきょり2",fa_car_kouho)

        fa_syucar[i] = fa_car_kouho
        #print("fa_kouhoについて",fa_syucar)
    return fa_syucar


def fa_sen(alpha0, syudan, n , cars, n_cars):
    # cars は一つの始点(xcar, ycar)をもとにした三次元配列
    #ところどころで参照する配列の位置が間違えている
    pi = math.pi
    #print("fa_carのためのalpha0",alpha0)
    fa_syucar = np.full(n,10.00)
    l_abc = np.array([0,1,-10])
    fa_abc = np.zeros((n, 3))

    for i in range(n):
        #それぞれの歩行者エージェントが自動車に対してもつfa
        hantei = 10
        fa_car_kouho = 10
        #forループによってnum_carについてのループも行ったほうがいいのではないか

        ireruyatu = alpha0[i]
        if ireruyatu < 0:
            ireruyatu = 2*pi - ireruyatu
            #fa_car_kouho = 10
        if  ireruyatu < 0:
                #print("角度がマイナスで変化させる必要がある角度",ireruyatu)
            ireruyatu = math.pi - ireruyatu
                #print("角度がマイナスで変化さsetaatri",ireruyatu)
            #集団は進行方向aをもち，関数になる
            #print("車に対しての距離までの計算のための角度",alpha0[i])

        if ireruyatu == pi/2:
            fa_abc[i, 1] = 1/syudan[i,1]
            fa_abc[i, 2] = -1
                #print("要チェック",cars[k,1,0])

            if syudan[i, 0] >= 8 and syudan[i, 0] <= 15:
                fa_car_kouho = abs(syudan[i,1] - l_abc[2])

        elif ireruyatu == 3*(pi/2) :
                #print("syudan[i,1]",syudan[i,1])
            fa_abc[i, 1] = 1/syudan[i,1]
            fa_abc[i, 2] = -1
                #print("要チェック",cars[k,3,0])
            if syudan[i, 0] >= 2 and syudan[i, 0] <= 20:
                fa_car_kouho = abs(syudan[i,1] - l_abc[2])
        else:
            fa_abc[i,0] = -math.tan(ireruyatu)
            fa_abc[i,1] = 1
            fa_abc[i,2] = math.tan(ireruyatu)*syudan[i,0] -syudan[i,1]
            kouho = 10
            kouten_x = (10-fa_abc[i,2])/fa_abc[i,0]
            kouten_x = round(kouten_x,4)
            kouten_y = 10
            kouten_y = round(kouten_y,4)
            print("交点",kouten_x,kouten_y)
            #print("faの候補",fa_car_kouho)
            if kouten_x >= 2 and kouten_x<= 8:
                fa_car_kouho = ((kouten_x - syudan[i,0])**2 + (kouten_y - syudan[i,1])**2)**0.5
                fa_car_kouho = round(fa_car_kouho, 2)
                print("車までのきょり2",fa_car_kouho)
        if fa_car_kouho <= 10:
            fa_syucar[i] = fa_car_kouho
        #print("fa_kouhoについて",fa_syucar)
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
                kyori = (abs(syudan[i,0]-syudan[j,0])**2 + abs(syudan[i,1]-syudan[j,1])**2)**0.5
                #if kyori<=60/220 and
                #print("距離は",kyori)
                if kyori < 10:
                    fa_syudan[i] = kyori

    return fa_syudan


def fa_dasukai2(v_2d, syudan, n):
    # 第一のヒューリスティックに関する計算
    # 周囲のエージェントの存在を認知する
    #SAレベル３を考慮に入れたもの
    fa_syudan = np.full(n, 10.00)
    alpha_fa = np.zeros(n)
    syudan_ato = syudan + v_2d
    #それぞれのエージェントの進行角度の算出
    for i in range(n):
        if v_2d[i,0] == 0:
            if v_2d[i,1] >= 0:
                alpha_fa[i] = math.pi/2
            else:
                alpha_fa[i] = 3*math.pi/2
        else:
            alpha_fa[i] = np.arctan2(v_2d[i,1], v_2d[i,0])
    #各エージェントの処理
    for i in range(n):
        #この処理で，各エージェントを中心としたxy座標に置き換えられる
        soutai = syudan_ato - syudan_ato[i]
        #相対化した各エージェントと他の同志のの処理
        for j in range(n):
            fa_kouho = 10.00
            if soutai[j, 0] == 0 and soutai[j, 1] == 0:
                continue
            if alpha_fa[i] == math.pi/2:
                if soutai[j,0] >= -60/220 and soutai[j,0] <= 60/220:
                    fa_kouho = soutai[j,1] - 60/220
            elif alpha_fa[i] == 3*math.pi/2:
                if soutai[j,0] >= -60/220 and soutai[j,0] <= 60/220:
                    fa_kouho = soutai[j,1] - 60/220
            else:
                m = v_2d[i,1]/v_2d[i,0]
                yosou_y = m * soutai[j,0]
                if yosou_y >= soutai[j,1]-60/220 and yosou_y <= soutai[i,1]+60/220:
                    fa_kouho = (abs(soutai[j,0])**2  + abs(soutai[j,1])**2) ** 0.5
            fa_kouho = round(fa_kouho,2)

            if fa_kouho <= fa_syudan[i]:
                fa_syudan[i] = round(fa_kouho - 60/220,2)


            if abs(soutai[j,0]) <= 60/220 and abs(soutai[j,1]) <= 60/220:
                kyori = np.linalg.norm(soutai[j])
                i_x = round(syudan[i,0],2)
                i_y = round(syudan[i,1],2)
                j_x = round(syudan[j,0],2)
                j_y = round(syudan[j,1],2)
                kyori = (abs(i_x-j_x)**2 + abs(i_y-j_y)**2)**0.5
                kyori = round(kyori,2)
                #if kyori<=60/220 and
                #print("距離は",kyori)
                if kyori < 10:
                    fa_syudan[i] = round(kyori,2)


    return fa_syudan

def fa_dasukai2(v_2d, syudan, n):
    # 第一のヒューリスティックに関する計算
    # 周囲のエージェントの存在を認知する
    #SAレベル３を考慮に入れたもの
    fa_syudan = np.full(n, 10.00)
    alpha_fa = np.zeros(n)
    syudan_ato = syudan + v_2d
    #それぞれのエージェントの進行角度の算出
    for i in range(n):
        if v_2d[i,0] == 0:
            if v_2d[i,1] >= 0:
                alpha_fa[i] = math.pi/2
            else:
                alpha_fa[i] = 3*math.pi/2
        else:
            alpha_fa[i] = np.arctan2(v_2d[i,1], v_2d[i,0])
    #各エージェントの処理
    for i in range(n):
        #この処理で，各エージェントを中心としたxy座標に置き換えられる
        soutai = syudan_ato - syudan_ato[i]
        #相対化した各エージェントと他の同志のの処理
        for j in range(n):
            fa_kouho = 10.00
            if soutai[j, 0] == 0 and soutai[j, 1] == 0:
                continue
            if alpha_fa[i] == math.pi/2:
                if soutai[j,0] >= -60/220 and soutai[j,0] <= 60/220:
                    fa_kouho = soutai[j,1] - 60/220
            elif alpha_fa[i] == 3*math.pi/2:
                if soutai[j,0] >= -60/220 and soutai[j,0] <= 60/220:
                    fa_kouho = soutai[j,1] + 60/220
            else:
                m = v_2d[i,1]/v_2d[i,0]
                yosou_y = m * soutai[j,0]
                if yosou_y >= soutai[j,1]-60/220 and yosou_y <= soutai[i,1]+60/220:
                    fa_kouho = (abs(soutai[j,0])**2  + abs(soutai[j,1])**2) ** 0.5
            fa_kouho = round(fa_kouho,2)

            if fa_kouho <= fa_syudan[i]:
                fa_syudan[i] = round(fa_kouho - 60/220,2)



    return fa_syudan

def fa_kekka( n,fa_syudan,fa_syucar,hu_car):
    # fa_syudan, fa_carの代償比較
    fa_hontou = np.full(n,10.00)
    for i in range(n):
        if fa_syudan[i] <= fa_syucar[i]:
            fa_hontou[i] = fa_syudan[i]
            fa_hontou[i] = round(fa_hontou[i], 2)
            hu_car[i] = 0
        else:
            fa_hontou[i] = fa_syucar[i]
            fa_hontou[i] = round(fa_hontou[i], 2)
            hu_car[i] = 0

        if fa_hontou[i] == 0:
            fa_hontou[i] = 0.5
            fa_hontou[i] = round(fa_hontou[i], 2)

    return fa_hontou




# 関数を変更位させるnumpyの配列に対応
def hulistics_1(fa, alpha0,n,hu_car):
    # 目的関数
    Dmax = 10

    """def objective_function(theta, arufa):
        return (Dmax**2)+(fa**2)-(2*Dmax*fa*math.cos(arufa-theta))"""

    #alpha0 = alpha0.astype(np.float32)

    for i in range(n):
        # 歩行者の半径を考慮したものに
        def fufu(theta):
            return (Dmax ** 2) + (fa[i] ** 2) - (2 * Dmax * fa[i] * math.cos(alpha0[i] - theta))

        def fufu1(theta):
            return ((Dmax ** 2) - (2 * Dmax * fa[i] * math.cos(alpha0[i] - theta)))**2
        def fufu2(theta):
            return (Dmax ** 2) + (fa[i] ** 2) - (2 * Dmax * fa[i] * math.cos(alpha0[i] - theta))




        nagasa =(fa[i]**2 - (60/220)**2)**0.5

        #kakudo_gosa = np.arctan((60/220)/nagasa)
        kakudo_gosa = round(np.arctan2((60/220),nagasa),2)

        if hu_car[i] == 0:

            min1 = optimize.fminbound(fufu2, (alpha0[i] - math.pi*5/12), alpha0[i] - kakudo_gosa)
            min2 = optimize.fminbound(fufu2, alpha0[i] + kakudo_gosa, alpha0[i] + (math.pi*5/12))
        else:
            #min1 = optimize.fminbound(fufu1, (alpha0[i] - math.pi*5/12), alpha0[i] - kakudo_gosa)
            min1 = optimize.fminbound(fufu1, (alpha0[i] - math.pi*5/12), alpha0[i] + (math.pi*5/12))
            min2 = optimize.fminbound(fufu1, alpha0[i] + kakudo_gosa, alpha0[i] + (math.pi*5/12))


        min_1 = abs(alpha0[i] - abs(alpha0[i] - min1))
        min_2 = abs(alpha0[i] - abs(alpha0[i] - min2))

        #print("min1", "min2", "min3", min1, min2, alpha0[i])
        if min_1 >= min_2:
            alpha0[i] = min1
        else:
            alpha0[i] = min2
        alpha0[i] = round(alpha0[i], 5)
    return alpha0


def hulistics_1_kai(fa, alpha0,n):
    # 目的関数
    Dmax = 10

    """def objective_function(theta, arufa):
        return (Dmax**2)+(fa**2)-(2*Dmax*fa*math.cos(arufa-theta))"""

    #alpha0 = alpha0.astype(np.float32)

    for i in range(n):
        # 歩行者の半径を考慮したものに
        def fufu(theta):
            return (Dmax ** 2) + (fa[i] ** 2) - (2 * Dmax * fa[i] * math.cos(alpha0[i] - theta))

        def fufu(theta):
            return ((Dmax ** 2) - (2 * Dmax * fa[i] * math.cos(alpha0[i] - theta)))**2

        nagasa =(fa[i]**2 - (60/220)**2)**0.5

        #kakudo_gosa = np.arctan((60/220)/nagasa)
        kakudo_gosa = np.arctan2((60/220),nagasa)


        min1 = optimize.fminbound(fufu, (alpha0[i] - math.pi*5/12), alpha0[i] + (math.pi*5/12))
        #min2 = optimize.fminbound(fufu, alpha0[i] + kakudo_gosa, alpha0[i] + (math.pi*5/12))

        min_1 = alpha0[i] - abs(alpha0[i] - min1)
        #min_2 = alpha0[i] - abs(alpha0[i] - min2)
        #print("min1", "min2", "min3", min1, min2, alpha0[i])
        alpha0[i] = min_1
        alpha0[i] = round(alpha0[i], 2)
    return alpha0
"""
def hulistics_car(alpha, ):
    Dmax = 10
     #faは進行方向に対して衝突するまで
    alpha = alpha
    itizi = fa
    huyasu = alpha
    #衝突線分の表示
    for i in range
    #もし，線分限界のやつが両方10未満なら,その限界をいく
    #もし，線分限界のやつが片方10より大きいなら距離が10になる点を2天求めて，範囲外なら
    #その2点が
            #交差判定-> true -> 交点に対しての距離を測る +-両方を対象として，範囲内で10に近いものが出たらそこに更新，なかったら

"""



def cal_fij(n, syudan):
    # この関数は大幅に縮小できる気がする一応実装修了
    fij = np.zeros([n, 2])
    #print("fij", fij)
    """
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
        """
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
        #alpha = math.atan(vy/vx)
        alpha = math.atan2(vy,vx)
    alpha = round(alpha, 2)
    return alpha

def mokutekiti_siro(alpha,iti):
    if alpha == math.pi/2:
        y = 35
        x_ato = iti[0]
    elif alpha == -math.pi/2:
        y = 5
        x_ato = iti[0]
    else:
        m = np.tan(alpha)
        print("いちちt",iti)
        print("目的のalpha",alpha)
        if alpha >= 0 and alpha <= math.pi:
            x_ato = (41-iti[1])/m + iti[0]
            y = 37
        else:
            x_ato = (-1-iti[1])/m + iti[0]
            y = 2
    #print("x_ato", x_ato)
    iti_moku = np.array([[x_ato,y]])
    #print("iti_moku", iti_moku)
    return iti_moku

def alpha_kousin(moku, alpha,iti ,n):
    #求めるalphaの更新
    #print("iti", iti)
    #print("moku", moku)
    for i in range(n):
        #print("moku_iti", moku, iti)
        #print("このループ",i,"総数",n)
        #print("moku[i,0, iti[i,0]",moku[i,0], iti[i,0])
        x_hen = moku[i,0] - iti[i,0]
        y_hen = moku[i,1] - iti[i,1]
        #print("x_hen", x_hen)
        #print(" y_hen",y_hen)
        alpha_kari = np.arctan2(y_hen,x_hen)
        alpha[i] = alpha_kari

def syouhan(n,iti):
    for i in range(n):
        for j in range(n):
            if iti[i,0] == iti[j,0] and iti[i,1] == iti[j,1]:
                continue
            else:
                if abs(iti[i,0]- iti[j,0])<= 60/220 and  abs(iti[i,1]- iti[j,1])<= 60/220:
                    print(i,j,"が衝突しました")





def end_oudan(n,iti,alpha):
    for i in range(n):
        if alpha >= 0 and iti[i,1]>= 35:
            iti[i,0] = 0
            iti[i,1] = 0
        elif alpha <= 0 and iti[i,1]<=6:
            iti[i,0] = 0
            iti[i,1] = 0


