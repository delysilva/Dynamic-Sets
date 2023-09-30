import numpy as np
import matplotlib.pyplot as plt
import sys
from matplotlib.backend_bases import MouseButton
from numba import jit

if sys.argv[1] == 'julia':
    conjunto = 'julia'
else:
    conjunto = 'mandelbrot'


def iteracao_julia(c, i):
    z = (c * c) + i
    return z

def julia(c, max_iter, i):
    z = iteracao_julia(c, i)
    for n in range(max_iter):
        if abs(z) > 5:
            return n
        z = iteracao_julia(z, i)
    return max_iter
def gerar_conjunto_julia(largura, altura, xmin, xmax, ymin, ymax, max_iter, i):
    imagem = np.zeros((altura, largura))

    for x in range(largura):
        for y in range(altura):
            real = xmin + (x / (largura - 1)) * (xmax - xmin)
            imag = ymin + (y / (altura - 1)) * (ymax - ymin)
            c = complex(real, imag)

            cor = julia(c, max_iter, i)
            imagem[y, x] = cor

    return imagem
##################################################################################################################

@jit
def mandelbrot(c, max_iter):
    z = c
    # itera até que z "escape" (tenha a possibilidade de divergir)
    for n in range(max_iter):
        # se o valor absoluto de z for maior que 2, o ponto c não pertence ao conjunto de Mandelbrot
        if abs(z) > 2:
            # retorna o número de iterações em que z "escapou"
            return n
        # caso contrário, atualiza o valor de z
        z = z*z + c
    # se o ponto c pertencer ao conjunto de Mandelbrot, retorna o número máximo de iterações
    return max_iter

# função que gera o conjunto de Mandelbrot (parâmetros: largura {referente ao eixo x}, altura {referente ao eixo y}

@jit
def gerar_conjunto_mandelbrot(largura, altura, xmin, xmax, ymin, ymax, max_iter):
    # cria uma matriz de zeros com as dimensões da imagem
    imagem = np.zeros((altura, largura))

    # itera sobre cada pixel da imagem
    for x in range(largura):
        for y in range(altura):
            # converte as coordenadas do pixel para o plano complexo
            # essa operação é feita para cada pixel da imagem

            # a coordenada x é normalizada para o intervalo [0, 1]
            # a parte real de c é um número no intervalo [xmin, xmax]
            real = xmin + (x / (largura - 1)) * (xmax - xmin)

            # CORRIGIDO
            # a parte imaginária de c é um número no intervalo [ymin, ymax]
            imag = ymax - (y / (altura - 1)) * (ymax - ymin)


            # c é o número complexo que representa o pixel
            # a função complex() cria um número complexo a partir das partes real e imaginária
            c = complex(real, imag)

            # cor é o número de iterações para o pixel c
            cor = mandelbrot(c, max_iter)
            # atualiza a matriz de zeros com o número de iterações
            imagem[y, x] = cor

    return imagem


largura = 1200
altura = 1200
max_iter = 256

xmin, xmax, ymin, ymax = -2.0, 2.0, -2.0, 2.0


def update(xmin, xmax, ymin, ymax):
    """
    Gera a imagem com base no novo intervalo
    """
    global largura, altura, max_iter, i

    if conjunto == 'julia':
        img = gerar_conjunto_julia(
            largura, altura, xmin, xmax, ymin, ymax, max_iter, i)
    else:
        img = gerar_conjunto_mandelbrot(
            largura, altura, xmin, xmax, ymin, ymax, max_iter)
        
    plt.imshow(img, cmap='hot', extent=(xmin, xmax, ymin, ymax))
    plt.draw()


def on_click(event):
    """
    Defini o novo intervalo com base na posição do click
    """
    global xmin, xmax, ymin, ymax

    if event.button is MouseButton.LEFT:
        print('Dando Zoom no conjunto')
    # calculamos a amplitude do intervalo em x e y
        deltaX = (xmax - xmin)
        deltaY = (ymax - ymin)

    # reduzimos a amplitude em 60%
        deltaX = deltaX *0.4
        deltaY = deltaY *0.4

    # para garantir que o intervalo seja positivo
        if(deltaX < 0):
            deltaX = deltaX * -1
        if(deltaY < 0):
            deltaY = deltaY * -1
        


        print("Xmin: ",xmin, "Xmax: ",xmax, ymin, ymax)

    # calculamos o novo intervalo
        xmin = event.xdata - deltaX
        xmax = event.xdata + deltaX
        ymin = event.ydata - deltaY
        ymax = event.ydata + deltaY
        
    
        print("Novo intervalo:", xmin, xmax, ymin, ymax)
        print("mouse em: ", event.xdata, event.ydata)
        print("deltaX: ", deltaX, "deltaY: ", deltaY)
        update(xmin, xmax, ymin, ymax)
    elif event.button is MouseButton.RIGHT:
        print('Voltando ao conjunto original')
        xmin, xmax, ymin, ymax = -2.0, 2.0, -2.0, 2.0
        update(-2.0, 2.0, -2.0, 2.0)
    else:
        deltaX = (xmax - xmin) / 2 * 0.8
        deltaY = (ymax - ymin) / 2 * 0.8
        xmin = -1.5 - deltaX
        xmax = -1.5 + deltaX
        ymin = 0 - deltaY
        ymax = 0 + deltaY
        print("xmin, xmax, ymin, ymax = %lf, %lf, %lf, %lf", xmin, xmax, ymin, ymax)
        update(xmin, xmax, ymin, ymax)


plt.connect('button_press_event', on_click)

if conjunto == 'julia':
# Exibindo a imagem
    #Gerando o conjunto de Julia
    i = 0.6
    imagem1 = gerar_conjunto_julia(
        largura, altura, xmin, xmax, ymin, ymax, max_iter, i)
    plt.imshow(imagem1, extent=(xmin, xmax, ymin, ymax), cmap='hot')
    plt.colorbar()
    plt.title("Conjunto de Julia")
    plt.show()
else:

# Gera a imagem inicial
    img = gerar_conjunto_mandelbrot(
        largura, altura, xmin, xmax, ymin, ymax, max_iter)
    plt.imshow(img, cmap='hot', extent=(xmin, xmax, ymin, ymax))
    plt.colorbar()
    plt.title("Conjunto de Mandelbrot")
    plt.show()
