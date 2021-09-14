
import numpy as np
import random
import math
from moussaif import fa_dasukai, hulistics_1, cal_fij, cal_fiw , dasu_v_1d, dvdt
import matplotlib.pyplot as plt
import matplotlib.animation as animation

x1 = 0

car1 = np.matrix([[x1,9],
                [x1,6],
                [x1-4,9],
                [x1-4, 6]
            ])



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


for j in range(10):

    #車は秒ごとに3m動くとする
    v = 3
    v_san = np.array([v*math.cos(0), v*math.sin(0)])
    dv = np.matrix([[v_san[0],v_san[1]],
                      [v_san[0],v_san[1]],
                      [v_san[0],v_san[1]],
                      [v_san[0],v_san[1]]
                      ])

    car1 = car1 + dv

    ax.axhline(car1[0,1], xmin=0.2, xmax=0.8, color="black")
    ax.axhline(car1[1,1], xmin=0.2, xmax=0.8, color="black")
    plt.show()


#anim = animation.ArtistAnimation(fig)
#anim.save('car1.gif', writer='writer', fps=4)

#plt.show()
