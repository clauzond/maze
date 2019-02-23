from math import *
#from copy import deepcopy



def remove_doublon(nnliste):
    enlever=[]
    liste=nnliste[:]
    for i in range(0,len(liste)):
        if liste[i] in liste[(i+1):]:
            enlever.append(liste[i])
    for elem in enlever:
        liste.remove(elem)
    return(liste)



def creer_mur(coord01,coord02):
    L=[coord01]
    coord1=coord01[:]
    coord2=coord02[:]

    compteur_tour=0

    while True:
        #deltaX = X2 - X1
        #deltaY = Y2 - Y1
        deltaX=coord2[0] - coord1[0]
        deltaY=coord2[1] - coord1[1]

        # Le cas deltaX==0 et deltaY==0 est pris en compte ici, ça veut dire coord1 = coord2
        # C'est pour éviter avec la méthode pair/impair de ne pas finir la boucle, on va arriver à un milieu
        if coord02 in L or (deltaX==0 and deltaY==0):
            if coord02 not in L:
                L.append(coord02)
            L=remove_doublon(L)
            L=sorted(L, key=lambda x: x[0])
            #L.sort()
            return(L)

        # Si les 2 se trouvent au même X, on remonte/descend
        # copysign(1,deltaY) renvoie 1 si deltaY>0, et -1 si deltaY<0
        elif deltaX==0:
            #coord1[1] += int(copysign(1,deltaY))
            coord1 = (coord1[0],coord1[1]+int(copysign(1,deltaY)))
            L.append(list(coord1))

        # Si les 2 se trouvent au même Y, on va à droite/gauche
        elif deltaY==0:
            #coord1[0] += int(copysign(1,deltaX))
            coord1 = (coord1[0]+int(copysign(1,deltaX)),coord1[1])
            L.append(list(coord1))

        else:
        # Les tours pairs on ajoute "coord1 +/- 1", impairs on ajoute "coord2 +/- 1"
            # coord1[0] + sg(deltaX) /// coord1[1] + sg(deltaY)
            if compteur_tour%2==0:
                coord1 = (coord1[0] + int(copysign(1,deltaX)),coord1[1] + int(copysign(1,deltaY)))
                compteur_tour+=1
                L.append(list(coord1))

            # coord2[0] + sg(-deltaX) /// coord2[1] + sg(-deltaY)
            else:
                coord2 = (coord2[0] + int(copysign(1,-deltaX)),coord2[1] + int(copysign(1,-deltaY)))
                compteur_tour+=1
                L.append(list(coord2))

print(creer_mur([0,0],[10000,10000]))
