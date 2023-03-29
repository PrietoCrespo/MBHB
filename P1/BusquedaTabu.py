import math
import random
from itertools import permutations
import sys
import pandas as pd
import numpy as np
import funcionesAux as fA
np.set_printoptions(threshold=sys.maxsize)
np.printoptions

def busca_Elemento(lista, elemento):
    encontrado = False
    lista = np.array(lista)
    i = 0
    while(not encontrado and i < len(lista)):
        if(np.array_equal(lista[i],elemento)):
            encontrado = True
        else:
            i +=1
    return encontrado
def actualizaListaF(tablaF, v):

    for i in range(len(v)):

        indice = (np.floor(v[i]/10)).__round__()
        tablaF[indice][i] += 1
def solucionGreedy(tablaF):

    tablaF_aux = np.array(tablaF).view()

    Unos = np.ones(tablaF_aux.shape)
    Inv = tablaF_aux
    [filas, columnas] = np.shape(tablaF_aux)

    Inv = Unos / tablaF_aux


    Inv[Inv == math.inf] = 0
    for i in range(columnas):
        suma = sum(Inv[:,i])
        columna = Inv[:,i]
        columnaDividida = np.divide(columna,suma)
        tablaF_aux[:,i] = columnaDividida
    solGreedy = np.zeros(16)
    for i in range(16):
        n = random.uniform(0,1)
        suma = 0
        for j in range(filas):
            suma += tablaF_aux[j,i]

            if(n < suma): #Me quedo con este numero
                valor = j * 10
                valor = random.uniform(valor, valor + 10).__int__() #Como lo tenemos dividido por intervalos obtengo el numero así
                solGreedy[i] = valor                #Lo añado a la solución
                break

    ocupados = solGreedy
    slots = [0] * 16
    suma = sum(ocupados)
    print(len(ocupados))
    for i in range(len(ocupados)):
        slots[i] = ((220 * ocupados[i]) / suma).__int__()

    print("Solucion: "+solGreedy.__str__()+"\n")
    return slots
def act_Tabu(listaTabu,tiempoLT):
    tiempoLT = tiempoLT - 1
    listaTabu[tiempoLT == 0] = 0

    tiempoLT[tiempoLT < 0] = 0

    return [tiempoLT, listaTabu]
def busqueda_Tabu():
    semillas = [10, 20, 30, 40, 50]
    kmRecorridos = [99999, 99999, 99999, 99999, 99999]
    iteraciones = [0, 0, 0, 0, 0]
    mejor_S = np.zeros(shape=(5, 16))

    tablaF = np.zeros(shape=(22,16))

    nVecinos = 40
    nOperadorMovimiento = 3
    iteracionesTotales = 100
    cuartoIteraciones = (np.floor(iteracionesTotales / 4)).__int__()
    distanciaActual = 9999

    tListaT = 8
    list_tabu = np.zeros(shape=(8,2))
    tiempoLT = np.zeros(shape=(8,2))

    indice = 0
    mejora = False
    for j in range(len(semillas)):
        print("\n--------------Semilla " + j.__str__() + "----------------")
        seed = semillas[j]
        np.random.seed(seed)
        capacidadActual = fA.solucionAleatoria()

        mejor_S[:][j] = capacidadActual
        kmRecorridos[j] = fA.evalua(capacidadActual)


        iteracion = 0
        while(iteracion < iteracionesTotales):
            mejora = False
            for i in range(nVecinos):
                v = np.array(capacidadActual).view()
                actualizaListaF(tablaF,v) #Actualizo la lista de Frecuencias con ese nuevo vecino
                movimiento = fA.operadorMovimiento_RandomMovimiento(v,3)

                distanciaCandidata = fA.evalua(v)
                iteraciones[j] += 1

                if((distanciaCandidata < distanciaActual) and (not (busca_Elemento(list_tabu,[movimiento[0],movimiento[1]])) and not((busca_Elemento(list_tabu,[movimiento[2],movimiento[3]])))) or
                       (distanciaCandidata < kmRecorridos[j])): #Criterio de aspiración
                    distanciaActual = distanciaCandidata
                    mejorVecino = v
                    ultimoMovimiento = movimiento
                    mejora = True

            capacidadActual = mejorVecino

            if (mejora and (not (busca_Elemento(list_tabu, [ultimoMovimiento[0], ultimoMovimiento[1]])) and not (
            (busca_Elemento(list_tabu, [ultimoMovimiento[2], ultimoMovimiento[3]]))))):
                list_tabu[indice] = np.array([ultimoMovimiento[0], ultimoMovimiento[1]])
                list_tabu[indice + 1] = np.array([ultimoMovimiento[2], ultimoMovimiento[3]])
                tiempoLT[indice] = 3
                tiempoLT[indice + 1] = 3
            indice = indice + 2
            if (indice >= tListaT):
                indice = 0

            [tiempoLT, list_tabu] = act_Tabu(list_tabu,tiempoLT)


            #Si es la mejor solución la almaceno, ya que me va a servir para la reinicialización
            if(distanciaActual < kmRecorridos[j]):
                mejor_S[:][j] = capacidadActual
                kmRecorridos[j] = distanciaActual

            #Reinicialización

            if((iteracion+1) > (cuartoIteraciones) and ((iteracion) % cuartoIteraciones).__int__() == 0): #Hay que ejecutarlo 4 veces en total
                n = np.random.rand()

                [filas,columnas] = np.shape(list_tabu)
                if(filas > 2): #Establezco el minimo tamaño de la lista tabú a 2
                    if(n < 0.5): #Reinicializo lista tabú
                        list_tabu = np.zeros(shape=((filas*0.5).__int__(),2))
                        tiempoLT = np.zeros(shape=((filas*0.5).__int__(),2))
                        tListaT = filas*0.5
                    else:
                        list_tabu = np.zeros(shape=(filas*2,2))
                        tiempoLT = np.zeros(shape=((filas * 2).__int__(), 2))
                        tListaT = tListaT * 2

                print(list_tabu)
                print(tiempoLT)
                if (n < 0.25):
                    print("Reinicializar construyendo una solucion aleatoria")
                    capacidadActual = fA.solucionAleatoria()
                    print("kms: "+fA.evalua(capacidadActual).__str__())
                    print("Slots totales: " + sum(capacidadActual).__str__())
                elif (n >= 0.25 and n < 0.75):
                    print("Usar memoria a largo plazo al generar una nueva solución greedy")
                    capacidadActual = solucionGreedy(tablaF)
                    print("Slots totales: "+sum(capacidadActual).__str__())
                    print("kms: " + fA.evalua(capacidadActual).__str__())
                else:
                    capacidadActual = mejor_S[:][j]
                    print("Reinicialización desde la mejor solución obtenida")
                    print("kms: " + fA.evalua(capacidadActual).__str__())
                    print("Slots totales: " + sum(capacidadActual).__str__())

            iteracion += 1


    print("\n")
    print("Mejor S1: " + mejor_S[:][0].__str__())
    print("Mejor S2: " + mejor_S[:][1].__str__())
    print("Mejor S3: " + mejor_S[:][2].__str__())
    print("Mejor S4: " + mejor_S[:][3].__str__())
    print("Mejor S5: " + mejor_S[:][4].__str__())
    print("Iteraciones: " + iteraciones.__str__())
    print("Media iteraciones: " + (sum(iteraciones) / 5).__str__())
    print("Media kms : " + (sum(kmRecorridos) / 5).__str__())
    print("Desviacion tipica iteraciones: "+np.std(iteraciones).__str__())
    print("Desviacion tipica kms: "+np.std(kmRecorridos).__str__())
    print("Km recorridos: " + kmRecorridos.__str__())

def main():
    busqueda_Tabu()

main()