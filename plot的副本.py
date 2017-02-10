import numpy as np
import matplotlib.pyplot as plt
import subprocess

v_1=[]
N_1=[]

with open('/Users/jamesleepc/astroprogram/stage_2/thijstest.txt','r') as crs:
    for columns in ( raw.strip().split() for raw in crs ):
        v_1.append(columns[0])
        N_1.append(columns[1])
#    v_2.append(columns[2])
#    N_2.append(columns[3])
#    v_3.append(columns[4])
#    N_3.append(columns[5])
#    v_4.append(columns[6])
#    N_4.append(columns[7])

#del v_2[0]
#del N_2[0]
#del v_3[0]
#del N_3[0]
#del v_4[0]
#del N_4[0]

v_1 = list(map(float, v_1))
N_1 = list(map(float, N_1))
#v_2 = list(map(float, v_2))
#N_2 = list(map(float, N_2))
#v_3 = list(map(float, v_3))
#N_3 = list(map(float, N_3))
#v_4 = list(map(float, v_4))
#N_4 = list(map(float, N_4))

plt.plot(v_1,N_1,'r-')#,v_2,N_2,'yo',v_3,N_3,'bo',v_4,N_4,'go')
plt.show()
