"""このプログラムは実行部です"""

import numpy as np
import random
import math
from moussaif import fa_dasukai, hulistics_1, cal_fij, cal_fiw , dasu_v_1d, fa_car , fa_kekka
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime


#関数部の関数を全ぶmoussaif.pyからインポートしてから実行する

n = 4
n_cars = 1
pi = math.pi

fa = np.zeros(n)
v_1d = np.full(n, 1.7)
v_2d = np.zeros([n,2])
dvdt = np.zeros([n,2])
alpha = np.zeros(n)
time = 10
syudan = np.zeros([n,2])

cars = np.array([[[5,6],
                  [5,5],
                  [0,5],
                  [0,6]]])
"""
cars_v = np.array([[[1,0],
                  [1,0],
                  [1,0],
                  [1,0]]])
"""
cars_v = np.array([[[0,0],
                    [0,0],
                    [0,0],
                    [0,0]]])



#print(v_2d)
#print(v_2d[3,1])



for i in range(n):
    kakuritu = random.random()
    v_1d[i] = 1.7
    #v_itizi = v_2d[i,:]
    if kakuritu >= 0.5:
        alpha[i] = pi/2
        syudan[i,0] = round(random.randrange(2, 8)+random.random(),1)
        syudan[i,1] = round(random.randrange(0, 1)+random.random(),1)
    else :
        alpha[i] = 3*pi/2
        syudan[i, 0] = round(random.randrange(2, 8) + random.random(), 1)
        syudan[i, 1] = round(random.randrange(8, 10) + random.random(), 1)
    #print("v_2d", v_2d[i, 0])
    #print("alpha", alpha[i])
    #print("arekore", v_1d[i] * np.cos(alpha[i]))
    v_2d[i, 0] = v_1d[i] * np.cos(alpha[i])
    v_2d[i, 1] = v_1d[i] * np.sin(alpha[i])

#print("初めのalpha", alpha)

alpha[0] = pi/2
syudan[0,0]  = 2
syudan[0,1]  = 0

alpha[1] = pi/2
syudan[1,0]  = 5
syudan[1,1]  = 0

alpha[2] = 3*pi/2
syudan[2,0]  = 4
syudan[2,1]  = 10

alpha[3] = 3*pi/2
syudan[2,0]  = 8
syudan[2,1]  = 10






#print(v_1d, v_2d )
fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlim([0, 10])
ax.set_ylim([0, 9.5])
ax.set_xlabel("x", fontsize = 14)
ax.set_ylabel("y", fontsize = 14)


# y=5に水平線を引く
#横断歩道自体はあらかじめ決まった値であるが、それはexcelで参照するような形にした方が書かくちょうせいがたかい
"""実際ではforで変数を固定し、それぞれ回す"""
ax.axhline(0.5,xmin=0.2, xmax=0.8, color = "black")
ax.axhline(1,xmin=0.2, xmax=0.8,color = "black")

ax.axhline(2,xmin=0.2, xmax=0.8, color = "black")
ax.axhline(2.5,xmin=0.2, xmax=0.8,color = "black")

ax.axhline(3.5,xmin=0.2, xmax=0.8, color = "black")
ax.axhline(4,xmin=0.2, xmax=0.8,color = "black")

ax.axhline(5,xmin=0.2, xmax=0.8, color = "black")
ax.axhline(5.5,xmin=0.2, xmax=0.8,color = "black")

ax.axhline(6.5,xmin=0.2, xmax=0.8, color = "black")
ax.axhline(7,xmin=0.2, xmax=0.8,color = "black")

ax.axhline(8,xmin=0.2, xmax=0.8, color = "black")
ax.axhline(8.5,xmin=0.2, xmax=0.8,color = "black")



# x=3に垂直線を引く
ax.axvline(2, color = "navy")
ax.axvline(8, color = "navy")


iti = []

iti_x = []
iti_y = []


for j in range(time):

    print("####",j,"step目######")

    iti_x = []
    iti_y = []

    #周囲のエージェントを認識

    fa_syucar = fa_car(alpha, syudan , n, cars, n_cars)
    print("fa_syucar",fa_syucar)
    fa = fa_dasukai(v_2d, syudan, n)
    #fa = fa_dasukai(v_2d, syudan, n)
    fa = fa_kekka(n, fa, fa_syucar)

    #alphaを更新しようか迷う

    #print(fa, type(fa))
    print("fa", fa)


    alpha = hulistics_1(fa, alpha, n)
    print(alpha,"alpha")
    sum_fij = cal_fij(n, syudan)
    print("sum_fij", sum_fij)
    print("v_2d", v_2d)

    #print("sum_fij", sum_fij)
    #print("sum_fij", sum_fij)
    #v_2d = dvdt(n,v_2d,alpha,sum_fij)
    dvdt = np.zeros([n, 2])

    for i in range(n):
        #dvdt[i, 0] = (v_2d[i, 0] - 1.7 * math.cos(alpha[i])) / 0.5 + sum_fij[i, 0]
        dvdt[i, 0] = (v_1d[i] * math.cos(alpha[i]) - v_2d[i, 0] ) / 0.5 + sum_fij[i, 0]
        dvdt[i, 0] = round(dvdt[i,0], 1)
        #dvdt[i, 0] = round(dvdt[i, 0], 1)
        #print("dvdt[i, 0]",i,dvdt[i, 0])

        # dvdt[i, 0] = (v_2d[i, 0] - 1.7 * np.cos(alpha(i))) / 0.5 + fij(i, 0) + fiw(i, 0)
        #dvdt[i, 1] = (v_2d[i, 1] - 1.7 * math.sin(alpha[i])) / 0.5 + sum_fij[i, 1]
        dvdt[i, 1] = (v_1d[i] * math.sin(alpha[i]) - v_2d[i, 1] ) / 0.5 + sum_fij[i, 1]
        dvdt[i, 1] = round(dvdt[i, 1], 1)

    v_2d += dvdt
    syudan = syudan + v_2d
    print("syudan", syudan)
    cars = cars + cars_v
    v_1d = dasu_v_1d(v_2d, v_1d, n)
    #print("v_1d", v_1d)

    #plt.xlim(0, 10)
    # plt.ylim(-10, 70)
    iti_scatter = plt.scatter(syudan[:,0],syudan[:,1] ,c="blue")
    iti.append([iti_scatter])

#for i in range(time):

anim = animation.ArtistAnimation(fig, iti)
anim.save('ex1_8.gif', writer='writer', fps=4)

plt.show()
