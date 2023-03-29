import funcionesAux as fA

#Ejecucion Greedy
def main():
    ocupados = fA.primer_movimiento
    greedy = fA.slotsGreedy(ocupados)
    print(greedy)
    print(sum(greedy))
    kmR = fA.evalua(greedy)
    print(kmR)

main()