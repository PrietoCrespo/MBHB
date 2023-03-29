#BUSQUEDA LOCAL
import random
from itertools import combinations
import numpy as np
import funcionesAux as fA
import time
import pip
from matplotlib import pyplot as plt

def busqueda_Local(tLotes, numeroOperador):
    semillas = [10,20,30,40,50]
    kmRecorridos = [99999, 99999, 99999, 99999, 99999]
    iteraciones = [0, 0, 0, 0, 0]
    mejor_S = np.zeros(shape=(5, 16))

    nOperadorMovimiento = numeroOperador

    combinaciones = combinations([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],2) #120 combinaciones
    #120 / 3 = 4 paquetes de 40 vecinos
    nLotes = (120 / tLotes).__int__()
    bloques = np.zeros(nLotes)

    limiteLote = tLotes
    for i in range(nLotes):
        if(i == nLotes - 1):
            bloques[i] = 119
        else: bloques[i] = limiteLote
        limiteLote += tLotes

    print(bloques)
    combinaciones = list(combinaciones)
    np.random.shuffle(combinaciones)

    for j in range(len(semillas)):
        print("\n--------------Semilla " + j.__str__()+"----------------")
        seed = semillas[j]
        np.random.seed(seed)
        vSlots = fA.solucionAleatoria()
        solucionF = fA.evalua(vSlots)

        mejor_S[:][j] = vSlots
        kmRecorridos[j] = solucionF

        Mejora = True
        i = 0
        iteracionesTotales = 0
        while(Mejora and iteracionesTotales < 3000):
            Mejora = False

            k = 0
            distanciaActual = kmRecorridos[j]
            while(k < len(combinaciones) and iteracionesTotales < 3000):
                v = fA.operadorMovimiento_RandomBL(mejor_S[:][j], nOperadorMovimiento,combinaciones.__getitem__(k)[0],combinaciones.__getitem__(k)[1])
                distanciaCand = fA.evalua(v)
                iteraciones[j] = iteraciones[j] + 1
                iteracionesTotales += 1

                if(distanciaCand < distanciaActual):
                    distanciaActual = distanciaCand
                    vecinoActual = v
                    Mejora = True
                if(bloques.__contains__(k)): #En caso de terminar uno de los 4 bloques
                    if(Mejora):              #Si el mejor vecino del bloque mejora lo guardamos y seguimos desde ahi
                        mejor_S[:][j] = vecinoActual
                        kmRecorridos[j] = distanciaActual
                        np.random.shuffle(combinaciones)
                        break #Deberia salir del bucle

                k += 1


    print("\n")
    print("Mejor S1: " + mejor_S[:][0].__str__())
    print("Mejor S2: " + mejor_S[:][1].__str__())
    print("Mejor S3: " + mejor_S[:][2].__str__())
    print("Mejor S4: " + mejor_S[:][3].__str__())
    print("Mejor S5: " + mejor_S[:][4].__str__())
    mediaKms = (sum(kmRecorridos) / 5)
    print("Media kms : "+ mediaKms.__str__())
    print("Iteraciones: "+iteraciones.__str__())
    print("Media iteraciones: "+(sum(iteraciones) / 5).__str__())
    print("Desviacion tipica iteraciones: "+np.std(iteraciones).__str__())
    print("Desviacion tipica kms: "+np.std(kmRecorridos).__str__())
    print("Km recorridos: " + kmRecorridos.__str__())

    return mediaKms
def mainPrueba():
    mediasLote = np.zeros(5)
    tiemposLote = np.zeros(5)

    mediasMovimiento = np.zeros(5)
    tiemposMovimiento = np.zeros(5)

    fig, axs = plt.subplots(2)
    fig.suptitle('Modificando tamaño lote')
    axs[0].set_title('Media kms')
    axs[1].set_title('Tiempo ejecucion')
    tLotes = [10,20,30,40,60]
    nMovimientos = [1,2,3,5,10]
    print("Modificando tamaño lote: ")
    for i in range(5):
        start_time = time.time()
        mediasLote[i] = busqueda_Local(tLotes[i],3)
        tiemposLote[i] = (time.time() - start_time)

    axs[0].set_ylabel('Media kms')
    axs[0].set_xlabel('Tamaño lote')
    axs[0].plot(tLotes,mediasLote)

    axs[1].set_ylabel('Tiempo ejecucion')
    axs[1].set_xlabel('Tamaño lote')
    axs[1].plot(tLotes, tiemposLote)
    plt.show()

    fig, axs = plt.subplots(2)
    fig.suptitle('Modificando tamaño movimiento')
    axs[0].set_title('Media kms')
    axs[1].set_title('Tiempo ejecucion')
    print("Modificando tamaño movimiento: ")
    for i in range(5):
        mediasMovimiento[i] = busqueda_Local(40, nMovimientos[i])
        tiemposMovimiento[i] = (time.time() - start_time)

    axs[0].set_ylabel('Media kms')
    axs[0].set_xlabel('Tamaño movimiento')
    axs[0].plot(nMovimientos, mediasMovimiento)

    axs[1].set_ylabel('Tiempo ejecucion')
    axs[1].set_xlabel('Tamaño movimiento')
    axs[1].plot(nMovimientos, tiemposMovimiento)
    plt.show()

    print("Media km lote: "+mediasLote.__str__())
    print("Tiempos lote: "+tiemposLote.__str__())
    print("Media km movimiento: " + mediasMovimiento.__str__())
    print("Tiempos movimiento: " + tiemposMovimiento.__str__())

def main():
    busqueda_Local(20,2)
main()