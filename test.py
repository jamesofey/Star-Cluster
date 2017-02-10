import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os
import signal
import shutil


#def edit_encounter(k):
#    if k%2==0:
#        with open('/Users/jamesleepc/astroprogram/stage_{0}/big.in'.format(k), 'r') as wtf:
#            mess = wtf.readlines()
#            mess[22]=' ENCOUNTE   m=0. r=3.d0 d=1.\n'
#            mess[23]='  1000. 0. 0. \n'
#            mess[24]='  0. 0. 0. \n'
#        with open('/Users/jamesleepc/astroprogram/stage_{0}/big.in'.format(k), 'w') as fmbig:
#            fmbig.writelines(mess)

#    else:
#        with open('/Users/jamesleepc/astroprogram/stage_{0}/big.in'.format(k), 'r') as wtf:
#            mess = wtf.readlines()
#            mess[22]=' ENCOUNTE   m=1.447 r=3.d0 d=1.41\n'
#            mess[23]='  1414.213562 0. 0. \n'
#            mess[24]='  -3.052648534E-03 3.052648534E-03 0. \n'
#        with open('/Users/jamesleepc/astroprogram/stage_{0}/big.in'.format(k), 'w') as fmbig:
#            fmbig.writelines(mess)

#edit_encounter(3)
with open('/Users/jamesleepc/PycharmProjects/encounteringstar/inputtime.dat','r')as time_nodes:
    nodes_lis=time_nodes.readlines()


nodes_list=[]
for line in nodes_lis:
    line=line.strip('\n')
    nodes_list.append(line.strip().split()[0])

node=list(map(lambda element: float(element), nodes_list))
node=list(map(lambda element: 365.*element, node))

node_n=[0.]
loop=1
while loop<23:
    node_n.append(node[loop]-node[loop-1])
    loop=loop+1


with open('/Users/jamesleepc/PycharmProjects/encounteringstar/inputtime_n.dat','w')as wtf:
    for element in node_n:
        wtf.writelines('{0}\n'.format(element))



