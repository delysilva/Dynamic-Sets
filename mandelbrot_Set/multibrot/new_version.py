import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from numba import jit

# Parâmetros para o conjunto de Multibrot
q = 2
p = 4
N = 25
thresh = 5

# Tamanho da imagem
largura = 800
altura = 800

# Intervalo de valores para x e y
xmin, xmax, ymin, ymax = -2.5, 2.5, -2.5, 2.5

# Definindo o número máximo de iterações
max_iter = 100

@jit
def semigroup_map(C, c, thresh):
    D = []
    for i in range(len(C)):
        first = C[i]**2 + c
        second = -C[i]**2 + c
        if abs(first) < thresh:
            D.append(first)
        if abs(second) < thresh:
            D.append(second)
    return D

@jit
def get_iter(c, thresh, max_steps):
    z = [c]
    i = 1
    while i < max_steps and z:
        z = semigroup_map(z, 0.085 + 1.210j, thresh)
        if len(z) >= N:
            i = max_steps
        else:
            i += 1
    return i

@jit
def gerar_conjunto_multibrot(largura, altura, xmin, xmax, ymin, ymax):
    imagem = np.zeros((altura, largura), dtype=np.int64)

    for x in range(largura):
        for y in range(altura):
            real = xmin + (x / (largura - 1)) * (xmax - xmin)
            imag = ymax - (y / (altura - 1)) * (ymax - ymin)
            c = complex(real, imag)
            cor = get_iter(c, thresh, max_iter)
            imagem[y, x] = cor

    return imagem

################################################################################################
# vamos incluir as ferramentas de zoom aqui


###########################################################################################################################


# função que atualiza a imagem com base no novo intervalo
def update(xmin, xmax, ymin, ymax):
    """
    Gera a imagem com base no novo intervalo
    """
    global largura, altura, max_iter, i

    # geramos a imagem
    img = gerar_conjunto_multibrot(largura, altura, xmin, xmax, ymin, ymax)


    plt.imshow(img, cmap='hot', extent=(xmin, xmax, ymin, ymax))
    plt.draw()



########################################################################################################################3
# evento de click do mouse
# função que define o novo intervalo com base na posição do click
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

    # para garantir que a amplitude do intervalo seja positivo
        if(deltaX < 0):
            deltaX = deltaX * -1
        if(deltaY < 0):
            deltaY = deltaY * -1
        


        print("Xmin: ",xmin, "Xmax: ",xmax, ymin, ymax)

    # calculamos o novo intervalo (o zoom do y está invertido, como corrigo isso?)
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

    # aqui podemos voltar ao conjunto original
    elif event.button is MouseButton.RIGHT:
        print('Voltando ao conjunto original')
        xmin, xmax, ymin, ymax = -2.0, 2.0, -2.0, 2.0
        update(-2.0, 2.0, -2.0, 2.0)

    # aqui damos zoom em um ponto específico (não recomendo usar, vou mudar a funcionalidade)
    else:
        deltaX = (xmax - xmin) / 2 * 0.8
        deltaY = (ymax - ymin) / 2 * 0.8
        xmin = -1.5 - deltaX
        xmax = -1.5 + deltaX
        ymin = 0 - deltaY
        ymax = 0 + deltaY
        print("xmin, xmax, ymin, ymax = %lf, %lf, %lf, %lf", xmin, xmax, ymin, ymax)
        update(xmin, xmax, ymin, ymax)

##############################################################################################

# conectamos a função on_click ao evento de click do mouse
plt.connect('button_press_event', on_click)

###########################################################################################


# geramos a imagem

img = gerar_conjunto_multibrot(largura, altura, xmin, xmax, ymin, ymax)
plt.imshow(img, cmap='hot', extent=(xmin, xmax, ymin, ymax))
plt.colorbar()
plt.title('Multibrot')
plt.show()
