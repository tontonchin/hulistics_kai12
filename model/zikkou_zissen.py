"""このプログラムは実行部です"""

import numpy as np
import random
import math
from moussaif import fa_dasu, hulistics_1, cal_fij, cal_fiw , dasu_v_1d, dvdt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd


#関数部の関数を全ぶmoussaif.pyからインポートしてから実行する

#n = 10
pi = math.pi

df1 = pd.read_excel('syoki_alpha.xlsx')
df2 = pd.read_excel('syoki_hayasa.xlsx')


n_mae = df1.iloc[-1,0]
n = n_mae.item()

#要素が0の配列をそれぞれ作成し，準備をする
fa = np.zeros(n)
#v_1d = np.full(n, 1.7)
v_1d = np.zeros(n)
v_2d = np.zeros([n,2])
dvdt = np.zeros([n,2])
alpha = np.zeros(n)
time = 10
syudan = np.zeros([n,2])

#print(v_2d)
#print(v_2d[3,1])


"""
for i in range(n):
    kakuritu = random.random()
    v_1d[i] = 1.7
    #v_itizi = v_2d[i,:]
    if kakuritu >= 0.5:
        alpha[i] = pi/2
        syudan[i,0] = round(random.randrange(0, 10)+random.random(),2)
        syudan[i,1] = round(random.randrange(0, 5)+random.random(),2)
    else :
        alpha[i] = 3*pi/2
        syudan[i, 0] = round(random.randrange(0, 5) + random.random(), 2)
        syudan[i, 1] = round(random.randrange(40, 50) + random.random(), 2)
    print("v_2d", v_2d[i, 0])
    print("alpha", alpha[i])
    #print("arekore", v_1d[i] * np.cos(alpha[i]))
    v_1d[i] = df2[i, 1]
    v_2d[i, 0] = v_1d[i] * np.cos(alpha[i])
    v_2d[i, 1] = v_1d[i] * np.sin(alpha[i])
"""

for i in range(n):
    kakuritu = random.random()
    v_1d[i] = 1.7
    #v_itizi = v_2d[i,:]
    if kakuritu >= 0.5:
        alpha[i] = pi/2
        syudan[i,0] = round(random.randrange(0, 10)+random.random(),2)
        syudan[i,1] = round(random.randrange(0, 5)+random.random(),2)
    else :
        alpha[i] = 3*pi/2
        syudan[i, 0] = round(random.randrange(0, 5) + random.random(), 2)
        syudan[i, 1] = round(random.randrange(40, 50) + random.random(), 2)
    print("v_2d", v_2d[i, 0])
    print("alpha", alpha[i])
    #print("arekore", v_1d[i] * np.cos(alpha[i]))
    v_1d[i] = df2[i, 1]
    v_2d[i, 0] = v_1d[i] * np.cos(alpha[i])
    v_2d[i, 1] = v_1d[i] * np.sin(alpha[i])

print("初めのalpha", alpha)


#print(v_1d, v_2d )
fig = plt.figure()
iti = []

iti_x = []
iti_y = []


for j in range(time):
    print("####",i,"step目######")

    #周囲のエージェントを認識
    fa = fa_dasu(v_2d, syudan, n)
    print(fa, type(fa))
    print("fa", fa)

    alpha = hulistics_1(fa, alpha, n)
    sum_fij = cal_fij(n, syudan)
    print("sum_fij", sum_fij)
    #print("sum_fij", sum_fij)
    #v_2d = dvdt(n,v_2d,alpha,sum_fij)
    dvdt = np.zeros([n, 2])

    for i in range(n):
        dvdt[i, 0] = (v_2d[i, 0] - v_1d[i] * np.cos(alpha[i])) / 0.5 + sum_fij[i, 0]

        # dvdt[i, 0] = (v_2d[i, 0] - 1.7 * np.cos(alpha(i))) / 0.5 + fij(i, 0) + fiw(i, 0)
        dvdt[i, 1] = (v_2d[i, 1] - v_1d[i] * np.sin(alpha[i])) / 0.5 + sum_fij[i, 1]
    v_2d += dvdt

    v_1d = dasu_v_1d(v_2d, v_1d, n)

    plt.xlim(0, 10)
    plt.ylim(-10, 70)
    iti_scatter = plt.scatter(iti_x, iti_y, c="blue")
    iti.append([iti_scatter])

#for i in range(time):

anim = animation.ArtistAnimation(fig, iti)
anim.save('kotu_1225_anim.gif', writer='writer', fps=4)

plt.show()
