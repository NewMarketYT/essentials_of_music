import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# wave speed
c = 1

# spatial domain
xmin = 0
xmax = 1

n = 50 # num of grid points

# x grid of n points
X, dx = np.linspace(xmin,xmax,n,retstep=True)

# for CFL of 0.1
dt = 0.1*dx/c

# initial conditions
def initial_u(x):
    return np.exp(-0.5*np.power(((x-0.5)/0.08), 2))

# each value of the U array contains the solution for all x values at each timestep
U = []

# explicit euler solution
def u(x, t):
    if t == 0: # initial condition
        return initial_u(x)
    uvals = [] # u values for this time step
    for j in range(len(x)):
        if j == 0: # left boundary
            uvals.append(U[t-1][j] + c*dt/(2*dx)*(U[t-1][j+1]-U[t-1][n-1]))
        elif j == n-1: # right boundary
            uvals.append(U[t-1][j] + c*dt/(2*dx)*(U[t-1][0]-U[t-1][j-1]))
        else:
            uvals.append(U[t-1][j] + c*dt/(2*dx)*(U[t-1][j+1]-U[t-1][j-1]))
    return uvals

# solve for 500 time steps
for t in range(500):
    U.append(u(X, t))

# plot solution
plt.style.use('dark_background')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

# animate the time data
k = 0
def animate(i):
    global k
    x = U[k]
    k += 1
    ax1.clear()
    plt.plot(X,x,color='cyan')
    plt.grid(True)
    plt.ylim([-2,2])
    plt.xlim([0,1])

anim = animation.FuncAnimation(fig,animate,frames=360,interval=20)
plt.show()

