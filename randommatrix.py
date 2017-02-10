import numpy as np
import random
import matplotlib.pyplot as plt
def randommatrix():
    x_1 = random.random()
    x_2 = random.random()
    x_3 = random.random()

    R = np.matrix(
        [[np.cos(2 * np.pi * x_1), np.sin(2 * np.pi * x_1), 0], [-np.sin(2 * np.pi * x_1), np.cos(2 * np.pi * x_1), 0],
         [0, 0, 1]])
    # print(R)

    v_rt = np.matrix([np.cos(2 * np.pi * x_2) * np.sqrt(x_3), np.sin(2 * np.pi * x_2) * np.sqrt(x_3), np.sqrt(1 - x_3)])
    v_r = v_rt.T
    id = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])

    H = id - 2 * v_r * v_rt
    M = -H * R
    return M

u=np.matrix([[1],[0],[0]])

loop=1
phi=[]
theta=[]
while loop<100000:
    ml=randommatrix()
    ru=ml*u
    r_tmp=np.reshape(ru,3)
    rl=r_tmp.tolist()
    phi.append(np.arccos(rl[0][2]))
    tmp=np.sqrt(1-(rl[0][2])**2)
    theta.append(np.arccos(rl[0][0]/tmp))
    loop=loop+1

plt.hist(theta,bins=100,normed=1)
plt.show()
