'''
This script uses the Poisson's equation in a 2D grid with a charge distribution to simulate  mountains and a rift. 
'''
import numpy as np
import matplotlib.pyplot as plt
from IPython import get_ipython

get_ipython().run_line_magic('matplotlib', 'qt5')

# define grid dimensions
a = 50
b = 55

# create the x-y meshgrid and the initial array (V)
x, y = np.linspace(0, b-1, b), np.linspace(0, a-1, a)
X, Y = np.meshgrid(x, y)
V = np.random.random([a, b]) #initial array w/ random values

# boundary conditions
V[0] = np.sin(2*np.pi*x/a) # first row of V
V[a-1] = np.cos(2*np.pi*x/a) #last row of V
V[:,0] = 0 # first column
V[:,b-1] = 0 # last column
q = 10

# define charge distribution function
def charge(xo,yo, sigma2=1):
    return np.cos(-((X-xo)**2+(Y-yo)**2)/2/sigma2)

rho = - charge(a/3, b/2) + charge(2*a/3, b/2) - charge(5*a/2, b/3) + charge(5*a/2, b/4)
 
## set a low threshold for q
while q>10**(-6):
    A = np.copy(V)
    q = 0.0
    for i in range(1, a-1):
        for j in range(1, b-1):
            # each point is the average of its four neighbors
            A[i, j] = ( V[i+1,j] + V[i-1,j] + V[i,j-1] + V[i,j+1] + rho[i,j])/4
            # q is a measure of the differences between two frames
            q += (A[i, j]-V[i, j])**2
            print(q)
    V = np.copy(A)

#plotting
fig, ax = plt.subplots(subplot_kw={'projection':'3d'})
surf1 = ax.plot_surface(X, Y, V, cmap='twilight')
plt.show()