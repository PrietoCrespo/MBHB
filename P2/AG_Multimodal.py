import random
import numpy as np
import funcionesAux as fA

#Modelo estacionario

def generaPoblacion(numero):
    poblacion = np.zeros(shape=(numero, 16))
    kmRecorridos = np.zeros(shape=(numero))

    for i in range(numero-1):
        poblacion[i][:] = fA.solucionAleatoria()
        kmRecorridos[i] = fA.evaluaGenetico(poblacion[i][:])

    poblacion[-1][:] = fA.slotsGreedy(fA.primer_movimiento)
    kmRecorridos[-1] = fA.evaluaGenetico(poblacion[-1])
    #print(f"Genero poblacion y me sale: {kmRecorridos}")
    return  poblacion,kmRecorridos

def ordenaPoblacion(poblacionOrdenable,kmRecorridosOrdenables):
    indicesOrdenados = np.argsort(kmRecorridosOrdenables)

    poblacion = np.zeros(poblacionOrdenable.shape)
    kmRecorridos = np.zeros(shape=len(poblacionOrdenable))

    for i in range(len(indicesOrdenados)):
        poblacion[i] = poblacionOrdenable[indicesOrdenados[i]]
        kmRecorridos[i] = kmRecorridosOrdenables[indicesOrdenados[i]]

    return poblacion,kmRecorridos

def seleccion(poblacion,kmRecorridos, distanciaMinima):
    poblacion = np.array(poblacion).view()
    kmRecorridos = np.array(kmRecorridos).view()
    seleccionados = list()
    seleccionadosKm = list()
    #Ordeno
    poblacion,kmRecorridos = ordenaPoblacion(poblacion,kmRecorridos)

    indiceAux = 1
    individuoAux = poblacion[indiceAux]
    kmsAux = kmRecorridos[indiceAux]

    final = False
    while not final:
        seleccionados.append(poblacion[0])
        seleccionadosKm.append(kmRecorridos[0])
        #Lo guardo y comparo con el resto
        aux = list()
        auxKm = list()

        for i in range(len(poblacion)):
            distancia = distanciaHamming(seleccionados[-1],poblacion[i])
            if sum(distancia) > distanciaMinima:
                aux.append(poblacion[i])
                auxKm.append(kmRecorridos[i])
        if len(aux) > 0:
            poblacion = aux
            kmRecorridos = auxKm
        else:
            final = True

    #Para que, en caso de solo haber un individuo, guardo el segundo mejor
    if len(seleccionados) == 1:
        seleccionados.append(individuoAux)
        seleccionadosKm.append(kmsAux)
    return seleccionados, seleccionadosKm

def torneo(kms, k, poblacion):
    candidatos = np.zeros(shape=k)
    indices = list()
    if len(poblacion) > 2:
        for i in range(k):
            n = random.uniform(0,len(kms)).__int__()
            while indices.__contains__([n]):
                n += 1
                if n > 13:
                    n = 0
            indices.append(n)
            candidatos[i] = kms[n]
        km1,km2 = np.partition(candidatos,1)[0:2]
        padre1 = poblacion[np.where(kms == km1)[0][0]]
        padre2 = poblacion[np.where(kms == km2)[0][0]]
    else:
        padre1 = poblacion[0]
        padre2 = poblacion[1]

    #Deberia de seleccionar los dos mejores, digamos que son los dos primeros
    return padre1, padre2

def reemplazo(poblacion, kmRecorridos, k, hijos):
    #Reemplazo el peor de la población
    nuevaPoblacion = np.array(poblacion).view()

    vectorOrdenado = np.sort(kmRecorridos, axis=0)
    km1,km2 = vectorOrdenado[-2::]

    indicePeor1 = np.where(kmRecorridos == km1)
    indicePeor2 = np.where(kmRecorridos == km2)

    #Si los hijos son mejores que esos dos, los sustituyo
    if sum(hijos[0]) > 205:
        kmsHijo0 = fA.evaluaGenetico(hijos[0])
        if kmsHijo0 < km1:
            #Es mejor que el menos malo
            km1 = kmsHijo0
            nuevaPoblacion[indicePeor1] = hijos[0]
            kmRecorridos[indicePeor1] = kmsHijo0
        elif kmsHijo0 < km2:
            km2 = kmsHijo0
            nuevaPoblacion[indicePeor2] = hijos[0]
            kmRecorridos[indicePeor2] = kmsHijo0

    if sum(hijos[1]) > 205:
        kmsHijo1 = fA.evaluaGenetico(hijos[1])
        if kmsHijo1 < km1:
            #Comprobar si he quitao al hijo 1, y ver si pal segundo se puede
            km1 = kmsHijo1
            nuevaPoblacion[indicePeor1] = hijos[1]
            kmRecorridos[indicePeor1] = kmsHijo1
        elif kmsHijo1 < km2:
            km2 = kmsHijo1
            nuevaPoblacion[indicePeor2] = hijos[1]
            kmRecorridos[indicePeor2] = kmsHijo1

    return kmRecorridos, nuevaPoblacion

def cruce(padre1,padre2):


    puntos = np.random.choice(2, 16)
    hijo1 = np.zeros(shape=16)
    hijo2 = np.zeros(shape=16)

    hijo1 = np.array(padre1).view()
    hijo1[puntos] = padre2[puntos]

    hijo2 = np.array(padre2).view()
    hijo2[puntos] = padre1[puntos]

    return hijo1,hijo2

def mutacion(hijo):
    n = (15 * 0.01 * len(hijo) / 2).__round__()
    operadorMovimiento = 3

    #Tengo que hacer n mutaciones
    for i in range(n):
        hijo = fA.operadorMovimiento_Random(hijo, operadorMovimiento)
    return hijo

def elite(poblacion, kms):
    elite = list()
    km1,km2 = np.partition(kms,1)[0:2]

    mejor1 = poblacion[np.where(kms == km1)[0][0]]
    mejor2 = poblacion[np.where(kms == km2)[0][0]]

    return mejor1, mejor2

def distanciaHamming(vector1, vector2): #Devuelve donde los indices son diferentes señalados por un 1
    vectorDiferencia = np.abs(vector1 - vector2)
    vectorDiferencia[vectorDiferencia> 0] = 1

    return vectorDiferencia

def genetico_basico():
    #Cambiar fitness
    semillas = [10, 20, 30]
    kmMinimos= [99999, 99999, 99999]
    mejor_S = np.zeros(shape=(len(semillas), 16))
    nPoblacion = 16
    t = 0
    #Tamaño del torneo un 30% de la poblacion
    k = (15 * 0.3).__int__()
    clearing = False
    p = 15 #Para el clearing

    valorClearing = ((10 * (nPoblacion))/ 2).__int__()

    dMinima = 2

    #Inicializo población
    for i in range(len(semillas)):
        print(f"Semilla {i}:")
        seed = semillas[i]
        # Establezco la semilla para la serie pseudoaleatoria
        np.random.seed(seed)
        [poblacion, kmRecorridos] = generaPoblacion(nPoblacion)
        NoMejora = 0
        indCastigo = 5
        iteraciones = 0


        evaluaciones = 0
        mejorMedia = 99999
        while NoMejora < 250 :

            MediaKmsAnt = sum(kmRecorridos) / len(poblacion)
            #Clearing
            if (iteraciones == valorClearing):
                poblacion,kmRecorridos = seleccion(poblacion,kmRecorridos, dMinima)
                iteraciones = 1


            #Seleccion por torneo
            padre1, padre2 = torneo(kmRecorridos,k,poblacion)
            #Cruzo a los padres
            hijo1,hijo2 = cruce(padre1,padre2)
            #Muto a los hijos
            mutado1 = mutacion(hijo1)
            mutado2 = mutacion(hijo2)

            hijos = [mutado1,mutado2]

            #Solo reemplazo si la población está llena
            if len(poblacion) < (nPoblacion):
                poblacion = list(poblacion)
                kmRecorridos = list(kmRecorridos)

                kmsHijo1 = fA.evaluaGenetico(mutado1)
                kmsHijo2 = fA.evaluaGenetico(mutado2)

                if len(poblacion) == (nPoblacion - 1): #Si solo cabe uno
                    #Meto al mejor de los dos hijos
                    if kmsHijo1 < kmsHijo2:
                        poblacion.append(mutado1)
                        kmRecorridos.append(kmsHijo1)
                    else:
                        poblacion.append(mutado2)
                        kmRecorridos.append(kmsHijo2)
                else:
                    #Añado los hijos a la poblacion
                    poblacion.append(mutado1)
                    poblacion.append(mutado2)

                    kmRecorridos.append(kmsHijo1)
                    kmRecorridos.append(kmsHijo2)

                #Los devuelvo a np.array
                kmRecorridos = np.array(kmRecorridos)
                poblacion = np.array(poblacion)
            else:
                #Reemplazo
                kmRecorridos, poblacion = reemplazo(poblacion, kmRecorridos, k, hijos)
            evaluaciones += 2

            MediaKms = sum(kmRecorridos)/len(poblacion)
            if MediaKms >= mejorMedia:
                NoMejora += 1
            else:
                NoMejora = 0
                mejorMedia = MediaKms
            iteraciones += 1
        poblacion,kmRecorridos = seleccion(poblacion,kmRecorridos,dMinima)

        indiceMinimo = np.argmin(kmRecorridos)


        Kms = np.zeros(len(poblacion))
        for j in range(len(poblacion)):
            capacidadVector = sum(poblacion[j])
            if capacidadVector > 205:
                Kms[j] = kmRecorridos[j] - (capacidadVector - 205) * indCastigo
            else:
                Kms[j] = kmRecorridos[j]





        for j in range(len(poblacion)):
            print(f"[{j}] {poblacion[j]} Puntos: {kmRecorridos[j]} Kms: {Kms[j]}  Capacidad: {sum(poblacion[j])}")
        print(f"Puntos minimo para la semilla {semillas[i]}: {kmRecorridos[indiceMinimo]}")
        print(f"Evaluaciones: {evaluaciones}")
        kmMinimos[i] = kmRecorridos[indiceMinimo]
    print(f"Mejores puntos: {kmMinimos}")


def main():
    genetico_basico()
main()