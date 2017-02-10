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
    #return id


with open('/Users/jamesleepc/Documents/Astrnomy/list.planets/encounters_of_star_0423','r') as star_list:
    star_chart=star_list.readlines()

loop_k=1
m_chart=[]
r_pchart=[]
v_pchart=[]
full_list=[]


while loop_k<12:
    spliter=star_chart[2*loop_k+1].strip().split()
    m_chart.append(float(spliter[5]))
    r_pchart.append(float(spliter[6]))
    v_pchart.append(float(spliter[9]))
    loop_k=loop_k+1



loop_j=0
while loop_j<11:
    #read data
    m = m_chart[loop_j]
    r_p = r_pchart[loop_j]
    v_p = v_pchart[loop_j] * 0.2108
    #orbit parameter
    e = (((v_p) ** 2) * (r_p)) / (4 * ((np.pi) ** 2) * (1+m)) - 1
    a = r_p / (e - 1)
    l = r_p * v_p
    #Euler solver
    steps=60000
    t = np.linspace(0, 30000, steps+1)
    dt = 30000./steps
    theta_p=[0.]
    loop_s=0
    while loop_s<steps:
        tmp=l*(1+e*np.cos(theta_p[loop_s]))*(1+e*np.cos(theta_p[loop_s]))/(a*a*(e*e-1)*(e*e-1))
        theta_p.append(tmp*dt+ theta_p[loop_s])
        loop_s=loop_s+1

    r = (a * ((e ** 2) - 1)) / (1 + e * np.cos(theta_p))
    x = r * (np.cos(theta_p))
    y = r * (np.sin(theta_p))
    v_x = [0]
    v_y = [v_p]
    loop = 1
    while loop < (steps+1):
        v_x.append((x[loop] - x[loop - 1]) / dt)
        v_y.append((y[loop] - y[loop - 1]) / dt)
        loop = loop + 1
    #print(r)
    loop_1 = 0
    while loop_1 < (steps+1):
        if r[loop_1] > 10000.:
            esc_index = loop_1
            break
        else:
            loop_1 = loop_1 + 1

    vx_en = -v_x[esc_index]/(365.25)
    vy_en = -v_y[esc_index]/(365.25)
    x_en = x[esc_index]
    y_en = y[esc_index]
    r_en=r[esc_index]
    t_en=2*t[esc_index]
    print(t[esc_index])
    print(t_en)
    m_en=m

    v_random = np.matrix([[vx_en], [vy_en], [0]])
    r_random = np.matrix([[x_en], [y_en], [0]])

    matrix = randommatrix()
    v_random = matrix * v_random
    v_randomn=v_random.T
    v_randomn=v_randomn.tolist()[0]
    r_random = matrix * r_random
    r_randomn=r_random.T
    r_randomn=r_randomn.tolist()[0]

    theta_0=np.linspace(0,np.pi/2,10001)
    x_0=10000.*np.cos(theta_0)
    y_0=10000.*np.sin(theta_0)

    plt.plot(x,y,x_0,y_0)
    plt.savefig('test_{0}'.format(loop_j))
    plt.close()
    full_list.append([r_randomn,v_randomn,t_en,m_en,r_en])
    #print(loop_j)
    loop_j=loop_j+1

print(len(full_list))
for element in full_list:
    print(element)

loop_l=0
with open('encounter.dat','w') as enter:
    while loop_l<12:
        if loop_l==0:
            enter.writelines('x y   z   vx  vy  vz  m r_esc\n')
        else:
            enter.writelines('{0}   {1} {2} {3} {4} {5} {6}\n'.format(full_list[loop_l-1][0][0],full_list[loop_l-1][0][1],full_list[loop_l-1][0][2],full_list[loop_l-1][1][0],full_list[loop_l-1][1][1],full_list[loop_l-1][1][2],full_list[loop_l-1][3],full_list[loop_l-1][4]))
        loop_l=loop_l+1

loop_d=0
with open('inputtime.dat','w') as wtf:
    while loop_d<12:
        if loop_d==0:
            wtf.writelines('0.\n')
        else:
            wtf.writelines('{0}\n'.format(full_list[loop_d-1][2]))
        loop_d=loop_d+1
