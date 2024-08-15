import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from numba import jit
import random

k = input("Digite o valor de k: ")
k = int(k)
n = input("Digite o valor de n: ")
n = int(n)

c = complex(-0.8, 0.156)

# Parâmetros para gerar a imagem
largura = 1200
altura = 1200
max_iter = 256
xmin, xmax, ymin, ymax = -2.0, 1.0, -1.5, 1.5
julia_xmin, julia_xmax, julia_ymin, julia_ymax = -2.0, 2.0, -2.0, 2.0
julia_largura = 1200
julia_altura = 1200
flag = False


# Lista global para armazenar referências dos círculos
pre_image_circles = []

# Variáveis globais para controle de navegação
pre_images_points = []
current_index = 0

# Função que realiza a iteração de Julia
@jit
def iteracao_julia(c, i):
    z = (c * c) + i
    return z

# Função que gera o conjunto de Julia
@jit
def julia(c, max_iter, i):
    z = iteracao_julia(c, i)
    for n in range(max_iter):
        if abs(z) > 5:
            return n
        z = iteracao_julia(z, i)
    return max_iter

# Função que gera o conjunto de Julia
@jit
def gerar_conjunto_julia(largura, altura, xmin, xmax, ymin, ymax, max_iter, i):
    imagem = np.zeros((altura, largura))
    for x in range(largura):
        for y in range(altura):
            real = xmin + (x / (largura - 1)) * (xmax - xmin)
            imag = ymax - (y / (altura - 1)) * (ymax - ymin)
            c = complex(real, imag)
            cor = julia(c, max_iter, i)
            imagem[y, x] = cor
    return imagem

def choose():
    i = random.randint(0, 1)
    return i

# Função que gera os pre-imagens de um ponto z
@jit
def pre_images(z, c):
    global k
    global n
    global pre_images_points
    vetor = [z]
    ans = []
    for i in range(n):
        a = len(vetor)
        for j in range(a):
            p = vetor.pop()
            coeff = [1, 0, c-p]
            roots = np.roots(coeff)
            w = roots[choose()]
            vetor.append(w)
           
            if(i >= k - 1):
                ans.append(w)

    return ans

#####################################################################################################

# Função que desenha os pontos das pré-imagens
@jit
def draw_pre_images(points):
    global pre_image_circles
    ax = plt.gca()
    x = len(points)
    for i in range(x):
        point = points[i]
        circle = plt.Circle((point.real, point.imag), radius=(0.009), color='blue', fill=True)
        ax.add_patch(circle)
        pre_image_circles.append(circle)
    plt.draw()

# Função que remove os círculos das pré-imagens
def clear_pre_images():
    global pre_image_circles
    ax = plt.gca()
    for circle in pre_image_circles:
        circle.remove()
    pre_image_circles = []
    pre_images_points = []
    
    plt.draw()


# Função que atualiza a imagem
def update(xmin, xmax, ymin, ymax):
    global largura, altura, max_iter
    im = gerar_conjunto_julia(largura, altura, xmin, xmax, ymin, ymax, max_iter, complex(-0.8, 0.156))
    plt.imshow(im, extent=(xmin, xmax, ymin, ymax), cmap='hot')
    plt.draw()


####################################################################################################

# Evento de click do mouse
def on_click(event):
    global xmin, xmax, ymin, ymax, altura, largura, max_iter, flag, pre_images_points, current_index
    global n, c
    if event.button is MouseButton.LEFT:
        # Código existente para zoom
        deltaX = (xmax - xmin) * 0.4
        deltaY = (ymax - ymin) * 0.4
        xmin = event.xdata - deltaX
        xmax = event.xdata + deltaX
        ymin = event.ydata - deltaY
        ymax = event.ydata + deltaY
        update(xmin, xmax, ymin, ymax)
    elif event.button is MouseButton.RIGHT:
        # Código existente para des-zoom
        deltaX = (xmax - xmin) / 1.6
        deltaY = (ymax - ymin) / 1.6
        xmin = event.xdata - deltaX
        xmax = event.xdata + deltaX
        ymin = event.ydata - deltaY
        ymax = event.ydata + deltaY
        update(xmin, xmax, ymin, ymax)
    elif event.button is MouseButton.MIDDLE:
        print("Calculando pré-imagens")
        clear_pre_images()  # Limpa os círculos das pré-imagens anteriores
        z = complex(event.xdata, event.ydata)
        c # Certifique-se de usar o valor de c correto
        points = pre_images(z, c)
        current_index = 0
        draw_pre_images(points)

################################################################################################

##############################################################################################

plt.figure("Conjunto de Julia")
plt.connect('button_press_event', on_click)
im = gerar_conjunto_julia(julia_largura, julia_altura, julia_xmin, julia_xmax, julia_ymin, julia_ymax, max_iter, c)
plt.imshow(im, extent=(julia_xmin, julia_xmax, julia_ymin, julia_ymax), cmap='hot')
plt.colorbar()
plt.title("Conjunto de Julia")
plt.show()
