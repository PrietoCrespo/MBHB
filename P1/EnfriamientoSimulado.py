#ENFRIAMIENTO SIMULADO
import math
import numpy as np
import funcionesAux as fA

#Función para obtener la temperatura inicial a partir de mu y phi
def temperatura_Inicial():
    ocupados = fA.primer_movimiento
    greedy = fA.slotsGreedy(ocupados)

    coste = fA.evalua(greedy)
    print("Coste greedy: " + coste.__str__())
    mu = 0.2
    phi = 0.1

    return ((mu/-math.log(phi))*coste)

#Función para comprobar que, dados un mu y un phi, solo se acepte un 80% de las soluciones iniciales
def comprobar_TempInicial():
    #Para estos valores me da una media de 80% aceptado
    ocupados = fA.primer_movimiento

    mu = 0.2
    phi = 0.1
    cociente = mu / -np.log(phi)
    costeGreedy = fA.evalua(fA.slotsGreedy(ocupados))
    tInicial = cociente * costeGreedy
    Scand = costeGreedy

    k = 0
    for i in range(100):
        Sact = fA.evalua(fA.solucionAleatoria())
        d = Scand - Sact

        n = np.random.rand()

        if ((n < np.exp(-d / tInicial)) or d < 0):
            k = k+1

    return k

#Función principal ES
def enfriamiento_Simulado():
    semillas = [10, 20, 30, 40, 50]
    kmRecorridos = [99999, 99999, 99999, 99999, 99999]
    iteraciones = [0, 0, 0, 0, 0]

    mejor_S = np.zeros(shape=(5, 16))

    Tinicial = temperatura_Inicial()
    print("Tinicial: "+Tinicial.__str__())
    Tactual = Tinicial

    nVecinos = 20
    LT = nVecinos
    nOperadorMovimiento = 3

    nIteraciones = 40
    np.random.seed(10)

    for j in range(len(semillas)):
        print("\n--------------Semilla " + j.__str__() + "----------------")
        seed = semillas[j]
        np.random.seed(seed)
        vSlots = fA.solucionAleatoria()
        kmRecorridos[j] = fA.evalua(vSlots)

        mejor_S[:][j] = vSlots
        k = 0
        while (k < nIteraciones):
            k += 1
            for i in range(LT):
                v = fA.operadorMovimiento_Random(mejor_S[:][j], nOperadorMovimiento)
                kmCandidata = fA.evalua(v)
                iteraciones[j] = iteraciones[j]+1
                d = kmCandidata - kmRecorridos[j]
                n = np.random.rand()
                if ((n < np.exp(-d / Tactual)) or d < 0):
                    mejorCapacidad = v
                    mejorKm = kmCandidata

                    if(mejorKm < kmRecorridos[j]):
                        mejor_S[:][j] = mejorCapacidad
                        kmRecorridos[j] = mejorKm
                    print(".",end='')

            Tactual = Tinicial / (1 + k)
    print("\n")
    print("Mejor S1: " + mejor_S[:][0].__str__())
    print("Mejor S2: " + mejor_S[:][1].__str__())
    print("Mejor S3: " + mejor_S[:][2].__str__())
    print("Mejor S4: " + mejor_S[:][3].__str__())
    print("Mejor S5: " + mejor_S[:][4].__str__())
    print("Media kms : " + (sum(kmRecorridos) / 5).__str__())
    print("Iteraciones: " + iteraciones.__str__())
    print("Media iteraciones: " + (sum(iteraciones) / 5).__str__())
    print("Desviacion tipica iteraciones: "+np.std(iteraciones).__str__())
    print("Desviacion tipica kms: "+np.std(kmRecorridos).__str__())
    print("Km recorridos: " + kmRecorridos.__str__())

def main():
    enfriamiento_Simulado()

main()