from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator
import matplotlib.pyplot as plt
import numpy as np
import argparse
# import re
# result = re.sub(p, subst, test_str)
# p = re.compile(ur'(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+\d')
regexp = r'(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+\d'

parser = argparse.ArgumentParser(description='Displays a Figure of Mesh Points TxtFile X Y Z Newline', epilog='''   	
   	-0.100     1.000     4.900\n
   	-0.100     2.141     5.081\n
   	-0.100     3.282     5.262\n
   	''')
parser.add_argument('filename',help='300.txt')
args = parser.parse_args()

print("~ Filename: {}".format(args.filename))

# fig = plt.figure(num=None, figsize=(12, 6), dpi=120, facecolor='w', edgecolor='k')
# ax = fig.gca(projection='3d')
#       
#        x = np.fromregex(c, r"(\d+)\s+...", dt)
dt = np.dtype([	('X', np.float),
				('Y',  np.float), 
				('Z', np.float)])
data = np.fromregex(args.filename,regexp,dt)
# data = np.genfromtxt(args.filename)
x = data['X']
y = data['Y']
z = data['Z']
# print data

print x
print y
print z

for xv in x:
	for yv in y:
		for zv in z:
			print " ", xv + "  " + yv + "  " + zv
	
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.plot_wireframe(x, y, z, rstride=5, cstride=5)
ax.scatter(x, y, z, c='r', marker='+')

plt.show()