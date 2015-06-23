from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib.pyplot as plt
from matplotlib.mlab import griddata
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='Displays a Figure of Mesh Points TxtFile X Y Z Newline', epilog='''   	
   	-0.100     1.000     4.900\n
   	-0.100     2.141     5.081\n
   	-0.100     3.282     5.262\n
   	''')
parser.add_argument('filename',help='300.txt')
args = parser.parse_args()

print("~ Filename: {}".format(args.filename))

fig = plt.figure(num=None, figsize=(12, 6), dpi=120, facecolor='w', edgecolor='k')
# ax = fig.gca(projection='3d')

data = np.genfromtxt(args.filename)
x = data[:,0]
y = data[:,1]
z = data[:,2]

# xi = np.linspace(min(x), max(x))
# yi = np.linspace(min(y), max(y))

# X, Y = np.meshgrid(xi, yi)
# Z = griddata(x, y, z, xi, yi)

# surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=cm.jet,
                       # linewidth=1, antialiased=False)

ax = fig.add_subplot(111, projection='3d')
# X, Y, Z = Axes3D.get_test_data(0.05)
# ax.plot_wireframe(x, y, z, rstride=1, cstride=1)
# ax.plot_trisurf(x, y, z, cmap=cm.Greys, linewidth=0.2)
# ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=cm.YlGnBu_r)
# ax.plot_surface(x, y, z,  rstride=4, cstride=4, color='b')
ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=cm.YlGnBu_r)
# ax.set_zlim3d(np.min(Z), np.max(Z))
# fig.colorbar(surf)

plt.show()