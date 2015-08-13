from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y, Z = <array<[[3403.591972, 909.970061,4126.497142],[3403.121842,2505.129693,4428.462883],[3402.631172,4234.205289,4743.622134],[3402.301302,5425.507511,4955.498579],[3401.976419,6615.784131,5164.172009]]>>
ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)

plt.show()

