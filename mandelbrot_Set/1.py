import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backend_bases import MouseButton


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


def gerar_conjunto_mandelbrot(largura, altura, xmin, xmax, ymin, ymax, max_iter):
    # cria uma matriz de zeros com as dimensões da imagem
    imagem = np.zeros((altura, largura))

    # itera sobre cada pixel da imagem
    for x in range(largura):
        for y in range(altura):
            # converte as coordenadas do pixel para o plano complexo
            # essa operação é feita para cada pixel da imagem

            # a coordenada x é normalizada para o intervalo [0, 1]
            real = xmin + (x / (largura - 1)) * (xmax - xmin)

            # a coordenada y é invertida para que o eixo y aponte para cima
            imag = ymin + (y / (altura - 1)) * (ymax - ymin)
            # c é o número complexo que representa o pixel
            c = complex(real, imag)

            # cor é o número de iterações para o pixel c
            cor = mandelbrot(c, max_iter)
            # atualiza a matriz de zeros com o número de iterações
            imagem[y, x] = cor

    return imagem


largura = 800
altura = 800
max_iter = 256

xmin, xmax, ymin, ymax = -2.0, 1.0, -1.5, 1.5


def update(xmin, xmax, ymin, ymax):
    """
    Gera a imagem com base no novo intervalo
    """
    global largura, altura, max_iter
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
        print('Dando Zoom no conjunto de Mandelbrot')
        deltaX = (xmax - xmin) / 3
        deltaY = (ymax - ymin) / 3
        xmin = event.xdata - deltaX
        xmax = event.xdata + deltaX
        ymin = event.ydata - deltaY
        ymax = event.ydata + deltaY
        print("Novo intervalo:", xmin, xmax, ymin, ymax)
        update(xmin, xmax, ymin, ymax)
    elif event.button is MouseButton.RIGHT:
        print('Voltando ao conjunto de Mandelbrot original')
        update(-2.0, 1.0, -1.5, 1.5)
    else:
        deltaX = (xmax - xmin) / 2 * 0.8
        deltaY = (ymax - ymin) / 2 * 0.8
        xmin = -1.5 - deltaX
        xmax = -1.5 + deltaX
        ymin = 0 - deltaY
        ymax = 0 + deltaY
        print("Novo intervalo:", xmin, xmax, ymin, ymax)
        update(xmin, xmax, ymin, ymax)


plt.connect('button_press_event', on_click)
# Gera a imagem inicial
img = gerar_conjunto_mandelbrot(
    largura, altura, xmin, xmax, ymin, ymax, max_iter)
plt.imshow(img, cmap='hot', extent=(xmin, xmax, ymin, ymax))
plt.show()
