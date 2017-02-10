import numpy as np
#from mpmath import mp,fp
import matplotlib.pyplot as plt

#mp.dps=50

v_p=1.603

e=13.013968548546474811
a=548.88865185166675105
l=2228.3062146044000552

def f(theta):
    tmp=l*(1+e*np.cos(theta))*(1+e*np.cos(theta))/(a*a*(e*e-1)*(e*e-1))
    return tmp

steps=50000
t = np.linspace(0, 10000, steps+1)
dt = 10000. / (steps)
theta_p=[0.]
loop_s=0
while loop_s<steps:
    k_1=f(theta_p[loop_s])
    k_2=f(theta_p[loop_s]+(dt*k_1/2))
    k_3=f(theta_p[loop_s]+(dt*k_2/2))
    k_4 = f(theta_p[loop_s] + dt * k_3)
    tmp=theta_p[loop_s]+((dt*(k_1+2*k_2+2*k_3+k_4)/6))
    theta_p.append(tmp)
    loop_s=loop_s+1

print(theta_p)
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

loop_1 = 0
while loop_1 < (steps+1):
    if r[loop_1] > 10000.:
        esc_index = loop_1
        break
    else:
        loop_1 = loop_1 + 1

#vx_en = -v_x[esc_index]
#vy_en = -v_y[esc_index]
#x_en = x[esc_index]
#y_en = y[esc_index]
#t_en=2*t[esc_index]



plt.plot(x,y)
plt.savefig('test')
plt.close()

