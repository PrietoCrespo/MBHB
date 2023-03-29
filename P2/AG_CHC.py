import numpy as np
import random
import funcionesAux as fA

def generaPoblacion(numero):
    poblacion = np.zeros(shape=(numero, 16))
    kmRecorridos = np.zeros(shape=(numero))


    for i in range(numero):
        poblacion[i][:] = fA.solucionAleatoria()
        kmRecorridos[i] = fA.evaluaGenetico(poblacion[i][:])

    return  poblacion,kmRecorridos

def evaluaPoblacion(poblacionAEvaluar):
    poblacion = np.array(poblacionAEvaluar).view()
    filas = len(poblacion)
    kmRecorridos = np.zeros(filas)

    for i in range(filas):
        kmRecorridos[i] = fA.evaluaGenetico(poblacion[i])

    return kmRecorridos


def distanciaHamming(vector1, vector2): #Devuelve donde los indices son diferentes señalados por un 1
    vectorDiferencia = np.abs(vector1 - vector2)
    vectorDiferencia[vectorDiferencia> 0] = 1

    return vectorDiferencia

def selectR(poblacion):
    poblacion = np.array(poblacion).view()
    np.random.shuffle(poblacion)
    c = poblacion
    kmRecorridos = evaluaPoblacion(c)

    return c,kmRecorridos

def selectS(poblacionC, kmsC, poblacionC2, kmsC2):
    #Tengo que sustituir los mejores de la poblacionC2 por los peores de la poblacionC
    for i in range(len(kmsC2)):
        indPeor = np.argmax(kmsC)
        if kmsC2[i] < kmsC[indPeor]: #Si mejora al peor
            kmsC[indPeor] = kmsC2[i]
            poblacionC[indPeor] = poblacionC2[i]

    return poblacionC, kmsC

def recombina(poblacion, d):
    i = 0
    c = list() #Creo la poblacion C

    while i < len(poblacion):
        distancia = distanciaHamming(np.array(poblacion[i]), np.array(poblacion[i+1])) #Calculo dist. Hamming
        if (sum(distancia) / 2) > d:
            indices = np.argwhere(distancia == 1) #Indices donde difieren ambos vectores
            np.random.shuffle(indices) #Cambio de orden los indices para que no esten ordenados

            numeroCambios = (len(indices) / 2).__round__()
            if numeroCambios < 1:
                numeroCambios = 1
            for j in range(numeroCambios): #Intercambio la mitad de los valores que cambien
                v3 = np.array(poblacion[j].view())
                v4 = np.array(poblacion[j+1].view())
                v3[indices[j]] = poblacion[j+1][indices[j]]
                v4[indices[j]] = poblacion[j][indices[j]]
                #Muto
                v3[indices[j]] = np.random.normal(v3[indices[j]],2).__int__()
                v4[indices[j]] = np.random.normal(v4[indices[j]],2).__int__()
            c.append(v3)
            c.append(v4)
        i = i + 2

    return c

def diverge(poblacion, kmRecorridos, M, tam):
    #Genero una nueva poblacion de tamaño "tam", mismo que el inicial
    nuevaPoblacion,kmNuevaPoblacion = generaPoblacion(tam)
    #Obtengo los M mejores de la población actual, antes del reinicio
    indices = np.argsort(kmRecorridos)
    indices = indices[0:M]

    #Los inserto en la población
    nuevaPoblacion[0:M] = poblacion[indices]
    kmNuevaPoblacion[0:M] = kmRecorridos[indices]
    print(f"Me quedo con: {poblacion[indices]}")

    return nuevaPoblacion,kmNuevaPoblacion

def ordenaPoblacion(poblacionOrdenable,kmRecorridosOrdenables):
    indicesOrdenados = np.argsort(kmRecorridosOrdenables)

    poblacion = np.zeros(poblacionOrdenable.shape)
    kmRecorridos = np.zeros(shape=len(poblacionOrdenable))

    for i in range(len(indicesOrdenados)):
        poblacion[i] = poblacionOrdenable[indicesOrdenados[i]]
        kmRecorridos[i] = kmRecorridosOrdenables[indicesOrdenados[i]]

    return poblacion,kmRecorridos

def genetico_CHC():
    semillas = [10, 20, 30]
    kmMinimos = [99999, 99999, 99999]

    reiniciosMaximos = 10
    tamaElite = 5

    for k in range(len(semillas)):
        print(f"Semilla {k}:")
        seed = semillas[k]
        # Establezco la semilla para la serie pseudoaleatoria
        np.random.seed(seed)
        L = 16
        d = L / 4
        nReinicios = 0

        [poblacion, kmRecorridos] = generaPoblacion(L)
        print(f"Poblacion inicial, mejor individuo: {kmRecorridos[np.argmin(kmRecorridos)]}")
        #Añado el greedy
        poblacion[-1][:] = fA.slotsGreedy(fA.primer_movimiento)
        kmRecorridos[-1] = fA.evaluaGenetico(poblacion[-1])

        evaluaciones = 0

        while nReinicios <= reiniciosMaximos:
            c, kmRecorridosC = selectR(poblacion)

            evaluaciones += len(poblacion)

            c2 = recombina(c, d)
            kmRecorridosC2 = evaluaPoblacion(c2)

            evaluaciones += len(c2)

            kmRecorridosAnt = kmRecorridos
            poblacionAnt = np.array(poblacion).view()
            poblacion,kmRecorridos = selectS(c,kmRecorridosC,c2,kmRecorridosC2)

            poblacion,kmRecorridos = ordenaPoblacion(poblacion,kmRecorridos)
            poblacionAnt,kmRecorridosAnt = ordenaPoblacion(poblacionAnt,kmRecorridosAnt)

            indicesPoblacion = np.argsort(kmRecorridos)
            indicesPoblacionAnt = np.argsort(kmRecorridosAnt)

            if (indicesPoblacionAnt == indicesPoblacion).all():
                d -= 1
            if d < 0:

                nReinicios += 1
                if nReinicios <= reiniciosMaximos:
                    poblacion,kmRecorridos = diverge(poblacion,kmRecorridos,tamaElite,L)

                    evaluaciones += tamaElite

                    print(f"-----------------------------------REINICIA POBLACION-----------------------------------")
                d = L / 4

        print(f"\n\nPoblacion final ")
        for j in range(len(poblacion)):
            print(f"[{j}] {poblacion[j]} Puntos: {kmRecorridos[j]} Capacidad: {sum(poblacion[j])}")
        mejorInd = np.argmin(kmRecorridos)
        capacidadVector = sum(poblacion[mejorInd])
        indCastigo = 5
        print(f"Mejor vector: \n\tCapacidad: {capacidadVector} Puntos: {kmRecorridos[mejorInd]} Kms: "
              f"{kmRecorridos[mejorInd] - (capacidadVector-205)*indCastigo}")
        print(f"Evaluaciones: {evaluaciones}")


def main():
    genetico_CHC()

if __name__ == '__main__':
    main()