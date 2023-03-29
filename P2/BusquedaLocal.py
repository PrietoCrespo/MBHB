#BUSQUEDA LOCAL
import random
from itertools import combinations
import numpy as np
import funcionesAux as fA
import time
import pip
from matplotlib import pyplot as plt

def busqueda_Local(capacidad,tLotes, numeroOperador):

    nOperadorMovimiento = numeroOperador
    evaluaciones = 0
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

    #print(bloques)
    combinaciones = list(combinaciones)
    np.random.shuffle(combinaciones)


    vSlots = capacidad
    solucionF = fA.evalua(vSlots)
    evaluaciones += 1

    mejor_S = vSlots
    kmRecorridos = solucionF

    Mejora = True
    i = 0
    iteracionesTotales = 0
    while(Mejora and iteracionesTotales < 3000):
        Mejora = False

        k = 0
        distanciaActual = kmRecorridos
        while(k < len(combinaciones) and iteracionesTotales < 3000):
            v = fA.operadorMovimiento_RandomBL(mejor_S, nOperadorMovimiento,combinaciones.__getitem__(k)[0],combinaciones.__getitem__(k)[1])
            distanciaCand = fA.evalua(v)
            evaluaciones += 1
            iteracionesTotales += 1

            if(distanciaCand < distanciaActual):
                distanciaActual = distanciaCand
                vecinoActual = v
                Mejora = True
            if k % 40 == 0: #En caso de terminar uno de los 4 bloques
                #print("K: "+k.__str__())
                if(Mejora):              #Si el mejor vecino del bloque mejora lo guardamos y seguimos desde ahi
                    mejor_S = vecinoActual
                    kmRecorridos = distanciaActual
                    np.random.shuffle(combinaciones)
                    #print("Ha mejorado con " + kmRecorridos.__str__())
                    break #Deberia salir del bucle
            k += 1
    return kmRecorridos, mejor_S, evaluaciones
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

'''def main():
    busqueda_Local(20,2)'''