import math
import random
from itertools import permutations
import sys
import pandas as pd
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
np.printoptions

cercanas_indices = pd.read_csv('./bicicletas/cercanas_indices.csv')
cercanas_km = pd.read_csv('./bicicletas/cercanas_kms.csv')
deltas_5m = pd.read_csv('./bicicletas/deltas_5m.csv')

primer_movimiento = deltas_5m.values[0]

class move():
    def __init__(self):
        self.estacion = ""
        self.bicis = ""

    def __str__(self):
        return "Estacion: " + self.estacion.__str__() + " Movimiento: " + self.bicis.__str__()

# GREEDY
def slotsGreedy(ocupados):
    slots = [0] * 16
    suma = sum(ocupados)
    print(len(ocupados))
    for i in range(len(ocupados)):
        slots[i] = ((220 * ocupados[i]) / suma).__round__()
    return slots

# BUCLE PARA OBTENER LA LISTA DE MOVIMIENTOS, CUYO RESULTADO ES UNA LISTA DE OBJETOS TIPO "MOVE", QUE CONTIENE UN ATRIBUTO
# "ESTACIÓN" Y OTRO "BICIS"
def lista_Mov(lista_movimientos, deltas_5m):
    for f in range(len(deltas_5m)):
        arrayAct = deltas_5m.values[f]
        for c in range(len(arrayAct)):
            if (arrayAct[c] != 0):
                aux = move()
                aux.estacion = c
                if (f > 0):
                    aux.bicis = arrayAct[c]* 2
                else:
                    aux.bicis = arrayAct[c]

                lista_movimientos.append(aux)

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

#Genera una solución aleatoria
def solucionAleatoria():

    capacidad = [0]*16
    for i in range(len(capacidad)):

        n = np.random.rand() * 11 + 1
        capacidad[i] = n

    propor = 220 / sum(capacidad)
    #Normalizacion
    for i in range(len(capacidad)):
        capacidad[i] = (capacidad[i]*propor).__int__()

    np.random.shuffle(capacidad)
    return capacidad

#Generador de vecinos
def operadorMovimiento_Random(capacidad,numero):
    capacidad = np.array(capacidad).view()
    a = random.uniform(0,len(capacidad)).__int__()
    b = random.uniform(0,len(capacidad)).__int__()
    if((capacidad[a] - numero) < 0):
        numero = capacidad[a]
        capacidad[a] = 0
    else:
        capacidad[a] = capacidad[a] - numero

    capacidad[b] = capacidad[b] + numero

    return capacidad

#Sobrecargado para la BL
def operadorMovimiento_RandomBL(capacidad,numero,a = -1,b=-1):
    capacidad = np.array(capacidad).view()
    if(a == -1 or b == -1):
        a = random.uniform(0,16).__int__()
        b = random.uniform(0,16).__int__()
    if((capacidad[a] - numero) < 0):
        numero = capacidad[a]
        capacidad[a] = 0
    else:
        capacidad[a] = capacidad[a] - numero

    capacidad[b] = capacidad[b] + numero

    return capacidad #S

#Devuelve lo que he modificado y la capacidad la modifica
def operadorMovimiento_RandomMovimiento(capacidad,numero):


    a = random.uniform(0,len(capacidad)).__int__()
    b = random.uniform(0,len(capacidad)).__int__()
    if((capacidad[a] - numero) < 0):
        numero = capacidad[a]
        capacidad[a] = 0
    else:
        capacidad[a] = capacidad[a] - numero

    capacidad[b] = capacidad[b] + numero
    movimiento = [a,capacidad[a],b,capacidad[b]]
    return movimiento

#Funcion que evalua una solución
def evalua(solucion):
    vSlots = np.array(solucion).view()
    capMax = np.array(solucion).view()

    vSolucion = 0  # km recorridos
    incremento = -1

    lista_movimientos = []
    lista_Mov(lista_movimientos,deltas_5m)

    for movimiento in lista_movimientos:
        incremento += 1
        if (movimiento.bicis < 0):
            if ((capMax[movimiento.estacion] - vSlots[movimiento.estacion]) >= abs(
                    movimiento.bicis)):  # Puedo sacar todas las bicis del tirón
                vSlots[movimiento.estacion] = vSlots[movimiento.estacion] - movimiento.bicis
            else:
                # Tengo que ir metiendo bicis en las estaciones más cercanas
                id = cercanas_indices.values[movimiento.estacion][1]  # Estacion mas cercana
                restantes = abs((abs(movimiento.bicis) - (capMax[movimiento.estacion] - vSlots[movimiento.estacion])))
                vSlots[movimiento.estacion] = capMax[movimiento.estacion]
                n = 1


                while (restantes > 0):
                    id = cercanas_indices.values[movimiento.estacion][n]
                    if(vSlots[id] < capMax[id]):
                        if((capMax[id] - vSlots[id]) <= restantes):
                            guardadas = (capMax[id] - vSlots[id])
                            restantes = restantes - guardadas
                            vSlots[id] = capMax[id]
                        else:
                            guardadas = restantes
                            vSlots[id] = vSlots[id] + restantes
                            restantes = 0
                        distancia = cercanas_km.values[movimiento.estacion][n]  #Distancia a la estación más cercana
                        if (incremento > 15):
                            vSolucion = vSolucion + distancia * 3 * guardadas # *3 porque voy a pie
                        anterior = id
                        n = 0
                    n += 1
        elif (vSlots[movimiento.estacion] > 0 and vSlots[movimiento.estacion] >= movimiento.bicis):  # Si caben todas las bicis
            vSlots[movimiento.estacion] = vSlots[movimiento.estacion] - movimiento.bicis
        else:
            id = cercanas_indices.values[movimiento.estacion][1]
            n = 1
            restantes = abs(vSlots[movimiento.estacion] - movimiento.bicis)
            vSlots[movimiento.estacion] = 0
            anterior = movimiento.estacion
            while (restantes > 0):
                id = cercanas_indices.values[movimiento.estacion][n]

                if(vSlots[id] > 0):
                    if(vSlots[id] <= restantes):
                        aux = restantes
                        restantes = restantes - vSlots[id]
                        guardadas = aux - restantes
                        vSlots[id] = 0
                    else:
                        vSlots[id] = vSlots[id] - restantes
                        guardadas = restantes
                        restantes = 0

                    distancia = cercanas_km.values[movimiento.estacion][n]  # Distancia a la estación más cercana
                    if (incremento > 15):
                        vSolucion = vSolucion + distancia * guardadas  # Sumo la distancia recorrida a la solución
                    anterior = id
                    n = 0
                n += 1
    return vSolucion

#Funcion que evalua una solución y castiga si la capacidad es mayor que 205
def evaluaGenetico(solucion):
    vSlots = np.array(solucion).view()
    capMax = np.array(solucion).view()

    vSolucion = 0  # km recorridos
    incremento = -1

    lista_movimientos = []
    lista_Mov(lista_movimientos,deltas_5m)

    if (sum(solucion) < 205):
        vSolucion = 1000
    else:
        for movimiento in lista_movimientos:
            incremento += 1
            if (movimiento.bicis < 0):
                if ((capMax[movimiento.estacion] - vSlots[movimiento.estacion]) >= abs(
                        movimiento.bicis)):  # Puedo sacar todas las bicis del tirón
                    vSlots[movimiento.estacion] = vSlots[movimiento.estacion] - movimiento.bicis
                else:
                    # Tengo que ir metiendo bicis en las estaciones más cercanas
                    id = cercanas_indices.values[movimiento.estacion][1]  # Estacion mas cercana
                    restantes = abs((abs(movimiento.bicis) - (capMax[movimiento.estacion] - vSlots[movimiento.estacion])))
                    vSlots[movimiento.estacion] = capMax[movimiento.estacion]
                    n = 1


                    while (restantes > 0):
                        id = cercanas_indices.values[movimiento.estacion][n]
                        if(vSlots[id] < capMax[id]):
                            if((capMax[id] - vSlots[id]) <= restantes):
                                guardadas = (capMax[id] - vSlots[id])
                                restantes = restantes - guardadas
                                vSlots[id] = capMax[id]
                            else:
                                guardadas = restantes
                                vSlots[id] = vSlots[id] + restantes
                                restantes = 0
                            distancia = cercanas_km.values[movimiento.estacion][n]  #Distancia a la estación más cercana
                            if (incremento > 15):
                                vSolucion = vSolucion + distancia * 3 * guardadas # *3 porque voy a pie
                            anterior = id
                            n = 0
                        n += 1
            elif (vSlots[movimiento.estacion] > 0 and vSlots[movimiento.estacion] >= movimiento.bicis):  # Si caben todas las bicis
                vSlots[movimiento.estacion] = vSlots[movimiento.estacion] - movimiento.bicis
            else:
                id = cercanas_indices.values[movimiento.estacion][1]
                n = 1
                restantes = abs(vSlots[movimiento.estacion] - movimiento.bicis)
                vSlots[movimiento.estacion] = 0
                anterior = movimiento.estacion
                while (restantes > 0):
                    id = cercanas_indices.values[movimiento.estacion][n]

                    if(vSlots[id] > 0):
                        if(vSlots[id] <= restantes):
                            aux = restantes
                            restantes = restantes - vSlots[id]
                            guardadas = aux - restantes
                            vSlots[id] = 0
                        else:
                            vSlots[id] = vSlots[id] - restantes
                            guardadas = restantes
                            restantes = 0

                        distancia = cercanas_km.values[movimiento.estacion][n]  # Distancia a la estación más cercana
                        if (incremento > 15):
                            vSolucion = vSolucion + distancia * guardadas  # Sumo la distancia recorrida a la solución
                        anterior = id
                        n = 0
                    n += 1
        if sum(solucion) > 205:
            indCastigo = 5
            vSolucion = vSolucion + ((sum(solucion) - 205) * indCastigo).__round__()
    return vSolucion