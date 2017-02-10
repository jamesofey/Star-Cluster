import subprocess
import numpy as np
import matplotlib.pyplot as plt
import os
import signal
import shutil

def makedir(k):
    os.chdir('/Users/jamesleepc/astroprogram')
    shutil.copytree('/Users/jamesleepc/astroprogram/planet_nine','/Users/jamesleepc/astroprogram/planetnine_{0}'.format(k))

def get_lastlist(filename):
    with open(filename) as j:
       last_j = None
       for line in (line for line in j if line.rstrip('\n')):
           last_j = line
    j_last=last_j.strip().split()
    return j_last

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
            self.t.append(float(columns[0])/1000.)
            self.e.append(np.sqrt(1-float(columns[2])**2))
            self.a.append(np.log(float(columns[1])))
            self.i.append(np.cos(float(columns[3])))

    def getlastline(self):
        last_j = None
        for line in (line for line in self.roughplanet if line.rstrip('\n')):
            last_j = line
        self.lastline = last_j.strip().split()
        return self.lastline


def plot(t_j,e_j,a_j,i_j,t_s,e_s,a_s,i_s,t_u,e_u,a_u,i_u,t_n,e_n,a_n,i_n,k,planet_1,planet_2,planet_3,planet_4):
    plt.figure(1)
    plt.suptitle('Eccentricity versus time',fontsize=14, fontweight='bold')
    plt.subplot(221)
    plt.xlabel('Time(KYrs)')
    plt.ylabel(r'$\sqrt{1-e^2}$',rotation=0)
    plt.plot(t_j,e_j,'r-',label=planet_1)
    plt.legend(loc='best')
    plt.subplot(222)
    plt.xlabel('Time(KYrs)')
    plt.ylabel(r'$\sqrt{1-e^2}$',rotation=0)
    plt.plot(t_s,e_s,'r-',label=planet_2)
    plt.legend(loc='best')
    plt.subplot(223)
    plt.xlabel('Time(KYrs)')
    plt.ylabel(r'$\sqrt{1-e^2}$',rotation=0)
    plt.plot(t_u,e_u,'r-',label=planet_3)
    plt.legend(loc='best')
    plt.subplot(224)
    plt.xlabel('Time(KYrs)')
    plt.ylabel(r'$\sqrt{1-e^2}$',rotation=0)
    plt.plot(t_n,e_n,'r-',label=planet_4)
    plt.legend(loc='best')
    plt.savefig('/Users/jamesleepc/astroprogram/pics_fornine/e-t for {0}.png'.format(k))
    plt.figure(2)
    plt.suptitle('Semimajor versus time',fontsize=14, fontweight='bold')
    plt.subplot(221)
    plt.xlabel('Time(KYrs)')
    plt.ylabel('a')
    plt.plot(t_j,a_j,'r-',label=planet_1)
    plt.legend(loc='best')
    plt.subplot(222)
    plt.xlabel('Time(KYrs)')
    plt.ylabel('a')
    plt.plot(t_s,a_s,'r-',label=planet_2)
    plt.legend(loc='best')
    plt.subplot(223)
    plt.xlabel('Time(KYrs)')
    plt.ylabel('a')
    plt.plot(t_u,a_u,'r-',label=planet_3)
    plt.legend(loc='best')
    plt.subplot(224)
    plt.xlabel('Time(KYrs)')
    plt.ylabel('a')
    plt.plot(t_n,a_n,'r-',label=planet_4)
    plt.legend(loc='best')
    plt.savefig('/Users/jamesleepc/astroprogram/pics_fornine/a-t for {0}.png'.format(k))

    plt.figure(3)
    plt.suptitle('Inclination versus time',fontsize=14, fontweight='bold')
    plt.subplot(221)
    plt.xlabel('Time(KYrs)')
    plt.ylabel('i')
    plt.plot(t_j,i_j,'r-',label=planet_1)
    plt.legend(loc='best')
    plt.subplot(222)
    plt.xlabel('Time(KYrs)')
    plt.ylabel('i')
    plt.plot(t_s,i_s,'r-',label=planet_2)
    plt.legend(loc='best')
    plt.subplot(223)
    plt.xlabel('Time(KYrs)')
    plt.ylabel('i')
    plt.plot(t_u,i_u,'r-',label=planet_3)
    plt.legend(loc='best')
    plt.subplot(224)
    plt.xlabel('Time(KYrs)')
    plt.ylabel('i')
    plt.plot(t_n,i_n,'r-',label=planet_4)
    plt.legend(loc='best')
    plt.savefig('/Users/jamesleepc/astroprogram/pics_fornine/i-t for {0}.png'.format(k))
    plt.close('all')

os.chdir('/Users/jamesleepc/astroprogram/planet_nine')
with  open('/Users/jamesleepc/astroprogram/planet_nine/param.in', 'r') as pab:
    pab = pab.readlines()

pab[6] = ' start time (days)=0\n'
pab[7] = ' stop time (days)=36525000.\n'

with open('/Users/jamesleepc/astroprogram/planet_nine/param.in', 'w') as pran:
    pran.writelines(pab)

#p = subprocess.Popen('./cleanup', shell=True)
#subprocess.Popen.wait(p)

mercury = Planet('/Users/jamesleepc/astroprogram/planet_nine/MERCURY.aei',
                 '/Users/jamesleepc/astroprogram/planet_nine/Mercurym.aei')
mercury.columngrab()
t_m = mercury.t
e_m = mercury.e
a_m = mercury.a
i_m = mercury.i

venus = Planet('/Users/jamesleepc/astroprogram/planet_nine/VENUS.aei',
               '/Users/jamesleepc/astroprogram/planet_nine/Venusm.aei')
venus.columngrab()
t_v = venus.t
e_v = venus.e
a_v = venus.a
i_v = venus.i

earth = Planet('/Users/jamesleepc/astroprogram/planet_nine/EARTHMOO.aei',
               '/Users/jamesleepc/astroprogram/planet_nine/Earthm.aei')
earth.columngrab()
t_e = earth.t
e_e = earth.e
a_e = earth.a
i_e = earth.i

mars = Planet('/Users/jamesleepc/astroprogram/planet_nine/MARS.aei',
              '/Users/jamesleepc/astroprogram/planet_nine/Marsm.aei')
mars.columngrab()
t_ma = mars.t
e_ma = mars.e
a_ma = mars.a
i_ma = mars.i

jupiter = Planet('/Users/jamesleepc/astroprogram/planet_nine/JUPITER.aei',
                 '/Users/jamesleepc/astroprogram/planet_nine/Jupiterm.aei')
jupiter.columngrab()
t_j = jupiter.t
e_j = jupiter.e
a_j = jupiter.a
i_j = jupiter.i

saturn = Planet('/Users/jamesleepc/astroprogram/planet_nine/SATURN.aei',
                '/Users/jamesleepc/astroprogram/planet_nine/Saturnm.aei')
saturn.columngrab()
t_s = saturn.t
e_s = saturn.e
a_s = saturn.a
i_s = saturn.i

uranus = Planet('/Users/jamesleepc/astroprogram/planet_nine/URANUS.aei',
                '/Users/jamesleepc/astroprogram/planet_nine/Uranusm.aei')
uranus.columngrab()
t_u = uranus.t
e_u = uranus.e
a_u = uranus.a
i_u = uranus.i

neptune = Planet('/Users/jamesleepc/astroprogram/planet_nine/NEPTUNE.aei',
                 '/Users/jamesleepc/astroprogram/planet_nine/Neptunem.aei')
neptune.columngrab()
t_n = neptune.t
e_n = neptune.e
a_n = neptune.a
i_n = neptune.i

pluto = Planet('/Users/jamesleepc/astroprogram/planet_nine/PLUTO.aei',
               '/Users/jamesleepc/astroprogram/planet_nine/Plutom.aei')
pluto.columngrab()
t_p = pluto.t
e_p = pluto.e
a_p = pluto.a
i_p = pluto.i

ninth = Planet('/Users/jamesleepc/astroprogram/planet_nine/NINTH.aei',
               '/Users/jamesleepc/astroprogram/planet_nine/Ninthm.aei')
ninth.columngrab()
t_ni = ninth.t
e_ni = ninth.e
a_ni = ninth.a
i_ni = ninth.i

plot(t_m, e_m, a_m, i_m, t_v, e_v, a_v, i_v, t_e, e_e, a_e, i_e, t_ma, e_ma, a_ma, i_ma, 'Inner Run','Mercury','Venus','Earth','Mars')
plot(t_j, e_j, a_j, i_j, t_s, e_s, a_s, i_s, t_u, e_u, a_u, i_u, t_n, e_n, a_n, i_n, 'Giants Run','Jupiter','Saturn','Uranus','Neptune')
plot(t_p, e_p, a_p, i_p, t_ni, e_ni, a_ni, i_ni, [0], [0], [0], [0], [0], [0], [0], [0], 'Kuiper Run','Pluto','Planet Nine','Null','Null')



