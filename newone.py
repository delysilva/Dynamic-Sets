import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


# our origin is z = 0 + 0j
def complex_to_point(z):
    x = z.real
    y = z.imag
    p = (x**2 + y**2)

    a = (2*x)/(p + 1)
    b = (2*y)/(p + 1)
    c = (p - 1)/(p + 1)

    return a, b, c

# Set up the figure and axes

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')



# Create sphere, same as before (kind of redundant, but works) RED

u, v = np.mgrid[0:2*np.pi:100j, 0:np.pi:100j]

x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)


ax.plot_surface(x, y, z, color='r', alpha = 0.4,antialiased=True)



# Plot points on the sphere using polar coordinates BLUE

#for d in range(-200, 200, 1):
#    for l in range(-200, 200, 1):
#        z = (d + 0j) + l*(0 + 1j)
#        a, b, c = complex_to_point(z)
#        ax.plot_surface(a, b, c, color='g', alpha=0.8, antialiased=True)


# we're gonna plot points that satisfies the equation z = d + li, where d and l are integers that go from -200 to 200 with a 0.1 step using mgrid
d, l = np.mgrid[-200:200:1, -200:200:1]
z = d + l*1j
# we need to take eache part and convert it to a point on the sphere
a, b, c = complex_to_point(z)

ax.plot_surface(a, b, c, color='g', antialiased=False)

# Set an equal aspect to the sphere
ax.set_aspect('equal')

#Displays the output sphere 
plt.show()





# We will have a Z = x + iy, where x and y are the real and imaginary parts of the complex number z




# FIXME - (I'LL BE BACK LATER, FIRST MAKE SURE EVERYTHING ABOVE IT WORKS) We will have a function that takes a complex number z and returns the corresponding point on the sphere



# FIXME - (IMPORTANT, keep it as backup plan) I guess we may have a problem when plotting a lot of points on the sphere (speaking of memory) [so we may have to plot the points in batches - Git Copilot][--> for instance, ill desagree with this, but we can try to plot the points in a 2D plane, and then project them to the sphere]