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



#AS ALTERAÇÕES ABAIXO SÃO AS QUE EU FIZ, E QUE FUNCIONARAM

d, l = np.mgrid[-200:200:0.1, -200:200:0.1] #o mgrid cria uma matriz com os valores de d e l, que vão de -200 a 200 com um step de 0.1, resultando em uma matriz 4000x4000

z1 = d + l*1j # z é o nosso número complexo, que vai de -200 - 200i até 200 + 200i, z também é uma mgrid que vai de -200 - 200i até 200 + 200i, ou seja z é uma matriz 4000x4000

a, b, c = complex_to_point(z1) # aplicamos a função complex_to_point para cada valor de z, e armazenamos os valores em a, b e c. que são as coordenadas X, Y e Z dos pontos que vamos plotar

# plotamos os pontos na esfera
ax.plot_surface(a, b, c, color='g', antialiased=False)

# Set an equal aspect to the sphere
ax.set_aspect('equal')

#Displays the output sphere 
plt.show()





# We will have a Z = x + iy, where x and y are the real and imaginary parts of the complex number z




# FIXME - (I'LL BE BACK LATER, FIRST MAKE SURE EVERYTHING ABOVE IT WORKS) We will have a function that takes a complex number z and returns the corresponding point on the sphere



# FIXME - (IMPORTANT, keep it as backup plan) I guess we may have a problem when plotting a lot of points on the sphere (speaking of memory) [so we may have to plot the points in batches - Git Copilot][--> for instance, ill desagree with this, but we can try to plot the points in a 2D plane, and then project them to the sphere]