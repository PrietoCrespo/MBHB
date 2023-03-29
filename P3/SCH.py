import random

import numpy
import time
import fAux
import numpy as np
import math
import copy



def sistemaHormigas():
    ciudades = fAux.leer_Ciudades('a280.tsp')
    tam = len(ciudades)
    print(f"Ciudades: {ciudades}")
    m = 10 #Numero hormigas
    alpha = 1
    beta = 2
    p = 0.1
    e = 15
    q0 = 0.98
    fi = 0.1

    semillas = [10, 20, 30]
    for seed in semillas:

        np.random.seed(seed)
        print(f"Semilla: {seed}")
        evaluaciones = 0
        tiempo = 0

        #Coste de los caminos para cada hormiga
        costes = np.ones(shape=m)
        costes *= 999
        #Lista de nodos visitados por cada hormiga
        L = np.ones(shape=(m,tam+1))
        L *= -1
        LnV = np.ones(shape=(m,tam))
        LnV[0:m] = np.arange(0, tam)
        #Calculo la matriz de distancias
        D = fAux.matrizDistancias(ciudades=ciudades)
        #Calculo la matriz de heuristica a partir de D
        nH = fAux.matrizHeuristica(D)
        #Inicializo matriz de feromonas al valor indicado
        t = np.ones(shape=(tam,tam))

        if tam < 200:
            t0 = 1 / (tam*valorGreedy('ch130.tsp'))
        else:
            t0 = 1 / (tam * valorGreedy('a280.tsp'))
        t *= t0
        # Mejores costes
        mejorCosteGlobal = 999999
        #Inicializo cada hormiga con el nodo inicial
        for i in range(m):
            numeroAleatorio = np.random.randint(0, tam)
            L[i,0] = numeroAleatorio
            LnV[i,numeroAleatorio] = -1

        start_time = time.time()
        tiempo_ejecucion = abs(time.time() - start_time)


        while tiempo_ejecucion < 300:
            mejorCosteActual = 999999
            #Construyo soluciones para cada hormiga
            for i in range(m):
                for j in range(1,tam):
                    numAleatorio = np.random.uniform(0,1)
                    if numAleatorio > q0:
                        ciudad = fAux.reglaTransicion(L[i,:], int(L[i,j-1]), ciudades, t,nH, alpha, beta, LnV[i,:])
                    else:
                        ciudad = fAux.reglaTransicionColonia(L[i, :], int(L[i,j-1]), ciudades, t, nH, alpha, beta, q0, LnV[i, :])
                    L[i,j] = ciudad
                    LnV[i, ciudad] = -1

                    ciudadAnt = int(L[i,j-1])
                    # Actualizacion local feromonas

                    t[ciudad, ciudadAnt] *= (1-fi)
                    t[ciudad, ciudadAnt] += fi*t0

                    t[ciudadAnt, ciudad ] = copy.copy(t[ciudad, ciudadAnt])
                L[i,j+1] = L[i,0]

                costes[i] = fAux.funcionCoste(L[i, :], D)
                evaluaciones += 1
                if costes[i] < mejorCosteActual:
                    mejorCosteActual = copy.copy(costes[i])
                    mejorSolActual = copy.copy(L[i])
            tiempo_inicio = time.time()

            #Me quedo con el mejor global
            if mejorCosteActual < mejorCosteGlobal:
                mejorCosteGlobal = copy.copy(mejorCosteActual)
                mejorSolGLobal = copy.copy(mejorSolActual)
                print(f"---> Mejor coste global FINAL: {mejorCosteGlobal} con {evaluaciones} evaluaciones")

            # Actualizo feromonas
            t *= (1 - p)
            for i in range(1, len(mejorSolGLobal)):
                ciudadAnt = int(mejorSolGLobal[i-1])
                ciudad = int(mejorSolGLobal[i])
                t[ciudadAnt, ciudad] += (p/mejorCosteGlobal)
                t[ciudad, ciudadAnt] = copy.copy(t[ciudadAnt, ciudad])

            tiempo_ejecucion = time.time() - start_time



            #Reinicializo
            LnV[0:m] = np.arange(0, tam)
            for i in range(m):
                L[i,1:] = -1
                LnV[i, int(L[i,0])] = -1
            tiempo_ejecucion = abs(time.time() - start_time)
        print(f"Coste FINAL: {mejorCosteGlobal}")
        print(f"Evaluaciones: {evaluaciones}")
        print(f"Solucion: {mejorSolGLobal}")
        fAux.dibujaCamino(mejorSolGLobal, ciudades, "SCH" + str(seed))

def valorGreedy(fichero):
    numpy.random.seed(10)
    ciudades = fAux.leer_Ciudades(fichero)
    tam = len(ciudades)
    D = fAux.matrizDistancias(ciudades=ciudades)
    numeroRandom = np.random.randint(0,tam)
    L = np.ones(shape=(tam+1))
    L *= -1
    L[0] = numeroRandom


    for i in range(1,len(L)):
        L[i] = fAux.nodoMasCercano(D[int(L[i-1])],i-1, L)
    L[-1] = L[0]
    coste = fAux.funcionCoste(L, D)


    return coste

sistemaHormigas()



