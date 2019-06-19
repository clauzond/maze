from math import *
from tkinter import *
from copy import deepcopy
from time import *

class maze:

    # Comment définir entièrement une case
    def __init__( self,coords,parent=[] ):
        self.coords=coords

    def __repr__(self):
        return("||"+str(self.coords[0])+","+str(self.coords[1])+"||")




    # G est la distance par rapport au point de départ
    # On peut dire que c'est la distance par rapport au parent + 1


    # Distance par rapport à l'arrivée
    # approximation h = x² + y², x et y les droites pour arriver à l'arrivée

    def h(self,fin,ret=1):
        x = abs(self.coords[0] - fin.coords[0])
        y = abs(self.coords[1] - fin.coords[1])

        self.h=x**2 + y**2

        if ret==1:
            return(self.h)


    # f = g + h, approximation de la distance pour atteindre l'arrivée pour une case donnée

    # Actualise directement self.f,self.g,self.h pour pouvoir les manipuler sans calcul
    def fh(self,debut,fin):
        x = abs(self.coords[0] - fin.coords[0])
        y = abs(self.coords[1] - fin.coords[1])
        self.h=x**2 + y**2

        self.f = self.g + self.h





# Chercher l'élément avec le plus petit "F" d'une liste
# Renvoie l'indice de l'élément

# A noter que les F ne sont pas re-calculés, comme l'openlist est censé être calculée déjà
# Possibilité de trier la liste directement selon le critère de F, à voir.
def lowest_F(liste,fin):
    min=liste[0]
    i=0

    for k in range(0,len(liste)):
        if min.f > liste[k].f:
            min=liste[k]
            i=k
    return(i)

# Identique à lowest_F, mais en booléen pour tester si element est le plus petit G
def is_lowest_G(element,liste,fin):

    for k in range(0,len(liste)):
        if element > liste[k].g:
            return(False)
    return(True)


# (*) A ajouter : ne pas faire de "diagonale" si il y a trop d'obstacles autour
def qui_adjacents(x,y,couple_x1y1,couple_x2y2):
    liste=[]
    petitX=min(couple_x1y1[0],couple_x2y2[0])
    grandX=max(couple_x1y1[0],couple_x2y2[0])
    petitY=min(couple_x1y1[1],couple_x2y2[1])
    grandY=max(couple_x1y1[1],couple_x2y2[1])

    if petitX<=(x+1)<=grandX :
        a1=maze([x+1,y])
        liste.append(a1)
    if petitX<=(x+1)<=grandX and petitY<=(y+1)<=grandY:
        a2=maze([x+1,y+1])
        liste.append(a2)
    if petitX<=(x+1)<=grandX and petitY<=(y-1)<=grandY :
        a3=maze([x+1,y-1])
        liste.append(a3)
    if petitX<=(x-1)<=grandX :
        a4=maze([x-1,y])
        liste.append(a4)
    if petitX<=(x-1)<=grandX and petitY<=(y+1)<=grandY :
        a5=maze([x-1,y+1])
        liste.append(a5)
    if petitX<=(x-1)<=grandX and petitY<=(y-1)<=grandY :
        a6=maze([x-1,y-1])
        liste.append(a6)
    if petitY<=(y+1)<=grandY :
        a7=maze([x,y+1])
        liste.append(a7)
    if petitY<=(y-1)<=grandY :
        a8=maze([x,y-1])
        liste.append(a8)
    return(liste)

# Initialise l'algorithme A*

# Contient la boucle principale de l'algo
def start_algo(debut_coords,fin_coords,couple_x1y1,couple_x2y2,obstacles=[],retour=""):
    a=0
    
    fin=maze(fin_coords)
    
    openlist=[]
    openlist_coords=[]
    
    closedlist=[]
    closedlist_coords= deepcopy(obstacles)

    debut=maze(debut_coords)
    debut.g=0
    debut.h(fin,0)
    debut.f=debut.h

    openlist.append(debut)
    openlist_coords.append(debut.coords)
    
    Liste_Fin=[]
    Liste_Fin_F=[]
    
    while a!=1:
        
        # cherche le plus petit F de openlist, l'enlève de openlist, et le met dans closedlist
        indice=lowest_F(openlist,fin)
        current=openlist[indice]
        del openlist[indice]
        del openlist_coords[indice]
        
        closedlist.append(current)
        closedlist_coords.append(current.coords)


        [x,y]=current.coords


        # les 8 carrés autour
        adjacents=qui_adjacents(x,y,couple_x1y1,couple_x2y2)

        
        for square in adjacents:
            # S'il n'est pas dans la closedlist, continue
            if square.coords not in closedlist_coords:
                # S'il n'est pas dans l'openlist, l'ajoute, défini son parent, et calcule fgh
                if square.coords not in openlist_coords:
                    square.g=current.g + int(copysign(1,current.coords[0]-square.coords[0] + current.coords[1] - square.coords[1]))
                    #square.g = current.g + 1
                    square.h=square.h(fin,1)
                    square.f=square.g+square.h
                    
                    openlist.append(square)
                    openlist_coords.append(square.coords)
                    square.parent = current
                    # On définit son G comme le G du parent +1, longueur du chemin de "square" à "debut"
                    
                    
                # Sinon, on regarde si son chemin est meilleur (proche du départ).
                else:
                    # Si son chemin est meilleur, défini son parent et calcule son f,g,h
                    try:
                        if is_lowest_G(square.g,openlist,fin):
                            square.parent=current
                    except:
                        square.g=current.g + int(copysign(1,current.coords[0]-square.coords[0] + current.coords[1] - square.coords[1]))
                        if is_lowest_G(square.g,openlist,fin):
                            square.parent=current

        # Conditions d'arrêts
        if fin.coords in closedlist_coords:
            a=1
            Liste_Fin_F=[closedlist[-1].f]
            Liste_Fin=[closedlist[-1].coords]
            bidule=closedlist[-1]
            while debut.coords not in Liste_Fin:
                Liste_Fin.append( (bidule.parent).coords)
                Liste_Fin_F.append( (bidule.parent).f )
                
                bidule=bidule.parent
                
            Liste_Fin.reverse()
            Liste_Fin_F.reverse()
            if retour=="liste/liste_f":
                return(Liste_Fin,Liste_Fin_F)
            elif retour=="liste_f":
                return(Liste_Fin_F)
            elif retour=="chemin_opti":
                portion_f=portions_effe(Liste_Fin,Liste_Fin_F)
                return(refaire_chemin(portion_f,obstacles,couple_x1y1,couple_x2y2))
            else:
                return(Liste_Fin)
            
        elif openlist==[] or openlist_coords==[]:
            a=1
            return("error")





def labbi(coord1,coord2):
    xmin=min(coord1[0],coord2[0])
    xmax=max(coord1[0],coord2[0])
    ymin=min(coord1[1],coord2[1])
    ymax=max(coord1[1],coord2[1])

    L=[]
    for i in range (xmin,xmax+1):
        for j in range(ymin,ymax+1):
            L+=[[i,j]]
    L=sorted(L, key=lambda x: x[0])
    return(L)

def remove_doublon(nnliste):
    enlever=[]
    liste=nnliste[:]
    for i in range(0,len(liste)):
        if liste[i] in liste[(i+1):]:
            enlever.append(liste[i])
    for elem in enlever:
        liste.remove(elem)
    return(liste)



def creer_mur(coord01,coord02,fat=0):
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
            if fat==0:
                return(L)
            else:
                break

        # Si les 2 se trouvent au même X, on remonte/descend
        # copysign(1,deltaY) renvoie 1 si deltaY>0, et -1 si deltaY<0
        elif deltaX==0:
            coord1 = (coord1[0],coord1[1]+int(copysign(1,deltaY)))
            L.append(list(coord1))

        # Si les 2 se trouvent au même Y, on va à droite/gauche
        elif deltaY==0:
            coord1 = (coord1[0]+int(copysign(1,deltaX)),coord1[1])
            L.append(list(coord1))

        else:
        # Les tours pairs on ajoute "coord1 +/- 1", impairs on ajoute "coord2 +/- 1"
            if compteur_tour%2==0:
                coord1 = (coord1[0] + int(copysign(1,deltaX)),coord1[1] + int(copysign(1,deltaY)))
                compteur_tour+=1
                L.append(list(coord1))

            else:
                coord2 = (coord2[0] + int(copysign(1,-deltaX)),coord2[1] + int(copysign(1,-deltaY)))
                compteur_tour+=1
                L.append(list(coord2))
    if fat!=0:
        
        for i in range(0,len(L)):
            L.append( list( (L[i][0] + 1, L[i][1] + 1) ) )
            L.append( list( (L[i][0] + 1, L[i][1]) ) )
            L.append( list( (L[i][0] , L[i][1] + 1) ) )
            
            
            
            L.append( list( (L[i][0] - 1, L[i][1] - 1) ) )
            L.append( list( (L[i][0] - 1, L[i][1] ) ) )
            L.append( list( (L[i][0] , L[i][1] - 1) ) )
            
            
            L.append( list( (L[i][0] - 1, L[i][1] +1) ) )
            L.append( list( (L[i][0] + 1, L[i][1] - 1) ) )
            
            
            
            
        L=remove_doublon(L)
        L=sorted(L, key=lambda x: x[0])
        return(L)

# Fonction qui détecte les portions où F augmente (dernier "checkpoint" -> dernier "f baisse")
# Il renvoie les portions à changer !
def portions_effe(Liste_Coords,Liste_F):
    Liste_de_listes = []
    Liste_first_indice = []
    i=0
    while i!=(len(Liste_F)-1):
        first_indice=i
        while Liste_F[i+1]>Liste_F[i] :
            i+=1
        # Si l'indice n'a pas changé, pas de changements (on stocke les coordonnées pour les ajouter plus tard)
        if first_indice==i :
            Liste_first_indice.append( first_indice )
        # Si l'indice a bien changé, on rajoute les coordonnées "stockées avant" puis les dernières, ceci constitue une portion, on recommence...
        else:
            L= Liste_first_indice + [k for k in range(first_indice,i + 1)]
            Liste_de_listes.append( L )
            Liste_first_indice=[]
        i+=1
    Liste_de_listes.append((Liste_first_indice)+[len(Liste_F)-1])
    
    final=[]
    for liste in Liste_de_listes :
        final.append( [ Liste_Coords[liste[0]],Liste_Coords[liste[-1]]] )
    
    return(final)

def refaire_chemin(portion_f,obstacles,limite1,limite2):
    new_chemin=[]
    new_chemin_F=[]
    for couples_coords in portion_f:
        (liste_chemin,liste_chemin_f)=start_algo(couples_coords[0],couples_coords[1],limite1,limite2,obstacles,"liste/liste_f")
        new_chemin+=liste_chemin
        new_chemin_F+=liste_chemin_f
    return(new_chemin,new_chemin_F)
        

# Creation de la fenêtre
def start_window(coord1,coord2):
    global grid_window, mainCanvas
    
    grid_window = Toplevel()
    grid_window.title("Pathfinding - A* Algorithm")
    grid_window.aspect(1,1,1,1)
    grid_window.resizable(False, False)
    mainCanvas=Canvas(grid_window,bg="lightgray")
    mainCanvas.pack(fill=BOTH,expand=1)
    
    setup(coord1,coord2)
    
    grid_window.mainloop()
    
    



# Variables à modifier selon les coordonnées de départ




def colorier_liste(liste_coords,coord1,coord2,col_arg="green",debut_coords=[],fin_coords=[]):
    
    for coord0 in liste_coords:
        if coord0 != debut_coords and coord0 != fin_coords:
            window_coord=[(coord0[0] + abs(coord1[0]))*pas , (coord0[1] + abs(coord1[1]))*pas]
            mainCanvas.create_rectangle(window_coord[0],window_coord[1],window_coord[0]+pas,window_coord[1]+pas,fill=col_arg,tag="carre")
    mainCanvas.update()
  
def colorier_case(coord0,coord1,coord2,col_arg="green"):
    #mainCanvas.delete("carre")
    window_coord=[(coord0[0] + abs(coord1[0]))*pas , (coord0[1] + abs(coord1[1]))*pas]
    if not (0<=window_coord[0]<=largeur_bc*pas):
        print("erreur")
    elif not (0<=window_coord[1]<=hauteur_bc*pas):
        print("erreur 2")
    
    mainCanvas.create_rectangle(window_coord[0],window_coord[1],window_coord[0]+pas,window_coord[1]+pas,fill=col_arg,tag="carre")
    mainCanvas.update()

# Clique droit pour remettre la bonne taille de fenêtre
# (*) La fonction qui détermine le pas est minable pour rentrer dans "tout écran"
def setup(coord1,coord2):
    global largeur_bc,hauteur_bc,pas
    largeur_bc = abs(coord2[0] - coord1[0]) + 1
    hauteur_bc = abs(coord2[1] - coord1[1]) + 1
    
    
    # Le pas doit dépendre des hauteurs/largeurs pour rentrer dans l'écran.
    pas=int(600/((hauteur_bc+largeur_bc)/2))
    
    # La taille de la fenêtre, REEL * PAS
    grid_window.geometry('%dx%d' % (largeur_bc*pas, hauteur_bc*pas))
    
    create_grid()
    




def create_grid():
    mainCanvas.delete("ligne")
    
    # On doit pouvoir générer le bon nombre de carré (en ligne, et en colonne)
    # Là, c'est bon !


    # Génération de lignes sur toute la hauteur (haut en bas), avec un pas proportionnel aux coordonnées
    for i in range(0,hauteur_bc*pas,pas):
        mainCanvas.create_line([(0,i), (largeur_bc*pas,i)], tag="ligne")
    
    
    # Génération de lignes sur toute la largeur (gauce à droite), avec un pas proportionnel aux coordonnées
    for i in range(0,largeur_bc*pas,pas):
        mainCanvas.create_line([(i,0), (i,hauteur_bc*pas)], tag="ligne")
    

def BoutonConfirmer():
    global coord1,coord2
    coord1_0=int(coord1_0var.get())
    coord1_1=int(coord1_1var.get())
    coord2_0=int(coord2_0var.get())
    coord2_1=int(coord2_1var.get())
    coord1=[coord1_0,coord1_1]
    coord2=[coord2_0,coord2_1]
    
    start_window([coord1_0,coord1_1],[coord2_0,coord2_1])

def BoutonResoudre():
    mainCanvas.delete("carre")
    
    c1_0=int(c1_0var.get())
    c1_1=int(c1_1var.get())
    c2_0=int(c2_0var.get())
    c2_1=int(c2_1var.get())
    
    c1=[c1_0,c1_1]
    c2=[c2_0,c2_1]
    
    obs1_0=int(obs1_0var.get())
    obs1_1=int(obs1_1var.get())
    obs2_0=int(obs2_0var.get())
    obs2_1=int(obs2_1var.get())
    obs1=[obs1_0,obs1_1]
    obs2=[obs2_0,obs2_1]
    
    obstacl = creer_mur(obs1,obs2,1)
    colorier_liste(obstacl,coord1,coord2,"red")
    colorier_case(c1,coord1,coord2,"green")
    colorier_case(c2,coord1,coord2,"orange")
    
    (Liste_Fin,Liste_Fin_F)=start_algo(c1,c2,coord1,coord2,obstacl,"liste/liste_f")
    
    a=portions_effe(Liste_Fin,Liste_Fin_F)
    (nc,ncf)=refaire_chemin(a,obstacl,coord1,coord2)
    
    b=portions_effe(nc,ncf)
    (nc1,ncf1)=refaire_chemin(b,obstacl,coord1,coord2)
    
    new_chemin=nc1
    
    colorier_liste(new_chemin,coord1,coord2,"yellow",new_chemin[0],new_chemin[-1])

Niveau=Tk()

Niveau.title("Sélection des coordonnées")
Niveau.resizable(width=False,height=False)

canvasniveau=Canvas(Niveau,bg="lightgray")
canvasniveau.grid(row=0,column=0,rowspan=10,columnspan=10)

# Limite 1 coord x
coord1_0var=IntVar()
coord1_0var.set("-10")
ChampCoord1_0=Entry(canvasniveau,textvariable=coord1_0var,font="Constantia 18",width=10)
ChampCoord1_0.grid(row=0,column=0,padx=30,pady=30)

# Limite 1 y
coord1_1var=IntVar()
coord1_1var.set("-10")
ChampCoord1_1=Entry(canvasniveau,textvariable=coord1_1var,font="Constantia 18",width=10)
ChampCoord1_1.grid(row=0,column=1,padx=30,pady=30)

# Limite 2 x
coord2_0var=IntVar()
coord2_0var.set("10")
ChampCoord2_0=Entry(canvasniveau,textvariable=coord2_0var,font="Constantia 18",width=10,bg="gray")
ChampCoord2_0.grid(row=2,column=0,padx=30,pady=30)

# Limite 2 y
coord2_1var=IntVar()
coord2_1var.set("10")
ChampCoord2_1=Entry(canvasniveau,textvariable=coord2_1var,font="Constantia 18",width=10,bg="gray")
ChampCoord2_1.grid(row=2,column=1,padx=30,pady=30)

# Bouton confirmer
Confirm=Button(canvasniveau,text="Confirmer",font="Constantia 15",justify="center",overrelief="groove",activeforeground="blue",activebackground="white",bg="white",command=BoutonConfirmer)
Confirm.grid(row=3,column=0,columnspan=2,padx=10,pady=10)

# Bouton résoudre
Resoudre=Button(canvasniveau,text="Résoudre",font="Constantia 15",justify="center",overrelief="groove",activeforeground="blue",activebackground="white",bg="white",command=BoutonResoudre)
Resoudre.grid(row=6,column=0,rowspan=2,columnspan=2,padx=10,pady=10)


# Début coord x
c1_0var=IntVar()
#c1_0var.set("début 0")
c1_0var.set("-10")
ChampCoord1_0=Entry(canvasniveau,textvariable=c1_0var,font="Constantia 18",width=10,bg="green")
ChampCoord1_0.grid(row=4,column=0,padx=30,pady=30)

# Début coord y
c1_1var=IntVar()
#c1_1var.set("début 1")
c1_1var.set("-10")
ChampCoord1_1=Entry(canvasniveau,textvariable=c1_1var,font="Constantia 18",width=10,bg="green")
ChampCoord1_1.grid(row=4,column=1,padx=30,pady=30)

# Fin coord x
c2_0var=IntVar()
#c2_0var.set("fin 0")
c2_0var.set("10")
ChampCoord2_0=Entry(canvasniveau,textvariable=c2_0var,font="Constantia 18",width=10,bg="orange")
ChampCoord2_0.grid(row=6,column=0,padx=30,pady=30)

# Fin coord y
c2_1var=IntVar()
#c2_1var.set("fin 1")
c2_1var.set("-10")
ChampC2_1=Entry(canvasniveau,textvariable=c2_1var,font="Constantia 18",width=10,bg="orange")
ChampC2_1.grid(row=6,column=1,padx=30,pady=30)

# Obstacle "creer_mur" 
obs1_0var=IntVar()
#obs1_0var.set("obsdeb 0")
obs1_0var.set("2")
ChampCoord1_0=Entry(canvasniveau,textvariable=obs1_0var,font="Constantia 18",width=10,bg="IndianRed1")
ChampCoord1_0.grid(row=7,column=0,padx=30,pady=30)

obs1_1var=IntVar()
#obs1_1var.set("obsdeb 1")
obs1_1var.set("-10")


Champobs1_1=Entry(canvasniveau,textvariable=obs1_1var,font="Constantia 18",width=10,bg="IndianRed1")
Champobs1_1.grid(row=7,column=1,padx=30,pady=30)

obs2_0var=IntVar()
#obs2_0var.set("obsfin 0")
obs2_0var.set("2")

Champobs2_0=Entry(canvasniveau,textvariable=obs2_0var,font="Constantia 18",width=10,bg="IndianRed4")
Champobs2_0.grid(row=8,column=0,padx=30,pady=30)

obs2_1var=IntVar()
#obs2_1var.set("obsfin 1")
obs2_1var.set("0")

Champobs2_1=Entry(canvasniveau,textvariable=obs2_1var,font="Constantia 18",width=10,bg="IndianRed4")
Champobs2_1.grid(row=8,column=1,padx=30,pady=30)


def test_ostacle_bas_fonction(coord1,coord2):
    xmin,ymin=coord1[0],coord1[1]
    xmax,ymax=coord2[0],coord2[1]
    L=labbi(coord1,coord2)
    for k in range (xmin,xmax+1):
        for t in range(ymin,ymax+1):
            if k%2==0 or t%2==0:
                L.remove([k,t])
    return(L)

truc_chelou_lol = creer_mur([1,1],[1,7]) + creer_mur([1,7],[8,7])+creer_mur([8,7],[8,1])



Niveau.mainloop()