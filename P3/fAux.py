import numpy as np
import math
import copy
import matplotlib.pyplot as plt


def leer_Ciudades(nombreFichero):
    infile = open(nombreFichero, 'r')

    name = infile.readline().strip().split()[1]
    fileType = infile.readline().strip().split()[1]
    comment = infile.readline().strip().split()[1]
    dimension = infile.readline().strip().split()[1]
    edgeWeightType = infile.readline().strip().split()[1]
    infile.readline()

    #Leo lista ciudades
    ciudades = []
    n = int(dimension)

    for i in range(n):
        x,y = infile.readline().strip().split()[1:]
        ciudades.append([float(x), float(y)])

    return ciudades

def nodoMasCercano(D, ciudad, L):
    mDistancia = copy.copy(D)
    ciudadesVisitadas = L[L!=-1]

    for city in ciudadesVisitadas:
        mDistancia[int(city)] += 999
    mDistancia[mDistancia < 1] += 999

    return np.argmin(mDistancia)



def actFeromona(valorFeromona, ciudad1, ciudad2,L, costes, p):
    primerSumando = (1 - p) * valorFeromona

    segundoSumando = 0
    for i in range(len(costes)):
        #Hormiga i
        existeCiudad1 = sum(L[i] == ciudad1)
        existeCiudad2 = sum(L[i] == ciudad2)
        if existeCiudad1 > 0 and existeCiudad2 > 0 and L[i,ciudad1+1] == ciudad2:
            segundoSumando += 1/costes[i]

    return (primerSumando + segundoSumando)

def actFeromonaGlobal(valorFeromona, L, mejorGlobal, p):
    primerSumando = (1 - p) * valorFeromona

    segundoSumando = p * (1 / mejorGlobal)

    return (primerSumando + segundoSumando)


def actFeromonaElitista(valorFeromona, ciudad1, ciudad2,L, costes, p, e, mejor):
    primerSumando = (1 - p) * valorFeromona

    segundoSumando = 0
    for i in range(len(costes)):
        #Hormiga i
        existeCiudad1 = sum(L[i] == ciudad1)
        existeCiudad2 = sum(L[i] == ciudad2)
        if existeCiudad1 > 0 and existeCiudad2 > 0 and L[i,ciudad1+1] == ciudad2:
            segundoSumando += 1/costes[i]

    tercerSumando = e*mejor
    return (primerSumando + segundoSumando + tercerSumando)

def funcionCoste(L, D):
    costeT = 0
    for i in range(len(L)-1):
        suma = D[int(L[i]),int(L[i+1])]
        costeT += suma
    return costeT

def reglaTransicion(L,ciudad, ciudades, t, matrizHeuristica, alpha, beta, LnV):
    #L: lista de ciudades recorridas
    #ciudad: en que ciudad estoy
    #ciudades: lista ciudades
    #t: array feromonas

    ciudadesNoVisitadas = np.array(LnV[LnV != -1])
    tam = len(L)
    probabilidades = np.zeros(shape=tam)
    numerador = np.zeros(shape=len(ciudadesNoVisitadas))

    denominador = 0
    for j in range(len(ciudadesNoVisitadas)):
        denominador += (t[ciudad, int(ciudadesNoVisitadas[j])]) ** alpha * (matrizHeuristica[ciudad, int(ciudadesNoVisitadas[j])]) ** beta
        numerador[j] = (t[ciudad, int(ciudadesNoVisitadas[j])]) ** alpha * (matrizHeuristica[ciudad, int(ciudadesNoVisitadas[j])]) ** beta

    probabilidades = numerador[:] / denominador

    indice = eligeProbabilidad(probabilidades)

    return int(ciudadesNoVisitadas[indice])

def eligeProbabilidad(arrayProbabilidades):
    uniforme = np.random.random()
    condition = False

    indice = i = 0
    while not condition:
        if arrayProbabilidades[i] < uniforme:
            arrayProbabilidades[i+1] += arrayProbabilidades[i]
            i += 1
        else:
            condition = True
            indice = i

    return indice

def reglaTransicionColonia(L,ciudad, ciudades, t, matrizHeuristica, alpha, beta, q0, LnV):
    #L: lista de ciudades recorridas
    #ciudad: en que ciudad estoy
    #ciudades: lista ciudades
    #t: array feromonas

    ciudadesNoVisitadas = np.array(LnV[LnV != -1])
    tam = len(ciudadesNoVisitadas)
    valores = np.zeros(shape=tam)

    for j in range(len(ciudadesNoVisitadas)):
        factor1 = (t[ciudad, int(ciudadesNoVisitadas[j])]) ** alpha
        factor2 = (matrizHeuristica[ciudad, int(ciudadesNoVisitadas[j])]) ** beta
        valores[j] = factor1 * factor2
    ciudadDevuelta = ciudadesNoVisitadas[np.argmax(valores)]

    return int(ciudadDevuelta)

def matrizHeuristica(matrizDistancia):
    #La copio para que sea por valor
    nH = copy.copy(matrizDistancia)
    #Pongo los 0 a -1, de forma que no me de indeterminación
    nH[np.where(nH == 0)] = -1
    #Divido por 1 para convertirla en la matriz heuristica
    nH = np.divide(1, nH)

    return nH

def matrizDistancias(ciudades):
    tam = len(ciudades)
    print(tam)
    D = np.zeros(shape=(tam, tam))

    for i in range(tam):
        for j in range(tam):
            D[i,j] = int(distancia(ciudades[i],ciudades[j]))
    return D

def distancia(nodo1, nodo2):
    x = nodo1[0] - nodo2[0]
    y = nodo1[1] - nodo2[1]
    distancia = float(math.sqrt(x**2 + y**2))

    return distancia

def dibujaCamino(camino, ciudades, nombre):

    x = np.zeros(shape=len(ciudades))
    y = np.zeros(shape=len(ciudades))

    for ciudad in range(len(ciudades)):
        x[ciudad] = ciudades[ciudad][0]
        y[ciudad] = ciudades[ciudad][1]

    plt.scatter(x, y)
    for i in range(len(camino)-1):
        Punto1 = (x[int(camino[i])],x[int(camino[i + 1])] )
        Punto2 = (y[int(camino[i])], y[int(camino[i + 1])])
        plt.plot( Punto1, Punto2, color='black')
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(nombre)
    plt.show()