"""このプログラムは実行部です"""

import numpy as np
import random
import math
from moussaif import fa_dasukai,fa_dasukai2, hulistics_1, cal_fij, cal_fiw , dasu_v_1d, dvdt , alpha_dasu,mokutekiti_siro, alpha_kousin, syouhan
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

df = pd.read_excel("MAH00556-01_全データ回帰分析強化版.xlsx", sheet_name='Sheet1')
nmp=df.to_numpy()
syudan = nmp

np.set_printoptions(suppress=True)
syudan = np.delete(syudan, 0, axis=1)

print("syudan.shape",syudan.shape)

#syudan = syudan[:,2:4 ]

n_kei = syudan.shape[0]

syudan_gen = np.empty((0,10),int)
mokuteki = np.empty((0,2))

#print("syudan_gen", syudan_gen)
for i in range(n_kei):
    #print("syudan[i,0", syudan[i,0])
    if syudan[i,0] == 0:
        #print("syudan[i]",syudan[i])
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
v_2d = v_2d.astype(np.float64)
alpha = syudan_gen[:, 9]

for j in range(n_gen):
    #moku_j = mokutekiti_siro(alpha[j], xy_iti[j])
    moku_j = np.array([[syudan_gen[j,7], syudan_gen[j,8]]])
    print("moku_j",moku_j)
    mokuteki = np.append(mokuteki,moku_j, axis=0)

alpha_kousin(mokuteki, alpha, xy_iti, n_gen)

#mokuteki = alpha

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

#iti_x = []
#iti_y = []

print("###alpha", alpha)
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
                v_2d = v_2d.astype(np.float64)
                v_2d = np.append(v_2d, v2d, axis=0)
                print("計算前ののalpha",alpha)
                alpha = np.append(alpha, syudan[t,9])
                #mokuteki = np.append(mokuteki, syudan[t,7])
                #moku_t = mokutekiti_siro(syudan[t,7],syudan[t,2:4])
                moku_t = np.array([[syudan[t,7], syudan[t,8]]])

                mokuteki = np.append(mokuteki, moku_t,axis=0)
    print(j,"秒目のn_gen",n_gen)
    print(j,"秒目のxy_iti",xy_iti)






    iti_x = []
    iti_y = []
    #周囲のエージェントを認識
    fa = fa_dasukai2(v_2d, xy_iti, n_gen)
    #print(fa, type(fa))
    #print("fa", fa)
    print("mokuteki", mokuteki)
    print("xy_iti", xy_iti)

    print("n_gen", n_gen)
    alpha_kousin(mokuteki, alpha,xy_iti,n_gen)
    alpha = hulistics_1(fa, alpha, n_gen)

    print("alpha$$$$$$$$$$$$$$$$$$$$$",alpha)
    #print(alpha,"alpha")

    sum_fij = cal_fij(n_gen, xy_iti)
    #sum_fij = np.zeros(n_gen)
    print("sum_fij", sum_fij)
    #print("v_2d", v_2d)

    dvdt = np.zeros([n_gen, 2])

    for i in range(n_gen):
        #dvdt[i, 0] = (v_2d[i, 0] - 1.7 * math.cos(alpha[i])) / 0.5 + sum_fij[i, 0]
        #vdes と d / tの関係を記述しきれてないのではないか
        vdes_1 = 1.6
        vdes = fa[i]/0.5
        if vdes >= vdes_1:
            vdes = vdes_1
        dvdt[i, 0] = (vdes * math.cos(alpha[i]) - v_2d[i, 0] ) / 0.5 + sum_fij[i, 0]
        dvdt[i, 0] = round(dvdt[i,0], 2)/2

        dvdt[i, 1] = (v_1d[i] * math.sin(alpha[i]) - v_2d[i, 1] ) / 0.5 + sum_fij[i, 1]
        dvdt[i, 1] = round(dvdt[i, 1], 2)/2

    print("cast",v_2d,dvdt,v_2d.dtype,dvdt.dtype)
    v_2d += dvdt
    xy_iti = xy_iti + v_2d

    syouhan(n_gen, xy_iti)
    v_1d = dasu_v_1d(v_2d, v_1d, n_gen)
    #print("v_1d", v_1d)
    #print("v_2d", v_2d)
    #print("v_1d", v_1d)

    #plt.xlim(0, 10)
    # plt.ylim(-10, 70)
    #plt.text(15, 40, j )
    ax.text(10, 15, j, ha='center', transform=ax.transAxes)
    iti_scatter = plt.scatter(xy_iti[:,0],xy_iti[:,1] ,c="blue")
    iti.append([iti_scatter])

#for i in range(time):

anim = animation.ArtistAnimation(fig, iti)

aaa = Path("hozon")
anim.save(aaa/'zikkou_単回帰全てAI今日カバン1210.gif', writer='writer', fps=2)

plt.show()
