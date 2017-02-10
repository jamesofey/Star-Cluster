import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os
import signal
import shutil

def makedir(k):
    os.chdir('/Users/jamesleepc/astroprogram')
    shutil.copytree('/Users/jamesleepc/astroprogram/original','/Users/jamesleepc/astroprogram/stage_{0}'.format(k))

def get_lastlist(filename):
    with open(filename) as j:
       last_j = None
       for line in (line for line in j if line.rstrip('\n')):
           last_j = line
    j_last=last_j.strip().split()
    return j_last

full_list=[]
with open('/Users/jamesleepc/PycharmProjects/encounteringstar/encounter.dat','r') as rangers_line:
    ranger_line=rangers_line.readlines()

for line in ranger_line:
    rangers = line.strip().split()
    full_list.append(rangers)

del full_list[0]

def edit_encounter(k):
    if k==1:
        with open('/Users/jamesleepc/astroprogram/original/big.in', 'r') as wtf:
            mess = wtf.readlines()
            mess[22]='\n'
            mess[23]='\n'
            mess[24]='\n'
            mess[25]='\n'
        with open('/Users/jamesleepc/astroprogram/original/big.in', 'w') as fmbig:
            fmbig.writelines(mess)
#    elif k%2==0:
#        with open('/Users/jamesleepc/astroprogram/stage_{0}/big.in'.format(k),'r') as wtf:
#            mess=wtf.readlines()
#            mess[22]=' ENCOUNTE   m={0} r=3.d0 d=1.41\n'.format(full_list[int(k/2)-1][6])
#            mess[23]='  {0} {1} {2} \n'.format(full_list[int(k/2)-1][0],full_list[int(k/2)-1][1],full_list[int(k/2)-1][2])
#            mess[24]='  {0} {1} {2} \n'.format(full_list[int(k / 2) - 1][3], full_list[int(k / 2) - 1][4],full_list[int(k / 2) - 1][5])
#            mess[25] = '   0. 0.  0.\n'
#        with open('/Users/jamesleepc/astroprogram/stage_{0}/big.in'.format(k), 'w') as fmbig:
#            fmbig.writelines(mess)
    else:
        with open('/Users/jamesleepc/astroprogram/stage_{0}/big.in'.format(k), 'r') as wtf:
            mess = wtf.readlines()
            mess[22]='\n'
            mess[23]='\n'
            mess[24]='\n'
            mess[25]='\n'
        with open('/Users/jamesleepc/astroprogram/stage_{0}/big.in'.format(k), 'w') as fmbig:
            fmbig.writelines(mess)

def judge_ejection(path1,path2):
    with open(path1, 'r') as info:
        info_l = info.readlines()
    ejected_planet = []
    for item in info_l:
        if 'ejected' in item:
            search_e = item.strip().split()
            ejected_planet.append(search_e[0])
    with open(path2,'r') as big:
        big_l=big.readlines()
    if len(ejected_planet)==0:
        return 0
    else:
        index_l = []
        for planet in ejected_planet:
            for item in big_l:
                if planet in item:
                    index_l.append(big_l.index(item))
        for pos in index_l:
            big_l[pos] = '\n'
            big_l[pos + 1] = '\n'
            big_l[pos + 2] = '\n'
            big_l[pos + 3] = '\n'
        with open(path2, 'w') as newb:
            newb.writelines(big_l)

def judge_collision(path1,path2):
    with open(path1, 'r') as info:
        info_l = info.readlines()
    survivor = []
    dead_planet=[]
    for item in info_l:
        if 'was hit' in item:
            search_e = item.strip().split()
            survivor.append(search_e[0])
            dead_planet.append(search_e[4])

    with open(path2,'r') as big:
        big_l=big.readlines()
    if len(dead_planet)==0:
        return 0
    else:
        index_d = []
        for planet in dead_planet:
            for item in big_l:
                if planet in item:
                    index_d.append(big_l.index(item))
        for pos in index_d:
            big_l[pos] = '\n'
            big_l[pos + 1] = '\n'
            big_l[pos + 2] = '\n'
            big_l[pos + 3] = '\n'

        index_s = []
        m_p = []
        d_p = []
        for planet in survivor:
            with open('{0}.aei'.format(planet),'r') as outol:
                out=outol.readlines()
                out_str=out[-1].strip().split()
                m_p.append(out_str[-2])
                d_p.append(out_str[-1])
            for item in big_l:
                if planet in item:
                    index_s.append(big_l.index(item))
        #print(index_s)
        for pos in index_s:
            big_l[pos] = ' {0}      m={1} r=3.d0 d={2}\n'.format(survivor[index_s.index(pos)],m_p[index_s.index(pos)],d_p[index_s.index(pos)])

        with open(path2, 'w') as newb:
            newb.writelines(big_l)


class Planet(object):

    def __init__(self, path1, path2):
        self.roughplanet=open(path1).readlines()
        open(path2,'w').writelines(self.roughplanet[4:])
        self.planet = open(path2, 'r')

    def columngrab(self):
        self.t = []
        self.e = []
        self.a = []
        self.i = []
        for columns in (raw.strip().split() for raw in self.planet):
            self.t.append(columns[0])
            self.e.append(columns[8])
            self.a.append(columns[7])
            self.i.append(columns[9])

    def getlastline(self):
        last_j = None
        for line in (line for line in self.roughplanet if line.rstrip('\n')):
            last_j = line
        self.lastline = last_j.strip().split()
        return self.lastline




def plot(t_j,e_j,a_j,i_j,t_s,e_s,a_s,i_s,t_u,e_u,a_u,i_u,t_n,e_n,a_n,i_n,k):
    plt.figure(1)
    plt.suptitle('Eccentricity versus time',fontsize=14, fontweight='bold')
    plt.subplot(221)
    plt.xlabel('Time(Yrs)')
    plt.ylabel('e')
    plt.plot(t_j,e_j,'r-')
    plt.subplot(222)
    plt.xlabel('Time(Yrs)')
    plt.ylabel('e')
    plt.plot(t_s,e_s,'r-')
    plt.subplot(223)
    plt.xlabel('Time(Yrs)')
    plt.ylabel('e')
    plt.plot(t_u,e_u,'r-')
    plt.subplot(224)
    plt.xlabel('Time(Yrs)')
    plt.ylabel('e')
    plt.plot(t_n,e_n,'r-')
    plt.savefig('/Users/jamesleepc/astroprogram/pics/comparison_e-t Stage{0}.png'.format(k))
    plt.figure(2)
    plt.suptitle('Semimajor versus time',fontsize=14, fontweight='bold')
    plt.subplot(221)
    plt.xlabel('Time(Yrs)')
    plt.ylabel('a')
    plt.plot(t_j,a_j,'r-')
    plt.subplot(222)
    plt.xlabel('Time(Yrs)')
    plt.ylabel('a')
    plt.plot(t_s,a_s,'r-')
    plt.subplot(223)
    plt.xlabel('Time(Yrs)')
    plt.ylabel('a')
    plt.plot(t_u,a_u,'r-')
    plt.subplot(224)
    plt.xlabel('Time(Yrs)')
    plt.ylabel('a')
    plt.plot(t_n,a_n,'r-')
    plt.savefig('/Users/jamesleepc/astroprogram/pics/comparison_a-t Stage{0}.png'.format(k))

    plt.figure(3)
    plt.suptitle('Inclination versus time',fontsize=14, fontweight='bold')
    plt.subplot(221)
    plt.xlabel('Time(Yrs)')
    plt.ylabel('i')
    plt.plot(t_j,i_j,'r-')
    plt.subplot(222)
    plt.xlabel('Time(Yrs)')
    plt.ylabel('i')
    plt.plot(t_s,i_s,'r-')
    plt.subplot(223)
    plt.xlabel('Time(Yrs)')
    plt.ylabel('i')
    plt.plot(t_u,i_u,'r-')
    plt.subplot(224)
    plt.xlabel('Time(Yrs)')
    plt.ylabel('i')
    plt.plot(t_n,i_n,'r-')
    plt.savefig('/Users/jamesleepc/astroprogram/pics/comparison_i-t Stage{0}.png'.format(k))
    plt.close('all')

with open('/Users/jamesleepc/PycharmProjects/encounteringstar/inputtime_n.dat','r')as time_nodes:
    nodes_lis=time_nodes.readlines()
nodes_list=[]
for line in nodes_lis:
    line=line.strip('\n')
    nodes_list.append(line.strip().split()[0])

loop=1
while loop<11:
    if loop==1:
        os.chdir('/Users/jamesleepc/astroprogram/original')
        with  open('/Users/jamesleepc/astroprogram/original/param.in', 'r') as pab:
            pab = pab.readlines()

        pab[6] = ' start time (days)={0}\n'.format(nodes_list[loop-1])
        pab[7] = ' stop time (days)={0}\n'.format(nodes_list[loop])

        with open('/Users/jamesleepc/astroprogram/original/param.in', 'w') as pran:
            pran.writelines(pab)

        edit_encounter(loop)
        p = subprocess.Popen('./cleanup', shell=True)
        subprocess.Popen.wait(p)
        jupiter = Planet('/Users/jamesleepc/astroprogram/original/JUPITER.aei',
                         '/Users/jamesleepc/astroprogram/original/Jupiterm.aei')
        jupiter.columngrab()
        t_j = jupiter.t
        e_j = jupiter.e
        a_j = jupiter.a
        i_j = jupiter.i

        saturn = Planet('/Users/jamesleepc/astroprogram/original/SATURN.aei',
                        '/Users/jamesleepc/astroprogram/original/Saturnm.aei')
        saturn.columngrab()
        t_s = saturn.t
        e_s = saturn.e
        a_s = saturn.a
        i_s = saturn.i

        uranus = Planet('/Users/jamesleepc/astroprogram/original/URANUS.aei',
                        '/Users/jamesleepc/astroprogram/original/Uranusm.aei')
        uranus.columngrab()
        t_u = uranus.t
        e_u = uranus.e
        a_u = uranus.a
        i_u = uranus.i

        neptune = Planet('/Users/jamesleepc/astroprogram/original/NEPTUNE.aei',
                         '/Users/jamesleepc/astroprogram/original/Neptunem.aei')
        neptune.columngrab()
        t_n = neptune.t
        e_n = neptune.e
        a_n = neptune.a
        i_n = neptune.i

        plot(t_j, e_j, a_j, i_j, t_s, e_s, a_s, i_s, t_u, e_u, a_u, i_u, t_n, e_n, a_n, i_n, 1)
        loop=loop+1
    else:
        makedir(loop)

        os.chdir('/Users/jamesleepc/astroprogram/stage_{0}'.format(loop))

        edit_encounter(loop)

        with open('/Users/jamesleepc/astroprogram/stage_{0}/big.in'.format(loop), 'r') as fbig:
            messbig = fbig.readlines()
        if loop==2:
            ju_stage_1 = get_lastlist('/Users/jamesleepc/astroprogram/original/JUPITER.aei')
            sa_stage_1 = get_lastlist('/Users/jamesleepc/astroprogram/original/SATURN.aei')
            ur_stage_1 = get_lastlist('/Users/jamesleepc/astroprogram/original/URANUS.aei')
            ne_stage_1 = get_lastlist('/Users/jamesleepc/astroprogram/original/NEPTUNE.aei')
        else:
            ju_stage_1 = get_lastlist('/Users/jamesleepc/astroprogram/stage_{0}/JUPITER.aei'.format(loop-1))
            sa_stage_1 = get_lastlist('/Users/jamesleepc/astroprogram/stage_{0}/SATURN.aei'.format(loop-1))
            ur_stage_1 = get_lastlist('/Users/jamesleepc/astroprogram/stage_{0}/URANUS.aei'.format(loop-1))
            ne_stage_1 = get_lastlist('/Users/jamesleepc/astroprogram/stage_{0}/NEPTUNE.aei'.format(loop-1))

        messbig[7] = ' {0} {1} {2}\n'.format(ju_stage_1[1], ju_stage_1[2], ju_stage_1[3])
        messbig[8] = ' {0} {1} {2}\n'.format(ju_stage_1[4], ju_stage_1[5], ju_stage_1[6])
        messbig[11] = ' {0} {1} {2}\n'.format(sa_stage_1[1], sa_stage_1[2], sa_stage_1[3])
        messbig[12] = ' {0} {1} {2}\n'.format(sa_stage_1[4], sa_stage_1[5], sa_stage_1[6])
        messbig[15] = ' {0} {1} {2}\n'.format(ur_stage_1[1], ur_stage_1[2], ur_stage_1[3])
        messbig[16] = ' {0} {1} {2}\n'.format(ur_stage_1[4], ur_stage_1[5], ur_stage_1[6])
        messbig[19] = ' {0} {1} {2}\n'.format(ne_stage_1[1], ne_stage_1[2], ne_stage_1[3])
        messbig[20] = ' {0} {1} {2}\n'.format(ne_stage_1[4], ne_stage_1[5], ne_stage_1[6])

        with open('/Users/jamesleepc/astroprogram/stage_{0}/big.in'.format(loop), 'w') as fmbig:
            fmbig.writelines(messbig)

        if loop==2:
            judge_collision('/Users/jamesleepc/astroprogram/original/info.out', '/Users/jamesleepc/astroprogram/stage_2/big.in')
            judge_ejection('/Users/jamesleepc/astroprogram/original/info.out', '/Users/jamesleepc/astroprogram/stage_2/big.in')
        else:
            judge_collision('/Users/jamesleepc/astroprogram/stage_{0}/info.out'.format(loop - 1), '/Users/jamesleepc/astroprogram/stage_{0}/big.in'.format(loop))
            judge_ejection('/Users/jamesleepc/astroprogram/stage_{0}/info.out'.format(loop-1),'/Users/jamesleepc/astroprogram/stage_{0}/big.in'.format(loop))

        with  open('/Users/jamesleepc/astroprogram/stage_{0}/param.in'.format(loop), 'r') as pab:
            pab = pab.readlines()

        pab[6] = ' start time (days)={0}\n'.format(nodes_list[0])
        pab[7] = ' stop time (days)={0}\n'.format(nodes_list[loop])

        with open('/Users/jamesleepc/astroprogram/stage_{0}/param.in'.format(loop), 'w') as pran:
            pran.writelines(pab)

        q = subprocess.Popen('./cleanup', shell=True)
        subprocess.Popen.wait(q)
        jupiter = Planet('/Users/jamesleepc/astroprogram/stage_{0}/JUPITER.aei'.format(loop),
                         '/Users/jamesleepc/astroprogram/stage_{0}/Jupiterm.aei'.format(loop))
        jupiter.columngrab()
        t_j = jupiter.t
        e_j = jupiter.e
        a_j = jupiter.a
        i_j = jupiter.i

        saturn = Planet('/Users/jamesleepc/astroprogram/stage_{0}/SATURN.aei'.format(loop),
                        '/Users/jamesleepc/astroprogram/stage_{0}/Saturnm.aei'.format(loop))
        saturn.columngrab()
        t_s = saturn.t
        e_s = saturn.e
        a_s = saturn.a
        i_s = saturn.i

        uranus = Planet('/Users/jamesleepc/astroprogram/stage_{0}/URANUS.aei'.format(loop),
                        '/Users/jamesleepc/astroprogram/stage_{0}/Uranusm.aei'.format(loop))
        uranus.columngrab()
        t_u = uranus.t
        e_u = uranus.e
        a_u = uranus.a
        i_u = uranus.i

        neptune = Planet('/Users/jamesleepc/astroprogram/stage_{0}/NEPTUNE.aei'.format(loop),
                         '/Users/jamesleepc/astroprogram/stage_{0}/Neptunem.aei'.format(loop))
        neptune.columngrab()
        t_n = neptune.t
        e_n = neptune.e
        a_n = neptune.a
        i_n = neptune.i

        plot(t_j, e_j, a_j, i_j, t_s, e_s, a_s, i_s, t_u, e_u, a_u, i_u, t_n, e_n, a_n, i_n, loop)
        loop = loop + 1