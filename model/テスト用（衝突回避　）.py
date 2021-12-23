"""このプログラムは実行部です"""

import numpy as np
import random
import math
from moussaif import fa_dasukai,fa_dasukai2, hulistics_1,hulistics_1_kai, cal_fij, fa_car , dasu_v_1d, fa_kekka , alpha_dasu,mokutekiti_siro, alpha_kousin, syouhan
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
import pandas as pd
from pathlib import Path
import openpyxl
import xlrd

pi = math.pi
#関数部の関数を全ぶmoussaif.pyからインポートしてから実行する
zikan = np.arange(100)/2

n_cars = 1


cars = np.array([[[10,30],
                  [10,25],
                  [0,30],
                  [0,25]]])
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

df = pd.read_excel("iiyatu_test1203.xlsx", sheet_name='Sheet3')
nmp=df.to_numpy()
syudan = nmp

np.set_printoptions(suppress=True)
syudan = np.delete(syudan, 0, axis=1)

print("syudan.shape",syudan.shape)

#syudan = syudan[:,2:4 ]

n_kei = syudan.shape[0]

syudan_gen = np.empty((0,10),int)
#mokuteki = np.empty((0,2))

print("syudan_gen", syudan_gen)
for i in range(n_kei):
    print("syudan[i,0", syudan[i,0])
    if syudan[i,0] == 0:
        print("syudan[i]",syudan[i])
        tuika= np.array([syudan[i]])
        syudan_gen = np.append(syudan_gen,tuika,axis=0)
print()
#昔は集団だったもの，x,yを格納する
print("syudan_gen", syudan_gen)

n_gen = syudan_gen.shape[0]
print("n_gen", n_gen)
fa  = np.zeros(n_gen)
xy_iti = syudan_gen[:,2:4]

v_1d = syudan_gen[:,6]
v_2d = syudan_gen[:, 4:6]
alpha = syudan_gen[:, 7]
mokuteki = syudan_gen[:,8:10]


print("xy_iti", xy_iti)
print("v_1d", v_1d)
print("v_2d", v_2d)
print("alpha", alpha)


#fig = plt.figure(figsize=(8, 6))
fig = plt.figure()
fig.patch.set_facecolor('white')
ax = fig.add_subplot(1, 1, 1)
ax.grid()
ax.set_xlim([0,30])
ax.set_ylim([0,40])
ax.set_xlabel("x", fontsize = 14)
ax.set_ylabel("y", fontsize = 14)

#ax.set_xlim([-2, 40])
#ax.set_ylim([-2, 30])

im = Image.open("oudan_2.png")
#im_resize = im.resize(size=(100,60))
ax.imshow(im, extent=[0, 30, 0, 40], aspect='auto', alpha=0.6)


iti = []


for j in zikan:
    print("####",j,"s秒目######")
    if not j == 0:
        for t in range(n_kei):
            if syudan[t,0] == j:
                n_gen += 1
                xy = np.array([syudan[t,2:4]])
                xy_iti = np.append(xy_iti, xy, axis=0)
                v_1d = np.append(v_1d, syudan[t, 6])
                v2d = np.array([syudan[t, 4:6]])
                v_2d = np.append(v_2d, v2d, axis=0)
                alpha = np.append(alpha, syudan[t,7])
                moku_i = np.array([syudan[t,8:10]])
                mokuteki = np.append(mokuteki, moku_i,axis=0)
    print(j,"秒目のn_gen",n_gen)
    print(j,"秒目のxy_iti",xy_iti)

    iti_x = []
    iti_y = []
    print("変化前のalpha",alpha)

    for a in range(10):
        #print("aaaaa",a)
        fa_syucar = fa_car(alpha, xy_iti , n_gen, cars, n_cars)
        #print("fa車",fa_syucar)
        """
        for l in range(n_gen):
            if fa_syucar[l] < 10:
                print(fa_syucar[l],l,"車のfaはちゃんと計算されてる")
        """
    #周囲のエージェントを認識
        fa = fa_dasukai2(v_2d, xy_iti, n_gen)
        fa = fa_kekka(n_gen, fa, fa_syucar)

    #print(fa, type(fa))
        #print("fa", fa)
    #alpha = alpha_ini
    #print("目的地",mokuteki)
        alpha_kousin(mokuteki, alpha,xy_iti,n_gen)
            #print("変化前のalpha",alpha)
        alpha = hulistics_1_kai(fa, alpha, n_gen)
            #print(alpha,"alpha")

    sum_fij = cal_fij(n_gen, xy_iti)
    #sum_fij = np.zeros(n_gen)
    #print("sum_fij", sum_fij)
        #print("v_2d", v_2d)
    print(alpha,"alpha")

    dvdt = np.zeros([n_gen, 2])

    for i in range(n_gen):
        #dvdt[i, 0] = (v_2d[i, 0] - 1.7 * math.cos(alpha[i])) / 0.5 + sum_fij[i, 0]
        #vdes と d / tの関係を記述しきれてないのではないか
        vdes_1 = 1.3
        vdes = fa[i]/0.5
        if vdes >= vdes_1:
            vdes = vdes_1
        dvdt[i, 0] = (vdes * math.cos(alpha[i]) - v_2d[i, 0] ) / 0.5 + sum_fij[i, 0]
        dvdt[i, 0] = round(dvdt[i,0], 2)/4

        dvdt[i, 1] = (v_1d[i] * math.sin(alpha[i]) - v_2d[i, 1] ) / 0.5 + sum_fij[i, 1]
        dvdt[i, 1] = round(dvdt[i, 1], 2)/4

    v_2d += dvdt
    xy_iti = xy_iti + v_2d
    v_1d = dasu_v_1d(v_2d, v_1d, n_gen)
    print("v_1d", v_1d)
    print("v_2d", v_2d)
    #print("v_1d", v_1d)

    #plt.xlim(0, 10)
    # plt.ylim(-10, 70)
    iti_scatter = plt.scatter(xy_iti[:,0],xy_iti[:,1] ,c="blue")
    iti.append([iti_scatter])

#for i in range(time):

anim = animation.ArtistAnimation(fig, iti)

aaa = Path("hozon")
anim.save(aaa/'teatsampke12010car.gif', writer='writer', fps=2)

plt.show()
