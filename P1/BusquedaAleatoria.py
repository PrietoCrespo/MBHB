import funcionesAux as fA
import numpy as np
import time



def Busqueda_Aleatoria(iteraciones):
    print("Busqueda aleatoria: \n")

    semillas = [10,20,30,40,50]
    kmRecorridos = [99999,99999,99999,99999,99999]

    #mejor_S = [[0for x in range(16)] for y in range(5)]
    mejor_S = np.zeros(shape=(5,16))

    for j in range(len(semillas)):
        print("Semilla "+j.__str__())
        seed = semillas[j]
        #Establezco la semilla para la serie pseudoaleatoria
        np.random.seed(seed)
        for i in range(iteraciones):
            vSlots = fA.solucionAleatoria()
            kmR = fA.evalua(vSlots)
            #Si los kms recorridos son menores que los actuales se actualiza
            if(kmR < kmRecorridos[j]):
                kmRecorridos[j] = kmR
                mejor_S[:][j] = vSlots

    print("Mejor S1: "+mejor_S[:][0].__str__())
    print("Mejor S2: " + mejor_S[:][1].__str__())
    print("Mejor S3: " + mejor_S[:][2].__str__())
    print("Mejor S4: " + mejor_S[:][3].__str__())
    print("Mejor S5: " + mejor_S[:][0].__str__())
    print("Km recorridos: "+kmRecorridos.__str__())
    print("Media kms : " + (sum(kmRecorridos) / 5).__str__())

def main():
    iteraciones = [100,200,500,1000,2000]
    for i in iteraciones:
        print("Iteraciones: "+i.__str__())
        start_time = time.time()
        print(Busqueda_Aleatoria(i))
        print("\n\n---->Segundos ejecucion: "+ (time.time() - start_time).__str__())
main()
