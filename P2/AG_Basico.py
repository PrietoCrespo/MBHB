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
    return  poblacion,kmRecorridos

def torneo(kms, k, poblacion):
    candidatos = np.zeros(shape=k)
    indices = list()
    for i in range(k):
        n = random.uniform(0,len(kms)).__int__()
        while indices.__contains__([n]):
            n += 1
            if n > 13:
                n = 0
        indices.append(n)
        candidatos[i] = kms[n]
    km1= np.partition(candidatos,1)[0]

    padre1 = poblacion[np.where(kms == km1)[0][0]]
    #Deberia de seleccionar el mejor padre
    return padre1


def reemplazo(poblacion, kmRecorridos, k, hijos):
    #Reemplazo el peor de la población
    nuevaPoblacion = np.array(poblacion).view()

    vectorOrdenado = np.sort(kmRecorridos, axis=0)
    km1,km2 = vectorOrdenado[-2::]

    indicePeor1 = np.where(kmRecorridos == km1)
    indicePeor2 = np.where(kmRecorridos == km2)

    #Si los hijos son mejores que esos dos, los sustituyo
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
    n = (8 * 0.01 * len(hijo) / 2).__round__()
    operadorMovimiento = 3

    #Tengo que hacer n mutaciones
    for i in range(n):
        hijo = fA.operadorMovimiento_Random(hijo, operadorMovimiento)
    return hijo


def genetico_basico():
    #Cambiar fitness
    semillas = [10, 20, 30]
    kmMinimos= [99999, 99999, 99999]
    mejor_S = np.zeros(shape=(len(semillas), 16))
    nPoblacion = 16
    indCastigo = 5
    t = 0
    #Tamaño del torneo un 30% de la poblacion
    k = (15 * 0.3).__int__()
    #Inicializo población
    for i in range(len(semillas)):
        print(f"Semilla {i}:")
        seed = semillas[i]
        # Establezco la semilla para la serie pseudoaleatoria
        np.random.seed(seed)
        [poblacion, kmRecorridos] = generaPoblacion(nPoblacion)
        NoMejora = 0

        mejorMedia = 9999
        evaluaciones = 0
        while NoMejora < 250:

            #Seleccion por torneo
            padre1 = torneo(kmRecorridos,k,poblacion)
            padre2 = torneo(kmRecorridos,k,poblacion)
            #Cruzo a los padres
            hijo1,hijo2 = cruce(padre1,padre2)
            #Muto a los hijos
            mutado1 = mutacion(hijo1)
            mutado2 = mutacion(hijo2)

            hijos = [mutado1,mutado2]
            #Reemplazo
            kmRecorridos, poblacion = reemplazo(poblacion, kmRecorridos, k, hijos)
            evaluaciones += 2
            MediaKms = sum(kmRecorridos) / len(poblacion)
            if MediaKms >= mejorMedia:
                NoMejora += 1
            else:
                NoMejora = 0
                mejorMedia = MediaKms

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
        print(f"Evaluaciones: {evaluaciones}")
        print(f"Puntos minimo para la semilla {semillas[i]}: {kmRecorridos[indiceMinimo]}")
        kmMinimos[i] = kmRecorridos[indiceMinimo]
    print(f"Mejores km: {kmMinimos}")


def main():
    genetico_basico()

main()