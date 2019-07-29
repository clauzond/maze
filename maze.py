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
    # Racine carré pas obligatoire, mais ça me rassure un peu
 
    def h(self,fin,ret=1):
        x = abs(self.coords[0] - fin.coords[0])
        y = abs(self.coords[1] - fin.coords[1])
 
        self.h=sqrt(x**2 + y**2)
 
        if ret==1:
            return(self.h)
 
 
    # f = g + h, approximation de la distance pour atteindre l'arrivée pour une case donnée
    # Racine carré pas obligatoire, mais ça me rassure un peu
 
    # Actualise directement self.f,self.h pour pouvoir les manipuler sans calcul
    def fh(self,debut,fin):
        x = abs(self.coords[0] - fin.coords[0])
        y = abs(self.coords[1] - fin.coords[1])
        self.h=sqrt(x**2 + y**2)
 
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
def qui_adjacents(x,y,couple_x1y1,couple_x2y2,obstacles):
    liste=[]
    petitX=min(couple_x1y1[0],couple_x2y2[0])
    grandX=max(couple_x1y1[0],couple_x2y2[0])
    petitY=min(couple_x1y1[1],couple_x2y2[1])
    grandY=max(couple_x1y1[1],couple_x2y2[1])
 
    if petitX<=(x+1)<=grandX :
        a1=maze([x+1,y])
        liste.append(a1)
    if petitX<=(x+1)<=grandX and petitY<=(y+1)<=grandY:
        if ([x+1,y] not in obstacles) and ([x,y+1] not in obstacles):
            a2=maze([x+1,y+1])
            liste.append(a2)
    if petitX<=(x+1)<=grandX and petitY<=(y-1)<=grandY :
        if ([x,y-1] not in obstacles) and ([x+1,y] not in obstacles):
            a3=maze([x+1,y-1])
            liste.append(a3)
    if petitX<=(x-1)<=grandX :
        a4=maze([x-1,y])
        liste.append(a4)
    if petitX<=(x-1)<=grandX and petitY<=(y+1)<=grandY :
        if ([x,y+1] not in obstacles) and ([x-1,y] not in obstacles):
            a5=maze([x-1,y+1])
            liste.append(a5)
    if petitX<=(x-1)<=grandX and petitY<=(y-1)<=grandY :
        if ([x,y-1] not in obstacles) and ([x-1,y] not in obstacles):
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
        adjacents=qui_adjacents(x,y,couple_x1y1,couple_x2y2,obstacles)
 
       
        for square in adjacents:
            # S'il n'est pas dans la closedlist, continue
            if square.coords not in closedlist_coords:
                # S'il n'est pas dans l'openlist, l'ajoute, défini son parent, et calcule F G et H
                if square.coords not in openlist_coords:
                    # On définit son G comme le G du parent +1
                    square.g = current.g + 1
                    # On calcule F et H 
                    square.fh(debut,fin)
                   
                    openlist.append(square)
                    openlist_coords.append(square.coords)
                    square.parent = current
                   
                   
                # Sinon, on regarde si son chemin est meilleur (proche du départ).
                else:
                    # Si son chemin est meilleur, défini son parent et recalcule son f,g,h si ce n'est pas déjà fait
                    square.g = current.g + 1
                    square.fh(debut,fin)
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
                N=len(Liste_Fin)
                portion_f=portions_effe(Liste_Fin,Liste_Fin_F)
                chemin_opti=refaire_chemin(portion_f,obstacles,couple_x1y1,couple_x2y2)[0]
                N_opti=len(chemin_opti)
                
                if N<N_opti:
                    print("chemin opti plus long")
                if N>N_opti:
                    print("chemin opti plus long")
                
                return(chemin_opti)
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
   
   
 
 
 

# Itération sur une liste de la fonction "colorier_case"
def colorier_liste(liste_coords,coord1,coord2,col_arg="green",debut_coords=[],fin_coords=[]):
    for coord0 in liste_coords:
        if coord0 != debut_coords and coord0 != fin_coords:
            window_coord=[(coord0[0] + abs(coord1[0]))*pas , (coord0[1] + abs(coord1[1]))*pas]
            mainCanvas.create_rectangle(window_coord[0],window_coord[1],window_coord[0]+pas,window_coord[1]+pas,fill=col_arg,tag="carre")
    mainCanvas.update()
 
# coord0 correspond à la case à colorier
# coord1 correspond à la limite "haut gauche" de la fenêtre
# coord2 correspond à la limite "bas droite" de la fenêtre (pas nécessaire, car si on sort de l'écran alors colorier revient à ne rien faire)
def colorier_case(coord0,coord1,coord2,col_arg="green"):
    window_coord=[(coord0[0] + abs(coord1[0]))*pas , (coord0[1] + abs(coord1[1]))*pas]
   
    mainCanvas.create_rectangle(window_coord[0],window_coord[1],window_coord[0]+pas,window_coord[1]+pas,fill=col_arg,tag="carre")
    mainCanvas.update()
 
 
# Fonction qui initialise le pas, la largeur et hauteur de nos intervalles
# (*) La fonction ne détermine pas la taille de l'écran de l'utilisateur
def setup(coord1,coord2):
    global largeur_bc,hauteur_bc,pas
    largeur_bc = abs(coord2[0] - coord1[0]) + 1
    hauteur_bc = abs(coord2[1] - coord1[1]) + 1
   
   
    # Le pas doit dépendre des hauteurs/largeurs pour rentrer dans l'écran.
    # Le chiffre avant division correspond à la plus petite dimension de l'écran.
    # Exemple : si je suis en 1920*1080, je dois mettre 1080
    pas=int(600/((hauteur_bc+largeur_bc)/2))
   
    # La taille de la fenêtre, REEL * PAS
    grid_window.geometry('%dx%d' % (largeur_bc*pas, hauteur_bc*pas))
   
    create_grid()
   
 
 
 
 
def create_grid():
    mainCanvas.delete("ligne")
   
    # On doit pouvoir générer le bon nombre de carré (en ligne, et en colonne)
 
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
    # coord1 = limites fenêtre
    coord2=[coord2_0,coord2_1]
    # coord2 = 2 eme limite fenetre
    start_window([coord1_0,coord1_1],[coord2_0,coord2_1])
 
def BoutonResoudre():
    mainCanvas.delete("carre")
   
    c1_0=int(c1_0var.get())
    c1_1=int(c1_1var.get())
    c2_0=int(c2_0var.get())
    c2_1=int(c2_1var.get())
   
    c1=[c1_0,c1_1]
    # c1 = départ
    c2=[c2_0,c2_1]
    # c2 = arrivée
   
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
   
    chemin_opti=start_algo(c1,c2,coord1,coord2,obstacl,"chemin_opti")
    
    points_clefs_x,points_clefs_y=Chemin_into_points_clefs(chemin_opti)
    liste_couple_points_clefs=convert_x_and_y_into_xy(points_clefs_x,points_clefs_y)
    #print("Points clefs",liste_couple_points_clefs)
    
    
    colorier_liste(chemin_opti,coord1,coord2,"yellow",chemin_opti[0],chemin_opti[-1])

    colorier_liste(liste_couple_points_clefs,coord1,coord2,"blue")
    

    
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
 
 
def test_obstacle_bas_fonction(coord1,coord2):
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
 
##tracer courbe bézier
 
#fonction qui regarde sur deux coordonnés s'ils sont adjacents ou pas, renvoie un boléen
def est_adjacent(x,y):
    if x[0] == y[0] + 1 or x[0] == y [0] -1 or x[0]==y[0]:
        if x[1] == y[1] + 1 or x[1] == y[1] -1 or x[1]==y[1]:
            return(True)
        else:
            return(False)
    else:
        return(False)
    return(False)
 
#focntion qui détecte les portions qui touchent les obstacles
 
def portion_adjacente(Listcoord,obstacle):
    L=[]
    for i in range(0,len(Listcoord)):
        I=[]
        for j in range(0,len(obstacle)):
            if est_adjacent(Listcoord[i], obstacle[j]):
                a=Listcoord[i]
                if a not in I:
                    I.append(a)
        L+=I
    return(L)
import numpy
import scipy.interpolate
import akima
from scipy.interpolate import Akima1DInterpolator,CubicSpline
from scipy.interpolate import interp1d
from matplotlib import pyplot

def example(x,y):
    '''Plot interpolated Gaussian noise.'''
    #x = numpy.sort(numpy.random.random(10) * 100)
    #y = numpy.random.normal(0.0, 10, size=len(x))
    x2 = numpy.linspace(x[0],x[-1], 1000)
    f2 = Akima1DInterpolator(x, y)
    f3 = interp1d(x,y)
    #f4 = CubicSpline(x,y)
    print(f2(x2))
    pyplot.title('Akima interpolation of Gaussian noise')
    pyplot.plot(x2, f2(x2), 'r-', label='akima')
    pyplot.plot(x2, f3(x2), 'b:', label='scipy', linewidth=2.5)
    #pyplot.plot(x2, f4(x2), 'g:', label='cubicspline', linewidth=2.5)
    pyplot.plot(x, y, 'bo', label='data')
    pyplot.legend()
    pyplot.show()
    
def convert_xy_into_x_and_y(L):
    x=[]
    y=[]
    for i in range(0,len(L)):
        if i!=0 and L[i][0]==L[i-1][0]:
            x+=[x[i-1]]
            y+=[L[i][1]]
            None
        else:
            x+=[L[i][0]]
            y+=[L[i][1]]
    return(x,y)
    
# Transforme deux listes [x0,x1..] et [y0,y1,...] en [ [x0,y0] , ... ]
def convert_x_and_y_into_xy(L1,L2):
    liste_couples=[]
    for i in range(0,len(L1)):
        liste_couples.append([L1[i],L2[i]])
    return(liste_couples)
            

L_chemin=[[-10, -10], [-9, -9], [-8, -8], [-7, -7], [-6, -6], [-5, -5], [-4, -4], [-3, -3], [-2, -2], [-1, -1], [0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [3, 2], [4, 2], [5, 1], [6, 0], [7, -1], [8, -2], [9, -3], [10, -4], [10, -5], [10, -6], [10, -7], [10, -8], [10, -9], [10, -10]]
(x,y)=convert_xy_into_x_and_y(L_chemin)
0,9,12,16,22,-1
Lx=[x[0],x[9],x[12],x[16],x[-1]]
Ly=[y[0],y[9],y[12],y[16],y[-1]]

# Fonction qui :
# enlève les lignes droites (en laisant début/fin)
# enlève identité
# enlève les x successifs (ne prend que le premier, et celui après le dernier)
#est censé marché car dans le cas contraire on se trouve dans le cas où il yt a plein d'obstacle et donc ou c'est bien droit


# Tentative de "points clefs" pour tracer un Akima spline
def Chemin_into_points_clefs(L):
    x=[L[0][0]]
    y=[L[0][1]]
    x_portion=[]
    y_portion=[]
    variable= 0
    for i in range(1,len(L)):
        if L[i][0]==L[i-1][0]+1 and L[i][1]==L[i-1][1]+1:
            if variable == 0 or variable == 1: 
                variable=1
            else :
                x+=[L[i-1][0]]
                y+=[L[i-1][1]]
                variable = 1
            
        elif L[i][0]==L[i-1][0]-1 or L[i][1]==L[i-1][1]-1:
            if variable == 2:
                variable = 2
            else :
                x+=[L[i-1][0]]
                y+=[L[i-1][1]]
                variable = 2
        elif L[i][0] == L[i-1][0] :
            if variable == 3:
                variable = 3
            else :
                x+=[L[i-1][0]]
                y+=[L[i-1][1]]
                variable = 3
        elif  L[i][1]==L[i-1][1]:
            if variable == 5:
                variable = 5
            else :
                x+=[L[i-1][0]]
                y+=[L[i-1][1]]
                variable = 5
        else:
            if variable == 4:
                variable = 4
            else :
                x+=[L[i-1][0]]
                y+=[L[i-1][1]]
                variable = 4
    return((x+[L[-1][0]],y+[L[-1][1]]))
            


#x = numpy.sort(numpy.random.random(10) * 100)
#y = numpy.random.normal(0.0, 10, size=len(x))
#x2 = numpy.arange(x[0], x[-1], 0.01)

# import matplotlib.pyplot as plt
# from scipy.interpolate import splev, splrep
# x = np.linspace(0, 10, 10)
# y = np.sin(x)
# spl = splrep(x, y)
# x2 = np.linspace(0, 10, 200)
# y2 = splev(x2, spl)
# plt.plot(x, y, 'o', x2, y2)
# plt.show()