import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from numba import jit

##############################################################################################
# Parâmetros para gerar a imagem

# a largura e a altura da imagem são referentes ao eixo x e y, respectivamente

largura = 1200
altura = 1200

# o número máximo de iterações pode ser alterado para gerar imagens com mais ou menos detalhes
max_iter = 256

# o intervalo de valores iniciais para x e Y:
xmin, xmax, ymin, ymax = -2.0, 1.0, -1.5, 1.5

julia_largura = 1200
julia_altura = 1200

julia_xmin, julia_xmax, julia_ymin, julia_ymax = -2.0, 2.0, -2.0, 2.0


# flag de controle do click do mouse
flag = False

##############################################################################################
##############################################################################################
# isso é uma função que gera os pre-imagens de um ponto z, com n iterações e um valor de c
def pre_images(z, n, c):
    vetor = [z]

    for i in range(n):
        ## [w11, w12, w21, w22]

        a = len(vetor)
        for j in range (a):
            
            p = vetor.pop()
            coeff = [1, 0, c-p]
            roots = np.roots(coeff)
            
            w1 = roots[0]
            w2 = roots[1]

            vetor.append(w1)
            vetor.append(w2)

    return vetor

# raio = 1/(2^n)

###############################################################################################



# função que realiza a iteração de Julia
@jit
def iteracao_julia(c, i):
    z = (c * c) + i
    return z

# função que gera o conjunto de Julia a partir de uma complexo c e um número máximo de iterações
# @jit significa que a função será compilada em tempo de execução
@jit
def julia(c, max_iter, i):
    z = iteracao_julia(c, i)
    for n in range(max_iter):
        if abs(z) > 5:
            return n
        z = iteracao_julia(z, i)
    return max_iter


# função que gera o conjunto de Julia (parâmetros: largura {referente ao eixo x}, altura {referente ao eixo y}
# mesma base do conjunto de Mandelbrot, porém iteranddo com a função de Julia
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


##################################################################################################################

# função que realiza a iteração de Mandelbrot
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

            # a coordenada y é invertida para que o eixo y aponte para cima
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



###########################################################################################################################


# função que atualiza a imagem com base no novo intervalo
def update(xmin, xmax, ymin, ymax):
    """
    Gera a imagem com base no novo intervalo
    """
    global largura, altura, max_iter, i

    img = gerar_conjunto_mandelbrot(
            largura, altura, xmin, xmax, ymin, ymax, max_iter)
    
    plt.figure("Conjunto de Mandelbrot")
        
    plt.imshow(img, cmap='hot', extent=(xmin, xmax, ymin, ymax))
    plt.draw()



########################################################################################################################3
# evento de click do mouse
# função que define o novo intervalo com base na posição do click
def on_click(event):
    """
    Defini o novo intervalo com base na posição do click
    """
    global xmin, xmax, ymin, ymax, altura, largura, max_iter, flag

    if event.button is MouseButton.LEFT:
        print('Dando Zoom no conjunto')
        # calculamos a amplitude do intervalo em x e y
        deltaX = (xmax - xmin)
        deltaY = (ymax - ymin)
        print(deltaX, " " ,deltaY)

        # reduzimos a amplitude em 60%
        deltaX = deltaX *0.4
        deltaY = deltaY *0.4

        # para garantir que a amplitude do intervalo seja positivo
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
        
        # alguns prints para debug
    
        print("Novo intervalo:", xmin, xmax, ymin, ymax)
        print("mouse em: ", event.xdata, event.ydata)
        print("deltaX: ", deltaX, "deltaY: ", deltaY)

        # atualizamos a imagem
        update(xmin, xmax, ymin, ymax)

    # aqui vamos gerar uma nova janela de um conjunto de julia a partir de um ponto específico (x, y) do conjunto de Mandelbrot
    elif event.button is MouseButton.MIDDLE:

        # calculamos a posição do click no eixo x e y
        x = event.xdata
        y = event.ydata
        

        i = complex(x, y) # i é o número complexo que representa o ponto clicado no conjunto de Mandelbrot

        # agora vamos gerar uma nova janela com o conjunto de Julia plotando a figura 2

        plt.figure("Conjunto de Julia")
        i = complex(x, y) # i é o número complexo que representa o ponto clicado no conjunto de Mandelbrot

        im = gerar_conjunto_julia(julia_largura, julia_altura, julia_xmin, julia_xmax, julia_ymin, julia_ymax, max_iter, i)

        plt.imshow(im, extent=(julia_xmin, julia_xmax, julia_xmin, julia_ymax), cmap='hot')

        
        plt.show(block=False)  # Use block=False to avoid blocking the code execution
        plt.pause(0.01)


    # aqui utilizamos o mesmo fator de ampliação do zoom para voltar ao zoom anterior
    elif event.button is MouseButton.RIGHT:
        print('Voltando ao zoom anterior')
        # calculamos a amplitude do intervalo em x e y
        deltaX = (xmax - xmin)
        deltaY = (ymax - ymin)
        print(deltaX, " " ,deltaY)

        deltaX = deltaX/(1.6)
        deltaY = deltaY/(1.6)

        # para garantir que a amplitude do intervalo seja positivo
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
        
        # alguns prints para debug
    
        print("Novo intervalo:", xmin, xmax, ymin, ymax)
        print("mouse em: ", event.xdata, event.ydata)
        print("deltaX: ", deltaX, "deltaY: ", deltaY)

        # atualizamos a imagem
        update(xmin, xmax, ymin, ymax)


##############################################################################################



###########################################################################################



# Gera a imagem inicial e definir como 1 para não conflitar com a imagem gerada a partir do click

# o erro ocorre aqui, há uma confusão entre figura 1 e figura 2
plt.figure("Conjunto de Mandelbrot")
# conectamos a função on_click ao evento de click do mouse
plt.connect('button_press_event', on_click)

img = gerar_conjunto_mandelbrot(
    largura, altura, xmin, xmax, ymin, ymax, max_iter)
    

plt.imshow(img, cmap='hot', extent=(xmin, xmax, ymin, ymax))
plt.colorbar()
plt.title("Conjunto de Mandelbrot")

plt.figure("Conjunto de Julia")

# gerar uma imagem em branco para im
im = np.zeros((julia_altura, julia_largura))
plt.imshow(im, extent=(julia_xmin, julia_xmax, julia_ymin, julia_ymax), cmap='hot')
plt.colorbar()
plt.title("Conjunto de Julia")
plt.show()
