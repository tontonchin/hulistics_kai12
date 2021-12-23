import numpy as np
import random
import math
from moussaif import fa_dasukai, hulistics_1, cal_fij, cal_fiw , dasu_v_1d, dvdt , alpha_dasu
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image
import pandas as pd
from pathlib import Path
import openpyxl
import xlrd

#読み取った


df = pd.read_excel("yomitori/MAF00069-04kaikiyousai.xlsx", sheet_name='Sheet3')
nmp=df.to_numpy()
syudan = nmp

np.set_printoptions(suppress=True)
syudan = np.delete(syudan, 0, axis=1)

n_kei = syudan.shape[0]

#syudan[:, 3] = syudan[:, 3] + 10.2
#syudan[:,4] = syudan[:,4] + 8.1

print("syudan.shape",syudan.shape)

n_nagasa = syudan.shape[0]

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

iti_x = []
iti_y = []

#print(syudan)
zikan = np.arange(200)/2


for i in range(n_kei):
    iti_x = []
    iti_y = []
    #print("あれこれ", i)
    n_i = 0
    xy_zikan = np.empty((0,2), int)
    for j in range(n_nagasa):
        #print(j)
        if syudan[j,0] == i:
            n_i += 1
            kozin_xy = syudan[j,3:5]
            print("kozin_xy",kozin_xy)
            kozin_xy = np.array([kozin_xy])
            #print("kozinn_xy", kozin_xy)
            #kozin_xy = np.array([syudan])
            xy_zikan = np.append(xy_zikan, kozin_xy, axis=0)
            #print("zikan",i )
            #print("集団", syudan[j,0])
    print(i,"時間目の",xy_zikan,"集団")
    iti_scatter = plt.scatter(xy_zikan[:,0],xy_zikan[:,1] ,c="red")
    iti.append([iti_scatter])

anim = animation.ArtistAnimation(fig, iti)

aaa = Path("hozon")
anim.save(aaa/'mati_zissaiMAF00069-04.gif', writer='writer', fps=120)

plt.show()

