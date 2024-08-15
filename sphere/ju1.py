import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numba import jit, prange

# Função que calcula o número de iterações para um ponto z no conjunto de Julia
@jit(nopython=True)
def julia_scalar(z, c, max_iter):
    n = 0  # Inicializa o contador de iterações
    # Itera até que o valor absoluto de z seja maior que 4 ou até atingir o número máximo de iterações
    while abs(z) <= 4 and n < max_iter:
        z = z*z + c  # Itera a fórmula z = z^2 + c
        n += 1  # Incrementa o contador de iterações
    return n  # Retorna o número de iterações

# Função que converte um número complexo z para um ponto (a, b, c) na esfera
@jit(nopython=True)
def complex_to_point(z):
    x = z.real  # Parte real do número complexo
    y = z.imag  # Parte imaginária do número complexo
    p = (x**2 + y**2)  # Calcula o quadrado da magnitude de z
    a = (2*x)/(p + 1)  # Converte x para coordenada a na esfera
    b = (2*y)/(p + 1)  # Converte y para coordenada b na esfera
    c = (p - 1)/(p + 1)  # Converte a magnitude para coordenada c na esfera
    return a, b, c  # Retorna as coordenadas (a, b, c)

# Função que calcula o conjunto de Julia e suas projeções em uma esfera
@jit(nopython=True, parallel=True)
def calculate_julia_set(Z, c, max_iter, resolution):
    a = np.empty((resolution, resolution), dtype=np.float64)  # Matriz para coordenadas a
    b = np.empty((resolution, resolution), dtype=np.float64)  # Matriz para coordenadas b
    c_ = np.empty((resolution, resolution), dtype=np.float64)  # Matriz para coordenadas c
    colors = np.empty((resolution, resolution), dtype=np.float64)  # Matriz para valores de iteração
    # Loop sobre cada ponto da matriz Z
    for i in prange(resolution):
        for j in prange(resolution):
            iter_count = julia_scalar(Z[i, j], c, max_iter)  # Calcula o número de iterações para o ponto Z[i, j]
            a_, b_, c_val = complex_to_point(Z[i, j])  # Converte o ponto complexo para coordenadas esféricas
            a[i, j] = a_  # Armazena coordenada a
            b[i, j] = b_  # Armazena coordenada b
            c_[i, j] = c_val  # Armazena coordenada c
            colors[i, j] = iter_count  # Armazena o número de iterações
    return a, b, c_, colors / max_iter  # Retorna as coordenadas e cores normalizadas

# Parâmetro c para o conjunto de Julia
c = complex(-0.7, 0.27015)  # Um valor comumente usado para Julia

# Configuração dos parâmetros
resolution = 800  # Resolução da imagem
x_min, x_max, y_min, y_max = -3.0, 3.0, -3.0, 3.0  # Intervalos dos eixos x e y
max_iter = 250  # Número máximo de iterações para o cálculo do Julia

# Cria uma malha de pontos no plano complexo
x = np.linspace(x_min, x_max, resolution)  # Pontos ao longo do eixo x
y = np.linspace(y_min, y_max, resolution)  # Pontos ao longo do eixo y
X, Y = np.meshgrid(x, y)  # Gera uma grade de coordenadas
Z = X + 1j * Y  # Cria a matriz de números complexos

# Calcula o conjunto de Julia e suas projeções
a, b, c, colors = calculate_julia_set(Z, c, max_iter, resolution)

# Configura a figura e o eixo para visualização 3D
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(111, projection='3d')

# Cria uma esfera vermelha para referência
u, v = np.mgrid[0:2*np.pi:100j, 0:np.pi:100j]
sphere_x = np.cos(u) * np.sin(v)
sphere_y = np.sin(u) * np.sin(v)
sphere_z = np.cos(v)
ax.plot_surface(sphere_x, sphere_y, sphere_z, color='r', alpha=0.1)

# Plota os pontos do conjunto de Julia na superfície da esfera
scatter = ax.scatter(a.flatten(), b.flatten(), c.flatten(), c=colors.flatten(), cmap='hot', s=1)

# Adiciona uma barra de cores para indicar o número de iterações
cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
cbar.set_label('Número de Iterações')

# Define a proporção igual para o eixo
ax.set_box_aspect([1, 1, 1])

# Adiciona rótulos e título
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Conjunto de Julia projetado em uma esfera com gradiente de cores')

# Mostra o gráfico
plt.show()
