"""このプログラムは実行部です"""

import numpy as np
import random
import math
from moussaif import fa_dasukai, hulistics_1, cal_fij, cal_fiw , dasu_v_1d, dvdt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
import pandas as pd
import openpyxl
import xlrd

#関数部の関数を全ぶmoussaif.pyからインポートしてから実行する

df = pd.read_excel("kokai.xlsx", sheet_name='Sheet1')

n = 12
pi = math.pi
time = 17

nmp=df.to_numpy()
syudan = nmp[:,:2]

v_1d = nmp[:,2]
alpha = nmp[:, 3]
for i in range(12):
    alpha[i] = math.radians(alpha[i])
    alpha[i] = round(alpha[i], 2)

v_2d = np.zeros([12,2])
for i in range(12):
    v_2d[i,0] = v_1d[i] * math.cos(alpha[i])
    v_2d[i,1] = v_1d[i] * math.sin(alpha[i])


alpha = nmp[:, 3]


mokuteki = alpha

fig = plt.figure()
ax = fig.add_subplot(111)
ax.grid()
ax.set_xlim([-2, 35])
ax.set_ylim([-2, 24])
ax.set_xlabel("x", fontsize = 14)
ax.set_ylabel("y", fontsize = 14)

im = Image.open("kokai.png")
im_resize = im.resize(size=(66,60))
ax.imshow(im, extent=[-2, 35, -2, 24], aspect='auto', alpha=0.6)

iti = []

iti_x = []
iti_y = []

print("###alpha", alpha)
for j in range(time):

    print("####",j,"step目######")

    iti_x = []
    iti_y = []

    #周囲のエージェントを認識
    fa = fa_dasukai(v_2d, syudan, n)

    #alphaを更新しようか迷う

    #print(fa, type(fa))
    print("fa", fa)

    alpha = mokuteki

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
        #vdes と d / tの関係を記述しきれてないのではないか
        vdes_1 = 1.75
        vdes = fa[i]/0.5
        if vdes >= vdes_1:
            vdes = vdes_1
        dvdt[i, 0] = (vdes * math.cos(alpha[i]) - v_2d[i, 0] ) / 0.5 + sum_fij[i, 0]
        dvdt[i, 0] = round(dvdt[i,0], 2)
        #dvdt[i, 0] = round(dvdt[i, 0], 1)
        #print("dvdt[i, 0]",i,dvdt[i, 0])

        # dvdt[i, 0] = (v_2d[i, 0] - 1.7 * np.cos(alpha(i))) / 0.5 + fij(i, 0) + fiw(i, 0)
        #dvdt[i, 1] = (v_2d[i, 1] - 1.7 * math.sin(alpha[i])) / 0.5 + sum_fij[i, 1]
        dvdt[i, 1] = (v_1d[i] * math.sin(alpha[i]) - v_2d[i, 1] ) / 0.5 + sum_fij[i, 1]
        dvdt[i, 1] = round(dvdt[i, 1], 2)
        #dvdt[i, 1] = round(dvdt[i, 1], 1)
        #print("dvdt[i, 1]",i,dvdt[i, 1])
        #print("dvdt[i]", i, dvdt[i])
    #v_2d += dvdt

    #print(j, "step", "v_2d", v_2d)

    #syudan = syudan + dvdt

    #print("syudan", syudan)

    #print("現在の位置は", syudan)
    v_2d += dvdt
    syudan = syudan + v_2d
    v_1d = dasu_v_1d(v_2d, v_1d, n)
    #print("v_1d", v_1d)

    #plt.xlim(0, 10)
    # plt.ylim(-10, 70)
    iti_scatter = plt.scatter(syudan[:,0],syudan[:,1] ,c="blue")
    iti.append([iti_scatter])

#for i in range(time):

anim = animation.ArtistAnimation(fig, iti)
anim.save('kokai.gif', writer='writer', fps=4)

plt.show()
