import numpy as np

time=[]

with open('/Users/jamesleepc/Documents/Astrnomy/list.planets/encounters_of_star_0423','r') as star_list:
    star_chart=star_list.readlines()


for line in star_chart:
    line_b=line.strip().split()
    time.append(line_b[0])

del time[0]
del time[0]

time=list(map(float,time))

time=list(map(lambda x: x*1000000,time))
print(time)
period=[46317.,30928.,25240.,24577.,15921.,16270.,17996.,20312.,10201.,56833.,36480.]
period=list(map(lambda x: x*0.5,period))

loop_1=0
while loop_1<11:
    time[2*loop_1]=time[2*loop_1+1]-period[loop_1]
    time[2*loop_1+1]=time[2*loop_1+1]+period[loop_1]+5000.
    loop_1=loop_1+1
print(len(time))
print(time)
with open('inputtime.dat','w') as node:
    for element in time:
        node.writelines('{0}\n'.format(element))