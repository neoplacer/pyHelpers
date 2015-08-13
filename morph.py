from numpy import *
from matplotlib.pyplot import *
from WaveBlocksND import *
from WaveBlocksND.Plot3D import *
from mayavi import mlab

I = eye(2)

N = 500
G = TensorProductGrid([(-1.5,1.5), (-1.5,1.5)], [N,N])
X, Y = vsplit(G.get_nodes(), 2)
X = X.reshape(N,N)
Y = Y.reshape(N,N)

K = HyperCubicShape([5,5])

HAWP = HagedornWavepacket(2, 1, 0.2)
HAWP.set_basis_shapes([K])
HAWP.set_coefficient(0, (2,3), 1.0)

for i, alpha in enumerate(linspace(0, 2, 61)):
    print(alpha)

    Q = I + alpha*fliplr(I)*1.0j
    P = 1.0j*I
    print(dot(conj(Q.T), P) - dot(conj(P.T), Q))
    print(dot(P.T, Q) - dot(Q.T, P))

    HAWP.set_parameters([Q,P], key=("Q","P"))

    psi = HAWP.evaluate_at(G, prefactor=True)[0]
    psi = psi.reshape(N,N)

    surfcf(X, Y, angle(psi), abs(psi))
    mlab.savefig("test2_" + str(i).zfill(3) + ".png")
    mlab.close()

mlab.show()