import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# We want a sphere where we will plot the points and create the Julia set

# So far we are able to create a sphere and plot points on it, but how are we gonna fo from complex coordinates to polar coordinates?


# Let's create a function that converts a cartesian complex coordinate to polar coordinates:

def cartesian_to_polar(x, y, z):
    norm = z**2 + 1
    r = 2*x/norm
    theta = 2*y/norm
    phi = (norm - 2)/norm
    return r, theta, phi


a, b, c = cartesian_to_polar(3, -2, 16)




fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')



# Create sphere, same as before (kind of redundant, but works)
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = np.cos(u)*np.sin(v)
y = np.sin(u)*np.sin(v)
z = np.cos(v)
ax.plot_surface(x, y, z, color='c', alpha=0.05)



# Plot points on the sphere using polar coordinates



r = 10
theta = np.linspace(0, 2*np.pi, 100)
phi = np.linspace(0, np.pi, 100)
THETA, PHI = np.meshgrid(theta, phi)
X = r*np.sin(PHI)*np.cos(THETA)
Y = r*np.sin(PHI)*np.sin(THETA)
Z = r*np.cos(PHI)
ax.plot_wireframe(X, Y, Z, color='b')


# Set an equal aspect to the sphere
ax.set_aspect('equal')

#Displays the output sphere
plt.show()
